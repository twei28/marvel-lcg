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
import { creerZip } from './zip.js'
import { MODES, NOMS_ETIQUETTE, POLICES, POLICE_PERSO, DIMENSIONS, chargerCalques, couleurOrigine, nouvellePochette, texteLibre, titreDefaut, changerMode, rendrePochette, nomFichierPochette } from './pochettes.js'
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
      await ecrireProjet(sansBrouillon())
      versionsModifie = true
      synchro.planifier()
    } catch (e) {
      message('Sauvegarde dans le navigateur impossible : ' + e.message)
    }
  }, 500)
}
/** Le projet tel qu'on l'ecrit : sans la carte en cours de creation dans le wizard (un brouillon n'existe pas encore). */
const sansBrouillon = () => ({ ...projet, cartes: projet.cartes.filter((c) => !c.brouillon) })
// Une version est gardee toutes les 5 minutes (si quelque chose a change) et quand on quitte la page.
let versionsModifie = false
async function garderVersion(raison = 'auto') {
  if (!versionsModifie) return
  versionsModifie = false
  try { await ajouterVersion(sansBrouillon(), raison) } catch {}
}
setInterval(() => garderVersion('auto'), 5 * 60 * 1000)
addEventListener('pagehide', () => { clearTimeout(minuteurSauvegarde); synchro.avantSauvegarde(); ecrireProjet(sansBrouillon()).catch(() => {}); garderVersion('fermeture') })

/** Apres que des dossiers (ou les reglages) viennent du serveur : la page repart de ce que contient le projet. */
function apresRapatriement() {
  preparerProjet(projet)
  historiques.clear()
  if (vue === 'accueil') return rendreAccueil()
  if (!listeDossiers().some((d) => d.nom === dossierOuvert)) return afficherAccueil()
  ouvrirDossier(dossierOuvert, projet.cartes.some((c) => c.id === projet.courante) ? projet.courante : null)
}

