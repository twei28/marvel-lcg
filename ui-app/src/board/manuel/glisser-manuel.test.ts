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
import { PILE_PAR_ZONE, reglagesGlisserManuel, type ContexteGlisserManuel } from './glisser-manuel'
import type { CibleAmelioration, Origine } from './poser-en-jeu'

/** Un contexte de trame minimal : type et origine de chaque carte, cibles d'amélioration. */
function monde(
  types: Record<number, string>,
  options: {
    origines?: Record<number, Origine>
    cibles?: CibleAmelioration[]
    engages?: number[]
    choisirCible?: ContexteGlisserManuel['choisirCible']
    cachees?: number[]
    proprietaires?: Record<number, number>
    interdites?: number[]
  } = {}
): ContexteGlisserManuel {
  const cibles = options.cibles ?? [{ id: 1, nom: 'Spider-Man' }]
  return {
    carte: (id) =>
      types[id] !== undefined
        ? { type: types[id], nom: `Carte ${id}`, faceCachee: (options.cachees ?? []).includes(id) }
        : undefined,
    origine: (id) => options.origines?.[id] ?? 'main',
    contexte: (siege) => ({ siege: siege ?? 0, identite: cibles[0], ciblesAmelioration: cibles }),
    proprietaire: (id) => options.proprietaires?.[id],
    peutBouger: (id) => !(options.interdites ?? []).includes(id),
    dejaEngage: (id) => (options.engages ?? []).includes(id),
    choisirCible: options.choisirCible ?? (() => undefined),
  }
}

async function commandeEnvoyee(emettreGeste: ReturnType<typeof emettreGesteDeTest>) {
  const [, deposer] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
  await deposer()
  return JSON.parse((vi.mocked(fetch).mock.calls[0][1] as RequestInit).body as string).commands as string[]
}

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

  it('se glisse aussi au doigt (lot 4, question 11)', () => {
    expect(reglagesGlisserManuel(emettreGesteDeTest()).auDoigt).toBe(true)
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

  // ⚠ LE CAS QUI MANQUAIT AU CORRECTIF DU 21/09/2026, signalé en jeu le
  // 22/09/2026 sur Angel ET Cable : « SPECIAL DECK » (un encadré fantôme,
  // vide) apparaissait pour TOUS les héros, y compris ceux qui n'ont AUCUN
  // deck spécial. Cause : `notre.additional_deck` vaut `[]` aussi bien pour
  // « ce héros n'a pas ce mécanisme » que pour « son deck spécial est
  // temporairement épuisé » (le moteur ne pose ce champ que si le héros le
  // crée lui-même en cours de partie) — rien ne les distingue depuis le
  // client. La zone « deck-special » ne doit donc JAMAIS afficher de pile
  // vide : seul le deck et la défausse PERSONNELS du joueur (témoin
  // ci-dessus) le peuvent, eux qui existent vraiment pour tout le monde.
  it('⚠ le deck spécial (Invocation, Reserve…) ne fantôme pas quand le héros n’en a pas', () => {
    const plateau = construirePlateau(mondeDeTest(), { playerId: 0, catalogue: catalogueVide })
    const zoneSpeciale = plateau.emplacements.find((zone) => zone.cle === 'deck-special')

    // La zone entière a disparu, comme avant le correctif du 21/09 : aucune
    // unité (vide ou non) ne doit y rester.
    expect(zoneSpeciale).toBeUndefined()
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
    expect(PILE_PAR_ZONE['annexes-nemesis']).toBeUndefined()
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

  it('refuse poliment un lâcher hors de la table, sans jamais interroger le moteur', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, {})).toBe(t('Lâche la carte sur la table ou sur une pile'))
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

  // Question 2 du 06/10/2026 : seule une amélioration (ou un attachement)
  // s'attache ; une autre carte se pose selon son type (voir plus bas).
  it('lâcher une amélioration sur une autre carte l’attache', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Upgrade' }))
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
      t('Lâche la carte sur la table ou sur une pile')
    )
    expect(emettreGeste).not.toHaveBeenCalled()
  })

  // Même gate, cette fois parce qu'aucune zone n'est connue du tout (lâcher
  // hors de tout `data-zone`, en théorie impossible en vraie table mais pas
  // à exclure d'un DOM inattendu) : refus, jamais un repli au hasard.
  it('refuse poliment l’attache quand la zone de la carte visée est inconnue', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste)
    expect(reglages.onDepot(42, { carteId: 501 })).toBe(t('Lâche la carte sur la table ou sur une pile'))
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
    expect(reglages.onDepot(42, { carteId: 42 })).toBe(t('Lâche la carte sur la table ou sur une pile'))
    expect(emettreGeste).not.toHaveBeenCalled()
  })

  // Lot 2 : `MoveTo` vers les engagés du siège, et non plus `Engage`, qui
  // BASCULE (un sbire déjà engagé se désengageait).
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
        body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EngagedEnemiesArea', 'Top', siege=0)"] }),
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
        body: JSON.stringify({ commands: ["Puzzle.MoveTo(42, 'EngagedEnemiesArea', 'Top', siege=0)"] }),
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


