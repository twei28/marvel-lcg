// LA FACE A DE LA MANIGANCE, EN GRAND, AVANT QU'ELLE SE RETOURNE.
//
// Demande de l'utilisateur, 15/09/2026 : « on doit voir la face A de la
// premiere manigance, puis on fait ok, puis elle se place sur la face B ».
// Le moteur ATTEND vraiment cette reponse (World.ConfirmMainSchemeReveal) :
// un second clic ne doit RIEN reposter, sous peine de repondre a la question
// SUIVANTE a la place du joueur.
//
// Correction du 15/09/2026 (relecture) : `repondre` demonte le panneau des
// que le moteur avance, ce qui coupait la transition CSS en plein vol sur un
// aller-retour local de quelques dizaines de ms — le joueur ne voyait qu'un
// eclair, jamais un retournement. On anime D'ABORD, on repond ENSUITE : le
// clic pose la classe tout de suite, la reponse part apres DUREE_RETOURNEMENT.
import { act, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { DUREE_RETOURNEMENT, PanneauManigance } from './PanneauManigance'
import type { WorldCard } from './world'

const carte = { id: 48, card_id: '01097a', pic_id: '01097a', name: 'The Break-In!' } as unknown as WorldCard

describe('PanneauManigance', () => {
  it('montre la carte en grand', () => {
    render(<PanneauManigance carte={carte} onValider={async () => true} />)
    const image = screen.getByRole('img')
    expect(image.getAttribute('src')).toContain('01097a')
  })

  describe('le retournement se joue avant la reponse au moteur', () => {
    beforeEach(() => {
      vi.useFakeTimers()
    })
    afterEach(() => {
      vi.useRealTimers()
    })

    it('pose la classe de retournement au clic, sans repondre tout de suite', () => {
      // Le cas qui garde le defaut trouve en relecture : si la reponse
      // repartait avant la fin de l'animation, ce cas resterait rouge.
      const onValider = vi.fn(async () => true)
      render(<PanneauManigance carte={carte} onValider={onValider} />)
      const panneau = screen.getByRole('dialog')
      fireEvent.click(screen.getByRole('button'))
      expect(panneau.className).toContain('est-retournee')
      expect(onValider).not.toHaveBeenCalled()
    })

    it('repond une seule fois, une fois le delai ecoule', () => {
      const onValider = vi.fn(async () => true)
      render(<PanneauManigance carte={carte} onValider={onValider} />)
      fireEvent.click(screen.getByRole('button'))
      vi.advanceTimersByTime(DUREE_RETOURNEMENT)
      expect(onValider).toHaveBeenCalledTimes(1)
    })

    it('ne valide pas deux fois, meme sur double clic rapproche', () => {
      // Le moteur n'attend qu'une reponse : une seconde poste dans le vide et
      // peut repondre a la question SUIVANTE.
      const onValider = vi.fn(async () => true)
      render(<PanneauManigance carte={carte} onValider={onValider} />)
      const bouton = screen.getByRole('button')
      fireEvent.click(bouton)
      fireEvent.click(bouton)
      vi.advanceTimersByTime(DUREE_RETOURNEMENT)
      expect(onValider).toHaveBeenCalledTimes(1)
    })
  })

  it('en mouvement reduit, repond sans attendre : rien a regarder, rien a attendre', () => {
    // ⚠ Pas de onTransitionEnd : sous prefers-reduced-motion la transition
    // CSS n'existe pas, l'evenement ne partirait jamais et la partie resterait
    // bloquee. Le delai doit tomber a 0 par une gate explicite, pas par un
    // evenement qui ne viendra pas.
    vi.stubGlobal('matchMedia', (media: string) => ({
      media,
      matches: true,
      onchange: null,
      addEventListener: () => {},
      removeEventListener: () => {},
      addListener: () => {},
      removeListener: () => {},
      dispatchEvent: () => false,
    }))
    try {
      const onValider = vi.fn(async () => true)
      render(<PanneauManigance carte={carte} onValider={onValider} />)
      fireEvent.click(screen.getByRole('button'))
      expect(onValider).toHaveBeenCalledTimes(1)
    } finally {
      vi.unstubAllGlobals()
    }
  })
})

// UN ENVOI QUI ECHOUE NE DOIT PAS FERMER LA PORTE.
//
// Defaut trouve en relecture le 15/09/2026 : `moteur.repondre` attrape
// l'erreur reseau, garde la demande et ne publie qu'une erreur. Le bouton du
// panneau, lui, restait `disabled` pour toujours : plus aucun moyen de
// renvoyer, partie figee sur la face A.
//
// Choix retenu : `repondre` DIT desormais si la reponse est partie
// (`Promise<boolean>`, voir moteur.ts). Le panneau se sert de ce fait, sans
// minuterie ni devinette.
describe('PanneauManigance — la reponse n’est pas partie', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })
  afterEach(() => {
    vi.useRealTimers()
  })

  it('⚠ ROUVRE SON BOUTON quand l’envoi a echoue', async () => {
    const onValider = vi.fn(async () => false)
    render(<PanneauManigance carte={carte} onValider={onValider} />)
    const bouton = screen.getByRole('button')
    const panneau = screen.getByRole('dialog')

    fireEvent.click(bouton)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(DUREE_RETOURNEMENT)
    })

    expect(onValider).toHaveBeenCalledTimes(1)
    expect(bouton.hasAttribute('disabled')).toBe(false)
    // La carte revient sur sa face A : rien n'a ete retourne, le moteur
    // attend toujours la meme reponse.
    expect(panneau.className).not.toContain('est-retournee')
  })

  it('et un second clic repart pour de bon', async () => {
    const onValider = vi.fn().mockResolvedValueOnce(false).mockResolvedValueOnce(true)
    render(<PanneauManigance carte={carte} onValider={onValider} />)
    const bouton = screen.getByRole('button')

    fireEvent.click(bouton)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(DUREE_RETOURNEMENT)
    })
    fireEvent.click(bouton)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(DUREE_RETOURNEMENT)
    })

    expect(onValider).toHaveBeenCalledTimes(2)
  })

  it('garde son bouton ferme quand la reponse est bien partie', async () => {
    // La garde « un seul envoi » ne doit pas sauter au passage : le moteur
    // n'attend qu'une reponse, une seconde repondrait a la question SUIVANTE.
    const onValider = vi.fn(async () => true)
    render(<PanneauManigance carte={carte} onValider={onValider} />)
    const bouton = screen.getByRole('button')

    fireEvent.click(bouton)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(DUREE_RETOURNEMENT)
    })
    fireEvent.click(bouton)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(DUREE_RETOURNEMENT)
    })

    expect(onValider).toHaveBeenCalledTimes(1)
    expect(bouton.hasAttribute('disabled')).toBe(true)
  })
})