/** L'indicateur de l'en-tete : ou est enregistre le travail. Cache hors du site (mode local). */
function majIndicateurServeur() {
  const z = $('#etat-serveur')
  if (!z) return
  z.className = 'etat-serveur doux'
  z.title = ''
  if (synchro.etat === 'local') {
    z.hidden = false
    z.textContent = '💾 Enregistré dans ce navigateur seulement : pense à « Tout enregistrer (.zip) »'
    z.title = 'Si tu effaces l’historique ou les données du navigateur, tes cartes disparaissent. Le fichier .zip te permet de tout retrouver.'
    return
  }
  z.hidden = false
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
  // « sombre » : les gris-bleus l'emportent, sauf sur les couleurs que le joueur a reglees lui-meme (toute carte porte des couleurs : celles du template ou le gris neutre)
  const couleurs = c.cadre === 'sombre' ? (c.couleursPerso ? { ...couleursSombres(TYPES[c.type]), ...c.couleurs } : { ...c.couleurs, ...couleursSombres(TYPES[c.type]) }) : { ...c.couleurs }
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
    if (t.infos?.deborde) deborde.add(c.id); else deborde.delete(c.id)
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
  if (carte()?.brouillon) return // la carte du wizard : on la dessine, rien d'autre
  sauvegarderPlusTard()
  majListe()
  majFil()
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
const ICONES_RUBRIQUES = { Texte: '✎', Nombres: '#', 'Boost et ressources': '⚡', Couleurs: '●', Illustration: '▣', 'Calques PNG': '❏', 'Dos de la carte': '▭', 'Style du cadre': '▢' }
function section(titre, ouvert, ...contenu) {
  const d = el('details', { open: ouvert, 'data-titre': titre }, el('summary', {}, el('span', { class: 'ico-rub' }, ICONES_RUBRIQUES[titre] ?? '•'), titre), el('div', { class: 'contenu' }, contenu))
  return d
}
// Les sections du formulaire sont TOUTES repliees a l'ouverture d'une carte (30/10/2026, « je veux que tout soit replié ») ;
// celles qu'on ouvre le restent tant qu'on reste sur la carte (le formulaire se reconstruit a chaque reglage).
const sectionsOuvertes = new Set()
let carteDesSections = null
function replierSections(blocs, idCarte) {
  if (carteDesSections !== idCarte) { sectionsOuvertes.clear(); carteDesSections = idCarte }
  for (const d of blocs) {
    if (d.tagName !== 'DETAILS') continue
    const cle = d.dataset.titre ?? d.querySelector(':scope > summary')?.textContent ?? ''
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

// ---------------------------------------------------------------- blocs du formulaire (partages avec le wizard)
// Chaque bloc rend des noeuds pour la carte courante : le formulaire les range en rubriques, le wizard en etapes.
const RECENTES = 'createur-couleurs-recentes'
function couleursRecentes() { try { return JSON.parse(localStorage.getItem(RECENTES) ?? '[]') } catch { return [] } }
function noterRecente(hex) {
  try { localStorage.setItem(RECENTES, JSON.stringify([hex, ...couleursRecentes().filter((x) => x !== hex)].slice(0, 10))) } catch {}
}
/** Un champ couleur : pastille cliquable, code hexadecimal, pipette, puis les couleurs recentes (et celles qu'on propose, ex. le template). */
function pickerCouleur(valeur, onChange, proposees = []) {
  const i = el('input', { type: 'color', value: hex6(valeur), 'aria-label': 'Couleur' })
  const hex = el('input', { type: 'text', class: 'hex', value: hex6(valeur), maxlength: 7, 'aria-label': 'Code couleur', spellcheck: 'false' })
  const barre = el('div', { class: 'recentes' })
  const poser = (v) => { i.value = v; hex.value = v; onChange(v); noterRecente(v); pastilles() }
  function pastilles() {
    const toutes = [...new Set([...proposees, ...couleursRecentes()].map((x) => String(x).toLowerCase()))].slice(0, 14)
    barre.replaceChildren(...toutes.map((cl) => el('button', { type: 'button', class: 'pastille', style: `background:${cl}`, title: cl, onclick: () => poser(cl) })))
  }
  i.addEventListener('input', () => { hex.value = i.value; onChange(i.value) })
  i.addEventListener('change', () => { noterRecente(i.value); pastilles() })
  hex.addEventListener('input', () => {
    let v = hex.value.trim()
    if (/^[0-9a-f]{6}$/i.test(v)) v = '#' + v
    if (/^#[0-9a-f]{6}$/i.test(v)) { i.value = v; onChange(v) }
  })
  hex.addEventListener('change', () => { if (/^#[0-9a-f]{6}$/i.test(hex.value.trim())) { noterRecente(hex.value.trim().toLowerCase()); pastilles() } else hex.value = i.value })
  pastilles()
  return el('div', { class: 'pick-bloc' }, el('div', { class: 'pick' }, i, hex, pipette(i)), barre)
}

/** Une bulle « ? » : un bouton qui ouvre une explication longue juste dessous. Rend [bouton, bulle]. */
function bulleAide(texte) {
  const bulle = el('div', { class: 'bulle-aide', hidden: true }, texte)
  const b = el('button', { class: 'btn petit btn-bulle', type: 'button', title: 'Plus d’explications', 'aria-expanded': 'false', onclick: () => { bulle.hidden = !bulle.hidden; b.setAttribute('aria-expanded', String(!bulle.hidden)) } }, '?')
  return [b, bulle]
}
/** Un noeud accompagne de sa bulle « ? » (le bouton a droite, l'explication dessous). */
function avecAide(noeud, texte) {
  const [b, bulle] = bulleAide(texte)
  return el('div', { class: 'avec-aide' }, el('div', { class: 'rang', style: 'align-items:flex-end;flex-wrap:nowrap' }, noeud, b), bulle)
}

function blocTitre(spec) {
  const b = [t('Titre', 'titre'), coche('Carte unique (✦)', (x) => x.contenu, 'unique')]
  if (aElement(spec, 'typestr')) b.push(t('Libellé du type (vide = automatique)', 'typeTexte'))
  if (aElement(spec, 'traits')) b.push(t('Traits (séparés par des points)', 'traits'))
  return b
}
function blocRegles(c, spec) {
  const b = []
  if (aElement(spec, 'rules')) b.push(editeurRiche('Règles', 'regles', 6))
  if (aElement(spec, 'quote')) b.push(editeurRiche('Citation', 'citation', 3))
  if (aElement(spec, 'rules')) {
    const auto = !(Number(c.contenu.echelleTexte) > 0)
    const r = el('input', { type: 'range', min: 40, max: 130, step: 1, value: auto ? 100 : Math.round(c.contenu.echelleTexte * 100) })
    const val = el('span', { class: 'aide' }, auto ? 'automatique' : r.value + ' %')
    r.addEventListener('input', () => { c.contenu.echelleTexte = Number(r.value) / 100; val.textContent = r.value + ' %'; changement() })
    b.push(el('label', {}, el('span', { class: 'rang' }, 'Taille des règles et de la citation', val), r,
      el('button', { class: 'btn petit', type: 'button', onclick: () => { c.contenu.echelleTexte = 0; changement(); construireFormulaire() } }, 'Automatique (réduit pour tenir)')))
    b.push(coche('Centrer le texte verticalement (comme les cartes officielles à texte court)', (x) => x.contenu, 'centrerTexte'))
  }
  return b
}
function blocLigne(c, spec) {
  const b = []
  if (aElement(spec, 'villainstagenew')) b.push(t('Étape du méchant (I, II, A, B…)', 'etape'))
  if (aElement(spec, 'set-line')) b.push(t('Ligne d’ensemble', 'ligneEnsemble'))
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
    b.push(el('label', { class: 'ligne' }, i, 'Points de vie par joueur (icône en fin de ligne)'))
  }
  if (aElement(spec, 'c-line')) b.push(t('Créateur / mention', 'createur'))
  return b
}
/** Les nombres de la carte : [{ noeud, aide }] (l'aide sert au wizard). */
function blocNombres(spec) {
  const N = []
  for (const n of nombresDuType(spec)) {
    N.push({ aide: n.aide, noeud: n.conseq ? liste(n.label, (x) => x.contenu, n.cle, [0, 1, 2, 3, 4, 5].map((k) => [k, k]), Number) : nombre(n.label, n.cle, n.etoile) })
  }
  if (aElement(spec, 'mainschemephase cost')) N.push({ aide: 'Le numéro de la manigance dans le scénario (1, 2, 3…) et sa face (A ou B).', noeud: el('div', { class: 'rang' }, t('Phase : numéro', 'phaseNumero'), t('Phase : lettre', 'phaseLettre')) })
  return N
}
function blocBoost(c, spec) {
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
  return R
}

const ROLES_PRINCIPAUX = ['left_color', 'right_color', 'left_accent', 'background_upper', 'background_lower', 'accent', 'divider', 'middle', 'splash_color']
/** Les couleurs d'une carte : pastilles de raccourci, pickers (3 principaux puis « Plus de couleurs »), d'ou elles viennent. */
function blocCouleurs(c, spec, { repli = true, apres = null, quand = changement, origineVisible = true } = {}) {
  const roles = rolesDe(spec)
  if (!roles.length) return [el('div', { class: 'aide' }, 'Ce type de carte n’a pas de couleurs à régler.')]
  const g = projet.gabarits?.[(c.dossier || '').trim()]
  const proposees = [...Object.values(g?.couleurs ?? {}), ...Object.values(c.couleurs ?? {})].filter((x) => /^#[0-9a-f]{6}$/i.test(x)).slice(0, 6)
  const origine = el('span', { class: 'origine' })
  const revenir = g ? el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { appliquerGabaritPack(c); quand(); apres?.(true) } }, 'Revenir au template') : null
  const majOrigine = () => {
    if (revenir) revenir.hidden = !c.couleursPerso
    origine.className = 'origine' + (c.couleursPerso ? ' perso' : '')
    origine.textContent = c.couleursPerso ? 'Couleurs personnalisées' : g ? 'Couleurs du template' : 'Couleurs neutres'
  }
  majOrigine()
  const changeeParLeJoueur = () => { c.couleursPerso = true; majOrigine(); quand(); apres?.(false) }
  const raccourcis = el('div', { class: 'pastilles', role: 'group', 'aria-label': 'Raccourcis de couleurs' })
  const choix = [['', 'Neutre (gris)', '#6e7179'], ...(spec.famille === 'villain' ? [] : Object.keys(ASPECTS).filter((n) => !n.startsWith('Basic')).map((n) => [n, n, ASPECTS[n].left_color]))]
  for (const [cle, nom, cl] of choix) {
    raccourcis.append(el('button', {
      type: 'button', class: 'pastille', style: `background:${cl}`, title: tr(nom),
      onclick: () => { c.preset = cle; appliquerPalette(c, spec, cle); c.couleursPerso = true; quand(); apres?.(true) },
    }))
  }
  const principaux = ROLES_PRINCIPAUX.filter((r) => roles.includes(r)).slice(0, 3)
  const autres = roles.filter((r) => !principaux.includes(r))
  const champ = (r) => el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, ROLES_COULEURS[r]),
    pickerCouleur(couleurDe(c, spec, r), (v) => { c.couleurs[r] = v; c.preset = ''; changeeParLeJoueur() }, proposees))
  const bloc = [
    el('div', { class: 'rang', style: 'align-items:center' }, origineVisible ? origine : null,
      revenir),
    el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Raccourcis'), raccourcis),
    ...principaux.map(champ),
  ]
  if (autres.length) {
    const reste = el('div', { class: 'couleurs' }, ...autres.map(champ))
    if (repli) bloc.push(el('details', {}, el('summary', {}, 'Plus de couleurs'), el('div', { class: 'contenu' }, reste)))
    else bloc.push(reste)
  }
  const preset = optionsPalette(spec)
  preset.value = c.preset ?? ''
  preset.addEventListener('change', () => { c.preset = preset.value; appliquerPalette(c, spec, preset.value); c.couleursPerso = true; quand(); apres?.(true) })
  bloc.push(el('label', {}, 'Partir de la palette d’un héros ou d’un méchant du jeu', preset))
  return bloc
}
function blocDos(c) {
  const v = (c.verso ??= { mode: 'aucun', carteId: null, blob: null })
  const autres = projet.cartes.filter((x) => x.id !== c.id && !x.brouillon)
  const mode = liste('Dos', (x) => x.verso, 'mode', [['aucun', 'Aucun'], ['joueur', 'Dos des cartes joueur'], ['rencontre', 'Dos des cartes rencontre'], ['carte', 'Une autre carte (autre face)'], ['image', 'Mon image']], (m) => m)
  mode.querySelector('select').addEventListener('change', () => { v.choisi = true; construireFormulaire(); reconstruireEtape() })
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
  return parts
}
const CADRES = [['officiel', 'Officiel (gabarit du jeu)'], ['sombre', 'Cadre sombre'], ['illustration', 'Pleine illustration (sans cadre)']]
function blocCadre(c) {
  return [
    liste('Style', (x) => x, 'cadre', CADRES, (v) => v),
    el('div', { class: 'aide' }, '« Cadre sombre » remplace les couleurs par un gris-bleu foncé avec des accents dorés (tu peux encore les modifier dans Couleurs). « Pleine illustration » enlève le cadre : l’image remplit la carte et le texte repose sur des panneaux translucides.'),
    TYPES_SANS_FISSURES.has(c.type) ? coche('Fissures dans le cadre', (x) => x, 'fissures') : null,
  ]
}
/** Le dos « automatique » selon le type : les cartes joueur ont le dos joueur, celles de rencontre le dos rencontre. */
function dosAutomatique(c) {
  const v = (c.verso ??= { mode: 'aucun', carteId: null, blob: null })
  if (v.mode !== 'aucun' || v.choisi) return
  v.mode = TYPES[c.type]?.famille === 'villain' ? 'rencontre' : 'joueur'
}

function construireFormulaire() {
  const c = carte()
  const racine = $('#champs')
  racine.replaceChildren()
  if (!c) return
  const spec = TYPES[c.type]
  $('#type').value = c.type
  const f = []
  f.push(section('Texte', false, ...blocTitre(spec), ...blocRegles(c, spec), ...blocLigne(c, spec)))
  const N = blocNombres(spec).map((n) => n.noeud)
  if (N.length) f.push(section('Nombres', false, ...N))
  const R = blocBoost(c, spec)
  if (R.length) f.push(section('Boost et ressources', false, ...R))
  if (rolesDe(spec).length) f.push(section('Couleurs', false, ...blocCouleurs(c, spec, { repli: false, apres: (r) => r && construireFormulaire() })))
  f.push(section('Illustration', false, ...boiteImage('Image derrière la carte', (x) => x.art, 'art'), el('hr'), ...boiteImage('Premier plan (devant le cadre)', (x) => x.artDevant, 'artDevant')))
  f.push(sectionLibres())
  f.push(section('Dos de la carte', false, ...blocDos(c)))
  // La « Tête d'angle » (image de coin pour certaines cartes) a ete retiree du formulaire le
  // 29/10/2026 : le reglage (zoom/decalage/rotation/detourage) ne fonctionnait pas, sur demande
  // de l'utilisateur. `rendu.js:teteVisible` ne dessine plus rien non plus.
  f.push(section('Style du cadre', false, ...blocCadre(c)))
  replierSections(f, c.id)
  racine.append(...f)
  majAide()
}
function majAide() {
  const cible = { art: 'l’illustration', artDevant: 'le premier plan', tete: 'la tête d’angle' }[ciblePointeur]
  $('#aide-toile').textContent = `Glisse sur l’aperçu pour déplacer ${cible} (molette : zoom).`
}

// ---------------------------------------------------------------- dossiers
// 30/10/2026 : le createur s'ouvre sur la PAGE DES DOSSIERS (un par heros, scenario ou modulaire) ; un clic ouvre l'editeur
// de ce dossier. Toute carte a un dossier (celles qui n'en avaient pas sont rangees dans « Divers »). Les dossiers vides
// existent (`projet.dossiers[nom] = { genre, ordre }`), comme leur template (`projet.gabarits[nom]`).
const DIVERS = 'Divers'
const GENRES_DOSSIER = { heros: 'Héros', scenario: 'Scénario', modulaire: 'Modulaire', divers: 'Divers' }
const TYPES_HEROS = new Set(['identity', 'alter-ego', 'ally', 'event', 'upgrade', 'support', 'resource', 'obligation', 'playersidescheme', 'identity-promo', 'alter-ego-promo'])
const ORDRE_TYPES = ['identity', 'alter-ego', 'ally', 'event', 'upgrade', 'support', 'resource', 'obligation', 'playersidescheme', 'villain', 'main_scheme_a', 'main_scheme_b', 'minion', 'treachery', 'sidescheme', 'attachment', 'environment', 'obligation-villain', 'identity-promo', 'alter-ego-promo', 'generic-promo', 'generic-promo-vert', 'starter-deck']
const vraiesCartes = () => projet.cartes.filter((c) => !c.brouillon)
const cartesDuDossier = (nom) => vraiesCartes().filter((c) => (c.dossier || '') === nom)

function genreInfere(nom) {
  const types = new Set(cartesDuDossier(nom).map((c) => c.type))
  if (nom === DIVERS) return 'divers'
  if (types.has('identity') || types.has('alter-ego')) return 'heros'
  if (types.has('villain') || types.has('main_scheme_a') || types.has('main_scheme_b')) return 'scenario'
  if ([...types].some((t) => TYPES[t]?.famille === 'villain')) return 'modulaire'
  return types.size && [...types].every((t) => TYPES_HEROS.has(t)) ? 'heros' : 'divers'
}
/** Tous les dossiers : [{ nom, genre, ordre, cartes }], dans l'ordre choisi. */
function listeDossiers() {
  projet.dossiers ??= {}
  const noms = new Set([...Object.keys(projet.dossiers), ...Object.keys(projet.gabarits ?? {}), ...vraiesCartes().map((c) => c.dossier).filter(Boolean)])
  return [...noms].map((nom) => {
    const m = (projet.dossiers[nom] ??= { genre: genreInfere(nom), ordre: Object.keys(projet.dossiers).length })
    return { nom, genre: m.genre, ordre: m.ordre ?? 0, cartes: cartesDuDossier(nom) }
  }).sort((a, b) => a.ordre - b.ordre || a.nom.localeCompare(b.nom))
}
function creerDossier(nom, genre) {
  projet.dossiers ??= {}
  if (!projet.dossiers[nom]) projet.dossiers[nom] = { genre, ordre: Math.max(-1, ...Object.values(projet.dossiers).map((m) => m.ordre ?? 0)) + 1 }
  return projet.dossiers[nom]
}
const nomLibre = (base) => {
  const pris = new Set(listeDossiers().map((d) => d.nom))
  if (!pris.has(base)) return base
  for (let k = 2; ; k++) if (!pris.has(`${base} (${k})`)) return `${base} (${k})`
}
/** Les cartes sans dossier (anciens projets) vont dans « Divers » ; une carte appartient toujours a un dossier. */
function ranger() {
  const libres = projet.cartes.filter((c) => !c.dossier && !c.brouillon)
  if (libres.length) { creerDossier(DIVERS, 'divers'); for (const c of libres) c.dossier = DIVERS }
}
function renommerDossier(ancien, nouveau) {
  nouveau = nouveau.trim()
  if (!nouveau || nouveau === ancien) return null
  if (listeDossiers().some((d) => d.nom === nouveau)) return 'Un dossier porte déjà ce nom.'
  for (const c of projet.cartes) if ((c.dossier || '') === ancien) c.dossier = nouveau
  if (projet.dossiers?.[ancien]) { projet.dossiers[nouveau] = projet.dossiers[ancien]; delete projet.dossiers[ancien] }
  if (projet.gabarits?.[ancien]) { projet.gabarits[nouveau] = projet.gabarits[ancien]; delete projet.gabarits[ancien] }
  for (const m of projet.modeles ?? []) if (m.dossier === ancien) m.dossier = nouveau
  for (const p of vraiesPochettes()) if (p.dossier === ancien) p.dossier = nouveau
  if (dossierOuvert === ancien) dossierOuvert = nouveau
  return null
}
function dupliquerDossier(nom) {
  const copie = nomLibre(`${nom} (${langueUI() === 'fr' ? 'copie' : 'copy'})`)
  const src = cartesDuDossier(nom)
  const ids = new Map(src.map((c) => [c.id, nouvelId()]))
  for (const c of src) {
    const x = { ...cloner(c), id: ids.get(c.id), dossier: copie }
    if (x.verso?.mode === 'carte' && ids.has(x.verso.carteId)) x.verso.carteId = ids.get(x.verso.carteId)
    projet.cartes.push(x)
  }
  projet.dossiers[copie] = { genre: projet.dossiers[nom]?.genre ?? genreInfere(nom), ordre: (projet.dossiers[nom]?.ordre ?? 0) + 0.5 }
  if (projet.gabarits?.[nom]) projet.gabarits[copie] = structuredClone(projet.gabarits[nom])
  for (const p of pochettesDuDossier(nom)) vraiesPochettes().push({ ...p, id: nouvelId(), dossier: copie, art: { ...p.art }, titre: { ...p.titre }, textes: p.textes.map((t) => ({ ...t })) })
  return copie
}
function supprimerDossier(nom) {
  projet.cartes = projet.cartes.filter((c) => (c.dossier || '') !== nom)
  delete projet.dossiers?.[nom]
  delete projet.gabarits?.[nom]
  projet.modeles = (projet.modeles ?? []).filter((m) => m.dossier !== nom)
  projet.pochettes = vraiesPochettes().filter((p) => p.dossier !== nom)
  historiques.clear()
  if (!projet.cartes.some((c) => c.id === projet.courante)) projet.courante = null
}

// ---------------------------------------------------------------- les deux vues : accueil des dossiers / editeur d'un dossier
let vue = 'accueil'
let dossierOuvert = ''
let filtreAccueil = ''
function montrerVue(v) {
  vue = v
  document.body.dataset.vue = v
  $('#vue-accueil').hidden = v !== 'accueil'
  $('#vue-editeur').hidden = v !== 'editeur'
  $('#vue-pochette').hidden = v !== 'pochette'
  fermerMenus()
  majFil()
}
function majFil() {
  const fil = $('#fil')
  if (!fil) return
  const sep = () => el('span', { class: 'sep' }, '›')
  if (vue === 'accueil') { fil.replaceChildren(el('span', { class: 'ici' }, 'Dossiers')); return }
  if (vue === 'pochette') {
    const p = pochetteParId(pochetteOuverte)
    fil.replaceChildren(el('button', { type: 'button', onclick: () => afficherAccueil() }, 'Dossiers'), sep(),
      ...(p?.dossier ? [el('button', { type: 'button', onclick: () => ouvrirDossier(p.dossier) }, p.dossier), sep()] : []),
      el('span', { class: 'ici' }, (p && (nomPochette(p) || libellePochette(p.mode))) || 'Pochette'))
    return
  }
  const c = carte()
  fil.replaceChildren(
    el('button', { type: 'button', onclick: () => afficherAccueil() }, 'Dossiers'), sep(),
    c ? el('button', { type: 'button', onclick: () => ouvrirDossier(dossierOuvert) }, dossierOuvert) : el('span', { class: 'ici' }, dossierOuvert),
    ...(c ? [sep(), el('span', { class: 'ici' }, c.contenu.titre || '(sans titre)')] : []))
}
function afficherAccueil() {
  validerHistorique()
  montrerVue('accueil')
  document.body.removeAttribute('data-vide')
  rendreAccueil()
}
function ouvrirDossier(nom, idCarte = null) {
  validerHistorique()
  dossierOuvert = nom
  const cartes = cartesDuDossier(nom)
  montrerVue('editeur')
  const vide = !cartes.length
  document.body.toggleAttribute('data-vide', vide)
  $('#vue-editeur').classList.toggle('est-vide', vide)
  $('#vide-dossier').hidden = !vide
  if (vide) {
    projet.courante = null
    $('#vide-dossier h3').textContent = nom
    majListe(); majPanneauTemplate(); majBoutonsLangue(); majBoutonsHistorique(); majFil()
    return
  }
  const cible = idCarte ?? (cartes.some((c) => c.id === projet.courante) ? projet.courante : (cartes.find((c) => c.type === 'identity') ?? cartes[0]).id)
  majPanneauTemplate()
  choisir(cible)
}

// ---------------------------------------------------------------- miniatures (accueil et colonne des cartes)
const miniaturesCache = new Map()
const derniereMini = new Map() // id de carte -> derniere miniature connue (affichee pendant qu'on refait la nouvelle)
const fileMini = []
let miniEnCours = false
const cleMini = (c) => JSON.stringify([c.type, c.langue, c.contenu, c.couleurs, c.cadre, c.fissures, c.art?.blob?.size, c.art?.blob?.lastModified, c.art?.zoom, c.art?.x, c.art?.y, c.art?.rotation, c.libres?.length])
function miniatureDans(noeud, c) {
  if (!c) return
  const cle = cleMini(c)
  const prete = miniaturesCache.get(cle) ?? derniereMini.get(c.id)
  if (prete) noeud.style.backgroundImage = `url(${prete})`
  if (miniaturesCache.has(cle)) return
  fileMini.push({ noeud, c: cloner(c), id: c.id, cle })
  setTimeout(pomperMiniatures, 250)
}
async function pomperMiniatures() {
  if (miniEnCours) return
  miniEnCours = true
  while (fileMini.length) {
    const j = fileMini.shift()
    if (miniaturesCache.has(j.cle)) { j.noeud.style.backgroundImage = `url(${miniaturesCache.get(j.cle)})`; continue }
    if (!j.noeud.isConnected) continue
    try {
      const t = await rendreCarte(j.c)
      const m = document.createElement('canvas')
      m.width = 160
      m.height = Math.round(t.height * (160 / t.width))
      m.getContext('2d').drawImage(t, 0, 0, m.width, m.height)
      const url = m.toDataURL('image/jpeg', 0.72)
      if (miniaturesCache.size > 400) miniaturesCache.clear()
      miniaturesCache.set(j.cle, url)
      derniereMini.set(j.id, url)
      j.noeud.style.backgroundImage = `url(${url})`
    } catch {}
    await new Promise((r) => setTimeout(r, 25))
  }
  miniEnCours = false
}

// ---------------------------------------------------------------- l'accueil
function menuFlottant(ancre, entrees) {
  fermerMenus()
  const r = ancre.getBoundingClientRect()
  const m = el('div', { class: 'menu-flottant', role: 'menu' }, ...entrees.map(([texte, action, danger]) =>
    el('button', { class: 'btn petit' + (danger ? ' danger' : ''), type: 'button', role: 'menuitem', onclick: () => { fermerMenus(); action() } }, texte)))
  document.body.append(m)
  m.style.top = Math.min(r.bottom + 4, innerHeight - m.offsetHeight - 8) + 'px'
  m.style.left = Math.max(8, Math.min(r.right - m.offsetWidth, innerWidth - m.offsetWidth - 8)) + 'px'
}
function fermerMenus() {
  for (const m of document.querySelectorAll('.menu-flottant')) m.remove()
  const mx = $('#menu-export')
  if (mx) { mx.hidden = true; $('#b-exporter')?.setAttribute('aria-expanded', 'false') }
}
const CREER = [
  ['heros', 'cartes', 'Héros', 'Un pack de héros : identité, alter-ego et ses 15 cartes.'],
  ['scenario', 'cartes', 'Scénario', 'Le méchant, ses manigances et ses cartes de rencontre.'],
  ['modulaire', 'cartes', 'Modulaire', 'Un set de cartes de rencontre, sans méchant.'],
  ['heros', 'pochette', 'Pochette héros', 'La couverture d’un pack de héros.'],
  ['scenario', 'pochette', 'Pochette scénario', 'La couverture d’un scénario (ou d’un modulaire).'],
  ['boite', 'pochette', 'Pochette extension', 'L’avant d’une boîte d’extension.'],
]
function construireAccueil() {
  const racine = $('#vue-accueil')
  const recherche = el('input', { type: 'search', placeholder: 'Chercher un dossier ou une carte…', 'aria-label': 'Chercher un dossier ou une carte', value: filtreAccueil })
  recherche.addEventListener('input', () => { filtreAccueil = recherche.value; rendreGrilles() })
  const creer = el('div', { class: 'grille-creer' }, ...CREER.map(([genre, famille, libelle, aide]) => el('button', {
    class: `tuile-plus tuile-creer ${famille}`, type: 'button', 'data-creer': genre, 'data-famille': famille,
    onclick: () => (famille === 'cartes' ? dialogueNouveauDossier(genre) : ouvrirWizardPochette(genre)),
  }, el('span', { class: 'plus' }, '+'), el('span', { class: 'libelle' }, libelle), el('small', {}, aide))))
  racine.replaceChildren(
    el('section', { class: 'zone-creer' }, el('h2', { class: 'grand-titre' }, 'Que veux-tu créer ?'), creer),
    el('div', { class: 'accueil-tete' }, el('h2', {}, 'Mes dossiers'), recherche),
    el('div', { class: 'aide' }, 'Un dossier par héros (avec son alter-ego), par scénario ou par set modulaire. Clique sur un dossier pour travailler sur ses cartes.'),
    el('div', { id: 'grilles' }))
}
function tuileDossier(d, grille) {
  const ident = d.cartes.find((c) => c.type === 'identity') ?? d.cartes.find((c) => c.type === 'villain') ?? d.cartes[0]
  const alter = d.cartes.find((c) => c.type === 'alter-ego')
  const g = projet.gabarits?.[d.nom]
  const teinte = g?.couleurs?.left_color ?? g?.couleurs?.background_upper ?? couleurDuPreset(g?.preset) ?? ident?.couleurs?.left_color ?? ident?.couleurs?.background_upper ?? '#3f86e0'
  const mini = el('div', { class: 'mini' }, ident ? '' : 'vide')
  miniatureDans(mini, ident)
  const sous = d.genre === 'heros' ? (alter?.contenu.titre || '') : tr(GENRES_DOSSIER[d.genre])
  const t = el('div', { class: 'tuile', role: 'button', tabindex: '0', draggable: 'true', style: `--teinte:${teinte}`, 'data-nom': d.nom },
    mini,
    el('div', {}, el('div', { class: 'nom' }, (d.genre === 'heros' && ident?.contenu.titre) || d.nom), sous ? el('div', { class: 'alter' }, sous) : null,
      el('div', { class: 'compte' }, d.cartes.length ? `${d.cartes.length} carte(s)` : 'Dossier vide'), ident?.contenu.titre && ident.contenu.titre !== d.nom ? el('div', { class: 'compte' }, '📁 ' + d.nom) : null),
    el('button', { class: 'menu-pt', type: 'button', title: 'Actions du dossier', 'aria-label': 'Actions du dossier', onclick: (e) => { e.stopPropagation(); menuDossier(e.currentTarget, d) } }, '⋯'))
  const ouvrir = () => ouvrirDossier(d.nom)
  t.addEventListener('click', ouvrir)
  t.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); ouvrir() } })
  t.addEventListener('dragstart', (e) => { e.dataTransfer.setData('text/plain', d.nom); t.classList.add('glisse') })
  t.addEventListener('dragend', () => t.classList.remove('glisse'))
  t.addEventListener('dragover', (e) => { e.preventDefault(); t.classList.add('cible') })
  t.addEventListener('dragleave', () => t.classList.remove('cible'))
  t.addEventListener('drop', (e) => {
    e.preventDefault(); t.classList.remove('cible')
    const source = e.dataTransfer.getData('text/plain')
    if (!source || source === d.nom) return
    const noms = [...grille.querySelectorAll('.tuile')].map((x) => x.dataset.nom).filter((x) => x !== source)
    noms.splice(noms.indexOf(d.nom), 0, source)
    noms.forEach((n, i) => { if (projet.dossiers[n]) projet.dossiers[n].ordre = i })
    sauvegarderPlusTard(); rendreGrilles()
  })
  return t
}
function rendreGrilles() {
  const zone = $('#grilles')
  if (!zone) return
  const q = filtreAccueil.trim().toLowerCase()
  const tous = listeDossiers()
  const correspond = (d) => !q || [d.nom, ...d.cartes.flatMap((c) => [c.contenu.titre])].some((x) => String(x ?? '').toLowerCase().includes(q))
  const rangee = (titre, genres, plus) => {
    const liste = tous.filter((d) => genres.includes(d.genre) && correspond(d))
    if (!liste.length && !plus.length && !q) return null
    const grille = el('div', { class: 'grille-dossiers' })
    grille.append(...liste.map((d) => tuileDossier(d, grille)), ...(q ? [] : plus))
    return el('section', { class: 'rangee-dossiers' }, el('h3', {}, titre), grille)
  }
  const noeuds = [
    rangee('Héros', ['heros'], []),
    rangee('Scénarios et modulaires', ['scenario', 'modulaire'], []),
    rangee('Divers', ['divers'], []),
  ].filter(Boolean)
  // les pochettes independantes (celles d'un dossier vivent dans ce dossier) ; une recherche les trouve toutes
  const pochettes = vraiesPochettes().filter((p) => (q ? [nomPochette(p), p.dossier, libellePochette(p.mode)].some((x) => String(x ?? '').toLowerCase().includes(q)) : !p.dossier))
  if (pochettes.length) noeuds.push(el('section', { class: 'rangee-dossiers rangee-pochettes' }, el('h3', {}, 'Pochettes'), el('div', { class: 'grille-dossiers' }, ...pochettes.map(tuilePochette))))
  if (!noeuds.length && !q) noeuds.push(el('div', { class: 'aide' }, 'Tu n’as encore rien créé : choisis une tuile ci-dessus pour commencer.'))
  if (q) {
    const trouvees = vraiesCartes().filter((c) => [c.contenu.titre, c.contenu.regles, c.contenu.traits, c.dossier].some((x) => String(x ?? '').toLowerCase().includes(q)))
    if (trouvees.length) noeuds.push(el('section', { class: 'trouvees' }, el('h3', { style: 'margin:0 0 6px;font:400 26px var(--affiche);color:#fff' }, 'Cartes trouvées'),
      ...trouvees.slice(0, 40).map((c) => el('button', { class: 'carte-liste', type: 'button', onclick: () => ouvrirDossier(c.dossier, c.id) },
        (() => { const m = el('div', { class: 'mini' }); miniatureDans(m, c); return m })(),
        el('span', { class: 'titre' }, c.contenu.titre || '(sans titre)', el('small', {}, `${NOMS[c.type] ?? c.type} · 📁 ${c.dossier}`)), el('span')))))
    if (!noeuds.length) noeuds.push(el('div', { class: 'aide' }, 'Rien ne correspond.'))
  }
  zone.replaceChildren(...noeuds)
}
function rendreAccueil() {
  if (!$('#grilles')) construireAccueil()
  rendreGrilles()
}

