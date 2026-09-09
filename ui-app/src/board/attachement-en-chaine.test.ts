// Une carte attachée à une carte ELLE-MÊME attachée doit rester visible.
//
// Superior Spider-Man, rapport de bug en partie réelle du 09/09/2026 (scénario
// Underground Distribution, Klaw). « Master Planner » (`su001b`) glisse une
// carte de la main FACE CACHÉE sous Contingency Plan (`su012`), qui est une
// amélioration posée sur l'identité. Le moteur faisait le travail — l'état du
// rapport dit « c14 Webbed Up [face cachée, attachée à c23] », et les 32 cas
// `su0` de `test_capacites` étaient verts — mais le plateau ne la dessinait
// NULLE PART : `enUnites` ne lisait les attachements que des racines
// (`bind_object_id === 0`), et Contingency Plan n'en est pas une.
//
// Le correctif est générique (`zones.ts`, sous-arbre aplati), donc les deux
// premiers cas valent pour les 50 cartes du dépôt qui appellent
// `PlaceCardHere`, pas seulement pour celle-ci.
import { describe, expect, it } from 'vitest'
import { carteSurTable, cartesDessinees, dessinee, siege, tableAvec } from './plateau-de-test'

const IDENTITE = 1
const PLAN = 23
const GLISSEE = 14

const monde = () =>
  tableAvec(
    siege({
      area_hero: [
        carteSurTable(IDENTITE, 'su001b', 'AlterEgo', 'Peter Parker'),
        carteSurTable(PLAN, 'su012', 'Upgrade', 'Contingency Plan', {
          bind_object_id: IDENTITE,
        }),
        carteSurTable(GLISSEE, 'su005', 'Event', 'Webbed Up', {
          bind_object_id: PLAN,
          is_face_up: false,
        }),
      ],
    })
  )

describe('attachement à deux étages', () => {
  it('dessine la carte glissée sous une amélioration posée sur l identité', () => {
    expect(dessinee(monde(), GLISSEE)).toBeDefined()
  })

  // La cascade d'améliorations est dessinée A PLAT derrière le porteur racine
  // (`.plateau-unite`), donc la carte glissée remonte à l'identité comme les
  // autres. Ce qui la montre posée SOUS Contingency Plan, c'est son rang : elle
  // suit immédiatement le Plan dans la cascade.
  it('la dessine dans l unité de l identité, juste derrière Contingency Plan', () => {
    const vues = cartesDessinees(monde())
    expect(dessinee(monde(), GLISSEE)?.portePar).toBe(IDENTITE)
    const rang = (id: number) => vues.findIndex((c) => c.id === id)
    expect(rang(GLISSEE)).toBe(rang(PLAN) + 1)
  })

  // Son propriétaire la VOIT — Contingency Plan l'autorise à la jouer plus
  // tard, donc le moteur la lui montre. C'est `peeking`, le cadre en
  // pointillés, qui dit « posée face cachée sur la table » ; `facedown` est
  // réservé à ce que ce siège ne voit PAS.
  it('la marque posée face cachée, sans la réduire à un dos de carte', () => {
    const carte = dessinee(monde(), GLISSEE)
    expect(carte?.peeking).toBe(true)
    expect(carte?.facedown).toBe(false)
  })

  // Cas témoin : sans lui, un correctif qui dessinerait TOUT en racine passerait.
  it('garde l amélioration porteuse attachée à l identité, face visible', () => {
    const carte = dessinee(monde(), PLAN)
    expect(carte?.portePar).toBe(IDENTITE)
    expect(carte?.peeking).toBe(false)
  })
})
