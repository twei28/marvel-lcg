// Rapport nicodede62 #149 (18/11/2026) : la question de Cosmo « nommez un type de carte » affichait 17 boutons
// « Empathetic Advantage » (nom de capacité de l'identité Mantis) au lieu des types de carte.
import { afterEach, describe, expect, it, vi } from 'vitest'
import type { Option } from './ask'
import { nomDeCapacite } from './DemandeCentrale'
import { libelleTypeDeCarte } from './types-de-carte'
import { traduireMoteur } from './vocabulaire-moteur'

afterEach(() => {
  vi.restoreAllMocks()
  localStorage.removeItem('marvel-langue')
})

const option = (name: string): Option =>
  ({ id: 1, name, bind_id: 1, bind_player_id: 0, all_legal_targets: [], target_num_range: [0, 0], target_payment: {},
     select_rule: '', select_rule_param: [0, 0], target_must_include_traits: [], failure_reason: '', is_search: false,
     is_text_choice: true }) as unknown as Option
const TEXTE_MANTIS = 'Empathetic Advantage — Resource: Discard a confused status card from an enemy or character you control → generate a [mental] resource.'

describe('« nommez un type de carte » (Cosmo)', () => {
  it('chaque bouton dit le TYPE, jamais le nom de capacité de la carte porteuse (français)', () => {
    localStorage.setItem('marvel-langue', 'fr')
    expect(nomDeCapacite(option('Hero'), TEXTE_MANTIS)).toBe('Héros')
    expect(nomDeCapacite(option('Ally'), TEXTE_MANTIS)).toBe('Allié')
    expect(nomDeCapacite(option('MainScheme'), TEXTE_MANTIS)).toBe('Manigance principale')
    expect(nomDeCapacite(option('Resource'), TEXTE_MANTIS)).toBe('Ressource')
  })

  it('en anglais, des mots lisibles (pas « AlterEgo » collé)', () => {
    localStorage.setItem('marvel-langue', 'en')
    expect(nomDeCapacite(option('AlterEgo'), TEXTE_MANTIS)).toMatch(/^Alter[ -]ego$/i)
    expect(nomDeCapacite(option('Hero'), TEXTE_MANTIS)).toBe('Hero')
    expect(nomDeCapacite(option('EncounterSideScheme'), TEXTE_MANTIS)).toBe('Encounter side scheme')
  })

  it('les 17 types du moteur (player_ask.py, DeclareCardType) ont tous un libellé', () => {
    localStorage.setItem('marvel-langue', 'fr')
    const moteur = ['Hero', 'AlterEgo', 'Ally', 'Event', 'Resource', 'Support', 'Upgrade', 'Obligation', 'MainScheme',
      'EncounterSideScheme', 'PlayerSideScheme', 'Minion', 'Villain', 'Treachery', 'Attachment', 'Environment', 'Evidence']
    for (const nom of moteur) expect(libelleTypeDeCarte(nom), nom).toBeTruthy()
  })

  it('les titres et les paquets de Cosmo se lisent en français', () => {
    localStorage.setItem('marvel-langue', 'fr')
    expect(traduireMoteur('Cosmo: name a card type')).toBe('Cosmo : nommez un type de carte')
    expect(traduireMoteur('Cosmo: discard the top card of which deck?')).toBe('Cosmo : défausser le dessus de quel deck ?')
    expect(traduireMoteur('Player deck (Mantis)')).toBe('Deck joueur (Mantis)')
    expect(traduireMoteur('Encounter deck')).toBe('Deck rencontre')
  })
})
