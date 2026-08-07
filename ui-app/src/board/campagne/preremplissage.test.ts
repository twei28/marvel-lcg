// L'ordre des sources est la seule chose que ce fichier protege, et c'est la
// seule chose qui compte : une suggestion du moteur DOIT battre un detecteur,
// parce que le moteur connait son propre etat et que le detecteur le redevine.
import { describe, expect, it } from 'vitest'
import type { World } from '../world'
import type { ChampVictoire } from './detecteurs'
import { preRemplir } from './preremplissage'

const CHAMP_AUTO: ChampVictoire = {
  cle: 'Tech Upgrade',
  type: 'auto',
  format: 'liste',
  detection: 'cartes_en_jeu',
  options: ['04155'],
  libelle: 'Amélioration technologique',
}

const CHAMP_CHOIX: ChampVictoire = {
  cle: 'Weapon',
  type: 'choix',
  format: 'liste',
  libelle: 'Arme',
}

/** Monde minimal : 04155 en jeu, un héros vivant, ce qui suffit aux détecteurs. */
const monde = (): World =>
  ({
    area_schemes_side: [
      { id: 1, card_id: '04155', card_type: 'Upgrade', name: '04155', bind_object_id: 0 },
    ],
    players: [
      {
        area_hero: [
          {
            id: 2,
            card_id: '03001b',
            card_type: 'AlterEgo',
            name: 'hero',
            bind_object_id: 0,
            info: { health: 11, max_health: 11 },
          },
        ],
      },
    ],
  }) as unknown as World

describe('preRemplir', () => {
  it('prend la valeur du moteur quand elle existe, pas celle du détecteur', () => {
    const sortie = preRemplir({
      champs: [CHAMP_AUTO],
      monde: monde(),
      suggestions: { 'Tech Upgrade': '04156' },
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04156')
  })

  it('retombe sur le détecteur quand le moteur ne dit rien', () => {
    const sortie = preRemplir({
      champs: [CHAMP_AUTO],
      monde: monde(),
      suggestions: {},
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04155')
  })

  it('retombe sur le carnet existant quand ni moteur ni détecteur ne répondent', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, options: ['09999'] }],
      monde: monde(),
      carnet: { 'Tech Upgrade': '04150' },
      suggestions: {},
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04150')
  })

  it('laisse un champ de type choix au joueur, même si le moteur a une valeur', () => {
    const sortie = preRemplir({
      champs: [CHAMP_CHOIX],
      monde: monde(),
      suggestions: { Weapon: '04072' },
      total: 1,
    })
    expect(sortie.Weapon).toBeUndefined()
  })

  it('préfixe la clé par joueur quand le champ est parJoueur', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, parJoueur: true }],
      monde: monde(),
      suggestions: { 'Player 1 Tech Upgrade': '04157' },
      total: 1,
    })
    expect(sortie['Player 1 Tech Upgrade']).toBe('04157')
  })

  it('un carnet moteur vide ne change rien au comportement actuel', () => {
    const avec = preRemplir({ champs: [CHAMP_AUTO], monde: monde(), suggestions: {}, total: 1 })
    expect(avec).toEqual({ 'Tech Upgrade': '04155' })
  })
})
