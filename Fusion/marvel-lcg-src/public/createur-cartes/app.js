// La page du créateur de cartes : liste de cartes, formulaire guidé par type, aperçu en direct, couleurs, illustration, tête d'angle,
// sauvegarde (IndexedDB + fichier .json), exports (PNG / JPG / WebP, FR + EN, planche à imprimer, planche TTS).
import { dessinerCarte, CHAMPS_VIDES, LIBELLES } from './carte.js'
import { chargerPolices } from './polices.js'
import { ICONES } from './polices.js'
import { TEXTES, chargerTraits, traduireTraits } from './langues.js'
import { $, el, S, nouvelId, blobVersDataUrl, dataUrlVersBlob } from './commun.js'
import { ajouterFichiers, brancherSurcouche, calqueChoisi, choisirCalque, commencerGlisser, dessinerSurcouche, molette, sectionLibres, touche } from './panneau-libres.js'
import { clicSurCarte } from './clic-carte.js'
import { ouvrirRecadrage } from './recadrage.js'
import { brancherStyles, chargerStyles, enveloppePerso } from './styles-texte.js'
import { changerLangueUI, demarrerI18n, langueMemorisee, langueUI, t as tr } from './i18n.js'
import { ajouterVersion, ecrireProjet, lireProjet } from './stockage.js'
import { alertesLisibilite, enregistrerModele, ouvrirAppliquer, ouvrirRemplacer, ouvrirVersions } from './projet-outils.js'

const BASE = '/createur-cartes/'
const IMAGES = BASE + 'img/'

const GROUPES = [
  ['Héros', ['ally', 'event', 'upgrade', 'support', 'resource', 'alter-ego', 'identity', 'obligation', 'playersidescheme']],
  ['Vilains et rencontres', ['villain', 'minion', 'treachery', 'environment', 'attachment', 'sidescheme', 'main_scheme_a', 'main_scheme_b', 'obligation-villain']],
  ['Promos et paquet de départ', ['generic-promo', 'generic-promo-vert', 'alter-ego-promo', 'identity-promo', 'starter-deck']],
]
const NOMS = {
  ally: 'Allié', event: 'Événement', upgrade: 'Amélioration', support: 'Soutien', resource: 'Ressource', 'alter-ego': 'Alter-ego', identity: 'Identité de héros',
  obligation: 'Obligation (héros)', playersidescheme: 'Manigance annexe de joueur', villain: 'Méchant', minion: 'Sbire', treachery: 'Trahison',
  environment: 'Environnement', attachment: 'Attachement', sidescheme: 'Manigance annexe', main_scheme_a: 'Manigance principale (face A)',
  main_scheme_b: 'Manigance principale (face B)', 'obligation-villain': 'Obligation (rencontre)', 'generic-promo': 'Promo générique',
  'generic-promo-vert': 'Promo générique (verticale)', 'alter-ego-promo': 'Promo alter-ego', 'identity-promo': 'Promo héros', 'starter-deck': 'Paquet de départ',
}
const ROLES_COULEURS = {
  left_color: 'Gauche', left_accent: 'Gauche (accent)', right_color: 'Droite', right_accent: 'Droite (accent)', divider: 'Séparateur',
  light_boxes: 'Cases claires', splash_color: 'Éclat de la tête', background_upper: 'Fond (haut)', background_lower: 'Fond (bas)',
  shading: 'Ombrage', middle: 'Milieu', outer: 'Contour', accent: 'Accent', cracks: 'Fissures',
}
// Les aspects : une couleur unie pour tous les roles, relevee sur les boutons d'aspect du Card Maker de reference.
const uni = (c, boites = c) => ({ left_color: c, left_accent: c, right_color: c, right_accent: c, divider: c, light_boxes: boites })
const ASPECTS = {
  'Basic (gris)': uni('#87868f', '#000000'), Agression: uni('#b12020'), Direction: uni('#2ea7b8'),
  Protection: uni('#46991b'), Justice: uni('#dbcb36'), Pool: uni('#d074ac', '#000000'),
}
const GENRES_RESSOURCE = [['', 'Aucune'], ['energy', 'Énergie'], ['mental', 'Mental'], ['physical', 'Physique'], ['wild', 'Joker']]
const ICONES_BARRE = [['energy', 'Énergie'], ['mental', 'Mental'], ['physical', 'Physique'], ['wild', 'Joker'], ['star', 'Étoile'], ['acceleration', 'Accélération'], ['crisis', 'Crise'], ['hazard', 'Danger'], ['boost', 'Renfort'], ['per_hero', 'Par héros'], ['consequential', 'Dégâts conséquents'], ['unique', 'Unique']]
const TYPES_SANS_FISSURES = new Set(['attachment', 'environment', 'minion', 'obligation-villain', 'sidescheme', 'treachery'])

let TYPES = null
let PALETTES = null
let projet = { cartes: [], courante: null }
let seq = 0
let ciblePointeur = 'art'
const imagesBlob = new WeakMap()
const imagesPretes = new WeakMap() // Blob -> image deja chargee (pour les calculs synchrones de l'apercu)

// ---------------------------------------------------------------- stockage
let minuteurSauvegarde = 0
function sauvegarderPlusTard() {
  clearTimeout(minuteurSauvegarde)
  minuteurSauvegarde = setTimeout(async () => {
    try {
      await ecrireProjet(projet)
      versionsModifie = true
    } catch (e) {
      message('Sauvegarde dans le navigateur impossible : ' + e.message)
    }
  }, 500)
}
// Une version est gardee toutes les 5 minutes (si quelque chose a change) et quand on quitte la page.
let versionsModifie = false
async function garderVersion(raison = 'auto') {
  if (!versionsModifie) return
  versionsModifie = false
  try { await ajouterVersion(projet, raison) } catch {}
}
setInterval(() => garderVersion('auto'), 5 * 60 * 1000)
addEventListener('pagehide', () => { clearTimeout(minuteurSauvegarde); ecrireProjet(projet).catch(() => {}); garderVersion('fermeture') })

// ---------------------------------------------------------------- images
function imageDe(blob) {
  if (!blob) return Promise.resolve(null)
  if (!imagesBlob.has(blob)) {
    imagesBlob.set(
      blob,
      new Promise((ok, ko) => {
        const im = new Image()
        im.onload = () => { imagesPretes.set(blob, im); ok(im) }
        im.onerror = () => ko(new Error('image illisible'))
        im.src = URL.createObjectURL(blob)
      })
    )
  }
  return imagesBlob.get(blob)
}

// ---------------------------------------------------------------- cartes

function valeursParDefaut(type, langue) {
  const l = langue
  return {
    ...CHAMPS_VIDES,
    langue: l,
    titre: l === 'fr' ? 'Nom de la carte' : 'Card name',
    ligneEnsemble: TEXTES[l].ligneEnsemble(6, 10),
    createur: TEXTES[l].createur,
    cout: '2', thw: '2', atk: '2', def: '1', rec: '3', pv: '10', tailleMain: '6',
    menaceDepart: '3', menaceCible: '5', acceleration: '1', phaseNumero: '1',
    phaseLettre: type === 'main_scheme_b' ? 'B' : 'A', etape: 'I',
  }
}

function nouvelleCarte(type = 'ally', langue = 'fr') {
  return {
    id: nouvelId(), type, langue, contenu: valeursParDefaut(type, langue), couleurs: {}, fissures: true, libres: [], cadre: 'officiel', dossier: '',
    art: { blob: null, zoom: 1, x: 0, y: 0, rotation: 0 }, artDevant: { blob: null, zoom: 1, x: 0, y: 0, rotation: 0 },
    tete: { blob: null, afficher: true, etoile: false, zoom: 0.8, x: -19, y: 232, rotation: 0 },
  }
}
const carte = () => projet.cartes.find((c) => c.id === projet.courante)

/** Une copie profonde d'une carte (les images, des Blob, sont partagees : elles ne changent jamais). */
const cloner = (c) => structuredClone(c)

