// Vérifie la REGLE DE DECK-BUILDING des cartes qu'un aspect IMPOSE au deck
// (`cartesImposees` de public/js/deckbuilder/regles.js).
//
// Pourquoi un outil à part : cette règle est écrite DEUX FOIS, une par côté.
//   - le MOTEUR l'applique  : `PlayerSetup.CartesImposeesParLesAspects`
//     (src/game/player/element/player_setup.py), verrouillé par
//     `tools/test_aspect_determination.py` ;
//   - l'EDITEUR l'annonce   : `regles.js`, verrouillé ici.
// Les deux tables doivent dire la même chose. Ce fichier garde la moitié JS.
//
// ⚠ Il a déjà servi : la première version JS oubliait de multiplier le coût
// par le NOMBRE D'EXEMPLAIRES, et trois « Feed the Hunger » pesaient 3 au lieu
// de 9. La seconde tranche n'était jamais atteinte. Le côté Python, qui itère
// sur une liste à plat, n'avait pas ce défaut : c'est bien la duplication qui
// est risquée, d'où ce garde-fou.
//
// La cible est la copie Windows du jeu : Node est le binaire Windows et ne lit
// pas les chemins WSL.
//
// Usage : node outils/verifier-regles-deck.mjs
const m = await import('../Fusion/marvel-lcg-src/public/js/deckbuilder/regles.js')
const cartes = {
  vz011: { class: 'Venomized', desc: { Cost: '3' } },
  vz024: { class: 'Venomized', desc: { Cost: '1' } },
  vz035: { class: 'Venomized', desc: { Cost: '0' } },
  vz012: { class: 'Venomized', desc: { Cost: 'X' } },
  '01088': { class: 'Basic', desc: {} },
}
const c = (id) => cartes[id]
const q = (o) => m.cartesImposees(new Map(Object.entries(o)), c)
const dire = (nom, obtenu, attendu) => {
  const ok = JSON.stringify(obtenu) === JSON.stringify(attendu)
  console.log(`  ${ok ? 'ok   ' : 'ECHEC'} ${nom} -> ${JSON.stringify(obtenu)}`)
  return ok ? 0 : 1
}
let ko = 0
ko += dire('Venomized est un aspect reconnu', m.ASPECTS.includes('Venomized'), true)
ko += dire('sans carte Venomized, rien n est impose', q({ '01088': 3 }).length, 0)
ko += dire('cout 0 (vz035 seul), rien n est impose', q({ vz035: 3 }).length, 0)
ko += dire('un cout X vaut 0, comme cote moteur', q({ vz012: 3 }).length, 0)
ko += dire('cout 20 -> 1 carte', q({ vz011: 6, vz024: 2 })[0].nombre, 1)
ko += dire('cout 21 -> 2 cartes', q({ vz011: 7 })[0].nombre, 2)
ko += dire('cout 40 -> 2 cartes', q({ vz011: 13, vz024: 1 })[0].nombre, 2)
ko += dire('au-dela de 40, derniere tranche', q({ vz011: 15 })[0].nombre, 2)
ko += dire('le set impose est nomme', q({ vz011: 7 })[0].set, 'Venomized Weakness')
// Multiverse : une carte Multiverse remplace celle de meme numero (MC4DB,
// 29/09/2026). `validerDeck` doit refuser les deux ensemble, signatures du
// heros comprises, et se taire quand une seule est presente.
const cartesMv = {
  ra002: { class: 'Hero', type: 'Ally', name: 'Odinson', set_name: 'Thor (Jane Foster)', multiverse_of: 'ra003', desc: {} },
  ra003: { class: 'Hero', type: 'Ally', name: 'Roz Solomon', set_name: 'Thor (Jane Foster)', desc: {} },
  '01088': { class: 'Basic', type: 'Event', name: 'Haymaker', desc: {} },
}
const cMv = (id) => cartesMv[id]
const problemesMv = (heroDeck, choisies) => m.validerDeck({
  hero: { name: 'Jane Foster', deck: { hero_deck: heroDeck } },
  choisies: new Map(Object.entries(choisies)), carte: cMv,
}).problemes.filter((x) => x.startsWith('Multiverse'))
ko += dire('les deux versions dans les signatures -> refuse', problemesMv(['ra002', 'ra003'], {}).length, 1)
ko += dire('la Multiverse choisie, l originale en signature -> refuse', problemesMv(['ra003'], { ra002: 1 }).length, 1)
ko += dire('une seule version -> rien a redire', problemesMv(['ra003'], { '01088': 3 }).length, 0)
ko += dire('la Multiverse seule -> rien a redire', problemesMv(['ra002'], {}).length, 0)
console.log(ko ? `ECHECS : ${ko}` : 'ECHECS : 0')
process.exit(ko ? 1 : 0)
