// Le bouton de tchat sur la table.
//
// La regle qui porte tout : PAS DE BOUTON QUAND IL N'Y A RIEN DERRIERE. Une
// partie locale n'a pas de site, un siege d'invite n'a pas de compte, et dans
// les deux cas le moteur repond `{actif: false}`. Un bouton qui n'ouvrirait
// qu'un panneau vide vaut moins que pas de bouton.
import { describe, expect, it, vi, afterEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { PanneauSalon } from './PanneauSalon'

const reponse = (donnees: unknown) =>
  ({ ok: true, json: async () => donnees }) as Response

afterEach(() => vi.unstubAllGlobals())

describe('bouton de tchat', () => {
  it('ne montre rien tant que le tchat ne repond pas', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(reponse({ actif: false })))
    const { container } = render(<PanneauSalon />)
    await waitFor(() => expect(container.querySelector('.bh-salon')).toBeNull())
  })

  it('apparait des que le tchat est joignable', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(reponse({ actif: true, pseudo: 'arnaud', messages: [], dernier: 0 }))
    )
    const { container } = render(<PanneauSalon />)
    await waitFor(() => expect(container.querySelector('.bh-salon')).not.toBeNull())
  })

  it('compte les messages des AUTRES arrives panneau ferme', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        reponse({
          actif: true,
          pseudo: 'arnaud',
          messages: [
            { id: 1, pseudo: 'chloe', texte: 'salut', quand: 'x' },
            { id: 2, pseudo: 'arnaud', texte: 'moi-meme', quand: 'x' },
          ],
          dernier: 2,
        })
      )
    )
    const { container } = render(<PanneauSalon />)
    // Un seul non lu : le notre ne compte pas, on sait ce qu'on vient d'ecrire.
    await waitFor(() => expect(container.querySelector('.salon-pastille')?.textContent).toBe('1'))
  })

  it('cesse d interroger quand il n y a pas de tchat derriere', async () => {
    // Sans cela, une partie SOLO — ou n'importe quelle table sans site — lancait
    // un appel toutes les quatre secondes, pour toujours, sans que rien ne
    // puisse jamais s'afficher. Le tchat n'apparait pas en cours de partie : une
    // seule reponse negative suffit a conclure.
    const fetch = vi.fn().mockResolvedValue(reponse({ actif: false }))
    vi.stubGlobal('fetch', fetch)
    vi.useFakeTimers()
    try {
      render(<PanneauSalon />)
      await vi.advanceTimersByTimeAsync(60_000)
      expect(fetch).toHaveBeenCalledTimes(1)
    } finally {
      vi.useRealTimers()
    }
  })

  it('ouvre le fil au clic et remet la pastille a zero', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue(
        reponse({
          actif: true,
          pseudo: 'arnaud',
          messages: [{ id: 1, pseudo: 'chloe', texte: 'je joue Shuri', quand: 'x' }],
          dernier: 1,
        })
      )
    )
    const { container } = render(<PanneauSalon />)
    const bouton = await waitFor(() => {
      const b = container.querySelector<HTMLButtonElement>('.bh-salon')
      expect(b).not.toBeNull()
      return b!
    })
    bouton.click()
    expect(await screen.findByText('je joue Shuri')).toBeInTheDocument()
    expect(container.querySelector('.salon-pastille')).toBeNull()
  })
})
