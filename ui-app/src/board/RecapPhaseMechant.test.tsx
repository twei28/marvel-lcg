// Ce que ces cas protègent : le bilan doit RÉSUMER la phase du méchant, pas la
// dérouler, et ranger chaque fait sous l'étape qui l'a produit.
//
// Les trois se sont déjà trompés autrement. Le panneau d'origine groupait par
// nature (dégâts / menace / révélé), ce qui mélangeait la menace posée à
// l'étape 1 et celle d'une manigance jouée à l'étape 4. Sa refonte a laissé
// entrer la narration du moteur : poser une menace affichait six lignes dont
// une seule disait quelque chose. Et un total en valeur absolue compterait une
// menace RETIRÉE comme une menace posée — un bilan faux dans le sens qui
// exagère le danger.
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import { bilanDeLaPhase, detailDuCalcul, RecapPhaseMechant, type Noms } from './RecapPhaseMechant'
import type { EntreeHistorique } from './HistoriquePartie'
import type { FaitMechant, World } from './world'

let compteur = 0
const entree = (partiel: Partial<EntreeHistorique>): EntreeHistorique => ({
  cle: `e${(compteur += 1)}`,
  type: 'card',
  renderId: compteur,
  round: 2,
  phase: 'Reveal Encounter Cards',
  titre: 'Carte',
  ...partiel,
})

/** L'historique empile les plus récentes EN TÊTE : les cas suivent cet ordre. */
const commeDansLHistorique = (...anciennesDAbord: EntreeHistorique[]) =>
  [...anciennesDAbord].reverse()

const noms: Noms = {
  carte: (id) => (id === undefined ? undefined : `Carte#${id}`),
  heros: (joueur) => (joueur === undefined ? undefined : `Héros${joueur}`),
  plafond: (id) => (id === 7 ? 6 : undefined),
}

describe('bilanDeLaPhase — découpage', () => {
  it('range chaque fait sous son étape, dans l’ordre de la carte de référence', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 1, restant: 1, plafond: 6, cibleId: 7 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3, acteur: 'Klaw', cibleId: 9 }),
        entree({ phase: 'Reveal Encounter Cards', nomCarte: 'Gang-Up' })
      ),
      2,
      noms
    )

    expect(bilan?.etapes.map((e) => e.numero)).toEqual([1, 2, 4])
  })

  it('ignore les autres rounds et les autres phases', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ round: 1, phase: 'Enemy Activation', type: 'damage', valeur: -9 }),
        entree({ phase: 'Player Turn', titre: 'Carte jouée' }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -1 })
      ),
      2,
      noms
    )
    expect(bilan?.etapes).toHaveLength(1)
    expect(bilan?.etapes[0].degats).toBe(1)
  })

  it('ne rend rien quand la phase n’a produit aucun fait', () => {
    expect(bilanDeLaPhase([], 2, noms)).toBeUndefined()
    expect(bilanDeLaPhase(commeDansLHistorique(entree({ phase: 'Player Turn' })), 2, noms)).toBeUndefined()
  })
})