function menuDossier(ancre, d) {
  menuFlottant(ancre, [
    ['Ouvrir', () => ouvrirDossier(d.nom)],
    ['Renommer…', () => dialogueRenommer(d)],
    ['Dupliquer', () => { dupliquerDossier(d.nom); sauvegarderPlusTard(); rendreGrilles(); message('Dossier dupliqué.') }],
    ['Exporter le pack…', () => {
      if (!d.cartes.length) return message('Ce dossier est vide : rien à exporter.')
      ouvrirExportPack({ cartes: () => projet.cartes.filter((c) => !c.brouillon), carte: () => d.cartes[0], rendre: rendreCarte, rendreVerso, serialiser, pochettes: pochettesPourPack })
    }],
    ['Supprimer…', () => dialogueSupprimerDossier(d), true],
  ])
}
function dialogueRenommer(d) {
  const champ = el('input', { type: 'text', value: d.nom })
  const erreur = el('div', { class: 'aide', style: 'color:#ff9b8f' })
  dialogue(`Renommer « ${d.nom} »`, el('div', { class: 'assistant-pile' }, el('label', {}, 'Nouveau nom', champ), erreur),
    [{ texte: 'Annuler' }, { texte: 'Renommer', principal: true, action: () => {
      const e = renommerDossier(d.nom, champ.value)
      if (e) { erreur.textContent = tr(e); return false }
      sauvegarderPlusTard(); rendreGrilles()
    } }])
  champ.select()
}
function dialogueSupprimerDossier(d) {
  const champ = el('input', { type: 'text', placeholder: d.nom, autocomplete: 'off' })
  const b = dialogue(`Supprimer « ${d.nom} »`, el('div', { class: 'assistant-pile' },
    el('p', { class: 'assistant-aide' }, `Le dossier et ses ${d.cartes.length} carte(s) seront effacés. Pour confirmer, tape son nom :`), champ),
  [{ texte: 'Annuler' }, { texte: 'Supprimer', principal: true, action: () => {
    if (champ.value.trim() !== d.nom) { champ.focus(); return false }
    supprimerDossier(d.nom); sauvegarderPlusTard(); rendreGrilles(); message('Dossier supprimé.')
  } }])
  const bouton = [...b.querySelectorAll('button')].find((x) => x.textContent === tr('Supprimer'))
  if (bouton) { bouton.classList.add('danger'); bouton.classList.remove('principal') }
}
/** Le « + » d'une rangee : un dossier vide, ou le wizard qui passe sur tout. */
function dialogueNouveauDossier(genre) {
  const libelles = { heros: 'héros', scenario: 'scénario', modulaire: 'set modulaire' }
  const champ = el('input', { type: 'text', placeholder: genre === 'heros' ? 'ex. Valkyrie' : genre === 'scenario' ? 'ex. Rhino' : 'ex. Bomb Scare' })
  const erreur = el('div', { class: 'aide', style: 'color:#ff9b8f' })
  const nom = () => champ.value.trim()
  dialogue(`Nouveau dossier ${tr(libelles[genre])}`, el('div', { class: 'assistant-pile' },
    el('label', {}, 'Nom du dossier', champ),
    el('div', { class: 'aide' }, 'Avec le wizard, je te guide pour tout créer d’un coup (couleurs, cartes de base…). Un dossier vide se remplit ensuite à la main.'), erreur),
  [{ texte: 'Annuler' },
    { texte: 'Dossier vide', action: () => {
      if (!nom()) { erreur.textContent = tr('Donne un nom au dossier.'); return false }
      if (listeDossiers().some((d) => d.nom === nom())) { erreur.textContent = tr('Un dossier porte déjà ce nom.'); return false }
      creerDossier(nom(), genre); sauvegarderPlusTard(); ouvrirDossier(nom())
    } },
    { texte: 'Avec le wizard', principal: true, action: () => {
      if (nom() && listeDossiers().some((d) => d.nom === nom())) { erreur.textContent = tr('Un dossier porte déjà ce nom.'); return false }
      setTimeout(() => (genre === 'heros' ? ouvrirWizardHeros(nom()) : ouvrirWizardRencontre(genre, nom())), 0)
    } }])
  champ.focus()
}

// ---------------------------------------------------------------- la colonne des cartes (editeur)
const groupesFermes = new Set()
function ligneCarte(c, n, total) {
  const spec = TYPES[c.type]
  const teinte = c.couleurs?.left_color ?? c.couleurs?.background_upper ?? '#6e7179'
  const mini = el('div', { class: 'mini' })
  miniatureDans(mini, c)
  const incomplete = !(c.contenu.titre ?? '').trim() || deborde.has(c.id)
  return el('button', { type: 'button', class: 'carte-liste', style: `--teinte:${teinte}`, 'aria-current': String(c.id === projet.courante), title: spec ? tr(NOMS[c.type] ?? c.type) : c.type, onclick: () => choisir(c.id) },
    mini,
    el('span', { class: 'titre' }, c.contenu.titre || '(sans titre)', el('small', {}, `${NOMS[c.type] ?? c.type} · ${c.langue.toUpperCase()}`)),
    el('span', { class: 'num' }, incomplete ? el('span', { class: 'alerte-c', title: (c.contenu.titre ?? '').trim() ? 'Le texte déborde du cadre.' : 'Le titre est vide.' }, '⚠ ') : null, `${n}/${total}`))
}
const deborde = new Set() // ids des cartes dont le texte deborde (renseigne par dessiner)
function majListe() {
  if (vue !== 'editeur') return
  const l = $('#liste')
  const q = ($('#recherche')?.value ?? '').trim().toLowerCase()
  const toutes = cartesDuDossier(dossierOuvert)
  const total = toutes.length
  const visibles = toutes.filter((c) => !q || [c.contenu.titre, c.contenu.regles, c.contenu.traits, NOMS[c.type]].some((x) => String(x ?? '').toLowerCase().includes(q)))
  const groupes = new Map()
  for (const c of visibles) { if (!groupes.has(c.type)) groupes.set(c.type, []); groupes.get(c.type).push(c) }
  const types = [...groupes.keys()].sort((a, b) => ORDRE_TYPES.indexOf(a) - ORDRE_TYPES.indexOf(b))
  const noeuds = types.map((t) => {
    const d = el('details', { class: 'groupe-type', open: !groupesFermes.has(t) || !!q, 'data-type': t },
      el('summary', {}, `${NOMS[t] ?? t} (${groupes.get(t).length})`),
      el('div', { class: 'liste-cartes' }, ...groupes.get(t).map((c) => ligneCarte(c, toutes.indexOf(c) + 1, total))))
    d.addEventListener('toggle', () => { d.open ? groupesFermes.delete(t) : groupesFermes.add(t) })
    return d
  })
  if (!noeuds.length) noeuds.push(el('div', { class: 'aide' }, q ? 'Aucune carte ne correspond.' : 'Aucune carte.'))
  if (!q) {
    const genre = projet.dossiers?.[dossierOuvert]?.genre ?? genreInfere(dossierOuvert)
    const modeDefaut = genre === 'scenario' ? 'scenario' : genre === 'modulaire' ? 'modulaire' : 'heros'
    const poch = pochettesDuDossier(dossierOuvert)
    const d = el('details', { class: 'groupe-type groupe-pochette', open: !groupesFermes.has('_pochette') },
      el('summary', {}, `Pochette (${poch.length})`),
      el('div', { class: 'liste-cartes' },
        ...poch.map((p) => {
          const m = el('div', { class: 'mini mini-pochette' }); miniaturePochetteDans(m, p)
          return el('button', { type: 'button', class: 'carte-liste', style: '--teinte:#965cc4', onclick: () => ouvrirPochette(p.id) }, m,
            el('span', { class: 'titre' }, nomPochette(p) || '(sans titre)', el('small', {}, libellePochette(p.mode))), el('span'))
        }),
        el('button', { class: 'btn petit', type: 'button', onclick: () => ouvrirWizardPochette(modeDefaut, dossierOuvert) }, '+ Nouvelle pochette')))
    d.addEventListener('toggle', () => { d.open ? groupesFermes.delete('_pochette') : groupesFermes.add('_pochette') })
    noeuds.unshift(d)
  }
  l.replaceChildren(...noeuds)
  l.dataset.total = String(vraiesCartes().length) // toutes les cartes du projet, quel que soit le dossier ouvert (tests)
  l.style.cssText = 'display:flex;flex-direction:column;gap:8px'
  const dl = $('#dossiers-connus')
  if (dl) dl.replaceChildren(...listeDossiers().map((d) => el('option', { value: d.nom })))
}
function choisir(id) {
  validerHistorique()
  projet.courante = id
  const c = carte()
  if (c && vue === 'editeur' && c.dossier !== dossierOuvert) dossierOuvert = c.dossier
  document.body.removeAttribute('data-vide')
  $('#vue-editeur').classList.remove('est-vide')
  const vd = $('#vide-dossier'); if (vd) vd.hidden = true
  { const h = histoDe(id); h.ref ??= cloner(carte()) }
  majListe()
  majBoutonsLangue()
  construireFormulaire()
  dessiner()
  sauvegarderPlusTard()
  majBoutonsHistorique()
  majFil()
}
function ajouter(c) {
  projet.cartes.push(c)
  if (c.dossier) creerDossier(c.dossier, genreInfere(c.dossier))
  choisir(c.id)
}

