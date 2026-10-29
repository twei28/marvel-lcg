// Dessiner une carte complete : calques + illustration (rendu.js), puis les textes et les nombres, un par element du gabarit.
//
// Le gabarit (`types.json`) donne, pour chaque element, sa boite SANS rotation, sa propre transformation et son origine ; on
// recompose la chaine de transformations de ses parents (comme CSS) puis on dessine dans la boite locale.
import { PORTRAIT, chargerImage, dessinerCalques, teteVisible } from './rendu.js'
import { dessinerNiveau } from './libres.js'
import { analyser, dessinerPage, mettreEnPage } from './texte.js'

/**
 * Le libelle du type est CUIT dans l'image du calque (en anglais) : pour une autre langue (ou un libelle libre) on le recouvre avec la
 * couleur du fond puis on redessine le texte. Les libelles anglais servent a mesurer la zone a recouvrir.
 */
export const LIBELLES = {
  en: {
    ally: 'ALLY', event: 'EVENT', upgrade: 'UPGRADE', support: 'SUPPORT', resource: 'RESOURCE', villain: 'VILLAIN', minion: 'MINION',
    treachery: 'TREACHERY', environment: 'ENVIRONMENT', attachment: 'ATTACHMENT', sidescheme: 'SIDE SCHEME', playersidescheme: 'PLAYER SIDE SCHEME',
    main_scheme_a: 'MAIN SCHEME', main_scheme_b: 'MAIN SCHEME', 'alter-ego': 'ALTER-EGO', 'alter-ego-promo': 'ALTER-EGO', identity: 'HERO',
    'identity-promo': 'HERO', obligation: 'OBLIGATION', 'obligation-villain': 'OBLIGATION', 'generic-promo': 'ALLY', 'generic-promo-vert': 'ALLY',
  },
  fr: {
    ally: 'ALLIÉ', event: 'ÉVÉNEMENT', upgrade: 'AMÉLIORATION', support: 'SOUTIEN', resource: 'RESSOURCE', villain: 'MÉCHANT', minion: 'SBIRE',
    treachery: 'TRAHISON', environment: 'ENVIRONNEMENT', attachment: 'ATTACHEMENT', sidescheme: 'MANIGANCE ANNEXE', playersidescheme: 'MANIGANCE ANNEXE',
    main_scheme_a: 'MANIGANCE PRINCIPALE', main_scheme_b: 'MANIGANCE PRINCIPALE', 'alter-ego': 'ALTER-EGO', 'alter-ego-promo': 'ALTER-EGO',
    identity: 'HÉROS', 'identity-promo': 'HÉROS', obligation: 'OBLIGATION', 'obligation-villain': 'OBLIGATION', 'generic-promo': 'ALLIÉ',
    'generic-promo-vert': 'ALLIÉ',
  },
}

/** Les champs de contenu d'une carte (tout est facultatif). `langue` : 'en' (defaut) ou 'fr'. */
export const CHAMPS_VIDES = {
  langue: 'en', echelleTexte: 0, titre: '', unique: false, typeTexte: '', traits: '', regles: '', citation: '', ligneEnsemble: '', createur: '',
  // nombres : texte affiche (« 3 », « X », « — »), avec leur etoile (« * ») eventuelle
  cout: '', coutEtoile: false, thw: '', thwEtoile: false, thwConseq: 0, atk: '', atkEtoile: false, atkConseq: 0,
  def: '', defEtoile: false, rec: '', recEtoile: false, pv: '', pvEtoile: false, tailleMain: '', menaceDepart: '',
  menaceDepartEtoile: false, menaceDepartParJoueur: false, menaceCible: '', menaceCibleParJoueur: false, acceleration: '', accelerationParJoueur: false, phaseNumero: '', phaseLettre: '', etape: '',
  renforts: 0, renfortEtoile: false, ressources: [], atkAttache: '', atkAttacheEtoile: false, schAttache: '', schAttacheEtoile: false,
  centrerTexte: false,
}

const px = (v, defaut = 0) => {
  const n = parseFloat(v)
  return Number.isFinite(n) ? n : defaut
}

/** La matrice [a,b,c,d,e,f] propre a un element : origine, translate, rotate, scale, transform (ordre CSS). */
function matricePropre(el) {
  const [ox, oy] = [el.boite[0] + el.origine[0], el.boite[1] + el.origine[1]]
  let m = [1, 0, 0, 1, ox, oy]
  const mul = (a, b) => [
    a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
    a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5],
  ]
  if (el.trn) m = mul(m, [1, 0, 0, 1, el.trn[0], el.trn[1]])
  if (el.rot) {
    const r = (el.rot * Math.PI) / 180
    m = mul(m, [Math.cos(r), Math.sin(r), -Math.sin(r), Math.cos(r), 0, 0])
  }
  if (el.scl) m = mul(m, [el.scl[0], 0, 0, el.scl[1], 0, 0])
  if (el.m) m = mul(m, el.m)
  return mul(m, [1, 0, 0, 1, -ox, -oy])
}