describe('bilanDeLaPhase — résumé', () => {
  it('écarte la narration du moteur des lignes, mais la garde sous le repli', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'Main scheme phase start' }),
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'would place 1 threat' }),
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 1, restant: 1, plafond: 6, cibleId: 7 }),
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'placed 1 threat token' }),
        entree({ phase: 'Main Scheme Place Threat', type: 'text', titre: 'Main scheme phase end' })
      ),
      2,
      noms
    )

    const etape = bilan!.etapes[0]
    expect(etape.lignes).toHaveLength(1)
    expect(etape.lignes[0]).toMatchObject({
      genre: 'menace',
      titre: 'Carte#7',
      valeur: 1,
      restant: 1,
      plafond: 6,
    })
    expect(etape.brut).toHaveLength(5)
  })

  it('rattache les cartes de boost à l’attaque qui les a retournées', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', nomCarte: 'Sonic Boom', boost: true, cibleId: 21 }),
        entree({ phase: 'Enemy Activation', nomCarte: 'T’Challa’s Shadow', boost: true, cibleId: 22 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3, restant: 8, acteur: 'Klaw', cibleId: 9 })
      ),
      2,
      noms
    )

    const etape = bilan!.etapes[0]
    expect(etape.lignes).toHaveLength(1)
    expect(etape.lignes[0]).toMatchObject({
      genre: 'attaque',
      titre: 'Klaw attaque Carte#9',
      valeur: -3,
      restant: 8,
    })
    expect(etape.lignes[0].boosts?.map((b) => b.nom)).toEqual(['Sonic Boom', 'T’Challa’s Shadow'])
    // Un boost n'est pas une carte de plus : il appartient à l'activation.
    expect(etape.cartes).toBe(0)
  })

  it('distingue une manigance d’ennemi d’une attaque', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'threat', valeur: 2, restant: 3, plafond: 6, acteur: 'Klaw', cibleId: 7 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].lignes[0]).toMatchObject({
      genre: 'manigance',
      titre: 'Klaw manigance sur Carte#7',
      valeur: 2,
      restant: 3,
      plafond: 6,
    })
  })

  it('attribue à une carte révélée ce qu’elle a produit ensuite', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ nomCarte: 'Gang-Up', joueur: 0, cibleId: 31 }),
        entree({ type: 'damage', valeur: -2, restant: 6, cibleId: 9 })
      ),
      2,
      noms
    )
    const ligne = bilan!.etapes[0].lignes[0]
    expect(ligne).toMatchObject({ genre: 'carte', titre: 'Gang-Up', heros: 'Héros0' })
    expect(ligne.effets).toEqual(['Carte#9 : 2 dégâts → 6 PV'])
    // Une seule ligne : la conséquence est DANS la carte, pas à côté.
    expect(bilan!.etapes[0].lignes).toHaveLength(1)
  })

  it('garde la phrase du moteur quand l’auteur de l’attaque est inconnu', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', titre: 'Black Panther subit 3 dégât(s)', valeur: -3, cibleId: 9 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].lignes[0].titre).toBe('Black Panther subit 3 dégât(s)')
  })

  it('ne compte qu’une fois un fait que le moteur a rendu trois fois', () => {
    // Vu en jeu : trois lignes « Underground Distribution +1 → 1/6 » et un
    // total de « +3 » sur une manigance qui n'en portait qu'une. L'état final
    // identique est ce qui les démasque — trois poses réelles auraient donné
    // 1/6, puis 2/6, puis 3/6.
    const triple = (rendu: number) =>
      entree({
        phase: 'Main Scheme Place Threat',
        type: 'threat',
        titre: 'Underground Distribution gagne 1 menace',
        renderId: rendu,
        valeur: 1,
        restant: 1,
        plafond: 6,
        cibleId: 7,
      })
    const bilan = bilanDeLaPhase(commeDansLHistorique(triple(10), triple(11), triple(12)), 2, noms)

    const etape = bilan!.etapes[0]
    expect(etape.lignes).toHaveLength(1)
    expect(etape.lignes[0].valeur).toBe(1)
    expect(etape.menace).toBe(1)
    // Le déroulé, lui, garde les trois : c'est ce que le moteur a vraiment émis.
    expect(etape.brut).toHaveLength(3)
  })

  it('fond en une seule ligne les deux temps d’une attaque gonflée par des boosts', () => {
    // Vu en jeu : « Black Panther : 2 dégâts → 9 PV » puis « 1 dégât → 8 PV ».
    // Ce sont deux temps du MÊME coup, pas deux attaques.
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', nomCarte: 'Sonic Boom', boost: true, cibleId: 21 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2, restant: 9, acteur: 'Klaw', cibleId: 9 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -1, restant: 8, acteur: 'Klaw', cibleId: 9 })
      ),
      2,
      noms
    )

    const etape = bilan!.etapes[0]
    expect(etape.lignes).toHaveLength(1)
    expect(etape.lignes[0].titre).toBe('Klaw attaque Carte#9')
    expect(etape.lignes[0].valeur).toBe(-3)
    expect(etape.lignes[0].restant).toBe(8)
    expect(etape.degats).toBe(3)
  })

  it('ne fond pas deux ennemis différents qui frappent la même cible', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2, restant: 9, acteur: 'Klaw', cibleId: 9 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -1, restant: 8, acteur: 'Tiger Shark', cibleId: 9 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].lignes).toHaveLength(2)
  })

  it('garde deux poses de menace réelles, qui laissent des états différents', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 1, restant: 1, plafond: 6, cibleId: 7 }),
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 1, restant: 2, plafond: 6, cibleId: 7 })
      ),
      2,
      noms
    )
    // Fondues en une ligne, comme demandé — mais le total reste juste.
    expect(bilan!.etapes[0].lignes).toHaveLength(1)
    expect(bilan!.etapes[0].lignes[0].valeur).toBe(2)
    expect(bilan!.etapes[0].lignes[0].restant).toBe(2)
    expect(bilan!.etapes[0].menace).toBe(2)
  })

  it('n’affiche qu’une fois une carte révélée que le moteur a rendue deux fois', () => {
    const revelee = (rendu: number) =>
      entree({ titre: 'Advance révélée', nomCarte: 'Advance', joueur: 0, cibleId: 31, renderId: rendu })
    const bilan = bilanDeLaPhase(commeDansLHistorique(revelee(10), revelee(11)), 2, noms)
    expect(bilan!.etapes[0].lignes).toHaveLength(1)
    expect(bilan!.etapes[0].cartes).toBe(1)
  })

  it('déduit la menace retirée du total au lieu de l’ajouter', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: 3, restant: 3 }),
        entree({ phase: 'Main Scheme Place Threat', type: 'threat', valeur: -1, restant: 2 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].menace).toBe(2)
  })

  it('compte les dégâts en positif, quel que soit le signe de la variation de PV', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2 })
      ),
      2,
      noms
    )
    expect(bilan!.etapes[0].degats).toBe(5)
  })
})