// ---------------------------------------------------------------- le template d'un dossier (panneau de la colonne de droite)
// Le template garde l'apparence commune a toutes les cartes du dossier : couleurs, style du cadre, mise en page du texte,
// mention du createur. On le modifie ici ; « Enregistrer » demande s'il faut aussi le recopier sur les cartes deja faites.
const defautGabarit = () => ({ preset: '', couleurs: {}, cadre: 'officiel', fissures: true, createur: '', centrerTexte: false, echelleTexte: 0 })
let brouillonTemplate = null
let templateOuvert = false
function specDuDossier(nom) {
  return TYPES[(projet.dossiers?.[nom]?.genre ?? genreInfere(nom)) === 'heros' ? 'identity' : 'villain'] ?? TYPES.ally
}
/** Une « fausse carte » qui porte les couleurs d'un template, pour reutiliser les blocs de couleurs. */
function carteDeTemplate(nom, g) {
  const spec = specDuDossier(nom)
  const c = { id: '_tpl', type: Object.keys(TYPES).find((k) => TYPES[k] === spec), dossier: '', couleurs: { ...(g.couleurs ?? {}) }, preset: g.preset ?? '', couleursPerso: false }
  if (!Object.keys(c.couleurs).length) c.couleurs = couleursNeutres(spec)
  return c
}
function majPanneauTemplate() {
  const zone = $('#panneau-template')
  if (!zone || vue !== 'editeur') return
  const nom = dossierOuvert
  const enregistre = projet.gabarits?.[nom]
  if (brouillonTemplate?.dossier !== nom) brouillonTemplate = { dossier: nom, ...structuredClone(enregistre ?? defautGabarit()) }
  const g = brouillonTemplate
  const spec = specDuDossier(nom)
  const pseudo = carteDeTemplate(nom, g)
  const modifie = () => { g.couleurs = { ...pseudo.couleurs }; g.preset = pseudo.preset }
  const bloc = blocCouleurs(pseudo, spec, { quand: modifie, origineVisible: false, apres: (r) => { modifie(); if (r) majPanneauTemplate() } })
  const cadre = el('select', {}, CADRES.map(([v, n]) => el('option', { value: v }, n)))
  cadre.value = g.cadre
  cadre.addEventListener('change', () => { g.cadre = cadre.value })
  const fissures = el('input', { type: 'checkbox' }); fissures.checked = g.fissures !== false
  fissures.addEventListener('change', () => { g.fissures = fissures.checked })
  const centrer = el('input', { type: 'checkbox' }); centrer.checked = !!g.centrerTexte
  centrer.addEventListener('change', () => { g.centrerTexte = centrer.checked })
  const mention = el('input', { type: 'text', value: g.createur ?? '', placeholder: 'ex. Créé par …' })
  mention.addEventListener('input', () => { g.createur = mention.value })
  const modeles = (projet.modeles ?? [])
  const choixModele = el('select', {}, el('option', { value: '' }, `— cartes de départ (${modeles.length}) —`), ...modeles.map((m) => el('option', { value: m.id }, m.nom)))
  const details = el('details', { class: 'panneau-template', open: templateOuvert },
    el('summary', {}, el('span', { class: 'ico-rub' }, '◧'), 'Template du dossier'),
    el('div', { class: 'contenu' },
      el('div', { class: 'rang', style: 'align-items:center' }, el('span', { class: 'origine' + (enregistre ? '' : ' perso') }, enregistre ? 'Template enregistré ✓' : 'Pas encore de template')),
      el('div', { class: 'aide' }, 'Les couleurs, le cadre et la mention communs à toutes les cartes du dossier.'),
      ...bloc,
      el('label', {}, 'Style du cadre', cadre),
      TYPES_SANS_FISSURES.size ? el('label', { class: 'ligne' }, fissures, 'Fissures dans le cadre (cartes de rencontre)') : null,
      el('label', { class: 'ligne' }, centrer, 'Centrer le texte des règles verticalement'),
      el('label', {}, 'Mention du créateur', mention),
      el('div', { class: 'rang' },
        el('button', { class: 'btn principal petit', type: 'button', onclick: () => enregistrerTemplate() }, 'Enregistrer le template'),
        el('button', { class: 'btn petit', type: 'button', onclick: () => { brouillonTemplate = null; majPanneauTemplate() } }, 'Annuler les changements')),
      el('hr'),
      el('div', { class: 'assistant-libelle' }, 'Cartes de départ'),
      el('div', { class: 'aide' }, 'Une carte entière gardée comme point de départ : on peut en créer d’autres à partir d’elle.'),
      choixModele,
      el('div', { class: 'outils' },
        el('button', { class: 'btn petit', type: 'button', onclick: () => {
          const m = (projet.modeles ?? []).find((x) => x.id === choixModele.value)
          if (!m) return message('Choisis d’abord une carte de départ.')
          const c = { ...cloner(m.carte), id: nouvelId(), dossier: nom }
          appliquerGabaritPack(c)
          ajouter(c)
        } }, 'Utiliser'),
        el('button', { class: 'btn petit', type: 'button', onclick: () => {
          if (!carte()) return message('Choisis d’abord une carte.')
          const n = prompt(tr('Nom de la carte de départ'), carte()?.contenu.titre ?? '')
          if (n === null) return
          enregistrerModele(n); projet.modeles.at(-1).dossier = nom; sauvegarderPlusTard(); majPanneauTemplate(); message('Carte de départ enregistrée.')
        } }, 'Enregistrer la carte actuelle'),
        el('button', { class: 'btn petit', type: 'button', onclick: () => {
          projet.modeles = (projet.modeles ?? []).filter((m) => m.id !== choixModele.value); sauvegarderPlusTard(); majPanneauTemplate()
        } }, 'Supprimer'))))
  details.addEventListener('toggle', () => { templateOuvert = details.open })
  zone.replaceChildren(details)
}
function enregistrerTemplate() {
  const nom = dossierOuvert
  const { dossier, ...g } = brouillonTemplate
  ;(projet.gabarits ??= {})[nom] = structuredClone(g)
  creerDossier(nom, genreInfere(nom))
  const cartes = cartesDuDossier(nom)
  const appliquer = () => {
    for (const x of cartes) appliquerGabaritPack(x)
    historiques.clear()
    const c = carte()
    if (c && c.dossier === nom) { construireFormulaire(); dessiner() }
    majListe(); sauvegarderPlusTard(); message(`${cartes.length} carte(s) mise(s) à jour.`)
  }
  sauvegarderPlusTard()
  majPanneauTemplate()
  if (!cartes.length) return message('Template enregistré.')
  dialogue('Template enregistré',
    el('div', { class: 'assistant-aide' }, `Appliquer ce template aux ${cartes.length} carte(s) du dossier « ${nom} » ? Les couleurs et le cadre personnalisés de ces cartes seront remplacés.`),
    [{ texte: 'Seulement les nouvelles cartes', action: () => message('Template enregistré.') }, { texte: `Les ${cartes.length} cartes`, principal: true, action: appliquer }])
}
/** Applique a `c` le template de son dossier, s'il y en a un (couleurs, cadre, mise en page, mention). */
function appliquerGabaritPack(c) {
  const g = (projet.gabarits ??= {})[(c.dossier || '').trim()]
  c.couleursPerso = false
  if (!g) return
  const spec = TYPES[c.type]
  c.preset = g.preset ?? ''
  if (spec) {
    appliquerPalette(c, spec, c.preset)
    // couleurs reglees a la main dans le template : par-dessus, role par role
    const roles = new Set(rolesDe(spec))
    for (const [r, v] of Object.entries(g.couleurs ?? {})) if (roles.has(r)) c.couleurs[r] = v
  }
  if (g.cadre) c.cadre = g.cadre
  if (g.fissures != null) c.fissures = g.fissures
  if (g.createur) c.contenu.createur = g.createur
  if (g.centrerTexte != null) c.contenu.centrerTexte = g.centrerTexte
  if (g.echelleTexte != null) c.contenu.echelleTexte = g.echelleTexte
}

// ---------------------------------------------------------------- le wizard : moteur d'etapes
// 30/10/2026 : le wizard PASSE SUR TOUT (chaque utilisateur voit au moins une fois toutes les options), une etape par rubrique
// du formulaire, avec les memes champs. L'aide tient en une ligne ; la version longue est derriere la bulle « ? ».
let reconstruireEtape = () => {}
const ORDRE_ETAPES_ALERTE = 'ff9b8f'

/** Fait tourner une suite d'etapes dans une boite de dialogue.
 * `etapes` : un tableau, ou une fonction (valeurs) -> tableau (les etapes dependent alors des choix, le type de carte par exemple).
 * etapes[i] = { titre, court?, aide, plus?, passable?, construire(valeurs, rafraichir) -> noeud, valider?(valeurs) -> string|undefined }.
 * opts.scene : la VRAIE apercu (avec sa souris : glisser l'image, molette) vient s'installer dans la fenetre.
 * opts.apercu(valeurs) -> carte|null : sinon, une carte dessinee a droite et redessinee a chaque saisie.
 * opts.annuler() : appele si on ferme sans terminer. opts.pied(fermer) : un lien de plus sous les boutons. */
function lancerAssistant(titreAssistant, etapes, fin, opts = {}) {
  const d = el('dialog', { class: 'dlg' })
  const corps = el('div', { class: 'assistant-corps' })
  const puces = el('ol', { class: 'assistant-puces' })
  const alerte = el('div', { class: 'aide', style: `color:#${ORDRE_ETAPES_ALERTE}` })
  const gauche = el('div', { class: 'rang' })
  const droite = el('div', { class: 'droite' })
  const toile = el('canvas', { class: 'toile assistant-apercu' })
  let i = 0
  let termine = false
  const valeurs = { ...(opts.valeurs ?? {}) }
  const liste = () => (typeof etapes === 'function' ? etapes(valeurs) : etapes)
  let minuteur = 0
  let n = 0
  async function redessiner() {
    if ((!opts.apercu && !opts.rendreCanvas) || opts.scene) return
    const k = ++n
    const c = opts.rendreCanvas ? true : opts.apercu(valeurs)
    if (!c) return
    try {
      const t = opts.rendreCanvas ? await opts.rendreCanvas(valeurs) : await rendreCarte(c)
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
    const [boutonAide, bulle] = etape.plus ? bulleAide(etape.plus) : [null, null]
    corps.replaceChildren(...[
      el('h3', { class: 'assistant-titre' }, `${i + 1}/${toutes.length} · ${etape.titre}`),
      etape.aide ? el('p', { class: 'assistant-aide' }, etape.aide, boutonAide) : null,
      bulle,
      etape.construire(valeurs, rendre)].filter(Boolean))
    puces.replaceChildren(...toutes.map((e, k) => el('li', { class: k === i ? 'en-cours' : k < i ? 'fait' : '' },
      k < i ? el('button', { type: 'button', onclick: () => { i = k; rendre() } }, e.court ?? e.titre) : el('span', {}, e.court ?? e.titre))))
    gauche.replaceChildren(...[
      i > 0 ? el('button', { class: 'btn', type: 'button', onclick: () => { i--; rendre() } }, '◀ Précédent') : null,
      el('button', { class: 'btn', type: 'button', onclick: () => d.close() }, 'Annuler')].filter(Boolean))
    const dernier = i === toutes.length - 1
    const avancer = () => { if (dernier) { termine = true; fin(valeurs); d.close() } else { i++; rendre() } }
    droite.replaceChildren(...[
      etape.passable && !dernier ? el('button', { class: 'btn', type: 'button', onclick: () => { i++; rendre() } }, 'Passer') : null,
      el('button', {
        class: 'btn principal', type: 'button',
        onclick: () => {
          const erreur = etape.valider?.(valeurs)
          if (typeof erreur === 'string') { alerte.textContent = erreur; return }
          avancer()
        },
      }, dernier ? 'Terminer' : 'Suivant ▶')].filter(Boolean))
    plusTard()
    if (opts.scene) dessiner()
  }
  reconstruireEtape = () => rendre()
  const figure = opts.scene
    ? el('figure', { class: 'assistant-figure' })
    : (opts.apercu || opts.rendreCanvas) ? el('figure', { class: 'assistant-figure' }, toile, el('figcaption', { class: 'aide' }, 'Aperçu')) : null
  const colonne = el('div', { class: 'assistant-colonne' }, corps, alerte,
    el('div', { class: 'rang assistant-boutons' }, gauche, droite),
    opts.pied ? el('div', { class: 'assistant-pied' }, opts.pied(() => { termine = true; d.close() })) : null)
  d.append(el('div', { class: 'panneau assistant' },
    el('h2', {}, titreAssistant), puces,
    el('div', { class: 'assistant-grille' + (figure ? '' : ' sans-apercu') }, colonne, figure)))
  document.body.append(d)
  // la scene (apercu + souris) quitte l'editeur le temps du wizard, et y revient apres
  const scene = $('#scene')
  const placeScene = scene ? { parent: scene.parentNode, suivant: scene.nextSibling } : null
  if (opts.scene && scene) figure.append(scene)
  d.addEventListener('close', () => {
    clearTimeout(minuteur)
    reconstruireEtape = () => {}
    if (opts.scene && scene && placeScene) placeScene.parent.insertBefore(scene, placeScene.suivant)
    d.remove()
    if (!termine) opts.annuler?.()
  })
  rendre()
  d.showModal()
  return d
}

/** Un champ du wizard : libelle, valeur gardee dans `v[cle]`, bulle « ? » pour l'explication. */
function champAssistant(v, cle, label, aide, opts = {}) {
  v[cle] ??= opts.defaut ?? ''
  const i = opts.long ? el('textarea', { rows: opts.lignes ?? 4, placeholder: opts.exemple ?? '' }) : el('input', { type: 'text', placeholder: opts.exemple ?? '', list: opts.list ?? null })
  i.value = v[cle]
  i.addEventListener('input', () => { v[cle] = i.value })
  const [b, bulle] = aide ? bulleAide(aide) : [null, null]
  return el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, label, b), bulle, i)
}
function caseAssistant(v, cle, label, aide, defaut = false) {
  v[cle] ??= defaut
  const i = el('input', { type: 'checkbox' })
  i.checked = !!v[cle]
  i.addEventListener('change', () => { v[cle] = i.checked })
  const [b, bulle] = aide ? bulleAide(aide) : [null, null]
  return el('div', { class: 'assistant-champ' }, el('label', { class: 'ligne' }, i, el('span', { class: 'assistant-libelle' }, label, b)), bulle)
}
function compteurAssistant(v, cle, label, max = 12, defaut = 0) {
  v[cle] ??= defaut
  const s = el('select', {}, Array.from({ length: max + 1 }, (_, k) => el('option', { value: k }, k)))
  s.value = String(v[cle])
  s.addEventListener('change', () => { v[cle] = Number(s.value) })
  return el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, label), s)
}

/** Le choix du dossier dans le wizard : les dossiers existants en tuiles, ou un nom nouveau. */
function choixDossier(v, rafraichir, { quand = null } = {}) {
  const tuiles = el('div', { class: 'assistant-tuiles' })
  const existants = listeDossiers()
  const choisirNom = (nom) => { v.dossier = nom; quand?.(nom) }
  for (const d of existants) {
    const g = projet.gabarits?.[d.nom]
    const coul = g?.couleurs?.left_color ?? g?.couleurs?.background_upper ?? couleurDuPreset(g?.preset) ?? '#3f86e0'
    tuiles.append(el('button', {
      type: 'button', class: 'tuile-dossier' + (v.dossier === d.nom ? ' choisie' : ''), style: `--teinte:${coul}`,
      onclick: () => { choisirNom(d.nom); rafraichir() },
    }, el('span', { class: 'tuile-nom' }, '📁 ' + d.nom), el('small', {}, `${d.cartes.length} carte(s)` + (g ? ' · template ✓' : ''))))
  }
  const nouveau = el('input', { type: 'text', placeholder: 'ex. Valkyrie', value: existants.some((d) => d.nom === v.dossier) ? '' : (v.dossier ?? '') })
  nouveau.addEventListener('input', () => { choisirNom(nouveau.value.trim()); for (const b of tuiles.children) b.classList.remove('choisie') })
  return el('div', { class: 'assistant-pile' },
    existants.length ? el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Un dossier existant'), tuiles) : null,
    el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, existants.length ? 'Ou un nouveau dossier' : 'Nom du dossier'), nouveau))
}

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
/** Change le type d'une carte : couleurs du template du dossier (ou neutres), valeurs propres au type. */
function changerType(c, type) {
  c.type = type
  c.preset = ''
  appliquerPalette(c, TYPES[type], '')
  const d = valeursParDefaut(type, c.langue)
  for (const k of ['phaseLettre']) c.contenu[k] = d[k]
  appliquerGabaritPack(c)
}

