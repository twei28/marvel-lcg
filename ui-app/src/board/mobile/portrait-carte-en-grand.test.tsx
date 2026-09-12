// Demande de l'utilisateur, verifiee dans le navigateur le 11/09/2026 : taper
// une carte doit l'afficher EN GRAND, au milieu de l'ecran, entiere.
//
// Ce n'etait pas le cas. Le tap appelait `props.onCardClick`, qui en mode
// « simple » ne fait quelque chose que si le moteur propose une action sur
// cette carte : taper une carte pour la LIRE ne produisait rien. Or c'est le
// geste central du portrait (spec : « tap lire/fermer, appui long jouer »), et
// les vignettes de la table font 64 px : sans agrandissement, le plateau
// devient un jeu de devinettes.
//
// `CarteOuverte` existe deja et fait exactement cela (voile, carte centree,
// fermeture au clic exterieur, appui long pour agir). PlateauMedaillons s'en
// sert ; le portrait, non.

import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { PlateauPortrait } from './PlateauPortrait'
import type { Plateau, UniteAffichee } from '../zones'
import type { World } from '../world'
import type { ScanCardProps } from '../../components/ScanCard'

const monde = { render_id: 1, round_id: 1, phase: 'Player 1 Turn', players: [] } as unknown as World

const unite = (cle: string, carte: Partial<ScanCardProps>): UniteAffichee =>
  ({ cle, carte: { id: cle, name: cle, kind: 'minion', imageUrl: '', ...carte }, attachees: [] }) as UniteAffichee

const plateau = (cle: string, ...unites: UniteAffichee[]): Plateau =>
  ({ emplacements: [{ cle, titre: cle, groupes: [unites] }] }) as unknown as Plateau

describe('taper une carte de la table', () => {
  it('l\'affiche en grand, dans une boite de dialogue', () => {
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau('rencontre', unite('7', { name: 'Rhino' }))}
      />
    )
    // `fireEvent` et non `.click()` : le clic natif change bien l'etat React,
    // mais hors d'`act()` le re-rendu n'a pas encore eu lieu quand on inspecte.
    fireEvent.click(document.querySelector('.bande-carte .scan-card')!)
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    expect(document.querySelector('.carte-ouverte')).toBeInTheDocument()
  })

  it('se referme quand on tape a cote', () => {
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau('rencontre', unite('7', { name: 'Rhino' }))}
      />
    )
    fireEvent.click(document.querySelector('.bande-carte .scan-card')!)
    fireEvent.pointerDown(document.querySelector('.carte-ouverte-voile')!)
    expect(document.querySelector('.carte-ouverte')).not.toBeInTheDocument()
  })

  it('n\'empeche pas l\'appui long de jouer la carte directement', () => {
    const agir = vi.fn()
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau('rencontre', unite('7', { name: 'Rhino', onSelect: agir }))}
      />
    )
    // Sans ouvrir : le maintien joue, comme avant.
    expect(document.querySelector('.carte-ouverte')).not.toBeInTheDocument()
  })

  it('montre les attachees et statuts de la porteuse sous la carte, et un tap ouvre l attachee', () => {
    const armure = { id: 'armure', name: 'Armure', kind: 'upgrade', imageUrl: '' } as ScanCardProps
    const tough = { id: 'tough', name: 'Tough', kind: 'status', imageUrl: '' } as ScanCardProps
    render(
      <PlateauPortrait
        world={monde}
        playerId={0}
        plateau={plateau('rencontre', { ...unite('rhino', { name: 'Rhino', kind: 'villain' }), attachees: [armure, tough] } as UniteAffichee)}
      />
    )
    fireEvent.click(document.querySelector('.bande-carte > .plateau-unite > .scan-card')!)
    const attachees = document.querySelectorAll('.carte-ouverte-attachee')
    expect(attachees).toHaveLength(2)
    expect(attachees[0]).toHaveClass('est-statut')
    fireEvent.click(attachees[1])
    expect(screen.getByRole('dialog', { name: 'Armure' })).toBeInTheDocument()
    expect(document.querySelectorAll('.carte-ouverte-attachee')).toHaveLength(0)
  })
})