/** Une carte -> du JSON (images en data URL). Sert aux fichiers, aux versions envoyees au serveur, aux modeles exportes. */
async function serialiser(c) {
  const copie = structuredClone({ ...c, art: { ...c.art, blob: null }, artDevant: { ...c.artDevant, blob: null }, tete: { ...c.tete, blob: null }, libres: [] })
  for (const k of ['art', 'artDevant', 'tete']) copie[k].image = c[k].blob ? await blobVersDataUrl(c[k].blob) : null
  copie.libres = []
  for (const L of c.libres ?? []) copie.libres.push({ ...structuredClone({ ...L, blob: null }), image: L.blob ? await blobVersDataUrl(L.blob) : null })
  return copie
}
/** L'inverse de `serialiser` : rend une carte utilisable (images en Blob), avec les champs ajoutes depuis. */
async function deserialiser(j) {
  const base = nouvelleCarte(TYPES[j.type] ? j.type : 'ally', j.langue ?? 'fr')
  const c = { ...base, ...j, contenu: { ...base.contenu, ...j.contenu }, art: { ...base.art, ...j.art }, artDevant: { ...base.artDevant, ...j.artDevant }, tete: { ...base.tete, ...j.tete } }
  for (const k of ['art', 'artDevant', 'tete']) { c[k].blob = c[k].image ? await dataUrlVersBlob(c[k].image) : null; delete c[k].image }
  c.libres = []
  for (const L of j.libres ?? []) { const x = { ...L, blob: L.image ? await dataUrlVersBlob(L.image) : null }; delete x.image; c.libres.push(x) }
  return c
}

