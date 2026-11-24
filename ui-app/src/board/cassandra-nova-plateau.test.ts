// Cassandra Nova (Hellfire Hunt, Dipsome, `hf`, scénario 5) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//
// Ce qui change à l'œil dans ce scénario :
//   - les compteurs « Cassandra Controls » sur l'IDENTITÉ du joueur (le coeur de la mécanique : c'est ce que le joueur doit pouvoir compter) ;
//   - hf371 Psychic Aegis, attachée au vilain (Setup) ; hf372 False Reality, attachée au COMPLOT PRINCIPAL ; hf373 Mind Maze, attachée à l'identité ;
//   - l'environnement hf607 Cassandra Domination, en jeu dès la mise en place ;
//   - l'obligation hf608 / hf610, posée dans la zone du joueur.
import { afterEach, describe, expect, it } from 'vitest'
import { nomDeCompteur } from './compteurs-fr'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const OBLIGATION = 2
const MAZE = 3
const NOVA = 10
const AEGIS = 11
const COMPLOT = 20
const REALITE = 21
const DOMINATION = 30

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker', { info: { c_cassandra_controls: 2 } }),
        carteSurTable(MAZE, 'hf373', 'Attachment', 'Mind Maze', { bind_object_id: IDENTITE }),
      ],
      obligations_area: [carteSurTable(OBLIGATION, 'hf610', 'Obligation', 'Psychic Control')],
    }),
    {
      area_villain: [
        carteSurTable(NOVA, 'hf601', 'EncounterVillain', 'Cassandra Nova'),
        carteSurTable(AEGIS, 'hf371', 'Attachment', 'Psychic Aegis', { bind_object_id: NOVA }),
      ],
      area_schemes_main: [
        carteSurTable(COMPLOT, 'hf604b', 'MainScheme', 'Diplomatic Sabotage', { info: { k_threat: 1 } }),
        carteSurTable(REALITE, 'hf372', 'Attachment', 'False Reality', { bind_object_id: COMPLOT }),
      ],
      area_environment: [carteSurTable(DOMINATION, 'hf607', 'Environment', 'Cassandra Domination')],
    }
  )

afterEach(() => window.localStorage.clear())

describe('Cassandra Controls : les compteurs sont lisibles sur l identité', () => {
  it('dessine les 2 compteurs posés sur l identité', () => {
    expect(dessinee(monde(), IDENTITE)?.compteurs.cassandra_controls).toBe(2)
  })

  it('TÉMOIN : sans compteur, rien n est dessiné sur l identité', () => {
    const sans = tableAvec(siege({ area_hero: [carteSurTable(IDENTITE, '01001b', 'AlterEgo', 'Peter Parker')] }))
    expect(dessinee(sans, IDENTITE)?.compteurs.cassandra_controls).toBeUndefined()
  })

  it('nomme le compteur en français (« contrôle de Cassandra »), en anglais il garde son nom du moteur', () => {
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(nomDeCompteur('cassandra_controls')).toBe('contrôle de Cassandra')
  })
})

describe('les cartes attachées sont toutes dessinées', () => {
  it('Psychic Aegis est dessinée, portée par Cassandra Nova', () => {
    expect(dessinee(monde(), AEGIS)).toBeDefined()
    expect(dessinee(monde(), AEGIS)?.portePar).toBe(NOVA)
  })

  it('False Reality est dessinée, portée par le COMPLOT PRINCIPAL', () => {
    expect(dessinee(monde(), REALITE)).toBeDefined()
    expect(dessinee(monde(), REALITE)?.portePar).toBe(COMPLOT)
  })

  it('Mind Maze est dessinée, portée par l identité', () => {
    expect(dessinee(monde(), MAZE)?.portePar).toBe(IDENTITE)
  })

  it('Cassandra Domination et l obligation Psychic Control sont sur la table', () => {
    expect(dessinee(monde(), DOMINATION)).toBeDefined()
    expect(dessinee(monde(), OBLIGATION)).toBeDefined()
    expect(cartesDessinees(monde()).length).toBeGreaterThanOrEqual(8)
  })
})