/** Applique au contexte la chaine de transformations de l'element (parents d'abord). */
function appliquerChaine(ctx, el, parId) {
  const chaine = []
  for (let e = el; e; e = parId.get(e.parent)) chaine.unshift(e)
  for (const e of chaine) {
    if (e.rot || e.trn || e.scl || e.m) ctx.transform(...matricePropre(e))
  }
}

function premiereFamille(s) {
  return (s || '').split(',')[0].replace(/["']/g, '').trim()
}

/** La police de base d'un champ a partir du style mesure. */
function baseDe(el, extra = {}) {
  const s = el.style
  const taille = px(s.fontSize, 50)
  const lh = s.lineHeight && s.lineHeight !== 'normal' ? px(s.lineHeight) : taille * 1.2
  return {
    famille: premiereFamille(s.fontFamily), taille, interligne: lh, poids: s.fontWeight === '400' ? 'normal' : s.fontWeight,
    style: s.fontStyle, espacement: px(s.letterSpacing, 0), capsPetites: s.fontVariant === 'small-caps', ...extra,
  }
}

// L'icone « par joueur » apres un nombre (taille, decalage vertical, ecart : en fraction de la taille du nombre), mesuree sur une vraie carte.
const PAR_JOUEUR = { fs: 0.56, dy: 0.14, ecart: 0 }
const PAR_JOUEUR_PAR_ROLE = { acceleration: { fs: 0.72, dy: 0.1, ecart: 0 } } // « +1 » de la manigance principale : une petite boite, une icone proportionnellement plus grande

const ROLES_NOMBRES = {
  'paycost cost': 'cout', 'thw sch cost': 'thw', 'atk cost': 'atk', 'def cost': 'def', 'rec cost': 'rec', 'hp cost': 'pv',
  'targetthreat cost': 'menaceCible', startingthreatwrap: 'menaceDepart', acceleration: 'acceleration',
  'attachmentatknums cost': 'atkAttache', 'attachmentschnums cost': 'schAttache', handsize: 'tailleMain',
}

/**
 * Le filtre `codeshadow` de la page de reference : contour noir de 4 px (dilatation), puis quatre ombres noires en cascade
 * (chaque ombre porte sur le resultat precedent) : les copies noires se trouvent donc a toutes les sommes de decalages.
 */
const OMBRES = [[-3, 3.5], [-2.5, 3], [-1.5, 2], [-0.5, 1]]
const DECALAGES = OMBRES.reduce((acc, [dx, dy]) => [...acc, ...acc.map(([x, y]) => [x + dx, y + dy])], [[0, 0]]).slice(1)
const MARGE_FILTRE = 40

/** Dessine `trace(ctx)` (formes pleines) avec le filtre : contour + ombres derriere, forme blanche devant. */
function avecContour(ctx, w, h, couleur, trace) {
  const toile = new OffscreenCanvas(w + 2 * MARGE_FILTRE, h + 2 * MARGE_FILTRE)
  const c = toile.getContext('2d')
  c.translate(MARGE_FILTRE, MARGE_FILTRE)
  c.lineJoin = 'round'
  c.lineWidth = 8
  c.strokeStyle = '#000'
  c.fillStyle = '#000'
  trace(c, 'contour')
  c.fillStyle = couleur
  trace(c, 'remplir')
  // silhouette noire de (contour + forme) pour les ombres
  const noir = new OffscreenCanvas(toile.width, toile.height)
  const n = noir.getContext('2d')
  n.drawImage(toile, 0, 0)
  n.globalCompositeOperation = 'source-in'
  n.fillStyle = '#000'
  n.fillRect(0, 0, noir.width, noir.height)
  for (const [dx, dy] of DECALAGES) ctx.drawImage(noir, -MARGE_FILTRE + dx, -MARGE_FILTRE + dy)
  ctx.drawImage(toile, -MARGE_FILTRE, -MARGE_FILTRE)
}

/**
 * Ligne de base d'un texte centre verticalement sur `centre`. Chrome centre la zone de glyphes de la police du DOM : pour ElektraMed
 * (chiffres) la mesure donne centre + 0,36 x taille, pour ChampionsIcons centre + 0,3 x taille (a 0,8 / d 0,2 de la taille).
 */
function baselineCentree(taille, famille, centre) {
  return centre + taille * (/ElektraMed/.test(famille) ? 0.36 : 0.3)
}

/**
 * Un nombre dans sa boite « ... cost » : centre dans la boite ; si une etoile le suit, la mesure donne le decalage du nombre
 * (`etoile.dx`), la taille de l'etoile, son ecart et son decalage vertical. Etoile sans valeur : l'etoile seule, plus grande.
 */
function dessinerNombre(ctx, el, texte, etoile, parJoueur = false) {
  if (!texte && !etoile) return
  const base = baseDe(el)
  if (/HorribleJefe/.test(base.famille)) {
    // promos : taille de main et PV en texte simple, centre dans la boite (pas de contour)
    ctx.save()
    ctx.font = `${el.style.fontWeight >= 600 ? 'bold ' : ''}${base.taille}px ${base.famille}`
    ctx.fillStyle = el.style.color || '#000'
    ctx.textBaseline = 'alphabetic'
    const m = ctx.measureText(texte)
    ctx.fillText(texte, el.style.textAlign === 'center' ? (el.boite[2] - m.width) / 2 : 0, el.boite[3] / 2 + (m.fontBoundingBoxAscent - m.fontBoundingBoxDescent) / 2 + base.taille * 0.04)
    ctx.restore()
    return
  }
  if (el.fsNombre) base.taille = el.fsNombre
  const [, , w, h] = el.boite
  const police = `${base.style === 'italic' ? 'italic ' : ''}${el.style.fontWeight >= 600 ? 'bold ' : ''}${base.taille}px ${base.famille}`
  const couleur = el.style.color || '#fff'
  ctx.save()
  ctx.textAlign = 'left'
  ctx.textBaseline = 'alphabetic'
  // PV : l'etoile est un pseudo-element mesure (68 px, marge 20 px, 38 px au-dessus du centre)
  const E = el.etoile ?? (el.cls === 'hp cost' ? { fs: 68, dy: -38, ecart: 20, dx: -39 } : { fs: base.taille * 0.36, dy: -base.taille * 0.15, ecart: 0, dx: -base.taille * 0.18 })
  const ES = el.etoileSeule ?? { fs: 120, dx: 0, dy: 0 }
  ctx.font = police
  const largeur = texte ? ctx.measureText(texte).width : 0
  const pieces = []
  let elargir = 0
  if (texte) {
    const cx = w / 2 + (etoile ? E.dx : 0)
    pieces.push({ s: texte, police, x: cx - largeur / 2, centre: h / 2, fs: base.taille, famille: base.famille })
    if (etoile) pieces.push({ s: 's', police: `italic bold ${E.fs}px ChampionsIcons`, x: cx + largeur / 2 + E.ecart, centre: h / 2 + E.dy, fs: E.fs, famille: 'ChampionsIcons' })
  } else {
    pieces.push({ s: 's', police: `italic bold ${ES.fs}px ChampionsIcons`, x: w / 2 + ES.dx - ES.fs / 2, centre: h / 2 + ES.dy, fs: ES.fs, famille: 'ChampionsIcons' })
  }
  // l'icone « par joueur » (le glyphe `g` de la police) suit le nombre : le groupe nombre + icone est recentre dans la boite
  if (parJoueur && texte) {
    const K = PAR_JOUEUR_PAR_ROLE[el.cls] ?? PAR_JOUEUR
    const PJ = el.parJoueur ?? { fs: base.taille * K.fs, dy: base.taille * K.dy, ecart: base.taille * K.ecart }
    const policeIcone = `${PJ.fs}px ChampionsIcons`
    ctx.font = policeIcone
    const largeurIcone = ctx.measureText('g').width
    const total = largeur + PJ.ecart + largeurIcone
    const debut = (w - total) / 2
    pieces[0].x = debut
    pieces.push({ s: 'g', police: policeIcone, x: debut + largeur + PJ.ecart, centre: h / 2 + PJ.dy, fs: PJ.fs, famille: 'ChampionsIcons' })
    // boites tres etroites (menace cible : 5 px) : on elargit la zone de dessin (et son filtre de contour) pour que le groupe y tienne
    elargir = Math.max(0, Math.ceil((total - w) / 2 + 30))
  }
  for (const p of pieces) p.y = baselineCentree(p.fs, p.famille, p.centre)
  ctx.translate(-elargir, 0)
  avecContour(ctx, w + 2 * elargir, h, couleur, (c, mode) => {
    for (const p of pieces) {
      c.font = p.police
      c.textAlign = 'left'
      c.textBaseline = 'alphabetic'
      if (mode === 'contour') c.strokeText(p.s, p.x + elargir, p.y)
      c.fillText(p.s, p.x + elargir, p.y)
    }
  })
  ctx.restore()
}

/** Numero + lettre de la phase : deux blocs centres verticalement, un ecart mesure entre eux, groupe centre dans la boite. */
function dessinerPhase(ctx, el, contenu) {
  const base = baseDe(el)
  const [, , w, h] = el.boite
  const P = el.phase
  const police = (fs) => `${base.style === 'italic' ? 'italic ' : ''}bold ${fs}px ${base.famille}`
  const pieces = []
  ctx.save()
  if (contenu.phaseNumero) {
    ctx.font = police(P.fsNum)
    pieces.push({ s: String(contenu.phaseNumero), fs: P.fsNum, w: ctx.measureText(String(contenu.phaseNumero)).width })
  }
  if (contenu.phaseLettre) {
    ctx.font = police(P.fsLettre)
    { const l = String(contenu.phaseLettre).toUpperCase(); pieces.push({ s: l, fs: P.fsLettre, w: ctx.measureText(l).width }) }
  }
  const total = pieces.reduce((a, p) => a + p.w, 0) + P.ecart * (pieces.length - 1)
  let x = (w - total) / 2
  for (const p of pieces) {
    p.x = x
    x += p.w + P.ecart
  }
  avecContour(ctx, w, h, el.style.color || '#fff', (c, mode) => {
    for (const p of pieces) {
      c.font = police(p.fs)
      c.textAlign = 'left'
      c.textBaseline = 'alphabetic'
      const y = baselineCentree(p.fs, base.famille, h / 2)
      if (mode === 'contour') c.strokeText(p.s, p.x, y)
      c.fillText(p.s, p.x, y)
    }
  })
  ctx.restore()
}

/** La couleur dominante d'un rectangle local (repere courant) : celle du fond sous le libelle cuit. */
function couleurDominante(ctx, x, y, w, h) {
  const m = ctx.getTransform()
  const pts = [[x, y], [x + w, y], [x, y + h], [x + w, y + h]].map(([px, py]) => [m.a * px + m.c * py + m.e, m.b * px + m.d * py + m.f])
  const x0 = Math.max(0, Math.floor(Math.min(...pts.map((p) => p[0]))))
  const y0 = Math.max(0, Math.floor(Math.min(...pts.map((p) => p[1]))))
  const x1 = Math.min(ctx.canvas.width, Math.ceil(Math.max(...pts.map((p) => p[0]))))
  const y1 = Math.min(ctx.canvas.height, Math.ceil(Math.max(...pts.map((p) => p[1]))))
  if (x1 <= x0 || y1 <= y0) return '#000'
  const d = ctx.getImageData(x0, y0, x1 - x0, y1 - y0).data
  const nb = new Map()
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] < 250) continue
    const k = ((d[i] >> 3) << 10) | ((d[i + 1] >> 3) << 5) | (d[i + 2] >> 3)
    nb.set(k, (nb.get(k) ?? 0) + 1)
  }
  let best = -1
  let n = 0
  for (const [k, c] of nb) if (c > n) { best = k; n = c }
  return best < 0 ? '#000' : `rgb(${((best >> 10) & 31) << 3},${((best >> 5) & 31) << 3},${(best & 31) << 3})`
}

