// BandeauPause.test.tsx — le bandeau de pause manuelle EN COURS DE PARTIE
// (tâche 3, complété tâche 5). Comportements couverts :
//   1. ne s'affiche pas hors pause
//   2. s'affiche en pause
//   3. nomme qui a mis en pause (ou « quelqu'un » à défaut)
//   4. n'a plus de bouton Reprendre (l'interrupteur de la barre reprend)
//   5. (tâche 5) une question passée avec succès n'affiche aucun motif
//   6. (tâche 5) un refus affiche un motif LISIBLE, pas un code nu
//   7. (tâche 5) deux codes de refus distincts donnent deux phrases distinctes
import { describe, expect, it, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { BandeauPause, dureeDepuis } from './BandeauPause'

describe('le bandeau de pause', () => {
  it('ne s\'affiche pas hors pause', () => {
    const { container } = render(
      <BandeauPause
        enPause={{ actif: false, par: '', depuis: '' }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(container.querySelector('.bandeau-pause')).toBeNull()
  })

  it('s\'affiche en pause', () => {
    const { container } = render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(container.querySelector('.bandeau-pause')).not.toBeNull()
  })

  it('nomme qui a mis en pause', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: 'Nick Fury', depuis: '2026-09-20 14-30' }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.getByText(/Nick Fury/)).toBeTruthy()
  })

  it('dit « quelqu\'un » quand aucun pseudo n\'a voyagé', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.getByText(/Quelqu.un/)).toBeTruthy()
  })

  it('n\'a plus de bouton Reprendre : c\'est l\'interrupteur de la barre qui reprend', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.queryByText('Reprendre')).toBeNull()
  })

  // --- Tâche 5 : passer la question fautive ---------------------------------

  it('une question passée avec succès n\'affiche aucun motif de refus', async () => {
    const passer = vi.fn(async () => ({ ok: true as const }))
    const { container } = render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
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

describe('le spectateur REGARDE la pause, il n’en sort pas (I2)', () => {
  // ⚠ CE N'EST PAS LA GARANTIE, C'EST LA POLITESSE : le moteur refuse déjà
  // les deux routes à un spectateur (`SpectateurPeutEcrire`, `web_server.py`,
  // et la garde de siège des routes `manuel_*`). Mais `BandeauPause` est
  // monté HORS de `.board-actions`, la seule chose que la CSS spectateur
  // masque : sans cette garde il voyait deux boutons vivants, dont « Passer
  // la question », qui répond à la place d'un joueur assis. C'est mot pour
  // mot le défaut du 15/09/2026 (« j'ai vu le bouton Annuler sur l'écran du
  // spectateur »).
  it('ne montre AUCUN bouton au spectateur, mais lui dit toujours pourquoi la table est arrêtée', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: 'Nick Fury', depuis: '2026-09-20 14-30' }}
        onPasser={async () => ({ ok: true })}
        lectureSeule
      />
    )
    expect(screen.queryByText('Reprendre')).toBeNull()
    expect(screen.queryByText('Passer la question')).toBeNull()
    // Le bandeau reste : un plateau arrêté et muet passe pour cassé.
    expect(screen.getByText(/Nick Fury/)).toBeTruthy()
  })

  it('garde le bouton Passer la question pour un joueur assis (témoin de contrôle)', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: 'Nick Fury', depuis: '' }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.getByText('Passer la question')).toBeTruthy()
  })
})

describe('le motif de refus ne survit pas à la pause qui l’a produit', () => {
  // Le bandeau reste MONTÉ hors pause (il rend `null`), donc son état de
  // refus survivait : une phrase affichée lors d'une pause réapparaissait
  // telle quelle à la pause suivante, des heures plus tard, sur une question
  // qui n'avait rien à voir.
  it('efface le motif quand la partie reprend', async () => {
    const passer = vi.fn(async () => ({ ok: false as const, code: 'question_forcee' }))
    const { rerender } = render(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onPasser={passer}
      />
    )
    fireEvent.click(screen.getByText('Passer la question'))
    expect(await screen.findByText(/exige une réponse/)).toBeTruthy()

    // La reprise, puis une NOUVELLE pause : le bandeau revient vierge.
    const reprise = (
      <BandeauPause
        enPause={{ actif: false, par: '', depuis: '' }}
        onPasser={passer}
      />
    )
    rerender(reprise)
    rerender(
      <BandeauPause
        enPause={{ actif: true, par: '', depuis: '' }}
        onPasser={passer}
      />
    )
    await waitFor(() => expect(screen.queryByText(/exige une réponse/)).toBeNull())
  })
})

describe('« depuis » est une DURÉE, pas l’heure murale du serveur', () => {
  // `pause_a` est un `Time.Format()` du SERVEUR (« 2026-09-20 17-12 ») :
  // affiché sous « depuis », un joueur distant y lisait une heure qui n'est
  // pas la sienne, et le format se lit mal comme une durée. Le moteur publie
  // désormais `pause_epoch` (secondes depuis l'époque, sans fuseau) et le
  // plateau en tire la durée avec SA propre horloge.
  const MAINTENANT = Date.UTC(2026, 8, 20, 17, 30, 0)

  it('rend « moins d’une minute » tout de suite après la pause', () => {
    expect(dureeDepuis(MAINTENANT / 1000 - 20, MAINTENANT)).toMatch(/moins d/)
  })

  it('rend des minutes, puis des heures', () => {
    expect(dureeDepuis(MAINTENANT / 1000 - 12 * 60, MAINTENANT)).toBe('12 min')
    expect(dureeDepuis(MAINTENANT / 1000 - (2 * 3600 + 5 * 60), MAINTENANT)).toBe('2 h 5 min')
  })

  it('ne rend jamais une durée négative quand l’horloge du serveur est en avance', () => {
    expect(dureeDepuis(MAINTENANT / 1000 + 300, MAINTENANT)).toMatch(/moins d/)
  })

  it('affiche la durée, et PAS l’horodatage du serveur, quand l’instant est connu', () => {
    vi.useFakeTimers()
    vi.setSystemTime(MAINTENANT)
    render(
      <BandeauPause
        enPause={{
          actif: true,
          par: 'Nick Fury',
          depuis: '2026-09-20 17-12',
          depuisEpoch: MAINTENANT / 1000 - 18 * 60,
        }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.getByText(/18 min/)).toBeTruthy()
    expect(screen.queryByText(/17-12/)).toBeNull()
    vi.useRealTimers()
  })

  it('retombe sur l’horodatage du moteur quand il ne publie aucun instant', () => {
    render(
      <BandeauPause
        enPause={{ actif: true, par: 'Nick Fury', depuis: '2026-09-20 17-12' }}
        onPasser={async () => ({ ok: true })}
      />
    )
    expect(screen.getByText(/17-12/)).toBeTruthy()
  })
})

