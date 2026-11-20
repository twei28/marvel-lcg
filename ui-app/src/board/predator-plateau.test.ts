// Predator (RyCoRan, `pd001a`-`pd030`) : ce que le plateau DESSINE (PROCESSUS-CARTE etape 8 bis).
// `tools/cas/predator*.py` prouvent ce que le moteur FAIT. Ici, ce que le joueur REGARDE :
//   - pd002 Infralocked : UNE amelioration qui change d'hote (sur l'identite, puis sur un sbire) ;
//   - pd001a : carte d'etat Cloaked sur le HEROS ;
//   - pd010 / pd011 : compteurs « skull » et « glyph » ;
//   - pd003 Xenomorph : SBIRE DE JOUEUR engage ;
//   - pd009 Honor Hunt : manigance annexe de joueur, puis en vitrine de victoire ;
//   - pd026 / pd029 : Chopper (manigance annexe Permanent) et M134 Minigun attachee a Dutch.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const INFRALOCKED = 2
const CAMOUFLE = 3
const SBIRE = 20
const SALLE = 30
const ARME = 31
const XENO = 40
const CHASSE = 50
const CHOPPER = 60
const DUTCH = 70
const MINIGUN = 71

const identite = () => carte(IDENTITE, 'pd001a', 'Hero', 'Predator')

describe('pd002 Infralocked : une seule amelioration, deux hotes possibles', () => {
  it('au depart elle est dessinee sur l identite', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          identite(),
          carte(INFRALOCKED, 'pd002', 'Upgrade', 'Infralocked', { bind_object_id: IDENTITE }),
        ],
      })
    )
    expect(dessinee(monde, INFRALOCKED)).toBeDefined()
    expect(dessinee(monde, INFRALOCKED)?.portePar).toBe(IDENTITE)
    expect(dessinee(monde, INFRALOCKED)?.kind).toBe('upgrade')
  })

  it('attachee a un sbire engage, elle est dessinee sur CE sbire', () => {
    const monde = tableAvec(
      siege({
        area_hero: [identite()],
        engaged_enemies: [
          carte(SBIRE, '01103', 'Minion', 'Shocker'),
          carte(INFRALOCKED, 'pd002', 'Upgrade', 'Infralocked', { bind_object_id: SBIRE }),
        ],
      })
    )
    expect(dessinee(monde, INFRALOCKED)).toBeDefined()
    expect(dessinee(monde, INFRALOCKED)?.portePar).toBe(SBIRE)
  })
})

describe('pd001a : carte Cloaked sur Predator', () => {
  it('la carte d etat est dessinee, portee par le heros', () => {
    const monde = tableAvec(
      siege({ area_hero: [identite(), carte(CAMOUFLE, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: IDENTITE })] })
    )
    expect(dessinee(monde, CAMOUFLE)).toBeDefined()
    expect(dessinee(monde, CAMOUFLE)?.kind).toBe('status')
    expect(dessinee(monde, CAMOUFLE)?.codeCarte).toBe('cloaked')
    expect(dessinee(monde, CAMOUFLE)?.portePar).toBe(IDENTITE)
  })
})

describe('pd010 Yautja Trophy Room, pd011 Self Destruct : compteurs', () => {
  it('le soutien porte ses crânes, l amélioration ses glyphes et elle est inclinée', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          identite(),
          carte(ARME, 'pd011', 'Upgrade', 'Self Destruct', { bind_object_id: IDENTITE, is_ready: false, info: { c_glyph: 2 } }),
        ],
        supports: [carte(SALLE, 'pd010', 'Support', 'Yautja Trophy Room', { info: { c_skull: 3 } })],
      })
    )
    expect(dessinee(monde, SALLE)?.compteurs.skull).toBe(3)
    expect(dessinee(monde, ARME)?.compteurs.glyph).toBe(2)
    expect(dessinee(monde, ARME)?.exhausted).toBe(true)
  })
})

describe('pd003 Xenomorph : sbire de joueur', () => {
  it('il est dessine parmi les ennemis engages avec son proprietaire', () => {
    const monde = tableAvec(
      siege({ area_hero: [identite()], engaged_enemies: [carte(XENO, 'pd003', 'PlayerMinion', 'Xenomorph')] })
    )
    expect(dessinee(monde, XENO)).toBeDefined()
  })
})

describe('pd009 Honor Hunt : manigance annexe de joueur', () => {
  it('en jeu, elle est dessinee avec ses 5 menaces', () => {
    const monde = tableAvec(siege({ area_hero: [identite()] }), {
      area_schemes_side: [carte(CHASSE, 'pd009', 'PlayerSideScheme', 'Honor Hunt', { info: { k_threat: 5 } })],
    })
    expect(dessinee(monde, CHASSE)).toBeDefined()
    expect(dessinee(monde, CHASSE)?.menace).toBe(5)
  })

  it('vaincue, elle est dessinee dans la pile de victoire', () => {
    const monde = tableAvec(siege({ area_hero: [identite()] }), {
      victory_display: [carte(CHASSE, 'pd009', 'PlayerSideScheme', 'Honor Hunt')],
    })
    expect(dessinee(monde, CHASSE)).toBeDefined()
  })
})

describe('pd026 Chopper, pd027 Dutch Schaefer, pd029 M134 Minigun', () => {
  const monde = () =>
    tableAvec(
      siege({
        area_hero: [identite()],
        engaged_enemies: [
          carte(DUTCH, 'pd027', 'Minion', 'Dutch Schaefer'),
          carte(MINIGUN, 'pd029', 'Attachment', 'M134 Minigun', { bind_object_id: DUTCH }),
        ],
      }),
      { area_schemes_side: [carte(CHOPPER, 'pd026', 'SideScheme', 'Chopper', { info: { k_threat: 3 } })] }
    )

  it('Chopper est dessinee avec 3 menaces', () => {
    expect(dessinee(monde(), CHOPPER)).toBeDefined()
    expect(dessinee(monde(), CHOPPER)?.menace).toBe(3)
  })

  it('M134 Minigun est dessinee, portee par Dutch', () => {
    expect(dessinee(monde(), MINIGUN)).toBeDefined()
    expect(dessinee(monde(), MINIGUN)?.portePar).toBe(DUTCH)
  })
})
