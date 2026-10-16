// Baxter Stockman (TMNT, `tx`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `tools/cas/tmnt_baxter.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le joueur
// REGARDE (PROCESSUS-CARTE.md, étape 8 bis). On pose à la main l'état d'arrivée que le moteur
// publie, et on affirme sur `dessinee(...)`.
//
// Ce que le scénario change à l'écran : la carte d'état DAZED (sixième état), trois
// ATTACHEMENTS (Baxter Blaster sur le vilain, Swarm Superiority sur un sbire, Intruder Alert!
// sur l'identité), et trois compteurs nommés neufs (câble, bouclier, mutagène) à côté de
// l'essaim. Cartes SANS cas ici, parce qu'elles ne font que chiffrer ou distribuer : tx001-tx003
// (Special, cartes face cachée), tx008, tx009, tx014, tx016 (hébète = statut, voir plus bas).
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'
import { nomDeCompteur } from './compteurs-fr'
import type { WorldCard } from './world'

const IDENTITE = 1
const BAXTER = 80
const identite = () => carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')
const baxter = () => carte(BAXTER, 'tx002', 'EncounterVillain', 'Baxter Stockman')

describe('dazed : la carte d état est dessinée sur son porteur', () => {
  it('sur l identité', () => {
    const m = tableAvec(siege({
      area_hero: [identite(), carte(70, 'dazed', 'StatusCard', 'Dazed', { bind_object_id: IDENTITE })],
    }))
    expect(dessinee(m, 70)).toBeDefined()
    expect(dessinee(m, 70)?.kind).toBe('status')
    expect(dessinee(m, 70)?.codeCarte).toBe('dazed')
    expect(dessinee(m, 70)?.portePar).toBe(IDENTITE)
  })

  it('sur un allié (tx016 Wrapped Up choisit un personnage ami)', () => {
    const m = tableAvec(siege({
      area_hero: [identite()],
      allies: [carte(50, '01058', 'Ally', 'Daredevil'), carte(71, 'dazed', 'StatusCard', 'Dazed', { bind_object_id: 50 })],
    }))
    expect(dessinee(m, 71)?.portePar).toBe(50)
    expect(dessinee(m, 71)?.codeCarte).toBe('dazed')
  })

  it('sur un ennemi (le statut vaut pour tout personnage)', () => {
    const m = tableAvec(siege({ area_hero: [identite()] }), {
      area_villain: [baxter(), carte(72, 'dazed', 'StatusCard', 'Dazed', { bind_object_id: BAXTER })],
    })
    expect(dessinee(m, 72)?.portePar).toBe(BAXTER)
  })

  it('Dazed et Cloaked cote a cote sur le meme personnage : les deux sont dessinees', () => {
    const m = tableAvec(siege({
      area_hero: [
        identite(),
        carte(70, 'dazed', 'StatusCard', 'Dazed', { bind_object_id: IDENTITE }),
        carte(73, 'cloaked', 'StatusCard', 'Cloaked', { bind_object_id: IDENTITE }),
      ],
    }))
    expect(dessinee(m, 70)).toBeDefined()
    expect(dessinee(m, 73)).toBeDefined()
  })
})

describe('tx005 Baxter Blaster : l attachement est dessine sur le vilain', () => {
  it('attache a Baxter Stockman, en genre attachement', () => {
    const m = tableAvec(siege({ area_hero: [identite()] }), {
      area_villain: [baxter(), carte(81, 'tx005', 'Attachment', 'Baxter Blaster', { bind_object_id: BAXTER })],
    })
    expect(dessinee(m, 81)).toBeDefined()
    expect(dessinee(m, 81)?.portePar).toBe(BAXTER)
  })
})

describe('tx006 Swarm Superiority : l attachement est dessine sur le sbire, qui garde ses compteurs', () => {
  const plague = (swarm: number, extra: Partial<WorldCard> = {}) =>
    carte(95, 'tx007', 'Minion', 'Plague of M.O.U.S.E.R.S.', { info: { c_swarm: swarm }, ...extra })
  const m = () => tableAvec(siege({
    area_hero: [identite()],
    engaged_enemies: [plague(4), carte(96, 'tx006', 'Attachment', 'Swarm Superiority', { bind_object_id: 95 })],
  }))

  it('l attachement est a l ecran, porte par le sbire', () => {
    expect(dessinee(m(), 96)).toBeDefined()
    expect(dessinee(m(), 96)?.portePar).toBe(95)
  })

  it('le sbire montre ses 4 compteurs d essaim (2 d entree + 2 de l attachement)', () => {
    expect(dessinee(m(), 95)?.compteurs.swarm).toBe(4)
    expect(dessinee(m(), 95)?.zone).toBe('terrain-combat')
  })
})

describe('tx018 Intruder Alert! : l attachement est dessine sur l identite', () => {
  it('attache a l identite', () => {
    const m = tableAvec(siege({
      area_hero: [identite(), carte(97, 'tx018', 'Attachment', 'Intruder Alert!', { bind_object_id: IDENTITE })],
    }))
    expect(dessinee(m, 97)).toBeDefined()
    expect(dessinee(m, 97)?.portePar).toBe(IDENTITE)
  })
})

describe('compteurs nommes du scenario : cable, bouclier, mutagene', () => {
  const sbire = (id: number, cardId: string, nom: string, info: Record<string, number>) =>
    carte(id, cardId, 'Minion', nom, { info })
  const m = () => tableAvec(siege({
    area_hero: [identite()],
    engaged_enemies: [
      sbire(100, 'tx015', 'Roadkill Rodneys', { c_cable: 2 }),
      sbire(101, 'tx017', 'Auto Defense Bots', { c_shield: 1 }),
      sbire(102, 'tx013', 'Superfly', { c_ooze: 3 }),
    ],
  }))

  it('chaque compteur est dessine sur son sbire', () => {
    expect(dessinee(m(), 100)?.compteurs.cable).toBe(2)
    expect(dessinee(m(), 101)?.compteurs.shield).toBe(1)
    expect(dessinee(m(), 102)?.compteurs.ooze).toBe(3)
  })

  it('les noms francais existent (aucun reste en anglais en pleine partie francaise)', () => {
    expect(nomDeCompteur('cable')).not.toBe('cable')
  })
})

describe('tx004b Baxter\'s Laboratory : la menace est dessinee sur la manigance principale', () => {
  it('menace 3 sur le complot 1B', () => {
    const m = tableAvec(siege({ area_hero: [identite()] }), {
      area_schemes_main: [carte(48, 'tx004b', 'MainScheme', "Baxter's Laboratory", { info: { k_threat: 3 } })],
    })
    expect(dessinee(m, 48)?.menace).toBe(3)
  })
})
