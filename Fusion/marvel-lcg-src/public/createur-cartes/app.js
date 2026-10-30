// La page du créateur de cartes : liste de cartes, formulaire guidé par type, aperçu en direct, couleurs, illustration, tête d'angle,
// sauvegarde (IndexedDB + fichier .json), exports (PNG / JPG / WebP, FR + EN, planche à imprimer, planche TTS).
import { dessinerCarte, CHAMPS_VIDES, LIBELLES } from './carte.js'
import { chargerImage } from './rendu.js'
import { chargerPolices } from './polices.js'
import { ICONES } from './polices.js'
import { TEXTES, chargerTraits, traduireTraits } from './langues.js'
import { $, dialogue, el, S, nouvelId, blobVersDataUrl, dataUrlVersBlob, pipette } from './commun.js'
import { ajouterFichiers, brancherSurcouche, calqueChoisi, choisirCalque, commencerGlisser, dessinerSurcouche, molette, sectionLibres, touche } from './panneau-libres.js'
import { clicSurCarte } from './clic-carte.js'
import { ouvrirRecadrage } from './recadrage.js'
import { ouvrirExportPack } from './export-pack.js'
import { brancherStyles, chargerStyles, enveloppePerso } from './styles-texte.js'
import { changerLangueUI, demarrerI18n, langueMemorisee, langueUI, t as tr } from './i18n.js'
import { ajouterVersion, ecrireProjet, lireProjet } from './stockage.js'
import { creerSynchro } from './serveur.js'
import { ouvrirComparable } from './comparable.js'
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
const ICONES_BARRE = [['energy', 'Énergie'], ['mental', 'Mental'], ['physical', 'Physique'], ['wild', 'Joker'], ['star', 'Étoile'], ['acceleration', 'Accélération'], ['crisis', 'Crise'], ['hazard', 'Aléas'], ['boost', 'Boost'], ['per_hero', 'Par joueur'], ['consequential', 'Dégâts consécutifs'], ['unique', 'Unique']]
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
// La sauvegarde sur le serveur du site (comptes createur) : voir serveur.js. Hors du site, elle reste en « local » et ne fait rien.
const synchro = creerSynchro({
  projet: () => projet,
  serialiser: (c) => serialiser(c),
  deserialiser: (j) => deserialiser(j),
  message: (t) => message(t),
  sauver: () => sauvegarderPlusTard(),
  apres: () => apresRapatriement(),
})
function sauvegarderPlusTard() {
  clearTimeout(minuteurSauvegarde)
  minuteurSauvegarde = setTimeout(async () => {
    try {
      synchro.avantSauvegarde()
      await ecrireProjet(projet)
      versionsModifie = true
      synchro.planifier()
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
addEventListener('pagehide', () => { clearTimeout(minuteurSauvegarde); synchro.avantSauvegarde(); ecrireProjet(projet).catch(() => {}); garderVersion('fermeture') })

/** Apres que des dossiers (ou les reglages) viennent du serveur : la page repart de ce que contient le projet. */
function apresRapatriement() {
  projet.cartes = projet.cartes.filter((c) => TYPES[c.type])
  if (!projet.cartes.length) projet.cartes = [nouvelleCarte('ally', 'en')]
  historiques.clear()
  majModeles()
  choisir(projet.cartes.some((c) => c.id === projet.courante) ? projet.courante : projet.cartes[0].id)
}

/** L'indicateur de l'en-tete : ou est enregistre le travail. Cache hors du site (mode local). */
function majIndicateurServeur() {
  const z = $('#etat-serveur')
  if (!z) return
  z.hidden = synchro.etat === 'local'
  z.className = 'etat-serveur'
  z.title = ''
  if (synchro.etat === 'deconnecte') {
    z.classList.add('doux')
    z.replaceChildren('☁ Non connecté : enregistré dans ce navigateur seulement. ', el('a', { href: '/connexion' }, 'Se connecter'))
    return
  }
  if (synchro.etat !== 'connecte') return
  const q = synchro.quota
  if (q) z.title = `Espace utilisé : ${Math.round(q.utilise / 1048576)} Mo sur ${Math.round(q.quota / 1048576)} Mo`
  const textes = { repos: '☁ Enregistré sur le serveur', attente: '☁ Enregistrement dans 5 secondes…', envoi: '☁ Enregistrement…' }
  if (synchro.activite === 'erreur') {
    z.classList.add('mauvais')
    z.textContent = synchro.detail === 'trop' ? '☁ Un dossier ne tient pas sur le serveur : il reste dans ce navigateur' : '☁ Serveur injoignable : nouvel essai bientôt'
  } else {
    z.classList.add(synchro.activite === 'repos' ? 'bon' : 'doux')
    z.textContent = textes[synchro.activite]
  }
}
synchro.onEtat = majIndicateurServeur

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

// Une carte neuve est VIDE (30/10/2026, « je veux un template vide ») : ni titre, ni stats d'exemple, cadre gris neutre.
// Avant : « Card name », des stats d'exemple et les couleurs par defaut du gabarit (rouge / bleu / jaune), qu'on prenait
// pour la carte de Miss Marvel. Seuls restent la lettre de face d'une manigance principale et la mention du createur.
function valeursParDefaut(type, langue) {
  return {
    ...CHAMPS_VIDES,
    langue,
    createur: TEXTES[langue].createur,
    phaseLettre: type === 'main_scheme_b' ? 'B' : type === 'main_scheme_a' ? 'A' : '',
  }
}

/** Le cadre neutre d'une carte vide : des gris, plus clairs pour les accents, cases claires noires (comme l'aspect Basique). */
function couleursNeutres(spec) {
  const accents = new Set(['left_accent', 'right_accent', 'divider', 'accent', 'splash_color'])
  const sombres = { light_boxes: '#000000', background_lower: '#4a4d55', shading: '#2b2d33', outer: '#25272c', cracks: '#3a3c42' }
  return Object.fromEntries(rolesDe(spec).map((r) => [r, sombres[r] ?? (accents.has(r) ? '#a3a5ab' : '#6e7179')]))
}

function nouvelleCarte(type = 'ally', langue = 'fr') {
  return {
    id: nouvelId(), type, langue, contenu: valeursParDefaut(type, langue), couleurs: couleursNeutres(TYPES[type]), fissures: true, libres: [], cadre: 'officiel', dossier: '', verso: { mode: 'aucun', carteId: null, blob: null },
    art: { blob: null, zoom: 1, x: 0, y: 0, rotation: 0 }, artDevant: { blob: null, zoom: 1, x: 0, y: 0, rotation: 0 },
    tete: { blob: null, afficher: true, etoile: false, zoom: 0.8, x: -19, y: 232, rotation: 0 },
  }
}
const carte = () => projet.cartes.find((c) => c.id === projet.courante)

/** Une copie profonde d'une carte (les images, des Blob, sont partagees : elles ne changent jamais). */
const cloner = (c) => structuredClone(c)

/** Une carte -> du JSON (images en data URL). Sert aux fichiers, aux versions envoyees au serveur, aux modeles exportes. */
async function serialiser(c) {
  const copie = structuredClone({ ...c, art: { ...c.art, blob: null }, artDevant: { ...c.artDevant, blob: null }, tete: { ...c.tete, blob: null }, verso: { ...(c.verso ?? {}), blob: null }, libres: [] })
  copie.verso.image = c.verso?.blob ? await blobVersDataUrl(c.verso.blob) : null
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
  c.verso = { mode: 'aucun', carteId: null, ...(j.verso ?? {}), blob: j.verso?.image ? await dataUrlVersBlob(j.verso.image) : null }
  delete c.verso.image
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
/** Le dos de la carte (canvas a la taille du recto) selon son mode : dos du jeu, autre carte, ou image ; null s'il n'y en a pas. */
async function rendreVerso(c, langue = null) {
  const v = c.verso ?? { mode: 'aucun' }
  if (v.mode === 'aucun') return null
  if (v.mode === 'carte') {
    const o = projet.cartes.find((x) => x.id === v.carteId)
    return o ? rendreCarte(o, langue) : null
  }
  const spec = TYPES[c.type]
  let im = null
  if (v.mode === 'image') im = await imageDe(v.blob)
  else im = await chargerImage(`${IMAGES}general/dos-${v.mode === 'joueur' ? 'joueur' : 'rencontre'}.webp`)
  if (!im) return null
  const t = document.createElement('canvas')
  t.width = spec.largeur
  t.height = spec.hauteur
  const x = t.getContext('2d')
  const k = Math.max(t.width / im.naturalWidth, t.height / im.naturalHeight)
  x.imageSmoothingQuality = 'high'
  x.drawImage(im, (t.width - im.naturalWidth * k) / 2, (t.height - im.naturalHeight * k) / 2, im.naturalWidth * k, im.naturalHeight * k)
  return t
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
  if (['menaceDepart', 'menaceCible', 'acceleration'].includes(cle)) ligne.append(coche('Par joueur', (x) => x.contenu, cle + 'ParJoueur'))
  return ligne
}
// Les nombres d'une carte, dans l'ordre du formulaire : [classe de l'element du gabarit, libelle, cle, etoile possible, explication].
// L'explication sert a l'assistant « Nouvelle carte ».
const NOMBRES = [
  ['paycost cost', 'Coût', 'cout', true, 'Ce que le joueur paie (en ressources) pour jouer la carte.'],
  ['thw sch cost', 'Contrer / manigance (THW / SCH)', 'thw', true, 'Héros et alliés : menace retirée en contrant. Méchants et sbires : menace ajoutée en manigançant.'],
  ['thwconsequential', 'Dégâts consécutifs (contrer)', 'thwConseq', false, 'Les dégâts que l’allié subit chaque fois qu’il contre (0 si aucun).', true],
  ['atk cost', 'Attaque (ATK)', 'atk', true, 'Les dégâts infligés en attaquant.'],
  ['atkconsequential', 'Dégâts consécutifs (attaque)', 'atkConseq', false, 'Les dégâts que l’allié subit chaque fois qu’il attaque (0 si aucun).', true],
  ['def cost', 'Défense (DEF)', 'def', true, 'Les dégâts évités en défendant.'],
  ['rec cost', 'Récupération (REC)', 'rec', true, 'Les points de vie rendus quand l’alter-ego récupère.'],
  ['hp cost', 'Points de vie', 'pv', true, 'Les dégâts que la carte encaisse avant d’être vaincue.'],
  ['handsize', 'Taille de main', 'tailleMain', false, 'Le nombre de cartes piochées en fin de tour.'],
  ['startingthreatwrap', 'Menace de départ', 'menaceDepart', true, 'La menace posée sur la manigance quand elle entre en jeu.'],
  ['targetthreat cost', 'Menace cible', 'menaceCible', false, 'La menace qui fait gagner le méchant (ou avancer la manigance).'],
  ['acceleration', 'Accélération', 'acceleration', false, 'La menace ajoutée à chaque phase du méchant.'],
  ['attachmentatknums cost', 'Attachement : bonus d’attaque', 'atkAttache', true, 'Le bonus (ou malus) d’attaque donné à la carte qui le porte.'],
  ['attachmentschnums cost', 'Attachement : bonus de manigance', 'schAttache', true, 'Le bonus (ou malus) de manigance donné à la carte qui le porte.'],
]
function nombresDuType(spec) {
  return NOMBRES.filter(([cls]) => aElement(spec, cls)).map(([cls, label, cle, etoile, aide, conseq]) => ({ cls, label, cle, etoile, aide, conseq: !!conseq }))
}
function section(titre, ouvert, ...contenu) {
  return el('details', { open: ouvert }, el('summary', {}, titre), el('div', { class: 'contenu' }, contenu))
}
// Les sections du formulaire sont TOUTES repliees a l'ouverture d'une carte (30/10/2026, « je veux que tout soit replié ») ;
// celles qu'on ouvre le restent tant qu'on reste sur la carte (le formulaire se reconstruit a chaque reglage).
const sectionsOuvertes = new Set()
let carteDesSections = null
function replierSections(blocs, idCarte) {
  if (carteDesSections !== idCarte) { sectionsOuvertes.clear(); carteDesSections = idCarte }
  for (const d of blocs) {
    if (d.tagName !== 'DETAILS') continue
    const cle = d.querySelector(':scope > summary')?.textContent ?? ''
    d.open = sectionsOuvertes.has(cle)
    d.addEventListener('toggle', () => { d.open ? sectionsOuvertes.add(cle) : sectionsOuvertes.delete(cle) })
  }
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
    selTaille, couleur, pipette(couleur),
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

// Preset vide = cadre neutre (gris) ; OFFICIEL = les couleurs d'origine du gabarit du jeu. Une palette qui ne colore
// aucun role du type (palette de heros sur une carte de rencontre) laisse aussi le cadre neutre.
const OFFICIEL = '__officiel'
function appliquerPalette(c, spec, cle) {
  const roles = new Set(rolesDe(spec))
  c.couleurs = {}
  if (cle === OFFICIEL) return
  const choix = cle ? ASPECTS[cle] : null
  const pal = cle ? (typeof choix === 'string' ? PALETTES[choix] : choix ?? PALETTES[cle]) : null
  for (const [k, v] of Object.entries(pal ?? {})) {
    const role = k === 'splash' ? 'splash_color' : k
    if (roles.has(role)) c.couleurs[role] = v
  }
  if (!Object.keys(c.couleurs).length) c.couleurs = couleursNeutres(spec)
}
/** Le menu des couleurs d'un type : neutre, couleurs d'origine, aspects (cartes joueur), palettes des heros ou des mechants. */
function optionsPalette(spec) {
  const noms = Object.keys(PALETTES)
  const famille = spec.famille === 'villain' ? noms.filter((n) => PALETTES[n].background_upper) : noms.filter((n) => PALETTES[n].left_color)
  const s = el('select', {}, el('option', { value: '' }, 'Neutre (gris)'), el('option', { value: OFFICIEL }, 'Couleurs d’origine du cadre du jeu'))
  if (spec.famille !== 'villain') s.append(el('optgroup', { label: 'Aspects' }, Object.keys(ASPECTS).map((n) => el('option', { value: n }, n))))
  s.append(el('optgroup', { label: spec.famille === 'villain' ? 'Méchants et rencontres' : 'Héros' }, famille.sort().map((n) => el('option', { value: n }, joliNom(n)))))
  return s
}
/** La couleur qui represente un preset (pastille d'un dossier) ; null si neutre. */
function couleurDuPreset(cle) {
  if (!cle || cle === OFFICIEL) return null
  const choix = ASPECTS[cle]
  const pal = typeof choix === 'string' ? PALETTES[choix] : choix ?? PALETTES[cle]
  return pal?.left_color ?? pal?.background_upper ?? pal?.middle ?? null
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
    dossier.addEventListener('change', () => {
      // une carte « vierge » (pas encore de couleurs a elle) qui rejoint un dossier deja gabarite en herite tout de suite.
      if (!c.preset && !Object.keys(c.couleurs ?? {}).length) {
        const avant = JSON.stringify(c.contenu)
        appliquerGabaritPack(c)
        if (JSON.stringify(c.contenu) !== avant || c.preset) { changement(); construireFormulaire() }
      }
      proposerGabaritPack(c)
    })
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
    texte.push(coche('Centrer le texte verticalement (comme les cartes officielles à texte court)', (x) => x.contenu, 'centrerTexte'))
  }
  if (aElement(spec, 'villainstagenew')) texte.push(t('Étape du méchant (I, II, A, B…)', 'etape'))
  if (aElement(spec, 'set-line')) texte.push(t('Ligne d’ensemble', 'ligneEnsemble'))
  // les PV d'un méchant sont dans la ligne d'ensemble (« … / HIT POINTS 14 » + icône « par joueur ») : une case pose ou retire l'icône
  if (aElement(spec, 'set-line') && c.type === 'villain') {
    const ICONE = /\s*\[per_hero\]\s*$/
    const i = el('input', { type: 'checkbox' })
    i.checked = ICONE.test(c.contenu.ligneEnsemble ?? '')
    i.addEventListener('change', () => {
      c.contenu.ligneEnsemble = (c.contenu.ligneEnsemble ?? '').replace(ICONE, '') + (i.checked ? '[per_hero]' : '')
      changement()
      construireFormulaire()
    })
    texte.push(el('label', { class: 'ligne' }, i, 'Points de vie par joueur (icône en fin de ligne)'))
  }
  if (aElement(spec, 'c-line')) texte.push(t('Créateur / mention', 'createur'))
  f.push(section('Texte', true, ...texte))

  // nombres
  const N = []
  for (const n of nombresDuType(spec)) {
    if (n.conseq) N.push(liste(n.label, (x) => x.contenu, n.cle, [0, 1, 2, 3, 4, 5].map((k) => [k, k]), Number))
    else N.push(nombre(n.label, n.cle, n.etoile))
  }
  if (aElement(spec, 'mainschemephase cost')) N.push(el('div', { class: 'rang' }, t('Phase : numéro', 'phaseNumero'), t('Phase : lettre', 'phaseLettre')))
  if (N.length) f.push(section('Nombres', true, ...N))

  // renforts et ressources
  if (spec.renforts || spec.ressources) {
    const R = []
    if (spec.renforts) R.push(el('div', { class: 'nombre' }, liste('Icônes de boost', (x) => x.contenu, 'renforts', [0, 1, 2, 3, 4, 5].map((n) => [n, n]), Number), coche('★', (x) => x.contenu, 'renfortEtoile')))
    if (spec.ressources) {
      for (let k = 0; k < 3; k++) {
        const ressources = () => (c.contenu.ressources = c.contenu.ressources?.length ? c.contenu.ressources : ['', '', ''])
        const s = el('select', {}, GENRES_RESSOURCE.map(([v, n]) => el('option', { value: v }, n)))
        s.value = ressources()[k] ?? ''
        s.addEventListener('change', () => { ressources()[k] = s.value; changement() })
        R.push(el('label', {}, `Ressource ${k + 1}`, s))
      }
    }
    f.push(section('Boost et ressources', true, ...R))
  }

  // couleurs
  const roles = rolesDe(spec)
  if (roles.length) {
    const preset = optionsPalette(spec)
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
      grille.append(el('label', {}, ROLES_COULEURS[r], el('span', { class: 'rang-couleur' }, i, pipette(i))))
    }
    f.push(section('Couleurs', false, el('label', {}, 'Préréglage', preset), grille,
      el('button', { class: 'btn petit', type: 'button', onclick: () => { c.preset = ''; appliquerPalette(c, spec, ''); construireFormulaire(); changement() } }, 'Remettre le cadre neutre (gris)')))
  }

  // illustration
  f.push(section('Illustration', false, ...boiteImage('Image derrière la carte', (x) => x.art, 'art'), el('hr'), ...boiteImage('Premier plan (devant le cadre)', (x) => x.artDevant, 'artDevant')))

  f.push(sectionLibres())

  // dos de la carte
  {
    const v = (c.verso ??= { mode: 'aucun', carteId: null, blob: null })
    const autres = projet.cartes.filter((x) => x.id !== c.id)
    const mode = liste('Dos', (x) => x.verso, 'mode', [['aucun', 'Aucun'], ['joueur', 'Dos des cartes joueur'], ['rencontre', 'Dos des cartes rencontre'], ['carte', 'Une autre carte (autre face)'], ['image', 'Mon image']], (m) => m)
    mode.querySelector('select').addEventListener('change', construireFormulaire)
    const parts = [mode]
    if (v.mode === 'carte') {
      const s = el('select', {}, el('option', { value: '' }, '—'), ...autres.map((x) => el('option', { value: x.id }, `${x.contenu.titre || '(sans titre)'} · ${NOMS[x.type] ?? x.type}`)))
      s.value = v.carteId ?? ''
      s.addEventListener('change', () => { v.carteId = s.value || null; changement() })
      parts.push(el('label', {}, 'Carte au dos', s))
    }
    if (v.mode === 'image') {
      const fichier = el('input', { type: 'file', accept: 'image/*' })
      fichier.addEventListener('change', () => { if (fichier.files[0]) { v.blob = fichier.files[0]; changement() } })
      parts.push(el('label', {}, 'Image du dos', fichier))
    }
    if (v.mode === 'joueur' || v.mode === 'rencontre') parts.push(el('div', { class: 'aide' }, 'Le dos du jeu est de petite taille (300 px) : correct pour l’écran, flou à l’impression. Pour imprimer, choisis « Mon image ».'))
    f.push(section('Dos de la carte', false, ...parts))
  }

  // La « Tête d'angle » (image de coin pour certaines cartes) a ete retiree du formulaire le
  // 29/10/2026 : le reglage (zoom/decalage/rotation/detourage) ne fonctionnait pas, sur demande
  // de l'utilisateur. `rendu.js:teteVisible` ne dessine plus rien non plus.

  // style de cadre et options
  f.push(section('Style du cadre', false,
    liste('Style', (x) => x, 'cadre', [['officiel', 'Officiel (gabarit du jeu)'], ['sombre', 'Cadre sombre'], ['illustration', 'Pleine illustration (sans cadre)']], (v) => v),
    el('div', { class: 'aide' }, '« Cadre sombre » remplace les couleurs par un gris-bleu foncé avec des accents dorés (tu peux encore les modifier dans Couleurs). « Pleine illustration » enlève le cadre : l’image remplit la carte et le texte repose sur des panneaux translucides.'),
    TYPES_SANS_FISSURES.has(c.type) ? coche('Fissures dans le cadre', (x) => x, 'fissures') : null))

  replierSections(f, c.id)
  racine.append(...f)
  majAide()
}
function majAide() {
  const cible = { art: 'l’illustration', artDevant: 'le premier plan', tete: 'la tête d’angle' }[ciblePointeur]
  $('#aide-toile').textContent = `Glisse sur l’aperçu pour déplacer ${cible} (molette : zoom).`
}

// ---------------------------------------------------------------- liste
let filtreListe = ''
// La colonne « Cartes » montre les dossiers en TUILES (30/10/2026, « que le créateur voie bien les différents dossiers
// pour chaque héros ») : la couleur du héros, son nom, le nombre de cartes ; un clic ouvre le dossier et ses cartes.
// `dossierVu` : null = les tuiles ; un nom = ce dossier ouvert ; SANS_DOSSIER = les cartes rangees nulle part.
// Une recherche montre toutes les cartes qui correspondent, tous dossiers confondus.
const SANS_DOSSIER = '\u0000sans-dossier'
let dossierVu = null
/** La couleur d'un dossier : celle de son template, sinon celle de sa premiere carte coloree, sinon un gris. */
function couleurDuDossier(nom) {
  const g = projet.gabarits?.[nom]
  const d = g && (g.couleurs?.left_color ?? g.couleurs?.background_upper ?? couleurDuPreset(g.preset))
  if (d) return d
  for (const c of projet.cartes) {
    if (c.dossier !== nom) continue
    const x = c.couleurs?.left_color ?? c.couleurs?.background_upper ?? couleurDuPreset(c.preset)
    if (x) return x
  }
  return '#6e7179'
}
function boutonCarte(c, avecDossier = false) {
  return el('button', { type: 'button', class: 'carte-liste', 'aria-current': String(c.id === projet.courante), onclick: () => choisir(c.id) },
    el('span', {}, c.contenu.titre || '(sans titre)'),
    el('small', {}, `${NOMS[c.type] ?? c.type} · ${c.langue.toUpperCase()}`), avecDossier && c.dossier ? el('small', {}, '📁 ' + c.dossier) : null)
}
function majListe() {
  const l = $('#liste')
  const q = filtreListe.trim().toLowerCase()
  const noeuds = []
  const dossiers = dossiersDuProjet()
  const sansDossier = projet.cartes.filter((c) => !c.dossier)
  if (q) {
    const visible = (c) => [c.contenu.titre, c.contenu.regles, c.contenu.traits, c.dossier, NOMS[c.type]].some((t) => String(t ?? '').toLowerCase().includes(q))
    for (const c of projet.cartes) if (visible(c)) noeuds.push(boutonCarte(c, true))
  } else if (!dossiers.length) {
    // pas encore de dossier : la liste simple
    dossierVu = null
    for (const c of projet.cartes) noeuds.push(boutonCarte(c))
  } else {
    if (dossierVu !== null && dossierVu !== SANS_DOSSIER && !dossiers.some(([d]) => d === dossierVu)) dossierVu = null
    if (dossierVu === SANS_DOSSIER && !sansDossier.length) dossierVu = null
    if (dossierVu === null) {
      const courant = carte()?.dossier ?? ''
      for (const [nom, nb] of dossiers) {
        noeuds.push(el('button', { type: 'button', class: 'dossier tuile-dossier' + (courant === nom ? ' choisie' : ''), style: `--teinte:${couleurDuDossier(nom)}`, onclick: () => { dossierVu = nom; majListe() } },
          el('span', { class: 'tuile-nom' }, '📁 ' + nom), el('small', {}, `${nb} carte(s)` + (projet.gabarits?.[nom] ? ' · template ✓' : ''))))
      }
      if (sansDossier.length) {
        noeuds.push(el('button', { type: 'button', class: 'dossier tuile-dossier tuile-sans' + (courant === '' ? ' choisie' : ''), style: '--teinte:#3a3d45', onclick: () => { dossierVu = SANS_DOSSIER; majListe() } },
          el('span', { class: 'tuile-nom' }, 'Sans dossier'), el('small', {}, `${sansDossier.length} carte(s)`)))
      }
    } else {
      const nom = dossierVu === SANS_DOSSIER ? '' : dossierVu
      const cartes = projet.cartes.filter((c) => (c.dossier || '') === nom)
      noeuds.push(el('div', { class: 'tete-dossier', style: `--teinte:${nom ? couleurDuDossier(nom) : '#3a3d45'}` },
        el('button', { type: 'button', class: 'dossier btn petit fixe', title: 'Revenir à tous les dossiers', onclick: () => { dossierVu = null; majListe() } }, '← Dossiers'),
        el('strong', {}, nom ? '📁 ' + nom : 'Sans dossier'), el('small', {}, `${cartes.length} carte(s)`)))
      if (nom) {
        noeuds.push(el('div', { class: 'outils' },
          el('button', { type: 'button', class: 'dossier btn petit', title: 'Une nouvelle carte dans ce dossier, avec l’assistant', onclick: () => ouvrirAssistantCarte(nom) }, '+ Carte ici'),
          el('button', { type: 'button', class: 'dossier btn petit', title: 'Les couleurs, le cadre et la mention communs à ce dossier', onclick: () => ouvrirAssistantTemplate(nom) }, projet.gabarits?.[nom] ? 'Modifier le template…' : 'Créer le template…')))
      }
      for (const c of cartes) noeuds.push(boutonCarte(c))
    }
  }
  if (!noeuds.length) noeuds.push(el('div', { class: 'aide' }, q ? 'Aucune carte ne correspond.' : 'Aucune carte.'))
  l.replaceChildren(...noeuds)
  l.dataset.total = String(projet.cartes.length) // toutes les cartes, quel que soit le dossier ouvert (tests)
  // dossiers deja utilises : propositions du champ « Dossier »
  const dl = $('#dossiers-connus')
  if (dl) dl.replaceChildren(...dossiers.map(([d]) => el('option', { value: d })))
  majModeles()
}
/** La liste « Templates » : le template de chaque dossier, puis les cartes de depart gardees. */
function majModeles() {
  const s = $('#modeles')
  if (!s) return
  const v = s.value
  const gabarits = Object.keys(projet.gabarits ?? {}).sort()
  const modeles = projet.modeles ?? []
  s.replaceChildren(...[el('option', { value: '' }, `— templates (${gabarits.length + modeles.length}) —`),
    gabarits.length ? el('optgroup', { label: 'Dossiers (apparence)' }, gabarits.map((d) => el('option', { value: 'g:' + d }, '📁 ' + d))) : null,
    modeles.length ? el('optgroup', { label: 'Cartes de départ' }, modeles.map((m) => el('option', { value: 'm:' + m.id }, '🃏 ' + m.nom))) : null].filter(Boolean))
  s.value = v
  if (s.value !== v) s.value = ''
}
function choisir(id) {
  validerHistorique()
  projet.courante = id
  { const d = carte()?.dossier || SANS_DOSSIER; if (dossierVu !== null && dossierVu !== d) dossierVu = d }
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
  if (dossierVu !== null || c.dossier) dossierVu = c.dossier || SANS_DOSSIER
  choisir(c.id)
}

// ---------------------------------------------------------------- assistants (gabarit de pack, nouvelle carte guidee)
// Deux assistants tres descriptifs (demande du 29/10/2026) : regler le gabarit d'un pack (couleurs, cadre,
// mise en page, mention du createur - les reglages qui doivent rester identiques sur toutes les cartes d'un
// meme dossier), et creer une nouvelle carte pas a pas. Chaque etape explique ce qu'elle regle avant de le
// demander ; on peut relancer l'un ou l'autre autant de fois qu'on veut (boutons « Gabarit du pack… » et
// « + Assistant… »), et le gabarit est reutilisable : « Gabarit du pack… » le rouvre pour le modifier.
const DESCRIPTIONS_TYPES = {
  ally: 'Combat ou contre le plan à tes côtés.', event: 'Un effet ponctuel, défaussé après usage.',
  upgrade: 'Reste attachée à ton héros, effet continu ou déclenché.', support: 'Reste en jeu devant toi, effet continu ou déclenché.',
  resource: 'Attachée pour produire une ressource (ou un effet ponctuel) chaque tour.',
  'alter-ego': 'Le côté civil du héros : récupération, actions d’alter-ego.',
  identity: 'La carte d’identité du héros : stats Contrer / Attaquer / Défendre, capacité de héros.',
  obligation: 'Une obligation mêlée au paquet de rencontre du joueur.',
  playersidescheme: 'Une manigance annexe qui appartient à un joueur, pas au paquet de rencontre.',
  villain: 'La carte de stats du méchant (une face).', minion: 'Un sbire de rencontre, qui attaque ou défend.',
  treachery: 'Un effet de rencontre ponctuel, défaussé après usage.', environment: 'Une carte de rencontre permanente (un lieu, par exemple).',
  attachment: 'S’attache à un héros ou un sbire, côté rencontre.', sidescheme: 'Une manigance supplémentaire à résoudre en plus de la principale.',
  main_scheme_a: 'La manigance principale, première face (menace de départ).', main_scheme_b: 'La manigance principale, deuxième face (après son avancée).',
  'obligation-villain': 'Une obligation pour le paquet du méchant.', 'generic-promo': 'Un gabarit promo générique, horizontal.',
  'generic-promo-vert': 'Un gabarit promo générique, vertical.', 'alter-ego-promo': 'Une carte alter-ego en promo.',
  'identity-promo': 'Une carte d’identité de héros en promo.', 'starter-deck': 'La liste d’un paquet de départ (texte seul, pas de stats).',
}

/** Fait tourner une suite d'etapes dans une boite de dialogue : chacune explique ce qu'elle regle avant de le demander.
 * `etapes` : un tableau, ou une fonction (valeurs) -> tableau (les etapes dependent alors des choix, le type de carte par exemple).
 * etapes[i] = { titre, aide?, construire(valeurs, rafraichir) -> noeud, valider?(valeurs) -> string|undefined (message d'erreur) }.
 * `fin(valeurs)` est appele apres la derniere etape validee.
 * opts.apercu(valeurs) -> carte|null : la carte telle qu'elle sortira, dessinee a droite et redessinee a chaque saisie.
 * opts.pied(fermer) -> noeud : un lien de plus sous les boutons (« carte vide, sans assistant »...). */
function lancerAssistant(titreAssistant, etapes, fin, opts = {}) {
  const d = el('dialog', { class: 'dlg' })
  const corps = el('div', { class: 'assistant-corps' })
  const puces = el('ol', { class: 'assistant-puces' })
  const alerte = el('div', { class: 'aide', style: 'color:#ff9b8f' })
  const gauche = el('div', { class: 'rang' })
  const droite = el('div', { class: 'rang' })
  const toile = el('canvas', { class: 'assistant-apercu' })
  let i = 0
  const valeurs = { ...(opts.valeurs ?? {}) }
  const liste = () => (typeof etapes === 'function' ? etapes(valeurs) : etapes)
  let minuteur = 0
  let n = 0
  async function redessiner() {
    if (!opts.apercu) return
    const k = ++n
    const c = opts.apercu(valeurs)
    if (!c) return
    try {
      const t = await rendreCarte(c)
      if (k !== n) return
      toile.width = t.width
      toile.height = t.height
      toile.getContext('2d').drawImage(t, 0, 0)
    } catch {}
  }
  const plusTard = () => { clearTimeout(minuteur); minuteur = setTimeout(redessiner, 150) }
  d.addEventListener('input', plusTard)
  d.addEventListener('change', plusTard)
  function rendre() {
    const toutes = liste()
    i = Math.min(i, toutes.length - 1)
    const etape = toutes[i]
    alerte.textContent = ''
    corps.replaceChildren(...[
      el('h3', { class: 'assistant-titre' }, `${i + 1}/${toutes.length} · ${etape.titre}`),
      etape.aide ? el('p', { class: 'assistant-aide' }, etape.aide) : null,
      etape.construire(valeurs, rendre)].filter(Boolean))
    puces.replaceChildren(...toutes.map((e, k) => el('li', { class: k === i ? 'en-cours' : k < i ? 'fait' : '' },
      k < i ? el('button', { type: 'button', onclick: () => { i = k; rendre() } }, e.court ?? e.titre) : el('span', {}, e.court ?? e.titre))))
    gauche.replaceChildren(...[
      i > 0 ? el('button', { class: 'btn', type: 'button', onclick: () => { i--; rendre() } }, '◀ Précédent') : null,
      el('button', { class: 'btn', type: 'button', onclick: () => d.close() }, 'Annuler')].filter(Boolean))
    const dernier = i === toutes.length - 1
    droite.replaceChildren(el('button', {
      class: 'btn principal', type: 'button',
      onclick: () => {
        const erreur = etape.valider?.(valeurs)
        if (typeof erreur === 'string') { alerte.textContent = erreur; return }
        if (dernier) { fin(valeurs); d.close() }
        else { i++; rendre() }
      },
    }, dernier ? 'Terminer' : 'Suivant ▶'))
    plusTard()
  }
  const colonne = el('div', { class: 'assistant-colonne' }, corps, alerte,
    el('div', { class: 'rang assistant-boutons' }, gauche, droite),
    opts.pied ? el('div', { class: 'assistant-pied' }, opts.pied(() => d.close())) : null)
  d.append(el('div', { class: 'panneau assistant' },
    el('h2', {}, titreAssistant), puces,
    el('div', { class: 'assistant-grille' + (opts.apercu ? '' : ' sans-apercu') }, colonne, opts.apercu ? el('figure', { class: 'assistant-figure' }, toile, el('figcaption', { class: 'aide' }, 'Aperçu')) : null)))
  document.body.append(d)
  d.addEventListener('close', () => { clearTimeout(minuteur); d.remove() })
  rendre()
  d.showModal()
  return d
}

/** Un champ de l'assistant : libelle, explication en dessous, valeur gardee dans `v[cle]`. */
function champAssistant(v, cle, label, aide, opts = {}) {
  v[cle] ??= opts.defaut ?? ''
  const i = opts.long ? el('textarea', { rows: opts.lignes ?? 4, placeholder: opts.exemple ?? '' }) : el('input', { type: 'text', placeholder: opts.exemple ?? '', list: opts.list ?? null })
  i.value = v[cle]
  i.addEventListener('input', () => { v[cle] = i.value })
  return el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, label), i, aide ? el('small', { class: 'aide' }, aide) : null)
}
function caseAssistant(v, cle, label, aide, defaut = false) {
  v[cle] ??= defaut
  const i = el('input', { type: 'checkbox' })
  i.checked = !!v[cle]
  i.addEventListener('change', () => { v[cle] = i.checked })
  return el('div', { class: 'assistant-champ' }, el('label', { class: 'ligne' }, i, el('span', { class: 'assistant-libelle' }, label)), aide ? el('small', { class: 'aide' }, aide) : null)
}

/** Les dossiers du projet, avec le nombre de cartes de chacun (« » = sans dossier exclu). */
function dossiersDuProjet() {
  const m = new Map()
  for (const c of projet.cartes) if (c.dossier) m.set(c.dossier, (m.get(c.dossier) ?? 0) + 1)
  for (const d of Object.keys(projet.gabarits ?? {})) if (!m.has(d)) m.set(d, 0)
  return [...m.entries()].sort((a, b) => a[0].localeCompare(b[0]))
}

/** Applique a `c` le template enregistre pour son dossier, s'il y en a un (couleurs, cadre, mise en page, mention). */
function appliquerGabaritPack(c) {
  const g = (projet.gabarits ??= {})[(c.dossier || '').trim()]
  if (!g) return
  const spec = TYPES[c.type]
  c.preset = g.preset ?? ''
  if (spec) appliquerPalette(c, spec, c.preset)
  // couleurs reglees a la main (« comme la carte actuelle ») : par-dessus, role par role
  if (spec && g.couleurs) { const roles = new Set(rolesDe(spec)); for (const [r, v] of Object.entries(g.couleurs)) if (roles.has(r)) c.couleurs[r] = v }
  if (g.cadre) c.cadre = g.cadre
  if (g.fissures != null) c.fissures = g.fissures
  if (g.createur) c.contenu.createur = g.createur
  if (g.centrerTexte != null) c.contenu.centrerTexte = g.centrerTexte
  if (g.echelleTexte != null) c.contenu.echelleTexte = g.echelleTexte
}

/** Propose de creer le template quand `c.dossier` est un dossier tout neuf (aucune autre carte dedans, pas de template). */
function proposerGabaritPack(c) {
  const dossier = (c.dossier || '').trim()
  if (!dossier) return
  if ((projet.gabarits ??= {})[dossier]) return
  if (projet.cartes.some((x) => x.id !== c.id && (x.dossier || '').trim() === dossier)) return
  dialogue(`Nouveau dossier « ${dossier} »`,
    el('div', { class: 'aide' },
      'Veux-tu lui créer un template maintenant (couleurs, style du cadre, mention du créateur) ? Il s’appliquera à cette carte, et à toutes celles que tu ajouteras ensuite dans ce dossier. Tu pourras le modifier à tout moment depuis le dossier ou la rubrique « Templates ».'),
    [{ texte: 'Plus tard' }, { texte: 'Créer le template', principal: true, action: () => { ouvrirAssistantTemplate(dossier); return true } }])
}

/** Le choix du dossier dans un assistant : les dossiers existants en tuiles, ou un nom nouveau. */
function choixDossier(v, rafraichir, { avecAucun = true } = {}) {
  const tuiles = el('div', { class: 'assistant-tuiles' })
  const existants = dossiersDuProjet()
  for (const [nom, nb] of existants) {
    const coul = couleurDuDossier(nom)
    tuiles.append(el('button', {
      type: 'button', class: 'tuile-dossier' + (v.dossier === nom ? ' choisie' : ''), style: `--teinte:${coul}`,
      onclick: () => { v.dossier = nom; rafraichir() },
    }, el('span', { class: 'tuile-nom' }, '📁 ' + nom), el('small', {}, `${nb} carte(s)` + (projet.gabarits?.[nom] ? ' · template ✓' : ''))))
  }
  if (avecAucun) {
    tuiles.append(el('button', {
      type: 'button', class: 'tuile-dossier' + (v.dossier === '' ? ' choisie' : ''), style: '--teinte:#3a3d45',
      onclick: () => { v.dossier = ''; rafraichir() },
    }, el('span', { class: 'tuile-nom' }, 'Sans dossier'), el('small', {}, 'La carte reste à part')))
  }
  const nouveau = el('input', { type: 'text', placeholder: 'ex. Valkyrie', value: existants.some(([n]) => n === v.dossier) ? '' : v.dossier })
  nouveau.addEventListener('input', () => { v.dossier = nouveau.value.trim(); for (const b of tuiles.children) b.classList.remove('choisie') })
  return el('div', { class: 'assistant-champ' },
    existants.length ? el('span', { class: 'assistant-libelle' }, 'Un dossier existant') : null, tuiles,
    el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Ou un nouveau dossier'), nouveau))
}

/** Le texte saisi dans une zone simple -> le mini-HTML de la carte (les retours a la ligne restent, les icones [energy] aussi). */
const versCarte = (txt) => echapper(String(txt ?? '').trim())

// ---------------------------------------------------------------- assistant « Nouvelle carte » (par blocs)
// 30/10/2026 : l'assistant passe sur TOUT, bloc par bloc (type, dossier, nom et traits, nombres, texte, illustration,
// couleurs), chaque bloc explique ses champs, et l'apercu a droite montre la carte a chaque saisie. « + Nouvelle »
// l'ouvre directement ; un lien en bas cree une carte vide sans assistant, pour les habitues.

/** La carte que donnera l'assistant (sert a l'apercu et a la fin). */
function carteDepuisAssistant(v) {
  const c = nouvelleCarte(v.type, v.langue)
  const spec = TYPES[c.type]
  c.dossier = (v.dossier ?? '').trim()
  appliquerGabaritPack(c)
  if (v.couleursPropres || !projet.gabarits?.[c.dossier]) {
    c.preset = v.preset ?? ''
    appliquerPalette(c, spec, c.preset)
  }
  const ct = c.contenu
  ct.titre = (v.titre ?? '').trim()
  ct.unique = !!v.unique
  ct.traits = (v.traits ?? '').trim()
  for (const n of nombresDuType(spec)) if (v['n:' + n.cle] !== undefined) ct[n.cle] = n.conseq ? Number(v['n:' + n.cle]) || 0 : String(v['n:' + n.cle]).trim()
  if (aElement(spec, 'mainschemephase cost')) ct.phaseNumero = (v.phaseNumero ?? '').trim()
  if (aElement(spec, 'villainstagenew')) ct.etape = (v.etape ?? '').trim()
  ct.ligneEnsemble = (v.ligneEnsemble ?? '').trim()
  ct.regles = versCarte(v.regles)
  ct.citation = versCarte(v.citation)
  if (v.art) c.art.blob = v.art
  return c
}

function ouvrirAssistantCarte(dossierDepart) {
  const depart = {
    type: carte()?.type ?? 'ally',
    langue: carte()?.langue ?? 'en',
    dossier: dossierDepart ?? (dossierVu && dossierVu !== SANS_DOSSIER ? dossierVu : ''),
  }
  const etapes = (v) => {
    const spec = TYPES[v.type]
    const e = []
    e.push({
      titre: 'Quel type de carte ?', court: 'Type',
      aide: 'Le type fixe le cadre et les cases de la carte (coût, stats, menace…). Les étapes suivantes ne te demanderont que ce qui existe sur ce type. Tu pourras encore le changer plus tard.',
      construire: (v, rafraichir) => {
        const zone = el('div', { style: 'display:flex;flex-direction:column;gap:10px' })
        for (const [titreGroupe, ids] of GROUPES) {
          const boutons = el('div', { class: 'assistant-types' },
            ...ids.filter((id) => TYPES[id]).map((id) => el('button', {
              class: 'btn petit' + (v.type === id ? ' principal' : ''), type: 'button',
              onclick: () => { v.type = id; rafraichir() },
            }, el('div', { style: 'font-weight:600' }, NOMS[id] ?? id), el('div', { class: 'aide' }, DESCRIPTIONS_TYPES[id] ?? ''))))
          zone.append(el('h4', { class: 'assistant-groupe' }, titreGroupe), boutons)
        }
        return zone
      },
    })
    e.push({
      titre: 'Dans quel dossier ?', court: 'Dossier',
      aide: 'Un dossier regroupe les cartes d’un même héros (ou d’un même set de rencontre). Si le dossier a un template, la carte en prend tout de suite les couleurs, le style du cadre et la mention du créateur. Pour un héros tout neuf (identité, alter-ego, némésis…), le bouton « + Nouveau héros » crée tout le dossier d’un coup.',
      construire: (v, rafraichir) => choixDossier(v, rafraichir),
    })
    const nomTraits = [
      (v) => champAssistant(v, 'titre', 'Nom de la carte', 'Écrit en haut de la carte, tel quel.', { exemple: 'ex. Bifrost' }),
      (v) => caseAssistant(v, 'unique', 'Carte unique (✦)', 'Un seul exemplaire en jeu à la fois : le symbole ✦ s’ajoute devant le nom (personnages, lieux célèbres…).'),
    ]
    if (aElement(spec, 'traits')) nomTraits.push((v) => champAssistant(v, 'traits', 'Traits', 'Les mots-clés en italique sous l’illustration, séparés par des points. D’autres cartes s’y réfèrent (« chaque allié Avenger… »).', { exemple: 'ex. Asgard. Avenger.' }))
    e.push({
      titre: 'Nom et traits', court: 'Nom',
      aide: 'Ce qui identifie la carte.',
      construire: (v) => el('div', { class: 'assistant-pile' }, ...nomTraits.map((f) => f(v))),
      valider: (v) => (String(v.titre ?? '').trim() ? undefined : 'Donne un nom à la carte.'),
    })
    const nombres = nombresDuType(spec)
    const avecPhase = aElement(spec, 'mainschemephase cost')
    const avecEtape = aElement(spec, 'villainstagenew')
    if (nombres.length || avecPhase || avecEtape || aElement(spec, 'set-line')) {
      e.push({
        titre: 'Les nombres', court: 'Nombres',
        aide: 'Chaque case explique à quoi sert le nombre. Laisse vide ce que tu ne veux pas afficher ; « X » ou « — » sont acceptés. Les options plus rares (★, par joueur, icônes de boost, ressources) sont dans le formulaire, rubriques « Nombres » et « Boost et ressources ».',
        construire: (v) => {
          const pile = el('div', { class: 'assistant-pile' })
          for (const n of nombres) {
            if (n.conseq) {
              v['n:' + n.cle] ??= 0
              const s = el('select', {}, [0, 1, 2, 3, 4, 5].map((k) => el('option', { value: k }, k)))
              s.value = String(v['n:' + n.cle])
              s.addEventListener('change', () => { v['n:' + n.cle] = Number(s.value) })
              pile.append(el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, n.label), s, el('small', { class: 'aide' }, n.aide)))
            } else pile.append(champAssistant(v, 'n:' + n.cle, n.label, n.aide))
          }
          if (avecPhase) pile.append(champAssistant(v, 'phaseNumero', 'Numéro de la manigance', 'L’ordre de la manigance dans le scénario (1, 2, 3…).', { exemple: 'ex. 1' }))
          if (avecEtape) pile.append(champAssistant(v, 'etape', 'Étape du méchant', 'I, II, III (ou A, B…) : la carte méchant de chaque étape.', { exemple: 'ex. I' }))
          if (aElement(spec, 'set-line')) {
            const heros = ['identity', 'alter-ego'].includes(v.type)
            pile.append(champAssistant(v, 'ligneEnsemble', 'Ligne du bas',
              heros ? 'Sur une identité ou un alter-ego : la taille de main et les points de vie du héros.' : 'Le nom du set et le numéro de la carte dans le set.',
              { exemple: heros ? TEXTES[v.langue].ligneEnsemble(6, 10) : 'ex. Valkyrie (3/15)' }))
          }
          return pile
        },
      })
    }
    if (aElement(spec, 'rules') || aElement(spec, 'quote')) {
      e.push({
        titre: 'Le texte', court: 'Texte',
        aide: 'Le texte de règles dit ce que fait la carte ; la citation est une phrase d’ambiance en italique, sans effet. Écris simplement ici : le gras, l’italique, les icônes de ressource et les mots-clés officiels (Action, Renfort…) s’ajoutent ensuite dans le formulaire, rubrique « Texte », avec le bouton « Styles » ou en tapant « / ».',
        construire: (v) => el('div', { class: 'assistant-pile' },
          aElement(spec, 'rules') ? champAssistant(v, 'regles', 'Texte de règles', 'Une capacité par ligne.', { long: true, lignes: 5, exemple: 'ex. Action : inflige 2 dégâts à un ennemi.' }) : null,
          aElement(spec, 'quote') ? champAssistant(v, 'citation', 'Citation (facultative)', 'Une réplique du personnage, ou une phrase d’ambiance.', { long: true, lignes: 2 }) : null),
      })
    }
    e.push({
      titre: 'L’illustration', court: 'Image',
      aide: 'L’image placée derrière le cadre. Prends-la assez grande (au moins 750 × 1050 pixels) pour qu’elle reste nette à l’impression. Une fois la carte créée, tu la déplaces en la glissant sur l’aperçu et tu zoomes à la molette. Facultatif : tu peux l’ajouter plus tard.',
      construire: (v, rafraichir) => {
        const f = el('input', { type: 'file', accept: 'image/*' })
        f.addEventListener('change', () => { v.art = f.files[0] ?? null; rafraichir() })
        return el('div', { class: 'assistant-pile' }, el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Image'), f),
          v.art ? el('div', { class: 'rang' }, el('span', { class: 'aide' }, '✓ ' + (v.art.name ?? 'image choisie')), el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { v.art = null; rafraichir() } }, 'Retirer')) : null)
      },
    })
    e.push({
      titre: 'Les couleurs', court: 'Couleurs',
      aide: 'Les couleurs du cadre. Sans choix, le cadre reste neutre (gris).',
      construire: (v, rafraichir) => {
        const g = projet.gabarits?.[(v.dossier ?? '').trim()]
        const pile = el('div', { class: 'assistant-pile' })
        if (g) {
          pile.append(el('p', { class: 'aide' }, `Le dossier « ${v.dossier} » a un template : la carte en prend les couleurs (${g.preset === OFFICIEL ? tr('couleurs d’origine') : g.preset ? joliNom(g.preset) : tr('neutre')}). Coche la case pour en choisir d’autres pour cette carte seulement.`))
          const i = el('input', { type: 'checkbox' })
          i.checked = !!v.couleursPropres
          i.addEventListener('change', () => { v.couleursPropres = i.checked; rafraichir() })
          pile.append(el('label', { class: 'ligne' }, i, 'D’autres couleurs pour cette carte'))
          if (!v.couleursPropres) return pile
        }
        const s = optionsPalette(spec)
        s.value = v.preset ?? ''
        s.addEventListener('change', () => { v.preset = s.value })
        pile.append(el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Couleurs'), s,
          el('small', { class: 'aide' }, 'Un aspect (Justice, Protection…) colore tout le cadre d’une seule teinte ; la palette d’un héros ou d’un méchant du jeu reprend ses couleurs. Le détail, couleur par couleur, est dans le formulaire, rubrique « Couleurs ».')))
        return pile
      },
    })
    e.push({
      titre: 'C’est prêt', court: 'Fin',
      aide: 'La carte va s’ouvrir dans le formulaire, toutes rubriques repliées : ouvre seulement celle dont tu as besoin pour les finitions (mise en forme du texte, ★, calques PNG, dos de la carte, style du cadre).',
      construire: (v) => el('ul', { style: 'margin:0;padding-left:18px' },
        el('li', {}, `Type : ${tr(NOMS[v.type] ?? v.type)}`), el('li', {}, `Titre : ${String(v.titre ?? '').trim()}`), el('li', {}, `Dossier : ${String(v.dossier ?? '').trim() || tr('(aucun)')}`)),
    })
    return e
  }
  lancerAssistant('Nouvelle carte', etapes, (v) => {
    const c = carteDepuisAssistant(v)
    ajouter(c)
    if (c.dossier) dossierVu = c.dossier
    majListe()
    proposerGabaritPack(c)
  }, {
    valeurs: depart,
    apercu: (v) => carteDepuisAssistant(v),
    pied: (fermer) => el('button', {
      class: 'lien', type: 'button',
      onclick: () => { const c = nouvelleCarte(depart.type, depart.langue); c.dossier = depart.dossier; appliquerGabaritPack(c); ajouter(c); fermer() },
    }, 'Créer une carte vide, sans assistant'),
  })
}