// --- Lot 2 du 06/10/2026 : poser une carte de la main, comme sur OCTGN ------
describe('poser une carte sur la table en mode manuel', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it.each([
    [{ zone: 'terrain-soutien', surLaTable: true }],
    [{ zone: 'terrain-combat', surLaTable: true }],
    [{ surLaTable: true }],
  ])('un allié lâché sur la table va dans les Alliés du siège (%o)', async (cible) => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Ally' }))
    expect(reglages.onDepot(42, cible)).toBeUndefined()
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'AlliesArea', 'Top', siege=0)"])
  })

  it('un allié lâché sur une carte en jeu se pose aussi selon son type (question 2)', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Ally' }))
    reglages.onDepot(42, { zone: 'terrain-soutien', carteId: 1, surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'AlliesArea', 'Top', siege=0)"])
  })

  it('la pile gagne toujours, même pour une carte qui se poserait', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, () => true, monde({ 42: 'Ally' }))
    reglages.onDepot(42, { zone: 'joueur-defausse', carteId: 3, surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'DiscardPile', 'Bottom', siege=0)"])
  })

  it('un événement lâché sur la manigance principale va à côté du héros, pas dans les manigances', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Event' }))
    reglages.onDepot(42, { zone: 'complot-principal', carteId: 7, surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'PlayerProcessingArea', 'Top', siege=0)"])
  })

  it('une manigance lâchée sur les manigances annexes y va', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(
      emettreGeste,
      undefined,
      monde({ 42: 'EncounterSideScheme' }, { origines: { 42: 'resolution' } })
    )
    reglages.onDepot(42, { zone: 'complots-secondaires', surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'SideSchemesArea', 'Top')"])
  })

  it('un sbire déjà engagé relâché sur son secteur : rien, jamais un désengagement', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(
      emettreGeste,
      undefined,
      monde({ 42: 'Minion' }, { origines: { 42: 'jeu' }, engages: [42] })
    )
    expect(reglages.onDepot(42, { secteur: CLE_PILE_ENGAGES, surLaTable: true })).toBeUndefined()
    expect(emettreGeste).not.toHaveBeenCalled()
    expect(reglages.accepte?.(42, { secteur: CLE_PILE_ENGAGES, surLaTable: true })).toBe(true)
  })

  it('une carte déjà en jeu relâchée sur la table : rien, aucun geste, pas de refus (question 13)', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Ally' }, { origines: { 42: 'jeu' } }))
    expect(reglages.onDepot(42, { zone: 'terrain-combat', surLaTable: true })).toBeUndefined()
    expect(emettreGeste).not.toHaveBeenCalled()
    expect(reglages.libelle(42, { zone: 'terrain-combat', surLaTable: true })).toBeUndefined()
    expect(reglages.accepte?.(42, { zone: 'terrain-combat', surLaTable: true })).toBe(true)
  })

  it('une ressource lâchée sur la table est refusée en bulle, rien n’est envoyé', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Resource' }))
    expect(reglages.onDepot(42, { surLaTable: true })).toBe(
      t('Une ressource se défausse pour payer : Suppr, ou glisse-la sur ta défausse')
    )
    expect(emettreGeste).not.toHaveBeenCalled()
    expect(reglages.accepte?.(42, { surLaTable: true })).toBe(false)
  })

  it('une amélioration lâchée sur la table s’attache à l’identité quand elle est la seule cible (question 3)', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Upgrade' }))
    reglages.onDepot(42, { surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(['Puzzle.Attach(42, 1)'])
  })

  it('une amélioration lâchée sur la table, plusieurs cibles : on ouvre le choix, rien n’est envoyé', () => {
    const emettreGeste = emettreGesteDeTest()
    const choisirCible = vi.fn()
    const cibles = [
      { id: 1, nom: 'Spider-Man' },
      { id: 4, nom: 'Black Cat' },
    ]
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Upgrade' }, { cibles, choisirCible }))
    expect(reglages.onDepot(42, { surLaTable: true })).toBeUndefined()
    expect(choisirCible).toHaveBeenCalledWith(42, 'Carte 42', cibles)
    expect(emettreGeste).not.toHaveBeenCalled()
  })

  it('l’étiquette nomme la carte et sa destination, sans coût (question 9)', () => {
    const reglages = reglagesGlisserManuel(emettreGesteDeTest(), undefined, monde({ 42: 'Support' }))
    const libelle = reglages.libelle(42, { surLaTable: true })
    expect(libelle).toBe(`${t('Poser en jeu')} : Carte 42 (${t('Soutiens')})`)
    expect(libelle).not.toMatch(/co[uû]t|cost/i)
  })

  it('lâcher hors du plateau : refus', () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Ally' }))
    expect(reglages.onDepot(42, {})).toBe(t('Lâche la carte sur la table ou sur une pile'))
    expect(emettreGeste).not.toHaveBeenCalled()
  })

  it('la table entière accueille une carte qui se pose, pas une ressource ni une carte déjà en jeu', () => {
    const reglages = reglagesGlisserManuel(
      emettreGesteDeTest(),
      undefined,
      monde({ 1: 'Ally', 2: 'Resource', 3: 'Ally' }, { origines: { 3: 'jeu' } })
    )
    expect(reglages.accueilleLaTable?.(1)).toBe(true)
    expect(reglages.accueilleLaTable?.(2)).toBe(false)
    expect(reglages.accueilleLaTable?.(3)).toBe(false)
  })

  it('les zones de manigance ne s’allument que pour une manigance', () => {
    const reglages = reglagesGlisserManuel(emettreGesteDeTest(), undefined, monde({ 1: 'Ally', 2: 'PlayerSideScheme' }))
    expect(reglages.zonesLegales(1).has('complot-principal')).toBe(false)
    expect(reglages.zonesLegales(2).has('complots-secondaires')).toBe(true)
    expect(reglages.zonesLegales(1).has('joueur-defausse')).toBe(true)
  })

  it('les cartes qui peuvent recevoir l’amélioration s’allument', () => {
    const cibles = [
      { id: 1, nom: 'Spider-Man' },
      { id: 4, nom: 'Black Cat' },
    ]
    const reglages = reglagesGlisserManuel(emettreGesteDeTest(), undefined, monde({ 42: 'Upgrade', 43: 'Ally' }, { cibles }))
    expect([...reglages.ciblesLegales(42)]).toEqual([1, 4])
    expect(reglages.ciblesLegales(43).size).toBe(0)
  })

  // ⚠ UNE PROPRIÉTÉ, PAS UN EXEMPLE : l'étiquette ne doit jamais promettre un
  // geste que le lâcher refuse, ni se taire sur un geste qu'il envoie.
  it('l’étiquette existe si et seulement si le lâcher envoie un geste', () => {
    const types: Record<number, string> = { 1: 'Ally', 2: 'Upgrade', 3: 'Resource', 4: 'Event', 5: 'Minion', 6: 'Hero', 7: 'Ally' }
    const cibles = [{}, { surLaTable: true }, { zone: 'joueur-deck' }, { zone: 'complot-principal', surLaTable: true },
      { zone: 'terrain-combat', carteId: 99, surLaTable: true }, { secteur: CLE_PILE_ENGAGES, surLaTable: true },
      { zone: 'annexes', carteId: 501, surLaTable: true }, { carteId: 1 }]
    for (const id of Object.keys(types).map(Number)) {
      for (const cible of cibles) {
        const emettreGeste = emettreGesteDeTest()
        const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde(types, { origines: { 7: 'jeu' } }))
        const libelle = reglages.libelle(id, cible)
        reglages.onDepot(id, cible)
        expect(libelle !== undefined, `carte ${id} (${types[id]}) sur ${JSON.stringify(cible)}`).toBe(
          emettreGeste.mock.calls.length > 0
        )
      }
    }
  })

  // D.8 de la spec : une carte face cachée (le dessus du deck) n'est jamais
  // nommée, et rien ne trahit son type avant qu'elle soit retournée. Constaté
  // dans le navigateur le 06/10/2026 : le dessus du deck, une ressource cachée,
  // était refusé avec « Une ressource se défausse pour payer ».
  it('une carte face cachée n’est ni nommée ni trahie par son type', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(
      emettreGeste,
      undefined,
      monde({ 30: 'Resource', 31: 'Ally', 32: 'Upgrade' }, { origines: { 30: 'pile', 31: 'pile', 32: 'pile' }, cachees: [30, 31, 32] })
    )
    expect(reglages.onDepot(30, { surLaTable: true })).toBe(
      t('Carte face cachée : retourne-la (Ctrl+F) ou glisse-la sur une pile')
    )
    expect(reglages.libelle(31, { surLaTable: true })).toBe(`${t('Poser en jeu')} : ${t('carte face cachée')}`)
    expect(reglages.ciblesLegales(32).size).toBe(0)
    expect(reglages.accueilleLaTable?.(30)).toBe(reglages.accueilleLaTable?.(31))
    reglages.onDepot(31, { surLaTable: true })
    const [libelle] = emettreGeste.mock.calls[0] as [string, () => Promise<boolean>]
    expect(libelle).not.toContain('Carte 31')
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(31, 'AlliesArea', 'Top', siege=0)"])
  })
})



