// La page « Traduction » de MC Creator : un outil AUTONOME (sans lien avec le catalogue du jeu, aucun card_id, aucune
// table de traductions existante) pour qu'un traducteur dépose des scans anglais, efface vraiment leurs lettres
// imprimées et tape son propre texte (n'importe quelle langue) avec le moteur de texte du créateur de cartes.
//
// Pourquoi une page séparée plutôt qu'une vue de plus dans app.js : app.js est un gros state-machine (un seul
// « projet » de cartes, historique, synchronisation serveur...) pensé pour UN SEUL document à la fois. Cet outil-ci
// gère une FILE de scans indépendants, sans rapport avec un « projet » de dossier/carte : le greffer dans app.js aurait
// forcé à inventer un faux « type de carte » de projet juste pour l'y faire rentrer, avec le risque de régresser
// l'éditeur existant. On reste donc dans le même dossier (mêmes styles, mêmes modules texte.js/polices.js/zip.js), avec
// son propre stockage (stockage-traduction.js, base IndexedDB séparée) et un lien depuis l'accueil du créateur.
//
// Briques réutilisées SANS modification de leur logique :
//  - effacer-texte.js / detecter-zone.js : ports fidèles de ui-app/src/board/{effacer-texte,traduction-posee}.ts.
//  - texte.js / polices.js : le moteur de texte riche (mini-HTML, icônes ChampionsIcons, réduction auto) des cartes.
//  - zip.js : l'écrivain .zip déjà utilisé par l'export de pack.
//  - donnees/types.json : les gabarits de carte. Trois zones par carte, chacune ajustable à la souris :
//    1. « règles » (zone jaune) : position trouvée par détection de pixels (detecter-zone.js), comme avant.
//    2. « titre » (zone verte) et « type » (zone magenta, le mot « UPGRADE »/« ALLY »...) : leur position de départ
//       vient directement de la boîte mesurée de l'élément `title`/`typestr` du type choisi (carte.js s'en sert pour
//       dessiner ces mêmes mots sur une carte générée). Certains types impriment le titre much tourné de 90°
//       (Upgrade, Attachment, Promo verticale, et les quatre manigances : leur élément `header` porte sa propre
//       rotation, carte.js `appliquerChaine`) : on ne rejoue pas ce calcul de transformation ici (trop fragile sans
//       rendu de test), ces types-là retombent sur un rectangle générique horizontal, à ajuster à la main — le
//       `typestr` (libellé du type), lui, n'est JAMAIS tourné sur les cartes portrait : sa position de gabarit est
//       fiable pour tous les types portrait, Upgrade compris.
import { $, el, nouvelId } from './commun.js'
import { analyser, ajuster, mettreEnPage, dessinerPage } from './texte.js'
import { ICONES, chargerPolices } from './polices.js'
import { effacerTexte } from './effacer-texte.js'
import { detecterZoneTexte, detecterZoneSurFondTeinte, detecterZoneTextePaysage, prolongerLaZone } from './detecter-zone.js'
import { creerZip } from './zip.js'
import { listerCartes, sauvegarderCarte, supprimerCarte, sauvegarderOrdre } from './stockage-traduction.js'

// ------------------------------------------------------------------ les types de carte connus (donnees/types.json)
// Copié de app.js (GROUPES / NOMS) : une liste stable, dupliquée ici pour ne pas importer tout app.js (qui démarre son
// propre état au chargement et suppose ses propres éléments #vue-*). À tenir à jour si de nouveaux types apparaissent.
const GROUPES = [
  ['Héros', ['ally', 'event', 'upgrade', 'support', 'resource', 'alter-ego', 'identity', 'obligation', 'playersidescheme']],
  ['Vilains et rencontres', ['villain', 'minion', 'treachery', 'environment', 'attachment', 'sidescheme', 'main_scheme_a', 'main_scheme_b', 'obligation-villain']],
  ['Inserts (feuillets de campagne et de règles)', ['insert', 'insert-page']],
  ['Promos et paquet de départ', ['generic-promo', 'generic-promo-vert', 'alter-ego-promo', 'identity-promo', 'starter-deck']],
]
const NOMS = {
  insert: 'Insert (format carte)', 'insert-page': 'Insert (page A4)',
  ally: 'Allié', event: 'Événement', upgrade: 'Amélioration', support: 'Soutien', resource: 'Ressource', 'alter-ego': 'Alter-ego', identity: 'Identité de héros',
  obligation: 'Obligation (héros)', playersidescheme: 'Manigance annexe de joueur', villain: 'Méchant', minion: 'Sbire', treachery: 'Trahison',
  environment: 'Environnement', attachment: 'Attachement', sidescheme: 'Manigance annexe', main_scheme_a: 'Manigance principale (face A)',
  main_scheme_b: 'Manigance principale (face B)', 'obligation-villain': 'Obligation (rencontre)', 'generic-promo': 'Promo générique',
  'generic-promo-vert': 'Promo générique (verticale)', 'alter-ego-promo': 'Promo alter-ego', 'identity-promo': 'Promo héros', 'starter-deck': 'Paquet de départ',
}
// Manigances (cartes « paysage ») : le côté de leur boîte de texte (coteDuTexte, ui-app/src/board/traduction-carte.tsx).
const COTE_PAYSAGE = { main_scheme_a: 'gauche', main_scheme_b: 'gauche', sidescheme: 'droite', playersidescheme: 'droite' }
const estPaysage = (type) => Object.prototype.hasOwnProperty.call(COTE_PAYSAGE, type)

// Le mot réellement IMPRIMÉ dans le bandeau de type, PAS le nom du menu « Type de carte » (NOMS, ci-dessus) : une
// première version de cet outil préremplissait avec NOMS (ex. « Identité de héros »), confondant le nom que MC
// Creator donne à SON PROPRE choix de gabarit avec le mot effectivement imprimé sur la carte (« HÉROS ») — repéré
// par l'utilisateur sur une vraie carte FR officielle (Cyclope/Scott Summers). Repris de carte.js `LIBELLES.fr`
// (déjà la table utilisée pour IMPRIMER ce mot sur une carte générée par le créateur normal, donc déjà vérifiée),
// sauf `alter-ego`/`alter-ego-promo` : LIBELLES.fr dit « ALTER-EGO » (avec trait d'union), la vraie carte dit
// « ALTER EGO » (sans — vérifié au zoom sur la carte de référence). Les autres valeurs de LIBELLES.fr correspondent
// exactement aux mots anglais vérifiés sur de vrais scans (assets/pics) ci-dessous, d'où la confiance.
const LIBELLES_TYPE_IMPRIME = {
  ally: 'ALLIÉ', event: 'ÉVÉNEMENT', upgrade: 'AMÉLIORATION', support: 'SOUTIEN', resource: 'RESSOURCE', villain: 'MÉCHANT', minion: 'SBIRE',
  treachery: 'TRAHISON', environment: 'ENVIRONNEMENT', attachment: 'ATTACHEMENT', sidescheme: 'MANIGANCE ANNEXE', playersidescheme: 'MANIGANCE ANNEXE',
  main_scheme_a: 'MANIGANCE PRINCIPALE', main_scheme_b: 'MANIGANCE PRINCIPALE', 'alter-ego': 'ALTER EGO', 'alter-ego-promo': 'ALTER EGO',
  identity: 'HÉROS', 'identity-promo': 'HÉROS', obligation: 'OBLIGATION', 'obligation-villain': 'OBLIGATION', 'generic-promo': 'ALLIÉ',
  'generic-promo-vert': 'ALLIÉ',
}

