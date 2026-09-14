// Le coup fatal se voit sur la table AVANT son panneau.
//
// Choix de l'utilisateur parmi trois (14/09/2026) : « le panneau, mais après
// avoir vu le coup ». Le coup se joue d'abord comme n'importe quelle étape (le
// trait, le nombre, les points de vie à zéro) et le panneau n'arrive qu'au clic
// suivant. On voit ce qui nous a tués.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `le bouton n'AVANCE pas sur un coup fatal`.
// S'il avançait, il sauterait la fin de la partie du joueur : le panneau ne
// paraîtrait jamais, et l'étape la plus importante d'une partie passerait comme
// une autre.
import { describe, expect, it } from 'vitest'

/**
 * La règle telle que `DeroulePhase` l'écrit. Copiée ici plutôt qu'importée :
 * `DeroulePhase` est un composant de 1700 lignes qu'il faudrait monter en
 * entier, et la règle tient en une ligne. Le test vaut garde-fou sur
 * l'INTENTION.
 */
const fatalAMontrer = (surTable: boolean, defaite: boolean, dejaVu: boolean) =>
  surTable && defaite && !dejaVu

/** La branche « rien qu'un bouton » accepte-t-elle cette étape ? */
const brancheMinimale = (surTable: boolean, temps: string, defaite: boolean, dejaVu: boolean) =>
  surTable && temps !== 'bilan' && (!defaite || fatalAMontrer(surTable, defaite, dejaVu))

describe('le coup fatal, sur la table', () => {
  it('se joue d’abord comme une étape ordinaire', () => {
    expect(brancheMinimale(true, 'mechant', true, false)).toBe(true)
  })

  it('⚠ puis cède la place au panneau, une fois vu', () => {
    expect(brancheMinimale(true, 'mechant', true, true)).toBe(false)
  })

  it('le bilan garde son panneau dans tous les cas', () => {
    // Il n'a aucune carte à montrer sur la table : le réduire à un bouton
    // perdrait ce qu'il a à dire.
    expect(brancheMinimale(true, 'bilan', false, false)).toBe(false)
    expect(brancheMinimale(true, 'bilan', true, false)).toBe(false)
  })

  it('le mode « Détaillé » n’attend rien : il montre le coup DANS son panneau', () => {
    expect(fatalAMontrer(false, true, false)).toBe(false)
    expect(brancheMinimale(false, 'mechant', true, false)).toBe(false)
  })

  it('une étape ordinaire n’est jamais concernée', () => {
    expect(fatalAMontrer(true, false, false)).toBe(false)
    expect(brancheMinimale(true, 'mechant', false, false)).toBe(true)
  })
})
