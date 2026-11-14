// Black Queen (Hellfire Hunt, Dipsome, `hf`, scénario 3) + module Darkhold : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//
// Quatre choses visibles changent dans ce scénario :
//   - l'environnement recto-verso jour / nuit (hf407a Under the Moonlight / hf407b Beneath the Sun) porte des compteurs « time »
//     que le joueur doit LIRE : ils décident du retournement, de la menace de hf406b et du coût des Actions de héros ;
//   - hf362 Darkhold est un attachement posé sur Selene, avec ses compteurs « darkspell » (Uses 2) ;
//   - hf361 Darkhold Dwarf garde SOUS LUI, face visible, le sort glissé (tuck) : le joueur doit voir ce qu'il révélera à sa défaite ;
//   - hf363 Eternal Manipulation s'attache à un allié qui devient un sbire.
// Le moteur émet les cartes glissées à la suite de leur hôte, liées par `bind_object_id` (`to_descriptor.py`, `placed_card`).
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const SELENE = 10
const DARKHOLD = 11
const COMPLOT = 20
const ENV_NUIT = 30
const DWARF = 40
const SORT_SOUS_DWARF = 41
const ALLIE_SBIRE = 50
const MANIPULATION = 51

const monde = (env: { code: string; nom: string }) =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(IDENTITE, '01001a', 'Hero', 'Spider-Man')],
      engaged_enemies: [
        carteSurTable(DWARF, 'hf361', 'Minion', 'Darkhold Dwarf'),
        carteSurTable(SORT_SOUS_DWARF, 'hf365', 'Treachery', 'Soul Siphon', { bind_object_id: DWARF }),
        carteSurTable(ALLIE_SBIRE, 'minion', 'Minion', 'Mockingbird', { pic_id: '01083' }),
        carteSurTable(MANIPULATION, 'hf363', 'Attachment', 'Eternal Manipulation', { bind_object_id: ALLIE_SBIRE }),
      ],
    }),
    {
      area_villain: [
        carteSurTable(SELENE, 'hf401', 'EncounterVillain', 'Selene'),
        carteSurTable(DARKHOLD, 'hf362', 'Attachment', 'Darkhold', { bind_object_id: SELENE, info: { c_darkspell: 2 } }),
      ],
      area_schemes_main: [carteSurTable(COMPLOT, 'hf406b', 'MainScheme', 'Ascending to Godhood', { info: { k_threat: 4 } })],
      area_environment: [carteSurTable(ENV_NUIT, env.code, 'Environment', env.nom, { info: { c_time: 3 } })],
    }
  )

const NUIT = { code: 'hf407a', nom: 'Under the Moonlight' }
const JOUR = { code: 'hf407b', nom: 'Beneath the Sun' }

describe('hf407a / hf407b : l environnement jour / nuit', () => {
  it('dessine la NUIT avec ses 3 compteurs time', () => {
    expect(dessinee(monde(NUIT), ENV_NUIT)).toBeDefined()
    expect(dessinee(monde(NUIT), ENV_NUIT)?.codeCarte).toBe('hf407a')
    expect(dessinee(monde(NUIT), ENV_NUIT)?.compteurs.time).toBe(3)
  })

  it('dessine le JOUR (autre face de la même carte) avec ses compteurs time', () => {
    expect(dessinee(monde(JOUR), ENV_NUIT)?.codeCarte).toBe('hf407b')
    expect(dessinee(monde(JOUR), ENV_NUIT)?.compteurs.time).toBe(3)
  })
})

describe('hf362 Darkhold sur Selene', () => {
  it('dessine le Darkhold, porté par Selene, avec ses 2 compteurs darkspell', () => {
    expect(dessinee(monde(NUIT), DARKHOLD)).toBeDefined()
    expect(dessinee(monde(NUIT), DARKHOLD)?.portePar).toBe(SELENE)
    expect(dessinee(monde(NUIT), DARKHOLD)?.compteurs.darkspell).toBe(2)
  })
})

describe('hf361 Darkhold Dwarf et son sort glissé dessous', () => {
  it('dessine le sort glissé, juste derrière le sbire, FACE VISIBLE', () => {
    const vues = cartesDessinees(monde(NUIT))
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(NUIT), SORT_SOUS_DWARF)).toBeDefined()
    expect(rang(SORT_SOUS_DWARF)).toBe(rang(DWARF) + 1)
    expect(dessinee(monde(NUIT), SORT_SOUS_DWARF)?.facedown).toBe(false)
    expect(dessinee(monde(NUIT), SORT_SOUS_DWARF)?.codeCarte).toBe('hf365')
  })
})

describe('hf363 Eternal Manipulation : l allié devenu sbire', () => {
  it('dessine le sbire (image de l allié) et l attachement posé dessus', () => {
    expect(dessinee(monde(NUIT), ALLIE_SBIRE)).toBeDefined()
    expect(dessinee(monde(NUIT), MANIPULATION)).toBeDefined()
    expect(dessinee(monde(NUIT), MANIPULATION)?.portePar).toBe(ALLIE_SBIRE)
  })
})
