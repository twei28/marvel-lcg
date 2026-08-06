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
const CARTES = resolve('Fusion/marvel-lcg-src/data/cards.json')

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

const fichiers = new Set(
  readdirSync(IMAGES)
    .filter((nom) => nom.startsWith('fr_') && nom.endsWith('.jpg'))
    .map((nom) => nom.slice(3, -4))
)

const catalogue = JSON.parse(readFileSync(CARTES, 'utf8'))
const picIds = new Set()
for (const cartes of Object.values(catalogue)) {
  if (!Array.isArray(cartes)) continue
  for (const carte of cartes) picIds.add(carte.pic_id ?? carte.card_id)
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

const manquants = [...picIds].filter(
  (code) => /^\d{5}[a-z]?$/.test(code) && !listes.has(code)
)
const officielles = manquants.filter((code) => Number(code.slice(0, 2)) < 61)
const fan = manquants.filter((code) => Number(code.slice(0, 2)) >= 61)
console.log(`INFO  couverture : ${listes.size} cartes en francais`)
console.log(`INFO  sans scan FR : ${officielles.length} officielles, ${fan.length} fan-made`)

process.exit(echecs === 0 ? 0 : 1)
