// Le piège du mode Bataille : le moteur n'envoie qu'UN descripteur pour les
// deux tables. Sans lecture par siège, l'écran de fin annoncerait la même
// chose au vainqueur et au vaincu.
import { describe, expect, it } from 'vitest'
import { finDePartie } from './fin-partie'
import type { World } from './world'

const monde = (champs: Partial<World>) => champs as World

describe('finDePartie', () => {
  it('rend la victoire des joueurs hors mode Bataille', () => {
    expect(finDePartie(monde({ players_won: true }), 0)).toEqual({ gagne: true })
    expect(finDePartie(monde({ players_won: false }), 1)).toEqual({ gagne: false })
  })

  it('ne se laisse pas prendre par `players_won` en Bataille', () => {
    // Le moteur met `players_won` à vrai dès qu'un camp gagne : c'est le camp
    // du siège qui tranche, pas ce drapeau.
    const partie = monde({ players_won: true, winning_team: 1, teams: [0, 1] })
    expect(finDePartie(partie, 0)).toEqual({ gagne: false, bataille: { nul: false } })
    expect(finDePartie(partie, 1)).toEqual({ gagne: true, bataille: { nul: false } })
  })

  it('lit le camp du siège en 2v2', () => {
    const partie = monde({ winning_team: 0, teams: [0, 0, 1, 1] })
    expect(finDePartie(partie, 1).gagne).toBe(true)
    expect(finDePartie(partie, 3).gagne).toBe(false)
  })

  it('annonce un match nul quand personne ne gagne', () => {
    const partie = monde({ players_won: false, winning_team: -1, teams: [0, 1] })
    expect(finDePartie(partie, 0)).toEqual({ gagne: false, bataille: { nul: true } })
    expect(finDePartie(partie, 1)).toEqual({ gagne: false, bataille: { nul: true } })
  })
})
