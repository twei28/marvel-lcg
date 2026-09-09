// Vérifie les fonctions pures autour des decks MarvelCDB : recherche,
// favoris, conversion vers le moteur, et REGLES DE CONSTRUCTION (regles.js),
// que l'import applique depuis le 09/09/2026 pour accepter le deck d'un autre
// héros sans accepter n'importe quelle pioche.
//
// Les modules visés n'importent rien et ne touchent au DOM que par un stockage
// injecté : Node les exécute tels quels, sans navigateur ni serveur.
//
// La cible est la copie Windows du jeu : Node est le binaire Windows et ne lit
// pas les chemins WSL. Synchroniser AVANT de lancer, sinon on teste la version
// précédente (bash ui-app/deployer.sh, ou le rsync du guide §1.3).
//
// Usage : node outils/verifier-marvelcdb.mjs

import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const mod = async (nom) =>
  import(pathToFileURL(resolve('Fusion/marvel-lcg-src/public/js/marvelcdb/' + nom)).href)
// regles.js vit chez l'editeur de deck, mais l'import marvelcdb l'applique
// AUSSI depuis le 09/09/2026 : coller le lien d'un autre heros ne prend que ses
// cartes d'aspect, et celles-ci doivent rester legales pour le heros du siege.
const modDeck = async (nom) =>
  import(pathToFileURL(resolve('Fusion/marvel-lcg-src/public/js/deckbuilder/' + nom)).href)

const { filtrer } = await mod('filtres.js')
const { lireFavoris, estFavori, basculerFavori } = await mod('favoris.js')
const { versDeckMoteur, ecartDeConversion } = await mod('conversion.js')
const { validerDeck, reglesAspect, choisiesDuDeck } = await modDeck('regles.js')

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

/* ---------------------------------------------------------------- filtres */
const deck = (id, o = {}) => ({
  id, nom: o.nom ?? ('deck ' + id), aspect: o.aspect ?? 'justice',
  tags: o.tags ?? [], date: o.date ?? '2026-01-01',
  jouable: o.jouable ?? true, cartes_absentes: o.cartes_absentes ?? [], cartes: {},
})
const ids = (l) => l.map((d) => d.id)

const jeu = [
  deck(1, { aspect: 'justice', date: '2026-03-01', tags: ['solo'] }),
  deck(2, { aspect: 'aggression', date: '2026-05-01', tags: ['multiplayer'] }),
  deck(3, { aspect: 'justice', date: '2026-04-01', nom: 'Le Grand Bleu' }),
  deck(4, { aspect: 'justice', date: '2026-06-01', jouable: false, cartes_absentes: ['99999'] }),
]

verifier('tri chronologique décroissant, incomplets masqués par défaut',
  ids(filtrer(jeu, {})), [2, 3, 1])
verifier('masquerIncomplets: false montre tout',
  ids(filtrer(jeu, { masquerIncomplets: false })), [4, 2, 3, 1])
verifier('filtre par aspect', ids(filtrer(jeu, { aspect: 'justice' })), [3, 1])
verifier('filtre par tag', ids(filtrer(jeu, { tag: 'solo' })), [1])
verifier('recherche par nom, insensible à la casse et aux accents',
  ids(filtrer(jeu, { texte: 'grand bleu' })), [3])
verifier('critères cumulés',
  ids(filtrer(jeu, { aspect: 'justice', texte: 'deck' })), [1])
verifier('aucun résultat rend une liste vide',
  filtrer(jeu, { aspect: 'pool' }), [])
verifier('liste vide en entrée', filtrer([], {}), [])

/* ---------------------------------------------------------------- favoris */
const fauxStockage = () => {
  const m = new Map()
  return {
    getItem: (k) => (m.has(k) ? m.get(k) : null),
    setItem: (k, v) => m.set(k, String(v)),
  }
}
const st = fauxStockage()
verifier('aucun favori au départ', lireFavoris(st), [])
verifier('ajout', basculerFavori(64331, st), ['64331'])
verifier('un deuxième favori s’ajoute', basculerFavori(64332, st), ['64331', '64332'])
verifier('estFavori', estFavori(64331, st), true)
verifier('retrait', basculerFavori(64331, st), ['64332'])
verifier('stockage illisible : aucun favori, aucune erreur',
  lireFavoris({ getItem: () => 'pas du json', setItem: () => {} }), [])

/* ------------------------------------------------------------- conversion */
// Deck starter du jeu, format réel (deck/starter/wasp.json, réduit ici).
const starterWasp = {
  name: 'Wasp', version: '0.5.8',
  hero: ['13001a,13001b,13001c'],
  hero_deck: ['13002', '13003', '13003'],
  obligations: ['13026'], nemesis_set: ['13027'], set_aside: [],
  player_deck: ['00000'],
}
// classeDe : « Hero » pour les signatures, l'aspect sinon (comme cards.aspectOf).
const classeDe = (id) => (['13002', '13003'].includes(String(id)) ? 'Hero' : 'Justice')