// ---------------------------------------------------------------- wizard « Nouvelle carte »
// La carte se construit pour de bon (en brouillon, invisible des listes et jamais enregistree) : les etapes reutilisent donc
// exactement les memes champs que le formulaire, et l'apercu est la vraie scene (on y glisse l'image, molette pour zoomer).
function ouvrirWizardCarte(dossierDepart = null) {
  const avant = projet.courante
  const langue = carte()?.langue ?? 'en'
  const dossier0 = dossierDepart ?? (vue === 'editeur' && dossierOuvert ? dossierOuvert : DIVERS)
  const c = nouvelleCarte('ally', langue)
  c.brouillon = true
  c.dossier = dossier0
  appliquerGabaritPack(c)
  projet.cartes.push(c)
  projet.courante = c.id
  construireFormulaire()
  const pile = (...n) => el('div', { class: 'assistant-pile' }, ...n.flat().filter(Boolean))
  const etapes = () => {
    const spec = TYPES[c.type]
    const e = []
    e.push({
      titre: 'Quel type de carte ?', court: 'Type',
      aide: 'Le type fixe le cadre et les cases de la carte.',
      plus: 'Le type fixe le cadre et les cases de la carte (coût, stats, menace…). Les étapes suivantes ne te demanderont que ce qui existe sur ce type. Tu pourras encore le changer plus tard dans l’éditeur.',
      construire: (v, rafraichir) => {
        const zone = el('div', { style: 'display:flex;flex-direction:column;gap:10px' })
        for (const [titreGroupe, ids] of GROUPES) {
          const boutons = el('div', { class: 'assistant-types' },
            ...ids.filter((id) => TYPES[id]).map((id) => el('button', {
              class: 'btn petit' + (c.type === id ? ' principal' : ''), type: 'button',
              onclick: () => { changerType(c, id); changement(); rafraichir() },
            }, el('b', {}, NOMS[id] ?? id), el('span', {}, DESCRIPTIONS_TYPES[id] ?? ''))))
          zone.append(el('h4', { class: 'assistant-groupe' }, titreGroupe), boutons)
        }
        return zone
      },
    })
    e.push({
      titre: 'Dans quel dossier ?', court: 'Dossier', passable: true,
      aide: 'Une carte est toujours rangée dans un dossier.',
      plus: 'Un dossier regroupe les cartes d’un même héros (ou d’un même scénario ou set modulaire). S’il a un template, la carte en prend tout de suite les couleurs, le style du cadre et la mention du créateur.',
      construire: (v, rafraichir) => { v.dossier ??= c.dossier; return choixDossier(v, rafraichir, { quand: (nom) => { c.dossier = nom || DIVERS; appliquerGabaritPack(c); changement() } }) },
      valider: () => ((c.dossier || '').trim() ? undefined : 'Choisis ou nomme un dossier.'),
    })
    e.push({
      titre: 'Nom et traits', court: 'Nom',
      aide: 'Ce qui identifie la carte : son nom, ses traits.',
      plus: 'Le nom est écrit tel quel en haut de la carte. « Carte unique » ajoute le symbole ✦ (un seul exemplaire en jeu à la fois). Les traits sont les mots-clés en italique sous l’illustration, séparés par des points ; d’autres cartes s’y réfèrent (« chaque allié Avenger… »).',
      construire: () => pile(blocTitre(spec)),
      valider: () => ((c.contenu.titre ?? '').trim() ? undefined : 'Donne un nom à la carte.'),
    })
    const N = blocNombres(spec)
    const L = blocLigne(c, spec).filter((n) => !n.querySelector?.('[data-champ=titre]'))
    if (N.length || L.length) {
      e.push({
        titre: 'Les nombres', court: 'Nombres', passable: true,
        aide: 'Coût, stats, points de vie : laisse vide ce que tu ne veux pas afficher.',
        plus: '« X » ou « — » sont acceptés. La case ★ ajoute une étoile au nombre ; « par joueur » multiplie la valeur par le nombre de joueurs. Chaque champ a sa propre bulle « ? ».',
        construire: () => pile(N.map((n) => avecAide(n.noeud, n.aide)), L),
      })
    }
    const R = blocBoost(c, spec)
    if (R.length) {
      e.push({
        titre: 'Boost et ressources', court: 'Boost', passable: true,
        aide: 'Les icônes de boost et les ressources produites par la carte.',
        plus: 'Les icônes de boost sont celles qu’on retourne pendant l’attaque d’un ennemi ; les ressources (énergie, mental, physique, joker) sont celles que la carte produit quand on la défausse pour payer.',
        construire: () => pile(R),
      })
    }
    if (aElement(spec, 'rules') || aElement(spec, 'quote')) {
      e.push({
        titre: 'Le texte', court: 'Texte', passable: true,
        aide: 'Les règles et la citation, avec la mise en forme complète.',
        plus: 'Sélectionne un passage pour le mettre en gras, en italique ou en couleur. « Styles » donne les mots-clés officiels (Action, Renfort…) ; taper « / » dans le texte ouvre le même menu. Les boutons d’icônes insèrent les ressources et symboles du jeu.',
        construire: () => pile(blocRegles(c, spec)),
      })
    }
    e.push({
      titre: 'L’illustration', court: 'Image', passable: true,
      aide: 'L’image derrière le cadre : choisis-la, puis place-la sur l’aperçu.',
      plus: 'Prends une image d’au moins 750 × 1050 pixels pour qu’elle reste nette à l’impression. Glisse sur l’aperçu pour la déplacer, molette pour zoomer ; « Détourer / recadrer » enlève un fond. Le premier plan est une image posée devant le cadre.',
      construire: () => { ciblePointeur = 'art'; majAide(); return pile(boiteImage('Image derrière la carte', (x) => x.art, 'art'), el('details', {}, el('summary', {}, 'Premier plan (devant le cadre)'), el('div', { class: 'contenu' }, boiteImage('Premier plan', (x) => x.artDevant, 'artDevant')))) },
    })
    if (rolesDe(spec).length) {
      e.push({
        titre: 'Les couleurs', court: 'Couleurs', passable: true,
        aide: 'Les couleurs du cadre : une pastille, ou un picker par couleur.',
        plus: 'Les pastilles de raccourci colorent tout le cadre d’un coup (aspects du jeu). Les pickers règlent chaque couleur : pastille cliquable, code hexadécimal et pipette pour prendre une couleur à l’écran. « Plus de couleurs » donne les réglages fins. Sans choix, la carte prend les couleurs du template du dossier.',
        construire: () => pile(blocCouleurs(c, spec, { apres: (r) => r && reconstruireEtape() })),
      })
    }
    e.push({
      titre: 'Le style du cadre', court: 'Cadre', passable: true,
      aide: 'Officiel, sombre ou pleine illustration : clique sur ta carte.',
      plus: '« Officiel » est le cadre du jeu, dans tes couleurs. « Sombre » le remplace par un gris-bleu foncé à accents dorés. « Pleine illustration » enlève le cadre : l’image remplit la carte et le texte repose sur des panneaux translucides.',
      construire: (v, rafraichir) => {
        const rangee = el('div', { class: 'vignettes-cadre' })
        for (const [id, nom] of CADRES) {
          const t = el('canvas')
          rendreCarte({ ...cloner(c), cadre: id }).then((r) => { t.width = r.width; t.height = r.height; t.getContext('2d').drawImage(r, 0, 0) }).catch(() => {})
          rangee.append(el('button', { type: 'button', class: 'vignette-cadre' + ((c.cadre ?? 'officiel') === id ? ' choisie' : ''), onclick: () => { c.cadre = id; changement(); rafraichir() } }, t, el('span', {}, nom)))
        }
        return pile(rangee, TYPES_SANS_FISSURES.has(c.type) ? coche('Fissures dans le cadre', (x) => x, 'fissures') : null)
      },
    })
    e.push({
      titre: 'Les calques PNG', court: 'Calques', passable: true,
      aide: 'Des images libres posées par-dessus la carte.',
      plus: 'Un calque est une image PNG (logo, effet, icône) que tu poses sur la carte, déplaces à la souris, redimensionnes, tournes ou masques. Tu peux aussi glisser des images directement sur l’aperçu. Les calques se gèrent ensuite dans la rubrique « Calques PNG » du formulaire.',
      construire: (v, rafraichir) => {
        const f = el('input', { type: 'file', accept: 'image/*', multiple: true, hidden: true })
        f.addEventListener('change', async () => { if (f.files.length) { await ajouterFichiers([...f.files]); rafraichir() } })
        return pile(el('div', { class: 'rang', style: 'align-items:center' }, el('button', { class: 'btn', type: 'button', onclick: () => f.click() }, 'Ajouter une image'), f,
          el('span', { class: 'aide' }, `${c.libres?.length ?? 0} calque(s) sur la carte`)))
      },
    })
    e.push({
      titre: 'Le dos de la carte', court: 'Dos', passable: true,
      aide: 'Choisi automatiquement selon le type ; change-le si besoin.',
      plus: 'Une carte joueur a le dos des cartes joueur, une carte de rencontre le dos des cartes rencontre. Tu peux aussi choisir une autre carte comme autre face (identité et alter-ego) ou ta propre image, nette à l’impression.',
      construire: () => { dosAutomatique(c); changement(); return pile(blocDos(c)) },
    })
    e.push({
      titre: 'C’est prêt', court: 'Fin',
      aide: 'La carte s’ouvre dans l’éditeur, rubriques repliées, pour les finitions.',
      construire: () => el('ul', { style: 'margin:0;padding-left:18px' },
        el('li', {}, `Type : ${tr(NOMS[c.type] ?? c.type)}`), el('li', {}, `Titre : ${(c.contenu.titre ?? '').trim()}`), el('li', {}, `Dossier : ${c.dossier}`)),
    })
    return e
  }
  const retirer = () => { projet.cartes = projet.cartes.filter((x) => x !== c) }
  lancerAssistant('Nouvelle carte', etapes, () => {
    dosAutomatique(c)
    delete c.brouillon
    creerDossier(c.dossier, genreInfere(c.dossier))
    ouvrirDossier(c.dossier, c.id)
    sauvegarderPlusTard()
  }, {
    scene: true,
    annuler: () => {
      retirer()
      projet.courante = projet.cartes.some((x) => x.id === avant) ? avant : null
      if (vue === 'editeur') ouvrirDossier(dossierOuvert, projet.courante && carte()?.dossier === dossierOuvert ? projet.courante : null)
    },
    pied: (fermer) => el('button', { class: 'lien', type: 'button', onclick: () => { c.contenu.titre ||= ''; delete c.brouillon; creerDossier(c.dossier, genreInfere(c.dossier)); const id = c.id; fermer(); ouvrirDossier(c.dossier, id); sauvegarderPlusTard() } }, 'Créer une carte vide, sans wizard'),
  })
}

