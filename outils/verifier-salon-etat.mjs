// Vérifie la décision « peut-on lancer la partie » du salon multijoueur.
//
// Le module visé est pur et sans import : Node peut l'exécuter tel quel, sans
// navigateur ni serveur. Même esprit que ui-app/outils/verifier-libelles-cible.mjs.
//
// Usage : node outils/verifier-salon-etat.mjs

import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const chemin = resolve('Fusion/marvel-lcg-src/public/js/prepare/salon-etat.js')
const { etatSalon } = await import(pathToFileURL(chemin).href)

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

const choix = (h = 'a', d = 'd') => ({ hero_card_id: h, deck_id: d })
const resume = (e) => [e.prete, e.manquants]

// 2 joueurs : on attend le seul invité, siège technique 1 = « Joueur 2 ».
verifier('2 joueurs, personne n’a choisi',
  resume(etatSalon({ nombreJoueurs: 2, sieges: {} })), [false, [2]])

verifier('2 joueurs, l’invité a choisi',
  resume(etatSalon({ nombreJoueurs: 2, sieges: { 1: choix('69001a', 'madame_web') } })),
  [true, []])

// 4 joueurs : on attend les sièges techniques 1, 2 et 3.
verifier('4 joueurs, un seul a choisi',
  resume(etatSalon({ nombreJoueurs: 4, sieges: { 1: choix() } })), [false, [3, 4]])

verifier('4 joueurs, tout le monde a choisi',
  resume(etatSalon({ nombreJoueurs: 4, sieges: { 1: choix(), 2: choix(), 3: choix() } })),
  [true, []])

// Le siège de l’hôte n’est jamais attendu, même s’il traîne dans le dict.
verifier('le siège de l’hôte ne compte pas',
  resume(etatSalon({ nombreJoueurs: 2, sieges: { 0: choix() } })), [false, [2]])

// Un choix incomplet ne vaut pas un choix.
verifier('choix sans deck',
  resume(etatSalon({ nombreJoueurs: 2, sieges: { 1: { hero_card_id: '69001a', deck_id: '' } } })),
  [false, [2]])

verifier('choix sans héros',
  resume(etatSalon({ nombreJoueurs: 2, sieges: { 1: { hero_card_id: '', deck_id: 'madame_web' } } })),
  [false, [2]])

// Un siège au-delà du nombre de joueurs est ignoré (l’hôte a réduit la table).
verifier('siège hors table ignoré',
  resume(etatSalon({ nombreJoueurs: 2, sieges: { 1: choix(), 3: choix() } })), [true, []])

// Les clés arrivent en CHAÎNES depuis le JSON du serveur.
verifier('clés en chaînes (JSON du serveur)',
  resume(etatSalon({ nombreJoueurs: 2, sieges: { '1': choix() } })), [true, []])

// Solo : un seul joueur, personne à attendre.
verifier('1 joueur, rien à attendre',
  resume(etatSalon({ nombreJoueurs: 1, sieges: {} })), [true, []])

// Le détail des choix est rendu pour que le wizard puisse les afficher.
const e = etatSalon({ nombreJoueurs: 2, sieges: { 1: choix('69001a', 'madame_web') } })
verifier('choixParSiege expose le choix',
  e.choixParSiege.get(1).hero_card_id, '69001a')

console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
process.exit(echecs === 0 ? 0 : 1)