const entree = {
  id: 63358, nom: 'Hives are Stronger Together',
  cartes: { '13002': 1, '13003': 2, '01062': 2, '01063': 1 },
}
const converti = versDeckMoteur(entree, starterWasp, classeDe)

verifier('le squelette du héros vient du deck du jeu, pas de marvelcdb',
  [converti.hero, converti.hero_deck, converti.obligations, converti.nemesis_set],
  [starterWasp.hero, starterWasp.hero_deck, starterWasp.obligations, starterWasp.nemesis_set])
verifier('les cartes signature sont exclues du player_deck',
  converti.player_deck.filter((id) => id === '13002' || id === '13003'), [])
verifier('les cartes joueur sont répétées selon leur quantité',
  converti.player_deck.slice().sort(), ['01062', '01062', '01063'])
verifier('le player_deck du deck starter est remplacé, jamais concaténé',
  converti.player_deck.includes('00000'), false)
verifier('nom et provenance conservés',
  [converti.name, converti.metadata.url],
  ['Hives are Stronger Together', 'https://marvelcdb.com/decklist/view/63358'])
verifier('version du deck du jeu conservée', converti.version, '0.5.8')

// 26002 : exclusion héritée de deck.html, reprise à l'identique.
verifier('la carte 26002 est ignorée',
  versDeckMoteur({ id: 1, nom: 'x', cartes: { '26002': 1, '01062': 1 } },
    starterWasp, classeDe).player_deck, ['01062'])

// Cohérence : 6 cartes déclarées, 3 signatures reconnues, 3 en pioche.
verifier('conversion cohérente : écart nul', ecartDeConversion(entree, converti), 0)
const bancal = versDeckMoteur(entree, starterWasp, () => 'Justice')
verifier('signature non reconnue : écart non nul',
  ecartDeConversion(entree, bancal) !== 0, true)


/* ------------------------------------------- deck d'un AUTRE heros */
// Le coeur de la fonctionnalite : le starter est celui du heros du SIEGE, les
// cartes viennent du deck marvelcdb de quelqu'un d'autre. Aucune carte
// signature ne doit franchir la frontiere, dans un sens comme dans l'autre.
const starterIronMan = {
  name: 'Iron Man', version: '0.5.8',
  hero: ['01001a,01001b'],
  hero_deck: ['01002', '01003'],
  obligations: ['01044'], nemesis_set: ['01045'], set_aside: ['01004'],
  player_deck: ['01050'],
}
// Deck marvelcdb de Wasp : ses signatures (13002/13003) + de la Justice.
const surIronMan = versDeckMoteur(
  { id: 63358, nom: 'Hives are Stronger Together (Iron Man)', cartes: { '13002': 1, '13003': 2, '01062': 2, '01063': 1 } },
  starterIronMan, classeDe)
verifier('deck d’un autre héros : les signatures du deck source sont écartées',
  surIronMan.player_deck.slice().sort(), ['01062', '01062', '01063'])
verifier('deck d’un autre héros : signatures, obligation et némésis restent celles du siège',
  [surIronMan.hero, surIronMan.hero_deck, surIronMan.obligations, surIronMan.nemesis_set, surIronMan.set_aside],
  [starterIronMan.hero, starterIronMan.hero_deck, starterIronMan.obligations, starterIronMan.nemesis_set, starterIronMan.set_aside])

/* ------------------------------------------------- regles de construction */
const heroDe = (nom, o = {}) => ({
  id: o.id || nom.toLowerCase().replace(/\W+/g, '_'),
  name: nom,
  deck: { hero_deck: Array.from({ length: o.signature ?? 15 }, (_, i) => 'sig' + i),
          metadata: o.metadata || {} },
})
// Catalogue minimal : un identifiant porte son aspect et son type.
const catalogue = {
  jus1: { name: 'For Justice!', class: 'Justice', type: 'Event', traits: [], desc: {} },
  jus2: { name: 'Great Responsibility', class: 'Justice', type: 'Event', traits: [], desc: {} },
  agr1: { name: 'Relentless Assault', class: 'Aggression', type: 'Event', traits: [], desc: {} },
  allie: { name: 'Nick Fury', class: 'Justice', type: 'Ally', traits: [], desc: {} },
  rencontre: { name: 'Magical Suspension', class: '', type: 'Attachment', traits: [], desc: {} },
}
// Bourrage neutre : des cartes BASIQUES toutes differentes, pour atteindre les
// 40 cartes sans buter sur la limite de 3 exemplaires par TITRE.
for (let i = 1; i <= 9; i += 1) {
  catalogue['bas' + i] = { name: 'Basique ' + i, class: 'Basic', type: 'Resource', traits: [], desc: {} }
}
/** n cartes basiques, 3 par titre. */
const bourrage = (n) => Object.fromEntries(
  Array.from({ length: Math.ceil(n / 3) }, (_, i) => ['bas' + (i + 1), Math.min(3, n - 3 * i)]))
