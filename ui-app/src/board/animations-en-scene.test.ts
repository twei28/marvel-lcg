// Le defaut signale en jeu le 15/09/2026 : en mode Detaille, la fenetre raconte
// une etape pendant que la table, derriere, joue le mouvement de cette meme
// etape. Deux recits en meme temps, et on ne sait plus lequel regarder.
import { describe, expect, it } from 'vitest'
import { animationsDuPlateau, estResynchronisation } from './animations-en-scene'

const base = { reglage: true, sceneCentrale: false, phaseMechantEnCours: false, enMiseEnPlace: false }

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
    expect(animationsDuPlateau({ ...base, reglage: false })).toBe(false)
    expect(animationsDuPlateau({ ...base, reglage: false, sceneCentrale: true, phaseMechantEnCours: true })).toBe(false)
  })

  it('se tait pendant la mise en place automatique', () => {
    expect(animationsDuPlateau({ ...base, enMiseEnPlace: true })).toBe(false)
  })

  it('reprend des le premier round, mise en place finie', () => {
    expect(animationsDuPlateau({ ...base, enMiseEnPlace: false })).toBe(true)
  })
})

// Signalement Yarro n25 + demande de l'utilisateur, 28/09/2026 : Undo relance
// toute la partie (GameSession.Undo) et rejoue son historique -- le
// render_id repart plus bas que celui deja affiche. C'est la seule chose qui
// distingue une resynchronisation d'un rendu normal.
describe('estResynchronisation', () => {
  it('detecte une baisse du render_id (Undo, remelange...)', () => {
    expect(estResynchronisation(120, 331)).toBe(true)
  })

  it('ne declenche PAS sur une hausse, meme un grand saut', () => {
    // Le moteur avance par dizaines a chaque mise a jour (commentaire de
    // CoucheAnimations.tsx) : un saut de +100 est un rendu normal.
    expect(estResynchronisation(431, 331)).toBe(false)
  })

  it('ne declenche pas sur une egalite (meme rendu revu)', () => {
    expect(estResynchronisation(331, 331)).toBe(false)
  })

  it('ne declenche pas sans repere anterieur (tout premier rendu)', () => {
    expect(estResynchronisation(331, undefined)).toBe(false)
  })

  it('ne declenche pas si le rendu actuel est absent', () => {
    expect(estResynchronisation(undefined, 331)).toBe(false)
  })
})