/** Une ligne de texte (titre, type, ligne d'ensemble, createur) dans sa boite : alignement du style, centree en hauteur, reduite si trop large. */
function dessinerLigne(ctx, el, source, { prefixeIcone = '' } = {}) {
  if (!source && !prefixeIcone) return
  const base = baseDe(el)
  const [, , w, h] = el.boite
  const transforme = el.style.textTransform === 'uppercase' ? (source || '').toUpperCase() : source || ''
  const jetons = analyser((prefixeIcone ? `<code>${prefixeIcone}</code>` : '') + transforme)
  let facteur = 1
  let page = mettreEnPage(ctx, jetons.filter((j) => j.t !== 'saut'), { ...base, interligne: h }, 1e6, facteur)
  const largeurTexte = Math.max(...page.lignes.map((l) => l.largeur), 0)
  if (largeurTexte > w) facteur = w / largeurTexte
  if (facteur < 1) infos.lignesReduites.push({ cls: el.cls, facteur })
  page = mettreEnPage(ctx, jetons, { ...base, interligne: h }, 1e6, facteur)
  const l0 = page.lignes[0]?.largeur ?? 0
  const align = el.style.textAlign
  const x = align === 'center' ? (w - l0) / 2 : align === 'right' || align === 'end' ? w - l0 : 0
  ctx.save()
  ctx.translate(x, 0)
  dessinerPage(ctx, page, { ...base, interligne: h }, l0 + 1, facteur, el.style.color || '#fff', 'left')
  ctx.restore()
}

