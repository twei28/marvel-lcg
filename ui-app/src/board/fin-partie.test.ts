// Le piège du mode Bataille : le moteur n'envoie qu'UN descripteur pour les
// deux tables. Sans lecture par siège, l'écran de fin annoncerait la même
// chose au vainqueur et au vaincu.
import { describe, expect, it } from 'vitest'
import { afficherFinDePartie, coupFatalLocal, finDePartie } from './fin-partie'
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

// Le coup fatal se voit AVANT l'ecran de fin : « on comprend ce qui nous a
// tues ». Le code faisait l'inverse, les deux basculaient sur la meme trame.
describe('coupFatalLocal', () => {
  const etape = (defaite?: boolean, cibleId?: number) => ({ defaite, cibleId })

  it('reconnait la chute du heros de ce siege', () => {
    expect(coupFatalLocal([etape(true, 12)], new Set([12]))).toBe(true)
  })

  it('ignore la chute du heros d un AUTRE joueur', () => {
    // En multijoueur la partie continue pour les autres : leur defaite ne
    // retient l'ecran de fin de personne.
    expect(coupFatalLocal([etape(true, 13)], new Set([12]))).toBe(false)
  })

  it('ignore une etape ordinaire sur notre heros', () => {
    expect(coupFatalLocal([etape(undefined, 12)], new Set([12]))).toBe(false)
  })

  it('ignore une defaite sans cible identifiee', () => {
    expect(coupFatalLocal([etape(true, undefined)], new Set([12]))).toBe(false)
  })
})

describe('afficherFinDePartie', () => {
  const cas = (extra: Partial<Parameters<typeof afficherFinDePartie>[0]> = {}) =>
    afficherFinDePartie({
      partieFinie: true,
      coupFatalAMontrer: true,
      coupFatalVu: false,
      filetEcoule: false,
      ...extra,
    })

  it('ne montre rien tant que le moteur n a pas declare la partie finie', () => {
    expect(cas({ partieFinie: false, coupFatalAMontrer: false })).toBe(false)
    // Meme avec un coup fatal deja vu : c'est le moteur qui dit la fin.
    expect(cas({ partieFinie: false, coupFatalVu: true })).toBe(false)
  })

  it('parait tout de suite quand il n y a aucun coup fatal a montrer', () => {
    // Le mode Instantane, la manigance qui va au bout, la chute d un autre
    // joueur : rien a lire, l ecran vient comme avant.
    expect(cas({ coupFatalAMontrer: false })).toBe(true)
  })

  it('attend que le joueur ait valide le coup fatal', () => {
    expect(cas()).toBe(false)
    expect(cas({ coupFatalVu: true })).toBe(true)
  })

  it('parait quand meme au bout du filet de temps', () => {
    expect(cas({ filetEcoule: true })).toBe(true)
  })
})