// La bande du bas des cartes Héros/Alter-ego (« HAND SIZE 5 / HIT POINTS 12 ») : seuls ces 4 types l'impriment.
const TYPES_AVEC_MAIN = new Set(['identity', 'alter-ego', 'identity-promo', 'alter-ego-promo'])
const mainPresente = (type) => TYPES_AVEC_MAIN.has(type)
const BASE_MAIN_DEFAUT = { famille: 'FuturaMedCond', tailleParLargeur: 0.024, poids: 'bold', style: 'normal', espacementParLargeur: 0, capsPetites: false, alignement: 'left', couleur: '#ffffff', majuscule: true }

// Les cartes imprimées ont un texte de règles ~19 % plus grand que le réglage par défaut du Card Maker de référence
// (mesuré sur une vraie carte : 70 px contre 59 px) — même constante que carte.js, pour une taille fidèle.
const TAILLE_REGLES_IMPRIMEE = 70 / 59
// Icônes proposées dans la barre d'outils du texte (sous-ensemble canonique de polices.js -> ICONES, sans les alias FR).
const ICONES_BARRE = ['energy', 'mental', 'physical', 'wild', 'star', 'acceleration', 'crisis', 'hazard', 'boost', 'per_hero', 'consequential', 'unique', 'infinity']
// Plus grande dimension du tampon de travail (perf + mémoire) : largement assez pour un export net.
const DIM_MAX = 2200
const MARGE = 0.012
// Zones dont la position de gabarit (types.json) n'est pas rejouée ici car leur boîte est TOURNÉE sur la vraie carte
// (le titre d'un Upgrade/Attachment/Promo verticale est imprimé à la verticale sur le bord gauche) : rectangle
// générique à la place, ajustable à la main. Connu et documenté : voir le commentaire d'en-tête.
const TYPES_TITRE_TOURNE = new Set(['upgrade', 'attachment', 'generic-promo-vert'])

// Les badges de stats (THW/ATK/DEF/REC) : types.json a un élément prévu pour recouvrir chacun (même classe
// `numberlabeloverwrite` que `typestr`), mais leur `cls` est COMPOSÉE (ex. « thwstr textstr numberlabeloverwrite »,
// pas juste « thwstr ») — boiteFractionDuChamp() doit chercher dans la liste des classes, pas l'égalité stricte.
// Abréviations FR officielles : ui-app/src/board/card-model.ts, table STATS_BASE (celle qui fait foi, pas inventée).
// SCH (« MNG ») n'a pas d'élément générique dans types.json (seulement `attachmentschstr`, propre aux nombres
// ATK/SCH des attachements — un autre champ, hors sujet ici) : aucun badge SCH à proposer pour l'instant.
const STATS = [
  { cls: 'thwstr', zoneCle: 'zoneThw', texteCle: 'texteThw', abrege: 'CTR', nom: 'THW → CTR' },
  { cls: 'atkstr', zoneCle: 'zoneAtk', texteCle: 'texteAtk', abrege: 'ATQ', nom: 'ATK → ATQ' },
  { cls: 'defstr', zoneCle: 'zoneDef', texteCle: 'texteDef', abrege: 'DEF', nom: 'DEF' },
  { cls: 'recstr', zoneCle: 'zoneRec', texteCle: 'texteRec', abrege: 'REC', nom: 'REC' },
]
// Police/couleur du badge : le style mesuré par types.json pour ces champs est inutilisable (polices système
// génériques, 16px — l'outil de mesure n'a visiblement pas capturé de vraie police ici, contrairement à `typestr`) ;
// en vrai, sur le scan, ces badges sont en texte BLANC sur fond sombre (vérifié visuellement, alors que le `color`
// mesuré dans types.json dit noir) — un style fixe, par analogie avec le libellé du type, est plus fiable ici.
// Alignement et poids mesurés à la main (THW/ATK, assets/pics/50002.jpg) : ces badges sont plus COMPACTS que le
// bandeau du type (une pointe de losange, pas un long fanion) et leur texte y est CENTRÉ (marges gauche/droite proches,
// ≈18/15 px sur ATK) — contrairement au libellé du type, à gauche. Pas de métadonnée de gabarit fiable ici (voir plus
// haut) : tout est fixé à la main d'après cette mesure.
const BASE_STAT_DEFAUT = { famille: 'FuturaMedCond', tailleParLargeur: 0.028, poids: 'bold', style: 'normal', espacementParLargeur: 0, capsPetites: false, alignement: 'center', couleur: '#ffffff', majuscule: true }

let TYPES = null
let cartes = []
let carteActiveId = null
let glisse = null
const minuteries = new Map() // carte.id -> timer de sauvegarde debouncee

// ------------------------------------------------------------------ demarrage
async function demarrer() {
  try {
    TYPES = await (await fetch('donnees/types.json')).json()
  } catch {
    TYPES = {}
  }
  cartes = (await listerCartes()).map((c) => ({ ...c, zone: c.zone ?? null, zoneTitre: c.zoneTitre ?? null, zoneType: c.zoneType ?? null }))
  construireSelectType()
  rendreListe()
  if (cartes.length) ouvrirCarte(cartes[0].id)
  else afficherAtelierVide()
  brancherEvenements()
  new ResizeObserver(() => positionnerRectangle(carteActive())).observe($('#toile'))
  void chargerPolices()
}

function construireSelectType() {
  const select = $('#type-carte')
  select.replaceChildren(
    el('option', { value: '' }, '— Générique (aucun gabarit) —'),
    ...GROUPES.map(([titre, types]) => el('optgroup', { label: titre }, ...types.map((t) => el('option', { value: t }, NOMS[t] ?? t))))
  )
}

// ------------------------------------------------------------------ file d'attente (liste a gauche)
function carteParId(id) {
  return cartes.find((c) => c.id === id)
}
function carteActive() {
  return carteActiveId ? carteParId(carteActiveId) : null
}

function ajouterFichiers(fichiers) {
  const nouvelles = []
  for (const f of fichiers) {
    if (!f.type || !f.type.startsWith('image/')) continue
    const carte = {
      id: nouvelId(), nom: f.name, blobOriginal: f, type: '',
      zone: null, sombre: false, texte: '',
      zoneTitre: null, texteTitre: '',
      zoneType: null, texteType: '',
      zoneThw: null, texteThw: '', zoneAtk: null, texteAtk: '', zoneDef: null, texteDef: '', zoneRec: null, texteRec: '',
      zoneMain: null, texteMain: '',
      effaceDataUrl: null,
    }
    cartes.push(carte)
    nouvelles.push(carte)
  }
  if (!nouvelles.length) return
  for (const c of nouvelles) void sauvegarderCarte(versPersistance(c))
  void sauvegarderOrdre(cartes.map((c) => c.id))
  rendreListe()
  if (!carteActiveId) ouvrirCarte(nouvelles[0].id)
}

function versPersistance(carte) {
  return {
    id: carte.id, nom: carte.nom, blobOriginal: carte.blobOriginal, type: carte.type,
    zone: carte.zone, sombre: carte.sombre, texte: carte.texte,
    zoneTitre: carte.zoneTitre, texteTitre: carte.texteTitre,
    zoneType: carte.zoneType, texteType: carte.texteType,
    zoneThw: carte.zoneThw, texteThw: carte.texteThw,
    zoneAtk: carte.zoneAtk, texteAtk: carte.texteAtk,
    zoneDef: carte.zoneDef, texteDef: carte.texteDef,
    zoneRec: carte.zoneRec, texteRec: carte.texteRec,
    zoneMain: carte.zoneMain, texteMain: carte.texteMain,
    effaceDataUrl: carte.effaceDataUrl,
  }
}

function planifierSauvegarde(carte) {
  clearTimeout(minuteries.get(carte.id))
  minuteries.set(
    carte.id,
    setTimeout(() => void sauvegarderCarte(versPersistance(carte)), 400)
  )
}