// ---------------------------------------------------------------- assistant « Nouveau héros »
// 30/10/2026 : un heros = un dossier, son template, et ses cartes de base deja creees (identite, alter-ego, et sur
// demande sa nemesis, la manigance annexe de la nemesis et son obligation), pretes a remplir.
const CARTES_HEROS = [
  ['nemesis', 'minion', 'Sa némésis (un sbire)', 'L’ennemi juré du héros : elle entre en jeu avec la manigance annexe de la némésis.'],
  ['manigance', 'sidescheme', 'La manigance annexe de la némésis', 'Révélée quand la némésis arrive (« Le méchant fait sa manigance… »).'],
  ['obligation', 'obligation', 'Son obligation', 'Le problème personnel de l’alter-ego, mêlé au paquet de rencontre.'],
]
function ouvrirAssistantHeros() {
  const langue = carte()?.langue ?? 'en'
  const cartesHeros = (v) => {
    const cartes = []
    const id = nouvelleCarte('identity', langue)
    id.contenu.titre = (v.nom ?? '').trim()
    const ae = nouvelleCarte('alter-ego', langue)
    ae.contenu.titre = (v.alterEgo ?? '').trim()
    cartes.push(id, ae)
    for (const [cle, type] of CARTES_HEROS) if (v[cle]) cartes.push(nouvelleCarte(type, langue))
    for (const c of cartes) {
      c.dossier = (v.nom ?? '').trim()
      c.preset = v.preset ?? ''
      appliquerPalette(c, TYPES[c.type], c.preset)
      if (v.createur) c.contenu.createur = v.createur
    }
    // l'identite et l'alter-ego sont les deux faces d'une meme carte
    id.verso = { mode: 'carte', carteId: ae.id, blob: null }
    ae.verso = { mode: 'carte', carteId: id.id, blob: null }
    return cartes
  }
  const etapes = [
    {
      titre: 'Un héros, c’est un dossier', court: 'Nom',
      aide: 'Je vais créer un dossier au nom du héros, son template (les couleurs et la mention communes à toutes ses cartes), puis ses cartes de base, prêtes à remplir. Les autres cartes (son paquet de départ, ses alliés…) s’ajouteront ensuite dans le dossier avec « + Nouvelle ».',
      construire: (v) => el('div', { class: 'assistant-pile' },
        champAssistant(v, 'nom', 'Nom du héros', 'Le nom de super-héros : il sert aussi de nom au dossier et au titre de la carte d’identité.', { exemple: 'ex. Valkyrie' }),
        champAssistant(v, 'alterEgo', 'Nom de l’alter-ego', 'Son identité civile, écrite sur l’autre face.', { exemple: 'ex. Brunnhilde' })),
      valider: (v) => {
        const nom = String(v.nom ?? '').trim()
        if (!nom) return 'Donne un nom au héros.'
        if (dossiersDuProjet().some(([d]) => d === nom)) return 'Un dossier porte déjà ce nom : choisis-en un autre, ou ajoute tes cartes dans ce dossier avec « + Nouvelle ».'
      },
    },
    {
      titre: 'Ses couleurs', court: 'Couleurs',
      aide: 'Les couleurs du cadre, communes à toutes les cartes du héros. Pars d’une palette proche de ton héros (ou du gris neutre) ; tu affineras couleur par couleur dans le formulaire, rubrique « Couleurs ».',
      construire: (v) => {
        const s = optionsPalette(TYPES.identity)
        v.preset ??= ''
        s.value = v.preset
        s.addEventListener('change', () => { v.preset = s.value })
        return el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Couleurs'), s)
      },
    },
    {
      titre: 'La mention du créateur', court: 'Mention',
      aide: 'La petite ligne en bas de chaque carte : ton nom ou ton pseudo. Elle sera la même sur toutes les cartes du héros.',
      construire: (v) => champAssistant(v, 'createur', 'Mention', '', { defaut: TEXTES[langue].createur }),
    },
    {
      titre: 'Les cartes à créer', court: 'Cartes',
      aide: 'L’identité et l’alter-ego sont toujours créés : ce sont les deux faces de la carte du héros (je les relie l’une à l’autre comme recto et verso). Coche ce que tu veux en plus.',
      construire: (v) => el('div', { class: 'assistant-pile' },
        el('label', { class: 'ligne' }, el('input', { type: 'checkbox', checked: true, disabled: true }), el('span', { class: 'assistant-libelle' }, 'Identité de héros + alter-ego')),
        ...CARTES_HEROS.map(([cle, , label, aide]) => caseAssistant(v, cle, label, aide, true))),
    },
    {
      titre: 'C’est prêt', court: 'Fin',
      aide: 'Le dossier s’ouvre dans la colonne « Cartes », avec la carte d’identité choisie. Remplis chaque carte dans le formulaire.',
      construire: (v) => el('ul', { style: 'margin:0;padding-left:18px' },
        el('li', {}, `Dossier : ${String(v.nom).trim()}`),
        ...cartesHeros(v).map((c) => el('li', {}, `${tr(NOMS[c.type] ?? c.type)}${c.contenu.titre ? ' : ' + c.contenu.titre : ''}`))),
    },
  ]
  lancerAssistant('Nouveau héros', etapes, (v) => {
    const nom = v.nom.trim()
    ;(projet.gabarits ??= {})[nom] = { preset: v.preset ?? '', cadre: 'officiel', fissures: true, createur: v.createur ?? '', centrerTexte: false, echelleTexte: 0 }
    const cartes = cartesHeros(v)
    projet.cartes.push(...cartes)
    dossierVu = nom
    choisir(cartes[0].id)
    message(`Héros « ${nom} » créé : ${cartes.length} carte(s).`)
  }, {
    apercu: (v) => {
      const c = nouvelleCarte('identity', langue)
      c.contenu.titre = (v.nom ?? '').trim()
      c.preset = v.preset ?? ''
      appliquerPalette(c, TYPES.identity, c.preset)
      if (v.createur !== undefined) c.contenu.createur = v.createur
      return c
    },
  })
}