// ---------------------------------------------------------------- wizards de dossier : fabrique de cartes
/** Des cartes toutes neuves pour un dossier, avec son template. specs = [{ type, titre?, apres?(c) }]. */
function fabriquerCartes(dossier, langue, specs) {
  const cartes = []
  for (const s of specs) {
    const c = nouvelleCarte(s.type, langue)
    c.dossier = dossier
    appliquerGabaritPack(c)
    if (s.titre) c.contenu.titre = s.titre
    s.apres?.(c)
    dosAutomatique(c)
    cartes.push(c)
  }
  return cartes
}
const GABARIT_ETAPE = (v) => ({ preset: v.pseudo.preset ?? '', couleurs: { ...v.pseudo.couleurs }, cadre: v.cadre ?? 'officiel', fissures: true, createur: v.createur ?? '', centrerTexte: !!v.centrer, echelleTexte: 0 })
/** Les etapes « template » communes aux wizards de dossier : couleurs, cadre et mise en page, mention. */
function etapesTemplate(specDuTemplate, langue) {
  return [
    {
      titre: 'Les couleurs du template', court: 'Couleurs', passable: true,
      aide: 'Les couleurs communes à toutes les cartes du dossier.',
      plus: 'Une pastille colore tout le cadre d’un coup ; les pickers règlent chaque couleur (pastille cliquable, code hexadécimal, pipette). « Plus de couleurs » donne les réglages fins. Tu pourras tout retoucher plus tard dans le panneau « Template du dossier ».',
      construire: (v, rafraichir) => {
        v.pseudo ??= { id: '_tpl', type: Object.keys(TYPES).find((k) => TYPES[k] === specDuTemplate), dossier: '', couleurs: couleursNeutres(specDuTemplate), preset: '', couleursPerso: false }
        return el('div', { class: 'assistant-pile' }, ...blocCouleurs(v.pseudo, specDuTemplate, { origineVisible: false, quand: () => {}, apres: (r) => r && rafraichir() }))
      },
    },
    {
      titre: 'Le cadre et la mise en page', court: 'Cadre', passable: true,
      aide: 'Style du cadre et centrage du texte, pour tout le dossier.',
      plus: '« Officiel » : le cadre du jeu. « Sombre » : gris-bleu foncé à accents dorés. « Pleine illustration » : pas de cadre. Centrer le texte verticalement convient aux cartes à texte court, comme beaucoup de cartes officielles.',
      construire: (v) => {
        v.cadre ??= 'officiel'
        const s = el('select', {}, CADRES.map(([k, n]) => el('option', { value: k }, n)))
        s.value = v.cadre
        s.addEventListener('change', () => { v.cadre = s.value })
        return el('div', { class: 'assistant-pile' }, el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Style du cadre'), s), caseAssistant(v, 'centrer', 'Centrer le texte des règles verticalement', ''))
      },
    },
    {
      titre: 'La mention du créateur', court: 'Mention', passable: true,
      aide: 'La petite ligne en bas de chaque carte : ton nom ou ton pseudo.',
      construire: (v) => champAssistant(v, 'createur', 'Mention', '', { defaut: TEXTES[langue].createur }),
    },
  ]
}
/** Un template provisoire (valeurs du wizard) sur une carte, pour l'apercu. */
function apercuTemplate(v, type, langue, titre) {
  const c = nouvelleCarte(type, langue)
  if (v.pseudo) { c.couleurs = { ...v.pseudo.couleurs }; c.preset = v.pseudo.preset }
  if (v.cadre) c.cadre = v.cadre
  if (v.createur !== undefined) c.contenu.createur = v.createur
  c.contenu.centrerTexte = !!v.centrer
  c.contenu.titre = titre ?? ''
  return c
}
function finDossier(nom, genre, v, cartes) {
  creerDossier(nom, genre)
  ;(projet.gabarits ??= {})[nom] = GABARIT_ETAPE(v.pseudo ? v : { ...v, pseudo: { preset: '', couleurs: {} } })
  const faites = cartes()
  projet.cartes.push(...faites)
  sauvegarderPlusTard()
  message(`Dossier « ${nom} » créé : ${faites.length} carte(s).`)
  ouvrirDossier(nom, (faites.find((c) => c.type === 'identity' || c.type === 'villain') ?? faites[0])?.id ?? null)
}

// ---------------------------------------------------------------- wizard « Nouveau héros »
const CARTES_HEROS = [
  ['nemesis', 'minion', 'Sa némésis (un sbire)', 'L’ennemi juré du héros : elle entre en jeu avec la manigance annexe de la némésis.'],
  ['manigance', 'sidescheme', 'La manigance annexe de la némésis', 'Révélée quand la némésis arrive.'],
  ['obligation', 'obligation', 'Son obligation', 'Le problème personnel de l’alter-ego, mêlé au paquet de rencontre.'],
]
const PAQUET_HEROS = ['ally', 'ally', 'ally', 'event', 'event', 'event', 'event', 'event', 'upgrade', 'upgrade', 'upgrade', 'support', 'support', 'resource', 'resource']
const TYPES_PAQUET = ['ally', 'event', 'upgrade', 'support', 'resource']
function ouvrirWizardHeros(nomDepart = '') {
  const langue = carte()?.langue ?? 'en'
  const cartesHeros = (v) => {
    const nom = (v.nom ?? '').trim()
    const specs = [{ type: 'identity', titre: nom }, { type: 'alter-ego', titre: (v.alterEgo ?? '').trim() }]
    for (const [cle, type] of CARTES_HEROS) if (v[cle]) specs.push({ type })
    ;(v.paquet ?? PAQUET_HEROS).forEach((type) => { if (type) specs.push({ type }) })
    return specs
  }
  const fabriquer = (v) => {
    const nom = (v.nom ?? '').trim()
    const g = GABARIT_ETAPE(v.pseudo ? v : { ...v, pseudo: { preset: '', couleurs: {} } })
    const sauve = projet.gabarits?.[nom]
    ;(projet.gabarits ??= {})[nom] = g
    const cartes = fabriquerCartes(nom, langue, cartesHeros(v))
    if (sauve) projet.gabarits[nom] = sauve; else delete projet.gabarits[nom]
    const [id, ae] = cartes
    id.verso = { mode: 'carte', carteId: ae.id, blob: null, choisi: true }
    ae.verso = { mode: 'carte', carteId: id.id, blob: null, choisi: true }
    return cartes
  }
  const etapes = [
    {
      titre: 'Un héros, c’est un dossier', court: 'Noms',
      aide: 'Le nom du héros et celui de son alter-ego.',
      plus: 'Je vais créer un dossier au nom du héros, son template (les couleurs et la mention communes à toutes ses cartes), puis ses cartes de base et les 15 cartes de son paquet, prêtes à remplir. Les deux noms s’affichent sur la tuile du dossier.',
      construire: (v) => el('div', { class: 'assistant-pile' },
        champAssistant(v, 'nom', 'Nom du héros', 'Le nom de super-héros : il sert aussi de nom au dossier et de titre à la carte d’identité.', { exemple: 'ex. Valkyrie', defaut: nomDepart }),
        champAssistant(v, 'alterEgo', 'Nom de l’alter-ego', 'Son identité civile, écrite sur l’autre face de la carte.', { exemple: 'ex. Brunnhilde' })),
      valider: (v) => {
        const nom = (v.nom ?? '').trim()
        if (!nom) return 'Donne un nom au héros.'
        if (listeDossiers().some((d) => d.nom === nom)) return 'Un dossier porte déjà ce nom : choisis-en un autre.'
      },
    },
    ...etapesTemplate(TYPES.identity, langue),
    {
      titre: 'Les cartes de base', court: 'Base', passable: true,
      aide: 'L’identité et l’alter-ego sont toujours créés ; coche le reste.',
      plus: 'L’identité et l’alter-ego sont les deux faces de la carte du héros : je les relie l’une à l’autre comme recto et verso. La némésis, sa manigance annexe et l’obligation sont des cartes de rencontre propres au héros.',
      construire: (v) => el('div', { class: 'assistant-pile' },
        el('label', { class: 'ligne' }, el('input', { type: 'checkbox', checked: true, disabled: true }), el('span', { class: 'assistant-libelle' }, 'Identité de héros + alter-ego')),
        ...CARTES_HEROS.map(([cle, , label, aide]) => caseAssistant(v, cle, label, aide, true))),
    },
    {
      titre: 'Les 15 cartes du paquet', court: '15 cartes', passable: true,
      aide: 'Un type par emplacement ; elles sont créées vides.',
      plus: 'Le paquet de départ d’un héros compte 15 cartes qui lui sont propres. Choisis le type de chacune (allié, événement, amélioration, soutien, ressource) ou « Aucune » pour ne pas la créer. Tu les rempliras une à une dans l’éditeur.',
      construire: (v) => {
        v.paquet ??= [...PAQUET_HEROS]
        const grille = el('div', { class: 'quinze' })
        v.paquet.forEach((type, k) => {
          const s = el('select', {}, el('option', { value: '' }, 'Aucune'), ...TYPES_PAQUET.map((t) => el('option', { value: t }, NOMS[t])))
          s.value = type
          s.addEventListener('change', () => { v.paquet[k] = s.value })
          grille.append(el('label', {}, el('span', {}, String(k + 1)), s))
        })
        return grille
      },
    },
    {
      titre: 'C’est prêt', court: 'Fin',
      aide: 'Le dossier s’ouvre, avec la carte d’identité choisie.',
      construire: (v) => {
        const cartes = cartesHeros(v)
        const nb = (t) => cartes.filter((c) => c.type === t).length
        return el('ul', { style: 'margin:0;padding-left:18px' },
          el('li', {}, `Dossier : ${(v.nom ?? '').trim()}`), el('li', {}, `${cartes.length} carte(s) : identité, alter-ego${CARTES_HEROS.some(([k]) => v[k]) ? ', cartes de base' : ''}, ${cartes.length - 2 - CARTES_HEROS.filter(([k]) => v[k]).length} cartes du paquet`),
          ...TYPES_PAQUET.filter((t) => nb(t)).map((t) => el('li', {}, `${NOMS[t]} : ${nb(t)}`)))
      },
    },
  ]
  lancerAssistant('Nouveau héros', etapes, (v) => finDossier(v.nom.trim(), 'heros', v, () => fabriquer(v)),
    { valeurs: { nom: nomDepart }, apercu: (v) => apercuTemplate(v, 'identity', langue, (v.nom ?? '').trim()) })
}

// ---------------------------------------------------------------- wizard « Nouveau scenario / modulaire »
const CARTES_RENCONTRE = [['minion', 'Sbires'], ['treachery', 'Trahisons'], ['sidescheme', 'Manigances annexes'], ['attachment', 'Attachements'], ['environment', 'Environnements']]
function ouvrirWizardRencontre(genre, nomDepart = '') {
  const langue = carte()?.langue ?? 'en'
  const scenario = genre === 'scenario'
  const specsDe = (v) => {
    const specs = []
    if (scenario) {
      const nbEtapes = Number(v.etapes ?? 3)
      const romains = ['I', 'II', 'III']
      for (let k = 0; k < nbEtapes; k++) specs.push({ type: 'villain', titre: (v.mechant ?? '').trim(), apres: (c) => { c.contenu.etape = romains[k] } })
      const nbManigances = Number(v.manigances ?? 1)
      for (let k = 1; k <= nbManigances; k++) {
        specs.push({ type: 'main_scheme_a', apres: (c) => { c.contenu.phaseNumero = String(k); c.contenu.phaseLettre = 'A' } })
        specs.push({ type: 'main_scheme_b', apres: (c) => { c.contenu.phaseNumero = String(k); c.contenu.phaseLettre = 'B' } })
      }
    }
    for (const [type] of CARTES_RENCONTRE) for (let k = 0; k < Number(v['n:' + type] ?? 0); k++) specs.push({ type })
    for (let k = 0; k < Number(v.obligations ?? 0); k++) specs.push({ type: 'obligation-villain' })
    return specs
  }
  const fabriquer = (v) => {
    const nom = (v.nom ?? '').trim()
    const sauve = projet.gabarits?.[nom]
    ;(projet.gabarits ??= {})[nom] = GABARIT_ETAPE(v.pseudo ? v : { ...v, pseudo: { preset: '', couleurs: {} } })
    const cartes = fabriquerCartes(nom, langue, specsDe(v))
    if (sauve) projet.gabarits[nom] = sauve; else delete projet.gabarits[nom]
    return cartes
  }
  const etapes = [
    {
      titre: scenario ? 'Un scénario, c’est un dossier' : 'Un set modulaire, c’est un dossier', court: 'Noms',
      aide: scenario ? 'Le nom du scénario et celui du méchant.' : 'Le nom du set modulaire.',
      plus: scenario
        ? 'Je vais créer un dossier au nom du scénario, son template (couleurs et mention communes), puis les cartes du méchant, ses manigances principales, ses cartes de rencontre et ses obligations.'
        : 'Je vais créer un dossier au nom du set, son template (couleurs et mention communes), puis ses cartes de rencontre. Un modulaire n’a ni méchant ni manigance principale.',
      construire: (v) => el('div', { class: 'assistant-pile' },
        champAssistant(v, 'nom', scenario ? 'Nom du scénario' : 'Nom du set modulaire', 'Il sert aussi de nom au dossier.', { exemple: scenario ? 'ex. Rhino' : 'ex. Bomb Scare', defaut: nomDepart }),
        scenario ? champAssistant(v, 'mechant', 'Nom du méchant', 'Écrit sur chacune de ses cartes (une par étape).', { exemple: 'ex. Rhino' }) : null),
      valider: (v) => {
        const nom = (v.nom ?? '').trim()
        if (!nom) return 'Donne un nom au dossier.'
        if (listeDossiers().some((d) => d.nom === nom)) return 'Un dossier porte déjà ce nom : choisis-en un autre.'
      },
    },
    ...etapesTemplate(TYPES.villain, langue),
    ...(scenario ? [
      {
        titre: 'Le méchant', court: 'Méchant', passable: true,
        aide: 'Combien d’étapes a le méchant ?',
        plus: 'Un méchant a généralement trois étapes (I, II, III) : une carte de stats par étape, qu’on retourne quand ses points de vie tombent à zéro. Je crée une carte par étape, au nom du méchant.',
        construire: (v) => { v.etapes ??= 3; return compteurAssistant(v, 'etapes', 'Nombre d’étapes', 3, 3) },
      },
      {
        titre: 'Les manigances principales', court: 'Manigances', passable: true,
        aide: 'Combien de manigances principales (faces A et B) ?',
        plus: 'Chaque manigance principale a deux faces : A (menace de départ) et B (après son avancée). Je crée les deux cartes de chaque manigance, avec leur numéro de phase.',
        construire: (v) => { v.manigances ??= 1; return compteurAssistant(v, 'manigances', 'Nombre de manigances principales', 3, 1) },
      },
    ] : []),
    {
      titre: 'Les cartes de rencontre', court: 'Rencontre', passable: true,
      aide: 'Combien de cartes de chaque sorte ? Elles sont créées vides.',
      plus: 'Sbires, trahisons, manigances annexes, attachements et environnements : indique combien de cartes de chaque sorte tu veux. Elles sont créées vides, aux couleurs du template.',
      construire: (v) => el('div', { class: 'compteurs' }, ...CARTES_RENCONTRE.map(([type, label]) => compteurAssistant(v, 'n:' + type, label, 20, 0))),
    },
    ...(scenario ? [{
      titre: 'Les obligations du méchant', court: 'Obligations', passable: true,
      aide: 'Combien de cartes obligation pour le paquet du méchant ?',
      plus: 'Une obligation est une carte de rencontre mêlée au paquet du méchant. Il en existe en général une par héros possible.',
      construire: (v) => compteurAssistant(v, 'obligations', 'Nombre d’obligations', 8, 0),
    }] : []),
    {
      titre: 'C’est prêt', court: 'Fin',
      aide: 'Le dossier s’ouvre, prêt à remplir.',
      construire: (v) => {
        const specs = specsDe(v)
        const compte = new Map()
        for (const s of specs) compte.set(s.type, (compte.get(s.type) ?? 0) + 1)
        return el('ul', { style: 'margin:0;padding-left:18px' }, el('li', {}, `Dossier : ${(v.nom ?? '').trim()}`), el('li', {}, `${specs.length} carte(s)`),
          ...[...compte].map(([t, k]) => el('li', {}, `${NOMS[t] ?? t} : ${k}`)))
      },
    },
  ]
  lancerAssistant(scenario ? 'Nouveau scénario' : 'Nouveau set modulaire', etapes, (v) => finDossier(v.nom.trim(), genre, v, () => fabriquer(v)),
    { valeurs: { nom: nomDepart }, apercu: (v) => apercuTemplate(v, scenario ? 'villain' : 'minion', langue, scenario ? (v.mechant ?? '').trim() : (v.nom ?? '').trim()) })
}

// ---------------------------------------------------------------- colonnes redimensionnables, menu d'export
function brancherPoignees() {
  const page = $('#vue-editeur')
  try {
    const m = JSON.parse(localStorage.getItem('createur-largeurs') ?? '{}')
    if (m.form) page.style.setProperty('--w-form', m.form + 'px')
    if (m.cartes) page.style.setProperty('--w-cartes', m.cartes + 'px')
  } catch {}
  const lier = (idPoignee, idColonne, variable, cle) => {
    const p = $(idPoignee)
    p.addEventListener('pointerdown', (e) => {
      e.preventDefault()
      const depart = e.clientX
      const l0 = $(idColonne).getBoundingClientRect().width
      p.setPointerCapture(e.pointerId)
      p.classList.add('actif')
      const bouge = (ev) => {
        const w = Math.max(300, Math.min(Math.round(innerWidth * 0.6), Math.round(l0 - (ev.clientX - depart))))
        page.style.setProperty(variable, w + 'px')
      }
      const fini = () => {
        p.classList.remove('actif')
        p.removeEventListener('pointermove', bouge)
        p.removeEventListener('pointerup', fini)
        try {
          const m = JSON.parse(localStorage.getItem('createur-largeurs') ?? '{}')
          m[cle] = Math.round($(idColonne).getBoundingClientRect().width)
          localStorage.setItem('createur-largeurs', JSON.stringify(m))
        } catch {}
        dessiner()
      }
      p.addEventListener('pointermove', bouge)
      p.addEventListener('pointerup', fini)
    })
    p.addEventListener('dblclick', () => {
      page.style.removeProperty(variable)
      try { const m = JSON.parse(localStorage.getItem('createur-largeurs') ?? '{}'); delete m[cle]; localStorage.setItem('createur-largeurs', JSON.stringify(m)) } catch {}
    })
  }
  lier('#poignee-1', '#formulaire', '--w-form', 'form')
  lier('#poignee-2', '#colonne-cartes', '--w-cartes', 'cartes')
}
function brancherMenuExport() {
  const b = $('#b-exporter')
  const m = $('#menu-export')
  b.addEventListener('click', (e) => { e.stopPropagation(); m.hidden = !m.hidden; b.setAttribute('aria-expanded', String(!m.hidden)) })
  m.addEventListener('click', () => { m.hidden = true; b.setAttribute('aria-expanded', 'false') })
  document.addEventListener('click', (e) => { if (!e.target.closest('.menu-flottant, .menu-exporter')) fermerMenus() })
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') fermerMenus() })
}

// ---------------------------------------------------------------- les pochettes (couvertures de pack)
// 30/10/2026 : « Images de pack » est integre a MC Creator (moteur dans pochettes.js). Une pochette est rattachee a un dossier OU
// independante (rangee « Pochettes » en bas de l'accueil). Elle s'enregistre avec le projet (navigateur + « Tout enregistrer »)
// et part dans le pack .zip du dossier. Pas d'envoi au serveur pour l'instant.
let pochetteOuverte = null // l'id de la pochette ouverte dans l'editeur de pochette
const vraiesPochettes = () => (projet.pochettes ??= [])
const pochetteParId = (id) => vraiesPochettes().find((p) => p.id === id)
const pochettesDuDossier = (nom) => vraiesPochettes().filter((p) => (p.dossier || '') === nom)
const libellePochette = (mode) => tr(MODES.find(([m]) => m === mode)?.[1] ?? 'Pochette')
const nomPochette = (p) => p.nom || p.titre?.texte?.split('\n')[0] || ''

// -- miniatures
const miniaturesPochettes = new Map()
let minPochettesEnCours = false
const filePochettes = []
const clePochette = (p) => JSON.stringify([p.mode, p.titre, p.art?.x, p.art?.y, p.art?.zoom, p.art?.blob?.size, p.titre?.blob?.size, p.couleurBoite, p.couleurEtiquette, p.textes])
function miniaturePochetteDans(noeud, p) {
  const cle = clePochette(p)
  const prete = miniaturesPochettes.get(cle) ?? miniaturesPochettes.get('id:' + p.id)
  if (prete) noeud.style.backgroundImage = `url(${prete})`
  if (miniaturesPochettes.has(cle)) return
  filePochettes.push({ noeud, p: { ...p, titre: { ...p.titre }, art: { ...p.art }, textes: p.textes.map((t) => ({ ...t })) }, cle })
  setTimeout(pomperPochettes, 250)
}
async function pomperPochettes() {
  if (minPochettesEnCours) return
  minPochettesEnCours = true
  while (filePochettes.length) {
    const j = filePochettes.shift()
    if (miniaturesPochettes.has(j.cle)) { j.noeud.style.backgroundImage = `url(${miniaturesPochettes.get(j.cle)})`; continue }
    if (!j.noeud.isConnected) continue
    try {
      const t = await rendrePochette(j.p, { apercu: false })
      const m = document.createElement('canvas')
      m.width = 160; m.height = Math.round(t.height * (160 / t.width))
      m.getContext('2d').drawImage(t, 0, 0, m.width, m.height)
      const url = m.toDataURL('image/jpeg', 0.72)
      if (miniaturesPochettes.size > 200) miniaturesPochettes.clear()
      miniaturesPochettes.set(j.cle, url); miniaturesPochettes.set('id:' + j.p.id, url)
      j.noeud.style.backgroundImage = `url(${url})`
    } catch {}
    await new Promise((r) => setTimeout(r, 25))
  }
  minPochettesEnCours = false
}

// -- l'accueil : la rangee « Pochettes » et le menu d'une pochette
function tuilePochette(p) {
  const mini = el('div', { class: 'mini mini-pochette' })
  miniaturePochetteDans(mini, p)
  const t = el('div', { class: 'tuile tuile-pochette', role: 'button', tabindex: '0', style: '--teinte:#965cc4', 'data-nom': nomPochette(p) },
    mini,
    el('div', {}, el('div', { class: 'nom' }, nomPochette(p) || '(sans titre)'), el('div', { class: 'alter' }, libellePochette(p.mode)),
      p.dossier ? el('div', { class: 'compte' }, '📁 ' + p.dossier) : null),
    el('button', { class: 'menu-pt', type: 'button', title: 'Actions de la pochette', 'aria-label': 'Actions de la pochette', onclick: (e) => { e.stopPropagation(); menuPochette(e.currentTarget, p) } }, '⋯'))
  t.addEventListener('click', () => ouvrirPochette(p.id))
  t.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); ouvrirPochette(p.id) } })
  return t
}
function menuPochette(ancre, p) {
  menuFlottant(ancre, [
    ['Ouvrir', () => ouvrirPochette(p.id)],
    ['Renommer…', () => {
      const champ = el('input', { type: 'text', value: nomPochette(p) })
      dialogue('Renommer la pochette', el('div', { class: 'assistant-pile' }, el('label', {}, 'Nouveau nom', champ)),
        [{ texte: 'Annuler' }, { texte: 'Renommer', principal: true, action: () => { p.nom = champ.value.trim(); sauvegarderPlusTard(); vue === 'accueil' ? rendreGrilles() : majListe() } }])
      champ.select()
    }],
    ['Dupliquer', () => { const c = structuredClone({ ...p, art: { ...p.art, blob: null }, titre: { ...p.titre, blob: null }, policeBlob: null }); Object.assign(c, { id: nouvelId(), nom: nomPochette(p) ? `${nomPochette(p)} (${langueUI() === 'fr' ? 'copie' : 'copy'})` : '' }); c.art.blob = p.art.blob; c.titre.blob = p.titre.blob; c.policeBlob = p.policeBlob; vraiesPochettes().push(c); sauvegarderPlusTard(); vue === 'accueil' ? rendreGrilles() : majListe(); message('Pochette dupliquée.') }],
    ['Exporter en PNG', () => exporterPochette(p)],
    ['Supprimer…', () => { if (!confirm(tr(`Supprimer « ${nomPochette(p) || libellePochette(p.mode)} » ?`))) return; projet.pochettes = vraiesPochettes().filter((x) => x.id !== p.id); sauvegarderPlusTard(); if (vue === 'pochette') afficherAccueil(); else (vue === 'accueil' ? rendreGrilles() : majListe()) }, true],
  ])
}

// -- la vue « editeur de pochette »
let minuteurPochette = 0
let textePochetteChoisi = -1
async function dessinerPochette() {
  const p = pochetteParId(pochetteOuverte)
  if (!p) return
  const n = ++seqPochette
  const t = await rendrePochette(p, { choisi: textePochetteChoisi })
  if (n !== seqPochette) return
  const vis = $('#toile-pochette')
  vis.width = t.width; vis.height = t.height
  vis.getContext('2d').drawImage(t, 0, 0)
  vis.boites = t.boites
}
let seqPochette = 0
function changementPochette() {
  clearTimeout(minuteurPochette)
  minuteurPochette = setTimeout(dessinerPochette, 40)
  sauvegarderPlusTard()
  majFil()
}
function ouvrirPochette(id) {
  const p = pochetteParId(id)
  if (!p) return
  validerHistorique()
  pochetteOuverte = id
  textePochetteChoisi = -1
  document.body.removeAttribute('data-vide')
  montrerVue('pochette')
  construireFormulairePochette()
  dessinerPochette()
}
const curseurP = (label, obj, cle, min, max, pas, defaut) => {
  const r = el('input', { type: 'range', min, max, step: pas })
  r.value = obj()[cle] ?? defaut
  r.addEventListener('input', () => { obj()[cle] = Number(r.value); changementPochette() })
  r.addEventListener('dblclick', () => { r.value = defaut; obj()[cle] = defaut; changementPochette() })
  return el('label', {}, label, r)
}
const coulP = (label, obj, cle, defaut) => el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, label),
  pickerCouleur(obj()[cle] ?? defaut, (v) => { obj()[cle] = v; changementPochette() }))
