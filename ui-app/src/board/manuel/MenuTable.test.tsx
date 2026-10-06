// MenuTable.test.tsx — le menu de la table (clic droit hors de toute carte).
import { fireEvent, render } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { MenuTable } from './MenuTable'

describe('MenuTable', () => {
  it('propose « Faire apparaître une carte », qui ouvre le catalogue et se ferme', () => {
    const onFaireApparaitre = vi.fn()
    const onFermer = vi.fn()
    const { getByText } = render(
      <MenuTable
        x={0}
        y={0}
        onFermer={onFermer}
        onFaireApparaitre={onFaireApparaitre}
        onTerminerPartie={vi.fn()}
        onVaincreStade={vi.fn()}
        onManigancePrincipale={vi.fn()}
        onToutRedresser={vi.fn()}
        onFinPhaseHeros={vi.fn()}
        onAmplification={vi.fn()}
        onHasard={vi.fn()}
      />
    )
    fireEvent.click(getByText('Faire apparaître une carte'))
    expect(onFaireApparaitre).toHaveBeenCalled()
    expect(onFermer).toHaveBeenCalled()
  })

  it('propose « Terminer la partie » (tâche 7), qui ouvre FinManuelle et se ferme', () => {
    const onTerminerPartie = vi.fn()
    const onFermer = vi.fn()
    const { getByText } = render(
      <MenuTable
        x={0}
        y={0}
        onFermer={onFermer}
        onFaireApparaitre={vi.fn()}
        onTerminerPartie={onTerminerPartie}
        onVaincreStade={vi.fn()}
        onManigancePrincipale={vi.fn()}
        onToutRedresser={vi.fn()}
        onFinPhaseHeros={vi.fn()}
        onAmplification={vi.fn()}
        onHasard={vi.fn()}
      />
    )
    fireEvent.click(getByText('Terminer la partie'))
    expect(onTerminerPartie).toHaveBeenCalled()
    expect(onFermer).toHaveBeenCalled()
  })

  it('propose les gestes OCTGN du méchant : vaincre ce stade, manigance terminée', () => {
    const onVaincreStade = vi.fn()
    const onManigancePrincipale = vi.fn()
    const onFermer = vi.fn()
    const { getByText } = render(
      <MenuTable
        x={0}
        y={0}
        onFermer={onFermer}
        onFaireApparaitre={vi.fn()}
        onTerminerPartie={vi.fn()}
        onVaincreStade={onVaincreStade}
        onManigancePrincipale={onManigancePrincipale}
        onToutRedresser={vi.fn()}
        onFinPhaseHeros={vi.fn()}
        onAmplification={vi.fn()}
        onHasard={vi.fn()}
      />
    )
    fireEvent.click(getByText('Vaincre ce stade'))
    expect(onVaincreStade).toHaveBeenCalledTimes(1)
    fireEvent.click(getByText('Manigance terminée'))
    expect(onManigancePrincipale).toHaveBeenCalledTimes(1)
    expect(onFermer).toHaveBeenCalledTimes(2)
  })

  it('se ferme à Échap', () => {
    const onFermer = vi.fn()
    render(
      <MenuTable
        x={0}
        y={0}
        onFermer={onFermer}
        onFaireApparaitre={vi.fn()}
        onTerminerPartie={vi.fn()}
        onVaincreStade={vi.fn()}
        onManigancePrincipale={vi.fn()}
        onToutRedresser={vi.fn()}
        onFinPhaseHeros={vi.fn()}
        onAmplification={vi.fn()}
        onHasard={vi.fn()}
      />
    )
    fireEvent.keyDown(document, { key: 'Escape' })
    expect(onFermer).toHaveBeenCalled()
  })

  it('se ferme au clic extérieur', () => {
    const onFermer = vi.fn()
    render(
      <MenuTable
        x={0}
        y={0}
        onFermer={onFermer}
        onFaireApparaitre={vi.fn()}
        onTerminerPartie={vi.fn()}
        onVaincreStade={vi.fn()}
        onManigancePrincipale={vi.fn()}
        onToutRedresser={vi.fn()}
        onFinPhaseHeros={vi.fn()}
        onAmplification={vi.fn()}
        onHasard={vi.fn()}
      />
    )
    fireEvent.mouseDown(document.body)
    expect(onFermer).toHaveBeenCalled()
  })

  it('propose le menu au hasard d’OCTGN et le tire sans toucher au moteur', () => {
    const onHasard = vi.fn()
    const onToutRedresser = vi.fn()
    const { getByText } = render(
      <MenuTable
        x={0}
        y={0}
        onFermer={vi.fn()}
        onFaireApparaitre={vi.fn()}
        onTerminerPartie={vi.fn()}
        onVaincreStade={vi.fn()}
        onManigancePrincipale={vi.fn()}
        onToutRedresser={onToutRedresser}
        onFinPhaseHeros={vi.fn()}
        onAmplification={vi.fn()}
        onHasard={onHasard}
      />
    )
    fireEvent.click(getByText('Pile ou face'))
    fireEvent.click(getByText('Nombre au hasard'))
    fireEvent.click(getByText('Joueur au hasard'))
    fireEvent.click(getByText('Tout redresser (Ctrl+Q)'))
    expect(onHasard.mock.calls.map((appel) => appel[0])).toEqual(['pile-ou-face', 'nombre', 'joueur'])
    expect(onToutRedresser).toHaveBeenCalled()
  })
})

// Constat du 06/10/2026 (lot 7, navigateur 1280x720) : ouvert au milieu de
// l'écran, le menu de la table (13 entrées depuis le lot 6) sortait par le bas ;
// « Mulligan » et « Terminer la partie » étaient inatteignables. Il devinait une
// hauteur fixe de 340 px, comme MenuTriche avant le 22/09/2026.
describe('MenuTable reste dans l’écran', () => {
  it('un menu plus haut que la place sous le curseur remonte, mesuré, pas deviné', () => {
    Object.defineProperty(window, 'innerWidth', { configurable: true, value: 1280 })
    Object.defineProperty(window, 'innerHeight', { configurable: true, value: 720 })
    vi.spyOn(HTMLElement.prototype, 'getBoundingClientRect').mockReturnValue({
      width: 242, height: 470, top: 0, left: 0, right: 242, bottom: 470, x: 0, y: 0,
      toJSON: () => ({}),
    })
    const { container } = render(
      <MenuTable
        x={640}
        y={330}
        onFermer={vi.fn()}
        onFaireApparaitre={vi.fn()}
        onTerminerPartie={vi.fn()}
        onVaincreStade={vi.fn()}
        onManigancePrincipale={vi.fn()}
        onToutRedresser={vi.fn()}
        onFinPhaseHeros={vi.fn()}
        onAmplification={vi.fn()}
        onHasard={vi.fn()}
      />
    )
    const boite = container.querySelector('.menu-triche') as HTMLElement
    // 720 - 470 - 8 de marge : le bas du menu tient dans l'écran.
    expect(parseFloat(boite.style.top)).toBe(242)
    vi.restoreAllMocks()
  })
})
