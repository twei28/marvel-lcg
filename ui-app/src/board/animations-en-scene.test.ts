// Le defaut signale en jeu le 15/09/2026 : en mode Detaille, la fenetre raconte
// une etape pendant que la table, derriere, joue le mouvement de cette meme
// etape. Deux recits en meme temps, et on ne sait plus lequel regarder.
import { describe, expect, it } from 'vitest'
import { animationsDuPlateau } from './animations-en-scene'

const base = { reglage: true, sceneCentrale: false, phaseMechantEnCours: false }

describe('animationsDuPlateau', () => {
  it('se tait pendant que la scene raconte la phase du mechant', () => {
    expect(
      animationsDuPlateau({ ...base, sceneCentrale: true, phaseMechantEnCours: true })
    ).toBe(false)
  })

  it('anime hors de la phase du mechant, meme en mode Detaille', () => {
    // Le tour du heros : aucune scene ne raconte rien, la table est le seul
    // endroit ou il se passe quelque chose.
    expect(animationsDuPlateau({ ...base, sceneCentrale: true })).toBe(true)
  })

  it('anime en mode Sur la table, ou le recit se joue justement sur la table', () => {
    expect(animationsDuPlateau({ ...base, phaseMechantEnCours: true })).toBe(true)
  })

  it('⚠ ne rallume JAMAIS ce que le joueur a coupe', () => {
    // Le temoin : cette regle ne fait que RETIRER des animations. Sans lui, une
    // refonte pourrait la transformer en « et sinon on anime », ce qui
    // rendrait les animations a qui n'en veut pas.
    expect(animationsDuPlateau({ reglage: false, sceneCentrale: false, phaseMechantEnCours: false })).toBe(false)
    expect(animationsDuPlateau({ reglage: false, sceneCentrale: true, phaseMechantEnCours: true })).toBe(false)
  })
})
