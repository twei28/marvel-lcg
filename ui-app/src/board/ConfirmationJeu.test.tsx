// Ce qui compte ici n'est pas l'apparence, c'est le CONTRAT : la promesse est
// toujours résolue. Un dialogue qui se fermerait sans répondre laisserait
// l'appelant suspendu, et le bouton qui l'a ouvert mort pour le reste de la
// partie — panne bien plus vicieuse que le `window.confirm` remplacé.
import { describe, expect, it } from 'vitest'
import { act, render, screen } from '@testing-library/react'
import { FournisseurConfirmation, useConfirmation } from './ConfirmationJeu'

/** Un bouton qui pose la question et affiche la réponse reçue. */
function Cobaye() {
  const confirmer = useConfirmation()
  return (
    <button
      type="button"
      onClick={async () => {
        const reponse = await confirmer({ titre: 'Quitter la partie ?', texte: 'Rien sauvegardé.' })
        document.title = reponse ? 'oui' : 'non'
      }}
    >
      poser
    </button>
  )
}

const monter = () =>
  render(
    <FournisseurConfirmation>
      <Cobaye />
    </FournisseurConfirmation>
  )

const poser = async () => {
  await act(async () => {
    screen.getByRole('button', { name: 'poser' }).click()
  })
}

const cliquer = async (nom: string) => {
  await act(async () => {
    screen.getByRole('button', { name: nom }).click()
  })
}

describe('FournisseurConfirmation', () => {
  it("n'affiche rien tant qu'on ne demande rien", () => {
    monter()
    expect(screen.queryByRole('alertdialog')).toBeNull()
  })

  it('affiche le titre et le texte demandés', async () => {
    monter()
    await poser()
    expect(screen.getByRole('alertdialog')).toBeTruthy()
    expect(screen.getByText('Quitter la partie ?')).toBeTruthy()
    expect(screen.getByText('Rien sauvegardé.')).toBeTruthy()
  })

  it('résout à vrai sur Confirmer, et se referme', async () => {
    monter()
    await poser()
    await cliquer('Confirmer')
    expect(document.title).toBe('oui')
    expect(screen.queryByRole('alertdialog')).toBeNull()
  })

  it('résout à faux sur Annuler', async () => {
    monter()
    await poser()
    await cliquer('Annuler')
    expect(document.title).toBe('non')
  })

  it('résout à faux sur Échap — la question ne reste jamais sans réponse', async () => {
    monter()
    await poser()
    await act(async () => {
      window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }))
    })
    expect(document.title).toBe('non')
    expect(screen.queryByRole('alertdialog')).toBeNull()
  })

  it('donne le focus au bouton qui valide, pour que Entrée réponde', async () => {
    monter()
    await poser()
    expect(document.activeElement?.textContent).toBe('Confirmer')
  })
})