/** Les couleurs a afficher : celles du gabarit, par-dessus celles de la carte. */
function rolesDe(spec) {
  const r = new Set()
  for (const c of spec.calques) {
    if (c.teinte) r.add(c.teinte)
    if (c.role === 'gradient') { r.add('background_upper'); r.add('background_lower') }
  }
  if (spec.tete?.splash) r.add('splash_color')
  return [...r].filter((x) => ROLES_COULEURS[x])
}
function couleurDe(c, spec, role) {
  if (c.couleurs[role]) return c.couleurs[role]
  if (spec.couleursParDefaut[role]) return spec.couleursParDefaut[role]
  const g = spec.calques.find((x) => x.role === 'gradient')?.degrade
  if (role === 'background_lower') return g?.[0] ?? '#87868f'
  if (role === 'background_upper') return g?.[1] ?? '#87868f'
  return role === 'splash_color' ? '#e0ca22' : '#888888'
}
const hex6 = (c) => (/^#[0-9a-f]{6}$/i.test(c) ? c : '#888888')

// ---------------------------------------------------------------- langue
const RE_LIGNE = /^\s*(?:hand size|taille de main)\s+(.+?)\s*\/\s*(?:hit points|points de vie)\s+(.+?)\s*$/i
/** Le contenu de la carte dans une autre langue : traits traduits, lignes par defaut refaites. Le reste (regles...) est du texte libre. */
function contenuDansLangue(c, langue) {
  const ct = { ...c.contenu, langue }
  ct.traits = traduireTraits(ct.traits, langue)
  if (ct.traits === '.') ct.traits = ''
  const m = RE_LIGNE.exec(ct.ligneEnsemble)
  if (m) ct.ligneEnsemble = TEXTES[langue].ligneEnsemble(m[1], m[2])
  for (const autre of ['fr', 'en']) if (ct.createur === TEXTES[autre].createur) ct.createur = TEXTES[langue].createur
  return ct
}
function changerLangue(l) {
  const c = carte()
  if (!c || c.langue === l) return majBoutonsLangue()
  c.contenu = contenuDansLangue(c, l)
  c.langue = l
  majBoutonsLangue()
  construireFormulaire()
  changement()
}
function majBoutonsLangue() {
  const c = carte()
  $('#lang-fr').setAttribute('aria-pressed', String(c?.langue === 'fr'))
  $('#lang-en').setAttribute('aria-pressed', String(c?.langue === 'en'))
}

// ---------------------------------------------------------------- rendu
async function etatDe(c) {
  const [art, artDevant, tete] = await Promise.all([imageDe(c.art.blob), imageDe(c.artDevant.blob), imageDe(c.tete.blob)])
  const couleurs = c.cadre === 'sombre' ? { ...couleursSombres(TYPES[c.type]), ...c.couleurs } : { ...c.couleurs }
  return {
    couleurs,
    art: art && { image: art, x: c.art.x, y: c.art.y, zoom: c.art.zoom, rotation: c.art.rotation },
    artDevant: artDevant && { image: artDevant, x: c.artDevant.x, y: c.artDevant.y, zoom: c.artDevant.zoom, rotation: c.artDevant.rotation },
    tete: tete && { image: tete, afficher: c.tete.afficher, etoile: c.tete.etoile, zoom: c.tete.zoom, x: c.tete.x, y: c.tete.y, rotation: c.tete.rotation },
    fissures: c.fissures,
    cadre: c.cadre ?? 'officiel',
    libres: await Promise.all((c.libres ?? []).map(async (L) => ({ ...L, image: await imageDe(L.blob) }))),
  }
}
/** Le cadre « sombre » : tous les roles teintes passent a des gris-bleus tres fonces, les accents a un or discret. */
function couleursSombres(spec) {
  const accents = new Set(['left_accent', 'right_accent', 'divider', 'accent', 'splash_color'])
  return Object.fromEntries(rolesDe(spec).map((r) => [r, accents.has(r) ? '#a98f4e' : r === 'light_boxes' ? '#000000' : r.includes('upper') ? '#2b2d38' : '#1b1c24']))
}
/** Dessine une carte sur un canvas neuf (la langue peut etre forcee). */
async function rendreCarte(c, langue = null) {
  const spec = TYPES[c.type]
  const toile = document.createElement('canvas')
  const contenu = langue && langue !== c.langue ? contenuDansLangue(c, langue) : c.contenu
  await dessinerCarte(toile, spec, contenu, await etatDe(c), IMAGES)
  return toile
}
async function dessiner() {
  const n = ++seq
  const c = carte()
  if (!c) return
  try {
    const t = await rendreCarte(c)
    if (n !== seq) return
    const vis = $('#toile')
    vis.width = t.width
    vis.height = t.height
    vis.getContext('2d').drawImage(t, 0, 0)
    dessinerSurcouche()
    S.infosRendu = t.infos
    afficherAlertes(c, t)
  } catch (e) {
    message('Rendu impossible : ' + e.message)
  }
}
async function afficherAlertes(c, t) {
  const images = { art: await imageDe(c.art.blob), artDevant: await imageDe(c.artDevant.blob) }
  const al = alertesLisibilite(c, TYPES[c.type], t.infos, images)
  const zone = $('#alertes')
  zone.replaceChildren(...al.map((x) => el('div', { class: 'alerte ' + x.niveau }, (x.niveau === 'alerte' ? '⚠ ' : 'ℹ ') + x.texte)))
}

let minuteurRendu = 0
function changement() {
  clearTimeout(minuteurRendu)
  minuteurRendu = setTimeout(dessiner, 40)
  sauvegarderPlusTard()
  majListe()
  planifierHistorique()
}

// ---------------------------------------------------------------- annuler / retablir
// Par carte : une pile « avant » et une pile « apres ». Une modification n'entre dans l'historique qu'apres 400 ms de calme (taper
// une phrase = un seul pas). `ref` est la photo de la carte au dernier point de reprise.
const historiques = new Map()
let minuteurHistorique = 0
let modifie = false // la carte a change depuis le dernier point de reprise
const histoDe = (id) => {
  if (!historiques.has(id)) historiques.set(id, { avant: [], apres: [], ref: null })
  return historiques.get(id)
}
function validerHistorique() {
  clearTimeout(minuteurHistorique)
  const c = carte()
  if (!c) return
  const h = histoDe(c.id)
  if (!h.ref) { h.ref = cloner(c); modifie = false; return }
  if (!modifie) return
  modifie = false
  h.avant.push(h.ref)
  if (h.avant.length > 100) h.avant.shift()
  h.apres = []
  h.ref = cloner(c)
  majBoutonsHistorique()
}
function planifierHistorique() {
  modifie = true
  clearTimeout(minuteurHistorique)
  minuteurHistorique = setTimeout(validerHistorique, 400)
}
function remplacerCarte(c, photo) {
  modifie = false
  const i = projet.cartes.findIndex((x) => x.id === c.id)
  projet.cartes[i] = cloner(photo)
  majBoutonsLangue()
  construireFormulaire()
  dessiner()
  sauvegarderPlusTard()
  majListe()
  majBoutonsHistorique()
}
function annuler() {
  validerHistorique()
  const c = carte()
  const h = histoDe(c.id)
  if (!h.avant.length) return message('Rien à annuler.')
  h.apres.push(cloner(c))
  const photo = h.avant.pop()
  h.ref = cloner(photo)
  remplacerCarte(c, photo)
  message('Annulé.')
}
function retablir() {
  validerHistorique()
  const c = carte()
  const h = histoDe(c.id)
  if (!h.apres.length) return message('Rien à rétablir.')
  h.avant.push(cloner(c))
  const photo = h.apres.pop()
  h.ref = cloner(photo)
  remplacerCarte(c, photo)
  message('Rétabli.')
}
function majBoutonsHistorique() {
  const c = carte()
  const h = c && historiques.get(c.id)
  $('#b-annuler').disabled = !h?.avant.length
  $('#b-retablir').disabled = !h?.apres.length
}
function message(t) {
  $('#message').textContent = t
}

// ---------------------------------------------------------------- formulaire
function aElement(spec, cls) {
  return spec.elements.some((e) => e.cls === cls)
}
function champTexte(label, chemin, opts = {}) {
  const c = carte()
  const [obj, cle] = chemin
  const champ = opts.long ? el('textarea', { rows: opts.lignes ?? 3 }) : el('input', { type: 'text', 'data-champ': cle })
  champ.value = obj(c)[cle] ?? ''
  champ.addEventListener('input', () => {
    obj(c)[cle] = champ.value
    changement()
  })
  return el('label', {}, label, champ)
}
const dansContenu = [(c) => c.contenu]
function t(label, cle, opts) { return champTexte(label, [(c) => c.contenu, cle], opts) }
function coche(label, obj, cle, apres) {
  const c = carte()
  const i = el('input', { type: 'checkbox' })
  i.checked = !!obj(c)[cle]
  i.addEventListener('change', () => {
    obj(c)[cle] = i.checked
    changement()
    apres?.()
  })
  return el('label', { class: 'ligne' }, i, label)
}
function liste(label, obj, cle, options, convertir = (v) => v) {
  const c = carte()
  const s = el('select', {}, options.map(([v, n]) => el('option', { value: v }, n)))
  s.value = String(obj(c)[cle] ?? '')
  s.addEventListener('change', () => {
    obj(c)[cle] = convertir(s.value)
    changement()
  })
  return el('label', {}, label, s)
}
function curseur(label, obj, cle, min, max, pas, defaut) {
  const c = carte()
  const r = el('input', { type: 'range', min, max, step: pas })
  r.value = obj(c)[cle] ?? defaut
  r.addEventListener('input', () => {
    obj(c)[cle] = Number(r.value)
    changement()
  })
  r.addEventListener('dblclick', () => {
    r.value = defaut
    obj(c)[cle] = defaut
    changement()
  })
  return el('label', {}, label, r)
}
function nombre(label, cle, avecEtoile = true) {
  const c = carte()
  const i = el('input', { type: 'text', 'data-champ': cle })
  i.value = c.contenu[cle] ?? ''
  i.addEventListener('input', () => {
    c.contenu[cle] = i.value
    changement()
  })
  const ligne = el('div', { class: 'nombre' }, el('label', {}, label, i))
  if (avecEtoile) ligne.append(coche('★', (x) => x.contenu, cle + 'Etoile'))
  return ligne
}
function section(titre, ouvert, ...contenu) {
  return el('details', { open: ouvert }, el('summary', {}, titre), el('div', { class: 'contenu' }, contenu))
}
// ---------------------------------------------------------------- editeur de texte sans balises
const ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;' }
const echapper = (t) => t.replace(/[&<>]/g, (c) => ESC[c])
const ENTITES_SRC = { '&mdash;': '—', '&ndash;': '–', '&nbsp;': ' ', '&rsquo;': '’', '&hellip;': '…', '&quot;': '"' }
const hexDe = (css) => {
  const m = /rgba?\(\s*(\d+)[ ,]+(\d+)[ ,]+(\d+)/i.exec(css)
  return m ? '#' + [m[1], m[2], m[3]].map((n) => Number(n).toString(16).padStart(2, '0')).join('') : css
}

/** Le mini-HTML de la carte -> le HTML de la zone d'edition (gras, italique... visibles, icones en vrai). */
function versEditeur(src) {
  const iconeDe = (nom) => (ICONES[nom] ? `<span class="ico" contenteditable="false" data-i="${nom}">${ICONES[nom]}</span>` : null)
  return String(src ?? '')
    .replace(/&[a-z]+;/g, (e) => ENTITES_SRC[e] ?? e)
    .split(/(<\/?(?:b|i|u|em|span)\b[^>]*>|<br\s*\/?>|<hr[^>]*>|\[[a-z_]+\]|\n)/i)
    .map((p, k) => {
      if (k % 2 === 0) return echapper(p).replace(/&amp;(lt|gt|amp);/g, '&$1;')
      const t = p.toLowerCase()
      if (t === '\n' || /^<br/.test(t)) return '<br>'
      if (/^<hr/.test(t)) return /class=["']?br/.test(t) ? '<br><br>' : '<span class="ico" contenteditable="false" data-hr="1">―――</span>'
      if (p[0] === '[') return iconeDe(p.slice(1, -1).toLowerCase()) ?? echapper(p)
      if (/^<em\b/.test(t)) return '<span class="trait">'
      if (/^<\/em/.test(t)) return '</span>'
      if (/^<span/.test(t)) {
        const css = /style\s*=\s*["']([^"']*)["']/i.exec(p)?.[1] ?? ''
        return `<span style="${echapper(css)}">`
      }
      return p.replace(/\s[^>]*/, '')
    })
    .join('')
}

/** La zone d'edition -> le mini-HTML de la carte. */
function depuisEditeur(racine) {
  const sortie = []
  const marche = (n, premier) => {
    if (n.nodeType === 3) return sortie.push(echapper(n.textContent.replace(/​/g, '')))
    if (n.nodeType !== 1) return
    const tag = n.tagName
    if (tag === 'BR') return sortie.push('\n')
    if (n.dataset?.hr) return sortie.push('<hr/>')
    if (n.dataset?.i) return sortie.push(`[${n.dataset.i}]`)
    let ouvre = ''
    let ferme = ''
    if (tag === 'DIV' || tag === 'P') { if (!premier) sortie.push('\n') }
    if (tag === 'B' || tag === 'STRONG' || /^(bold|[6-9]00)$/.test(n.style?.fontWeight)) { ouvre += '<b>'; ferme = '</b>' + ferme }
    if (tag === 'I' || tag === 'EM' || n.style?.fontStyle === 'italic') { ouvre += '<i>'; ferme = '</i>' + ferme }
    if (tag === 'U' || /underline/.test(n.style?.textDecorationLine ?? n.style?.textDecoration ?? '')) { ouvre += '<u>'; ferme = '</u>' + ferme }
    if (n.classList?.contains('trait')) { ouvre += '<em>'; ferme = '</em>' + ferme }
    const css = []
    const fs = /([\d.]+)(em|%)/.exec(n.style?.fontSize ?? '')
    if (fs) css.push(`font-size:${fs[2] === '%' ? (fs[1] / 100).toFixed(2) : fs[1]}em`)
    const coul = n.style?.color || (tag === 'FONT' ? n.getAttribute('color') : '')
    if (coul) css.push(`color:${hexDe(coul)}`)
    if (css.length) { ouvre += `<span style="${css.join(';')}">`; ferme = '</span>' + ferme }
    sortie.push(ouvre)
    let k = 0
    for (const c of n.childNodes) marche(c, k++ === 0 && premier)
    sortie.push(ferme)
  }
  let k = 0
  for (const c of racine.childNodes) marche(c, k++ === 0)
  return sortie.join('').replace(/<(\w+)([^>]*)><\/\1>/g, '')
}

/** Une espace si le curseur suit du texte sans espace (on n'accole pas « card. » et « Toughness. »). */
function espaceAvant(zone) {
  const s = getSelection()
  if (!s.rangeCount || !zone.contains(s.anchorNode)) return ''
  const n = s.anchorNode
  const avant = n.nodeType === 3 ? n.textContent.slice(0, s.anchorOffset) : ''
  const c = avant.slice(-1)
  // Chrome avale l'espace qui precede une insertion : on la remet sous forme d'espace insecable (relue comme une espace normale)
  return !c || c === '\u200b' || s.anchorOffset === 0 ? '' : '\u00a0'
}

/** Le champ de texte riche : on selectionne, on clique (gras, italique, souligne, taille, couleur, icones). Un bouton « </> » montre le code. */
function editeurRiche(label, cle, lignes = 5) {
  const c = carte()
  const zone = el('div', { class: 'editeur', 'data-champ': cle, contenteditable: 'true', spellcheck: 'true', role: 'textbox', 'aria-multiline': 'true', style: `min-height:${lignes * 1.5}em` })
  zone.innerHTML = versEditeur(c.contenu[cle])
  const code = el('textarea', { rows: lignes, hidden: true, style: 'font-family:monospace' })
  code.value = c.contenu[cle] ?? ''
  const pousse = () => { c.contenu[cle] = depuisEditeur(zone); changement() }
  zone.addEventListener('input', pousse)
  zone.addEventListener('paste', (e) => {
    e.preventDefault()
    document.execCommand('insertText', false, e.clipboardData.getData('text/plain'))
  })
  code.addEventListener('input', () => { c.contenu[cle] = code.value; zone.innerHTML = versEditeur(code.value); changement() })
  const cmd = (nom, val) => { zone.focus(); document.execCommand('styleWithCSS', false, nom === 'foreColor'); document.execCommand(nom, false, val); pousse() }
  const taille = (f) => {
    zone.focus()
    document.execCommand('styleWithCSS', false, false)
    document.execCommand('fontSize', false, '7')
    for (const fo of zone.querySelectorAll('font[size="7"]')) {
      const sp = el('span', { style: `font-size:${f}em` })
      for (const x of fo.querySelectorAll('[style*="font-size"]')) x.style.fontSize = ''
      sp.append(...fo.childNodes)
      fo.replaceWith(sp)
    }
    pousse()
  }
  const trait = () => {
    zone.focus()
    const s = getSelection()
    if (s.isCollapsed) return
    document.execCommand('insertHTML', false, `<span class="trait">${echapper(s.toString())}</span>`)
    pousse()
  }
  const icone = (nom) => {
    zone.focus()
    document.execCommand('insertHTML', false, `<span class="ico" contenteditable="false" data-i="${nom}">${ICONES[nom]}</span>&#8203;`)
    pousse()
  }
  const bouton = (txt, titre, fn, extra = {}) => el('button', { class: 'btn petit', type: 'button', title: titre, onmousedown: (e) => e.preventDefault(), onclick: fn, ...extra }, txt)
  const selTaille = el('select', { class: 'petit', title: 'Taille de la sélection', onmousedown: () => {}, onchange: (e) => { if (e.target.value) taille(Number(e.target.value)); e.target.value = '' } },
    el('option', { value: '' }, 'Taille'), ...[[0.7, '70 %'], [0.85, '85 %'], [1, '100 % (normale)'], [1.25, '125 %'], [1.5, '150 %'], [2, '200 %']].map(([v, n]) => el('option', { value: v }, n)))
  const couleur = el('input', { type: 'color', value: '#cc0000', title: 'Couleur de la sélection', onchange: (e) => cmd('foreColor', e.target.value) })
  const boutonStyles = el('button', { class: 'btn petit bouton-styles', type: 'button', title: 'Styles de texte : menu, ou tape « / » dans le texte', onmousedown: (e) => e.preventDefault(), onclick: () => (api.menuOuvert ? (api.fermerMenu(), (api.menuOuvert = false)) : (api.ouvrirMenu(), (api.menuOuvert = true))) }, 'Styles ▾')
  const barre = el('div', { class: 'outils' },
    boutonStyles,
    bouton(el('b', {}, 'G'), 'Gras (Ctrl+B)', () => cmd('bold')),
    bouton(el('i', {}, 'I'), 'Italique (Ctrl+I)', () => cmd('italic')),
    bouton(el('u', {}, 'S'), 'Souligné (Ctrl+U)', () => cmd('underline')),
    selTaille, couleur,
    bouton('Trait', 'Police des traits', trait),
    bouton('✕', 'Retirer la mise en forme de la sélection', () => cmd('removeFormat')),
    bouton('</>', 'Voir / modifier le code (balises)', () => { code.hidden = !code.hidden; zone.hidden = !code.hidden; if (!code.hidden) code.value = c.contenu[cle] ?? '' }))
  const icones = el('div', { class: 'outils' })
  for (const [nom, titre] of ICONES_BARRE) icones.append(bouton(ICONES[nom], titre, () => icone(nom), { style: 'font-family:ChampionsIcons' }))
  const conteneur = el('div', { class: 'champ-riche' }, el('label', {}, label), barre, icones, zone, code)
  const api = {
    zone, langue: () => c.langue, perso: () => projet.styles ?? [], menuOuvert: false,
    ajouterPerso: (p) => { (projet.styles ??= []).push(p); sauvegarderPlusTard(); message('Style créé.') },
    supprimerPerso: (id) => { projet.styles = (projet.styles ?? []).filter((x) => x.id !== id); sauvegarderPlusTard() },
    // une insertion garde un espace avec ce qui precede, et le curseur ressort des balises (l'italique ne « fuit » pas sur la suite)
    inserer: (h) => { zone.focus(); document.execCommand('insertHTML', false, espaceAvant(zone) + versEditeur(h) + '\u200b') },
    nommee: (fn) => { zone.focus(); document.execCommand('insertHTML', false, espaceAvant(zone) + versEditeur(fn(getSelection().toString())) + '\u200b') },
    format: (nom) => { if (nom === 'em') trait(); else cmd(nom === 'i' ? 'italic' : 'bold') },
    enveloppe: (p) => { zone.focus(); document.execCommand('insertHTML', false, versEditeur(enveloppePerso(p, echapper(getSelection().toString() || p.nom))) + '\u200b') },
    pousse,
  }
  brancherStyles(conteneur, api)
  return conteneur
}

function boiteImage(titre, obj, avecBascule) {
  const c = carte()
  const fichier = el('input', { type: 'file', accept: 'image/*' })
  fichier.addEventListener('change', async () => {
    const f = fichier.files[0]
    if (!f) return
    obj(c).blob = f
    if (avecBascule) ciblePointeur = avecBascule
    changement()
    construireFormulaire()
  })
  const parts = [
    el('label', {}, titre, fichier),
    curseur('Zoom', obj, 'zoom', 0.3, 4, 0.01, 1),
    el('div', { class: 'rang' }, curseur('Décalage X', obj, 'x', -1500, 1500, 1, 0), curseur('Décalage Y', obj, 'y', -2200, 2200, 1, 0)),
    curseur('Rotation (°)', obj, 'rotation', -180, 180, 1, 0),
  ]
  if (obj(c).blob) {
    parts.push(el('div', { class: 'rang' },
      el('button', { class: 'btn petit', type: 'button', onclick: () => { ciblePointeur = avecBascule; majAide() } }, 'Déplacer à la souris'),
      el('button', { class: 'btn petit', type: 'button', onclick: () => ouvrirRecadrage(obj(c).blob, (nb) => { obj(c).blob = nb; changement(); construireFormulaire() }) }, 'Détourer / recadrer…'),
      el('button', { class: 'btn petit', type: 'button', onclick: () => { obj(c).blob = null; changement(); construireFormulaire() } }, 'Retirer')))
  }
  return parts
}

function appliquerPalette(c, spec, cle) {
  const roles = new Set(rolesDe(spec))
  c.couleurs = {}
  if (!cle) return
  const choix = ASPECTS[cle]
  const pal = typeof choix === 'string' ? PALETTES[choix] : choix ?? PALETTES[cle]
  for (const [k, v] of Object.entries(pal)) {
    const role = k === 'splash' ? 'splash_color' : k
    if (roles.has(role)) c.couleurs[role] = v
  }
}
function joliNom(slug) {
  return slug.replace(/_(hero|nemesis|campaign_hero)$/, '').replace(/[_-]+/g, ' ').replace(/\b\w/g, (m) => m.toUpperCase())
}

function construireFormulaire() {
  const c = carte()
  const racine = $('#champs')
  racine.replaceChildren()
  if (!c) return
  const spec = TYPES[c.type]
  $('#type').value = c.type
  const f = []
  {
    const dossier = el('input', { type: 'text', list: 'dossiers-connus', placeholder: 'ex. Valkyrie', value: c.dossier ?? '' })
    dossier.addEventListener('input', () => { c.dossier = dossier.value.trim(); changement() })
    f.push(el('label', {}, 'Dossier (un héros, un set…)', dossier))
  }

  // texte
  const texte = [t('Titre', 'titre'), coche('Carte unique (✦)', (x) => x.contenu, 'unique')]
  if (aElement(spec, 'typestr')) texte.push(t('Libellé du type (vide = automatique)', 'typeTexte'))
  if (aElement(spec, 'traits')) texte.push(t('Traits (séparés par des points)', 'traits'))
  if (aElement(spec, 'rules')) {
    texte.push(editeurRiche('Règles', 'regles', 6))
  }
  if (aElement(spec, 'quote')) texte.push(editeurRiche('Citation', 'citation', 3))
  if (aElement(spec, 'rules')) {
    const auto = !(Number(c.contenu.echelleTexte) > 0)
    const r = el('input', { type: 'range', min: 40, max: 130, step: 1, value: auto ? 100 : Math.round(c.contenu.echelleTexte * 100) })
    const val = el('span', { class: 'aide' }, auto ? 'automatique' : r.value + ' %')
    r.addEventListener('input', () => { c.contenu.echelleTexte = Number(r.value) / 100; val.textContent = r.value + ' %'; changement() })
    texte.push(el('label', {}, el('span', { class: 'rang' }, 'Taille des règles et de la citation', val), r,
      el('button', { class: 'btn petit', type: 'button', onclick: () => { c.contenu.echelleTexte = 0; changement(); construireFormulaire() } }, 'Automatique (réduit pour tenir)')))
  }
  if (aElement(spec, 'villainstagenew')) texte.push(t('Étape du méchant (I, II, A, B…)', 'etape'))
  if (aElement(spec, 'set-line')) texte.push(t('Ligne d’ensemble', 'ligneEnsemble'))
  if (aElement(spec, 'c-line')) texte.push(t('Créateur / mention', 'createur'))
  f.push(section('Texte', true, ...texte))

  // nombres
  const N = []
  const A = (cls, label, cle, etoile = true) => aElement(spec, cls) && N.push(nombre(label, cle, etoile))
  A('paycost cost', 'Coût', 'cout')
  A('thw sch cost', 'Contrer / manigance (THW / SCH)', 'thw')
  aElement(spec, 'thwconsequential') && N.push(liste('Dégâts conséquents (contrer)', (x) => x.contenu, 'thwConseq', [0, 1, 2, 3, 4, 5].map((n) => [n, n]), Number))
  A('atk cost', 'Attaque (ATK)', 'atk')
  aElement(spec, 'atkconsequential') && N.push(liste('Dégâts conséquents (attaque)', (x) => x.contenu, 'atkConseq', [0, 1, 2, 3, 4, 5].map((n) => [n, n]), Number))
  A('def cost', 'Défense (DEF)', 'def')
  A('rec cost', 'Récupération (REC)', 'rec')
  A('hp cost', 'Points de vie', 'pv')
  A('handsize', 'Taille de main', 'tailleMain', false)
  A('startingthreatwrap', 'Menace de départ', 'menaceDepart')
  A('targetthreat cost', 'Menace cible', 'menaceCible', false)
  A('acceleration', 'Accélération', 'acceleration', false)
  A('attachmentatknums cost', 'Attachement : bonus d’attaque', 'atkAttache')
  A('attachmentschnums cost', 'Attachement : bonus de manigance', 'schAttache')
  if (aElement(spec, 'mainschemephase cost')) N.push(el('div', { class: 'rang' }, t('Phase : numéro', 'phaseNumero'), t('Phase : lettre', 'phaseLettre')))
  if (N.length) f.push(section('Nombres', true, ...N))

  // renforts et ressources
  if (spec.renforts || spec.ressources) {
    const R = []
    if (spec.renforts) R.push(el('div', { class: 'nombre' }, liste('Icônes de renfort', (x) => x.contenu, 'renforts', [0, 1, 2, 3, 4, 5].map((n) => [n, n]), Number), coche('★', (x) => x.contenu, 'renfortEtoile')))
    if (spec.ressources) {
      for (let k = 0; k < 3; k++) {
        const ressources = () => (c.contenu.ressources = c.contenu.ressources?.length ? c.contenu.ressources : ['', '', ''])
        const s = el('select', {}, GENRES_RESSOURCE.map(([v, n]) => el('option', { value: v }, n)))
        s.value = ressources()[k] ?? ''
        s.addEventListener('change', () => { ressources()[k] = s.value; changement() })
        R.push(el('label', {}, `Ressource ${k + 1}`, s))
      }
    }
    f.push(section('Renforts et ressources', true, ...R))
  }

  // couleurs
  const roles = rolesDe(spec)
  if (roles.length) {
    const noms = Object.keys(PALETTES)
    const famille = spec.famille === 'villain' ? noms.filter((n) => PALETTES[n].background_upper) : noms.filter((n) => PALETTES[n].left_color)
    const preset = el('select', {}, el('option', { value: '' }, '— couleurs du gabarit —'))
    if (spec.famille !== 'villain') preset.append(el('optgroup', { label: 'Aspects' }, Object.keys(ASPECTS).map((n) => el('option', { value: n }, n))))
    preset.append(el('optgroup', { label: spec.famille === 'villain' ? 'Méchants et rencontres' : 'Héros' }, famille.sort().map((n) => el('option', { value: n }, joliNom(n)))))
    preset.value = c.preset ?? ''
    preset.addEventListener('change', () => {
      c.preset = preset.value
      appliquerPalette(c, spec, preset.value)
      construireFormulaire()
      changement()
    })
    const grille = el('div', { class: 'couleurs' })
    for (const r of roles) {
      const i = el('input', { type: 'color', value: hex6(couleurDe(c, spec, r)) })
      i.addEventListener('input', () => { c.couleurs[r] = i.value; c.preset = ''; changement() })
      grille.append(el('label', {}, ROLES_COULEURS[r], i))
    }
    f.push(section('Couleurs', false, el('label', {}, 'Préréglage', preset), grille,
      el('button', { class: 'btn petit', type: 'button', onclick: () => { c.couleurs = {}; c.preset = ''; construireFormulaire(); changement() } }, 'Revenir aux couleurs du gabarit')))
  }

  // illustration
  f.push(section('Illustration', false, ...boiteImage('Image derrière la carte', (x) => x.art, 'art'), el('hr'), ...boiteImage('Premier plan (devant le cadre)', (x) => x.artDevant, 'artDevant')))

  f.push(sectionLibres())

  // tete d'angle
  if (spec.tete) {
    f.push(section('Tête d’angle', false,
      ...boiteImage('Image de la tête (cadrage carré)', (x) => x.tete, 'tete').slice(0, 1),
      coche('Afficher la tête', (x) => x.tete, 'afficher'),
      spec.tete.splash ? coche('Éclat en étoile', (x) => x.tete, 'etoile') : null,
      curseur('Zoom', (x) => x.tete, 'zoom', 0.2, 2.5, 0.01, 0.8),
      el('div', { class: 'rang' }, curseur('Décalage X', (x) => x.tete, 'x', -400, 1500, 1, -19), curseur('Décalage Y', (x) => x.tete, 'y', -400, 2150, 1, 232)),
      curseur('Rotation (°)', (x) => x.tete, 'rotation', -180, 180, 1, 0),
      c.tete.blob ? el('button', { class: 'btn petit', type: 'button', onclick: () => { ciblePointeur = 'tete'; majAide() } }, 'Déplacer à la souris') : null,
      c.tete.blob ? el('button', { class: 'btn petit', type: 'button', onclick: () => ouvrirRecadrage(c.tete.blob, (nb) => { c.tete.blob = nb; changement(); construireFormulaire() }, { carre: true }) }, 'Détourer / recadrer…') : null))
  }

  // style de cadre et options
  f.push(section('Style du cadre', false,
    liste('Style', (x) => x, 'cadre', [['officiel', 'Officiel (gabarit du jeu)'], ['sombre', 'Cadre sombre'], ['illustration', 'Pleine illustration (sans cadre)']], (v) => v),
    el('div', { class: 'aide' }, '« Cadre sombre » remplace les couleurs par un gris-bleu foncé avec des accents dorés (tu peux encore les modifier dans Couleurs). « Pleine illustration » enlève le cadre : l’image remplit la carte et le texte repose sur des panneaux translucides.'),
    TYPES_SANS_FISSURES.has(c.type) ? coche('Fissures dans le cadre', (x) => x, 'fissures') : null))

  racine.append(...f)
  majAide()
}
function majAide() {
  const cible = { art: 'l’illustration', artDevant: 'le premier plan', tete: 'la tête d’angle' }[ciblePointeur]
  $('#aide-toile').textContent = `Glisse sur l’aperçu pour déplacer ${cible} (molette : zoom).`
}

// ---------------------------------------------------------------- liste
let filtreListe = ''
const ouverts = new Set() // dossiers replies : on garde ceux qui sont fermes
const fermes = new Set()
function majListe() {
  const l = $('#liste')
  const q = filtreListe.trim().toLowerCase()
  const visible = (c) => !q || [c.contenu.titre, c.contenu.regles, c.contenu.traits, c.dossier, NOMS[c.type]].some((t) => String(t ?? '').toLowerCase().includes(q))
  const groupes = new Map()
  for (const c of projet.cartes) {
    if (!visible(c)) continue
    const d = c.dossier || ''
    if (!groupes.has(d)) groupes.set(d, [])
    groupes.get(d).push(c)
  }
  const noms = [...groupes.keys()].sort((x, y) => (x === '' ? 1 : y === '' ? -1 : x.localeCompare(y)))
  const avecDossiers = noms.length > 1 || (noms.length === 1 && noms[0] !== '')
  const noeuds = []
  for (const d of noms) {
    const cartes = groupes.get(d)
    if (avecDossiers) {
      const ferme = fermes.has(d) && !q
      noeuds.push(el('button', { class: 'dossier', type: 'button', onclick: () => { fermes.has(d) ? fermes.delete(d) : fermes.add(d); majListe() } },
        `${ferme ? '▸' : '▾'} ${d || 'Sans dossier'}`, el('small', {}, ` (${cartes.length})`)))
      if (ferme) continue
    }
    for (const c of cartes) {
      noeuds.push(el('button', { type: 'button', 'aria-current': String(c.id === projet.courante), onclick: () => choisir(c.id) },
        el('span', {}, c.contenu.titre || '(sans titre)'), el('small', {}, `${NOMS[c.type] ?? c.type} · ${c.langue.toUpperCase()}`)))
    }
  }
  if (!noeuds.length) noeuds.push(el('div', { class: 'aide' }, 'Aucune carte ne correspond.'))
  l.replaceChildren(...noeuds)
  // dossiers deja utilises : propositions du champ « Dossier »
  const dl = $('#dossiers-connus')
  if (dl) dl.replaceChildren(...[...new Set(projet.cartes.map((c) => c.dossier).filter(Boolean))].sort().map((d) => el('option', { value: d })))
  majModeles()
}
function majModeles() {
  const s = $('#modeles')
  if (!s) return
  const v = s.value
  s.replaceChildren(el('option', { value: '' }, `— modèles (${(projet.modeles ?? []).length}) —`), ...(projet.modeles ?? []).map((m) => el('option', { value: m.id }, m.nom)))
  s.value = v
}
function choisir(id) {
  validerHistorique()
  projet.courante = id
  { const h = histoDe(id); h.ref ??= cloner(carte()) }
  majListe()
  majBoutonsLangue()
  construireFormulaire()
  dessiner()
  sauvegarderPlusTard()
  majBoutonsHistorique()
}
function ajouter(c) {
  projet.cartes.push(c)
  choisir(c.id)
}

// ---------------------------------------------------------------- exports
function telecharger(blob, nom) {
  const a = el('a', { href: URL.createObjectURL(blob), download: nom })
  document.body.append(a)
  a.click()
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove() }, 1000)
}
const aBlob = (toile, type, q) => new Promise((ok) => toile.toBlob(ok, type, q))
const nomFichier = (c, suffixe = '') => (c.contenu.titre || 'carte').normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^\w]+/g, '_').replace(/^_|_$/g, '') + suffixe

