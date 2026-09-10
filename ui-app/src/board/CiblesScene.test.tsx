// Le choix d'une cible DANS la scene du deroule detaille (livraison D de la
// spec du 7 septembre 2026) : les candidats en cartes, cliquables la, et la
// validation a la place de Suivant.
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { CiblesScene, type CibleScene } from './CiblesScene'
import type { ScanCardProps } from '../components/ScanCard'

const scan = (id: number, nom: string): ScanCardProps => ({
  id: String(id),
  name: nom,
  kind: 'minion',
  imageUrl: `/scan/${id}`,
})

const cibles = (agir: () => void): CibleScene[] => [
  { props: scan(1, 'Hydra Regular'), choisie: false, agir },
  { props: scan(2, 'Hydra Jet-Trooper'), choisie: true, agir },
]

describe('les cibles dans la scene', () => {
  it('montre chaque candidat en carte, et dit ou l on en est', () => {
    const { container } = render(
      <CiblesScene
        titre="Minion Activates Order"
        cibles={cibles(() => {})}
        choisies={1}
        minimum={2}
        maximum={2}
        prete={false}
        raison="Choisis encore 1 cible"
        valider={() => {}}
        annuler={() => {}}
      />
    )
    expect(container.querySelectorAll('.cibles-scene-carte .scan-card')).toHaveLength(2)
    expect(screen.getByText('Minion Activates Order')).toBeInTheDocument()
    expect(screen.getByText('1 / 2')).toBeInTheDocument()
    expect(screen.getByText('Choisis encore 1 cible')).toBeInTheDocument()
  })

  it('cliquer une carte la choisit', () => {
    const agir = vi.fn()
    const { container } = render(
      <CiblesScene
        titre="t"
        cibles={cibles(agir)}
        choisies={0}
        minimum={1}
        maximum={1}
        prete={false}
        raison=""
        valider={() => {}}
        annuler={() => {}}
      />
    )
    const carte = container.querySelector('.cibles-scene-carte .scan-card')
    expect(carte).not.toBeNull()
    fireEvent.click(carte as Element)
    expect(agir).toHaveBeenCalledTimes(1)
  })

  it('ne valide que quand la reponse est prete', () => {
    const valider = vi.fn()
    const { rerender } = render(
      <CiblesScene
        titre="t"
        cibles={cibles(() => {})}
        choisies={0}
        minimum={1}
        maximum={1}
        prete={false}
        raison=""
        valider={valider}
        annuler={() => {}}
      />
    )
    const bouton = screen.getByRole('button', { name: 'Confirmer' })
    expect(bouton).toBeDisabled()
    fireEvent.click(bouton)
    expect(valider).not.toHaveBeenCalled()
    rerender(
      <CiblesScene
        titre="t"
        cibles={cibles(() => {})}
        choisies={1}
        minimum={1}
        maximum={1}
        prete
        raison=""
        valider={valider}
        annuler={() => {}}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: 'Confirmer' }))
    expect(valider).toHaveBeenCalledTimes(1)
  })

  it('ouvre l agrandissement habituel au survol, a cote et pas sur place', () => {
    class ResizeObserverBouchon {
      observe() {}
      unobserve() {}
      disconnect() {}
    }
    vi.stubGlobal('ResizeObserver', ResizeObserverBouchon)
    const { container } = render(
      <CiblesScene
        titre="t"
        cibles={cibles(() => {})}
        choisies={0}
        minimum={1}
        maximum={1}
        prete={false}
        raison=""
        valider={() => {}}
        annuler={() => {}}
      />
    )
    // Le survol est ecoute sur le CONTENEUR (`mouseOver`, qui remonte), plus
    // sur chaque carte : c'est la regle commune d'`apercu-survol.ts`.
    const carte = container.querySelector('.cibles-scene-carte .scan-card') as Element
    fireEvent.mouseOver(carte)
    expect(document.querySelector('.carte-apercu')).not.toBeNull()
    // Le pointeur passe sur l'entete du panneau : ce n'est PAS une carte,
    // l'agrandissement doit se fermer.
    fireEvent.mouseOver(container.querySelector('.cibles-scene-entete') as Element)
    expect(document.querySelector('.carte-apercu')).toBeNull()
    vi.unstubAllGlobals()
  })

  it('la cible qui quitte la liste emporte son agrandissement', () => {
    // LE DEFAUT DU 10 SEPTEMBRE 2026, en petit : une carte demontee sous le
    // pointeur n'emet jamais `mouseleave`, et l'agrandissement restait ouvert
    // pour toujours, par-dessus les boutons du panneau. Aucun evenement de
    // souris ici : c'est la liste qui change, et cela doit suffire.
    class ResizeObserverBouchon {
      observe() {}
      unobserve() {}
      disconnect() {}
    }
    vi.stubGlobal('ResizeObserver', ResizeObserverBouchon)
    const panneau = (liste: ReturnType<typeof cibles>) => (
      <CiblesScene
        titre="t"
        cibles={liste}
        choisies={0}
        minimum={1}
        maximum={1}
        prete={false}
        raison=""
        valider={() => {}}
        annuler={() => {}}
      />
    )
    const toutes = cibles(() => {})
    const { container, rerender } = render(panneau(toutes))
    fireEvent.mouseOver(container.querySelector('.cibles-scene-carte .scan-card') as Element)
    expect(document.querySelector('.carte-apercu')).not.toBeNull()
    rerender(panneau(toutes.slice(1)))
    expect(document.querySelector('.carte-apercu')).toBeNull()
    vi.unstubAllGlobals()
  })

  it('annuler rend la main', () => {
    const annuler = vi.fn()
    render(
      <CiblesScene
        titre="t"
        cibles={[]}
        choisies={0}
        minimum={1}
        maximum={1}
        prete={false}
        raison=""
        valider={() => {}}
        annuler={annuler}
      />
    )
    fireEvent.click(screen.getByRole('button', { name: 'Annuler' }))
    expect(annuler).toHaveBeenCalledTimes(1)
  })
})