function rendreListe() {
  const liste = $('#liste')
  liste.replaceChildren(
    ...cartes.map((c) =>
      el(
        'div',
        { class: 'vignette' + (c.id === carteActiveId ? ' choisie' : ''), onclick: () => ouvrirCarte(c.id) },
        el('img', { src: URL.createObjectURL(c.blobOriginal), alt: '' }),
        el('div', { class: 'infos-vignette' },
          el('div', { class: 'nom-vignette' }, c.nom),
          el('div', { class: 'etat-vignette' }, [
            c.type ? (NOMS[c.type] ?? c.type) : 'Type non choisi',
            c.zone ? (c.effaceDataUrl ? ' · effacé' : ' · zone posée') : '',
          ].join(''))),
        el('button', { class: 'btn petit fixe', type: 'button', title: 'Télécharger ce PNG', onclick: (e) => { e.stopPropagation(); void exporterPng(c) } }, '⬇'),
        el('button', { class: 'btn petit fixe danger', type: 'button', title: 'Retirer de la liste', onclick: (e) => { e.stopPropagation(); void retirerCarte(c.id) } }, '✕')
      )
    )
  )
  $('#compte-liste').textContent = cartes.length ? `${cartes.length} carte(s)` : 'Aucun scan chargé.'
  $('#b-tout-telecharger').disabled = cartes.length === 0
}

async function retirerCarte(id) {
  cartes = cartes.filter((c) => c.id !== id)
  await supprimerCarte(id)
  if (carteActiveId === id) {
    carteActiveId = null
    if (cartes.length) ouvrirCarte(cartes[0].id)
    else afficherAtelierVide()
  }
  rendreListe()
}

function afficherAtelierVide() {
  $('#atelier').hidden = true
  $('#aide-vide').hidden = false
}

// ------------------------------------------------------------------ les trois zones (regles / titre / type) et leur position de depart
function zoneParDefaut(paysage, cote) {
  if (!paysage) return { x0: 0.09, y0: 0.56, x1: 0.91, y1: 0.86 }
  if (cote === 'droite') return { x0: 0.46, y0: 0.14, x1: 0.92, y1: 0.86 }
  return { x0: 0.08, y0: 0.14, x1: 0.54, y1: 0.86 }
}
function zoneTitreParDefaut(paysage, cote) {
  if (!paysage) return { x0: 0.08, y0: 0.025, x1: 0.92, y1: 0.095 }
  if (cote === 'droite') return { x0: 0.5, y0: 0.03, x1: 0.95, y1: 0.12 }
  return { x0: 0.05, y0: 0.03, x1: 0.5, y1: 0.12 }
}
function zoneTypeParDefaut(paysage, cote) {
  if (!paysage) return { x0: 0.04, y0: 0.1, x1: 0.5, y1: 0.16 }
  if (cote === 'droite') return { x0: 0.5, y0: 0.02, x1: 0.95, y1: 0.08 }
  return { x0: 0.05, y0: 0.02, x1: 0.5, y1: 0.08 }
}

/** Le chemin (l'élément et ses ancêtres, jusqu'à la racine) ne porte AUCUNE rotation/translation/mise à l'échelle
    propre (carte.js `appliquerChaine`) : la boîte mesurée est alors directement en pixels de la carte, sans calcul de
    transformation à rejouer. Les cartes paysage (manigances) sont tournées globalement : jamais « sans transform ». */
function cheminSansTransform(spec, el) {
  if (!spec || spec.paysage) return false
  const parId = new Map(spec.elements.map((e) => [e.i, e]))
  for (let e = el; e; e = e.parent === -1 ? null : parId.get(e.parent)) {
    if (e.rot || e.trn || e.scl || e.m) return false
  }
  return true
}
/** L'élément de ce type dont la classe (ex. « thwstr textstr numberlabeloverwrite ») CONTIENT `cls` — le gabarit
    donne plusieurs classes espacées par élément, pas toujours une seule (contrairement à « title »/« typestr »). */
function trouverChamp(spec, cls) {
  return spec?.elements?.find((e) => e.cls.split(' ').includes(cls))
}
function statPresente(type, cls) {
  return !!trouverChamp(type ? TYPES?.[type] : null, cls)
}
/** Les badges de stats que ce type imprime réellement (ex. "ally" -> thw+atk, "alter-ego" -> rec seul). */
function statsActives(type) {
  return STATS.filter((s) => statPresente(type, s.cls))
}
/** La boîte mesurée (carte.js/types.json) d'un champ (« title », « typestr », « thwstr »...), en fractions de la
    carte — seulement quand elle est fiable sans rejouer de rotation (voir cheminSansTransform et TYPES_TITRE_TOURNE). */
// Marge ajoutée au rectangle de départ lu dans le gabarit : mesurée sur LE Card Maker de référence, elle tombe souvent
// 1 à 2 % de la hauteur de la carte trop haute ou trop basse sur un scan réel (autre tirage, autre résolution de
// référence) — constaté avec effacerTexte lui-même pendant les essais (texte alors coupé, aucune lettre trouvée).
// Une PETITE marge aide sans texte coupé ; une marge trop généreuse peut au contraire inclure le coin coupé décoratif
// du bandeau du titre (une grande tache qui trouble le regroupement en lignes d'effacerTexte) — constaté aussi en
// essai. D'où une marge modeste : elle n'élimine pas tous les cas, le rectangle reste ajustable à la main.
const MARGE_CHAMP_GABARIT = 0.012
function boiteFractionDuChamp(type, cls) {
  const spec = type ? TYPES?.[type] : null
  const champ = trouverChamp(spec, cls)
  if (!champ || !cheminSansTransform(spec, champ)) return null
  if (cls === 'title' && TYPES_TITRE_TOURNE.has(type)) return null
  const mx = MARGE_CHAMP_GABARIT * spec.largeur
  const my = MARGE_CHAMP_GABARIT * spec.hauteur
  return {
    x0: Math.max(0, (champ.boite[0] - mx)) / spec.largeur,
    y0: Math.max(0, (champ.boite[1] - my)) / spec.hauteur,
    x1: Math.min(spec.largeur, champ.boite[0] + champ.boite[2] + mx) / spec.largeur,
    y1: Math.min(spec.hauteur, champ.boite[1] + champ.boite[3] + my) / spec.hauteur,
  }
}
function zoneTitreInitiale(type) {
  return boiteFractionDuChamp(type, 'title') ?? zoneTitreParDefaut(estPaysage(type), COTE_PAYSAGE[type])
}
function zoneTypeInitiale(type) {
  return boiteFractionDuChamp(type, 'typestr') ?? zoneTypeParDefaut(estPaysage(type), COTE_PAYSAGE[type])
}
/** Position par défaut d'un badge de stat quand le gabarit n'est pas exploitable (type générique, ou carte paysage) :
    empilés le long du bord gauche, dans l'ordre THW/ATK/DEF/REC. */
function zoneStatParDefaut(index) {
  const y0 = 0.27 + index * 0.1
  return { x0: 0.02, y0, x1: 0.24, y1: y0 + 0.075 }
}
function zoneStatInitiale(type, cls, index) {
  return boiteFractionDuChamp(type, cls) ?? zoneStatParDefaut(index)
}
/** La bande « HAND SIZE n / HIT POINTS n » : `identity-promo`/`alter-ego-promo` ont CHACUN un élément séparé pour
    chaque moitié (`handtext`, `hptext`, rien à voir avec les nombres eux-mêmes, cls `handsize`/`hp cost`) — on fait
    l'union des deux boîtes pour une SEULE zone (un traducteur tape « Taille de main 5 / Points de vie 10 » d'un
    coup). `identity`/`alter-ego` (non-promo) n'ont AUCUN élément prévu ici : rectangle générique, mesuré à la main
    sur un vrai scan (assets/pics/01010a.jpg : la bande est tout en bas, juste au-dessus du filet, x≈[0,0.78]). */