/**
 * Le flux du panneau de texte : traits, regles, citation empiles dans l'ordre mesure, chacun dans sa largeur.
 * Rend, pour chaque bloc, { el, jetons, base, y, page, facteur } (y relatif au haut du panneau).
 */
/** Les coins coupes (`pinchleft`, `pinchright`) : une forme que le texte contourne. Rend la bordure a la hauteur y (px de carte). */
/** Rapport entre la taille des regles d'une carte imprimee (70 px a 1500 px de large) et le reglage par defaut du Card Maker de reference (59 px). */
const TAILLE_REGLES_IMPRIMEE = 70 / 59

const FORMES = {
  'polygon(0px 0px, 50% 0px, 100% 100%, 0px 100%)': [[0, 0], [0.5, 0], [1, 1], [0, 1]],
  'polygon(50% 0px, 0px 100%, 100% 100%, 100% 0px)': [[0.5, 0], [0, 1], [1, 1], [1, 0]],
  'polygon(0px 0px, 100% 0px, 75% 100%)': [[0, 0], [1, 0], [0.75, 1]],
}

/** Les abscisses (px de carte) ou le bord de la forme coupe la hauteur y. */
function coupures(poly, boite, y) {
  const [x0, y0, w, h] = boite
  const t = (y - y0) / h
  const xs = []
  for (let k = 0; k < poly.length; k++) {
    const [ax, ay] = poly[k]
    const [bx, by] = poly[(k + 1) % poly.length]
    if ((ay <= t && by >= t) || (by <= t && ay >= t)) xs.push(x0 + w * (ay === by ? Math.max(ax, bx) : ax + ((bx - ax) * (t - ay)) / (by - ay)))
  }
  return xs
}

