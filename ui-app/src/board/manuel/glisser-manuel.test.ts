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
import { ZONES_MANUELLES } from '../MenuTriche'
import { CLE_PILE_ENGAGES } from '../zones'
import { construirePlateau } from '../zones'
import { catalogueVide } from '../catalogue'
import { mondeDeTest } from './fixture-monde'
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

  it('conserve une cible pour les défausses vides', () => {
    const plateau = construirePlateau(mondeDeTest(), { playerId: 0, catalogue: catalogueVide })
    const pilesJoueur = plateau.emplacements.find((zone) => zone.cle === 'piles-joueur')
    const defausse = pilesJoueur?.groupes.flat().find((unite) => unite.pile === 'joueur-defausse')

    expect(defausse?.pileVide).toBe(true)
    expect(defausse?.pile).toBe('joueur-defausse')
  })

  // ⚠ LE CAS QUI COMPTE : le deck du héros et le deck spécial (Invocation,
  // Reserve...) partagent le même `pile.cle` (« deck ») côté zones.ts, mais
  // ce sont deux piles moteur DIFFÉRENTES (`PlayerDeck` vs `AdditionalDeck`).
  // Une table qui les confondrait déplacerait une carte lâchée sur le deck
  // spécial dans le deck du héros, en silence.
  it('distingue le deck du héros du deck spécial, et leurs défausses', () => {
    expect(PILE_PAR_ZONE['joueur-deck']).toBe('PlayerDeck')
    expect(PILE_PAR_ZONE['soutien-deck']).toBe('AdditionalDeck')
    expect(PILE_PAR_ZONE['joueur-deck']).not.toBe(PILE_PAR_ZONE['soutien-deck'])
    // Ronde de correction 1 : `soutien-defausse` (la défausse du deck
    // spécial) doit rester distincte de `joueur-defausse` (celle du héros),
    // maintenant que le moteur expose les deux (`AdditionalDiscardPile`,
    // `puzzle.py`).
    expect(PILE_PAR_ZONE['soutien-defausse']).toBe('AdditionalDiscardPile')
    expect(PILE_PAR_ZONE['soutien-defausse']).not.toBe(PILE_PAR_ZONE['joueur-defausse'])
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
    expect(reglages.onDepot(42, { zone: 'terrain-combat', carteId: 99 })).toBeUndefined()
    const [, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    await deposer()
    expect(fetch).toHaveBeenCalledWith(
      '/sandbox_command',
      expect.objectContaining({
        body: JSON.stringify({ commands: ["Puzzle.Attach(42, 99)"] }),
      })
    )
  })

  // ⚠ I1, LE CAS QUI COMPTE (correction finale). Une pile fondue (« Cartes
  // visibles », « Cartes cachées » — voir `zones.ts`, `pileFondue`) montre un
  // REPRÉSENTANT : une vraie carte, mais que le plateau ne dessine nulle
  // part comme un objet attachable. Avant la gate, l'attache s'y rabattait
  // par défaut et la carte lâchée disparaissait purement et simplement de la
  // table. `zone: 'annexes'` est précisément la zone de ces piles fondues,
  // absente de `PILE_PAR_ZONE` (voir plus haut) : elle doit rester absente
  // aussi des zones attachables.
  it('refuse poliment l’attache sur le représentant d’une pile fondue, sans faire disparaître la carte', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, { zone: 'annexes', carteId: 501 })).toBe(
      t('Lâche la carte sur une pile')
    )
    expect(emettreGeste).not.toHaveBeenCalled()
  })

  // Même gate, cette fois parce qu'aucune zone n'est connue du tout (lâcher
  // hors de tout `data-zone`, en théorie impossible en vraie table mais pas
  // à exclure d'un DOM inattendu) : refus, jamais un repli au hasard.
  it('refuse poliment l’attache quand la zone de la carte visée est inconnue', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, { carteId: 501 })).toBe(t('Lâche la carte sur une pile'))
    expect(emettreGeste).not.toHaveBeenCalled()
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

  it('lâcher un sbire sur le secteur des ennemis engagés l’engage', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    // Ronde de correction 2 (constat C1) : l'engagement se lit désormais sur
    // `secteur`, distinct de `zone` (que le mode ordinaire lit seul).
    expect(reglages.onDepot(42, { secteur: CLE_PILE_ENGAGES })).toBeUndefined()
    const [, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    await deposer()
    expect(fetch).toHaveBeenCalledWith(
      '/sandbox_command',
      expect.objectContaining({
        body: JSON.stringify({ commands: ['Puzzle.Engage(42)'] }),
      })
    )
  })

  // Le secteur l'emporte même quand une carte engagée est touchée en même
  // temps (le même geste qu'avant la séparation C1 zone/secteur).
  it('l’engagement l’emporte même en touchant une carte engagée', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(
      reglages.onDepot(42, { secteur: CLE_PILE_ENGAGES, zone: 'terrain-combat', carteId: 7 })
    ).toBeUndefined()
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

// Ronde de correction 1 (19/09/2026) : trois piles (`ReserveArea`,
// `MainSchemesArea`, `AdditionalDeck`) étaient atteignables au glisser mais
// absentes du menu de triche (`ZONES_MANUELLES`). Or `zones.ts` ne dessine
// PAS un emplacement vide (`emplacement()`) : une pile qui en disparaît sans
// être dans le menu devient DÉFINITIVEMENT inatteignable — ni glisser (rien à
// viser sur l'écran), ni clic droit (absente de la liste). C'est exactement
// l'impasse que « toute carte va dans toute pile » doit empêcher.
//
// ⚠ UNE PROPRIÉTÉ, PAS UN EXEMPLE : un test qui nomme les trois piles
// manquantes ne protège que celles-là. Celui-ci compare les deux tables
// entière et attrapera tout seul la prochaine pile ajoutée à l'une sans
// l'autre, sans attendre qu'un relecteur la remarque.
describe('toute pile atteignable au glisser reste atteignable au clic droit', () => {
  it('chaque pile moteur de PILE_PAR_ZONE figure dans ZONES_MANUELLES', () => {
    // + `CLE_PILE_ENGAGES`, qui n'est pas une entrée de `PILE_PAR_ZONE`
    // (Engage n'est pas un `MoveTo`) mais vise la même pile moteur que le
    // menu propose déjà sous 'EngagedEnemiesArea'.
    const piles = new Set([...Object.values(PILE_PAR_ZONE), 'EngagedEnemiesArea'])
    const manquantes = [...piles].filter((pile) => !ZONES_MANUELLES.includes(pile))
    expect(manquantes, `pile(s) atteignable(s) au glisser mais pas au clic droit : ${manquantes.join(', ')}`).toEqual([])
  })

  it('le témoin n’est pas vide : la propriété teste vraiment quelque chose', () => {
    expect(Object.keys(PILE_PAR_ZONE).length).toBeGreaterThan(0)
    expect(ZONES_MANUELLES.length).toBeGreaterThan(0)
  })
})
