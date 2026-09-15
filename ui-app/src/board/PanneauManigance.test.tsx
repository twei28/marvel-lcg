// LA FACE A DE LA MANIGANCE, EN GRAND, AVANT QU'ELLE SE RETOURNE.
//
// Demande de l'utilisateur, 15/09/2026 : « on doit voir la face A de la
// premiere manigance, puis on fait ok, puis elle se place sur la face B ».
// Le moteur ATTEND vraiment cette reponse (World.ConfirmMainSchemeReveal) :
// un second clic ne doit RIEN reposter, sous peine de repondre a la question
// SUIVANTE a la place du joueur.
import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { PanneauManigance } from './PanneauManigance'
import type { WorldCard } from './world'

const carte = { id: 48, card_id: '01097a', pic_id: '01097a', name: 'The Break-In!' } as unknown as WorldCard

describe('PanneauManigance', () => {
  it('montre la carte en grand', () => {
    render(<PanneauManigance carte={carte} onValider={() => {}} />)
    const image = screen.getByRole('img')
    expect(image.getAttribute('src')).toContain('01097a')
  })

  it('valide au clic sur le bouton', () => {
    const onValider = vi.fn()
    render(<PanneauManigance carte={carte} onValider={onValider} />)
    fireEvent.click(screen.getByRole('button'))
    expect(onValider).toHaveBeenCalledTimes(1)
  })

  it('ne valide pas deux fois, meme sur double clic', () => {
    // Le moteur n'attend qu'une reponse : une seconde poste dans le vide et
    // peut repondre a la question SUIVANTE.
    const onValider = vi.fn()
    render(<PanneauManigance carte={carte} onValider={onValider} />)
    const bouton = screen.getByRole('button')
    fireEvent.click(bouton)
    fireEvent.click(bouton)
    expect(onValider).toHaveBeenCalledTimes(1)
  })

  it('se retourne au clic avant de disparaitre', () => {
    render(<PanneauManigance carte={carte} onValider={() => {}} />)
    const panneau = screen.getByRole('dialog')
    expect(panneau.className).not.toContain('est-retournee')
    fireEvent.click(screen.getByRole('button'))
    expect(panneau.className).toContain('est-retournee')
  })
})