/**
 * Ce qu'une forme flottante retire a la ligne qui occupe [ya, yb] (px de carte), comme `shape-outside` : le bord le plus avance
 * sur toute la hauteur de la ligne. Rend l'abscisse du bord, ou null si la ligne est hors de la forme.
 */
function bordureForme(el, ya, yb, cote) {
  const poly = FORMES[el.style.clipPath]
  if (!poly) return null
  const [, y0, , h] = el.boite
  const a = Math.max(ya, y0)
  const b = Math.min(yb, y0 + h)
  if (a > b) return null
  const ys = [a, b, ...poly.map(([, py]) => y0 + py * h).filter((y) => y > a && y < b)]
  const bords = ys.flatMap((y) => coupures(poly, el.boite, y))
  if (!bords.length) return null
  return cote === 'g' ? Math.max(...bords) : Math.min(...bords)
}

/** Traits, regles et citation empiles dans l'ordre mesure ; si tout depasse le panneau, regles et citation se reduisent d'un meme facteur. */
function fluxTexte(ctx, spec, contenu) {
  const E = Object.fromEntries(spec.elements.map((e) => [e.cls, e]))
  const blocs = ['traits', 'rules', 'quote'].filter((c) => E[c]).sort((a, b) => E[a].boite[1] - E[b].boite[1])
  const panneau = E.cardtext
  if (!panneau) return []
  const source = { traits: contenu.traits, rules: contenu.regles, quote: contenu.citation }
  const villain = spec.famille === 'villain'
  const gauche = spec.elements.filter((e) => e.cls === 'pinchleft')
  const droite = spec.elements.filter((e) => e.cls === 'pinchright')
  const disposer = (facteur) => {
    const sortie = []
    // le premier bloc du flux part de sa propre place (promos : le panneau a 20 px de marge)
    const premier = E[blocs.find((c) => E[c].boite[1] >= panneau.boite[1])]
    let y = premier ? Math.max(0, premier.boite[1] - panneau.boite[1]) : 0
    for (const c of blocs) {
      const el = E[c]
      const libre = el.boite[1] < panneau.boite[1] || el.boite[1] > panneau.boite[1] + panneau.boite[3]
      const brut = c === 'traits' && el.style.textTransform === 'uppercase' ? (source[c] || '').toUpperCase() : source[c]
      const jetons = source[c] ? analyser(c === 'traits' ? `<em>${brut}</em>` : brut) : []
      if (!jetons.length) continue
      // les cartes imprimees ont un texte de regles ~19 % plus grand que le reglage par defaut du Card Maker de reference
      // (mesure sur une vraie carte : 70 px contre 59 px) ; la citation, elle, est a la meme taille.
      const base = baseDe(el, c === 'traits' ? { ecartParagraphe: 0 } : c === 'rules' ? { ecartParagraphe: 8, poidsGras: '500' } : { ecartParagraphe: 8 })
      if (c === 'rules') { base.taille *= TAILLE_REGLES_IMPRIMEE; base.interligne *= TAILLE_REGLES_IMPRIMEE }
      if (c === 'traits') base.interligne = el.boite[3]
      base.alignement = el.style.textAlign === 'center' ? 'center' : 'left'
      const largeur = el.boite[2]
      const bloc0 = panneau.boite[1] + y
      // une ligne qui occupe [a, b] du bloc evite les formes voisines sur toute sa hauteur
      const contrainte = (a, b) => {
        let g = 0
        let d = 0
        for (const f of gauche) {
          const bord = bordureForme(f, bloc0 + a, bloc0 + b, 'g')
          if (bord != null) g = Math.max(g, bord - el.boite[0])
        }
        for (const f of droite) {
          const bord = bordureForme(f, bloc0 + a, bloc0 + b, 'd')
          if (bord != null) d = Math.max(d, el.boite[0] + largeur - bord)
        }
        return { g: Math.max(0, g), d: Math.max(0, d) }
      }
      const f = c === 'traits' ? 1 : facteur
      const page = mettreEnPage(ctx, jetons, base, largeur, f, contrainte)
      if (libre) {
        sortie.push({ c, el, jetons, base, y: el.boite[1] - panneau.boite[1], page, facteur: f, largeur, retrait: 0, libre: true })
        continue
      }
      sortie.push({ c, el, jetons, base, y, page, facteur: f, largeur, retrait: 0 })
      // ecart au bloc suivant : celui du gabarit (mesure avec un contenu d'une ligne), sinon 20 / 30
      const suivant = E[blocs[blocs.indexOf(c) + 1]]
      const mesure = suivant ? suivant.boite[1] - el.boite[1] - el.boite[3] : -1
      y += page.hauteur + (mesure >= 0 && mesure <= 60 ? mesure : c === 'traits' ? (villain ? 30 : 20) : 30)
    }
    return { sortie, hauteur: y - 30 }
  }
  // le paquet de depart est une liste qui s'allonge : pas de reduction
  const maxi = spec.id === 'starter-deck' ? 1e6 : panneau.boite[3] - 40
  // reglage manuel de la taille des regles et de la citation : plus de reduction automatique
  const manuel = Number(contenu.echelleTexte) > 0 ? Number(contenu.echelleTexte) : null
  let facteur = manuel ?? 1
  let r = disposer(facteur)
  while (!manuel && r.hauteur > maxi && facteur > 0.4) {
    facteur *= 0.97
    r = disposer(facteur)
  }
  infos.facteurTexte = facteur
  infos.deborde = r.hauteur > maxi
  // Centrage vertical optionnel (demande du 29/10/2026) : texte court, bouton « Centrer le texte » coche.
  // Les blocs places librement dans le gabarit (hors du flux normal) ne bougent pas.
  if (contenu.centrerTexte) {
    const decalage = Math.max(0, (maxi - r.hauteur) / 2)
    if (decalage > 0) for (const bloc of r.sortie) if (!bloc.libre) bloc.y += decalage
  }
  return r.sortie
}

