// Étape 8 bis de PROCESSUS-CARTE pour le scénario Kree Sentry (Galactic Storm, lot GS-4, 20/10/2026) : ce que les cartes
// DESSINENT. Sentry's Grasp (gs082) s'attache à n'importe quel personnage (allié Rick Jones, identité, sbire) et porte des
// compteurs de DÉGÂTS (« attack this card as if it were a minion ») ; Optic Blast Cannon / Repulsor Blast Unit s'attachent
// à Kree Sentry ; Imperial Guard pose un environnement SETTING dès la mise en place.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const HEROS = 1
const RICK = 20
const POIGNE_RICK = 21
const POIGNE_HEROS = 22
const SBIRE = 30
const POIGNE_SBIRE = 31
const SENTRY = 40
const OPTIC = 41
const ENV = 50

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(HEROS, '01001a', 'Hero', 'Spider-Man'),
        carteSurTable(POIGNE_HEROS, 'gs082', 'Attachment', "Sentry's Grasp", { bind_object_id: HEROS }),
      ],
      allies: [
        carteSurTable(RICK, 'gs081', 'Ally', 'Rick Jones'),
        carteSurTable(POIGNE_RICK, 'gs082', 'Attachment', "Sentry's Grasp", {
          bind_object_id: RICK,
          info: { c_damage: 2 },
        }),
      ],
      engaged_enemies: [
        carteSurTable(SBIRE, '01103', 'Minion', 'Shocker'),
        carteSurTable(POIGNE_SBIRE, 'gs082', 'Attachment', "Sentry's Grasp", { bind_object_id: SBIRE }),
      ],
      environment_area: [carteSurTable(ENV, 'gs091', 'Environment', 'Disciplined Training')],
    }),
    {
      area_villain: [
        carteSurTable(SENTRY, 'gs076', 'Villain', 'Kree Sentry'),
        carteSurTable(OPTIC, 'gs083', 'Attachment', 'Optic Blast Cannon', { bind_object_id: SENTRY }),
      ],
    }
  )

describe('Kree Sentry : cartes dessinées', () => {
  it('dessine Rick Jones et la Poigne attachée à lui', () => {
    expect(dessinee(monde(), RICK)).toBeDefined()
    expect(dessinee(monde(), POIGNE_RICK)).toBeDefined()
  })

  it('dessine la Poigne attachée à l\'identité du héros', () => {
    expect(dessinee(monde(), POIGNE_HEROS)).toBeDefined()
  })

  it('dessine la Poigne attachée à un sbire engagé', () => {
    expect(dessinee(monde(), POIGNE_SBIRE)).toBeDefined()
  })

  it('montre les dégâts posés sur une Poigne comme un compteur « damage »', () => {
    const poigne = dessinee(monde(), POIGNE_RICK)
    expect(Object.values(poigne?.compteurs ?? {})).toContain(2)
  })

  it('dessine Optic Blast Cannon attaché à Kree Sentry', () => {
    expect(dessinee(monde(), OPTIC)).toBeDefined()
  })

  it('dessine l\'environnement Imperial Guard en jeu', () => {
    expect(dessinee(monde(), ENV)).toBeDefined()
  })

  it('témoin : une carte absente de la table n\'est pas dessinée', () => {
    expect(dessinee(monde(), 999)).toBeUndefined()
  })
})