// ---------------------------------------------------------------- assistant « Template »
// 30/10/2026 : un seul mot, « Template ». Le template d'un dossier = son apparence commune (couleurs, style du
// cadre, mise en page, mention), appliquee a chaque nouvelle carte du dossier ; on peut y joindre une carte de
// depart complete (l'ancien « modele »), proposee dans la liste des templates.
function ouvrirAssistantTemplate(dossierDepart) {
  const c = carte()
  const etapes = (v) => {
    const spec = TYPES[v.type] ?? TYPES.ally
    return [
      {
        titre: 'À quoi sert un template ?', court: 'Dossier',
        aide: 'Un template garde l’apparence commune à toutes les cartes d’un dossier : couleurs, style du cadre, mise en page du texte et mention du créateur. Chaque nouvelle carte du dossier le prend automatiquement. Choisis le dossier concerné.',
        construire: (v, rafraichir) => choixDossier(v, rafraichir, { avecAucun: false }),
        valider: (v) => (String(v.dossier ?? '').trim() ? undefined : 'Choisis ou nomme un dossier.'),
      },
      {
        titre: 'Les couleurs', court: 'Couleurs',
        aide: 'Neutre (gris), les couleurs d’origine du cadre du jeu, un aspect, ou la palette d’un héros ou d’un méchant existant. « Comme la carte actuelle » reprend exactement ses couleurs, y compris celles réglées à la main.',
        construire: (v) => {
          const s = optionsPalette(spec)
          if (c) s.prepend(el('option', { value: '__carte' }, 'Comme la carte actuelle'))
          s.value = v.preset
          s.addEventListener('change', () => { v.preset = s.value })
          return el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Couleurs'), s)
        },
      },
      {
        titre: 'Le style du cadre', court: 'Cadre',
        aide: '« Officiel » : le cadre du jeu, dans les couleurs choisies. « Sombre » : gris-bleu foncé avec des accents dorés. « Pleine illustration » : pas de cadre, l’image remplit la carte et le texte repose sur des panneaux translucides.',
        construire: (v) => {
          const s = el('select', {}, [['officiel', 'Officiel (gabarit du jeu)'], ['sombre', 'Cadre sombre'], ['illustration', 'Pleine illustration (sans cadre)']].map(([k, n]) => el('option', { value: k }, n)))
          s.value = v.cadre
          s.addEventListener('change', () => { v.cadre = s.value })
          return el('div', { class: 'assistant-pile' }, el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Style'), s),
            caseAssistant(v, 'fissures', 'Fissures dans le cadre', 'Les craquelures des cartes de rencontre (sbires, trahisons…). Sans effet sur les autres types.'))
        },
      },
      {
        titre: 'La mise en page du texte', court: 'Texte',
        aide: 'Une carte à texte court peut avoir son texte centré verticalement dans le cadre, comme beaucoup de cartes officielles.',
        construire: (v) => caseAssistant(v, 'centrerTexte', 'Centrer le texte des règles verticalement', ''),
      },
      {
        titre: 'La mention du créateur', court: 'Mention',
        aide: 'La petite ligne en bas de chaque carte (ton nom, ton pseudo…).',
        construire: (v) => champAssistant(v, 'createur', 'Mention', ''),
      },
      {
        titre: 'Une carte de départ ?', court: 'Carte',
        aide: c ? `En plus de l’apparence, le template peut garder la carte actuelle entière (« ${c.contenu.titre || tr('(sans titre)')} » : type, nombres, texte, illustration) comme point de départ. Elle apparaîtra dans la liste des templates : « Utiliser » en fait une nouvelle carte.` : 'Aucune carte choisie : rien à garder.',
        construire: (v) => (c ? caseAssistant(v, 'garderCarte', 'Garder aussi la carte actuelle comme carte de départ', '') : el('span')),
      },
      {
        titre: 'Appliquer', court: 'Fin',
        aide: 'Le template sera appliqué à chaque nouvelle carte du dossier. Veux-tu aussi le recopier sur les cartes qui y sont déjà ?',
        construire: (v) => caseAssistant(v, 'appliquerDossier', 'Appliquer aussi aux cartes déjà dans ce dossier', '', true),
      },
    ]
  }
  const dossier0 = (dossierDepart ?? c?.dossier ?? '').trim()
  const g0 = projet.gabarits?.[dossier0]
  const depart = {
    dossier: dossier0,
    type: c?.type ?? 'ally',
    preset: g0 ? g0.preset ?? '' : c ? '__carte' : '',
    cadre: g0?.cadre ?? c?.cadre ?? 'officiel',
    fissures: g0?.fissures ?? c?.fissures ?? true,
    centrerTexte: g0?.centrerTexte ?? !!c?.contenu.centrerTexte,
    createur: g0?.createur ?? c?.contenu.createur ?? '',
  }
  // « Comme la carte actuelle » : ses couleurs exactes, gardees dans le template
  const resoudre = (v) => (v.preset === '__carte' ? { preset: c?.preset ?? '', couleurs: structuredClone(c?.couleurs ?? {}) } : { preset: v.preset ?? '' })
  const apercu = (v) => {
    const x = c ? cloner(c) : nouvelleCarte('ally', 'en')
    const r = resoudre(v)
    x.preset = r.preset
    if (r.couleurs) x.couleurs = r.couleurs
    else appliquerPalette(x, TYPES[x.type], r.preset)
    x.cadre = v.cadre
    x.fissures = v.fissures
    x.contenu.centrerTexte = v.centrerTexte
    x.contenu.createur = v.createur
    return x
  }
  lancerAssistant('Template', etapes, (v) => {
    const dossier = v.dossier.trim()
    const r = resoudre(v)
    const gabarit = { preset: r.preset, couleurs: r.couleurs, cadre: v.cadre, fissures: v.fissures, createur: v.createur ?? '', centrerTexte: !!v.centrerTexte, echelleTexte: c?.contenu.echelleTexte ?? 0 }
    ;(projet.gabarits ??= {})[dossier] = gabarit
    if (v.garderCarte && c) { enregistrerModele(`${dossier} · ${c.contenu.titre || tr('(sans titre)')}`); projet.modeles.at(-1).dossier = dossier }
    const cibles = projet.cartes.filter((x) => (x.dossier || '').trim() === dossier && (v.appliquerDossier || x.id === c?.id))
    for (const x of cibles) appliquerGabaritPack(x)
    message(cibles.length ? `${cibles.length} carte(s) mise(s) à jour.` : 'Template enregistré.')
    dossierVu = dossier
    changement()
    construireFormulaire()
    majListe()
    sauvegarderPlusTard()
  }, { valeurs: depart, apercu })
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
    const dos = el('input', { type: 'checkbox', checked: !!(c.verso && c.verso.mode !== 'aucun') })
    const boite = el('dialog', {}, el('div', { class: 'panneau', style: 'min-width:280px' },
      el('h2', {}, 'Exporter'),
      el('label', {}, 'Format', format),
      el('label', {}, `Largeur (px) — taille d’origine ${TYPES[c.type].largeur}`, largeur),
      el('label', { class: 'ligne' }, perdu, 'Fond perdu de 3 mm (bords étirés)'),
      el('label', { class: 'ligne' }, dos, 'Exporter aussi le dos (s’il y en a un)'),
      el('div', { class: 'rang' },
        el('button', { class: 'btn', type: 'button', onclick: () => { boite.close(); ok(null) } }, 'Annuler'),
        el('button', { class: 'btn principal', type: 'button', onclick: () => { boite.close(); ok({ format: format.value, largeur: Number(largeur.value), perdu: perdu.checked, dos: dos.checked }) } }, 'Exporter'))))
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
    const ext = '.' + (o.format === 'jpeg' ? 'jpg' : o.format)
    telecharger(blob, nomFichier(c, deuxLangues ? '_' + l : '') + ext)
    if (o.dos) {
      const dosToile = await rendreVerso(c, l)
      if (dosToile) telecharger(await sortie(dosToile, o), nomFichier(c, (deuxLangues ? '_' + l : '') + '_back') + ext)
    }
  }
  message('Export terminé.')
}
function dialoguePlanche() {
  const dos = el('input', { type: 'checkbox', checked: projet.cartes.some((c) => c.verso?.mode && c.verso.mode !== 'aucun') })
  const dossier = el('select', {}, el('option', { value: 'tout' }, 'Toutes les cartes'), el('option', { value: 'dossier' }, 'Le dossier de la carte choisie'))
  dialogue('Imprimer', el('div', { class: 'contenu', style: 'display:flex;flex-direction:column;gap:8px' },
    el('label', {}, 'Cartes', dossier),
    el('label', { class: 'ligne' }, dos, 'Ajouter les dos sur des pages à part (recto-verso : les dos sont dans l’ordre inverse de chaque rangée)'),
    el('div', { class: 'aide' }, 'Cartes à 63 × 88 mm, 9 par feuille A4, sans marge entre elles : découpe sur les bords. Les cartes paysage sont tournées.')),
  [{ texte: 'Annuler' }, { texte: 'Imprimer', principal: true, action: () => planchePourImprimer({ dos: dos.checked, dossier: dossier.value }) }])
}
async function planchePourImprimer(opts = { dos: false, dossier: 'tout' }) {
  message('Préparation de la planche…')
  const images = []
  const dosImages = []
  const pourPlanche = async (toile) => {
    if (!toile) return null
    const k = 750 / toile.width
    const r = document.createElement('canvas')
    r.width = 750
    r.height = Math.round(toile.height * k)
    r.getContext('2d').drawImage(toile, 0, 0, r.width, r.height)
    if (r.width <= r.height) return r.toDataURL('image/jpeg', 0.92)
    const t = document.createElement('canvas')
    t.width = r.height
    t.height = r.width
    const x = t.getContext('2d')
    x.translate(r.height, 0)
    x.rotate(Math.PI / 2)
    x.drawImage(r, 0, 0)
    return t.toDataURL('image/jpeg', 0.92)
  }
  const cartes = opts.dossier === 'dossier' ? projet.cartes.filter((x) => (x.dossier || '') === (carte().dossier || '')) : projet.cartes
  for (const c of cartes) {
    images.push(await pourPlanche(await rendreCarte(c)))
    dosImages.push(await pourPlanche(await rendreVerso(c)))
  }
  const pages = []
  for (let i = 0; i < images.length; i += 9) {
    const lot = images.slice(i, i + 9)
    pages.push(lot)
    if (opts.dos && dosImages.slice(i, i + 9).some(Boolean)) {
      // le dos d'une carte doit tomber derriere elle : on inverse l'ordre dans chaque rangee de trois (retournement sur le bord long)
      const d = dosImages.slice(i, i + 9)
      const miroir = []
      for (let r = 0; r < d.length; r += 3) miroir.push(...d.slice(r, r + 3).reverse())
      pages.push(miroir.map((x) => x ?? ''))
    }
  }
  const w = window.open('', '_blank')
  if (!w) return message('Le navigateur a bloqué la fenêtre d’impression.')
  w.document.write(`<!doctype html><meta charset="utf-8"><title>Planche d'impression</title><style>
    @page { size: A4; margin: 10mm }
    body { margin: 0 }
    .feuille { display: grid; grid-template-columns: repeat(3, 63mm); grid-auto-rows: 88mm; justify-content: center; break-after: page }
    .feuille:last-child { break-after: auto }
    img { width: 63mm; height: 88mm; display: block }
    .vide { width: 63mm; height: 88mm }
    @media screen { body { background: #ccc; padding: 10mm } .feuille { margin-bottom: 10mm; background: #fff } }
  </style>${pages.map((p) => `<div class="feuille">${p.map((s) => (s ? `<img src="${s}">` : '<div class="vide"></div>')).join('')}</div>`).join('')}<script>onload=()=>setTimeout(()=>print(),400)<\/script>`)
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
  const avecDos = cartes.find((c) => c.verso?.mode && c.verso.mode !== 'aucun')
  if (avecDos) { const d = await rendreVerso(avecDos); if (d) telecharger(await aBlob(d, 'image/png'), 'dos_TTS.png') }
  message(`Planche TTS : ${cartes.length} carte(s), ${colonnes} colonnes (taille de cellule ${L} × ${H}).`)
}