// --- Lot 5 du 06/10/2026 : plusieurs héros, et chacun ses cartes ----------
describe('plusieurs héros en mode manuel', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it('lâchée dans le groupe du héros 2, la carte arrive chez lui (question 6)', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Ally' }))
    reglages.onDepot(42, { zone: 'terrain-soutien', surLaTable: true, siege: 1 })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'AlliesArea', 'Top', siege=1)"])
  })

  it('lâchée dans le vide, chez le héros d’où elle vient', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Ally' }, { proprietaires: { 42: 1 } }))
    reglages.onDepot(42, { surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'AlliesArea', 'Top', siege=1)"])
  })

  it('une pile du joueur vise son siège, jamais le premier joueur du moment', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, undefined, monde({ 42: 'Ally' }))
    reglages.onDepot(42, { zone: 'joueur-deck', carteId: 3, surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'PlayerDeck', 'Top', siege=0)"])
  })

  it('en ligne, la carte d’un autre joueur ne se soulève pas (question 14)', () => {
    const reglages = reglagesGlisserManuel(emettreGesteDeTest(), undefined, monde({ 42: 'Ally', 43: 'Ally' }, { interdites: [43] }))
    expect(reglages.estSource(42)).toBe(true)
    expect(reglages.estSource(43)).toBe(false)
  })
})

// Lot 6 du 06/10/2026 : comme sur OCTGN, Maj enfoncée pendant le glisser pose
// la carte FACE CACHÉE, en une seule commande.
describe('Maj pendant le glisser sur la table', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it('pose la carte face cachée, et l’étiquette le dit', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, () => true, monde({ 42: 'Support' }))
    expect(reglages.libelle(42, { surLaTable: true })).toContain(t('face cachée'))
    reglages.onDepot(42, { surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual([
      "Puzzle.MoveTo(42, 'SupportsArea', 'Top', siege=0, face_cachee=True)",
    ])
  })

  it('sans Maj, face visible', async () => {
    const emettreGeste = emettreGesteDeTest()
    const reglages = reglagesGlisserManuel(emettreGeste, () => false, monde({ 42: 'Support' }))
    reglages.onDepot(42, { surLaTable: true })
    expect(await commandeEnvoyee(emettreGeste)).toEqual(["Puzzle.MoveTo(42, 'SupportsArea', 'Top', siege=0)"])
  })
})
