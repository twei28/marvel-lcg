// La page du créateur de cartes : liste de cartes, formulaire guidé par type, aperçu en direct, couleurs, illustration, tête d'angle,
// sauvegarde (IndexedDB + fichier .json), exports (PNG / JPG / WebP, FR + EN, planche à imprimer, planche TTS).
import { dessinerCarte, CHAMPS_VIDES, LIBELLES } from './carte.js'
import { chargerPolices } from './polices.js'
import { ICONES } from './polices.js'
import { TEXTES, chargerTraits, traduireTraits } from './langues.js'

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
// Les aspects ne sont pas dans palettes.json (sauf Agression, Justice, Basic) : trois sont approchés a la main.
const ASPECTS = {
  'Basic (gris)': 'basic-grey_hero', Agression: 'aggression_hero', Justice: 'justice_hero',
  Direction: { left_color: '#1d5da6', right_color: '#1f63ad', left_accent: '#a6c4e6', right_accent: '#4f95d6', divider: '#1d5da6', light_boxes: '#b5c4d6', splash: '#174a86' },
  Protection: { left_color: '#2f7d3a', right_color: '#2e8a3d', left_accent: '#a8d3a9', right_accent: '#5fb56a', divider: '#2f7d3a', light_boxes: '#b8d0b4', splash: '#226b2d' },
  Pool: { left_color: '#c9741c', right_color: '#cf7a1a', left_accent: '#f0c28f', right_accent: '#f2a24b', divider: '#c9741c', light_boxes: '#e4cdb2', splash: '#9c5714' },
}
const GENRES_RESSOURCE = [['', 'Aucune'], ['energy', 'Énergie'], ['mental', 'Mental'], ['physical', 'Physique'], ['wild', 'Joker']]
const ICONES_BARRE = [['energy', 'Énergie'], ['mental', 'Mental'], ['physical', 'Physique'], ['wild', 'Joker'], ['star', 'Étoile'], ['acceleration', 'Accélération'], ['crisis', 'Crise'], ['hazard', 'Danger'], ['boost', 'Renfort'], ['per_hero', 'Par héros'], ['consequential', 'Dégâts conséquents'], ['unique', 'Unique']]
const TYPES_SANS_FISSURES = new Set(['attachment', 'environment', 'minion', 'obligation-villain', 'sidescheme', 'treachery'])

const $ = (s, r = document) => r.querySelector(s)
const el = (tag, attrs = {}, ...enfants) => {
  const e = document.createElement(tag)
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'class') e.className = v
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v)
    else if (v === true) e.setAttribute(k, '')
    else if (v !== false && v != null) e.setAttribute(k, v)
  }
  for (const c of enfants.flat()) if (c != null) e.append(c.nodeType ? c : document.createTextNode(c))
  return e
}

let TYPES = null
let PALETTES = null
let projet = { cartes: [], courante: null }
let seq = 0
let ciblePointeur = 'art'
const imagesBlob = new WeakMap()

// ---------------------------------------------------------------- stockage
function ouvrirBase() {
  return new Promise((ok, ko) => {
    const r = indexedDB.open('createur-cartes', 1)
    r.onupgradeneeded = () => r.result.createObjectStore('kv')
    r.onsuccess = () => ok(r.result)
    r.onerror = () => ko(r.error)
  })
}
async function lireProjet() {
  try {
    const db = await ouvrirBase()
    return await new Promise((ok) => {
      const q = db.transaction('kv').objectStore('kv').get('projet')
      q.onsuccess = () => ok(q.result ?? null)
      q.onerror = () => ok(null)
    })
  } catch {
    return null
  }
}
let minuteurSauvegarde = 0
function sauvegarderPlusTard() {
  clearTimeout(minuteurSauvegarde)
  minuteurSauvegarde = setTimeout(async () => {
    try {
      const db = await ouvrirBase()
      db.transaction('kv', 'readwrite').objectStore('kv').put(projet, 'projet')
    } catch (e) {
      message('Sauvegarde dans le navigateur impossible : ' + e.message)
    }
  }, 500)
}

