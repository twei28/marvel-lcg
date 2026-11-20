// Sentry / Robert Reynolds (rr001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - rr002 Duality Aspect (permanente, porteuse des compteurs d'équilibre) et rr009 Purposeful Disparity : améliorations attachées au héros ; rr003 C.L.O.C. : allié ;
//    rr004 Cornelius Worth et rr005 The Watchtower : soutiens (la tour peut porter un compteur d'équilibre) ;
//  - rr016 Void : sbire némésis engagé, porteur de rr018 Angel of Death (attachement à un ENNEMI, pas à l'identité) ; rr017 Monster of Antithesis : manigance annexe (paysage) ;
//  - modulaire : rr020 Merged Sentry (sbire engagé, rr022 Newfound Nature attachée à lui) et rr021 External Darkness (manigance annexe, paysage).
// Le dessin d'un attachement à un ennemi est générique (`zones.ts`) : ce cas le vaut pour Sentry.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const SENTRY = 1
const DUALITY = 2
const CLOC = 3
const CORNELIUS = 4
const WATCHTOWER = 5
const DISPARITY = 9
const VOID = 16
const MONSTER = 17
const ANGEL = 18
const EXTERNAL = 21
const MERGED = 20
const NATURE = 22

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(SENTRY, 'rr001a', 'Hero', 'Sentry'),
        carteSurTable(DUALITY, 'rr002', 'Upgrade', 'Duality Aspect', { bind_object_id: SENTRY }),
        carteSurTable(DISPARITY, 'rr009', 'Upgrade', 'Purposeful Disparity', { bind_object_id: SENTRY }),
      ],
      allies: [carteSurTable(CLOC, 'rr003', 'Ally', 'C.L.O.C.')],
      supports: [carteSurTable(CORNELIUS, 'rr004', 'Support', 'Cornelius Worth'), carteSurTable(WATCHTOWER, 'rr005', 'Support', 'The Watchtower')],
      engaged_enemies: [
        carteSurTable(VOID, 'rr016', 'Minion', 'Void'),
        carteSurTable(ANGEL, 'rr018', 'Attachment', 'Angel of Death', { bind_object_id: VOID }),
        carteSurTable(MERGED, 'rr020', 'Minion', 'Merged Sentry'),
        carteSurTable(NATURE, 'rr022', 'Attachment', 'Newfound Nature', { bind_object_id: MERGED }),
      ],
    }),
    { area_schemes_side: [carteSurTable(MONSTER, 'rr017', 'SideScheme', 'Monster of Antithesis'), carteSurTable(EXTERNAL, 'rr021', 'SideScheme', 'External Darkness')] },
  )

describe('Sentry : ce que la table dessine', () => {
  it("dessine Sentry, ses deux améliorations (portées par l'identité), C.L.O.C., Cornelius Worth et The Watchtower", () => {
    for (const id of [SENTRY, DUALITY, DISPARITY, CLOC, CORNELIUS, WATCHTOWER]) expect(dessinee(monde(), id)).toBeDefined()
    for (const id of [DUALITY, DISPARITY]) expect(dessinee(monde(), id)?.portePar).toBe(SENTRY)
  })
  it('dessine Void avec Angel of Death attaché à lui, Merged Sentry avec Newfound Nature, et les deux manigances annexes', () => {
    for (const id of [VOID, ANGEL, MERGED, NATURE, MONSTER, EXTERNAL]) expect(dessinee(monde(), id)).toBeDefined()
    expect(dessinee(monde(), ANGEL)?.portePar).toBe(VOID)
    expect(dessinee(monde(), NATURE)?.portePar).toBe(MERGED)
    expect(dessinee(monde(), ANGEL)?.codeCarte).toBe('rr018')
  })
})
