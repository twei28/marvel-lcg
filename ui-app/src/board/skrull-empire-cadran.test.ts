// L'environnement Skrull Empire (pack custom skrull_menace, scénario Skrull
// Empire) porte le cadran de PV des méchants : « The villains in this scenario
// do not have a hit point dial. Instead, the Skrull Empire environment has a
// hit point dial » (livret p. 8). Décision de l'utilisateur (15/10/2026) : un
// VRAI cadran de PV, pas un simple compteur de dégâts.
//
// Le moteur (environment.py) publie `cadran_pv`, `health` et `max_health` sur
// le SEUL environnement qui déclare son cadran ; les dégâts restent stockés en
// jetons `k_damage`. Le plateau doit alors dessiner la pastille et la jauge de
// PV, et ne plus montrer les dégâts comme un compteur à part.
import { describe, expect, it } from 'vitest'
import { catalogueVide } from './catalogue'
import { toScanCard } from './card-model'
import { carteSurTable } from './plateau-de-test'

const contexte = () => ({ playerId: 0, actives: new Set<number>(), catalogue: catalogueVide })

const empire = (info: Record<string, number>) =>
  carteSurTable(7, 'sk086', 'Environment', 'Skrull Empire', { info })

describe("le cadran de PV de l'environnement Skrull Empire", () => {
  it('montre les PV restants sur le maximum', () => {
    const carte = toScanCard(empire({ cadran_pv: 1, health: 20, max_health: 28, k_damage: 8 }), contexte())
    expect(carte.allyHp).toBe('20/28')
  })

  it('dessine une jauge de PV, sans alarme (c est le camp du mechant)', () => {
    const jauge = toScanCard(empire({ cadran_pv: 1, health: 20, max_health: 28, k_damage: 8 }), contexte()).jauge
    expect(jauge?.genre).toBe('pv')
    expect(jauge?.alarme).toBe(false)
    expect(jauge?.texte).toBe('20 / 28')
  })

  it('ne recompte pas les degats en compteur a part', () => {
    const carte = toScanCard(empire({ cadran_pv: 1, health: 20, max_health: 28, k_damage: 8 }), contexte())
    expect((carte.counters ?? []).map((c) => c.cle)).not.toContain('damage')
  })

  // Témoin : un environnement ordinaire, sans cadran déclaré, ne gagne rien.
  it('TEMOIN : un environnement sans cadran ne montre pas de PV', () => {
    const autre = carteSurTable(8, '21100a', 'Environment', 'Avengers Tower', { info: { k_damage: 3 } })
    expect(toScanCard(autre, contexte()).allyHp).toBeUndefined()
  })

  // Les mechants du scenario n'ont pas de cadran : leur pastille ne doit pas
  // dire « INF » (invulnerable), elle disparait.
  it('le mechant marque pv_sur_environnement ne montre ni PV ni jauge', () => {
    const dorrek = carteSurTable(9, 'sk070', 'EncounterVillain', 'Emperor Dorrek I', {
      info: { is_infinite_health: 1, health: 1, max_health: 0, pv_sur_environnement: 1 },
    })
    const carte = toScanCard(dorrek, contexte())
    expect(carte.allyHp).toBeUndefined()
    expect(carte.jauge).toBeUndefined()
  })

  // Temoin : un mechant invulnerable ordinaire (Collector) garde son « INF ».
  it('TEMOIN : un mechant a PV infinis sans marque garde INF', () => {
    const collector = carteSurTable(10, '16080b', 'EncounterVillain', 'Collector', {
      info: { is_infinite_health: 1, health: 1, max_health: 0 },
    })
    expect(toScanCard(collector, contexte()).allyHp).toBe('∞')
  })
})