// ---------------------------------------------------------------- images
function imageDe(blob) {
  if (!blob) return Promise.resolve(null)
  if (!imagesBlob.has(blob)) {
    imagesBlob.set(
      blob,
      new Promise((ok, ko) => {
        const im = new Image()
        im.onload = () => ok(im)
        im.onerror = () => ko(new Error('image illisible'))
        im.src = URL.createObjectURL(blob)
      })
    )
  }
  return imagesBlob.get(blob)
}
const blobVersDataUrl = (blob) => new Promise((ok) => { const r = new FileReader(); r.onload = () => ok(r.result); r.readAsDataURL(blob) })
const dataUrlVersBlob = async (url) => (await fetch(url)).blob()

// ---------------------------------------------------------------- cartes
const nouvelId = () => Math.random().toString(36).slice(2, 10)

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
    id: nouvelId(), type, langue, contenu: valeursParDefaut(type, langue), couleurs: {}, fissures: true,
    art: { blob: null, zoom: 1, x: 0, y: 0, rotation: 0 }, artDevant: { blob: null, zoom: 1, x: 0, y: 0, rotation: 0 },
    tete: { blob: null, afficher: true, etoile: false, zoom: 0.8, x: -19, y: 232, rotation: 0 },
  }
}
const carte = () => projet.cartes.find((c) => c.id === projet.courante)

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
  const couleurs = { ...c.couleurs }
  return {
    couleurs,
    art: art && { image: art, x: c.art.x, y: c.art.y, zoom: c.art.zoom, rotation: c.art.rotation },
    artDevant: artDevant && { image: artDevant, x: c.artDevant.x, y: c.artDevant.y, zoom: c.artDevant.zoom, rotation: c.artDevant.rotation },
    tete: tete && { image: tete, afficher: c.tete.afficher, etoile: c.tete.etoile, zoom: c.tete.zoom, x: c.tete.x, y: c.tete.y, rotation: c.tete.rotation },
    fissures: c.fissures,
  }
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
  } catch (e) {
    message('Rendu impossible : ' + e.message)
  }
}
let minuteurRendu = 0
function changement() {
  clearTimeout(minuteurRendu)
  minuteurRendu = setTimeout(dessiner, 40)
  sauvegarderPlusTard()
  majListe()
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
  const champ = opts.long ? el('textarea', { rows: opts.lignes ?? 3 }) : el('input', { type: 'text' })
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
  const i = el('input', { type: 'text' })
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
function barreRegles(zone) {
  const insere = (avant, apres = '') => {
    const a = zone.selectionStart
    const b = zone.selectionEnd
    zone.setRangeText(avant + zone.value.slice(a, b) + apres, a, b, 'end')
    zone.dispatchEvent(new Event('input'))
    zone.focus()
  }
  const barre = el('div', { class: 'outils' })
  barre.append(
    el('button', { class: 'btn petit', type: 'button', title: 'Gras', onclick: () => insere('<b>', '</b>') }, el('b', {}, 'G')),
    el('button', { class: 'btn petit', type: 'button', title: 'Italique', onclick: () => insere('<i>', '</i>') }, el('i', {}, 'I')),
    el('button', { class: 'btn petit', type: 'button', title: 'Trait (police des traits)', onclick: () => insere('<em>', '</em>') }, 'Trait'),
    el('button', { class: 'btn petit', type: 'button', title: 'Saut de paragraphe', onclick: () => insere('\n\n') }, '¶'),
    el('button', { class: 'btn petit', type: 'button', title: 'Filet horizontal', onclick: () => insere('<hr/>') }, '―')
  )
  for (const [nom, titre] of ICONES_BARRE) {
    barre.append(el('button', { class: 'btn petit', type: 'button', title: titre, style: 'font-family:ChampionsIcons', onclick: () => insere(`[${nom}]`) }, ICONES[nom]))
  }
  return barre
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

  // texte
  const texte = [t('Titre', 'titre'), coche('Carte unique (✦)', (x) => x.contenu, 'unique')]
  if (aElement(spec, 'typestr')) texte.push(t('Libellé du type (vide = automatique)', 'typeTexte'))
  if (aElement(spec, 'traits')) texte.push(t('Traits (séparés par des points)', 'traits'))
  if (aElement(spec, 'rules')) {
    const regles = t('Règles', 'regles', { long: true, lignes: 5 })
    texte.push(barreRegles(regles.querySelector('textarea')), regles)
  }
  if (aElement(spec, 'quote')) texte.push(t('Citation', 'citation', { long: true, lignes: 2 }))
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

  // tete d'angle
  if (spec.tete) {
    f.push(section('Tête d’angle', false,
      ...boiteImage('Image de la tête (cadrage carré)', (x) => x.tete, 'tete').slice(0, 1),
      coche('Afficher la tête', (x) => x.tete, 'afficher'),
      spec.tete.splash ? coche('Éclat en étoile', (x) => x.tete, 'etoile') : null,
      curseur('Zoom', (x) => x.tete, 'zoom', 0.2, 2.5, 0.01, 0.8),
      el('div', { class: 'rang' }, curseur('Décalage X', (x) => x.tete, 'x', -400, 1500, 1, -19), curseur('Décalage Y', (x) => x.tete, 'y', -400, 2150, 1, 232)),
      curseur('Rotation (°)', (x) => x.tete, 'rotation', -180, 180, 1, 0),
      c.tete.blob ? el('button', { class: 'btn petit', type: 'button', onclick: () => { ciblePointeur = 'tete'; majAide() } }, 'Déplacer à la souris') : null))
  }

  // options
  if (TYPES_SANS_FISSURES.has(c.type)) f.push(section('Options', false, coche('Fissures dans le cadre', (x) => x, 'fissures')))

  racine.append(...f)
  majAide()
}
function majAide() {
  const cible = { art: 'l’illustration', artDevant: 'le premier plan', tete: 'la tête d’angle' }[ciblePointeur]
  $('#aide-toile').textContent = `Glisse sur l’aperçu pour déplacer ${cible} (molette : zoom).`
}

// ---------------------------------------------------------------- liste
function majListe() {
  const l = $('#liste')
  l.replaceChildren(...projet.cartes.map((c) => {
    const b = el('button', { type: 'button', 'aria-current': String(c.id === projet.courante), onclick: () => choisir(c.id) },
      el('span', {}, c.contenu.titre || '(sans titre)'), el('small', {}, `${NOMS[c.type] ?? c.type} · ${c.langue.toUpperCase()}`))
    return b
  }))
}
function choisir(id) {
  projet.courante = id
  majListe()
  majBoutonsLangue()
  construireFormulaire()
  dessiner()
  sauvegarderPlusTard()
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
  for (const c of projet.cartes) {
    const copie = JSON.parse(JSON.stringify({ ...c, art: { ...c.art, blob: null }, artDevant: { ...c.artDevant, blob: null }, tete: { ...c.tete, blob: null } }))
    copie.art.image = c.art.blob ? await blobVersDataUrl(c.art.blob) : null
    copie.artDevant.image = c.artDevant.blob ? await blobVersDataUrl(c.artDevant.blob) : null
    copie.tete.image = c.tete.blob ? await blobVersDataUrl(c.tete.blob) : null
    cartes.push(copie)
  }
  telecharger(new Blob([JSON.stringify({ format: 'createur-cartes', version: 1, cartes })], { type: 'application/json' }), 'cartes.json')
}
async function importerProjet(fichier) {
  const j = JSON.parse(await fichier.text())
  if (j.format !== 'createur-cartes') throw new Error('fichier inconnu')
  for (const c of j.cartes) {
    for (const k of ['art', 'artDevant', 'tete']) {
      c[k].blob = c[k].image ? await dataUrlVersBlob(c[k].image) : null
      delete c[k].image
    }
    if (!TYPES[c.type]) continue
    c.id = nouvelId()
    projet.cartes.push(c)
  }
  if (projet.cartes.length) choisir(projet.cartes[projet.cartes.length - 1].id)
}

// ---------------------------------------------------------------- souris sur l'apercu
function brancherToile() {
  const toile = $('#toile')
  let depart = null
  const cible = () => {
    const c = carte()
    return ciblePointeur === 'tete' ? c.tete : ciblePointeur === 'artDevant' ? c.artDevant : c.art
  }
  toile.addEventListener('pointerdown', (e) => {
    const c = carte()
    if (!c || !cible().blob && ciblePointeur !== 'tete') return
    depart = { x: e.clientX, y: e.clientY, ox: cible().x, oy: cible().y }
    toile.setPointerCapture(e.pointerId)
    toile.classList.add('glisse')
  })
  toile.addEventListener('pointermove', (e) => {
    if (!depart) return
    const k = toile.width / toile.getBoundingClientRect().width
    const o = cible()
    // une carte paysage est dessinee dans son repere : le glisser suit l'ecran
    o.x = Math.round(depart.ox + (e.clientX - depart.x) * k)
    o.y = Math.round(depart.oy + (e.clientY - depart.y) * k)
    changement()
  })
  const fin = () => {
    if (depart) construireFormulaire()
    depart = null
    toile.classList.remove('glisse')
  }
  toile.addEventListener('pointerup', fin)
  toile.addEventListener('pointercancel', fin)
  toile.addEventListener('wheel', (e) => {
    const c = carte()
    if (!c || (!cible().blob && ciblePointeur !== 'tete')) return
    e.preventDefault()
    const o = cible()
    o.zoom = Math.max(0.2, Math.min(4, o.zoom * (e.deltaY < 0 ? 1.05 : 1 / 1.05)))
    changement()
    clearTimeout(brancherToile.t)
    brancherToile.t = setTimeout(construireFormulaire, 300)
  }, { passive: false })
  // glisser-deposer d'une image sur l'apercu
  toile.addEventListener('dragover', (e) => e.preventDefault())
  toile.addEventListener('drop', (e) => {
    e.preventDefault()
    const f = [...e.dataTransfer.files].find((x) => x.type.startsWith('image/'))
    const c = carte()
    if (!f || !c) return
    cible().blob = f
    changement()
    construireFormulaire()
  })
}

// ---------------------------------------------------------------- demarrage
async function demarrer() {
  const [types, palettes] = await Promise.all([
    fetch(BASE + 'donnees/types.json').then((r) => r.json()),
    fetch(BASE + 'donnees/palettes.json').then((r) => r.json()),
    chargerPolices(BASE + 'polices/'),
    chargerTraits(BASE + 'donnees/'),
  ]).then((r) => [r[0], r[1]])
  TYPES = types
  PALETTES = palettes
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
  else projet = { cartes: [nouvelleCarte('ally', 'fr')], courante: null }
  projet.cartes = projet.cartes.filter((c) => TYPES[c.type])
  if (!projet.cartes.length) projet.cartes = [nouvelleCarte('ally', 'fr')]
  if (!projet.cartes.some((c) => c.id === projet.courante)) projet.courante = projet.cartes[0].id

  $('#lang-fr').addEventListener('click', () => changerLangue('fr'))
  $('#lang-en').addEventListener('click', () => changerLangue('en'))
  $('#c-nouvelle').addEventListener('click', () => ajouter(nouvelleCarte(carte()?.type ?? 'ally', carte()?.langue ?? 'fr')))
  $('#c-dupliquer').addEventListener('click', () => {
    const c = carte()
    const copie = { ...JSON.parse(JSON.stringify({ ...c, art: { ...c.art, blob: null }, artDevant: { ...c.artDevant, blob: null }, tete: { ...c.tete, blob: null } })), id: nouvelId() }
    copie.art.blob = c.art.blob
    copie.artDevant.blob = c.artDevant.blob
    copie.tete.blob = c.tete.blob
    copie.contenu.titre += ' (copie)'
    ajouter(copie)
  })
  $('#c-supprimer').addEventListener('click', () => {
    const c = carte()
    if (!c || !confirm(`Supprimer « ${c.contenu.titre || 'cette carte'} » ?`)) return
    projet.cartes = projet.cartes.filter((x) => x.id !== c.id)
    if (!projet.cartes.length) projet.cartes.push(nouvelleCarte('ally', c.langue))
    choisir(projet.cartes[0].id)
  })
  $('#b-export').addEventListener('click', () => exporter(false))
  $('#b-export-2').addEventListener('click', () => exporter(true))
  $('#b-print').addEventListener('click', planchePourImprimer)
  $('#b-tts').addEventListener('click', plancheTTS)
  $('#p-exporter').addEventListener('click', exporterProjet)
  $('#p-importer').addEventListener('click', () => $('#p-fichier').click())
  $('#p-fichier').addEventListener('change', async (e) => {
    try { await importerProjet(e.target.files[0]) } catch (err) { message('Ouverture impossible : ' + err.message) }
    e.target.value = ''
  })
  brancherToile()
  choisir(projet.courante)
}
demarrer().catch((e) => message('Démarrage impossible : ' + e.message))
