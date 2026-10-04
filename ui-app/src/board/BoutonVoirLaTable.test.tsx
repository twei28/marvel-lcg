// « Voir la table » : efface toutes les fenetres de decision d'un coup
// (signalement Yarro, 30/09/2026).
import { afterEach, describe, expect, it } from 'vitest'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { BoutonVoirLaTable, CLASSE_VOIR_LA_TABLE } from './BoutonVoirLaTable'

function poserFenetre(classe = 'demande-centrale') {
  const fenetre = document.createElement('section')
  fenetre.className = classe
  document.body.appendChild(fenetre)
  return fenetre
}

afterEach(() => {
  document.body.innerHTML = ''
  document.body.className = ''
})

describe('BoutonVoirLaTable', () => {
  it("reste grise tant qu'aucune fenetre de decision n'est ouverte", () => {
    render(<BoutonVoirLaTable />)
    expect((screen.getByRole('button', { name: 'Voir la table' }) as HTMLButtonElement).disabled).toBe(true)
  })

  it("s'active avec une fenetre, efface puis ramene toutes les fenetres a chaque clic", async () => {
    poserFenetre('assistant-action')
    render(<BoutonVoirLaTable />)
    const bouton = await screen.findByRole('button', { name: 'Voir la table' })
    await waitFor(() => expect((bouton as HTMLButtonElement).disabled).toBe(false))
    expect(bouton.getAttribute('aria-pressed')).toBe('false')
    expect(document.body.classList.contains(CLASSE_VOIR_LA_TABLE)).toBe(false)

    fireEvent.click(bouton)
    expect(document.body.classList.contains(CLASSE_VOIR_LA_TABLE)).toBe(true)
    expect(screen.getByRole('button', { name: 'Réafficher les fenêtres' }).getAttribute('aria-pressed')).toBe('true')

    fireEvent.click(screen.getByRole('button'))
    expect(document.body.classList.contains(CLASSE_VOIR_LA_TABLE)).toBe(false)
  })

  it("ramene les fenetres quand une nouvelle decision arrive", async () => {
    poserFenetre('deroule-phase')
    render(<BoutonVoirLaTable />)
    fireEvent.click(await screen.findByRole('button', { name: 'Voir la table' }))
    expect(document.body.classList.contains(CLASSE_VOIR_LA_TABLE)).toBe(true)

    act(() => {
      poserFenetre('plateau-selecteur')
    })
    await waitFor(() => expect(document.body.classList.contains(CLASSE_VOIR_LA_TABLE)).toBe(false))
  })

  it("se grise et laisse la table nette quand la derniere fenetre se ferme", async () => {
    const fenetre = poserFenetre()
    render(<BoutonVoirLaTable />)
    fireEvent.click(await screen.findByRole('button', { name: 'Voir la table' }))

    act(() => {
      fenetre.remove()
    })
    await waitFor(() => expect(document.body.classList.contains(CLASSE_VOIR_LA_TABLE)).toBe(false))
    expect((screen.getByRole('button') as HTMLButtonElement).disabled).toBe(true)
  })
})
