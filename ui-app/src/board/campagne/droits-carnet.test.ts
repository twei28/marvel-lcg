// Qui a le droit d'écrire quoi dans le carnet.
//
// La règle en une phrase : un champ `parJoueur` appartient au siège qu'il
// nomme, tout le reste appartient à l'hôte. Sans elle, deux joueurs écrivent
// la même case et le dernier gagne, en silence.
import { describe, expect, it } from 'vitest'
import { droitSurChamp, peutValider } from './droits-carnet'
import type { ChampVictoire } from './detecteurs'

const commun: ChampVictoire = { cle: 'Bombs Defused', type: 'choix', libelle: '' }
const personnel: ChampVictoire = { cle: 'Upgrade', type: 'choix', parJoueur: true, libelle: '' }

describe('les droits sur le carnet', () => {
  it("un champ personnel appartient au siège qu'il nomme", () => {
    expect(droitSurChamp(personnel, 1, 1, false)).toBe('saisie')
    expect(droitSurChamp(personnel, 0, 1, false)).toBe('lecture')
  })

  it("l'hôte ne s'approprie pas les champs personnels des autres", () => {
    // Sinon deux personnes remplissent la même case, et « chacun ses champs »
    // ne veut plus rien dire.
    expect(droitSurChamp(personnel, 2, 0, true)).toBe('lecture')
    expect(droitSurChamp(personnel, 0, 0, true)).toBe('saisie')
  })

  it("un champ commun n'appartient qu'à l'hôte", () => {
    expect(droitSurChamp(commun, 0, 0, true)).toBe('saisie')
    expect(droitSurChamp(commun, 0, 2, false)).toBe('lecture')
  })

  it('un siège inconnu ne peut rien écrire', () => {
    expect(droitSurChamp(personnel, 1, -1, false)).toBe('lecture')
    expect(droitSurChamp(commun, 0, -1, false)).toBe('lecture')
  })
})

describe('qui valide pour la table', () => {
  it("seul l'hôte valide", () => {
    expect(peutValider(0)).toBe(true)
    expect(peutValider(1)).toBe(false)
    expect(peutValider(3)).toBe(false)
  })

  it('un siège inconnu ne valide pas', () => {
    // Une page ouverte sans `?p=` ne doit pas pouvoir terminer le scénario de
    // toute la table depuis un écran qu'elle n'a pas rempli.
    expect(peutValider(-1)).toBe(false)
  })
})
