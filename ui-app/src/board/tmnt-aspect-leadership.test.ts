// Étape 8 bis (PROCESSUS-CARTE) du pack d'aspect TMNT Leadership (`ul`, Inkwire) : ce que les cartes
// DESSINENT. Trois cartes changent ce qu'on voit sur la table :
//  - `ul039` Venus : « attach it to her FACEDOWN » (`PlaceCardHere(..., False)`), une carte de la défausse
//    glissée face cachée sous un ALLIÉ ;
//  - `ul016` Naginata : amélioration attachée à un allié ;
//  - `ul024` Sense of Dread : amélioration du JOUEUR attachée à un SBIRE engagé.
// (Alopex / Midnight Veil / Zato-Ino posent des cartes d'état Cloaked / Dazed : chemin des états, déjà
// couvert par les tests des packs shredder / baxter.)
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const VENUS = 30
const GLISSEE = 31
const MARIA = 40
const NAGINATA = 41
const SBIRE = 50
const SENSE = 51

const monde = () =>
  tableAvec(
    siege({
      area_hero: [carteSurTable(IDENTITE, '01001a', 'Hero', 'Spider-Man')],
      allies: [
        carteSurTable(VENUS, 'ul039', 'Ally', 'Venus'),
        carteSurTable(GLISSEE, 'ul021', 'Ally', 'Red Shell', { bind_object_id: VENUS, is_face_up: false }),
        carteSurTable(MARIA, '01067', 'Ally', 'Maria Hill'),
        carteSurTable(NAGINATA, 'ul016', 'Upgrade', 'Naginata', { bind_object_id: MARIA }),
      ],
      engaged_enemies: [
        carteSurTable(SBIRE, '01101', 'Minion', 'Hydra Mercenary'),
        carteSurTable(SENSE, 'ul024', 'Upgrade', 'Sense of Dread', { bind_object_id: SBIRE }),
      ],
    })
  )

describe('aspect TMNT Leadership : ce qui est dessiné', () => {
  it('ul039 Venus : la carte glissée sous elle est à l écran, portée par Venus, face cachée visible du joueur', () => {
    const carte = dessinee(monde(), GLISSEE)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(VENUS)
    expect(carte?.peeking).toBe(true)
  })

  it('ul016 Naginata : dessinée dans l unité de l allié qui la porte', () => {
    expect(dessinee(monde(), NAGINATA)?.portePar).toBe(MARIA)
  })

  it('ul024 Sense of Dread : dessinée sur le sbire engagé qui la porte', () => {
    expect(dessinee(monde(), SENSE)).toBeDefined()
    expect(dessinee(monde(), SENSE)?.portePar).toBe(SBIRE)
  })
})
