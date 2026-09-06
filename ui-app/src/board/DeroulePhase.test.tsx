// Le cartouche du deroule : une etape a la fois, validee avant la suivante.
//
// Il est FIXE en bas au centre et ne bouge jamais : l'oeil sait ou lire et la
// main ou cliquer des le deuxieme tour. On peut revenir en arriere pour relire,
// ce qui ne rejoue rien dans la partie : c'est une relecture, pas un undo.
import { describe, expect, it, vi } from 'vitest'
import { fireEvent, render, screen } from '@testing-library/react'
import { DeroulePhase } from './DeroulePhase'
import type { EtapeDeroule } from './deroule-phase'

const noms = (id: number) => ({ 50: 'Ultron', 12: 'Shuri' })[id] ?? `Carte ${id}`

const etapes: EtapeDeroule[] = [
  { cle: 'a', temps: 'menace', titre: 'menace', regle: 'regle:menace', boosts: [], consequences: [] },
  {
    cle: 'b',
    temps: 'activations',
    titre: 'attaque',
    regle: 'regle:activations',
    carteId: 50,
    cibleId: 12,
    boosts: [],
    consequences: [],
  },
]

const suivant = () => screen.getByRole('button', { name: /Suivant/i })

describe('cartouche du deroule', () => {
  it('montre la premiere etape et rien d autre', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    expect(screen.queryByText('Ultron attaque Shuri')).not.toBeInTheDocument()
  })

  it('avance d une etape au clic sur Suivant', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('rappelle la regle de l etape courante', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(screen.getByText(/Point 1/)).toBeInTheDocument()
  })

  it('revient en arriere sans rien rejouer', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    fireEvent.click(suivant())
    fireEvent.click(screen.getByRole('button', { name: /Précédent/i }))
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
  })

  it('n offre pas de Precedent sur la premiere etape', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(screen.queryByRole('button', { name: /Précédent/i })).toBeNull()
  })

  it('previent quand la derniere etape est validee', () => {
    const onTerminer = vi.fn()
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={onTerminer} />)
    fireEvent.click(suivant())
    fireEvent.click(suivant())
    expect(onTerminer).toHaveBeenCalledTimes(1)
  })

  it('ne rend rien sans etape', () => {
    const { container } = render(<DeroulePhase etapes={[]} noms={noms} onTerminer={() => {}} />)
    expect(container).toBeEmptyDOMElement()
  })

  it('montre les quatre temps, celui en cours mis en avant', () => {
    const { container } = render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(container.querySelectorAll('.deroule-temps li')).toHaveLength(4)
    expect(container.querySelector('.deroule-temps li.est-courant')?.textContent).toMatch(/Menace/i)
  })

  it('avance a la touche Entree', () => {
    // fireEvent (et non document.dispatchEvent) : setIndex declenche un
    // rendu, et fireEvent l'enveloppe dans un act() pour eviter
    // l'avertissement React sur une mise a jour hors act().
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: 'Enter' })
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('avance aussi a la barre d espace', () => {
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    fireEvent.keyDown(document, { key: ' ' })
    expect(screen.getByText('Ultron attaque Shuri')).toBeInTheDocument()
  })

  it('deroule tout a la touche Echap', () => {
    const onToutDerouler = vi.fn()
    render(
      <DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} onToutDerouler={onToutDerouler} />
    )
    document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', bubbles: true }))
    expect(onToutDerouler).toHaveBeenCalledTimes(1)
  })

  it('supporte de passer de zero etape a plusieurs sans tomber', () => {
    // Le plateau monte ce composant des que le mode « detaille » est actif,
    // donc hors phase du mechant, avec une liste vide. Si le `return null`
    // court-circuite un hook, React compte un hook de plus au rendu suivant
    // et fait tomber tout le plateau.
    const { rerender } = render(<DeroulePhase etapes={[]} noms={noms} onTerminer={() => {}} />)
    rerender(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
  })

  it('laisse le clavier tranquille quand on ecrit ailleurs', () => {
    // Le tchat est a portee de main pendant la phase : taper un espace dans son
    // champ ne doit pas faire avancer la phase du mechant.
    render(<DeroulePhase etapes={etapes} noms={noms} onTerminer={() => {}} />)
    const champ = document.createElement('input')
    document.body.append(champ)
    champ.focus()
    champ.dispatchEvent(new KeyboardEvent('keydown', { key: ' ', bubbles: true }))
    expect(screen.getByText('Menace sur la manigance principale')).toBeInTheDocument()
    champ.remove()
  })
})