const cochP = (label, obj, cle) => {
  const i = el('input', { type: 'checkbox' }); i.checked = !!obj()[cle]
  i.addEventListener('change', () => { obj()[cle] = i.checked; changementPochette() })
  return el('label', { class: 'ligne' }, i, label)
}
/** Les reglages de l'illustration d'une pochette : image, zoom, decalages. */
function blocIllustrationPochette(p, apres = null) {
  const f = el('input', { type: 'file', accept: 'image/*' })
  f.addEventListener('change', () => { if (f.files[0]) { p.art.blob = f.files[0]; p.art.x = p.art.y = 0; p.art.zoom = 1; changementPochette(); apres?.() } })
  return [
    el('label', {}, 'Image (ou glisse-la sur l’aperçu)', f),
    curseurP('Zoom', () => p.art, 'zoom', 0.5, 4, 0.01, 1),
    el('div', { class: 'rang' }, curseurP('Décalage X', () => p.art, 'x', -1000, 1000, 1, 0), curseurP('Décalage Y', () => p.art, 'y', -1500, 1500, 1, 0)),
    p.art.blob ? el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { p.art.blob = null; changementPochette(); apres?.() } }, 'Retirer l’image') : null,
    el('div', { class: 'aide' }, 'Glisse sur l’aperçu pour déplacer l’image, molette pour zoomer.'),
  ]
}
function blocTitrePochette(p, apres = null) {
  const t = () => p.titre
  const zone = el('textarea', { rows: 2, placeholder: 'Nom du pack' }); zone.value = p.titre.texte
  zone.addEventListener('input', () => { p.titre.texte = zone.value; changementPochette() })
  const fichier = el('input', { type: 'file', accept: 'image/*' })
  fichier.addEventListener('change', () => { p.titre.blob = fichier.files[0] ?? null; changementPochette(); apres?.() })
  const police = el('select', {}, ...POLICES.map(([v, n]) => el('option', { value: v }, n)), p.policeBlob ? el('option', { value: POLICE_PERSO }, 'Ma police') : null, el('option', { value: '__ajouter' }, 'Ma police (.ttf / .otf)…'))
  police.value = p.titre.police
  const fp = el('input', { type: 'file', accept: '.ttf,.otf,.woff,.woff2', hidden: true })
  fp.addEventListener('change', () => { if (fp.files[0]) { p.policeBlob = fp.files[0]; p.titre.police = POLICE_PERSO; changementPochette(); apres?.() } })
  police.addEventListener('change', () => { if (police.value === '__ajouter') { police.value = p.titre.police; fp.click(); return } p.titre.police = police.value; changementPochette() })
  return [
    el('label', {}, 'Texte (une ligne par retour)', zone),
    el('label', {}, 'Ou une image de titre déjà dessinée', fichier),
    p.titre.blob ? el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { p.titre.blob = null; changementPochette(); apres?.() } }, 'Retirer l’image de titre') : null,
    el('label', {}, 'Police', police), fp,
    coulP('Remplissage haut', t, 'haut', '#e23a6a'), coulP('Remplissage bas', t, 'bas', '#a3123a'), coulP('Contour', t, 'contour', '#ffffff'),
    curseurP('Épaisseur du contour', t, 'epaisseur', 0, 40, 1, 0), curseurP('Taille', t, 'taille', 20, 400, 1, TITRE_DEFAUT(p.mode)),
    el('div', { class: 'rang' }, curseurP('Position horizontale', t, 'x', -400, 400, 1, 0), curseurP('Position verticale', t, 'y', -600, 600, 1, 0)),
    cochP('Ombre portée', t, 'ombre'),
  ]
}
const TITRE_DEFAUT = (mode) => titreDefaut(mode).taille
function blocCouleursPochette(p, apres = null) {
  const boite = couleurOrigine(p.mode, 'boite'), etiquette = couleurOrigine(p.mode, 'etiquette')
  return [
    el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Boîte du bas'),
      pickerCouleur(p.couleurBoite ?? boite, (v) => { p.couleurBoite = v; changementPochette() })),
    el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, `Étiquette (« ${NOMS_ETIQUETTE[p.mode]} »)`),
      pickerCouleur(p.couleurEtiquette ?? etiquette, (v) => { p.couleurEtiquette = v; changementPochette() })),
    el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { p.couleurBoite = p.couleurEtiquette = null; changementPochette(); apres ? apres() : construireFormulairePochette() } }, 'Revenir aux couleurs d’origine'),
  ]
}
function blocMentionsPochette(p, apres = null) {
  const liste = el('div', { class: 'liste-textes' })
  const relancer = () => (apres ? apres() : construireFormulairePochette())
  p.textes.forEach((t, i) => {
    const zone = el('textarea', { rows: 2, placeholder: 'Ton texte' }); zone.value = t.texte
    zone.addEventListener('input', () => { t.texte = zone.value; changementPochette() })
    const police = el('select', {}, ...POLICES.map(([v, n]) => el('option', { value: v }, n)))
    police.value = t.police
    police.addEventListener('change', () => { t.police = police.value; changementPochette() })
    liste.append(el('div', { class: 'texte-libre' + (i === textePochetteChoisi ? ' choisi' : ''), onpointerdown: () => { if (textePochetteChoisi !== i) { textePochetteChoisi = i; dessinerPochette() } } },
      zone, police,
      el('div', { class: 'rang' }, el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Couleur'), pickerCouleur(t.couleur, (v) => { t.couleur = v; changementPochette() })),
        el('div', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Contour'), pickerCouleur(t.contour, (v) => { t.contour = v; changementPochette() }))),
      el('div', { class: 'rang' }, curseurP('Taille', () => t, 'taille', 12, 200, 1, 44), curseurP('Épaisseur du contour', () => t, 'epaisseur', 0, 40, 1, 6)),
      el('div', { class: 'rang' }, cochP('Gras', () => t, 'gras'), cochP('Ombre', () => t, 'ombre'),
        el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { p.textes.splice(i, 1); textePochetteChoisi = -1; changementPochette(); relancer() } }, 'Supprimer'))))
  })
  return [
    el('div', { class: 'aide' }, 'Les logos de la gamme sont intégrés au gabarit. Ajoute ici le nom du créateur, une mention, ce que tu veux ; glisse un texte sur l’aperçu pour le placer.'),
    liste,
    el('button', { class: 'btn petit fixe', type: 'button', onclick: () => { p.textes.push(texteLibre(p.mode, carte()?.langue ?? (langueUI() === 'fr' ? 'fr' : 'en'))); textePochetteChoisi = p.textes.length - 1; changementPochette(); relancer() } }, '+ Ajouter un texte'),
  ]
}
function construireFormulairePochette() {
  const racine = $('#form-pochette')
  racine.replaceChildren()
  const p = pochetteParId(pochetteOuverte)
  if (!p) return
  const nom = el('input', { type: 'text', value: p.nom ?? '', placeholder: 'ex. Valkyrie' })
  nom.addEventListener('input', () => { p.nom = nom.value; changementPochette() })
  const mode = el('select', {}, MODES.map(([m, n]) => el('option', { value: m }, n)))
  mode.value = p.mode
  mode.addEventListener('change', () => { changerMode(p, mode.value); changementPochette(); construireFormulairePochette() })
  const dossier = el('select', {}, el('option', { value: '' }, 'Indépendante (sans dossier)'), ...listeDossiers().map((d) => el('option', { value: d.nom }, d.nom)))
  dossier.value = p.dossier || ''
  dossier.addEventListener('change', () => { p.dossier = dossier.value; changementPochette() })
  const f = [
    section('Général', true, el('label', {}, 'Nom de la pochette', nom), el('label', {}, 'Type de pochette', mode), el('label', {}, 'Rattachée au dossier', dossier)),
    section('Illustration', false, ...blocIllustrationPochette(p, construireFormulairePochette)),
    section('Titre', false, ...blocTitrePochette(p, construireFormulairePochette)),
    section('Couleurs', false, ...blocCouleursPochette(p)),
    section('Logos et mentions', false, ...blocMentionsPochette(p)),
    section('Exporter', false, el('button', { class: 'btn principal', type: 'button', onclick: () => exporterPochette(p) }, 'Télécharger en PNG'), el('div', { class: 'aide' }, `PNG ${DIMENSIONS[p.mode][0]} × ${DIMENSIONS[p.mode][1]}. Elle part aussi dans le pack .zip de son dossier.`)),
  ]
  replierSections(f, 'pochette:' + p.id)
  racine.append(...f)
}
/** Les pochettes d'un pack (dossier ou tout le projet), en PNG, pour le .zip : [{ nom, octets }]. */
async function pochettesPourPack(dossier, portee) {
  const liste = portee === 'tout' ? vraiesPochettes() : pochettesDuDossier(dossier || '')
  const sortie = []
  let k = 0
  for (const p of liste) {
    const t = await rendrePochette(p, { apercu: false })
    const blob = await new Promise((ok) => t.toBlob(ok, 'image/png'))
    sortie.push({ nom: `pochettes/${nomFichierPochette(p)}${liste.length > 1 ? '-' + ++k : ''}.png`, octets: new Uint8Array(await blob.arrayBuffer()) })
  }
  return sortie
}
async function exporterPochette(p) {
  const t = await rendrePochette(p, { apercu: false })
  const blob = await new Promise((ok) => t.toBlob(ok, 'image/png'))
  telecharger(blob, nomFichierPochette(p) + '.png')
  message(`PNG exporté (${t.width} × ${t.height}).`)
}
/** Souris sur l'apercu de la pochette : glisser un texte ou l'image, molette pour zoomer l'image. */
function brancherPochette() {
  const toile = $('#toile-pochette')
  let prise = null
  const pointe = (e) => {
    const r = toile.getBoundingClientRect(), k = toile.width / r.width
    const px = (e.clientX - r.left) * k, py = (e.clientY - r.top) * k
    const boites = toile.boites ?? []
    for (let i = boites.length - 1; i >= 0; i--) { const b = boites[i]; if (b && px >= b.x && px <= b.x + b.l && py >= b.y && py <= b.y + b.h) return i }
    return -1
  }
  toile.addEventListener('pointerdown', (e) => {
    const p = pochetteParId(pochetteOuverte); if (!p) return
    const i = pointe(e)
    if (i >= 0) { textePochetteChoisi = i; const t = p.textes[i]; prise = { t, x: e.clientX, y: e.clientY, tx: t.x, ty: t.y } }
    else { textePochetteChoisi = -1; prise = { x: e.clientX, y: e.clientY, ax: p.art.x, ay: p.art.y } }
    toile.setPointerCapture(e.pointerId)
  })
  toile.addEventListener('pointermove', (e) => {
    if (!prise) return
    const p = pochetteParId(pochetteOuverte); if (!p) return
    const k = toile.width / toile.getBoundingClientRect().width
    if (prise.t) { prise.t.x = prise.tx + (e.clientX - prise.x) * k; prise.t.y = prise.ty + (e.clientY - prise.y) * k }
    else { p.art.x = prise.ax + (e.clientX - prise.x) * k; p.art.y = prise.ay + (e.clientY - prise.y) * k }
    changementPochette()
  })
  const fin = () => { if (prise) { prise = null; construireFormulairePochette() } }
  toile.addEventListener('pointerup', fin); toile.addEventListener('pointercancel', fin)
  toile.addEventListener('wheel', (e) => {
    const p = pochetteParId(pochetteOuverte); if (!p || !p.art.blob) return
    e.preventDefault()
    p.art.zoom = Math.max(0.5, Math.min(4, p.art.zoom * (e.deltaY < 0 ? 1.05 : 1 / 1.05)))
    changementPochette()
    clearTimeout(brancherPochette.t); brancherPochette.t = setTimeout(construireFormulairePochette, 300)
  }, { passive: false })
  toile.addEventListener('dragover', (e) => e.preventDefault())
  toile.addEventListener('drop', (e) => {
    e.preventDefault()
    const p = pochetteParId(pochetteOuverte); const f = [...e.dataTransfer.files].find((x) => x.type.startsWith('image/'))
    if (p && f) { p.art.blob = f; p.art.x = p.art.y = 0; p.art.zoom = 1; changementPochette(); construireFormulairePochette() }
  })
}

