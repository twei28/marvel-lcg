// La « Phase dynamique » (16/10/2026) : les pièces qui lui sont propres, sans moteur.
import { act, cleanup, fireEvent, render, renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  DELAI_COMMANDE_MS,
  HistoriqueDynamique,
  QuestionDynamique,
  cleDeDecision,
  evenementsConfirmes,
  phraseQuestion,
  useCommandeUneFois,
} from './PhaseDynamique'
import type { EtapeDeroule } from './deroule-phase'
import type { QuestionDuMoteur } from './sous-cadre'

afterEach(() => {
  cleanup()
  vi.useRealTimers()
})

const etape = (cle: string, titre: string, extra: Partial<EtapeDeroule> = {}): EtapeDeroule =>
  ({ cle, titre, temps: 'activation', boosts: [], ...extra }) as unknown as EtapeDeroule

function question(): QuestionDuMoteur & { appels: string[] } {
  const appels: string[] = []
  const options = [
    { id: 1, name: 'Defense', bind_id: 0 },
    { id: 2, name: 'Ne pas defendre', bind_id: 0 },
  ]
  return {
    appels,
    demande: { event_name: 'Defend', prompt_text: '', options, ability_type: 'Normal' },
    interaction: {
      options,
      cibles: [],
      ressources: [],
      choisirOption: (o: { id: number }) => appels.push(`interaction:${o.id}`),
      valider: () => appels.push('valider'),
      annuler: () => appels.push('annuler'),
    },
    cartesParId: new Map(),
    choisirOption: (o: { id: number }) => appels.push(`option:${o.id}`),
    survolerOption: () => {},
    nomPorteur: () => undefined,
    texteCapacite: () => undefined,
    estEnMain: () => false,
    carteScene: () => undefined,
  } as unknown as QuestionDuMoteur & { appels: string[] }
}

describe('la phrase de la décision', () => {
  it('une défense se dit en clair, quelle que soit la carte qui attaque', () => {
    expect(phraseQuestion(question(), true)).toBe('Qui défend contre cette attaque ?')
  })

  it('sans question, rien ne s’affiche ; avec une question, une ligne annoncée', () => {
    const { container, rerender } = render(<QuestionDynamique q={undefined} defense={false} />)
    expect(container.textContent).toBe('')
    rerender(<QuestionDynamique q={question()} defense />)
    expect(container.querySelector('.dyn-question')?.textContent).toBe('Qui défend contre cette attaque ?')
  })
})

describe('l’historique des événements confirmés', () => {
  const etapes = [
    etape('a', 'menace'),
    etape('b', 'attaque'),
    etape('c', 'attaque', { etat: 'annonce' }),
    etape('d', 'revelation'),
    etape('e', 'bilan'),
  ]

  it('ne garde que ce qui est DÉJÀ passé, jamais l’étape en cours ni une annonce, le plus récent d’abord', () => {
    expect(evenementsConfirmes(etapes, 4).map((e) => e.cle)).toEqual(['d', 'b', 'a'])
    expect(evenementsConfirmes(etapes, 0)).toEqual([])
    expect(evenementsConfirmes(etapes, -3)).toEqual([])
  })

  it('montre trois lignes au plus, et un bouton pour tout voir quand il y en a davantage', () => {
    const beaucoup = Array.from({ length: 6 }, (_, i) => etape(`e${i}`, 'menace'))
    const { container, getByRole } = render(<HistoriqueDynamique etapes={beaucoup} index={6} />)
    expect(container.querySelectorAll('li')).toHaveLength(3)
    const bouton = getByRole('button')
    expect(bouton.getAttribute('aria-expanded')).toBe('false')
    fireEvent.click(bouton)
    expect(container.querySelectorAll('li')).toHaveLength(6)
    expect(bouton.getAttribute('aria-expanded')).toBe('true')
  })

  it('le paquet rencontre vide se lit en clair, jamais sous son nom interne', () => {
    const { container } = render(<HistoriqueDynamique etapes={[etape('p', 'paquet-vide'), etape('z', 'bilan')]} index={1} />)
    expect(container.textContent).toContain('Paquet rencontre vide')
    expect(container.textContent).not.toContain('paquet-vide')
  })

  it('rien du tout au premier événement', () => {
    const { container } = render(<HistoriqueDynamique etapes={etapes} index={0} />)
    expect(container.textContent).toBe('')
  })
})

describe('une commande une seule fois par décision', () => {
  it('un double clic sur la même option ne part qu’une fois ; une autre option reste libre', () => {
    const q = question()
    const { result } = renderHook(() => useCommandeUneFois(q, true))
    result.current!.choisirOption(q.demande.options[0]!)
    result.current!.choisirOption(q.demande.options[0]!)
    result.current!.choisirOption(q.demande.options[1]!)
    expect(q.appels).toEqual(['option:1', 'option:2'])
  })

  it('valider et annuler suivent la même règle', () => {
    const q = question()
    const { result } = renderHook(() => useCommandeUneFois(q, true))
    result.current!.interaction.valider()
    result.current!.interaction.valider()
    result.current!.interaction.annuler()
    result.current!.interaction.annuler()
    expect(q.appels).toEqual(['valider', 'annuler'])
  })

  it('la commande peut être redite quand le délai est passé (rien n’est retenu à jamais)', () => {
    vi.useFakeTimers()
    const q = question()
    const { result } = renderHook(() => useCommandeUneFois(q, true))
    result.current!.interaction.valider()
    act(() => {
      vi.advanceTimersByTime(DELAI_COMMANDE_MS + 10)
    })
    result.current!.interaction.valider()
    expect(q.appels).toEqual(['valider', 'valider'])
  })

  it('une décision différente repart de zéro', () => {
    const premiere = question()
    const seconde = question()
    seconde.demande = { ...seconde.demande, prompt_text: 'Autre question' }
    expect(cleDeDecision(premiere)).not.toBe(cleDeDecision(seconde))
  })

  it('hors Phase dynamique, la question n’est pas touchée (mêmes fonctions qu’avant)', () => {
    const q = question()
    const { result } = renderHook(() => useCommandeUneFois(q, false))
    expect(result.current).toBe(q)
  })
})