// Le journal du moteur (étape 2) : la seule source qui connaisse la COMPOSITION
// d'un coup. Ce que ces cas protègent, c'est qu'il REMPLACE la déduction au lieu
// de s'y ajouter — les deux ensemble afficheraient chaque activation deux fois,
// ce qui est précisément le défaut qu'il vient corriger.
describe('bilanDeLaPhase — journal du moteur', () => {
  const attaque: FaitMechant = {
    genre: 'attaque',
    auteur: 'Klaw',
    auteur_id: 3,
    cible: 'Black Panther',
    cible_id: 9,
    base: 3,
    boost: 2,
    defense: 0,
    inflige: 5,
    subi: 5,
    restant: 8,
    boosts: [
      { nom: 'Sonic Boom', id: 21, apport: 2 },
      { nom: 'T’Challa’s Shadow', id: 22, apport: 0 },
    ],
  }

  it('remplace les activations déduites au lieu de s’y ajouter', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', nomCarte: 'Sonic Boom', boost: true, cibleId: 21 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -5, restant: 8, acteur: 'Klaw', cibleId: 9 })
      ),
      2,
      noms,
      [attaque]
    )

    const etape = bilan!.etapes.find((e) => e.numero === 2)!
    expect(etape.lignes).toHaveLength(1)
    expect(etape.lignes[0].titre).toBe('Klaw attaque Black Panther')
    expect(etape.lignes[0].calcul).toEqual({ base: 3, boost: 2, defense: 0 })
    expect(etape.lignes[0].boosts?.map((b) => `${b.nom} +${b.apport}`)).toEqual([
      'Sonic Boom +2',
      'T’Challa’s Shadow +0',
    ])
  })

  it('aligne les totaux sur ce qui est affiché, pas sur les entrées déduites', () => {
    // La déduction voyait 5 + 5 (le même coup rendu deux fois) ; le journal
    // n'en connaît qu'un. Un total resté sur la déduction annoncerait 10.
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -5, restant: 8, acteur: 'Klaw', cibleId: 9, renderId: 10 }),
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -5, restant: 3, acteur: 'Klaw', cibleId: 9, renderId: 11 })
      ),
      2,
      noms,
      [attaque]
    )
    expect(bilan!.etapes.find((e) => e.numero === 2)!.degats).toBe(5)
  })

  it('retombe sur la déduction quand le moteur ne publie rien', () => {
    // Sauvegarde ancienne, ou moteur non mis à jour : le bilan doit rester
    // utile plutôt que de se vider.
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -3, restant: 8, acteur: 'Klaw', cibleId: 9 })
      ),
      2,
      noms,
      []
    )
    expect(bilan!.etapes[0].lignes[0].titre).toBe('Klaw attaque Carte#9')
    expect(bilan!.etapes[0].lignes[0].calcul).toBeUndefined()
  })

  it('lit le seuil de la manigance sur la carte, que le journal ne porte pas', () => {
    const manigance: FaitMechant = {
      genre: 'manigance', auteur: 'Klaw', auteur_id: 3,
      cible: 'Underground Distribution', cible_id: 7,
      base: 1, boost: 2, defense: 0, inflige: 3, subi: 3, restant: 4,
      boosts: [{ nom: 'Sonic Boom', id: 21, apport: 2 }],
    }
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(entree({ phase: 'Enemy Activation', type: 'threat', valeur: 3, acteur: 'Klaw', cibleId: 7 })),
      2,
      noms,
      [manigance]
    )
    const ligne = bilan!.etapes[0].lignes[0]
    expect(ligne).toMatchObject({ genre: 'manigance', valeur: 3, restant: 4, plafond: 6 })
  })
})

