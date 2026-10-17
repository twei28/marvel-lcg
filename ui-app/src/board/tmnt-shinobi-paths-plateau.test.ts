// TMNT Shinobi, les Paths (`se`) : ce que le plateau DESSINE une fois la carte résolue.
//
// `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_paths.py` prouve ce que le moteur FAIT ; ce fichier prouve ce que le
// joueur REGARDE (PROCESSUS-CARTE.md, étape 8 bis). Seule `se005` The Last Rōnin change ce qu'on voit : Kanpeki glisse une
// carte Shinobi SOUS la Voie (jusqu'à 2), jouable ensuite comme en main. Le test pose à la main l'état d'arrivée que le
// moteur publie (`bind_object_id` = la Voie, `is_face_up: false`) et affirme sur `dessinee(...)`.
//
// Cartes SANS cas ici, parce qu'elles ne font que chiffrer, piocher, camoufler / hébéter (badge déjà couvert par
// `effets-statuts.test.ts`) ou incliner : se001, se002 (regarder n'affiche rien), se003 (compteurs samouraï sur les
// améliorations OATH : `ScanCard.jetons.test.tsx`), se004, se006-se011.
import { describe, expect, it } from 'vitest'
import { kindLabel } from '../components/ScanCard'
import { carteSurTable as carte, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const VOIE = 10
const GLISSEE_1 = 11
const GLISSEE_2 = 12

const voie = (extra = {}) => carte(VOIE, 'se005', 'Path', 'The Last Rōnin', extra)
const glissee = (id: number, cardId: string, nom: string) =>
  carte(id, cardId, 'Event', nom, { bind_object_id: VOIE, is_face_up: false })

const monde = (...glissees: ReturnType<typeof glissee>[]) =>
  tableAvec(
    siege({
      area_hero: [carte(IDENTITE, '01001a', 'Hero', 'Spider-Man')],
      supports: [voie(), ...glissees],
    })
  )

describe('se005 The Last Rōnin : les cartes glissées sous la Voie sont dessinées', () => {
  it('la Voie est dessinée en genre voie (Path), dans la zone des soutiens', () => {
    const v = dessinee(monde(), VOIE)
    expect(v).toBeDefined()
    expect(v?.kind).toBe('path')
    expect(kindLabel.path).toBe('Voie')
  })

  it('une carte glissée sous la Voie est à l écran (assertion qui aurait attrapé Contingency Plan)', () => {
    expect(dessinee(monde(glissee(GLISSEE_1, 'tj005', 'Moonlighting')), GLISSEE_1)).toBeDefined()
  })

  it('elle est portée par la Voie et marquée face cachée, sans être réduite à un dos de carte', () => {
    const c = dessinee(monde(glissee(GLISSEE_1, 'tj005', 'Moonlighting')), GLISSEE_1)
    expect(c?.portePar).toBe(VOIE)
    expect(c?.peeking).toBe(true)
    expect(c?.facedown).toBe(false)
  })

  it('les DEUX cartes glissées (le maximum) sont dessinées, derrière la Voie', () => {
    const m = monde(glissee(GLISSEE_1, 'tj005', 'Moonlighting'), glissee(GLISSEE_2, 'tj004', 'Decisive Strike'))
    const vues = cartesDessinees(m)
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(m, GLISSEE_1)).toBeDefined()
    expect(dessinee(m, GLISSEE_2)).toBeDefined()
    expect(rang(GLISSEE_1)).toBeGreaterThan(rang(VOIE))
    expect(rang(GLISSEE_2)).toBeGreaterThan(rang(VOIE))
  })

  it('témoin : sans carte glissée, rien n est dessiné sous la Voie', () => {
    expect(dessinee(monde(), GLISSEE_1)).toBeUndefined()
  })
})
