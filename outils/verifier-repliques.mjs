// Vérifie les RÉPLIQUES des héros (public/js/prepare/repliques-heros.js) : la
// phrase qui claque sur la carte au recrutement (liste de l'utilisateur,
// 11/09/2026, officiels et homebrew).
//
// Ce qui peut casser en silence :
//   - une clé qui n'est pas un identifiant de deck (« lady_thor » au lieu de
//     `thor_jane_foster`) : le héros retomberait sur « BAM ! » sans un mot ;
//   - un pool vide, un doublon, un SNIKT ou un THWIP oublié ;
//   - un tirage qui répète la dernière réplique alors qu'il en a d'autres.
//
// Usage : node outils/verifier-repliques.mjs   (depuis la racine du dépôt)
import { readdirSync } from 'node:fs'
const m = await import('../Fusion/marvel-lcg-src/public/js/prepare/repliques-heros.js')
const decks = new Set(readdirSync('Fusion/marvel-lcg-src/deck/starter')
  .filter((f) => f.endsWith('.json')).map((f) => f.slice(0, -5)))
const dire = (nom, obtenu, attendu) => {
  const ok = JSON.stringify(obtenu) === JSON.stringify(attendu)
  console.log(`  ${ok ? 'ok   ' : 'ECHEC'} ${nom} -> ${JSON.stringify(obtenu)}`)
  return ok ? 0 : 1
}
let ko = 0
const cles = Object.keys(m.REPLIQUES)
ko += dire('toutes les cles sont des decks starter', cles.filter((c) => !decks.has(c)), [])
ko += dire('aucun pool vide', cles.filter((c) => m.REPLIQUES[c].length === 0), [])
ko += dire('aucun doublon dans un pool',
  cles.filter((c) => new Set(m.REPLIQUES[c]).size !== m.REPLIQUES[c].length), [])
ko += dire('aucune phrase vide', cles.filter((c) => m.REPLIQUES[c].some((r) => !r.trim())), [])
const OFFICIELS = ['adam_warlock','angel','ant_man','bishop','black_panther','black_panther_shuri','black_widow','cable',
  'captain_america','captain_marvel','colossus','cyclops','daredevil','deadpool','doctor_strange','domino','drax','echo',
  'falcon','gambit','gamora','ghost_spider','groot','hawkeye','hercules','hulk','hulkling','iceman','iron_man','ironheart',
  'jessica_jones','jubilee','luke_cage','magik','magneto','maria_hill','ms_marvel','nebula','nick_fury','nightcrawler',
  'nova','phoenix','psylocke','quicksilver','rocket_raccoon','rogue','scarlet_witch','shadowcat','she_hulk','silk','sp_dr',
  'spectrum','spider_ham','spider_man','spider_man_miles_morales','spider_woman','star_lord','storm','thor','tigra',
  'valkyrie','venom','vision','war_machine','wasp','winter_soldier','wolverine','wonder_man','x_23']
ko += dire('les 69 heros officiels ont leur pool', OFFICIELS.filter((c) => !m.REPLIQUES[c]), [])
const SNIKT = ['wolverine', 'x_23', 'albert', 'wolverine_x23']
ko += dire('SNIKT chez les Wolverine', SNIKT.filter((c) => !(m.REPLIQUES[c] || []).includes('SNIKT !')), [])
const THWIP = ['spider_man', 'spider_man_miles_morales', 'ghost_spider', 'silk', 'spider_ham', 'sp_dr',
  'spider_man_rainy', 'spider_man_2099', 'spider_man_noir', 'armored_spidey', 'scarlet_spider',
  'superior_spider_man']
ko += dire('THWIP chez les tisseurs', THWIP.filter((c) => !(m.REPLIQUES[c] || []).includes('THWIP !')), [])
// Le tirage : jamais la derniere quand il y a le choix, et la seule quand il n'y en a qu'une.
const pool = ['a', 'b', 'c']
let repete = 0
for (let i = 0; i < 300; i += 1) if (m.choisirReplique(pool, 'b', Math.random) === 'b') repete += 1
ko += dire('le tirage ne repete jamais la derniere (300 tirages)', repete, 0)
ko += dire('un pool d une phrase la rend toujours', m.choisirReplique(['seule'], 'seule', Math.random), 'seule')
ko += dire('sans derniere, tout le pool est possible',
  new Set(Array.from({ length: 300 }, () => m.choisirReplique(pool, undefined, Math.random))).size, 3)
ko += dire('taille : courte', m.classeTaille('SNIKT !'), '')
ko += dire('taille : moyenne', m.classeTaille('I can do this all day.'), 'ono-moyenne')
ko += dire('taille : longue', m.classeTaille("Why don't you pick on someone your own size?"), 'ono-longue')
ko += dire('taille : 62 caracteres, donc tres longue', m.classeTaille('Do you guys just put the word quantum in front of everything?'), 'ono-tres-longue')
ko += dire('taille : tres longue', m.classeTaille("I'm not seeking penance for what I've done. I'm asking forgiveness for what I'm about to do."), 'ono-tres-longue')
console.log(ko ? `ECHECS : ${ko}` : 'ECHECS : 0')
process.exit(ko ? 1 : 0)