// ---------------------------------------------------------------- projet (fichier)
async function exporterProjet() {
  const cartes = []
  for (const c of projet.cartes) cartes.push(await serialiser(c))
  const modeles = []
  for (const m of projet.modeles ?? []) modeles.push({ id: m.id, nom: m.nom, dossier: m.dossier, carte: await serialiser(m.carte) })
  telecharger(new Blob([JSON.stringify({ format: 'createur-cartes', version: 2, cartes, modeles, styles: projet.styles ?? [], gabarits: projet.gabarits ?? {} })], { type: 'application/json' }), 'cartes.json')
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
      for (const m of j.modeles ?? []) { projet.modeles ??= []; projet.modeles.push({ id: nouvelId(), nom: m.nom, dossier: m.dossier, carte: await deserialiser(m.carte) }) }
      for (const [d, g] of Object.entries(j.gabarits ?? {})) (projet.gabarits ??= {})[d] ??= g
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
    rendreVerso, serialiser,
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
    // les couleurs suivent le nouveau type : celles du template du dossier, sinon le cadre neutre
    c.preset = ''
    appliquerPalette(c, TYPES[c.type], '')
    appliquerGabaritPack(c)
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
  for (const c of projet.cartes) { c.libres ??= []; c.cadre ??= 'officiel'; c.dossier ??= ''; c.verso ??= { mode: 'aucun', carteId: null, blob: null } }
  if (!projet.cartes.some((c) => c.id === projet.courante)) projet.courante = projet.cartes[0].id
  synchro.baseline()

  $('#lang-fr').addEventListener('click', () => changerLangue('fr'))
  $('#lang-en').addEventListener('click', () => changerLangue('en'))
  $('#c-nouvelle').addEventListener('click', () => ouvrirAssistantCarte())
  $('#c-heros').addEventListener('click', () => ouvrirAssistantHeros())
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
  $('#p-versions').addEventListener('click', () => ouvrirVersions(restaurerLocal, synchro.etat !== 'connecte' ? null : {
    dossier: carte().dossier || '',
    versions: () => synchro.versions(carte().dossier),
    restaurer: async (n) => { await ajouterVersion(projet, 'avant restauration'); await synchro.restaurerVersion(carte().dossier, n); apresRapatriement(); message('Version restaurée.') },
  }))
  const restaurerLocal = (p) => { projet = p; projet.cartes = projet.cartes.filter((c) => TYPES[c.type]); for (const c of projet.cartes) { c.libres ??= []; c.cadre ??= 'officiel'; c.dossier ??= ''; c.verso ??= { mode: 'aucun', carteId: null, blob: null } } historiques.clear(); choisir(projet.cartes.some((c) => c.id === projet.courante) ? projet.courante : projet.cartes[0].id); message('Version restaurée.') }
  $('#p-remplacer').addEventListener('click', ouvrirRemplacer)
  $('#p-appliquer').addEventListener('click', () => ouvrirAppliquer(rolesDe))
  // Templates : « g:<dossier> » = le template d'un dossier, « m:<id> » = une carte de depart gardee
  const templateChoisi = () => {
    const v = $('#modeles').value
    if (v.startsWith('g:')) return { dossier: v.slice(2) }
    if (v.startsWith('m:')) return { modele: (projet.modeles ?? []).find((x) => x.id === v.slice(2)) }
    return null
  }
  $('#m-enregistrer').addEventListener('click', () => ouvrirAssistantTemplate(templateChoisi()?.dossier))
  $('#m-utiliser').addEventListener('click', () => {
    const x = templateChoisi()
    if (!x) return message('Choisis d’abord un template.')
    if (x.dossier !== undefined) return ouvrirAssistantCarte(x.dossier)
    const c = { ...cloner(x.modele.carte), id: nouvelId(), dossier: x.modele.dossier ?? carte()?.dossier ?? '' }
    ajouter(c)
  })
  $('#m-supprimer').addEventListener('click', () => {
    const x = templateChoisi()
    if (!x) return message('Choisis d’abord un template.')
    if (x.dossier !== undefined) {
      if (!confirm(tr(`Supprimer le template du dossier « ${x.dossier} » ? Les cartes ne changent pas.`))) return
      delete projet.gabarits[x.dossier]
    } else projet.modeles = (projet.modeles ?? []).filter((m) => m !== x.modele)
    majListe()
    sauvegarderPlusTard()
  })
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
  $('#b-print').addEventListener('click', dialoguePlanche)
  $('#b-pack').addEventListener('click', () => ouvrirExportPack({ cartes: () => projet.cartes, carte, rendre: rendreCarte, rendreVerso, serialiser }))
  $('#b-tts').addEventListener('click', plancheTTS)
  $('#b-comparer').addEventListener('click', () => ouvrirComparable(rendreCarte))
  $('#p-exporter').addEventListener('click', exporterProjet)
  $('#p-importer').addEventListener('click', () => $('#p-fichier').click())
  $('#p-fichier').addEventListener('change', async (e) => {
    try { await importerFichiers([...e.target.files]) } catch (err) { message('Ouverture impossible : ' + err.message) }
    e.target.value = ''
  })
  brancherToile()
  choisir(projet.courante)
  synchro.demarrer() // sans attendre : la page marche tout de suite avec ce qu'elle a, la fusion arrive ensuite
}
demarrer().catch((e) => message('Démarrage impossible : ' + e.message))
