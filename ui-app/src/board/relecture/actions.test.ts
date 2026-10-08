import { describe, expect, it } from 'vitest'
import { actionsDe, degatsParRendu, ressourcesLisibles } from './actions'
import { phrasesDe } from './BandeauRelecture'
import type { Relecture } from './fichier'
import type { World } from '../world'

type Carte = { id: number; name: string; info?: Record<string, number> }
type Etat = {
  main?: Carte[]
  defausse?: Carte[]
  allies?: Carte[]
  heros?: Carte
  vilain?: Carte
  event_name?: string
  active_card_ids?: number[]
}

const ombre = (id: number, name: string, health?: number): Carte => ({ id, name, info: health === undefined ? {} : { health } })

function monde(n: number, e: Etat): World {
  return {
    render_id: n,
    round_id: 1,
    phase: 'Player 1 Turn',
    prompt: '',
    event_name: e.event_name ?? '',
    active_card_ids: e.active_card_ids ?? [],
    area_villain: [e.vilain ?? ombre(50, 'Rhino', 15)],
    players: [
      {
        area_hero: [e.heros ?? ombre(1, 'Captain America', 11)],
        hand_cards: e.main ?? [],
        player_discard_pile: e.defausse ?? [],
        allies: e.allies ?? [],
      },
    ],
  } as unknown as World
}

const relecture = (mondes: World[], ressources: Record<number, string> = {}): Relecture => ({
  entete: { format: 1, joueurs: [{ heros: 'Captain America' }] },
  trames: mondes.map((m, i) => ({ t: i * 1000, monde: m, demandes: {} })),
  curseurs: [],
  etapes: [],
  vus: [],
  ressources,
})

const bouclier = ombre(20, 'Bouclier')
const poing = ombre(21, 'Poing de fer')
const esquive = ombre(22, 'Esquive')
const vieille = ombre(23, 'Vieille carte')

describe('actions de la relecture', () => {
  // Une ressource depensee, telle que le moteur la rend.
  const depense = (n: number, e: Etat, id: number, nom: string, symbole: string) => {
    const m = monde(n, { ...e, event_name: 'WhenCardBeSpendAsResource', active_card_ids: [id] })
    ;(m as unknown as Record<string, unknown>).prompt = `Captain America gagne la ressource [[${symbole}]] de [(${id},01001) ${nom}], total [[${symbole}]]`
    return m
  }

  it('carte jouee, payee par deux cartes : la ressource vient du moteur', () => {
    const r = relecture([
      monde(1, { main: [bouclier, poing, esquive] }),
      monde(2, { main: [poing, esquive], allies: [bouclier] }),
      depense(3, { main: [esquive], defausse: [poing], allies: [bouclier] }, 21, 'Poing de fer', 'physical'),
      depense(4, { defausse: [poing, esquive], allies: [bouclier] }, 22, 'Esquive', 'wild'),
    ])
    const [action] = actionsDe(r)
    expect(action).toMatchObject({ index: 1, genre: 'joue', siege: 0, carte: { id: 20, nom: 'Bouclier' } })
    expect(phrasesDe(action, r)).toEqual([
      'Joueur 1 (Captain America) joue Bouclier',
      'Payé avec : Poing de fer (Physique), Esquive (Joker)',
    ])
  })

  it('une carte defaussee de la main sans depense n est ni jouee ni un paiement', () => {
    const r = relecture([
      monde(1, { main: [bouclier, vieille] }),
      monde(2, { main: [bouclier], defausse: [vieille] }),
      monde(3, { main: [], defausse: [vieille], allies: [bouclier] }),
    ])
    const actions = actionsDe(r)
    expect(actions.map((a) => a.carte?.nom)).toEqual(['Bouclier'])
    expect(actions[0].paiement).toEqual([])
  })

  it('une depense trop ancienne ne paie pas le coup suivant', () => {
    const r = relecture([
      monde(1, { main: [bouclier, poing] }),
      depense(2, { main: [bouclier], defausse: [poing] }, 21, 'Poing de fer', 'physical'),
      ...[3, 4, 5, 6, 7, 8, 9, 10, 11].map((n) => monde(n, { main: [bouclier], defausse: [poing] })),
      monde(12, { main: [], defausse: [poing], allies: [bouclier] }),
    ])
    expect(actionsDe(r)[0].paiement).toEqual([])
  })

  it('attaque nommee par le moteur, et ses degats', () => {
    const r = relecture([
      monde(1, {}),
      monde(2, { event_name: 'WhenUnitWouldTakeDamage', active_card_ids: [50, 1], vilain: ombre(50, 'Rhino', 12) }),
      monde(3, { event_name: 'WhenUnitWouldTakeDamage', active_card_ids: [50, 1], vilain: ombre(50, 'Rhino', 12) }),
    ])
    const actions = actionsDe(r)
    expect(actions).toHaveLength(1)
    expect(actions[0]).toMatchObject({ genre: 'attaque', acteur: { nom: 'Captain America' }, cible: { nom: 'Rhino' } })
    expect(actions[0].degats).toEqual([{ id: 50, nom: 'Rhino', montant: 3 }])
    expect(phrasesDe(actions[0], r)).toEqual(['Captain America attaque Rhino', '3 dégâts à Rhino'])
    expect(degatsParRendu(r).get(1)).toEqual([{ id: 50, nom: 'Rhino', montant: 3 }])
  })

  it('ressources lisibles, en lettres comme en mots', () => {
    expect(ressourcesLisibles('YB')).toEqual(['Mental', 'Énergie'].reverse())
    expect(ressourcesLisibles('[energy][energy]')).toEqual(['Énergie', 'Énergie'])
    expect(ressourcesLisibles('')).toEqual([])
  })
})

describe('partie reelle enregistree (Rhino / Spider-Man, 07/10/2026)', () => {
  it('Lance-toile paye par Daredevil, Salle d interrogatoire payee par le Joker du Lance-toile', async () => {
    const { readFileSync } = await import('node:fs')
    const { dirname, join } = await import('node:path')
    const { fileURLToPath } = await import('node:url')
    const { lireRelecture } = await import('./fichier')
    const brut = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '__fixtures__/partie-reelle.marvelreplay'))
    const r = await lireRelecture(brut.buffer.slice(brut.byteOffset, brut.byteOffset + brut.byteLength))
    const jouees = actionsDe(r).filter((a) => a.genre === 'joue')
    expect(jouees.map((a) => [a.carte?.id, a.paiement.map((p) => [p.id, p.ressources])])).toEqual([
      [20, [[23, ['Physique']]]],
      [31, [[20, ['Joker']]]],
    ])
  })
})