/**
 * L'attachement : la colonne de gauche empile le titre et, selon les valeurs presentes, les boites ATK / SCH ; le titre monte quand
 * une boite apparait (mesure : 1865 sans boite, 1560 avec une, 1310 avec deux). Rend le gabarit adapte et la place de chaque boite.
 */
function adapterAttachement(spec, contenu) {
  const a = !!(contenu.atkAttache || contenu.atkAttacheEtoile)
  const s = !!(contenu.schAttache || contenu.schAttacheEtoile)
  const yAtk = s ? 1710 : 1695
  const ySch = a ? 1460 : 1695
  const decal = [1865, 1560, 1310][(a ? 1 : 0) + (s ? 1 : 0)] - 1865
  const elements = spec.elements.map((e) => {
    if (e.cls === 'attachmentatknums cost') return { ...e, boite: [e.boite[0], yAtk - 11, e.boite[2], e.boite[3]] }
    if (e.cls === 'attachmentschnums cost') return { ...e, boite: [e.boite[0], ySch - 11, e.boite[2], e.boite[3]] }
    if (['header', 'title'].includes(e.cls) || e.parent === spec.elements.find((x) => x.cls === 'title')?.i) return { ...e, boite: [e.boite[0], e.boite[1] + decal, e.boite[2], e.boite[3]] }
    return e
  })
  return { spec: { ...spec, elements }, a, s, yAtk, ySch }
}

/**
 * Dessine toute la carte sur `canvas` (taille du type). `etat` : { couleurs, art, artDevant, tete }.
 */
/** Ce que le dernier rendu a du faire pour que tout tienne (lu par le controle de lisibilite de la page). */
let infos = { facteurTexte: 1, deborde: false, lignesReduites: [], blocs: [] }