function boiteFractionMain(type) {
  const spec = type ? TYPES?.[type] : null
  const ht = trouverChamp(spec, 'handtext')
  const pt = trouverChamp(spec, 'hptext')
  if (!ht || !pt || !cheminSansTransform(spec, ht) || !cheminSansTransform(spec, pt)) return null
  const x0 = Math.min(ht.boite[0], pt.boite[0])
  const y0 = Math.min(ht.boite[1], pt.boite[1])
  const x1 = Math.max(ht.boite[0] + ht.boite[2], pt.boite[0] + pt.boite[2])
  const y1 = Math.max(ht.boite[1] + ht.boite[3], pt.boite[1] + pt.boite[3])
  const mx = MARGE_CHAMP_GABARIT * spec.largeur
  const my = MARGE_CHAMP_GABARIT * spec.hauteur
  return {
    x0: Math.max(0, x0 - mx) / spec.largeur,
    y0: Math.max(0, y0 - my) / spec.hauteur,
    x1: Math.min(spec.largeur, x1 + mx) / spec.largeur,
    y1: Math.min(spec.hauteur, y1 + my) / spec.hauteur,
  }
}
function zoneMainParDefaut() {
  return { x0: 0.02, y0: 0.915, x1: 0.78, y1: 0.975 }
}
function zoneMainInitiale(type) {
  return boiteFractionMain(type) ?? zoneMainParDefaut()
}

// ------------------------------------------------------------------ ouverture d'une carte dans l'atelier
function ouvrirCarte(id) {
  carteActiveId = id
  const carte = carteParId(id)
  if (!carte) return afficherAtelierVide()
  $('#aide-vide').hidden = true
  $('#atelier').hidden = false
  $('#type-carte').value = carte.type || ''
  $('#ch-sombre').checked = !!carte.sombre
  $('#texte-fr').value = carte.texte || ''
  $('#titre-fr').value = carte.texteTitre || ''
  $('#type-fr').value = carte.texteType || ''
  $('#info-zone').textContent = carte._detectionMessage || ''
  if (!carte.zone) {
    carte.zone = zoneParDefaut(estPaysage(carte.type), COTE_PAYSAGE[carte.type])
    carte._zoneAuto = false
  }
  if (!carte.zoneTitre) carte.zoneTitre = zoneTitreInitiale(carte.type)
  if (!carte.zoneType) carte.zoneType = zoneTypeInitiale(carte.type)
  for (const [i, s] of statsActives(carte.type).entries()) {
    if (!carte[s.zoneCle]) carte[s.zoneCle] = zoneStatInitiale(carte.type, s.cls, i)
    if (!carte[s.texteCle]) carte[s.texteCle] = s.abrege
  }
  if (mainPresente(carte.type)) {
    if (!carte.zoneMain) carte.zoneMain = zoneMainInitiale(carte.type)
    if (!carte.texteMain) carte.texteMain = 'Taille de main / Points de vie'
  }
  $('#champ-main').hidden = !mainPresente(carte.type)
  $('#main-fr').value = carte.texteMain || ''
  construireChampsStats(carte)
  rendreListe()
  void dessinerCarte(carte)
}

/** Un champ texte + son étiquette par badge de stat RÉELLEMENT présent sur ce type (thw/atk/def/rec) — la liste
    change avec le type choisi, reconstruite ici plutôt que figée dans le HTML. */
function construireChampsStats(carte) {
  const conteneur = $('#stats-champs')
  const actives = statsActives(carte.type)
  conteneur.replaceChildren(
    ...actives.map((s) =>
      el(
        'label',
        {},
        `Badge ${s.nom}`,
        el('input', {
          type: 'text', value: carte[s.texteCle] || '',
          oninput: (e) => {
            const c = carteActive()
            if (!c) return
            c[s.texteCle] = e.target.value
            clearTimeout(c._debounceStat)
            c._debounceStat = setTimeout(() => void dessinerCarte(c), 120)
            planifierSauvegarde(c)
          },
        })
      )
    )
  )
}

// ------------------------------------------------------------------ canevas (chargement, rotation paysage, cache)
function chargerImageDepuisUrl(src) {
  return new Promise((ok, ko) => {
    const image = new Image()
    image.onload = () => ok(image)
    image.onerror = ko
    image.src = src
  })
}

/** Construit (une fois, mis en cache sur la carte) le canevas d'ORIGINE : le scan, réduit si besoin, tourné de 90°
    si c'est une manigance scannée debout (comme zoneDuScan de TraductionPosee.tsx). Reconstruit si le type a changé
    l'orientation attendue. */
async function obtenirCanvasOriginal(carte) {
  const paysageAttendu = estPaysage(carte.type)
  if (carte._canvasOriginal && carte._paysageDuCanvas === paysageAttendu) return carte._canvasOriginal
  const url = URL.createObjectURL(carte.blobOriginal)
  let image
  try {
    image = await chargerImageDepuisUrl(url)
  } finally {
    URL.revokeObjectURL(url)
  }
  const imagePaysage = image.naturalWidth > image.naturalHeight
  const tourner = paysageAttendu && !imagePaysage
  const reduction = Math.min(1, DIM_MAX / Math.max(image.naturalWidth, image.naturalHeight))
  const li = Math.max(1, Math.round(image.naturalWidth * reduction))
  const hi = Math.max(1, Math.round(image.naturalHeight * reduction))
  const [L, H] = tourner ? [hi, li] : [li, hi]
  const c = document.createElement('canvas')
  c.width = L
  c.height = H
  const ctx = c.getContext('2d', { willReadFrequently: true })
  if (tourner) {
    ctx.translate(L, 0)
    ctx.rotate(Math.PI / 2)
    ctx.drawImage(image, 0, 0, H, L)
  } else {
    ctx.drawImage(image, 0, 0, L, H)
  }
  carte._canvasOriginal = c
  carte._paysageDuCanvas = paysageAttendu
  carte._canvasTravail = null // l'original a change de forme : le fond nettoye (s'il y en avait un) n'est plus valide
  if (carte.effaceDataUrl) {
    try {
      const img2 = await chargerImageDepuisUrl(carte.effaceDataUrl)
      const t = document.createElement('canvas')
      t.width = L
      t.height = H
      t.getContext('2d').drawImage(img2, 0, 0, L, H)
      carte._canvasTravail = t
    } catch {
      carte.effaceDataUrl = null
    }
  }
  return c
}
function canvasDeFond(carte) {
  return carte._canvasTravail || carte._canvasOriginal
}