const carteDe = (id) => catalogue[id]
// Pioche : { id: nombre } -> la Map attendue par validerDeck.
const pioche = (o) => new Map(Object.entries(o))
const verdict = (hero, o) => validerDeck({ hero, choisies: pioche(o), carte: carteDe })

const spiderMan = heroDe('Spider-Man')
verifier('25 cartes d’un seul aspect sur un héros ordinaire : légal',
  verdict(spiderMan, { jus1: 3, jus2: 3, allie: 3, ...bourrage(16) }).ok, true)
verifier('deux aspects sur un héros qui n’en admet qu’un : refusé',
  verdict(spiderMan, { jus1: 3, jus2: 3, agr1: 3, ...bourrage(16) }).ok, false)
verifier('le message nomme les deux aspects',
  verdict(spiderMan, { jus1: 3, agr1: 3, ...bourrage(19) }).problemes.some((m) => /Justice/.test(m) && /Aggression/.test(m)),
  true)

// Spider-Woman : exactement deux aspects. C'est LE cas ou coller le deck d'un
// autre heros produit une liste mono-aspect, donc illegale pour elle.
const spiderWoman = heroDe('Spider-Woman')
verifier('Spider-Woman : deux aspects, légal',
  verdict(spiderWoman, { jus1: 3, agr1: 3, ...bourrage(19) }).ok, true)
verifier('Spider-Woman : un seul aspect, refusé',
  verdict(spiderWoman, { jus1: 3, jus2: 3, ...bourrage(19) }).ok, false)

// Regles DECLAREES par le heros, via metadata.deckbuilding de son starter.
const fatalis = heroDe('Fatalis', { metadata: { deckbuilding: { types_interdits: ['Ally'] } } })
verifier('héros qui s’interdit les alliés : refusé',
  verdict(fatalis, { allie: 1, jus1: 3, ...bourrage(21) }).ok, false)
const libre = heroDe('Adam Warlock', { metadata: { deckbuilding: { aspects: { min: 0, max: 99 } } } })
verifier('héros aux aspects libres : quatre aspects acceptés',
  verdict(libre, { jus1: 3, jus2: 3, agr1: 3, ...bourrage(16) }).ok, true)

verifier('plus de 3 exemplaires d’un même titre : refusé',
  verdict(spiderMan, { jus1: 4, ...bourrage(21) }).ok, false)
verifier('deck trop petit : refusé',
  verdict(spiderMan, { jus1: 3, ...bourrage(5) }).ok, false)
verifier('carte de rencontre glissée dans la pioche : refusée',
  verdict(spiderMan, { rencontre: 1, jus1: 3, ...bourrage(21) }).problemes
    .some((m) => /Magical Suspension/.test(m)), true)

// Stan Lee (Marvelous) : ses 15 cartes signature sont EMPRUNTEES a d'autres
// heros, donc choisies par le joueur, et elles vivent dans hero_deck. Les
// oublier declarerait tout import a court de 15 cartes.
// 15 signatures empruntees, toutes differentes : la limite de 3 exemplaires
// par titre s'applique aussi a elles.
for (let i = 1; i <= 15; i += 1) {
  catalogue['emp' + i] = { name: 'Signature ' + i, class: 'Hero', type: 'Ally', traits: [], desc: {}, set_name: 'Spider-Man' }
}
const stanLee = heroDe('Stan Lee', { signature: 15 })
const deckStanLee = {
  hero_deck: Array.from({ length: 15 }, (_, i) => 'emp' + (i + 1)),
  player_deck: [...Array(3).fill('jus1'), ...Array(3).fill('jus2'),
    ...Object.entries(bourrage(19)).flatMap(([id, n]) => Array(n).fill(id))],
}
verifier('Stan Lee : les signatures empruntées comptent dans les cartes choisies',
  [...choisiesDuDeck(stanLee, deckStanLee).values()].reduce((a, b) => a + b, 0), 40)
verifier('Stan Lee : un deck complet reste légal',
  validerDeck({ hero: stanLee, choisies: choisiesDuDeck(stanLee, deckStanLee), carte: carteDe }).ok, true)
verifier('un héros ordinaire ne récupère PAS les signatures du hero_deck',
  [...choisiesDuDeck(spiderMan, deckStanLee).values()].reduce((a, b) => a + b, 0), 25)

// Le libelle sert a expliquer le refus a l'import : il doit exister sans i18n.
verifier('règle d’aspect lisible sans traduction',
  typeof reglesAspect(spiderWoman).label === 'string' && reglesAspect(spiderWoman).max === 2, true)

console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
process.exit(echecs === 0 ? 0 : 1)
