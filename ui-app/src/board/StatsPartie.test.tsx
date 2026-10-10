// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { StatsPartie, formaterDuree } from './StatsPartie'
import { DICO_EN_BASE } from './dico-en'
import type { StatsJoueur, StatsPartie as Stats } from './world'

afterEach(cleanup)

const joueur = (siege: number, heros: string, degats: number): StatsJoueur => ({
  siege,
  heros,
  heros_id: '01001a',
  aspects: ['Leadership'],
  pv: 5,
  pv_max: 12,
  compteurs: { degats_mechant: degats, degats_sbires: 12, menace_principale: 32, menace_annexes: 9, attaques_defendues: 7 },
  plus_jouees: [{ card_id: '01072', nom: 'Strength in Numbers', n: 8, piochee: 9, jouee: 8 }],
  moins_jouees: [{ card_id: '01090', nom: 'Energy Channel', n: 0, piochee: 3, jouee: 0 }],
})

const solo: Stats = { temps: 58 * 60, rounds: 10, joueurs: [joueur(0, 'Captain Marvel', 45)] }

describe('l’onglet Stats de l’écran de fin', () => {
  it('solo : les tuiles, les lignes du héros et les cartes', () => {
    render(<StatsPartie stats={solo} gagne />)
    expect(screen.getByText('Gagnée')).toBeTruthy()
    expect(screen.getByText('58 min')).toBeTruthy()
    // Dégâts infligés = méchant + sbires, menace = principale + annexes : de simples sommes.
    expect(screen.getByText('57')).toBeTruthy()
    expect(screen.getByText('41')).toBeTruthy()
    expect(screen.getByText('Captain Marvel')).toBeTruthy()
    expect(screen.getByText(/Commandement · 5\/12/)).toBeTruthy()
    expect(screen.getByText('×8')).toBeTruthy()
    expect(screen.getByText('Piochées mais peu jouées')).toBeTruthy()
    expect(screen.getByText('×0')).toBeTruthy()
    expect(document.querySelector('table')).toBeNull()
  })

  it('multijoueur : un tableau, une colonne par héros', () => {
    const multi: Stats = { ...solo, joueurs: [joueur(0, 'Captain Marvel', 45), joueur(1, 'Spider-Man', 20)] }
    render(<StatsPartie stats={multi} gagne={false} />)
    const entetes = [...document.querySelectorAll('thead th')].map((th) => th.textContent)
    expect(entetes.some((x) => x?.includes('Captain Marvel'))).toBe(true)
    expect(entetes.some((x) => x?.includes('Spider-Man'))).toBe(true)
    expect(screen.getByText('Perdue')).toBeTruthy()
    // 45 + 12 + 20 + 12 = 89 dégâts infligés au total.
    expect(screen.getByText('89')).toBeTruthy()
  })

  it('sans mesure (ancienne relecture) : le dit, sans inventer de chiffre', () => {
    render(<StatsPartie stats={undefined} gagne />)
    expect(screen.getByText('Statistiques indisponibles pour cette partie.')).toBeTruthy()
  })

  it('le survol d’une vignette ouvre l’aperçu, et le retire en sortant', () => {
    render(<StatsPartie stats={solo} gagne />)
    const carte = screen.getByText('×8').closest('li')!
    fireEvent.mouseEnter(carte)
    expect(screen.getByTestId('stats-apercu')).toBeTruthy()
    fireEvent.mouseLeave(carte)
    expect(screen.queryByTestId('stats-apercu')).toBeNull()
  })

  it('la durée : minutes, puis heures', () => {
    expect(formaterDuree(58 * 60)).toBe('58 min')
    expect(formaterDuree(65 * 60)).toBe('1 h 05')
  })

  it('chaque libellé a son anglais', () => {
    for (const fr of ['Résultat', 'Dégâts évités', 'Piochées mais peu jouées', 'Ressources dépensées', 'Commandement']) {
      expect(DICO_EN_BASE[fr], fr).toBeTruthy()
    }
  })
})