// -- le wizard de pochette (court, passe sur tout)
function ouvrirWizardPochette(modeDepart = 'heros', dossierDepart = '') {
  const p = nouvellePochette(modeDepart, dossierDepart)
  const pile = (...n) => el('div', { class: 'assistant-pile' }, ...n.flat().filter(Boolean))
  const aide = {
    heros: 'La couverture d’un pack de héros (format carte, titre en haut).',
    scenario: 'La couverture d’un scénario (format carte, titre en bas).',
    modulaire: 'La couverture d’un set modulaire (comme le scénario, étiquette « Modular Set »).',
    boite: 'L’avant d’une grosse boîte d’extension (format carré).',
  }
  const etapes = [
    {
      titre: 'Quelle pochette ?', court: 'Type',
      aide: 'Le type fixe le format, les logos et l’étiquette.',
      plus: 'Héros, scénario et modulaire ont le format carte du jeu (938 × 1538) avec leurs propres logos ; l’extension est carrée (1000 × 1000), pour l’avant d’une boîte.',
      construire: (v, rafraichir) => el('div', { class: 'assistant-types' }, ...MODES.map(([m, nom]) => el('button', {
        class: 'btn petit' + (p.mode === m ? ' principal' : ''), type: 'button', onclick: () => { changerMode(p, m); rafraichir() },
      }, el('b', {}, tr(nom)), el('span', {}, tr(aide[m]))))),
    },
    {
      titre: 'Rattachement', court: 'Dossier', passable: true,
      aide: 'À un dossier existant, ou indépendante.',
      plus: 'Rattachée à un dossier, la pochette apparaît dans sa colonne des cartes et part dans son pack .zip. Indépendante, elle est rangée dans la rangée « Pochettes » de l’accueil.',
      construire: (v, rafraichir) => {
        const tuiles = el('div', { class: 'assistant-tuiles' },
          el('button', { type: 'button', class: 'tuile-dossier' + (!p.dossier ? ' choisie' : ''), style: '--teinte:#965cc4', onclick: () => { p.dossier = ''; rafraichir() } },
            el('span', { class: 'tuile-nom' }, 'Indépendante'), el('small', {}, 'Sans dossier')),
          ...listeDossiers().map((d) => el('button', { type: 'button', class: 'tuile-dossier' + (p.dossier === d.nom ? ' choisie' : ''), onclick: () => { p.dossier = d.nom; rafraichir() } },
            el('span', { class: 'tuile-nom' }, '📁 ' + d.nom), el('small', {}, `${d.cartes.length} carte(s)`))))
        return pile(tuiles)
      },
    },
    {
      titre: 'Le nom et le titre', court: 'Titre', passable: true,
      aide: 'Le titre écrit sur la pochette, et son nom dans ta liste.',
      plus: 'Le titre peut être un texte (avec la police et les couleurs de ton choix, à l’étape suivante) ou une image déjà dessinée. Le nom sert seulement à retrouver la pochette dans tes listes ; sans nom, c’est le titre qui sert.',
      construire: () => {
        const nom = el('input', { type: 'text', value: p.nom, placeholder: 'ex. Valkyrie' })
        nom.addEventListener('input', () => { p.nom = nom.value })
        const zone = el('textarea', { rows: 2, placeholder: 'Nom du pack' }); zone.value = p.titre.texte
        zone.addEventListener('input', () => { p.titre.texte = zone.value })
        const fichier = el('input', { type: 'file', accept: 'image/*' })
        fichier.addEventListener('change', () => { p.titre.blob = fichier.files[0] ?? null })
        return pile(el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Nom de la pochette'), nom),
          el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Titre (une ligne par retour)'), zone),
          el('label', { class: 'assistant-champ' }, el('span', { class: 'assistant-libelle' }, 'Ou une image de titre déjà dessinée'), fichier))
      },
    },
    {
      titre: 'L’illustration', court: 'Image', passable: true,
      aide: 'L’image de fond, avec son zoom et sa position.',
      plus: 'Prends une image assez grande pour couvrir la pochette. Zoom et décalages règlent le cadrage ; dans l’éditeur de pochette, tu pourras aussi la déplacer à la souris sur l’aperçu.',
      construire: (v, rafraichir) => pile(blocIllustrationPochette(p, rafraichir)),
    },
    {
      titre: 'Le style du titre', court: 'Style', passable: true,
      aide: 'Police, couleurs, contour, taille et position du titre.',
      plus: 'Le titre est dessiné avec un dégradé (haut / bas), un contour et une ombre facultatifs. Tu peux charger ta propre police (.ttf, .otf). Si tu as chargé une image de titre, seuls la taille et la position comptent.',
      construire: (v, rafraichir) => pile(blocTitrePochette(p, rafraichir)),
    },
    {
      titre: 'Les couleurs', court: 'Couleurs', passable: true,
      aide: 'La boîte du bas et l’étiquette : un picker chacune.',
      plus: 'Les couleurs sont appliquées en gardant les ombres et les blancs du gabarit. « Revenir aux couleurs d’origine » remet celles du PSD.',
      construire: (v, rafraichir) => pile(blocCouleursPochette(p, rafraichir)),
    },
    {
      titre: 'Logos et mentions', court: 'Mentions', passable: true,
      aide: 'Le nom du créateur et tes textes libres.',
      plus: 'Les logos de la gamme sont déjà dans le gabarit. Ajoute un texte pour le nom du créateur ou une mention : tu le places ensuite à la souris dans l’éditeur de pochette.',
      construire: (v, rafraichir) => pile(blocMentionsPochette(p, rafraichir)),
    },
    {
      titre: 'C’est prête', court: 'Fin',
      aide: 'La pochette s’ouvre dans son éditeur, pour les finitions.',
      construire: () => el('ul', { style: 'margin:0;padding-left:18px' },
        el('li', {}, `Type : ${libellePochette(p.mode)}`), el('li', {}, `Titre : ${(p.titre.texte || '').split('\n')[0] || '—'}`), el('li', {}, `Dossier : ${p.dossier || tr('Indépendante')}`)),
    },
  ]
  lancerAssistant('Nouvelle pochette', etapes, () => {
    vraiesPochettes().push(p)
    sauvegarderPlusTard()
    ouvrirPochette(p.id)
  }, { rendreCanvas: () => rendrePochette(p) })
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
/** Le projet entier en un fichier : dossiers (genre, ordre), templates, cartes de depart, styles, cartes avec leurs images.
 * Reouvert par « Importer » (ajouter, ou remplacer tout) il remet la page comme elle etait. */
async function serialiserPochette(p) {
  const c = structuredClone({ ...p, art: { ...p.art, blob: null }, titre: { ...p.titre, blob: null }, policeBlob: null })
  c.art.image = p.art.blob ? await blobVersDataUrl(p.art.blob) : null
  c.titre.image = p.titre.blob ? await blobVersDataUrl(p.titre.blob) : null
  c.policeImage = p.policeBlob ? await blobVersDataUrl(p.policeBlob) : null
  return c
}
async function deserialiserPochette(j) {
  const base = nouvellePochette(MODES.some(([m]) => m === j.mode) ? j.mode : 'heros')
  const p = { ...base, ...j, art: { ...base.art, ...j.art }, titre: { ...base.titre, ...j.titre }, textes: j.textes ?? [] }
  p.art.blob = p.art.image ? await dataUrlVersBlob(p.art.image) : null; delete p.art.image
  p.titre.blob = p.titre.image ? await dataUrlVersBlob(p.titre.image) : null; delete p.titre.image
  p.policeBlob = j.policeImage ? await dataUrlVersBlob(j.policeImage) : null; delete p.policeImage
  return p
}
async function documentProjetComplet() {
  const cartes = []
  for (const c of vraiesCartes()) cartes.push(await serialiser(c))
  const modeles = []
  for (const m of projet.modeles ?? []) modeles.push({ id: m.id, nom: m.nom, dossier: m.dossier, carte: await serialiser(m.carte) })
  const pochettes = []
  for (const p of vraiesPochettes()) pochettes.push(await serialiserPochette(p))
  return { format: 'createur-cartes', version: 3, complet: true, cartes, modeles, pochettes, styles: projet.styles ?? [], gabarits: projet.gabarits ?? {}, dossiers: projet.dossiers ?? {} }
}
async function exporterProjet() {
  const doc = await documentProjetComplet()
  const lisezmoi = `MC Creator : sauvegarde complete (${doc.cartes.length} carte(s), ${doc.pochettes.length} pochette(s), ${Object.keys(doc.dossiers).length} dossier(s)).\n\nPour tout retrouver sur un autre ordinateur : ouvre MC Creator, clique sur « Importer… » (colonne de droite) et choisis ce fichier .zip.\nTu pourras alors AJOUTER son contenu a ton projet, ou le REMPLACER entierement : dossiers, couleurs des templates, cartes, images.\n\nGarde ce fichier en lieu sur : tes cartes ne sont conservees que dans ton navigateur.\n`
  const zip = creerZip([{ nom: 'projet.json', octets: new TextEncoder().encode(JSON.stringify(doc)) }, { nom: 'LISEZ-MOI.txt', octets: new TextEncoder().encode(lisezmoi) }])
  telecharger(zip, `mc-creator-${new Date().toISOString().slice(0, 10)}.zip`)
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
  // 1) on LIT tout dans une zone de preparation (rien n'est change tant qu'on n'a pas choisi)
  const prep = { cartes: [], modeles: [], pochettes: [], styles: [], gabarits: {}, dossiers: {}, complet: false }
  const traiter = async (j) => {
    if (Array.isArray(j)) { for (const x of j) await traiter(x); return }
    if (j?.format === 'createur-cartes') {
      if (j.complet) prep.complet = true
      prep.styles.push(...(j.styles ?? []))
      for (const m of j.modeles ?? []) prep.modeles.push({ id: m.id, nom: m.nom, dossier: m.dossier, carte: await deserialiser(m.carte) })
      for (const x of j.pochettes ?? []) prep.pochettes.push(await deserialiserPochette(x))
      Object.assign(prep.gabarits, j.gabarits ?? {})
      Object.assign(prep.dossiers, j.dossiers ?? {})
      for (const x of j.cartes) {
        if (!TYPES[x.type]) continue
        prep.cartes.push(await deserialiser(x))
      }
    } else if (j?.selectType) prep.cartes.push(await carteDepuisReference(j))
  }
  for (const f of fichiers) {
    const buf = await f.arrayBuffer()
    if (/\.zip$/i.test(f.name)) {
      for (const e of await lireZip(buf)) if (/\.json$/i.test(e.nom)) { try { await traiter(JSON.parse(texteJson(e.octets))) } catch {} }
    } else {
      await traiter(JSON.parse(texteJson(buf)))
    }
  }
  if (!prep.cartes.length && !prep.pochettes.length && !Object.keys(prep.dossiers).length) throw new Error('aucune carte reconnue dans ces fichiers')
  // 2) une sauvegarde complete sur un projet qui contient deja des cartes : on demande « ajouter » ou « remplacer »
  const deja = vraiesCartes().length > 0 || vraiesPochettes().length > 0
  const choix = prep.complet && deja ? await demanderModeImport(prep) : (prep.complet ? 'remplacer' : 'ajouter')
  if (!choix) return
  appliquerImport(prep, choix)
}
function demanderModeImport(prep) {
  return new Promise((fini) => {
    let rendu = false
    const repondre = (v) => { if (!rendu) { rendu = true; fini(v) } }
    const d = dialogue('Importer une sauvegarde complète',
      el('div', { class: 'assistant-pile' },
        el('p', { class: 'assistant-aide' }, `Ce fichier contient ${prep.cartes.length} carte(s) dans ${Object.keys(prep.dossiers).length} dossier(s). Ton projet actuel contient déjà ${vraiesCartes().length} carte(s).`),
        el('p', { class: 'aide' }, '« Ajouter » garde ton projet et y met le contenu du fichier (les dossiers du même nom sont fusionnés). « Remplacer » efface ton projet actuel et remet exactement celui du fichier.')),
      [{ texte: 'Annuler', action: () => repondre(null) }, { texte: 'Ajouter', action: () => repondre('ajouter') }, { texte: 'Remplacer tout', principal: true, action: () => repondre('remplacer') }])
    d.addEventListener('close', () => repondre(null))
  })
}
function appliquerImport(prep, mode) {
  historiques.clear()
  if (mode === 'remplacer') {
    projet.cartes = []
    projet.dossiers = {}
    projet.gabarits = {}
    projet.modeles = []
    projet.styles = []
    projet.pochettes = []
    projet.courante = null
  }
  // en « ajouter », chaque carte recoit un identifiant neuf (et les liens recto-verso suivent) ; en « remplacer », elles gardent les leurs
  const ids = new Map(prep.cartes.map((c) => [c.id, mode === 'remplacer' ? c.id : nouvelId()]))
  for (const c of prep.cartes) {
    if (c.verso?.mode === 'carte' && ids.has(c.verso.carteId)) c.verso.carteId = ids.get(c.verso.carteId)
    c.id = ids.get(c.id)
    projet.cartes.push(c)
  }
  for (const p of prep.pochettes) { p.id = mode === 'remplacer' ? p.id : nouvelId(); vraiesPochettes().push(p) }
  for (const st of prep.styles) { projet.styles ??= []; if (!projet.styles.some((x) => x.id === st.id)) projet.styles.push(st) }
  for (const m of prep.modeles) { projet.modeles ??= []; if (mode === 'ajouter' || !projet.modeles.some((x) => x.id === m.id)) projet.modeles.push({ ...m, id: mode === 'remplacer' ? m.id : nouvelId() }) }
  for (const [d, g] of Object.entries(prep.gabarits)) (projet.gabarits ??= {})[d] ??= g
  for (const [d, m] of Object.entries(prep.dossiers)) (projet.dossiers ??= {})[d] ??= m
  ranger()
  sauvegarderPlusTard()
  message(`${prep.cartes.length} carte(s) importée(s).`)
  if (prep.complet || !prep.cartes.length) return afficherAccueil()
  const derniere = prep.cartes[prep.cartes.length - 1]
  ouvrirDossier(derniere.dossier || DIVERS, derniere.id)
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
    changerType(c, sel.value)
    construireFormulaire()
    changement()
  })
  const sauve = await lireProjet()
  projet = sauve?.cartes ? sauve : { cartes: [], courante: null }
  preparerProjet(projet)
  synchro.baseline()

  // le vide du dossier (un dossier sans carte)
  $('#vue-editeur').append(el('div', { class: 'vide-dossier', id: 'vide-dossier', hidden: true },
    el('h3', {}, ''), el('p', { class: 'aide' }, 'Ce dossier est vide.'),
    el('div', { class: 'rang', style: 'justify-content:center' },
      el('button', { class: 'btn principal', type: 'button', onclick: () => ouvrirWizardCarte(dossierOuvert) }, '+ Nouvelle carte'))))

  $('#lang-fr').addEventListener('click', () => changerLangue('fr'))
  $('#lang-en').addEventListener('click', () => changerLangue('en'))
  $('#c-nouvelle').addEventListener('click', () => ouvrirWizardCarte(dossierOuvert))
  $('#c-dupliquer').addEventListener('click', () => {
    if (!carte()) return message('Choisis d’abord une carte.')
    const copie = { ...cloner(carte()), id: nouvelId() }
    copie.contenu.titre += langueUI() === 'fr' ? ' (copie)' : ' (copy)'
    ajouter(copie)
  })
  $('#c-deplacer').addEventListener('click', () => {
    const c = carte()
    if (!c) return message('Choisis d’abord une carte.')
    const autres = listeDossiers().filter((d) => d.nom !== c.dossier)
    const choix = el('select', {}, el('option', { value: '' }, '—'), ...autres.map((d) => el('option', { value: d.nom }, d.nom)))
    const nouveau = el('input', { type: 'text', placeholder: 'ex. Valkyrie' })
    dialogue('Déplacer la carte', el('div', { class: 'assistant-pile' }, el('label', {}, 'Vers le dossier', choix), el('label', {}, 'Ou un nouveau dossier', nouveau)),
      [{ texte: 'Annuler' }, { texte: 'Déplacer', principal: true, action: () => {
        const nom = nouveau.value.trim() || choix.value
        if (!nom) return false
        c.dossier = nom
        creerDossier(nom, genreInfere(nom))
        sauvegarderPlusTard()
        ouvrirDossier(nom, c.id)
      } }])
  })
  $('#c-supprimer').addEventListener('click', () => {
    const c = carte()
    if (!c || !confirm(tr(`Supprimer « ${c.contenu.titre || 'cette carte'} » ?`))) return
    projet.cartes = projet.cartes.filter((x) => x.id !== c.id)
    ouvrirDossier(c.dossier)
  })
  $('#recherche').addEventListener('input', () => majListe())
  $('#p-versions').addEventListener('click', () => ouvrirVersions(restaurerLocal, synchro.etat !== 'connecte' ? null : {
    dossier: dossierOuvert || '',
    versions: () => synchro.versions(dossierOuvert),
    restaurer: async (n) => { await ajouterVersion(projet, 'avant restauration'); await synchro.restaurerVersion(dossierOuvert, n); apresRapatriement(); message('Version restaurée.') },
  }))
  const restaurerLocal = (p) => { projet = p; preparerProjet(projet); historiques.clear(); apresRapatriement(); message('Version restaurée.') }
  $('#p-remplacer').addEventListener('click', ouvrirRemplacer)
  $('#p-appliquer').addEventListener('click', () => { if (!carte()) return message('Choisis d’abord une carte.'); ouvrirAppliquer(rolesDe) })
  $('#b-annuler').addEventListener('click', annuler)
  $('#b-retablir').addEventListener('click', retablir)
  document.addEventListener('keydown', (e) => {
    if (vue !== 'editeur' || !carte()) return
    if (!(e.ctrlKey || e.metaKey) || e.altKey) return
    const natif = e.target.isContentEditable || /^(INPUT|TEXTAREA)$/.test(e.target.tagName) && e.target.type !== 'range'
    if (natif) return
    const k = e.key.toLowerCase()
    if (k === 'z' && !e.shiftKey) { e.preventDefault(); annuler() } else if (k === 'y' || (k === 'z' && e.shiftKey)) { e.preventDefault(); retablir() }
  })
  $('#b-export').addEventListener('click', () => (vue === 'pochette' ? exporterPochette(pochetteParId(pochetteOuverte)) : exporter(false)))
  $('#b-export-2').addEventListener('click', () => exporter(true))
  $('#b-print').addEventListener('click', dialoguePlanche)
  $('#b-pack').addEventListener('click', () => ouvrirExportPack({ cartes: () => projet.cartes.filter((c) => !c.brouillon), carte, rendre: rendreCarte, rendreVerso, serialiser, pochettes: pochettesPourPack }))
  $('#b-tts').addEventListener('click', plancheTTS)
  $('#b-comparer').addEventListener('click', () => ouvrirComparable(rendreCarte))
  $('#p-exporter').addEventListener('click', exporterProjet)
  $('#p-importer').addEventListener('click', () => $('#p-fichier').click())
  $('#p-fichier').addEventListener('change', async (e) => {
    try { await importerFichiers([...e.target.files]) } catch (err) { message('Ouverture impossible : ' + err.message) }
    e.target.value = ''
  })
  brancherToile()
  brancherPochette()
  chargerCalques('/createur-cartes/img/pochettes/')
  brancherPoignees()
  brancherMenuExport()
  afficherAccueil()
  synchro.demarrer() // sans attendre : la page marche tout de suite avec ce qu'elle a, la fusion arrive ensuite
}
/** Remet un projet charge (disque, serveur, version) dans l'etat que la page attend. */
function preparerProjet(p) {
  p.cartes = (p.cartes ?? []).filter((c) => TYPES[c.type] && !c.brouillon)
  for (const c of p.cartes) { c.libres ??= []; c.cadre ??= 'officiel'; c.dossier ??= ''; c.verso ??= { mode: 'aucun', carteId: null, blob: null } }
  p.dossiers ??= {}
  p.gabarits ??= {}
  p.pochettes = (p.pochettes ?? []).filter((x) => MODES.some(([m]) => m === x.mode))
  ranger()
  if (!p.cartes.some((c) => c.id === p.courante)) p.courante = null
}
demarrer().catch((e) => message('Démarrage impossible : ' + e.message))
