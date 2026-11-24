// Shang-Chi (DesignHacker, SEALED, `ch001a`-`ch021`) : ce que le plateau DESSINE une fois les cartes résolues.
//
// `Fusion/marvel-lcg-src/tools/cas/shang_chi.py` et `shang_chi_b.py` prouvent ce que le moteur FAIT ; ce fichier prouve ce
// que le joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). Les cartes du pack qui changent ce qu'on VOIT :
//   - ch002 State of Flow : les attaques jouées sont glissées FACE VISIBLE sous le soutien (la pile du Flow) : le joueur doit
//     pouvoir LIRE la carte du dessus, c'est elle qui active le Flow suivant (même mécanisme que Imprisoned on Chandilar) ;
//   - ch015 Stark Nunchaku / ch016 Metal Bracers / ch017 Martial Mastery : compteurs charge / reflet / chi ;
//   - ch019 Zheng Zu : compteurs mystiques sur le sbire némésis ; ch020 The Life Stealer : manigance annexe, compteurs mystiques.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const PILE = 2
const BAS = 3
const DESSUS = 4
const NUNCHAKU = 5
const BRACELETS = 6
const MAITRISE = 7
const ZHENG = 10
const VOLEUR = 11

const heros = () => carte(IDENTITE, 'ch001a', 'Hero', 'Shang-Chi')

describe('ch002 State of Flow : la pile d attaques est dessinée', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros()],
        supports: [
          carte(PILE, 'ch002', 'Support', 'State of Flow'),
          carte(BAS, 'ch011', 'Event', 'Chi Jabs', { bind_object_id: PILE }),
          carte(DESSUS, 'ch009', 'Event', 'Dragon Strike', { bind_object_id: PILE }),
        ],
      })
    )

  it('dessine le soutien et les deux attaques empilées dessous', () => {
    expect(dessinee(monde(), PILE)).toBeDefined()
    expect(dessinee(monde(), BAS)).toBeDefined()
    expect(dessinee(monde(), DESSUS)).toBeDefined()
  })

  it('les attaques de la pile sont FACE VISIBLE (on lit la carte du dessus) et suivent le soutien dans l ordre', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(BAS)).toBe(rang(PILE) + 1)
    expect(rang(DESSUS)).toBe(rang(PILE) + 2)
    expect(dessinee(monde(), DESSUS)?.facedown).toBe(false)
    expect(dessinee(monde(), DESSUS)?.peeking).toBe(false)
    expect(dessinee(monde(), DESSUS)?.codeCarte).toBe('ch009')
  })

  it('une pile vide ne dessine que le soutien', () => {
    const vide = tableAvec(siege({ area_hero: [heros()], supports: [carte(PILE, 'ch002', 'Support', 'State of Flow')] }))
    expect(dessinee(vide, PILE)).toBeDefined()
    expect(cartesDessinees(vide).filter((c) => c.id === BAS || c.id === DESSUS)).toHaveLength(0)
  })
})

describe('ch015 / ch016 / ch017 : les compteurs des améliorations sont dessinés', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [
          heros(),
          carte(NUNCHAKU, 'ch015', 'Upgrade', 'Stark Nunchaku', { bind_object_id: IDENTITE, info: { c_charge: 3 } }),
          carte(BRACELETS, 'ch016', 'Upgrade', 'Metal Bracers', { bind_object_id: IDENTITE, info: { c_reflection: 2 } }),
          carte(MAITRISE, 'ch017', 'Upgrade', 'Martial Mastery', { bind_object_id: IDENTITE, info: { c_chi: 3 } }),
        ],
      })
    )

  it('3 charges sur Stark Nunchaku', () => {
    expect(dessinee(monde(), NUNCHAKU)?.compteurs.charge).toBe(3)
  })

  it('2 reflets sur Metal Bracers', () => {
    expect(dessinee(monde(), BRACELETS)?.compteurs.reflection).toBe(2)
  })

  it('3 chi sur Martial Mastery', () => {
    expect(dessinee(monde(), MAITRISE)?.compteurs.chi).toBe(3)
  })
})

describe('ch019 Zheng Zu / ch020 The Life Stealer : compteurs mystiques', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [heros()],
        engaged_enemies: [carte(ZHENG, 'ch019', 'Minion', 'Zheng Zu', { info: { c_mystic: 2 } })],
      }),
      { area_schemes_side: [carte(VOLEUR, 'ch020', 'SideScheme', 'The Life Stealer', { info: { c_mystic: 1, threat: 4 } })] }
    )

  it('Zheng Zu est dessiné avec ses 2 compteurs mystiques', () => {
    expect(dessinee(monde(), ZHENG)).toBeDefined()
    expect(dessinee(monde(), ZHENG)?.compteurs.mystic).toBe(2)
  })

  it('The Life Stealer est dessinée avec son compteur mystique', () => {
    expect(dessinee(monde(), VOLEUR)).toBeDefined()
    expect(dessinee(monde(), VOLEUR)?.compteurs.mystic).toBe(1)
  })
})
