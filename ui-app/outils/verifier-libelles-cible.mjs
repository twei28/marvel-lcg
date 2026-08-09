// Vérifie les libellés de l'étape « choisir les cibles ».
//
// ui-app n'a pas de framework de test : ce script compile le module pur
// libelles-cible.ts avec tsc, puis contrôle les phrases produites. Le cas de
// référence est celui qui a motivé le correctif — 43006 Regenerative
// Longevity, dont le moteur envoie all_legal_targets = [1,1,1,1,9] pour un
// target_num_range de [1,4].
//
// Usage : node outils/verifier-libelles-cible.mjs

import { execFileSync } from 'node:child_process'
import { mkdirSync, rmSync, writeFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { createRequire } from 'node:module'

// Dossier de sortie DANS le projet : node tourne ici via l'interop Windows,
// os.tmpdir() rend un chemin C:\ que le tsc appelé depuis WSL ne sait pas
// écrire.
const sortie = '.tmp-verif-libelles'
let code = 1

try {
  // CommonJS : les imports compilés restent sans extension, ce que le
  // résolveur ESM de node refuse. Le package.json local rétablit le mode CJS
  // malgré le "type": "module" du projet.
  execFileSync(
    process.execPath,
    ['node_modules/typescript/bin/tsc', 'src/board/libelles-cible.ts',
      '--outDir', sortie, '--module', 'commonjs', '--target', 'es2022',
      '--moduleResolution', 'bundler', '--skipLibCheck', '--ignoreConfig'],
    { stdio: 'inherit' }
  )
  mkdirSync(sortie, { recursive: true })
  writeFileSync(join(sortie, 'package.json'), '{"type":"commonjs"}')

  const requerir = createRequire(import.meta.url)
  const { libellesCible } = requerir(resolve(sortie, 'libelles-cible.js'))

  let echecs = 0
  const verifier = (nom, obtenu, attendu) => {
    const ok = obtenu === attendu
    if (!ok) echecs += 1
    console.log(`${ok ? 'OK   ' : 'ECHEC'} ${nom}`)
    if (!ok) {
      console.log(`      obtenu  : ${JSON.stringify(obtenu)}`)
      console.log(`      attendu : ${JSON.stringify(attendu)}`)
    }
  }

  // --- Le cas de la régression : 43006, X-23 à 5 dégâts, Honey Badger à 1.
  const repartition = libellesCible({
    choisies: 1, minimum: 1, maximum: 4, cartesCiblables: 2, repetable: true,
  })
  verifier('43006 · titre annonce le maximum',
    repartition.titre, 'Choisir jusqu’à 4 cibles')
  verifier('43006 · detail progresse vers le maximum',
    repartition.detail, '1/4 attribuée(s) · 1 minimum · 2 carte(s) ciblable(s)')
  verifier('43006 · indice de répétition présent',
    repartition.indice,
    'Une même carte peut être choisie plusieurs fois (1 clic = 1 attribution)')

  // --- Non-régression : une cible unique garde l'ancien libellé.
  const unique = libellesCible({
    choisies: 0, minimum: 1, maximum: 1, cartesCiblables: 1, repetable: false,
  })
  verifier('cible unique · titre', unique.titre, 'Choisir la seule cible')
  verifier('cible unique · detail', unique.detail, '0/1 requise(s) · 1 possible(s)')
  verifier('cible unique · aucun indice', unique.indice, undefined)

  // --- Non-régression : nombre libre (minimum 0).
  const libre = libellesCible({
    choisies: 2, minimum: 0, maximum: 5, cartesCiblables: 5, repetable: false,
  })
  verifier('nombre libre · detail',
    libre.detail, '2/5 sélectionnée(s) · nombre au choix')

  // --- Non-régression : plusieurs cibles distinctes, sans répétition.
  const multiple = libellesCible({
    choisies: 0, minimum: 2, maximum: 2, cartesCiblables: 4, repetable: false,
  })
  verifier('2 cibles exigées · detail',
    multiple.detail, '0/2 requise(s) · 4 possible(s)')
  verifier('2 cibles exigées · aucun indice', multiple.indice, undefined)

  // --- Mulligan : libellé dédié, inchangé.
  const mulligan = libellesCible({
    choisies: 0, minimum: 0, maximum: 6, cartesCiblables: 6,
    repetable: false, mulligan: true,
  })
  verifier('mulligan · titre', mulligan.titre, 'Choisir les cartes du mulligan')
  // Le detail ne doit PAS rester vide : c'est le premier ecran de la partie et
  // « mulligan » ne parle pas a un debutant (mode Decouverte, lecon 1).
  verifier('mulligan · le détail explique qu’on peut ne rien défausser',
    mulligan.detail.includes('aucune'), true)

  console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
  code = echecs === 0 ? 0 : 1
} finally {
  // Surtout PAS de process.exit() dans le try : il court-circuite ce finally
  // et laisse le dossier de compilation derriere lui.
  rmSync(sortie, { recursive: true, force: true })
}

process.exit(code)