export async function dessinerCarte(canvas, spec, contenu, etat, dossierImages = 'img/') {
  infos = { facteurTexte: 1, deborde: false, lignesReduites: [], blocs: [] }
  const attache = spec.id === 'attachment' ? adapterAttachement(spec, contenu) : null
  if (attache) spec = attache.spec
  canvas.width = spec.largeur
  canvas.height = spec.hauteur
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  etat = { ...etat, avecStats: !!(contenu.thw || contenu.thwEtoile) }
  await dessinerCalques(ctx, spec, etat, dossierImages)
  if (attache) {
    for (const [actif, nom, y] of [[attache.s, 'sch', attache.ySch], [attache.a, 'atk', attache.yAtk]]) {
      if (actif) ctx.drawImage(await chargerImage(`${dossierImages}attachment/${nom}_box.webp`), 0, y)
    }
  }

  ctx.save()
  if (spec.paysage) ctx.transform(0, 1, -1, 0, spec.largeur, 0)
  const parId = new Map(spec.elements.map((e) => [e.i, e]))
  const E = Object.fromEntries(spec.elements.map((e) => [e.cls, e]))
  const dans = (el, fn) => {
    ctx.save()
    appliquerChaine(ctx, el, parId)
    ctx.translate(el.boite[0], el.boite[1])
    fn()
    ctx.restore()
  }

  // Fonds pleins du gabarit (promos : panneau de texte blanc, ligne d'ensemble noire, traits noirs), sous les textes
  for (const e of spec.elements) {
    const bg = e.style.backgroundColor
    if (!bg || /rgba\(0, 0, 0, 0\)|transparent/.test(bg) || !['cardtext', 'set-line', 'traits'].includes(e.cls)) continue
    if (e.cls === 'traits' && !contenu.traits) continue
    dans(e, () => {
      if (e.cls === 'cardtext') {
        // panneau des promos : ombre pleine decalee de 28 px + bordure noire de 5 px
        ctx.fillStyle = '#000'
        ctx.fillRect(28, 28, e.boite[2], e.boite[3])
        ctx.fillRect(0, 0, e.boite[2], e.boite[3])
        ctx.fillStyle = bg
        ctx.fillRect(5, 5, e.boite[2] - 10, e.boite[3] - 10)
        return
      }
      ctx.fillStyle = bg
      ctx.fillRect(0, 0, e.boite[2], e.boite[3])
    })
  }

  // la bulle de PV des promos se pose par-dessus le panneau blanc
  const bulle = spec.calques.find((c) => c.role === 'hp_bubble' && c.pos)
  if (bulle) ctx.drawImage(await chargerImage(dossierImages + bulle.src), ...bulle.pos)

  // Nombres (cout, stats, PV, menace)
  for (const [cls, champ] of Object.entries(ROLES_NOMBRES)) {
    const el = E[cls]
    if (!el) continue
    dans(el, () => dessinerNombre(ctx, el, contenu[champ], contenu[champ + 'Etoile'], contenu[champ + 'ParJoueur']))
  }

  // Tete d'angle (au-dessus des nombres, comme la reference) : l'image (300 x 300 « cover ») centree sur (boite + 150 + decalage), zoomee et tournee comme la reference
  if (teteVisible(spec, etat)) {
    const T = etat.tete
    const E0 = spec.elements.find((e) => e.cls === 'photoimg headshot')
    const [bx, by] = E0 ? [E0.boite[0], E0.boite[1]] : [1, 0]
    const im = T.image
    const k = Math.max(300 / im.naturalWidth, 300 / im.naturalHeight)
    ctx.save()
    ctx.translate(bx + 150 + (T.x ?? -19), by + 150 + (T.y ?? 232))
    ctx.rotate((((spec.paysage ? -90 : 0) + (T.rotation ?? 0)) * Math.PI) / 180)
    ctx.scale(T.zoom ?? 0.8, T.zoom ?? 0.8)
    ctx.beginPath()
    ctx.rect(-150, -150, 300, 300)
    ctx.clip()
    ctx.drawImage(im, -(im.naturalWidth * k) / 2, -(im.naturalHeight * k) / 2, im.naturalWidth * k, im.naturalHeight * k)
    ctx.restore()
  }

  // Phase de la manigance principale : numero + lettre, groupe centre dans la boite
  const phase = E['mainschemephase cost']
  if (phase?.phase && (contenu.phaseNumero || contenu.phaseLettre)) dans(phase, () => dessinerPhase(ctx, phase, contenu))

  // Ressources (3 emplacements fixes) et icones de renfort (ancrees a droite), images posees dans le repere de la carte
  const IMG = {}
  const img = async (nom) => (IMG[nom] ??= await chargerImage(`${dossierImages}general/${nom}.webp`))
  for (const [k, genre] of (contenu.ressources ?? []).entries()) {
    if (!genre || !spec.ressources?.[k]) continue
    ctx.drawImage(await img(`resource-${genre}`), ...spec.ressources[k])
  }
  const R = spec.renforts
  const n = contenu.renforts | 0
  if (R && (n || contenu.renfortEtoile)) {
    if (R.fond) ctx.drawImage(await img(`../${R.fond}/boostbox${n + (contenu.renfortEtoile ? 1 : 0)}`), 0, 0)
    for (let i = 1; i <= n; i++) ctx.drawImage(await img('boost_icon'), R.x - 95 * (i - 1), R.y)
    if (contenu.renfortEtoile) ctx.drawImage(await img('boost_star'), n ? R.x - 95 * (n - 1) - 90 : R.x + 5, R.y)
  }

  // Degats consequents : n icones « d » blanches, centrees dans la boite (ligne de base a 0,9125 x taille du haut)
  for (const [cls, champ] of [['thwconsequential', 'thwConseq'], ['atkconsequential', 'atkConseq']]) {
    const el = E[cls]
    const n = contenu[champ] | 0
    if (!el || !n) continue
    dans(el, () => {
      const fs = px(el.style.fontSize, 80)
      ctx.font = `${fs}px ChampionsIcons`
      ctx.fillStyle = el.style.color || '#fff'
      ctx.textBaseline = 'alphabetic'
      const t = 'd'.repeat(n)
      ctx.fillText(t, (el.boite[2] - ctx.measureText(t).width) / 2, fs * 0.9125)
    })
  }

  // Lignes : titre, type, ligne d'ensemble, createur
  const pleine = etat.cadre === 'illustration'
  if (pleine) {
    // pas de cadre : des panneaux translucides donnent un fond aux textes
    const panneauTranslucide = (cls, couleur, rayon) => {
      const e = E[cls]
      if (!e) return
      dans(e, () => {
        ctx.fillStyle = couleur
        ctx.beginPath()
        ctx.roundRect(-14, -6, e.boite[2] + 28, e.boite[3] + 12, rayon)
        ctx.fill()
      })
    }
    panneauTranslucide('cardtext', 'rgba(255,255,255,0.86)', 36)
    panneauTranslucide('header', 'rgba(255,255,255,0.86)', 30)
    panneauTranslucide('set-line', 'rgba(0,0,0,0.62)', 20)
    panneauTranslucide('c-line', 'rgba(0,0,0,0.5)', 14)
    panneauTranslucide('typestr', 'rgba(0,0,0,0.62)', 14)
  }
  const titre = E.title
  if (titre) dans(titre, () => dessinerLigne(ctx, titre, contenu.titre, { prefixeIcone: contenu.unique ? 'u' : '' }))
  // Libelle du type : recouvre le libelle anglais cuit puis ecrit le libelle de la langue (ou le libelle libre)
  const ty = E.typestr
  const libre = contenu.typeTexte
  const voulu = libre || (contenu.langue === 'fr' ? LIBELLES.fr[spec.id] : '')
  if (pleine && ty) {
    // sans cadre le libelle n'est pas cuit dans l'image : on l'ecrit toujours
    const mot = libre || LIBELLES[contenu.langue === 'fr' ? 'fr' : 'en'][spec.id]
    if (mot) dans(ty, () => dessinerLigne(ctx, ty, mot))
  } else if (ty && voulu && LIBELLES.en[spec.id]) {
    dans(ty, () => {
      const base = baseDe(ty)
      const [, , w, h] = ty.boite
      // le libelle cuit est plus grand que notre police : on recouvre toute la boite, un peu plus haut et plus bas
      ctx.fillStyle = couleurDominante(ctx, 0, -8, w, h + 16)
      ctx.fillRect(0, -10, w, h + 20)
      ctx.letterSpacing = '0px'
      dessinerLigne(ctx, ty, voulu)
    })
  }
  for (const [cls, champ] of [['villainstagenew', 'etape'], ['set-line', 'ligneEnsemble'], ['c-line', 'createur']]) {
    if (E[cls]) dans(E[cls], () => dessinerLigne(ctx, E[cls], contenu[champ]))
  }

  // Panneau de texte : traits / regles / citation
  const panneau = E.cardtext
  if (panneau) {
    infos.blocs = []
    for (const b of fluxTexte(ctx, spec, contenu)) {
      infos.blocs.push({ c: b.c, y0: b.y, y1: b.y + b.page.hauteur })
      dans(panneau, () => {
        ctx.translate(b.el.boite[0] - panneau.boite[0] + b.retrait, b.y)
        dessinerPage(ctx, b.page, b.base, b.largeur, b.facteur, spec.id === 'identity-promo' && b.c === 'traits' ? 'rgba(255,255,255,0.6)' : b.el.style.color || '#000', b.base.alignement)
      })
    }
  }
  ctx.restore()
  dessinerNiveau(ctx, spec, etat, 'dessus')
  canvas.infos = infos
  return canvas
}

