// glisser-manuel.test.ts — le glisser-déposer libre du mode manuel.
//
// ⚠ CORRECTIONS AU BRIEF (voir task-5-report.md) :
//  1. La table `PILE_PAR_ZONE` du brief confondait deux piles différentes
//     sous le même nom moteur `'AsideDeck'` (le set némésis du joueur ET les
//     mises de côté du scénario). Les clés ici sont celles que le plateau
//     pose RÉELLEMENT (`zones.ts`, `unite.pile`), jamais un raccourci
//     inventé — et chaque zone ambiguë (deck/défausse partagés par deux
//     piles moteur différentes) est vérifiée une par une dans le rapport.
//  2. Pas de second suivi de Maj : `sousLaPile` est un simple rappel fourni
//     par l'appelant (`board.tsx` lit `useTriche().estToucheEnfoncee`), cette
//     fonction ne pose aucune écoute.
//  3. Le geste passe par `emettreGeste` (celui de `useTriche`/`CoucheTriche`,
//     tâche 4 ter), jamais par un écrit direct au journal : c'est lui qui
//     retarde la ligne jusqu'au rendu qui connaît l'issue réelle.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { t } from '../langue'
import { CLE_PILE_ENGAGES } from '../zones'
import { PILE_PAR_ZONE, reglagesGlisserManuel } from './glisser-manuel'

/** Simule `emettreGeste` : invoque tout de suite le dépôt, comme le fait la
 *  vraie fonction (voir `CoucheTriche.tsx`), pour que les tests puissent
 *  observer la commande envoyée sans monter tout `useTriche`. */
function emettreGesteDeTest() {
  return vi.fn(async (_libelle: string, deposer: () => Promise<boolean>) => {
    await deposer()
  })
}

describe('le glisser du mode manuel', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it('soulève n’importe quelle carte', () => {
    const reglages = reglagesGlisserManuel(emettreGesteDeTest())
    expect(reglages.estSource(1)).toBe(true)
    expect(reglages.estSource(999)).toBe(true)
  })

  it('n’allume aucune cible : tout est permis, rien n’est suggéré', () => {
    const reglages = reglagesGlisserManuel(emettreGesteDeTest())
    expect(reglages.ciblesLegales(1).size).toBe(0)
  })

  it('accepte toutes les piles connues', () => {
    const reglages = reglagesGlisserManuel(emettreGesteDeTest())
    expect(reglages.zonesLegales(1).has('joueur-deck')).toBe(true)
    expect(reglages.zonesLegales(1).has('rencontre-encounter-deck')).toBe(true)
    expect(reglages.zonesLegales(1).has(CLE_PILE_ENGAGES)).toBe(true)
  })

  // ⚠ LE CAS QUI COMPTE : le deck du héros et le deck spécial (Invocation,
  // Reserve...) partagent le même `pile.cle` (« deck ») côté zones.ts, mais
  // ce sont deux piles moteur DIFFÉRENTES (`PlayerDeck` vs `AdditionalDeck`).
  // Une table qui les confondrait déplacerait une carte lâchée sur le deck
  // spécial dans le deck du héros, en silence.
  it('distingue le deck du héros du deck spécial', () => {
    expect(PILE_PAR_ZONE['joueur-deck']).toBe('PlayerDeck')
    expect(PILE_PAR_ZONE['soutien-deck']).toBe('AdditionalDeck')
    expect(PILE_PAR_ZONE['joueur-deck']).not.toBe(PILE_PAR_ZONE['soutien-deck'])
  })

  // ⚠ MÊME FAMILLE DE DÉFAUT : le set némésis du joueur (`annexes-nemesis`)
  // et les mises de côté du scénario sont visuellement dans la même colonne
  // « annexes », mais le set némésis SEUL a une pile désignable sans
  // ambiguïté (les mises de côté du scénario sont FONDUES avec la pile de
  // victoire et les cartes retirées — voir `zones.ts`, `pileFondue` — donc
  // volontairement ABSENTES de cette table, un lâcher dessus est refusé
  // plutôt que d'aller au hasard dans l'une des trois).
  it('traduit la pile du plateau en pile moteur', () => {
    expect(PILE_PAR_ZONE['rencontre-encounter-deck']).toBe('EncounterDeck')
    expect(PILE_PAR_ZONE['rencontre-encounter-discard']).toBe('EncounterDiscardPile')
    expect(PILE_PAR_ZONE['joueur-defausse']).toBe('DiscardPile')
    expect(PILE_PAR_ZONE['annexes-nemesis']).toBe('AsideDeck')
    expect(PILE_PAR_ZONE['annexes-visibles']).toBeUndefined()
    expect(PILE_PAR_ZONE['annexes-cachees']).toBeUndefined()
  })

  it('envoie le déplacement au lâcher, par la file du journal', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, { zone: 'rencontre-encounter-deck' })).toBeUndefined()
    expect(emettreGeste).toHaveBeenCalledTimes(1)
    const [libelle, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    expect(typeof libelle).toBe('string')
    await deposer()
    expect(fetch).toHaveBeenCalledWith(
      '/sandbox_command',
      expect.objectContaining({
        body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Top')"] }),
      })
    )
  })

  it('refuse poliment un lâcher dans le vide, sans jamais interroger le moteur', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, {})).toBe(t('Lâche la carte sur une pile'))
    expect(emettreGeste).not.toHaveBeenCalled()
  })

  it('dépose sous la pile quand Maj est enfoncée', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, () => true)
    reglages.onDepot(42, { zone: 'rencontre-encounter-deck' })
    const [, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    await deposer()
    expect(fetch).toHaveBeenCalledWith(
      '/sandbox_command',
      expect.objectContaining({
        body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Bottom')"] }),
      })
    )
  })

  // --- Les deux gestes que le brief oubliait -------------------------------

  it('lâcher une carte sur une autre carte attache', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, { carteId: 99 })).toBeUndefined()
    const [, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    await deposer()
    expect(fetch).toHaveBeenCalledWith(
      '/sandbox_command',
      expect.objectContaining({
        body: JSON.stringify({ commands: ["Puzzle.Attach(42, 99)"] }),
      })
    )
  })

  // ⚠ LE CAS QUI COMPTE : une pile se dessine avec une carte (son dessus, ou
  // sa carte-repère). Lâcher SUR CETTE CARTE doit rester un déplacement de
  // pile, pas une tentative d'attache sur le dessus du deck — sans quoi
  // relâcher une carte pile sur le deck Rencontre l'attacherait dessus.
  it('la pile l’emporte sur la carte quand on lâche sur son propre dessus', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    reglages.onDepot(42, { zone: 'rencontre-encounter-deck', carteId: 777 })
    const [, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    await deposer()
    expect(fetch).toHaveBeenCalledWith(
      '/sandbox_command',
      expect.objectContaining({
        body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EncounterDeck', 'Top')"] }),
      })
    )
  })

  it('ne s’attache pas à elle-même', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, { carteId: 42 })).toBe(t('Lâche la carte sur une pile'))
    expect(emettreGeste).not.toHaveBeenCalled()
  })

  it('lâcher un sbire sur la zone des ennemis engagés l’engage', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, { zone: CLE_PILE_ENGAGES })).toBeUndefined()
    const [, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    await deposer()
    expect(fetch).toHaveBeenCalledWith(
      '/sandbox_command',
      expect.objectContaining({
        body: JSON.stringify({ commands: ['Puzzle.Engage(42)'] }),
      })
    )
  })
})
