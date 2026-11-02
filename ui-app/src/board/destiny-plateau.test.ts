// Destiny (dy001a/b) : ce que la table DESSINE (étape 8 bis de PROCESSUS-CARTE).
//  - dy002 Glimpse of the Future est une amélioration posée sur l'identité (Permanent, Setup) ;
//  - Précognition glisse UNE carte du deck Rencontre sous elle (`TuckCardUnderHere(.., peek=True)`) : dy014 Mister Sinister doit rester
//    dessinée, portée par Destiny, juste derrière Glimpse (seule sa zone de boost compte pour X) ;
//  - dy015 Destiny's Warning (complot annexe) et dy014 (sbire némésis engagé) sont à l'écran.
// Le dessin des cartes glissées à deux étages est générique (`zones.ts`, voir attachement-en-chaine.test.ts) : ce cas le vaut pour Glimpse.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const DESTINY = 1
const GLIMPSE = 2
const GLISSEE = 3
const SINISTER = 4
const WARNING = 5

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(DESTINY, 'dy001a', 'Hero', 'Destiny'),
        carteSurTable(GLIMPSE, 'dy002', 'Upgrade', 'Glimpse of the Future', { bind_object_id: DESTINY }),
        carteSurTable(GLISSEE, 'dy016', 'Treachery', "So, What's the Plan?", { bind_object_id: GLIMPSE, is_face_up: false }),
      ],
      engaged_enemies: [carteSurTable(SINISTER, 'dy014', 'Minion', 'Mister Sinister')],
    }),
    { area_schemes_side: [carteSurTable(WARNING, 'dy015', 'SideScheme', "Destiny's Warning")] },
  )

describe('Destiny : ce que la table dessine', () => {
  it('dessine Glimpse of the Future sur Destiny', () => {
    expect(dessinee(monde(), GLIMPSE)).toBeDefined()
    expect(dessinee(monde(), GLIMPSE)?.portePar).toBe(DESTINY)
  })
  it('dessine la carte glissée sous Glimpse, juste derrière elle, marquée posée face cachée', () => {
    const vues = cartesDessinees(monde())
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
    expect(dessinee(monde(), GLISSEE)?.peeking).toBe(true)
    expect(rang(GLISSEE)).toBe(rang(GLIMPSE) + 1)
  })
  it('dessine Mister Sinister (engagé) et Destiny\'s Warning (complot annexe)', () => {
    expect(dessinee(monde(), SINISTER)).toBeDefined()
    expect(dessinee(monde(), WARNING)).toBeDefined()
  })
})
