// Vérifie les détections de fin de leçon du mode Découverte.
//
// Le module lecons.ts est pur : Node peut l'exécuter une fois compilé. Même
// montage que verifier-libelles-cible.mjs (sortie CommonJS dans un dossier
// local, jamais de process.exit dans le try, sinon le finally ne nettoie pas).
//
// Usage : node outils/verifier-lecons.mjs

import { execFileSync } from 'node:child_process'
import { mkdirSync, rmSync, writeFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { createRequire } from 'node:module'

const sortie = '.tmp-verif-lecons'
let code = 1

try {
  execFileSync(
    process.execPath,
    ['node_modules/typescript/bin/tsc', 'src/board/lecons.ts',
      '--outDir', sortie, '--module', 'commonjs', '--target', 'es2022',
      '--moduleResolution', 'bundler', '--skipLibCheck', '--ignoreConfig'],
    { stdio: 'inherit' }
  )
  mkdirSync(sortie, { recursive: true })
  writeFileSync(join(sortie, 'package.json'), '{"type":"commonjs"}')

  const requerir = createRequire(import.meta.url)
  const { LECONS, prendreRepere } = requerir(resolve(sortie, 'lecons.js'))

  let echecs = 0
  const verifier = (nom, obtenu, attendu) => {
    const ok = JSON.stringify(obtenu) === JSON.stringify(attendu)
    if (!ok) echecs += 1
    console.log(`${ok ? 'OK   ' : 'ECHEC'} ${nom}`)
    if (!ok) {
      console.log(`      obtenu  ${JSON.stringify(obtenu)}`)
      console.log(`      attendu ${JSON.stringify(attendu)}`)
    }
  }

  /** Monde minimal, ajustable par ce qu'on lui passe. */
  const monde = (o = {}) => ({
    round_id: o.round ?? 1,
    area_schemes_main: [{ info: { k_threat: o.menace ?? 5 } }],
    area_villain: [{ card_id: '01095', info: { health: o.pvVilain ?? 14 } }],
    players: [{
      area_hero: [{ card_type: o.forme ?? 'AlterEgo', info: { health: o.pv ?? 10 } }],
      allies: o.allies ?? [],
      hand_cards: (o.main ?? ['01005', '01060']).map((id) => ({ card_id: id })),
    }],
  })

  const lecon = (id) => LECONS.find((l) => l.id === id)
  const repere = prendreRepere(monde())

  // --- Structure
  // 8 leçons de jeu (détectées sur l'état) puis 4 leçons de plateau (manuelles).
  verifier('les 12 leçons sont là', LECONS.length, 12)
  verifier('les identifiants sont uniques',
    new Set(LECONS.map((l) => l.id)).size, LECONS.length)
  verifier('les 4 leçons du plateau sont manuelles',
    LECONS.slice(8).every((l) => l.manuelle === true), true)
  verifier('aucune leçon de jeu n’est manuelle',
    LECONS.slice(0, 8).some((l) => l.manuelle === true), false)
  verifier('le mulligan est la toute première leçon', LECONS[0].id, 'mulligan')

  // --- Le repère lit bien l'état de départ
  verifier('le repère retient les PV du vilain', repere.pvVilain, 14)
  verifier('le repère retient la menace', repere.menacePrincipale, 5)
  verifier('le repère retient la main', repere.cartesEnMain, ['01005', '01060'])

  // --- 0 : le mulligan (round_id passe a 1 quand le round demarre, donc APRES)
  verifier('0 mulligan : mise en place, le round n’a pas commencé',
    lecon('mulligan').accomplie(monde({ round: 0 }), repere), false)
  verifier('0 mulligan : le round a commencé',
    lecon('mulligan').accomplie(monde({ round: 1 }), repere), true)
  verifier('0 mulligan : la leçon nomme la carte de la leçon « jouer-carte »',
    lecon('mulligan').texte.includes('Coup de pied volant'), true)

  // --- 1 : changer de forme
  verifier('1 forme : encore en civil',
    lecon('forme-heros').accomplie(monde({ forme: 'AlterEgo' }), repere), false)
  verifier('1 forme : passé en héros',
    lecon('forme-heros').accomplie(monde({ forme: 'Hero' }), repere), true)

  // --- 2 : jouer une carte
  verifier('2 jouer : la carte est encore en main',
    lecon('jouer-carte').accomplie(monde({ main: ['01005', '01060'] }), repere), false)
  verifier('2 jouer : la carte a quitté la main',
    lecon('jouer-carte').accomplie(monde({ main: ['01060'] }), repere), true)
  verifier('2 jouer : ne se déclenche pas si la carte n’y était jamais',
    lecon('jouer-carte').accomplie(monde({ main: ['01060'] }),
      { ...repere, cartesEnMain: ['01060'] }), false)

  // --- 3 : attaquer
  verifier('3 attaquer : le vilain est intact',
    lecon('attaquer').accomplie(monde({ pvVilain: 14 }), repere), false)
  verifier('3 attaquer : le vilain a perdu des PV',
    lecon('attaquer').accomplie(monde({ pvVilain: 12 }), repere), true)

  // --- 4 : contrer (il en faut DEUX, pas une)
  verifier('4 contrer : une seule menace retirée',
    lecon('contrer').accomplie(monde({ menace: 4 }), repere), false)
  verifier('4 contrer : deux menaces retirées',
    lecon('contrer').accomplie(monde({ menace: 3 }), repere), true)
  verifier('4 contrer : la menace a monté',
    lecon('contrer').accomplie(monde({ menace: 7 }), repere), false)

  // --- 5 : finir son tour
  verifier('5 tour : même round',
    lecon('finir-tour').accomplie(monde({ round: 1 }), repere), false)
  verifier('5 tour : round suivant',
    lecon('finir-tour').accomplie(monde({ round: 2 }), repere), true)

  // --- 6 : un allié
  verifier('6 allié : aucun en jeu',
    lecon('allie').accomplie(monde({ allies: [] }), repere), false)
  verifier('6 allié : un en jeu',
    lecon('allie').accomplie(monde({ allies: [{ card_id: '01059' }] }), repere), true)

  // --- 7 : récupérer (les DEUX conditions)
  verifier('7 récupérer : en héros, PV remontés',
    lecon('recuperer').accomplie(monde({ forme: 'Hero', pv: 13 }), repere), false)
  verifier('7 récupérer : en civil, PV inchangés',
    lecon('recuperer').accomplie(monde({ forme: 'AlterEgo', pv: 10 }), repere), false)
  verifier('7 récupérer : en civil et PV remontés',
    lecon('recuperer').accomplie(monde({ forme: 'AlterEgo', pv: 13 }), repere), true)

  // --- Robustesse : un monde à moitié vide ne doit rien casser
  const vide = {}
  verifier('un monde vide ne fait pas planter le repère',
    typeof prendreRepere(vide).pvVilain, 'number')
  verifier('un monde vide ne valide aucune leçon de jeu',
    LECONS.slice(0, 8).some((l) => l.accomplie(vide, prendreRepere(vide))), false)

  console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
  code = echecs === 0 ? 0 : 1
} finally {
  rmSync(sortie, { recursive: true, force: true })
}

process.exit(code)
