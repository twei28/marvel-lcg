// Wasp (Hank Pym) (JackHKP, `hp001a`-`hp018`) : ce que le plateau DESSINE une fois les cartes résolues.
//
// `Fusion/marvel-lcg-src/tools/cas/wasp_hank_pym.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). Les cartes du pack qui changent ce qu'on VOIT :
//   - hp010 Huge Surprise : amélioration ATTACHÉE À UN ENNEMI (le méchant) ;
//   - hp014 Return of the Prodigal Son : une amélioration ou un soutien glissé FACE CACHÉE sous le complot annexe ;
//   - hp016 Seized Control : une carte glissée face cachée sous l'attachement, lui-même posé sur Ultron.
// Aucun correctif de plateau : le rendu générique (attachement à deux étages, `zones.ts`) suffisait.
import { describe, expect, it } from 'vitest'
import { carteSurTable as carte, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const RHINO = 80
const ULTRON = 81
const CONTROLE = 82
const GLISSEE = 83
const COMPLOT = 84
const SURPRISE = 85

const heros = () => carte(IDENTITE, 'hp001a', 'Hero', 'Wasp')

describe('hp010 Huge Surprise : attachée à un ennemi', () => {
  it('est dessinée sur le méchant, plus sur le héros', () => {
    const monde = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carte(SURPRISE, 'hp010', 'Upgrade', 'Huge Surprise', { bind_object_id: RHINO }),
      ],
    })
    expect(dessinee(monde, SURPRISE)).toBeDefined()
    expect(dessinee(monde, SURPRISE)?.portePar).toBe(RHINO)
  })
})

describe('hp016 Seized Control : glisse une carte sous l attachement posé sur Ultron', () => {
  const monde = () =>
    tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carte(ULTRON, 'hp015', 'Minion', 'Ultron'),
        carte(CONTROLE, 'hp016', 'Attachment', 'Seized Control', { bind_object_id: ULTRON }),
        carte(GLISSEE, 'hp008', 'Support', 'Jocasta', { bind_object_id: CONTROLE, is_face_up: false }),
      ],
    })

  it('dessine l attachement sur Ultron et la carte glissée dessous', () => {
    expect(dessinee(monde(), CONTROLE)?.portePar).toBe(ULTRON)
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
  })
})

describe('hp014 Return of the Prodigal Son : glisse un soutien face cachée sous le complot annexe', () => {
  it('dessine la carte glissée sous le complot', () => {
    const monde = tableAvec(siege({ area_hero: [heros()] }), {
      area_villain: [
        carte(RHINO, '01094', 'EncounterVillain', 'Rhino'),
        carte(COMPLOT, 'hp014', 'SideScheme', 'Return of the Prodigal Son'),
        carte(GLISSEE, 'hp008', 'Support', 'Jocasta', { bind_object_id: COMPLOT, is_face_up: false }),
      ],
    })
    expect(dessinee(monde, GLISSEE)).toBeDefined()
  })
})

// CORRECTIF du 26/10/2026 (hp007 Infinite Avengers Mansion : « a card you control » inclut l'identité) : le compteur pym peut
// désormais se poser sur Hank Pym lui-même, et il doit se lire à l'écran comme sur un Size Manipulation (hp011).
describe('hp007 Infinite Avengers Mansion : un compteur pym sur l identité', () => {
  const valeurs = (id: number, monde: ReturnType<typeof tableAvec>) => Object.values(dessinee(monde, id)?.compteurs ?? {})

  it('l identité porte son compteur pym à l écran (le Size Manipulation aussi)', () => {
    const monde = tableAvec(
      siege({
        area_hero: [
          carte(IDENTITE, 'hp001b', 'AlterEgo', 'Hank Pym', { info: { c_pym: 1 } }),
          carte(SURPRISE, 'hp011', 'Upgrade', 'Size Manipulation', { bind_object_id: IDENTITE, info: { c_pym: 2 } }),
        ],
      })
    )
    expect(valeurs(IDENTITE, monde)).toContain(1)
    expect(valeurs(SURPRISE, monde)).toContain(2)
  })
})