describe('bilanDeLaPhase — où se range une activation', () => {
  // Signalé en jeu : « on dirait que Klaw m'attaque deux fois sans raison ».
  // La seconde attaque venait d'Assault, révélée à l'étape 4 — mais le bilan
  // versait TOUTES les activations dans l'étape 2, sans dire d'où elles
  // venaient.
  const activation = (phase: string, cause: string): FaitMechant => ({
    genre: 'attaque', phase, cause,
    auteur: 'Klaw', auteur_id: 3, cible: 'Black Panther', cible_id: 9,
    base: 0, boost: 2, defense: 0, inflige: 2, subi: 2, restant: 9, boosts: [],
  })

  it('range l’attaque déclenchée sous l’étape où elle a eu lieu', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2, acteur: 'Klaw', cibleId: 9 }),
        entree({ phase: 'Reveal Encounter Cards', nomCarte: 'Assault', joueur: 0, cibleId: 41 })
      ),
      2,
      noms,
      [activation('Enemy Activation', ''), activation('Reveal Encounter Cards', 'Assault')]
    )

    const activations = bilan!.etapes.find((e) => e.numero === 2)!
    const revelees = bilan!.etapes.find((e) => e.numero === 4)!
    expect(activations.lignes).toHaveLength(1)
    expect(activations.lignes[0].cause).toBeUndefined()
    // Dans l'étape 4, l'attaque suit IMMÉDIATEMENT la carte qui l'a causée.
    expect(revelees.lignes.map((l) => l.titre)).toEqual(['Assault', 'Klaw attaque Black Panther'])
    expect(revelees.lignes[1].cause).toBe('Assault')
  })

  it('n’attribue plus à la carte révélée des dégâts qui ne sont pas les siens', () => {
    // La déduction collait les dégâts à la dernière carte révélée, qui n'y
    // était souvent pour rien : ici Melter recevait le coup d'Assault.
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({ phase: 'Reveal Encounter Cards', nomCarte: 'Melter', joueur: 0, cibleId: 40 }),
        entree({ phase: 'Reveal Encounter Cards', type: 'damage', valeur: -2, restant: 9, cibleId: 9 })
      ),
      2,
      noms,
      [activation('Reveal Encounter Cards', 'Assault')]
    )
    const melter = bilan!.etapes[0].lignes.find((l) => l.titre === 'Melter')!
    expect(melter.effets).toBeUndefined()
    expect(bilan!.etapes[0].degats).toBe(2)
  })

  it('garde à l’étape des activations ce qu’un moteur ancien envoie sans phase', () => {
    const sansPhase = { ...activation('', ''), phase: undefined }
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(entree({ phase: 'Enemy Activation', type: 'damage', valeur: -2, cibleId: 9 })),
      2,
      noms,
      [sansPhase]
    )
    expect(bilan!.etapes.find((e) => e.numero === 2)!.lignes).toHaveLength(1)
  })
})

