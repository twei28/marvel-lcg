// Garde-fou : le serveur du jeu route les fichiers PAR EXTENSION, en liste
// blanche stricte. Un fichier hors liste ne provoque pas d'erreur : il tombe
// dans le fourre-tout qui renvoie une image « no image ». La panne est donc
// SILENCIEUSE, et ce script est le seul endroit qui la rend visible.
//
// Liste blanche reelle, relevee dans web_server.py et verifiee en direct sur
// le serveur en cours :
//   .html / .js / .css   -> 200 avec le bon type MIME
//   .woff2 / .json / .png -> 200 + image/jpeg de 2035 octets (echec SILENCIEUX)
//   .svg / .woff hachés   -> 404
//
// Usage : node outils/verifier-sortie.mjs [dossier]   (defaut : dist)

import { readdirSync, statSync, existsSync } from 'node:fs'
import { join, extname } from 'node:path'

const AUTORISEES = new Set(['.html', '.js', '.css'])

const DOSSIER = process.argv[2] ?? 'dist'

function parcourir(dossier) {
  return readdirSync(dossier).flatMap((nom) => {
    const chemin = join(dossier, nom)
    return statSync(chemin).isDirectory() ? parcourir(chemin) : [chemin]
  })
}

if (!existsSync(DOSSIER)) {
  console.error(
    `Dossier de sortie introuvable : ${DOSSIER}\n` +
      "Lance d'abord `npm run build`."
  )
  process.exit(1)
}

const fichiers = parcourir(DOSSIER)

if (fichiers.length === 0) {
  console.error(
    `Le dossier de sortie ${DOSSIER} est vide.\n` +
      "Un build qui ne produit rien passerait ce controle pour de mauvaises raisons."
  )
  process.exit(1)
}

const intrus = fichiers.filter((f) => !AUTORISEES.has(extname(f).toLowerCase()))

if (intrus.length) {
  console.error(
    "Le build a produit des fichiers que le serveur du jeu ne sait pas servir :\n" +
      intrus.map((f) => '  - ' + f).join('\n') +
      "\nCes fichiers ne renverraient PAS d'erreur : le serveur repondrait une image vide" +
      " (200 OK, image/jpeg de 2035 octets) ou un 404, sans rien afficher en console.\n" +
      "Extensions autorisees : " +
      [...AUTORISEES].join(', ') +
      "\nCorrige la configuration Vite (assetsInlineLimit) ou sors ces fichiers du build."
  )
  process.exit(1)
}

console.log(
  `Sortie conforme : ${fichiers.length} fichiers dans ${DOSSIER}, extensions autorisees uniquement.`
)
