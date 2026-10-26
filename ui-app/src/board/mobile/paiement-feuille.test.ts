// La feuille de PAIEMENT du telephone (26/10/2026) : quelles cartes elle montre pour payer.
// Rapport de l'utilisateur : « je ne peux pas selectionner de cartes pour payer sur le telephone » (« Pay 2 to play » cachait la main).
import { describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../../components/ScanCard'
import type { EtatInteractif } from '../interaction'
import type { Plateau, UniteAffichee } from '../zones'
import { cartesPayantes, resumePaiement } from './paiement-feuille'

const carte = (id: string, extra: Partial<ScanCardProps> = {}): ScanCardProps => ({ id, name: `Carte ${id}`, kind: 'event', imageUrl: `/scan/${id}.jpg`, ...extra })
const unite = (id: string): UniteAffichee => ({ cle: `u${id}`, carte: carte(id), attachees: [] })

function plateau(emplacements: Array<{ cle: string; ids: string[] }>): Plateau {
  return {
    emplacements: emplacements.map((e) => ({ cle: e.cle, titre: e.cle, groupes: e.ids.map((id) => [unite(id)]) })),
    nombreDeCartes: 0,
    idsAffiches: new Set<number>(),
  } as unknown as Plateau
}

describe('cartesPayantes : les cartes que la feuille de paiement propose', () => {
  it('prend les cartes au role « ressource », celles de la main d abord, puis celles de la table', () => {
    const interactifs = new Map<number, EtatInteractif>([
      [3, { role: 'ressource', choisie: false, agir: vi.fn() }],
      [1, { role: 'ressource', choisie: false, agir: vi.fn() }],
      [2, { role: 'porteur', choisie: false }],
    ])
    const p = plateau([
      { cle: 'heros', ids: ['3'] },
      { cle: 'main', ids: ['1', '2'] },
    ])
    expect(cartesPayantes(p, interactifs, new Map()).map((u) => u.carte.id)).toEqual(['1', '3'])
  })

  it('applique l interaction : la carte devient jouable, un toucher appelle l action du moteur', () => {
    const agir = vi.fn()
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'ressource', choisie: false, agir }]])
    const [payante] = cartesPayantes(plateau([{ cle: 'main', ids: ['1'] }]), interactifs, new Map())
    expect(payante!.carte.state).toBe('playable')
    payante!.carte.onSelect?.()
    expect(agir).toHaveBeenCalledTimes(1)
  })

  it('une carte deja posee en paiement reste dans la rangee (on peut la retirer d un second toucher)', () => {
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'ressource', choisie: true, fois: 1, agir: vi.fn() }]])
    const [payante] = cartesPayantes(plateau([{ cle: 'main', ids: ['1'] }]), interactifs, new Map())
    expect(payante!.carte.state).toBe('selected')
  })

  it('une carte n apparait qu une fois, et rien sans payeur', () => {
    const interactifs = new Map<number, EtatInteractif>([[1, { role: 'ressource', choisie: false, agir: vi.fn() }]])
    const p = plateau([
      { cle: 'main', ids: ['1'] },
      { cle: 'soutiens', ids: ['1'] },
    ])
    expect(cartesPayantes(p, interactifs, new Map())).toHaveLength(1)
    expect(cartesPayantes(plateau([{ cle: 'main', ids: ['1'] }]), new Map(), new Map())).toEqual([])
  })
})

describe('resumePaiement : payé, requis, manquant', () => {
  it('compte le manque', () => {
    expect(resumePaiement({ coutRequis: 2, coutPaye: 0 })).toEqual({ requis: 2, paye: 0, manque: 2, couvert: false })
    expect(resumePaiement({ coutRequis: 2, coutPaye: 1 })).toEqual({ requis: 2, paye: 1, manque: 1, couvert: false })
  })
  it('un cout couvert, ou un surpaiement, ne manque de rien', () => {
    expect(resumePaiement({ coutRequis: 2, coutPaye: 2 })).toEqual({ requis: 2, paye: 2, manque: 0, couvert: true })
    expect(resumePaiement({ coutRequis: 2, coutPaye: 3 }).manque).toBe(0)
  })
  it('un cout inconnu ne pretend rien', () => {
    expect(resumePaiement({ coutRequis: undefined, coutPaye: 0 })).toEqual({ requis: 0, paye: 0, manque: 0, couvert: false })
  })
})
