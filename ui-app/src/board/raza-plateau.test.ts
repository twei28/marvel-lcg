// Raza Longknife (Starjammers, rl001a) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE, leçon Contingency Plan).
//
// New Host (rl016) s'attache à un SBIRE ennemi, et Shi'ar Host (rl015) reçoit un attachement tiré de la défausse
// rencontre : deux attachements posés sur un sbire engagé, plus les améliorations TECH / WEAPON de Raza sur son identité
// (Alien Augmentations les compte). Le moteur les émet à la suite de leur hôte, liés par `bind_object_id`
// (modèle `attachement-en-chaine.test.ts`) : un attachement non dessiné serait invisible alors que sa règle s'applique.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const RAZA = 1
const BLASTER = 2
const SABRE = 3
const SBIRE = 40
const NEW_HOST = 41
const SHIAR_HOST = 42
const ATTACHEMENT = 43

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(RAZA, 'rl001a', 'Hero', 'Raza Longknife'),
        carteSurTable(BLASTER, 'rl010', 'Upgrade', "Raza's Blaster", { bind_object_id: RAZA }),
        carteSurTable(SABRE, 'rl011', 'Upgrade', "Raza's Sabre", { bind_object_id: RAZA }),
      ],
      engaged_enemies: [
        carteSurTable(SBIRE, '01101', 'Minion', 'Hydra Mercenary'),
        carteSurTable(NEW_HOST, 'rl016', 'Attachment', 'New Host', { bind_object_id: SBIRE }),
        carteSurTable(SHIAR_HOST, 'rl015', 'Minion', "Shi'ar Host"),
        carteSurTable(ATTACHEMENT, '01163', 'Attachment', 'Genetically Enhanced', { bind_object_id: SHIAR_HOST }),
      ],
    }),
  )

describe('Raza, améliorations sur son identité', () => {
  it('dessine Raza et ses deux armes, portées par lui', () => {
    expect(dessinee(monde(), RAZA)).toBeDefined()
    expect(dessinee(monde(), BLASTER)?.portePar).toBe(RAZA)
    expect(dessinee(monde(), SABRE)?.portePar).toBe(RAZA)
  })
})

describe('New Host et Shi\'ar Host, attachements posés sur un sbire', () => {
  it('dessine le sbire et New Host qui lui est attaché, juste derrière lui', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), SBIRE)).toBeDefined()
    expect(dessinee(monde(), NEW_HOST)).toBeDefined()
    expect(rang(NEW_HOST)).toBe(rang(SBIRE) + 1)
  })

  it('dessine Shi\'ar Host et l\'attachement tiré de la défausse rencontre, juste derrière lui', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), SHIAR_HOST)).toBeDefined()
    expect(dessinee(monde(), ATTACHEMENT)).toBeDefined()
    expect(rang(ATTACHEMENT)).toBe(rang(SHIAR_HOST) + 1)
  })
})