/** Ajoute un fond perdu en etirant les bords de la carte. */
function avecFondPerdu(toile, marge) {
  const w = toile.width
  const h = toile.height
  const o = document.createElement('canvas')
  o.width = w + 2 * marge
  o.height = h + 2 * marge
  const x = o.getContext('2d')
  x.drawImage(toile, marge, marge)
  x.drawImage(toile, 0, 0, w, 1, marge, 0, w, marge)
  x.drawImage(toile, 0, h - 1, w, 1, marge, h + marge, w, marge)
  x.drawImage(toile, 0, 0, 1, h, 0, marge, marge, h)
  x.drawImage(toile, w - 1, 0, 1, h, w + marge, marge, marge, h)
  x.drawImage(toile, 0, 0, 1, 1, 0, 0, marge, marge)
  x.drawImage(toile, w - 1, 0, 1, 1, w + marge, 0, marge, marge)
  x.drawImage(toile, 0, h - 1, 1, 1, 0, h + marge, marge, marge)
  x.drawImage(toile, w - 1, h - 1, 1, 1, w + marge, h + marge, marge, marge)
  return o
}

function dialogueExport() {
  return new Promise((ok) => {
    const c = carte()
    const format = el('select', {}, ['png', 'jpeg', 'webp'].map((v) => el('option', { value: v }, v.toUpperCase())))
    const largeur = el('input', { type: 'number', min: 200, max: 6000, value: TYPES[c.type].largeur })
    const perdu = el('input', { type: 'checkbox' })
    const boite = el('dialog', {}, el('div', { class: 'panneau', style: 'min-width:280px' },
      el('h2', {}, 'Exporter'),
      el('label', {}, 'Format', format),
      el('label', {}, `Largeur (px) — taille d’origine ${TYPES[c.type].largeur}`, largeur),
      el('label', { class: 'ligne' }, perdu, 'Fond perdu de 3 mm (bords étirés)'),
      el('div', { class: 'rang' },
        el('button', { class: 'btn', type: 'button', onclick: () => { boite.close(); ok(null) } }, 'Annuler'),
        el('button', { class: 'btn principal', type: 'button', onclick: () => { boite.close(); ok({ format: format.value, largeur: Number(largeur.value), perdu: perdu.checked }) } }, 'Exporter'))))
    document.body.append(boite)
    boite.addEventListener('close', () => boite.remove())
    boite.showModal()
  })
}
async function sortie(toile, o) {
  let t = toile
  if (o.largeur && o.largeur !== toile.width) {
    const k = o.largeur / toile.width
    const r = document.createElement('canvas')
    r.width = Math.round(toile.width * k)
    r.height = Math.round(toile.height * k)
    const x = r.getContext('2d')
    x.imageSmoothingQuality = 'high'
    x.drawImage(toile, 0, 0, r.width, r.height)
    t = r
  }
  if (o.perdu) t = avecFondPerdu(t, Math.round((t.width / (toile.width > toile.height ? 88 : 63)) * 3))
  return aBlob(t, 'image/' + o.format, 0.95)
}
async function exporter(deuxLangues) {
  const c = carte()
  const o = await dialogueExport()
  if (!o) return
  message('Export…')
  const langues = deuxLangues ? ['fr', 'en'] : [c.langue]
  for (const l of langues) {
    const blob = await sortie(await rendreCarte(c, l), o)
    telecharger(blob, nomFichier(c, deuxLangues ? '_' + l : '') + '.' + (o.format === 'jpeg' ? 'jpg' : o.format))
  }
  message('Export terminé.')
}
async function planchePourImprimer() {
  message('Préparation de la planche…')
  const images = []
  for (const c of projet.cartes) {
    const toile = await rendreCarte(c)
    const k = 750 / toile.width
    const r = document.createElement('canvas')
    r.width = 750
    r.height = Math.round(toile.height * k)
    r.getContext('2d').drawImage(toile, 0, 0, r.width, r.height)
    // les cartes paysage sont tournees pour tenir sur la planche
    let sortieToile = r
    if (r.width > r.height) {
      sortieToile = document.createElement('canvas')
      sortieToile.width = r.height
      sortieToile.height = r.width
      const x = sortieToile.getContext('2d')
      x.translate(r.height, 0)
      x.rotate(Math.PI / 2)
      x.drawImage(r, 0, 0)
    }
    images.push(sortieToile.toDataURL('image/jpeg', 0.92))
  }
  const w = window.open('', '_blank')
  if (!w) return message('Le navigateur a bloqué la fenêtre d’impression.')
  w.document.write(`<!doctype html><meta charset="utf-8"><title>Planche d'impression</title><style>
    @page { size: A4; margin: 10mm }
    body { margin: 0; display: grid; grid-template-columns: repeat(3, 63mm); gap: 0; justify-content: center }
    img { width: 63mm; height: 88mm; display: block; break-inside: avoid }
    @media screen { body { background: #ccc; padding: 10mm } }
  </style>${images.map((s) => `<img src="${s}">`).join('')}<script>onload=()=>setTimeout(()=>print(),400)<\/script>`)
  w.document.close()
  message('')
}
async function plancheTTS() {
  const cartes = projet.cartes.filter((c) => !TYPES[c.type].paysage).slice(0, 69)
  if (!cartes.length) return message('Aucune carte portrait à mettre sur la planche.')
  message('Préparation de la planche TTS…')
  const L = 400
  const H = 574
  const colonnes = 10
  const lignes = Math.ceil(cartes.length / colonnes)
  const o = document.createElement('canvas')
  o.width = colonnes * L
  o.height = Math.max(2, lignes) * H
  const x = o.getContext('2d')
  x.imageSmoothingQuality = 'high'
  for (const [i, c] of cartes.entries()) x.drawImage(await rendreCarte(c), (i % colonnes) * L, Math.floor(i / colonnes) * H, L, H)
  telecharger(await aBlob(o, 'image/png'), 'planche_TTS.png')
  message(`Planche TTS : ${cartes.length} carte(s), ${colonnes} colonnes (taille de cellule ${L} × ${H}).`)
}

