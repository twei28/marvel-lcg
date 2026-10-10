import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { BandeauAnnuler, DUREE_BANDEAU_ANNULER_MS } from './BandeauAnnuler'
import { EVENEMENT_REPONSE_ENVOYEE } from '../moteur'
import { oublierGeste } from './telephone'

const reponseEnvoyee = () => act(() => {
  window.dispatchEvent(new CustomEvent(EVENEMENT_REPONSE_ENVOYEE))
})

describe('BandeauAnnuler (zone 3)', () => {
  beforeEach(() => {
    vi.useFakeTimers()
    oublierGeste()
  })
  afterEach(() => {
    vi.useRealTimers()
  })

  it('apparait apres une action du joueur, et « Annuler » appelle l annulation du menu', () => {
    const annuler = vi.fn()
    render(<BandeauAnnuler annuler={annuler} />)
    expect(document.querySelector('.bandeau-annuler')).toBeNull()
    fireEvent.pointerDown(document.body)
    reponseEnvoyee()
    fireEvent.click(screen.getByRole('button', { name: /Annuler/ }))
    expect(annuler).toHaveBeenCalledTimes(1)
    expect(document.querySelector('.bandeau-annuler')).toBeNull()
  })

  it('disparait seul au bout de 5 s', () => {
    render(<BandeauAnnuler annuler={() => {}} />)
    fireEvent.pointerDown(document.body)
    reponseEnvoyee()
    act(() => {
      vi.advanceTimersByTime(DUREE_BANDEAU_ANNULER_MS - 100)
    })
    expect(document.querySelector('.bandeau-annuler')).not.toBeNull()
    act(() => {
      vi.advanceTimersByTime(200)
    })
    expect(document.querySelector('.bandeau-annuler')).toBeNull()
  })

  it('une reponse AUTOMATIQUE (aucun geste recent) ne l allume pas', () => {
    render(<BandeauAnnuler annuler={() => {}} />)
    reponseEnvoyee()
    expect(document.querySelector('.bandeau-annuler')).toBeNull()
  })

  it('sans annulation possible (spectateur), rien ne s affiche', () => {
    render(<BandeauAnnuler />)
    fireEvent.pointerDown(document.body)
    reponseEnvoyee()
    expect(document.querySelector('.bandeau-annuler')).toBeNull()
  })

  it('la zone tactile du bouton est marquee pour le filet des 44 px', () => {
    render(<BandeauAnnuler annuler={() => {}} />)
    fireEvent.pointerDown(document.body)
    reponseEnvoyee()
    expect(screen.getByRole('button', { name: /Annuler/ })).toHaveAttribute('data-tactile', 'annuler')
  })
})
