// Les statuts identiques se replient en un seul, avec leur nombre.
//
// Pourquoi (14/09/2026, question de l'utilisateur sur Luke Cage) : « Luke Cage
// peut avoir plein de Tenaces, s'il y a dix cartes Tenaces sous la carte, ça
// ne va pas, ce ne serait pas du tout lisible ».
//
// MESURÉ sur le plateau réel avant de corriger, en clonant un vrai statut pour
// hériter de toute la CSS : la rangée `.statuts` est un `flex` sans repli, donc
// 2 statuts débordent déjà de la carte du porteur, 3 font 192 px, 10 font
// 647 px pour une carte de 106 — soit 270 px de débord de chaque côté,
// par-dessus les zones voisines. Luke Cage n'a aucune limite
// (`ThisCanHaveAdditionalTough("Any")`).
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `on ne replie jamais un statut cliquable`.
// Le moteur peut demander de choisir UNE carte de statut ; replier mettrait les
// autres hors d'atteinte et bloquerait le joueur sur un coup légal. Un
// affichage large vaut mieux qu'un coup impossible.
import { describe, expect, it } from 'vitest'
import { grouperStatuts } from './Board'
import type { CardEffectDelta, ScanCardProps } from '../components/ScanCard'
import type { EtatInteractif } from './interaction'

const statut = (id: number, nom: string): ScanCardProps =>
  ({ id: String(id), name: nom, kind: 'status' }) as unknown as ScanCardProps

const AUCUNE = new Map<number, EtatInteractif>()
const AUCUN = new Map<number, CardEffectDelta>()

/** Dix Tenaces, comme Luke Cage sait en accumuler. */
const dixTenaces = Array.from({ length: 10 }, (_, i) => statut(i + 1, 'Tenace'))

describe('les statuts identiques comptent au lieu de s’étaler', () => {
  it('dix Tenaces tiennent en UNE carte portant le nombre', () => {
    const groupes = grouperStatuts(dixTenaces, AUCUNE, AUCUN)
    expect(groupes).toHaveLength(1)
    expect(groupes[0].nombre).toBe(10)
    expect(groupes[0].carte.name).toBe('Tenace')
  })

  it('un seul Tenace ne porte aucun nombre', () => {
    const groupes = grouperStatuts([statut(1, 'Tenace')], AUCUNE, AUCUN)
    expect(groupes).toHaveLength(1)
    expect(groupes[0].nombre).toBe(1)
  })

  it('des statuts DIFFÉRENTS restent côte à côte', () => {
    // Tenace, Sonné et Confus ne disent pas la même chose : les fondre en un
    // seul chiffre perdrait l'information.
    const groupes = grouperStatuts(
      [statut(1, 'Tenace'), statut(2, 'Sonné'), statut(3, 'Confus')],
      AUCUNE,
      AUCUN
    )
    expect(groupes.map((g) => [g.carte.name, g.nombre])).toEqual([
      ['Tenace', 1],
      ['Sonné', 1],
      ['Confus', 1],
    ])
  })

  it('trois Tenaces et deux Sonnés donnent deux cartes, ×3 et ×2', () => {
    const groupes = grouperStatuts(
      [
        statut(1, 'Tenace'),
        statut(2, 'Sonné'),
        statut(3, 'Tenace'),
        statut(4, 'Sonné'),
        statut(5, 'Tenace'),
      ],
      AUCUNE,
      AUCUN
    )
    expect(groupes.map((g) => [g.carte.name, g.nombre])).toEqual([
      ['Tenace', 3],
      ['Sonné', 2],
    ])
  })

  it('l’ordre d’apparition est gardé', () => {
    const groupes = grouperStatuts(
      [statut(1, 'Sonné'), statut(2, 'Tenace'), statut(3, 'Sonné')],
      AUCUNE,
      AUCUN
    )
    expect(groupes.map((g) => g.carte.name)).toEqual(['Sonné', 'Tenace'])
  })

  it('aucun statut ne donne aucun groupe', () => {
    expect(grouperStatuts([], AUCUNE, AUCUN)).toEqual([])
  })
})

describe('on ne replie jamais un statut cliquable', () => {
  it('un seul statut ciblable suffit à tous les remontrer', () => {
    // ⚠ Le moteur demande de défausser UNE carte Tenace : si on repliait, les
    // neuf autres n'existeraient plus à l'écran et le joueur ne pourrait pas
    // choisir. On accepte le débord plutôt que de bloquer le coup.
    const interactifs = new Map<number, EtatInteractif>([
      [4, { role: 'cible', agir: () => {} } as unknown as EtatInteractif],
    ])
    const groupes = grouperStatuts(dixTenaces, interactifs, AUCUN)
    expect(groupes).toHaveLength(10)
    expect(groupes.every((g) => g.nombre === 1)).toBe(true)
  })

  it('un statut qui porte un delta les remontre tous aussi', () => {
    // Un +N / -N sur une carte précise : elle a quelque chose à montrer de son
    // propre chef, le chiffre global l'effacerait.
    const effets = new Map<number, CardEffectDelta>([
      [7, { degats: 1 } as unknown as CardEffectDelta],
    ])
    expect(grouperStatuts(dixTenaces, AUCUNE, effets)).toHaveLength(10)
  })

  it('sans cible ni delta, on replie bien', () => {
    // Le témoin : les deux gardes ci-dessus ne doivent pas tout bloquer.
    const interactifs = new Map<number, EtatInteractif>([
      [999, { role: 'cible', agir: () => {} } as unknown as EtatInteractif],
    ])
    expect(grouperStatuts(dixTenaces, interactifs, AUCUN)).toHaveLength(1)
  })
})