// ---------------------------------------------------------------- projet (fichier)
async function exporterProjet() {
  const cartes = []
  for (const c of projet.cartes) cartes.push(await serialiser(c))
  const modeles = []
  for (const m of projet.modeles ?? []) modeles.push({ id: m.id, nom: m.nom, carte: await serialiser(m.carte) })
  telecharger(new Blob([JSON.stringify({ format: 'createur-cartes', version: 2, cartes, modeles, styles: projet.styles ?? [] })], { type: 'application/json' }), 'cartes.json')
}

// ---------------------------------------------------------------- import des fichiers du Card Maker de reference
// Leur fichier : un .json par carte (UTF-8 avec BOM, cles a plat, images en data URL) ; leur « Save .zip » = un .json par carte dans un zip.
const vrai = (v) => v != null && v !== '' && v !== '0' && v !== 'none' && v !== false && v !== 'false'
const texteJson = (buf) => new TextDecoder('utf-8').decode(buf).replace(/^\uFEFF/, '')

/** Les fichiers d'un .zip (methodes 0 et 8) : [{ nom, octets }]. */
async function lireZip(buf) {
  const v = new DataView(buf)
  let fin = buf.byteLength - 22
  while (fin >= 0 && v.getUint32(fin, true) !== 0x06054b50) fin--
  if (fin < 0) throw new Error('zip illisible')
  const n = v.getUint16(fin + 10, true)
  let p = v.getUint32(fin + 16, true)
  const sortie = []
  for (let i = 0; i < n; i++) {
    const methode = v.getUint16(p + 10, true)
    const taille = v.getUint32(p + 20, true)
    const ln = v.getUint16(p + 28, true)
    const lx = v.getUint16(p + 30, true)
    const lc = v.getUint16(p + 32, true)
    const debut = v.getUint32(p + 42, true)
    const nom = new TextDecoder().decode(new Uint8Array(buf, p + 46, ln))
    p += 46 + ln + lx + lc
    if (nom.endsWith('/')) continue
    const dn = v.getUint16(debut + 26, true)
    const dx = v.getUint16(debut + 28, true)
    const brut = new Uint8Array(buf, debut + 30 + dn + dx, taille)
    let octets = brut
    if (methode === 8) octets = new Uint8Array(await new Response(new Blob([brut]).stream().pipeThrough(new DecompressionStream('deflate-raw'))).arrayBuffer())
    else if (methode !== 0) continue
    sortie.push({ nom, octets })
  }
  return sortie
}