describe('detailDuCalcul', () => {
  it('n’écrit la composition que si elle apprend quelque chose', () => {
    // Sans boost ni défense, elle répéterait le chiffre déjà affiché à droite.
    expect(detailDuCalcul({ base: 3, boost: 0, defense: 0 })).toBeUndefined()
    expect(detailDuCalcul({ base: 3, boost: 2, defense: 0 })).toBe('3 de base + 2 de boost')
    expect(detailDuCalcul({ base: 3, boost: 2, defense: 1 })).toBe(
      '3 de base + 2 de boost − 1 de défense'
    )
  })
})

// --- Deux panneaux ne se disputent pas l'ecran --------------------------------
// Le recap est un bilan d'APRES-phase, le cartouche du deroule un guide PENDANT
// la phase. En mode detaille les deux existent : ils doivent se suivre, jamais
// se superposer. Un doublon d'affichage a deja coute un tour de correction sur
// ce chantier (bandeau de phase contre splash de tour).
const ZONES = {
  area_schemes_main: [], main_schemes_deck: [], area_schemes_side: [],
  additional_decks: [], additional_discard_piles: [], area_villain: [],
  villain_deck: [], encounter_deck: [], encounter_discard_pile: [],
  area_boost: [], area_environment: [], area_evidence: [], area_rule: [],
  area_processing: [], area_revealing: [], area_resources: [],
  area_removed: [], area_insert: [], area_set_aside: [],
  victory_display: [], area_status_cards: [], players: [],
  active_card_ids: [],
}

/** Le monde a une phase donnee du round 2, le seul reglage qui compte ici. */
const mondeEnPhase = (phase: string): World => ({
  render_id: 1, round_id: 2, phase, prompt: '', event_name: '', ...ZONES,
})

/** Une phase du mechant qui a coute quelque chose, et rien d'autre. */
const phaseQuiACoute = (): EntreeHistorique[] =>
  commeDansLHistorique(
    entree({
      phase: 'Main Scheme Place Threat',
      type: 'threat',
      valeur: 1,
      restant: 1,
      plafond: 6,
      cibleId: 7,
    })
  )

