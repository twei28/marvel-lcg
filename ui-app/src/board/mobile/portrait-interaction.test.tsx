// Le defaut le plus grave de la recette du 11/09/2026 : sur telephone, AUCUNE
// carte n'etait jouable. Le plateau s'affichait, mais ne se jouait pas.
//
// Cause : `avecInteraction()` (Board.tsx) est le SEUL endroit qui pose
// `state`, `onSelect`, `targetPulse`, `spentCount` et `effectDelta` sur une
// carte. Le plateau PC l'appelle (table et main) ; PlateauPortrait ne
// l'appelait jamais et ne lisait meme pas `props.interactifs`. Rien ne
// s'allumait quand le moteur attendait une cible, et l'appui long retombait
// toujours sur `onCardClick`.
//
// Deuxieme cause, qui aurait annule la premiere correction : CarteAvecChiffres
// ecrivait `onSelect={onOuvrir}`, ecrasant par `undefined` le `onSelect` que la
// carte portait.

import { afterEach, describe, expect, it, vi } from 'vitest'
import { fireEvent, render } from '@testing-library/react'
import { APPUI_LONG_MS } from './useAppuiLong'
import { PlateauPortrait } from './PlateauPortrait'
import type { EtatInteractif } from '../interaction'
import type { Plateau, UniteAffichee } from '../zones'
import type { World } from '../world'
import type { ScanCardProps } from '../../components/ScanCard'

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] } as unknown as World

const unite = (cle: string, carte: Partial<ScanCardProps>): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'minion', imageUrl: '', ...carte }, attachees: [] }) as UniteAffichee

const plateau = (cle: string, ...unites: UniteAffichee[]): Plateau =>
  ({ emplacements: [{ cle, titre: cle, groupes: [unites] }] }) as unknown as Plateau

/** Ce que `interaction.ts` pose pour une carte que le moteur propose comme
    cible. Les roles sont en francais (ETAT_PAR_ROLE, Board.tsx) : « cible »
    devient l'etat `targetable`. */
const interactif = (agir: () => void): EtatInteractif =>
  ({ role: 'cible', agir, fois: 0, pulse: false, choisie: false }) as unknown as EtatInteractif

describe('l\'interaction sur le plateau portrait', () => {
  afterEach(() => {
    vi.useRealTimers()
  })

  it('marque une carte de la table comme cible quand le moteur la propose', () => {
    const { container } = render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau('rencontre', unite('7', { name: 'Rhino' }))}
        interactifs={new Map([[7, interactif(() => {})]])}
      />
    )
    // `avecInteraction` traduit le role en `state` : sans lui, la carte reste
    // dans son etat par defaut et rien ne signale au joueur qu'elle est cible.
    const carte = container.querySelector('.bande-carte .scan-card')
    expect(carte?.className).toContain('state-targetable')
  })

  it('joue la carte de la table sur appui long, via le onSelect du moteur', () => {
    vi.useFakeTimers()
    const agir = vi.fn()
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau('rencontre', unite('7', { name: 'Rhino' }))}
        interactifs={new Map([[7, interactif(agir)]])}
      />
    )
    fireEvent.pointerDown(document.querySelector('.bande-carte')!)
    vi.advanceTimersByTime(APPUI_LONG_MS)
    expect(agir).toHaveBeenCalledTimes(1)
  })

  it('ouvre la carte en grand au simple tap, sans la jouer', () => {
    const agir = vi.fn()
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau('rencontre', unite('7', { name: 'Rhino' }))}
        interactifs={new Map([[7, interactif(agir)]])}
      />
    )
    fireEvent.click(document.querySelector('.bande-carte .scan-card')!)
    // Lire n'est pas jouer : le tap montre la carte, il ne declenche pas
    // l'action que le moteur propose. C'est l'appui long qui joue.
    expect(document.querySelector('.carte-ouverte')).toBeInTheDocument()
    expect(agir).not.toHaveBeenCalled()
  })
})