// ------------------------------------------------------------------ detection de la zone de regles (pixels)
async function detecterZoneAuto() {
  const carte = carteActive()
  if (!carte) return
  const original = await obtenirCanvasOriginal(carte)
  const L = original.width
  const H = original.height
  const pixels = original.getContext('2d', { willReadFrequently: true }).getImageData(0, 0, L, H).data
  const paysage = estPaysage(carte.type)
  let zone = null
  if (paysage) {
    const cote = COTE_PAYSAGE[carte.type]
    zone = detecterZoneTextePaysage(pixels, L, H, cote)
    if (zone) zone = prolongerLaZone(zone, pixels, L, H)
  } else {
    zone = detecterZoneTexte(pixels, L, H) ?? detecterZoneSurFondTeinte(pixels, L, H)
  }
  if (zone) {
    carte.zone = { x0: zone.x0, y0: zone.y0, x1: zone.x1, y1: zone.y1 }
    carte.sombre = luma(zone.fond) < 128
    carte._zoneAuto = true
    carte._detectionMessage = 'Zone de règles détectée automatiquement — vérifie qu’elle couvre bien tout le texte, ajuste au besoin.'
  } else {
    carte.zone = zoneParDefaut(paysage, COTE_PAYSAGE[carte.type])
    carte._zoneAuto = false
    carte._detectionMessage = '⚠ Détection automatique impossible sur ce scan : rectangle de règles posé au hasard, ajuste-le à la main.'
  }
  carte._canvasTravail = null
  carte.effaceDataUrl = null
  carte._cadreTexte = null
  $('#ch-sombre').checked = !!carte.sombre
  $('#info-zone').textContent = carte._detectionMessage
  await dessinerCarte(carte)
  planifierSauvegarde(carte)
}
function luma([r, g, b]) {
  return 0.299 * r + 0.587 * g + 0.114 * b
}

// ------------------------------------------------------------------ effacement du texte anglais (les trois zones)
async function effacerZoneActive() {
  const carte = carteActive()
  if (!carte) return
  const original = await obtenirCanvasOriginal(carte)
  const L = original.width
  const H = original.height
  const travail = document.createElement('canvas')
  travail.width = L
  travail.height = H
  const ctxT = travail.getContext('2d')
  ctxT.drawImage(original, 0, 0)
  const ctxO = original.getContext('2d', { willReadFrequently: true })
  // Règles : fond clair/sombre choisi par la case à cocher. Titre : encre noire sur le gabarit (types.json), jamais
  // cochée. Libellé du type (« UPGRADE »...) : toujours blanc sur bandeau teinté (types.json, tous les types vérifiés).
  // `boost` (option déjà publique d'effacerTexte, sa LOGIQUE n'est pas touchée) : le titre est dans une police bien
  // plus grasse et plus grande que le texte de règles — la fermeture calibrée sur les règles (rayon ≈ 1,3 % de la
  // largeur de la carte) la traverse sans l'effacer, confirmé en essai (cadre introuvable à boost=1, trouvé dès 1,1).
  // Un boost modéré (1,3) couvre cette marge sans jamais revenir en arrière sur la zone de règles, elle, inchangée.
  //
  // `gommePleine` (5e valeur) : titre/type/badges/« taille de main » sont des rectangles ÉTROITS qu'on vient de poser
  // sur UN mot/une courte expression — contrairement aux règles (plusieurs lignes, l'illustration peut mordre sur les
  // bords), rien d'autre qu'une encre à enlever n'y est attendu. On y passe alors tout le rectangle en `gommes`
  // (option déjà publique d'effacerTexte : « toute encre, même pâle » — sans dépendre de la reconnaissance en LIGNES
  // de lettres). Nécessaire : un titre à trait d'union (« SPIDER-MAN », assets/pics/01001a.jpg) a un si grand blanc
  // autour du tiret que cadreDesLettres n'enchaîne pas « SPIDER » et « -MAN » dans la MÊME ligne — seul « SPIDER »
  // était effacé, « -MAN » anglais restait sous le françvais, repéré sur l'export final (pas seulement l'aperçu).
  // Les badges THW/ATK/DEF, eux, échouaient carrément à trouver une ligne sur certains scans (zone pourtant bien
  // cadrée) : `gommes` les efface quand même, sans dépendre de cette reconnaissance.
  const zones = [
    ['Règles', carte.zone, carte.sombre, 1, false],
    ['Titre', carte.zoneTitre, false, 1.3, true],
    ['Type', carte.zoneType, true, 1, true],
    ...statsActives(carte.type).map((s) => [s.nom, carte[s.zoneCle], true, 1, true]),
    ...(mainPresente(carte.type) ? [['Taille de main / PV', carte.zoneMain, true, 1, true]] : []),
  ].filter(([, zoneFrac]) => zoneFrac)
  const messages = []
  let dernierCadre = null
  for (const [nom, zoneFrac, sombre, boost, gommePleine] of zones) {
    const x = Math.max(0, Math.round(zoneFrac.x0 * L))
    const y = Math.max(0, Math.round(zoneFrac.y0 * H))
    const largeurZone = Math.min(L - x, Math.max(1, Math.round(zoneFrac.x1 * L) - x))
    const hauteurZone = Math.min(H - y, Math.max(1, Math.round(zoneFrac.y1 * H) - y))
    const region = ctxO.getImageData(x, y, largeurZone, hauteurZone)
    const options = optionsEffacement(L, H, sombre, boost)
    if (gommePleine) options.gommes = [{ x0: 0, y0: 0, x1: largeurZone, y1: hauteurZone }]
    const cadre = effacerTexte(region.data, largeurZone, hauteurZone, options)
    ctxT.putImageData(region, x, y)
    if (nom === 'Règles') dernierCadre = cadre
    if (gommePleine) messages.push(`${nom} : effacé.`)
    else messages.push(cadre ? `${nom} : ${cadre.lignes} ligne(s) effacée(s).` : `${nom} : ⚠ rien de reconnu, vérifie le cadrage.`)
  }
  carte._canvasTravail = travail
  carte._cadreTexte = dernierCadre
  carte.effaceDataUrl = travail.toDataURL('image/png')
  $('#info-zone').textContent = messages.join(' ')
  await dessinerCarte(carte)
  rendreListe()
  planifierSauvegarde(carte)
}
function optionsEffacement(largeurTravail, hauteurTravail, sombre, boost = 1) {
  return {
    largeurCarte: Math.min(largeurTravail, hauteurTravail) * boost,
    hauteurCarte: Math.max(largeurTravail, hauteurTravail) * boost,
    sombre,
    margeHaut: Math.round(MARGE * hauteurTravail),
    margeBas: Math.round(MARGE * hauteurTravail),
    margeCote: Math.round((MARGE + 0.012) * Math.min(largeurTravail, hauteurTravail)),
  }
}

// ------------------------------------------------------------------ mise en forme et rendu du texte traduit
/** Le style (police, taille, interligne...) du champ « règles » du gabarit du type choisi, ramené à la largeur du
    tampon de travail — le texte tapé a alors la même taille et la même police que l'anglais qu'il remplace. Générique
    sans type choisi (formule de TraductionPosee.tsx : ~4,3 % de la largeur de la carte). */
