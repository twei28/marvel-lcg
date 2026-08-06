// Verifie la coherence entre le pack de scans FR extrait et ce que le plateau
// croit disponible.
//
// Ce que ces cas protegent : un fichier efface a la main apres l'import laisse
// la liste generee en mentir, et le plateau demande alors une image qui
// n'existe pas. L'echec est silencieux a l'ecran, la carte reste simplement
// vide. Le seul moyen de le voir est de comparer les deux cotes.
//
// Usage : node outils/verifier-scans-fr.mjs

import { readdirSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'

const IMAGES = resolve('Fusion/marvel-lcg-src/assets/pics-fr')
const LISTE = resolve('ui-app/src/board/scans-fr-liste.ts')
const TEXTES = resolve('ui-app/src/board/textes-fr.ts')
const TEXTES_FANMADE = resolve('ui-app/src/board/textes-fr-fanmade.ts')
// Le catalogue tient en DEUX fichiers : ne lire que le premier laissait Rescue,
// Hulk (Rainy) et Stan Lee hors de tout controle, sans que rien ne le signale.
const CARTES = [
  resolve('Fusion/marvel-lcg-src/data/cards.json'),
  resolve('Fusion/marvel-lcg-src/data/cards_custom.json'),
]

let echecs = 0
const verifier = (nom, condition, detail) => {
  if (!condition) echecs += 1
  console.log(`${condition ? 'OK   ' : 'ECHEC'} ${nom}`)
  if (!condition && detail) console.log(`      ${detail}`)
}

/** Codes cites dans un module genere, lus comme du texte. */
function codesDe(chemin, motif) {
  const source = readFileSync(chemin, 'utf8')
  return new Set([...source.matchAll(motif)].map((trouve) => trouve[1]))
}

const listes = codesDe(LISTE, /^\s*'([^']+)',$/gm)
const textes = codesDe(TEXTES, /^\s*'([^']+)':/gm)
const fanmade = codesDe(TEXTES_FANMADE, /^\s*'([^']+)':/gm)

const fichiers = new Set(
  readdirSync(IMAGES)
    .filter((nom) => nom.startsWith('fr_') && nom.endsWith('.jpg'))
    .map((nom) => nom.slice(3, -4))
)

const picIds = new Set()
for (const chemin of CARTES) {
  for (const cartes of Object.values(JSON.parse(readFileSync(chemin, 'utf8')))) {
    if (!Array.isArray(cartes)) continue
    for (const carte of cartes) picIds.add(carte.pic_id ?? carte.card_id)
  }
}

const sansFichier = [...listes].filter((code) => !fichiers.has(code))
verifier(
  'chaque code annonce a son image',
  sansFichier.length === 0,
  `${sansFichier.length} manquants, ex. ${sansFichier.slice(0, 5).join(', ')}`
)

const horsListe = [...fichiers].filter((code) => !listes.has(code))
verifier(
  'chaque image est annoncee',
  horsListe.length === 0,
  `${horsListe.length} orphelins, ex. ${horsListe.slice(0, 5).join(', ')}`
)

const inconnus = [...listes].filter((code) => !picIds.has(code))
verifier(
  'chaque code annonce existe dans le catalogue',
  inconnus.length === 0,
  `${inconnus.length} inconnus, ex. ${inconnus.slice(0, 5).join(', ')}`
)

const doublons = [...textes].filter((code) => listes.has(code))
verifier(
  'le dictionnaire ne double aucun scan francais',
  doublons.length === 0,
  `${doublons.length} en trop, ex. ${doublons.slice(0, 5).join(', ')}`
)

// Le dictionnaire fan-made est ecrit a la main : rien ne le regenere, donc rien
// ne le corrige tout seul si une carte est renommee ou retiree d'un pack.
const fanmadeInconnus = [...fanmade].filter((code) => !picIds.has(code))
verifier(
  'chaque carte fan-made traduite existe dans le catalogue',
  fanmadeInconnus.length === 0,
  `${fanmadeInconnus.length} inconnus, ex. ${fanmadeInconnus.slice(0, 5).join(', ')}`
)

const fanmadeDoublons = [...fanmade].filter((code) => listes.has(code) || textes.has(code))
verifier(
  'aucune carte fan-made traduite deux fois',
  fanmadeDoublons.length === 0,
  `${fanmadeDoublons.length} en trop, ex. ${fanmadeDoublons.slice(0, 5).join(', ')}`
)

// Classer par prefixe de code (« 61 a 75 = fan-made ») s'est revele faux : les
// packs vivent aussi en 90xxx et dans cards_custom.json. La seule question qui
// compte pour le joueur est ailleurs : cette carte lui parle-t-elle francais,
// par son scan ou par son texte ? On compte donc ca, et rien d'autre.
const avecTexte = new Set()
for (const chemin of CARTES) {
  for (const cartes of Object.values(JSON.parse(readFileSync(chemin, 'utf8')))) {
    if (!Array.isArray(cartes)) continue
    for (const carte of cartes) {
      if (carte.text) avecTexte.add(carte.pic_id ?? carte.card_id)
    }
  }
}
const muettes = [...avecTexte].filter(
  (code) => !listes.has(code) && !textes.has(code) && !fanmade.has(code)
)
console.log(`INFO  scans francais : ${listes.size} cartes`)
console.log(`INFO  textes francais : ${textes.size} officiels + ${fanmade.size} ecrits a la main`)
console.log(`INFO  cartes encore muettes : ${muettes.length}${
  muettes.length ? ` (ex. ${muettes.slice(0, 5).join(', ')})` : ''
}`)

process.exit(echecs === 0 ? 0 : 1)
