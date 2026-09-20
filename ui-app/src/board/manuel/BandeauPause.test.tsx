// BandeauPause.test.tsx — le bandeau de pause manuelle EN COURS DE PARTIE
// (tâche 3, complété tâche 5). Comportements couverts :
//   1. ne s'affiche pas hors pause
//   2. s'affiche en pause
//   3. nomme qui a mis en pause (ou « quelqu'un » à défaut)
//   4. appelle `onReprendre`
//   5. (tâche 5) une question passée avec succès n'affiche aucun motif
//   6. (tâche 5) un refus affiche un motif LISIBLE, pas un code nu
//   7. (tâche 5) deux codes de refus distincts donnent deux phrases distinctes
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BandeauPause } from './BandeauPause'

describe('le bandeau de pause', () => {
  it('ne s\'affiche pas hors pause', () => {
    const { container } = render(
      <BandeauPause
        enPause={{ actif: false, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(container.querySelector('.bandeau-pause')).toBeNull()
  })

  it('s\'affiche en pause', () => {
    const { container } = render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(container.querySelector('.bandeau-pause')).not.toBeNull()
  })

  it('nomme qui a mis en pause', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: 'Nick Fury', depuis: '2026-09-20 14-30' }}
        onReprendre={() => {}}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.getByText(/Nick Fury/)).toBeTruthy()
  })

  it('dit « quelqu\'un » quand aucun pseudo n\'a voyagé', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.getByText(/Quelqu.un/)).toBeTruthy()
  })

  it('appelle onReprendre au clic sur Reprendre', () => {
    const reprendre = vi.fn()
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={reprendre}
        onPasser={async () => ({ ok: true })}
      />
    )
    fireEvent.click(screen.getByText('Reprendre'))
    expect(reprendre).toHaveBeenCalled()
  })

  // --- Tâche 5 : passer la question fautive ---------------------------------

  it('une question passée avec succès n\'affiche aucun motif de refus', async () => {
    const passer = vi.fn(async () => ({ ok: true as const }))
    const { container } = render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={passer}
      />
    )
    fireEvent.click(screen.getByText('Passer la question'))
    await waitFor(() => expect(passer).toHaveBeenCalled())
    expect(container.querySelector('.bandeau-pause-refus')).toBeNull()
  })

  it('une question forcée est refusée avec un motif LISIBLE, pas le code nu', async () => {
    const passer = vi.fn(async () => ({ ok: false as const, code: 'question_forcee' }))
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={passer}
      />
    )
    fireEvent.click(screen.getByText('Passer la question'))
    // ⚠ DISCRIMINANT : un plateau qui afficherait le CODE brut ("question_forcee")
    // au lieu de la phrase traduite passerait cette assertion textuelle-là si
    // elle cherchait juste "un texte est apparu" -- on vérifie donc l'ABSENCE
    // du code nu autant que la PRÉSENCE de la phrase lisible.
    const motif = await screen.findByText(/exige une réponse/)
    expect(motif).toBeTruthy()
    expect(screen.queryByText('question_forcee')).toBeNull()
  })

  it('aucune question en attente donne une phrase DIFFÉRENTE de « question forcée »', async () => {
    const passer = vi.fn(async () => ({ ok: false as const, code: 'aucune_question' }))
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={passer}
      />
    )
    fireEvent.click(screen.getByText('Passer la question'))
    const motif = await screen.findByText(/n’attend aucune réponse/)
    expect(motif).toBeTruthy()
    expect(screen.queryByText(/exige une réponse/)).toBeNull()
  })

  it('un échec réseau (code "reseau") affiche son propre motif, distinct des deux refus du moteur', async () => {
    const passer = vi.fn(async () => ({ ok: false as const, code: 'reseau' }))
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onReprendre={() => {}}
        onPasser={passer}
      />
    )
    fireEvent.click(screen.getByText('Passer la question'))
    const motif = await screen.findByText(/vérifie ta connexion/)
    expect(motif).toBeTruthy()
    expect(screen.queryByText(/exige une réponse/)).toBeNull()
    expect(screen.queryByText(/n’attend aucune réponse/)).toBeNull()
  })
})
