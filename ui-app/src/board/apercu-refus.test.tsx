// L'encart « Injouable » de l'aperçu au survol doit se VOIR.
//
// Demande de l'utilisateur, 30/09/2026 : la raison existait depuis le 10/09,
// mais en petite ligne rose APRÈS les mots-clés, et plusieurs signalements
// étaient des coups refusés que personne n'avait compris. L'encart est
// désormais juste sous la carte, avec un titre.
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, render } from '@testing-library/react'
import { CarteApercu } from './Board'

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon

afterEach(cleanup)

const carte = {
  id: '12',
  name: 'Uppercut',
  kind: 'event' as const,
  imageUrl: '/u.jpg',
  keywords: [{ nom: 'Riposte', definition: 'Inflige des dégâts à l’attaquant.' }],
}

describe('encart Injouable de l’aperçu', () => {
  it('titre, une ligne par raison, et placé AVANT les mots-clés', () => {
    render(<CarteApercu carte={carte} raisons={['Pas assez de ressources', 'Jouable seulement sous forme de héros']} />)
    const encart = document.querySelector('.apercu-refus')
    expect(encart).not.toBeNull()
    expect(encart?.querySelector('.apercu-refus-titre')?.textContent).toContain('Injouable')
    expect([...(encart?.querySelectorAll('li') ?? [])].map((li) => li.textContent)).toEqual([
      'Pas assez de ressources',
      'Jouable seulement sous forme de héros',
    ])
    const motsCles = document.querySelector('.apercu-mots-cles')
    expect(motsCles).not.toBeNull()
    expect(encart!.compareDocumentPosition(motsCles!) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('rien quand la carte est jouable', () => {
    render(<CarteApercu carte={carte} raisons={[]} />)
    expect(document.querySelector('.apercu-refus')).toBeNull()
  })
})