export { PORTRAIT }

// ---------------------------------------------------------------- clic sur la carte
const produit = (a, b) => [
  a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
  a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5],
]
const inverse = ([a, b, c, d, e, f]) => {
  const det = a * d - b * c
  return det ? [d / det, -b / det, -c / det, a / det, (c * f - d * e) / det, (b * e - a * f) / det] : null
}

/**
 * L'element du gabarit sous un point de la carte (pixels du canvas). Rend { cls, local: [x, y] } (le point dans le repere de
 * l'element) ou null. Les chaines de transformations (cartes paysage, libelles tournes) sont prises en compte.
 */
export function elementSousPoint(spec, x, y) {
  // canvas -> repere du gabarit portrait
  let gx = x
  let gy = y
  if (spec.paysage) { gx = y; gy = spec.largeur - x }
  const parId = new Map(spec.elements.map((e) => [e.i, e]))
  let meilleur = null
  for (const e of spec.elements) {
    if (!e.cls || !e.boite[2] || !e.boite[3]) continue
    let m = [1, 0, 0, 1, 0, 0]
    const chaine = []
    for (let p = e; p; p = parId.get(p.parent)) chaine.unshift(p)
    for (const c of chaine) if (c.rot || c.trn || c.scl || c.m) m = produit(m, matricePropre(c))
    const inv = inverse(m)
    if (!inv) continue
    const lx = inv[0] * gx + inv[2] * gy + inv[4]
    const ly = inv[1] * gx + inv[3] * gy + inv[5]
    const [bx, by, bw, bh] = e.boite
    if (lx < bx || lx > bx + bw || ly < by || ly > by + bh) continue
    const surface = bw * bh
    if (!meilleur || surface < meilleur.surface) meilleur = { cls: e.cls, local: [lx, ly], surface, panneau: e.boite }
  }
  return meilleur
}
