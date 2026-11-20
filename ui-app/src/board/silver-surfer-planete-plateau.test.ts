// Silver Surfer « Power Cosmic » : un personnage marqué « à une planète »
// (`pc_planete_actuelle` côté moteur) ne bouge JAMAIS de zone (décision
// utilisateur du 04/11/2026) — c'est le SEUL signal que le plateau peut
// montrer qui prouve que le marqueur existe. PROCESSUS-CARTE.md étape 8 bis :
// le moteur peut être juste (32/32 cas `su0` l'étaient pour Master Planner)
// sans que rien ne se voie à l'écran. Ici, le moteur expose le marqueur via
// `info.ui_marker_object_id` (canal générique, `card.py`), et `zones.ts`
// (`planetesParId`) doit le résoudre jusqu'à l'infobulle (`ScanCard.tsx`).
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const SILVER_SURFER = 1
const ZENN_LA = 2
const NON_MARQUE = 3

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(SILVER_SURFER, 'pc001a', 'Hero', 'Silver Surfer', {
          info: { ui_marker_object_id: ZENN_LA },
        }),
      ],
      allies: [
        carteSurTable(NON_MARQUE, 'pc004', 'Ally', 'Nova Frankie Raye'),
      ],
      environment_area: [carteSurTable(ZENN_LA, 'pc003', 'Environment', 'Zenn-La')],
    })
  )

describe('personnage marqué « à une planète » (infobulle plateau)', () => {
  it('résout le marqueur en nom + image de la carte PLANET', () => {
    const carte = dessinee(monde(), SILVER_SURFER)
    expect(carte?.environnementMarque).toBeDefined()
    expect(carte?.environnementMarque?.nom).toBe('Zenn-La')
  })

  // Cas témoin : sans marqueur, pas d'infobulle — une infobulle montrée à
  // tort serait aussi trompeuse qu'absente à tort.
  it('ne montre rien pour un personnage non marqué', () => {
    const carte = dessinee(monde(), NON_MARQUE)
    expect(carte?.environnementMarque).toBeUndefined()
  })

  // Marqueur pointant vers un object_id qui ne correspond à AUCUNE carte
  // connue (planète pas encore en jeu, ou hors de portée) : pas d'infobulle
  // fausse plutôt qu'un lien mort.
  it('ne montre rien si la carte visée est introuvable', () => {
    const sansZennLa = tableAvec(
      siege({
        area_hero: [
          carteSurTable(SILVER_SURFER, 'pc001a', 'Hero', 'Silver Surfer', {
            info: { ui_marker_object_id: 999 },
          }),
        ],
      })
    )
    expect(dessinee(sansZennLa, SILVER_SURFER)?.environnementMarque).toBeUndefined()
  })
})
