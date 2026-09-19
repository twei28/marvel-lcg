// Le monde minimal pour les tests du plateau manuel.
//
// Reexporte le meme genre de monde que `PagePartie.test.tsx` (`table`), avec
// UNE DIFFERENCE deliberee : celui-ci pose deja une phase du mechant engagee
// (une menace posee sur la manigance principale). Sans un fait a raconter,
// BandeauPhase et DeroulePhase resteraient invisibles de toute facon (aucune
// etape a montrer), et un test « le mode manuel les cache » ne prouverait
// rien : il faut d'abord qu'ils PARLENT en partie ordinaire.
import { carteSurTable, siege, tableAvec } from '../plateau-de-test'
import type { FaitMechant, World } from '../world'

const MANIGANCE_PRINCIPALE = carteSurTable(9, '01097a', 'main_scheme', "The Breakin' and Takin'")

const MENACE_POSEE: FaitMechant = {
  genre: 'menace',
  round_id: 2,
  phase: 'Main Scheme Place Threat',
  cible: "The Breakin' and Takin'",
  cible_id: 9,
  montant: 1,
  restant: 3,
  plafond: 10,
}

/** Un siege avec un heros ET une carte en main : de quoi peupler `zone-main`. */
function heros(nom: string, id: number) {
  return siege({
    area_hero: [carteSurTable(id, `0100${id}a`, 'hero', nom)],
    hand_cards: [carteSurTable(id + 100, `0100${id}b`, 'ally', 'Carte en main')],
  })
}

/**
 * Un monde de test, phase du mechant en cours : de quoi faire apparaitre
 * BandeauPhase et DeroulePhase en partie ordinaire, et verifier qu'un
 * fragment (`{ mode_manuel: true }`) les fait disparaitre.
 */
export function mondeDeTest(fragment: Partial<World> = {}): World {
  return tableAvec(heros('Spider-Man', 1), {
    phase: 'Main Scheme Place Threat',
    round_id: 2,
    villains: [],
    main_scheme: [],
    encounter_deck_size: 0,
    encounter_discard_pile: [],
    area_schemes_main: [MANIGANCE_PRINCIPALE],
    area_schemes_side: [],
    faits_mechant: [MENACE_POSEE],
    ...fragment,
  } as never)
}