/** Une carte de la reference -> une carte a nous. */
async function carteDepuisReference(j) {
  const type = TYPES[j.selectType] ? j.selectType : 'ally'
  const spec = TYPES[type]
  const langue = /^\s*(taille de main|hand size)/i.test(j.setline ?? '') && /taille/i.test(j.setline) ? 'fr' : 'en'
  const c = nouvelleCarte(type, langue)
  const titre = String(j.title ?? '')
  const ct = c.contenu
  ct.unique = /<code>\s*u\s*<\/code>/i.test(titre)
  ct.titre = titre.replace(/<code>\s*u\s*<\/code>/gi, '')
  ct.typeTexte = j.typestr ?? ''
  ct.regles = j.rules ?? ''
  ct.citation = j.quote ?? ''
  ct.traits = j.traits ?? ''
  ct.ligneEnsemble = j.setline ?? ''
  ct.createur = j.copyright ?? ''
  ct.etape = j.villainstagenew ?? ''
  const num = (cle, ref) => { ct[cle] = j[ref] == null ? '' : String(j[ref]) }
  num('cout', 'paycost'); num('thw', 'thw'); num('atk', 'atk'); num('def', 'def'); num('rec', 'rec'); num('pv', 'hp'); num('tailleMain', 'handsize')
  num('menaceDepart', 'startingthreat'); num('menaceCible', 'targetthreat'); num('acceleration', 'acceleration')
  num('atkAttache', 'attatk'); num('schAttache', 'attsch')
  ct.coutEtoile = vrai(j.paycostStar); ct.thwEtoile = vrai(j.thwStar); ct.atkEtoile = vrai(j.atkStar); ct.defEtoile = vrai(j.defStar)
  ct.recEtoile = vrai(j.recStar); ct.pvEtoile = vrai(j.hpStar); ct.menaceDepartEtoile = vrai(j.startingthreatStar)
  ct.atkAttacheEtoile = vrai(j.attatkStar); ct.schAttacheEtoile = vrai(j.attschStar)
  ct.thwConseq = Number(j.thwCon) || 0
  ct.atkConseq = Number(j.atkCon) || 0
  const m = /^\s*(\d*)\s*([a-z]?)\s*$/i.exec(String(j.mainschemenumber ?? ''))
  ct.phaseNumero = m?.[1] ?? ''
  ct.phaseLettre = (m?.[2] || (type === 'main_scheme_b' ? 'B' : type === 'main_scheme_a' ? 'A' : '')).toUpperCase()
  ct.renforts = Number(j.boosticons) || 0
  ct.renfortEtoile = vrai(j.booststar)
  ct.ressources = [1, 2, 3].map((k) => (vrai(j['resource' + k]) ? j['resource' + k] : ''))
  c.fissures = j.togglecracks !== false
  for (const [cle, dest] of [['photo', 'art'], ['photofront', 'artDevant']]) {
    if (typeof j[cle] === 'string' && j[cle].startsWith('data:')) c[dest].blob = await dataUrlVersBlob(j[cle])
    c[dest].zoom = Number(j[cle + 'zoom']) || 1
    c[dest].x = Number(j[cle + 'x']) || 0
    c[dest].y = Number(j[cle + 'y']) || 0
    c[dest].rotation = Number(j[cle + 'rotate']) || 0
  }
  if (typeof j.headshot === 'string' && j.headshot.startsWith('data:')) c.tete.blob = await dataUrlVersBlob(j.headshot)
  c.tete.afficher = j.showsplash !== false
  c.tete.etoile = vrai(j.starsplash)
  c.tete.zoom = Number(j.headshotzoom) || 0.8
  c.tete.x = Number(j.splashx ?? -19)
  c.tete.y = Number(j.splashy ?? 232)
  c.tete.rotation = Number(j.splashrotate) || 0
  for (const r of rolesDe(spec)) {
    const v = j[r === 'splash_color' ? 'splash' : r]
    if (/^#[0-9a-f]{6}$/i.test(v ?? '')) c.couleurs[r] = v
  }
  return c
}

/** Importe des fichiers : les notres (.json), ceux du Card Maker de reference (.json d'une carte, .zip de cartes). */
async function importerFichiers(fichiers) {
  let n = 0
  const ajoutees = []
  const traiter = async (j) => {
    if (Array.isArray(j)) { for (const x of j) await traiter(x); return }
    if (j?.format === 'createur-cartes') {
      for (const st of j.styles ?? []) { projet.styles ??= []; if (!projet.styles.some((x) => x.id === st.id)) projet.styles.push(st) }
      for (const m of j.modeles ?? []) { projet.modeles ??= []; projet.modeles.push({ id: nouvelId(), nom: m.nom, carte: await deserialiser(m.carte) }) }
      for (const x of j.cartes) {
        if (!TYPES[x.type]) continue
        const c = await deserialiser(x)
        c.id = nouvelId()
        ajoutees.push(c)
      }
    } else if (j?.selectType) ajoutees.push(await carteDepuisReference(j))
  }
  for (const f of fichiers) {
    const buf = await f.arrayBuffer()
    if (/\.zip$/i.test(f.name)) {
      for (const e of await lireZip(buf)) if (/\.json$/i.test(e.nom)) { try { await traiter(JSON.parse(texteJson(e.octets))); n++ } catch {} }
    } else {
      await traiter(JSON.parse(texteJson(buf)))
      n++
    }
  }
  if (!ajoutees.length) throw new Error('aucune carte reconnue dans ces fichiers')
  projet.cartes.push(...ajoutees)
  choisir(ajoutees[ajoutees.length - 1].id)
  message(`${ajoutees.length} carte(s) importée(s).`)
}

// ---------------------------------------------------------------- souris sur l'apercu
function brancherToile() {
  const toile = $('#toile')
  const sur = $('#surcouche')
  brancherSurcouche(sur, toile)
  let depart = null
  let libre = null
  let bouge = false
  const cible = () => {
    const c = carte()
    return ciblePointeur === 'tete' ? c.tete : ciblePointeur === 'artDevant' ? c.artDevant : c.art
  }
  sur.addEventListener('pointerdown', (e) => {
    const c = carte()
    if (!c) return
    bouge = false
    libre = commencerGlisser(e)
    if (libre) {
      sur.setPointerCapture(e.pointerId)
      sur.classList.add('glisse')
      return
    }
    // un clic dans le vide : plus de calque choisi ; un glisser deplace l'illustration (ou la tete)
    if (!cible().blob && ciblePointeur !== 'tete') { depart = { x: e.clientX, y: e.clientY, clic: true }; sur.setPointerCapture(e.pointerId); return }
    depart = { x: e.clientX, y: e.clientY, ox: cible().x, oy: cible().y }
    sur.setPointerCapture(e.pointerId)
    sur.classList.add('glisse')
  })
  sur.addEventListener('pointermove', (e) => {
    if (libre) { bouge = true; libre.deplacer(e); return }
    if (!depart || depart.clic) return
    bouge = true
    const k = toile.width / toile.getBoundingClientRect().width
    const o = cible()
    // une carte paysage est dessinee dans son repere : le glisser suit l'ecran
    o.x = Math.round(depart.ox + (e.clientX - depart.x) * k)
    o.y = Math.round(depart.oy + (e.clientY - depart.y) * k)
    changement()
  })
  const fin = (e) => {
    const etaitClic = !bouge
    if (libre) libre.fin()
    else if (depart && bouge) construireFormulaire()
    if (etaitClic && !libre && e.type === 'pointerup') {
      // clic sans glisser sur la carte : on choisit rien, ou on edite l'element touche
      choisirCalque(null)
      construireFormulaire()
      clicSurCarte(e, toile)
    }
    depart = null
    libre = null
    sur.classList.remove('glisse')
  }
  sur.addEventListener('pointerup', fin)
  sur.addEventListener('pointercancel', fin)
  sur.addEventListener('wheel', (e) => {
    const c = carte()
    if (!c) return
    if (molette(e)) { e.preventDefault(); clearTimeout(brancherToile.t); brancherToile.t = setTimeout(construireFormulaire, 300); return }
    if (!cible().blob && ciblePointeur !== 'tete') return
    e.preventDefault()
    const o = cible()
    o.zoom = Math.max(0.2, Math.min(4, o.zoom * (e.deltaY < 0 ? 1.05 : 1 / 1.05)))
    changement()
    clearTimeout(brancherToile.t)
    brancherToile.t = setTimeout(construireFormulaire, 300)
  }, { passive: false })
  // glisser-deposer d'images sur l'apercu : chacune devient un calque PNG libre
  sur.addEventListener('dragover', (e) => e.preventDefault())
  sur.addEventListener('drop', (e) => {
    e.preventDefault()
    const fs = [...e.dataTransfer.files].filter((x) => x.type.startsWith('image/'))
    if (fs.length && carte()) ajouterFichiers(fs)
  })
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && !e.target.isContentEditable && !/^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return
    if (touche(e)) e.preventDefault()
  })
}

