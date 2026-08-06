// Vérifie les fonctions pures du module de recherche de decks MarvelCDB.
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

const { filtrer } = await mod('filtres.js')
const { lireFavoris, estFavori, basculerFavori } = await mod('favoris.js')
const { versDeckMoteur, ecartDeConversion } = await mod('conversion.js')

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

console.log(echecs === 0 ? '\nTOUT PASSE' : `\n${echecs} ECHEC(S)`)
process.exit(echecs === 0 ? 0 : 1)
