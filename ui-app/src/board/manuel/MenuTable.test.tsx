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
