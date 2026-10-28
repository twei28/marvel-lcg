// Dessiner une carte complete : calques + illustration (rendu.js), puis les textes et les nombres, un par element du gabarit.
//
// Le gabarit (`types.json`) donne, pour chaque element, sa boite SANS rotation, sa propre transformation et son origine ; on
// recompose la chaine de transformations de ses parents (comme CSS) puis on dessine dans la boite locale.
import { PORTRAIT, dessinerCalques } from './rendu.js'
import { analyser, dessinerPage, mettreEnPage } from './texte.js'

/** Les champs de contenu d'une carte (tout est facultatif). */
export const CHAMPS_VIDES = {
  titre: '', unique: false, typeTexte: '', traits: '', regles: '', citation: '', ligneEnsemble: '', createur: '',
  // nombres : texte affiche (« 3 », « X », « — »), avec leur etoile (« * ») eventuelle
  cout: '', coutEtoile: false, thw: '', thwEtoile: false, thwConseq: 0, atk: '', atkEtoile: false, atkConseq: 0,
  def: '', defEtoile: false, rec: '', recEtoile: false, pv: '', pvEtoile: false, tailleMain: '', menaceDepart: '',
  menaceDepartEtoile: false, menaceCible: '', acceleration: '', phaseNumero: '', phaseLettre: '', etape: '',
  renforts: 0, renfortEtoile: false, ressources: [], atkAttache: '', schAttache: '',
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

const ROLES_NOMBRES = {
  'paycost cost': 'cout', 'thw sch cost': 'thw', 'atk cost': 'atk', 'def cost': 'def', 'rec cost': 'rec', 'hp cost': 'pv',
  'targetthreat cost': 'menaceCible',
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
function dessinerNombre(ctx, el, texte, etoile) {
  if (!texte && !etoile) return
  const base = baseDe(el)
  const [, , w, h] = el.boite
  const police = `${base.style === 'italic' ? 'italic ' : ''}${el.style.fontWeight >= 600 ? 'bold ' : ''}${base.taille}px ${base.famille}`
  const couleur = el.style.color || '#fff'
  ctx.save()
  ctx.textAlign = 'left'
  ctx.textBaseline = 'alphabetic'
  const E = el.etoile ?? { fs: base.taille * 0.36, dy: -base.taille * 0.15, ecart: 0, dx: -base.taille * 0.18 }
  const ES = el.etoileSeule ?? { fs: 120, dx: 0, dy: 0 }
  ctx.font = police
  const largeur = texte ? ctx.measureText(texte).width : 0
  const pieces = []
  if (texte) {
    const cx = w / 2 + (etoile ? E.dx : 0)
    pieces.push({ s: texte, police, x: cx - largeur / 2, centre: h / 2, fs: base.taille, famille: base.famille })
    if (etoile) pieces.push({ s: 's', police: `${E.fs}px ChampionsIcons`, x: cx + largeur / 2 + E.ecart, centre: h / 2 + E.dy, fs: E.fs, famille: 'ChampionsIcons' })
  } else {
    pieces.push({ s: 's', police: `${ES.fs}px ChampionsIcons`, x: w / 2 + ES.dx - ES.fs / 2, centre: h / 2 + ES.dy, fs: ES.fs, famille: 'ChampionsIcons' })
  }
  for (const p of pieces) p.y = baselineCentree(p.fs, p.famille, p.centre)
  avecContour(ctx, w, h, couleur, (c, mode) => {
    for (const p of pieces) {
      c.font = p.police
      c.textAlign = 'left'
      c.textBaseline = 'alphabetic'
      if (mode === 'contour') c.strokeText(p.s, p.x, p.y)
      c.fillText(p.s, p.x, p.y)
    }
  })
  ctx.restore()
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
    let y = 0
    for (const c of blocs) {
      const el = E[c]
      const brut = c === 'traits' && el.style.textTransform === 'uppercase' ? (source[c] || '').toUpperCase() : source[c]
      const jetons = source[c] ? analyser(c === 'traits' ? `<em>${brut}</em>` : brut) : []
      if (!jetons.length) continue
      const base = baseDe(el, c === 'traits' ? { ecartParagraphe: 0 } : { ecartParagraphe: 8 })
      if (c === 'traits') base.interligne = base.taille * 1.3
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
      sortie.push({ c, el, jetons, base, y, page, facteur: f, largeur, retrait: 0 })
      y += page.hauteur + (c === 'traits' ? (villain ? 30 : 20) : 30)
    }
    return { sortie, hauteur: y - 30 }
  }
  const maxi = panneau.boite[3] - 40
  let facteur = 1
  let r = disposer(facteur)
  while (r.hauteur > maxi && facteur > 0.4) {
    facteur *= 0.97
    r = disposer(facteur)
  }
  return r.sortie
}

/**
 * Dessine toute la carte sur `canvas` (taille du type). `etat` : { couleurs, art, artDevant, tete }.
 */
export async function dessinerCarte(canvas, spec, contenu, etat, dossierImages = 'img/') {
  canvas.width = spec.largeur
  canvas.height = spec.hauteur
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  await dessinerCalques(ctx, spec, etat, dossierImages)

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

  // Nombres (cout, stats, PV, menace)
  for (const [cls, champ] of Object.entries(ROLES_NOMBRES)) {
    const el = E[cls]
    if (!el) continue
    dans(el, () => dessinerNombre(ctx, el, contenu[champ], contenu[champ + 'Etoile']))
  }

  // Lignes : titre, type, ligne d'ensemble, createur
  const titre = E.title
  if (titre) dans(titre, () => dessinerLigne(ctx, titre, contenu.titre, { prefixeIcone: contenu.unique ? 'u' : '' }))
  for (const [cls, champ] of [['typestr', 'typeTexte'], ['set-line', 'ligneEnsemble'], ['c-line', 'createur']]) {
    if (E[cls]) dans(E[cls], () => dessinerLigne(ctx, E[cls], contenu[champ]))
  }

  // Panneau de texte : traits / regles / citation
  const panneau = E.cardtext
  if (panneau) {
    for (const b of fluxTexte(ctx, spec, contenu)) {
      dans(panneau, () => {
        ctx.translate(b.el.boite[0] - panneau.boite[0] + b.retrait, b.y)
        dessinerPage(ctx, b.page, b.base, b.largeur, b.facteur, b.el.style.color || '#000', b.base.alignement)
      })
    }
  }
  ctx.restore()
  return canvas
}

export { PORTRAIT }