function construireBase(type, largeurTravail) {
  const spec = type ? TYPES?.[type] : null
  const champ = spec?.elements?.find((e) => e.cls === 'rules')
  if (!spec || !champ) {
    const taille = largeurTravail * 0.043
    return { famille: 'AvenirNext', taille, interligne: taille * 1.18, poids: 'normal', style: 'normal', espacement: 0, capsPetites: false, alignement: 'left' }
  }
  const echelle = largeurTravail / spec.largeur
  const s = champ.style
  const tailleNative = parseFloat(s.fontSize) || 50
  const interligneNative = s.lineHeight && s.lineHeight !== 'normal' ? parseFloat(s.lineHeight) : tailleNative * 1.2
  return {
    famille: (s.fontFamily || 'AvenirNext').split(',')[0].replace(/["']/g, '').trim(),
    taille: tailleNative * echelle * TAILLE_REGLES_IMPRIMEE,
    interligne: interligneNative * echelle * TAILLE_REGLES_IMPRIMEE,
    poids: s.fontWeight === '400' ? 'normal' : s.fontWeight,
    style: s.fontStyle,
    espacement: (parseFloat(s.letterSpacing) || 0) * echelle,
    capsPetites: s.fontVariant === 'small-caps',
    alignement: s.textAlign === 'center' ? 'center' : 'left',
  }
}
/** Même principe pour le titre (champ « title ») et le libellé du type (champ « typestr ») : la police vient toujours
    du gabarit mesuré (même quand sa POSITION, elle, n'est pas réutilisée — voir boiteFractionDuChamp). */
// Poids : la carte imprimée est nettement plus GRASSE que le poids mesuré (« 400 », normal) ne le laisse croire — vu
// en comparant un rendu réel à côté du scan (assets/pics/50002.jpg, 01041.jpg, 10013.jpg) : la même famille FuturaMedCond
// en graisse « normal » reste visiblement plus fine que l'anglais imprimé, la version « bold » (gras SYNTHÉTIQUE du
// navigateur, un seul fichier de police est chargé pour cette famille) colle, elle, au bon poids. Comme pour la
// couleur des badges de stats (déjà documentée plus bas), le `fontWeight` mesuré par l'outil de référence n'est pas
// fiable ici : on l'ignore et on force « bold ».
function construireBaseLigne(type, cls, defaut) {
  const spec = type ? TYPES?.[type] : null
  const champ = spec?.elements?.find((e) => e.cls === cls)
  if (!spec || !champ) return defaut
  const echelle = 1 / spec.largeur // rapporté a` 1 ; multiplie par la largeur de travail au moment du dessin
  const s = champ.style
  const tailleNative = parseFloat(s.fontSize) || defaut.taille
  return {
    famille: (s.fontFamily || defaut.famille).split(',')[0].replace(/["']/g, '').trim(),
    tailleParLargeur: tailleNative * echelle,
    poids: 'bold',
    style: s.fontStyle,
    espacementParLargeur: (parseFloat(s.letterSpacing) || 0) * echelle,
    capsPetites: s.fontVariant === 'small-caps',
    // ATTENTION, vérifié sur 3 scans officiels réels (01041 Shuri, 10013 She-Hulk, 50002 Nick Fury) : le libellé du
    // type n'est PAS centré dans son bandeau, il est bien à GAUCHE (marge gauche ≈ 9-18 px, marge droite ≈ 41-82 px,
    // mesuré au pixel) — `textAlign: start` du gabarit dit donc vrai ici, contrairement à son `color`/`fontFamily`
    // (fiables, eux, voir plus bas) : NE PAS changer cette ligne en « center » sans une nouvelle mesure au pixel sur
    // un scan réel, une fausse « correction » ferait régresser un rendu qui est déjà conforme aux cartes imprimées.
    alignement: s.textAlign === 'center' ? 'center' : s.textAlign === 'right' ? 'right' : 'left',
    couleur: s.color || defaut.couleur,
    majuscule: s.textTransform === 'uppercase',
  }
}
const BASE_TITRE_DEFAUT = { famille: 'Exo2Mod', tailleParLargeur: 0.065, poids: '700', style: 'normal', espacementParLargeur: 0, capsPetites: true, alignement: 'center', couleur: '#111111', majuscule: false }
const BASE_TYPE_DEFAUT = { famille: 'FuturaMedCond', tailleParLargeur: 0.034, poids: 'bold', style: 'normal', espacementParLargeur: 0, capsPetites: false, alignement: 'left', couleur: '#ffffff', majuscule: true }
// Marge intérieure (fraction de la largeur de la boîte) côté aligné : sur le scan, le mot ne touche jamais le bord du
// bandeau/badge — mesuré ≈ 12 % de la largeur de la boîte côté gauche sur « ALLY » (3 scans). Sans cette marge, le
// texte « gauche » touchait le bord gauche EXACT de la boîte (x=0), plus près du bord que sur une vraie carte. Centré
// : la marge est retirée symétriquement des deux côtés, donc sans effet sur le centrage lui-même.
const MARGE_INTERIEURE_LIGNE = 0.1

function dessinerTexteSurCanvas(ctx, carte, L, H) {
  const z = carte.zone
  if (!z || !carte.texte || !carte.texte.trim()) return
  const xpx = z.x0 * L
  const ypx = z.y0 * H
  const lpx = Math.max(10, (z.x1 - z.x0) * L)
  const hpx = Math.max(10, (z.y1 - z.y0) * H)
  const base = construireBase(carte.type, L)
  const jetons = analyser(carte.texte)
  ctx.save()
  ctx.beginPath()
  ctx.rect(xpx, ypx, lpx, hpx)
  ctx.clip()
  ctx.translate(xpx, ypx)
  const { facteur, page } = ajuster(ctx, jetons, base, lpx, hpx, 0.45)
  const couleur = carte.sombre ? '#f2f2f2' : '#111111'
  dessinerPage(ctx, page, base, lpx, facteur, couleur, base.alignement || 'left')
  ctx.restore()
}

/** Titre et libellé du type : une seule ligne, centrée en hauteur dans sa boîte, réduite si trop large pour tenir —
    même technique que `dessinerLigne` de carte.js (l'interligne = la hauteur de la boîte centre le texte). */
function dessinerLigneSurCanvas(ctx, zoneFrac, texteBrut, baseParLargeur, L, H) {
  if (!zoneFrac || !texteBrut || !texteBrut.trim()) return
  const xpx = zoneFrac.x0 * L
  const ypx = zoneFrac.y0 * H
  const lpx = Math.max(10, (zoneFrac.x1 - zoneFrac.x0) * L)
  const hpx = Math.max(10, (zoneFrac.y1 - zoneFrac.y0) * H)
  const base = {
    famille: baseParLargeur.famille,
    taille: baseParLargeur.tailleParLargeur * L,
    interligne: hpx,
    poids: baseParLargeur.poids,
    style: baseParLargeur.style,
    espacement: baseParLargeur.espacementParLargeur * L,
    capsPetites: baseParLargeur.capsPetites,
    alignement: baseParLargeur.alignement,
  }
  const transforme = baseParLargeur.majuscule ? texteBrut.toUpperCase() : texteBrut
  const jetons = analyser(transforme).filter((j) => j.t !== 'saut' && j.t !== 'para')
  // Même calcul que dessinerLigne (carte.js) : TOUJOURS une seule ligne (largeur « 1e6 », jamais lpx, donc jamais de
  // retour à la ligne), le facteur de réduction est le ratio exact largeur de boîte / largeur du texte (sans plancher
  // — un plancher comme 0.3 laissait passer un mot encore trop large, qui retournait alors à la ligne et se cassait
  // en deux, ex. « ALTER-EGO » -> « ALT »/« EGO », constaté en test). Le décalage x (gauche/centre/droite) est
  // calculé à la main sur la largeur RÉELLE de la ligne obtenue, puis `dessinerPage` dessine en 'left' à cet endroit
  // — centrer ou aligner à droite dans `dessinerPage` lui-même n'aurait eu aucun effet puisque sa boîte de référence
  // (`largeur`) doit alors valoir exactement la largeur du texte, pas celle, plus grande, du rectangle.
  // Marge intérieure côté(s) aligné(s) (voir MARGE_INTERIEURE_LIGNE) : le texte ne doit ni toucher le bord de la
  // boîte (gauche/droite) ni déborder ailleurs qu'avant — donc on réduit la largeur DISPONIBLE pour le calcul du
  // facteur de réduction en même temps que l'on décale le départ, plutôt que de rajouter la marge après coup (qui
  // laisserait un mot encore trop grand déborder du bandeau réel).
  const marge = lpx * MARGE_INTERIEURE_LIGNE
  const lpxUtile = Math.max(10, lpx - marge)
  let facteur = 1
  let page = mettreEnPage(ctx, jetons, base, 1e6, facteur)
  const largeurTexte = Math.max(...page.lignes.map((l) => l.largeur), 0)
  if (largeurTexte > lpxUtile && largeurTexte > 0) facteur = lpxUtile / largeurTexte
  page = mettreEnPage(ctx, jetons, base, 1e6, facteur)
  const l0 = page.lignes[0]?.largeur ?? 0
  const alignement = base.alignement
  const x = alignement === 'center' ? (lpx - l0) / 2 : alignement === 'right' ? lpx - marge - l0 : marge
  ctx.save()
  ctx.beginPath()
  ctx.rect(xpx, ypx, lpx, hpx)
  ctx.clip()
  ctx.translate(xpx + x, ypx)
  dessinerPage(ctx, page, base, l0 + 1, facteur, baseParLargeur.couleur, 'left')
  ctx.restore()
}

/** Le canevas final (fond + titre + type + règles), indépendant de l'affichage : utilisé pour l'export comme pour
    l'aperçu. */
async function construireCanvasFinal(carte) {
  await obtenirCanvasOriginal(carte)
  const fond = canvasDeFond(carte)
  const sortie = document.createElement('canvas')
  sortie.width = fond.width
  sortie.height = fond.height
  const ctx = sortie.getContext('2d')
  ctx.drawImage(fond, 0, 0)
  const actives = statsActives(carte.type)
  const aLaMain = mainPresente(carte.type)
  const aDuTexte =
    (carte.texte && carte.texte.trim()) || (carte.texteTitre && carte.texteTitre.trim()) || (carte.texteType && carte.texteType.trim()) ||
    actives.some((s) => carte[s.texteCle] && carte[s.texteCle].trim()) || (aLaMain && carte.texteMain && carte.texteMain.trim())
  if (aDuTexte) {
    await chargerPolices()
    dessinerLigneSurCanvas(ctx, carte.zoneTitre, carte.texteTitre, construireBaseLigne(carte.type, 'title', BASE_TITRE_DEFAUT), fond.width, fond.height)
    dessinerLigneSurCanvas(ctx, carte.zoneType, carte.texteType, construireBaseLigne(carte.type, 'typestr', BASE_TYPE_DEFAUT), fond.width, fond.height)
    for (const s of actives) dessinerLigneSurCanvas(ctx, carte[s.zoneCle], carte[s.texteCle], BASE_STAT_DEFAUT, fond.width, fond.height)
    if (aLaMain) dessinerLigneSurCanvas(ctx, carte.zoneMain, carte.texteMain, BASE_MAIN_DEFAUT, fond.width, fond.height)
    dessinerTexteSurCanvas(ctx, carte, fond.width, fond.height)
  }
  return sortie
}

let compteurRendu = 0
async function dessinerCarte(carte) {
  const jeton = ++compteurRendu
  const sortie = await construireCanvasFinal(carte)
  if (jeton !== compteurRendu || carteActiveId !== carte.id) return // une saisie plus recente a deja relance le rendu
  const toile = $('#toile')
  toile.width = sortie.width
  toile.height = sortie.height
  toile.getContext('2d').drawImage(sortie, 0, 0)
  positionnerRectangle(carte)
}

// ------------------------------------------------------------------ rectangles des trois zones (glisser / redimensionner)
// En PIXELS (pas en %) : `#zone-cadre-conteneur` est dimensionné par son CONTENU (le canevas), une hauteur « auto ».
// Un pourcentage de hauteur sur un enfant absolument positionné d'un ancêtre à hauteur « auto » se résout alors mal
// selon les moteurs (bug constaté : les poignées s'étiraient en bandes sur toute la hauteur de la carte) ; les pixels
// réels du canevas affiché (`clientWidth`/`clientHeight`) n'ont pas ce travers et restent justes à tout zoom.
function positionnerUnRectangle(rect, zoneFrac) {
  if (!rect) return
  if (!zoneFrac) {
    rect.hidden = true
    return
  }
  const toile = $('#toile')
  const l = toile.clientWidth
  const h = toile.clientHeight
  if (!l || !h) {
    rect.hidden = true
    return
  }
  rect.hidden = false
  rect.style.left = `${zoneFrac.x0 * l}px`
  rect.style.top = `${zoneFrac.y0 * h}px`
  rect.style.width = `${Math.max(0, zoneFrac.x1 - zoneFrac.x0) * l}px`
  rect.style.height = `${Math.max(0, zoneFrac.y1 - zoneFrac.y0) * h}px`
}
const ID_RECT_STAT = { zoneThw: '#rect-thw', zoneAtk: '#rect-atk', zoneDef: '#rect-def', zoneRec: '#rect-rec' }
function positionnerRectangle(carte) {
  positionnerUnRectangle($('#rect-zone'), carte?.zone)
  positionnerUnRectangle($('#rect-titre'), carte?.zoneTitre)
  positionnerUnRectangle($('#rect-type'), carte?.zoneType)
  const actives = new Set(statsActives(carte?.type).map((s) => s.zoneCle))
  for (const [cle, id] of Object.entries(ID_RECT_STAT)) positionnerUnRectangle($(id), actives.has(cle) ? carte?.[cle] : null)
  positionnerUnRectangle($('#rect-main'), mainPresente(carte?.type) ? carte?.zoneMain : null)
}

function demarrerGlisse(e, mode, cible) {
  const carte = carteActive()
  if (!carte || !carte[cible]) return
  e.preventDefault()
  e.stopPropagation()
  glisse = { carte, cible, mode, depart: { ...carte[cible] }, sx: e.clientX, sy: e.clientY, rectConteneur: $('#toile').getBoundingClientRect() }
  window.addEventListener('pointermove', surGlisse)
  window.addEventListener('pointerup', finGlisse, { once: true })
}
function surGlisse(e) {
  if (!glisse) return
  const { carte, cible, mode, depart, sx, sy, rectConteneur } = glisse
  const borne = (v) => Math.min(1, Math.max(0, v))
  const dx = rectConteneur.width ? (e.clientX - sx) / rectConteneur.width : 0
  const dy = rectConteneur.height ? (e.clientY - sy) / rectConteneur.height : 0
  let { x0, y0, x1, y1 } = depart
  if (mode === 'deplacer') {
    const l = x1 - x0
    const h = y1 - y0
    x0 = borne(depart.x0 + dx)
    if (x0 + l > 1) x0 = 1 - l
    x1 = x0 + l
    y0 = borne(depart.y0 + dy)
    if (y0 + h > 1) y0 = 1 - h
    y1 = y0 + h
  } else {
    if (mode.includes('w')) x0 = Math.min(depart.x1 - 0.02, borne(depart.x0 + dx))
    if (mode.includes('e')) x1 = Math.max(depart.x0 + 0.02, borne(depart.x1 + dx))
    if (mode.includes('n')) y0 = Math.min(depart.y1 - 0.02, borne(depart.y0 + dy))
    if (mode.includes('s')) y1 = Math.max(depart.y0 + 0.02, borne(depart.y1 + dy))
  }
  carte[cible] = { x0, y0, x1, y1 }
  positionnerRectangle(carte)
}
function finGlisse() {
  window.removeEventListener('pointermove', surGlisse)
  if (!glisse) return
  const { carte, cible } = glisse
  glisse = null
  if (cible === 'zone') carte._zoneAuto = false
  planifierSauvegarde(carte)
  // Un rectangle a bouge : si un fond nettoye existait deja, on refait l'effacement avec les zones actuelles (sinon on
  // ne fait que redessiner — l'utilisateur clique « Effacer » quand il est content du cadrage).
  if (carte.effaceDataUrl) void effacerZoneActive()
  else void dessinerCarte(carte)
}

// ------------------------------------------------------------------ saisie du texte (mini-HTML, barre d'icones)
function inserer(avant, apres = '') {
  const zone = $('#texte-fr')
  const debut = zone.selectionStart
  const fin = zone.selectionEnd
  const texte = zone.value
  const selection = texte.slice(debut, fin)
  zone.value = texte.slice(0, debut) + avant + selection + apres + texte.slice(fin)
  const curseur = debut + avant.length + selection.length
  zone.focus()
  zone.setSelectionRange(selection ? curseur + apres.length : curseur, selection ? curseur + apres.length : curseur)
  zone.dispatchEvent(new Event('input', { bubbles: true }))
}

// ------------------------------------------------------------------ export (PNG individuel, zip global)
function nomFichierExport(carte, dejaVus) {
  let base = (carte.nom || 'carte').replace(/\.[a-z0-9]+$/i, '').trim() || 'carte'
  let nom = `${base}-traduit.png`
  let n = 2
  while (dejaVus?.has(nom)) {
    nom = `${base}-traduit-${n}.png`
    n += 1
  }
  dejaVus?.add(nom)
  return nom
}
async function exporterPng(carte) {
  const canvas = await construireCanvasFinal(carte)
  const lien = el('a', { href: canvas.toDataURL('image/png'), download: nomFichierExport(carte) })
  document.body.append(lien)
  lien.click()
  lien.remove()
}
async function exporterTout() {
  if (!cartes.length) return
  const bouton = $('#b-tout-telecharger')
  bouton.disabled = true
  const texteInitial = bouton.textContent
  try {
    const dejaVus = new Set()
    const fichiers = []
    for (const carte of cartes) {
      bouton.textContent = `Export… (${fichiers.length + 1}/${cartes.length})`
      const canvas = await construireCanvasFinal(carte)
      const blob = await new Promise((ok) => canvas.toBlob(ok, 'image/png'))
      fichiers.push({ nom: nomFichierExport(carte, dejaVus), octets: new Uint8Array(await blob.arrayBuffer()) })
    }
    const zip = creerZip(fichiers)
    const lien = el('a', { href: URL.createObjectURL(zip), download: 'traductions.zip' })
    document.body.append(lien)
    lien.click()
    lien.remove()
    setTimeout(() => URL.revokeObjectURL(lien.href), 30000)
  } finally {
    bouton.textContent = texteInitial
    bouton.disabled = false
  }
}

// ------------------------------------------------------------------ branchement des evenements (une fois)
function brancherEvenements() {
  const entree = $('#entree-fichiers')
  $('#b-ajouter').addEventListener('click', () => entree.click())
  entree.addEventListener('change', () => {
    ajouterFichiers([...entree.files])
    entree.value = ''
  })
  const depot = $('#zone-depot')
  ;['dragenter', 'dragover'].forEach((t) => depot.addEventListener(t, (e) => { e.preventDefault(); depot.classList.add('survole') }))
  ;['dragleave', 'drop'].forEach((t) => depot.addEventListener(t, (e) => { e.preventDefault(); depot.classList.remove('survole') }))
  depot.addEventListener('drop', (e) => ajouterFichiers([...(e.dataTransfer?.files ?? [])]))

  $('#type-carte').addEventListener('change', async (e) => {
    const carte = carteActive()
    if (!carte) return
    carte.type = e.target.value
    // Le type change l'orientation attendue (manigance = paysage) et la position des trois boites : on repart de zero.
    carte.zone = zoneParDefaut(estPaysage(carte.type), COTE_PAYSAGE[carte.type])
    carte.zoneTitre = zoneTitreInitiale(carte.type)
    carte.zoneType = zoneTypeInitiale(carte.type)
    // Le libelle du type se pre-remplit avec le mot REELLEMENT IMPRIME sur la carte (LIBELLES_TYPE_IMPRIME, verifie
    // sur de vrais scans), PAS le nom du menu « Type de carte » (NOMS) : un defaut pratique, toujours modifiable
    // (vers n'importe quelle langue) par l'utilisateur ensuite.
    carte.texteType = LIBELLES_TYPE_IMPRIME[carte.type] ?? ''
    $('#type-fr').value = carte.texteType
    // Badges de stats : repartis a zero (position ET texte, repris sur l'abreviation officielle FR) pour les champs
    // que CE type imprime reellement ; ceux qu'il n'imprime pas gardent leur etat (invisibles, sans effet).
    for (const [i, s] of statsActives(carte.type).entries()) {
      carte[s.zoneCle] = zoneStatInitiale(carte.type, s.cls, i)
      carte[s.texteCle] = s.abrege
    }
    construireChampsStats(carte)
    // Bande « taille de main / points de vie » : seuls 4 types l'impriment.
    if (mainPresente(carte.type)) {
      carte.zoneMain = zoneMainInitiale(carte.type)
      carte.texteMain = 'Taille de main / Points de vie'
    }
    $('#champ-main').hidden = !mainPresente(carte.type)
    $('#main-fr').value = carte.texteMain || ''
    carte._canvasTravail = null
    carte.effaceDataUrl = null
    carte._cadreTexte = null
    $('#info-zone').textContent = ''
    await dessinerCarte(carte)
    rendreListe()
    planifierSauvegarde(carte)
  })
  $('#ch-sombre').addEventListener('change', async (e) => {
    const carte = carteActive()
    if (!carte) return
    carte.sombre = e.target.checked
    if (carte.effaceDataUrl) await effacerZoneActive()
    else await dessinerCarte(carte)
    planifierSauvegarde(carte)
  })
  $('#b-detecter').addEventListener('click', () => void detecterZoneAuto())
  $('#b-effacer').addEventListener('click', () => void effacerZoneActive())
  $('#b-export-png').addEventListener('click', () => { const c = carteActive(); if (c) void exporterPng(c) })
  $('#b-tout-telecharger').addEventListener('click', () => void exporterTout())

  const brancherChamp = (idChamp, cle) => {
    const champ = $(idChamp)
    let debounce = null
    champ.addEventListener('input', () => {
      const carte = carteActive()
      if (!carte) return
      carte[cle] = champ.value
      clearTimeout(debounce)
      debounce = setTimeout(() => void dessinerCarte(carte), 120)
      planifierSauvegarde(carte)
    })
  }
  brancherChamp('#texte-fr', 'texte')
  brancherChamp('#titre-fr', 'texteTitre')
  brancherChamp('#type-fr', 'texteType')
  brancherChamp('#main-fr', 'texteMain')

  $('#barre-icones').append(
    ...ICONES_BARRE.filter((nom) => nom in ICONES).map((nom) =>
      el('button', { class: 'btn petit fixe', type: 'button', title: `[${nom}]`, onclick: () => inserer(`[${nom}]`) }, el('span', { style: 'font-family:ChampionsIcons' }, ICONES[nom]))
    )
  )
  $('#b-gras').addEventListener('click', () => inserer('<b>', '</b>'))
  $('#b-italique').addEventListener('click', () => inserer('<i>', '</i>'))
  $('#b-trait').addEventListener('click', () => inserer('<em>', '</em>'))
  $('#b-souligne').addEventListener('click', () => inserer('<u>', '</u>'))
  $('#b-filet').addEventListener('click', () => inserer('<hr/>\n'))
  $('#b-saut').addEventListener('click', () => inserer('\n\n'))

  for (const rect of document.querySelectorAll('.rect-ajustable')) {
    const cible = rect.dataset.cible
    rect.addEventListener('pointerdown', (e) => {
      if (e.target.closest('[data-poignee]')) return
      demarrerGlisse(e, 'deplacer', cible)
    })
    for (const poignee of rect.querySelectorAll('[data-poignee]')) {
      poignee.addEventListener('pointerdown', (e) => demarrerGlisse(e, poignee.dataset.poignee, cible))
    }
  }
}

demarrer()