describe('recap retenu tant qu un autre panneau occupe l ecran', () => {
  it('s affiche a la sortie de la phase du mechant', () => {
    const entrees = phaseQuiACoute()
    const { rerender } = render(
      <RecapPhaseMechant entrees={entrees} monde={mondeEnPhase('Enemy Activation')} actif />
    )
    rerender(<RecapPhaseMechant entrees={entrees} monde={mondeEnPhase('Player 1 Turn')} actif />)
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('ne s affiche pas tant qu il est suspendu', () => {
    const entrees = phaseQuiACoute()
    const { rerender } = render(
      <RecapPhaseMechant entrees={entrees} monde={mondeEnPhase('Enemy Activation')} actif suspendu />
    )
    rerender(
      <RecapPhaseMechant entrees={entrees} monde={mondeEnPhase('Player 1 Turn')} actif suspendu />
    )
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('ne PERD pas le bilan retenu : il parait des que la place se libere', () => {
    // Le point qui compte. La sortie de la phase du mechant est un instant qui
    // ne repasse pas : couper le recap a ce moment-la reviendrait a ne jamais
    // l'afficher. Il attend, il ne disparait pas.
    const entrees = phaseQuiACoute()
    const { rerender } = render(
      <RecapPhaseMechant entrees={entrees} monde={mondeEnPhase('Enemy Activation')} actif suspendu />
    )
    rerender(
      <RecapPhaseMechant entrees={entrees} monde={mondeEnPhase('Player 1 Turn')} actif suspendu />
    )
    expect(screen.queryByRole('dialog')).toBeNull()

    rerender(<RecapPhaseMechant entrees={entrees} monde={mondeEnPhase('Player 1 Turn')} actif />)
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })
})

// UNE SEULE SOURCE : les faits du moteur, avec un repli par genre.
//
// Le récap lisait les activations dans les faits et déduisait tout le reste
// (menace, distribution, révélations) du journal local, reconstruit par
// comparaison de photos et perdu au premier rechargement de page. Deux sources
// pour une seule phase, deux durées de vie (constat F6 de l'audit du
// 06/09/2026). Il lit désormais comme le cartouche du déroulé.
describe('bilanDeLaPhase — les quatre points viennent des faits', () => {
  const faitsDeLaPhase: FaitMechant[] = [
    {
      genre: 'menace',
      round_id: 2,
      cible: 'Underground Distribution',
      cible_id: 7,
      montant: 2,
      restant: 3,
      plafond: 6,
    },
    {
      genre: 'attaque',
      round_id: 2,
      auteur: 'Klaw',
      auteur_id: 3,
      cible: 'Black Panther',
      cible_id: 9,
      base: 3,
      boost: 0,
      defense: 0,
      inflige: 3,
      subi: 3,
      restant: 8,
      boosts: [],
    },
    { genre: 'distribution', round_id: 2, joueur: 0, joueur_nom: 'Colossus' },
    {
      genre: 'revelation',
      round_id: 2,
      joueur: 0,
      joueur_nom: 'Colossus',
      carte: 'Gang-Up',
      carte_id: 44,
    },
  ]

  it('construit les quatre étapes SANS aucune entrée de journal', () => {
    // Le cas du rechargement de page en pleine phase : le journal local est
    // vide, les faits, eux, voyagent avec le monde.
    const bilan = bilanDeLaPhase([], 2, noms, faitsDeLaPhase)
    expect(bilan?.etapes.map((e) => e.numero)).toEqual([1, 2, 3, 4])
    const titres = bilan?.etapes.flatMap((e) => e.lignes.map((l) => l.titre))
    expect(titres).toEqual([
      'Carte#7',
      'Klaw attaque Black Panther',
      'Carte rencontre distribuée',
      'Gang-Up',
    ])
  })

  it('donne à la menace le montant, le restant et le seuil du FAIT', () => {
    const bilan = bilanDeLaPhase([], 2, noms, faitsDeLaPhase)
    const menace = bilan?.etapes[0].lignes[0]
    expect(menace?.genre).toBe('menace')
    expect(menace?.valeur).toBe(2)
    expect(menace?.restant).toBe(3)
    expect(menace?.plafond).toBe(6)
    expect(bilan?.etapes[0].menace).toBe(2)
  })

  it('nomme le héros qui reçoit et celui qui révèle', () => {
    const bilan = bilanDeLaPhase([], 2, noms, faitsDeLaPhase)
    expect(bilan?.etapes[2].lignes[0].heros).toBe('Colossus')
    expect(bilan?.etapes[3].lignes[0].heros).toBe('Colossus')
  })

  it('REPLI par genre : sans fait de menace, la menace se relit dans le journal', () => {
    // Un moteur pas encore à jour, ou une sauvegarde plus ancienne, n'inscrit
    // que les activations. Le reste doit rester lisible, sans jamais compter
    // deux fois ce que les deux sources connaissent.
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({
          phase: 'Main Scheme Place Threat',
          type: 'threat',
          valeur: 1,
          restant: 1,
          plafond: 6,
          cibleId: 7,
        })
      ),
      2,
      noms,
      [faitsDeLaPhase[1]]
    )
    expect(bilan?.etapes[0].lignes).toHaveLength(1)
    expect(bilan?.etapes[0].lignes[0].valeur).toBe(1)
  })

  it('ne compte pas DEUX FOIS la menace que les deux sources connaissent', () => {
    const bilan = bilanDeLaPhase(
      commeDansLHistorique(
        entree({
          phase: 'Main Scheme Place Threat',
          type: 'threat',
          valeur: 2,
          restant: 3,
          plafond: 6,
          cibleId: 7,
        })
      ),
      2,
      noms,
      faitsDeLaPhase
    )
    expect(bilan?.etapes[0].lignes).toHaveLength(1)
    expect(bilan?.etapes[0].menace).toBe(2)
  })

  it('ignore les faits d un AUTRE round', () => {
    const bilan = bilanDeLaPhase(
      [],
      3,
      noms,
      faitsDeLaPhase.map((f) => ({ ...f }))
    )
    expect(bilan).toBeUndefined()
  })

  it('garde un fait SANS round_id, quel que soit le round demandé', () => {
    const sansRound = faitsDeLaPhase.map(({ round_id: _round, ...reste }) => reste as FaitMechant)
    expect(bilanDeLaPhase([], 9, noms, sansRound)?.etapes).toHaveLength(4)
  })

  it('n inscrit jamais une activation seulement ANNONCÉE', () => {
    const bilan = bilanDeLaPhase([], 2, noms, [
      {
        genre: 'attaque',
        etat: 'annonce',
        round_id: 2,
        auteur: 'Klaw',
        auteur_id: 3,
        cible: 'Black Panther',
        cible_id: 9,
        base: 3,
      },
    ])
    expect(bilan).toBeUndefined()
  })
})

describe('le recap suit la definition unique de la phase du mechant', () => {
  it('parait a la sortie annoncee par la PROP, pas par sa propre photo du monde', () => {
    // Le monde ne change pas de phase ici : seule la prop bascule. C'est elle
    // qui fait foi, et elle vient de `PHASES_DU_MECHANT` (moteur.ts).
    const entrees = phaseQuiACoute()
    const monde = mondeEnPhase('Enemy Activation')
    const { rerender } = render(
      <RecapPhaseMechant entrees={entrees} monde={monde} actif phaseMechantEnCours />
    )
    expect(screen.queryByRole('dialog')).toBeNull()
    rerender(
      <RecapPhaseMechant entrees={entrees} monde={monde} actif phaseMechantEnCours={false} />
    )
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })

  it('fait son bilan sur le round de la PHASE, meme si le round a deja tourne', () => {
    // Le moteur quitte la phase du mechant et incremente le round dans la meme
    // foulee : lire `monde.round_id` a la sortie rend parfois le round suivant,
    // et le bilan ne trouverait alors ni entree ni fait.
    const entrees = phaseQuiACoute()
    const { rerender } = render(
      <RecapPhaseMechant
        entrees={entrees}
        monde={mondeEnPhase('Enemy Activation')}
        actif
        phaseMechantEnCours
      />
    )
    const roundSuivant: World = { ...mondeEnPhase('Player Turn'), round_id: 3 }
    rerender(
      <RecapPhaseMechant
        entrees={entrees}
        monde={roundSuivant}
        actif
        phaseMechantEnCours={false}
      />
    )
    expect(screen.getByRole('dialog')).toBeInTheDocument()
  })
})
