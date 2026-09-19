// Fear No Evil, bloc 1 (18/09/2026) : une OEUVRE (attachement de rencontre
// ART, 60122-60125) change de porteur en pleine partie. Elle commence sur le
// vilain (Setup d'Art Museum Heist), passe sur le HEROS par sa Hero Action, et
// repart sur le vilain apres une attaque non defendue. C'est le premier
// attachement de rencontre du depot qui se pose sur une IDENTITE par choix
// du joueur : on prouve ici qu'il est dessine aux deux endroits, et que le
// serum du Hibou (60191) reste visible sur le vilain a cote d'une oeuvre.
//
// Etape 8 bis de PROCESSUS-CARTE : le mecanisme (attachement rattache par
// `bind_object_id`) est generique, ces cas sont des GARDES, ils etaient verts
// des la premiere execution ; aucun correctif du plateau n'a ete necessaire.
import { describe, expect, it } from 'vitest'
import { carteSurTable, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const VILAIN = 49
const OEUVRE = 83
const SERUM = 78

const oeuvreSurLeHeros = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(IDENTITE, '01001a', 'Hero', 'Spider-Man'),
        carteSurTable(OEUVRE, '60122', 'Attachment', 'Impossible Object', {
          bind_object_id: IDENTITE,
        }),
      ],
    }),
    {
      area_villain: [carteSurTable(VILAIN, '60086', 'Villain', 'Hammerhead')],
    }
  )

const oeuvreSurLeVilain = () =>
  tableAvec(
    siege({ area_hero: [carteSurTable(IDENTITE, '01001a', 'Hero', 'Spider-Man')] }),
    {
      area_villain: [
        carteSurTable(VILAIN, '60086', 'Villain', 'Hammerhead'),
        carteSurTable(OEUVRE, '60122', 'Attachment', 'Impossible Object', {
          bind_object_id: VILAIN,
        }),
        carteSurTable(SERUM, '60191', 'Attachment', 'Flight Serum', {
          bind_object_id: VILAIN,
        }),
      ],
    }
  )

describe('oeuvre d Art Museum Heist', () => {
  it('est dessinee sur le heros quand il la lui a prise', () => {
    const carte = dessinee(oeuvreSurLeHeros(), OEUVRE)
    expect(carte).toBeDefined()
    expect(carte?.portePar).toBe(IDENTITE)
    expect(carte?.facedown).toBe(false)
  })

  it('est dessinee sur le vilain, avec le serum du Hibou a cote', () => {
    const monde = oeuvreSurLeVilain()
    expect(dessinee(monde, OEUVRE)?.portePar).toBe(VILAIN)
    expect(dessinee(monde, SERUM)?.portePar).toBe(VILAIN)
  })

  // Temoin : le vilain lui-meme reste une racine, jamais « porte » par rien.
  it('laisse le vilain en racine', () => {
    expect(dessinee(oeuvreSurLeVilain(), VILAIN)?.portePar).toBe(0)
  })
})
