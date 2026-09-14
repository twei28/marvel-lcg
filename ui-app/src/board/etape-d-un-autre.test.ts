// À plusieurs, on voit tout mais on ne clique que pour ses étapes.
//
// Choix de l'utilisateur (14/09/2026) : « tout se joue sous tes yeux, mais tu ne
// cliques que pour toi ». Un coup porté à un autre héros se montre, puis passe
// tout seul ; c'est SON joueur qui donne le rythme, et le moteur attend son
// accusé de réception de toute façon.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `la manigance principale n'est le héros de
// personne`. Écrire la règle sur « une cible qui n'est pas la mienne » ferait
// défiler toute la phase sans un clic, en solo comme à plusieurs : la menace du
// point 1, les sbires, les alliés visés, rien de tout cela n'est une identité.
import { describe, expect, it } from 'vitest'

/**
 * La règle telle que `DeroulePhase` l'écrit. Copiée ici plutôt qu'importée : le
 * composant fait 1700 lignes et la règle tient en une ligne. Le test vaut
 * garde-fou sur l'INTENTION.
 */
const viseUnAutreJoueur = (cibleId: number | undefined, autres: ReadonlySet<number>) =>
  cibleId !== undefined && autres.has(cibleId)

const MON_HEROS = 1
const SON_HEROS = 2
const MANIGANCE = 50
const SBIRE = 80

describe('l’étape d’un autre joueur', () => {
  const autres = new Set([SON_HEROS])

  it('un coup porté à l’autre héros ne demande pas mon clic', () => {
    expect(viseUnAutreJoueur(SON_HEROS, autres)).toBe(true)
  })

  it('un coup porté à MON héros demande mon clic', () => {
    expect(viseUnAutreJoueur(MON_HEROS, autres)).toBe(false)
  })

  it('⚠ la manigance principale n’est le héros de personne', () => {
    // Le point 1 de chaque phase la vise. Si elle comptait comme « pas moi »,
    // la phase entière défilerait sans un clic.
    expect(viseUnAutreJoueur(MANIGANCE, autres)).toBe(false)
  })

  it('⚠ un sbire non plus', () => {
    expect(viseUnAutreJoueur(SBIRE, autres)).toBe(false)
  })

  it('une étape sans cible demande mon clic', () => {
    expect(viseUnAutreJoueur(undefined, autres)).toBe(false)
  })

  it('⚠ en SOLO et en HOT-SEAT, la règle ne joue jamais', () => {
    // L'ensemble est vide : tous les héros sont locaux. Aucune étape ne peut
    // donc passer toute seule, quelle que soit sa cible.
    const aucun: ReadonlySet<number> = new Set()
    for (const cible of [MON_HEROS, SON_HEROS, MANIGANCE, SBIRE, undefined]) {
      expect(viseUnAutreJoueur(cible, aucun)).toBe(false)
    }
  })
})