// ---------------------------------------------------------------- demarrage
function brancherEtat() {
  Object.assign(S, {
    carte, projet: () => projet, types: TYPES, changement, reconstruire: () => construireFormulaire(), message, imageDe,
    imageSync: (b) => (b ? imagesPretes.get(b) ?? null : null), rendre: rendreCarte, choisir: (id) => choisir(id),
    changerLangueDe: async (c, l) => { c.contenu = contenuDansLangue(c, l); c.langue = l },
  })
}

function majBoutonsLangueUI() {
  $('#ui-en').setAttribute('aria-pressed', String(langueUI() === 'en'))
  $('#ui-fr').setAttribute('aria-pressed', String(langueUI() === 'fr'))
}

async function demarrer() {
  demarrerI18n(langueMemorisee())
  $('#ui-en').addEventListener('click', () => { changerLangueUI('en'); majBoutonsLangueUI() })
  $('#ui-fr').addEventListener('click', () => { changerLangueUI('fr'); majBoutonsLangueUI() })
  majBoutonsLangueUI()
  const [types, palettes] = await Promise.all([
    fetch(BASE + 'donnees/types.json').then((r) => r.json()),
    fetch(BASE + 'donnees/palettes.json').then((r) => r.json()),
    chargerPolices(BASE + 'polices/'),
    chargerTraits(BASE + 'donnees/'),
    chargerStyles(BASE + 'donnees/'),
  ]).then((r) => [r[0], r[1]])
  TYPES = types
  PALETTES = palettes
  brancherEtat()
  const sel = $('#type')
  for (const [titre, ids] of GROUPES) {
    sel.append(el('optgroup', { label: titre }, ids.filter((i) => TYPES[i]).map((i) => el('option', { value: i }, NOMS[i] ?? TYPES[i].etiquette))))
  }
  sel.addEventListener('change', () => {
    const c = carte()
    c.type = sel.value
    c.couleurs = {}
    c.preset = ''
    // valeurs propres au type (numero de phase...) : on garde le texte, on remet les nombres par defaut manquants
    const d = valeursParDefaut(c.type, c.langue)
    for (const k of ['phaseLettre']) c.contenu[k] = d[k]
    construireFormulaire()
    changement()
  })
  const sauve = await lireProjet()
  if (sauve?.cartes?.length) projet = sauve
  else projet = { cartes: [nouvelleCarte('ally', 'en')], courante: null }
  projet.cartes = projet.cartes.filter((c) => TYPES[c.type])
  if (!projet.cartes.length) projet.cartes = [nouvelleCarte('ally', 'en')]
  for (const c of projet.cartes) { c.libres ??= []; c.cadre ??= 'officiel'; c.dossier ??= '' }
  if (!projet.cartes.some((c) => c.id === projet.courante)) projet.courante = projet.cartes[0].id

  $('#lang-fr').addEventListener('click', () => changerLangue('fr'))
  $('#lang-en').addEventListener('click', () => changerLangue('en'))
  $('#c-nouvelle').addEventListener('click', () => ajouter(nouvelleCarte(carte()?.type ?? 'ally', carte()?.langue ?? 'en')))
  $('#c-dupliquer').addEventListener('click', () => {
    const copie = { ...cloner(carte()), id: nouvelId() }
    copie.contenu.titre += ' (copie)'
    ajouter(copie)
  })
  $('#c-supprimer').addEventListener('click', () => {
    const c = carte()
    if (!c || !confirm(tr(`Supprimer « ${c.contenu.titre || 'cette carte'} » ?`))) return
    projet.cartes = projet.cartes.filter((x) => x.id !== c.id)
    if (!projet.cartes.length) projet.cartes.push(nouvelleCarte('ally', c.langue ?? 'en'))
    choisir(projet.cartes[0].id)
  })
  $('#recherche').addEventListener('input', (e) => { filtreListe = e.target.value; majListe() })
  $('#p-versions').addEventListener('click', () => ouvrirVersions((p) => { projet = p; projet.cartes = projet.cartes.filter((c) => TYPES[c.type]); for (const c of projet.cartes) { c.libres ??= []; c.cadre ??= 'officiel'; c.dossier ??= '' } historiques.clear(); choisir(projet.cartes.some((c) => c.id === projet.courante) ? projet.courante : projet.cartes[0].id); message('Version restaurée.') }))
  $('#p-remplacer').addEventListener('click', ouvrirRemplacer)
  $('#p-appliquer').addEventListener('click', () => ouvrirAppliquer(rolesDe))
  $('#m-enregistrer').addEventListener('click', () => { const n = prompt(tr('Nom du modèle'), carte().contenu.titre); if (n === null) return; enregistrerModele(n); majModeles(); sauvegarderPlusTard(); message('Modèle enregistré.') })
  $('#m-utiliser').addEventListener('click', async () => {
    const m = (projet.modeles ?? []).find((x) => x.id === $('#modeles').value)
    if (!m) return message('Choisis d’abord un modèle.')
    const c = { ...cloner(m.carte), id: nouvelId(), dossier: carte().dossier ?? '' }
    c.contenu.titre = TEXTES[c.langue]?.nouvelleCarte ?? c.contenu.titre
    ajouter(c)
  })
  $('#m-supprimer').addEventListener('click', () => { projet.modeles = (projet.modeles ?? []).filter((x) => x.id !== $('#modeles').value); majModeles(); sauvegarderPlusTard() })
  $('#b-annuler').addEventListener('click', annuler)
  $('#b-retablir').addEventListener('click', retablir)
  document.addEventListener('keydown', (e) => {
    if (!(e.ctrlKey || e.metaKey) || e.altKey) return
    const natif = e.target.isContentEditable || /^(INPUT|TEXTAREA)$/.test(e.target.tagName) && e.target.type !== 'range'
    if (natif) return
    const k = e.key.toLowerCase()
    if (k === 'z' && !e.shiftKey) { e.preventDefault(); annuler() } else if (k === 'y' || (k === 'z' && e.shiftKey)) { e.preventDefault(); retablir() }
  })
  $('#b-export').addEventListener('click', () => exporter(false))
  $('#b-export-2').addEventListener('click', () => exporter(true))
  $('#b-print').addEventListener('click', planchePourImprimer)
  $('#b-tts').addEventListener('click', plancheTTS)
  $('#p-exporter').addEventListener('click', exporterProjet)
  $('#p-importer').addEventListener('click', () => $('#p-fichier').click())
  $('#p-fichier').addEventListener('change', async (e) => {
    try { await importerFichiers([...e.target.files]) } catch (err) { message('Ouverture impossible : ' + err.message) }
    e.target.value = ''
  })
  brancherToile()
  choisir(projet.courante)
}
demarrer().catch((e) => message('Démarrage impossible : ' + e.message))
