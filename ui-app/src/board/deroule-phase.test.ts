// Le decoupage de la phase du mechant en ETAPES a valider une par une.
//
// La source n'est pas une relecture du monde : le moteur envoie deja ses
// activations resolues (`FaitMechant`), avec la composition du coup (base,
// boost, defense) qu'aucune deduction ne saurait reconstituer. Le journal
// complete pour ce que les faits ne couvrent pas.
import { describe, expect, it } from 'vitest'
import {
  arreterSurDefaite,
  avecBilan,
  etapesDeroule,
  lignesBilan,
  rangDansLeTemps,
  type EtapeDeroule,
} from './deroule-phase'
import type {
  FaitActivationAnnonce,
  FaitActivationResolue,
  FaitDistribution,
  FaitEntree,
  FaitMechant,
  FaitMenace,
  FaitRevelation,
  FaitStatut,
} from './world'
import type { EntreeHistorique } from './HistoriquePartie'

const attaque = (extra: Partial<FaitActivationResolue> = {}): FaitActivationResolue => ({
  genre: 'attaque',
  phase: 'Enemy Activation',
  auteur: 'Ultron',
  auteur_id: 50,
  cible: 'Shuri',
  cible_id: 12,
  base: 3,
  boost: 2,
  defense: 0,
  inflige: 5,
  subi: 5,
  restant: 7,
  boosts: [],
  ...extra,
})

const entree = (extra: Partial<EntreeHistorique> = {}): EntreeHistorique =>
  ({
    cle: 'k1',
    type: 'threat',
    renderId: 1,
    round: 1,
    phase: 'Main Scheme Place Threat',
    titre: 'Menace posee',
    valeur: 1,
    nomCarte: 'L’Effraction !',
    restant: 5,
    plafond: 8,
    ...extra,
  }) as EntreeHistorique

// Aucune de ces cartes n'est le vilain : les tests generiques (qui ne
// s'interessent pas a la distinction mechant/sbires) passent un ensemble vide
// et retrouvent leurs etapes sous « sbires », le cas le plus frequent.
const AUCUN_MECHANT = new Set<number>()

describe('etapesDeroule', () => {
  it('fait une etape par activation du moteur', () => {
    const etapes = etapesDeroule(
      [attaque(), attaque({ auteur: 'Drone', auteur_id: 60 })],
      [],
      1,
      AUCUN_MECHANT
    )
    const activations = etapes.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')
    expect(activations).toHaveLength(2)
  })

  it('met la carte qui agit en avant et retient sa cible', () => {
    const [etape] = etapesDeroule([attaque()], [], 1, AUCUN_MECHANT).filter(
      (e) => e.temps === 'mechant' || e.temps === 'sbires'
    )
    expect(etape.carteId).toBe(50)
    expect(etape.cibleId).toBe(12)
  })

  it('porte les boosts de l activation, dans l ordre', () => {
    const etapes = etapesDeroule(
      [attaque({ boosts: [{ nom: 'Boost A', id: 91, apport: 1 }, { nom: 'Boost B', id: 92, apport: 1 }] })],
      [],
      1,
      AUCUN_MECHANT
    )
    const [etape] = etapes.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')
    expect(etape.boosts.map((b) => b.nom)).toEqual(['Boost A', 'Boost B'])
    expect(etape.boosts.map((b) => b.cle)).toEqual(['boost:0:91', 'boost:1:92'])
  })

  it('range une activation declenchee par une carte revelee sous la revelation', () => {
    // Un vilain peut frapper une seconde fois hors de l'etape des activations :
    // le fait porte sa propre phase, on la suit plutot que de tout ranger sous
    // « mechant » ou « sbires ».
    const etapes = etapesDeroule([attaque({ phase: 'Reveal Encounter Cards' })], [], 1, new Set([50]))
    expect(etapes.filter((e) => e.temps === 'revelation')).toHaveLength(1)
    expect(etapes.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')).toHaveLength(0)
  })

  it('fait une etape de menace a partir du journal', () => {
    const etapes = etapesDeroule([], [entree()], 1, AUCUN_MECHANT)
    expect(etapes.filter((e) => e.temps === 'menace')).toHaveLength(1)
  })

  it('fait une etape PAR manigance touchee par la menace', () => {
    // Une seule etape a deux lignes disait deux fois la meme chose : le titre
    // generique, puis le detail juste en dessous. Une etape par manigance dit
    // chaque fait une fois, avec son propre compteur.
    // Le journal empile la PLUS RECENTE en tete (« Le Braquage » ici) : les
    // etapes doivent ressortir dans l'ordre ou les menaces ont ete posees.
    const etapes = etapesDeroule([], [
      entree({ cle: 'm2', nomCarte: 'Le Braquage', valeur: 1, restant: 3, plafond: 6 }),
      entree({ cle: 'm1', nomCarte: 'L’Effraction !', valeur: 2, restant: 5, plafond: 8 }),
    ], 1, AUCUN_MECHANT)
    const menaces = etapes.filter((e) => e.temps === 'menace')
    expect(menaces).toHaveLength(2)
    expect(menaces.map((e) => e.cibleNom)).toEqual(['L’Effraction !', 'Le Braquage'])
    expect(menaces.map((e) => e.montant)).toEqual([2, 1])
  })

  it('reprend le compteur de la manigance sur l entree du journal', () => {
    const [etape] = etapesDeroule([], [entree()], 1, AUCUN_MECHANT)
    expect(etape.restant).toBe(5)
    expect(etape.plafond).toBe(8)
  })

  it('designe la manigance visee comme cible de l etape de menace', () => {
    // Sans cible, l'etape de menace etait le seul temps de la phase sans mise
    // en scene : la manigance dont on parlait restait noyee dans la table.
    // L'identifiant vient de la MEME entree que le compteur affiche a cote.
    const [etape] = etapesDeroule([], [entree({ cibleId: 77 })], 1, AUCUN_MECHANT)
    expect(etape.cibleId).toBe(77)
    // Pas d'auteur : la menace est une regle du jeu, personne ne l'inflige.
    expect(etape.carteId).toBeUndefined()
  })

  it('ne met pas en phrase un RETRAIT de menace', () => {
    // `valeur` est la variation SIGNEE du compteur : « gagne -1 menaces »
    // n'aurait aucun sens. Sans montant, le titre se replie sur le generique.
    const [etape] = etapesDeroule([], [entree({ valeur: -1 })], 1, AUCUN_MECHANT)
    expect(etape.montant).toBeUndefined()
  })

  it('retient les degats REELLEMENT subis, pas ceux portes', () => {
    // `inflige` est ce qui a ete porte defense deduite, `subi` ce que la cible
    // a encaisse : une reduction de degats separe les deux, et le joueur lit
    // ce qui s'est passe.
    const [etape] = etapesDeroule([attaque({ inflige: 5, subi: 4, restant: 3 })], [], 1, AUCUN_MECHANT)
    expect(etape.montant).toBe(4)
    expect(etape.restant).toBe(3)
  })

  it('ne porte aucun compteur quand le fait n en donne pas', () => {
    const [etape] = etapesDeroule([attaque({ restant: null })], [], 1, AUCUN_MECHANT)
    expect(etape.restant).toBeUndefined()
  })

  it('donne une cle stable et unique a chaque etape', () => {
    const etapes = etapesDeroule([attaque(), attaque({ auteur_id: 60 })], [entree()], 1, AUCUN_MECHANT)
    const cles = etapes.map((e) => e.cle)
    expect(new Set(cles).size).toBe(cles.length)
  })

  it('range sous mechant un fait dont l auteur est dans l ensemble mechant', () => {
    const etapes = etapesDeroule([attaque({ auteur_id: 50 })], [], 1, new Set([50]))
    expect(etapes.map((e) => e.temps)).toEqual(['mechant'])
  })

  it('range sous sbires un fait dont l auteur n est pas dans l ensemble mechant', () => {
    const etapes = etapesDeroule([attaque({ auteur_id: 60 })], [], 1, new Set([50]))
    expect(etapes.map((e) => e.temps)).toEqual(['sbires'])
  })

  it('range sous sbires un fait dont l auteur est introuvable', () => {
    // Une carte deja partie de la table (minion tue par sa propre cible) n'a
    // pas d'entree dans l'ensemble mechant, quel qu'il soit : mieux vaut la
    // ranger sous le cas le plus frequent (sbires) qu'inventer un troisieme
    // etat.
    const etapes = etapesDeroule([attaque({ auteur_id: 999 })], [], 1, new Set([50]))
    expect(etapes.map((e) => e.temps)).toEqual(['sbires'])
  })

  it('rend les etapes dans l ordre des cinq temps', () => {
    const etapes = etapesDeroule(
      [
        attaque({ auteur_id: 50 }),
        attaque({ auteur_id: 60 }),
        attaque({ phase: 'Reveal Encounter Cards', auteur_id: 60 }),
      ],
      [entree()],
      1,
      new Set([50])
    )
    expect(etapes.map((e) => e.temps)).toEqual(['menace', 'mechant', 'sbires', 'revelation'])
  })

  it('ne rend aucune etape quand la phase n a rien produit', () => {
    expect(etapesDeroule([], [], 1, AUCUN_MECHANT)).toEqual([])
  })

  it('fait une etape par carte revelee', () => {
    const etapes = etapesDeroule([], [
      entree({
        cle: 'c1',
        type: 'card',
        phase: 'Reveal Encounter Cards',
        titre: 'Icy Grip revelee',
        cibleId: 77,
      }),
    ], 1, AUCUN_MECHANT)
    const revelations = etapes.filter((e) => e.temps === 'revelation')
    expect(revelations).toHaveLength(1)
    expect(revelations[0].carteId).toBe(77)
  })

  // Regle officielle : chaque joueur revele et resout sa carte dans l'ordre
  // du tour, en commencant par le premier joueur. Ce module ne voit pas le
  // monde (voir l'en-tete du fichier) : c'est l'appelant qui lui donne le
  // siege du premier joueur et le nom de chaque heros (voir le rapport de la
  // tache pour le champ retenu, `k_first_player_token`).
  describe('l ordre du tour des revelations', () => {
    // Le moteur revele une carte des qu'elle QUITTE le paquet de rencontre,
    // ce qui a lieu a l'etape de DISTRIBUTION ('Deal Encounter Cards') : voir
    // le rapport de la tache. Sans cet accueil, aucune carte revelee ne
    // remontait jamais en partie reelle.
    it('accueille aussi les cartes marquees sous la distribution', () => {
      const etapes = etapesDeroule(
        [],
        [entree({ cle: 'c1', type: 'card', phase: 'Deal Encounter Cards', nomCarte: 'Sonic Boom', cibleId: 77 })],
        1,
        AUCUN_MECHANT
      )
      const revelations = etapes.filter((e) => e.temps === 'revelation')
      expect(revelations).toHaveLength(1)
      expect(revelations[0].cibleNom).toBe('Sonic Boom')
    })

    it('range trois revelations arrivees dans le desordre selon l ordre du tour', () => {
      // Le journal les livre dans un ordre qui n'est ni l'ordre d'arrivee ni
      // l'ordre chronologique (B, C, A une fois inverse) : avec le siege 2
      // pour premier joueur, l'ordre attendu est C (siege 2), A (siege 0),
      // B (siege 1).
      const etapes = etapesDeroule(
        [],
        [
          entree({ cle: 'a', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 }),
          entree({ cle: 'c', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte C', joueur: 2 }),
          entree({ cle: 'b', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte B', joueur: 1 }),
        ],
        1,
        AUCUN_MECHANT,
        undefined,
        2,
        ['Joueur0', 'Joueur1', 'Joueur2']
      )
      const revelations = etapes.filter((e) => e.temps === 'revelation')
      expect(revelations.map((e) => e.cibleNom)).toEqual(['Carte C', 'Carte A', 'Carte B'])
    })

    it('le premier joueur passe en premier, meme s il n est pas le joueur 1', () => {
      const etapes = etapesDeroule(
        [],
        [
          entree({ cle: 'a', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 }),
          entree({ cle: 'b', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte B', joueur: 1 }),
        ],
        1,
        AUCUN_MECHANT,
        undefined,
        1,
        ['Joueur0', 'Joueur1']
      )
      const revelations = etapes.filter((e) => e.temps === 'revelation')
      expect(revelations.map((e) => e.cibleNom)).toEqual(['Carte B', 'Carte A'])
    })

    it('en solo, l ordre ne bouge pas et aucun compteur n apparait', () => {
      const etapes = etapesDeroule(
        [],
        [entree({ cle: 'a', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 })],
        1,
        AUCUN_MECHANT,
        undefined,
        0,
        ['★Colossus']
      )
      const revelations = etapes.filter((e) => e.temps === 'revelation')
      expect(revelations).toHaveLength(1)
      // Une seule etape dans ce temps : aucun compteur « 1 sur 1 ».
      expect(rangDansLeTemps(etapes, etapes.indexOf(revelations[0]))).toBeUndefined()
    })

    it('nomme le heros qui revele, nettoye de son prefixe decoratif', () => {
      const etapes = etapesDeroule(
        [],
        [entree({ cle: 'a', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Bombe à retardement', joueur: 0 })],
        1,
        AUCUN_MECHANT,
        undefined,
        0,
        ['★Colossus']
      )
      const [revelation] = etapes.filter((e) => e.temps === 'revelation')
      expect(revelation.auteurNom).toBe('Colossus')
      expect(revelation.cibleNom).toBe('Bombe à retardement')
    })

    it('garde l ordre du journal sans premier joueur connu', () => {
      // Ancien moteur sans jeton, ou source muette sur l'ordre : mieux vaut
      // l'ordre du journal qu'un ordre invente.
      const etapes = etapesDeroule(
        [],
        [
          // Le plus recent en tete, comme le vrai journal : b est arrivee
          // apres a.
          entree({ cle: 'b', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte B', joueur: 1 }),
          entree({ cle: 'a', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 }),
        ],
        1,
        AUCUN_MECHANT
      )
      const revelations = etapes.filter((e) => e.temps === 'revelation')
      expect(revelations.map((e) => e.cibleNom)).toEqual(['Carte A', 'Carte B'])
    })
  })

  it('ne fait pas d etape d une narration deja mise en phrase ailleurs', () => {
    // Le type `text` est la narration interne du moteur : elle a sa place
    // dans le journal, pas dans un deroule qu'on lit etape par etape.
    const etapes = etapesDeroule([], [
      entree({ cle: 'c3', type: 'text', phase: 'Reveal Encounter Cards', titre: 'Main scheme phase start' }),
    ], 1, AUCUN_MECHANT)
    expect(etapes).toEqual([])
  })

  it('ne produit aucune etape pour une entree de texte brut du moteur', () => {
    // La narration technique du moteur (defausses, fins d'activation,
    // « DiscardPile<3> »), en anglais et illisible, noyait les etapes utiles
    // du cartouche (8 sur 12 en partie reelle). Elle quitte le cartouche mais
    // reste entiere dans le journal et le Log, qui la rendent sur `brut` sans
    // passer par `etapesDeroule`.
    const etapes = etapesDeroule([], [
      entree({
        cle: 'c2',
        type: 'text',
        phase: 'Reveal Encounter Cards',
        titre: '',
        brut: '[(50,01113) Klaw] would deal 2 damage',
      }),
    ], 1, AUCUN_MECHANT)
    expect(etapes).toEqual([])
  })

  describe('le rang dans le temps', () => {
    // Le joueur doit savoir combien d'etapes ce temps compte encore, sans
    // etre encombre par un « 1 sur 1 » qui n'apprend rien.
    it('compte les etapes du temps courant', () => {
      const etapes = etapesDeroule(
        [attaque({ auteur_id: 60 }), attaque({ auteur: 'Drone', auteur_id: 61 })],
        [],
        1,
        new Set([50])
      )
      expect(etapes.map((e) => e.temps)).toEqual(['sbires', 'sbires'])
      expect(rangDansLeTemps(etapes, 0)).toEqual({ rang: 1, total: 2 })
      expect(rangDansLeTemps(etapes, 1)).toEqual({ rang: 2, total: 2 })
    })

    it('ne compte rien quand le temps n a qu une etape', () => {
      const etapes = etapesDeroule([attaque({ auteur_id: 60 })], [], 1, new Set([50]))
      expect(rangDansLeTemps(etapes, 0)).toBeUndefined()
    })

    it('compte dans le temps de l etape, pas dans toute la phase', () => {
      const etapes = etapesDeroule(
        [attaque({ auteur_id: 50 }), attaque({ auteur_id: 60 }), attaque({ auteur_id: 61 })],
        [],
        1,
        new Set([50])
      )
      expect(etapes.map((e) => e.temps)).toEqual(['mechant', 'sbires', 'sbires'])
      // L'unique etape du temps « mechant » n'affiche rien, les deux du temps
      // « sbires » se comptent entre elles.
      expect(rangDansLeTemps(etapes, 0)).toBeUndefined()
      expect(rangDansLeTemps(etapes, 1)).toEqual({ rang: 1, total: 2 })
      expect(rangDansLeTemps(etapes, 2)).toEqual({ rang: 2, total: 2 })
    })

    it('ne compte rien hors des etapes connues', () => {
      expect(rangDansLeTemps([], 0)).toBeUndefined()
    })
  })

  describe('le round', () => {
    // L'historique accumule TOUTE la partie, pas seulement la phase en cours.
    // Sans filtre, la phase du round 4 ferait revoir les cartes des rounds
    // precedents. Et il empile la plus recente EN TETE : sans inversion, ces
    // vieilles cartes s'afficheraient en plus a l'envers.
    const journalTroisRounds: EntreeHistorique[] = [
      // Le plus recent d'abord, comme le fait vraiment historique.entrees.
      entree({ cle: 'r3-b', round: 3, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R3-B', nomCarte: 'Carte R3-B', cibleId: 3 }),
      entree({ cle: 'r3-a', round: 3, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R3-A', nomCarte: 'Carte R3-A', cibleId: 2 }),
      entree({ cle: 'r2', round: 2, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R2', nomCarte: 'Carte R2', cibleId: 1 }),
      entree({ cle: 'r1', round: 1, type: 'threat', phase: 'Main Scheme Place Threat', titre: 'Menace R1' }),
    ]

    it('ne rend que les etapes du round demande', () => {
      // `titre` porte desormais la cle 'revelation' (voir plus haut) : c'est
      // `cibleNom`, le nom NU de la carte, qui distingue les etapes entre
      // elles ici.
      const etapes = etapesDeroule([], journalTroisRounds, 3, AUCUN_MECHANT)
      expect(etapes.map((e) => e.cibleNom)).toEqual(['Carte R3-A', 'Carte R3-B'])
    })

    it('rend ces etapes dans l ordre chronologique, pas l ordre du journal', () => {
      // Le journal les stocke la plus recente en tete (r3-b avant r3-a) : le
      // deroule doit les montrer dans l'ordre ou elles ont eu lieu.
      const etapes = etapesDeroule([], journalTroisRounds, 3, AUCUN_MECHANT)
      expect(etapes.map((e) => e.cle)).toEqual(['carte:r3-a', 'carte:r3-b'])
    })

    it('ne melange pas un autre round dans le decompte', () => {
      const etapes1 = etapesDeroule([], journalTroisRounds, 1, AUCUN_MECHANT)
      expect(etapes1.map((e) => e.titre)).toEqual(['menace'])
      const etapes2 = etapesDeroule([], journalTroisRounds, 2, AUCUN_MECHANT)
      expect(etapes2.map((e) => e.cibleNom)).toEqual(['Carte R2'])
    })

    // Defaut 2 (voir brief) : les FAITS ne portaient aucun round, seul le
    // journal etait filtre. Le cartouche rouvrait donc au round suivant, en
    // plein tour du joueur, sur une manigance deja vaincue.
    it('ne rend que les faits du round demande', () => {
      const faitsDeuxRounds = [
        attaque({ round_id: 1, auteur: 'Ultron', auteur_id: 50 }),
        attaque({ round_id: 2, auteur: 'Drone', auteur_id: 60 }),
      ]
      const etapes = etapesDeroule(faitsDeuxRounds, [], 2, AUCUN_MECHANT)
      const activations = etapes.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')
      expect(activations).toHaveLength(1)
      expect(activations[0]?.auteurNom).toBe('Drone')
    })

    // Un fait sans round_id vient d'un moteur pas encore mis a jour, ou d'une
    // sauvegarde rechargee anterieure a ce champ : mieux vaut le montrer en
    // trop (une etape de plus) que de rendre le deroule muet en le jetant a
    // tort.
    it('garde un fait SANS round_id, quel que soit le round demande', () => {
      const faitSansRound = attaque({ auteur: 'Ultron', auteur_id: 50 })
      expect(faitSansRound.round_id).toBeUndefined()
      const etapes1 = etapesDeroule([faitSansRound], [], 1, AUCUN_MECHANT)
      const etapes5 = etapesDeroule([faitSansRound], [], 5, AUCUN_MECHANT)
      expect(etapes1.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')).toHaveLength(1)
      expect(etapes5.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')).toHaveLength(1)
    })
  })
})

// ---------------------------------------------------------------------- A2 --
// Les cinq temps viennent des FAITS DU MOTEUR, et d'eux seuls.
//
// Avant la tache A2, les activations venaient des faits (persistants, portes
// par le monde) mais la menace et les cartes revelees venaient du journal
// local, reconstruit dans le navigateur en comparant deux photos du monde. Un
// F5 en pleine phase les perdait definitivement (constat F4 de l'audit), et le
// temps DISTRIBUTION n'avait aucune source du tout (constat M3).
describe('les cinq temps depuis les faits du moteur', () => {
  const faitMenace = (extra: Partial<FaitMenace> = {}): FaitMenace => ({
    genre: 'menace',
    phase: 'Main Scheme Place Threat',
    round_id: 1,
    cible: 'L’Effraction !',
    cible_id: 20,
    montant: 2,
    restant: 5,
    plafond: 8,
    ...extra,
  })

  const faitDistribution = (extra: Partial<FaitDistribution> = {}): FaitDistribution => ({
    genre: 'distribution',
    phase: 'Deal Encounter Cards',
    round_id: 1,
    joueur: 0,
    joueur_nom: '★Colossus',
    ...extra,
  })

  const faitRevelation = (extra: Partial<FaitRevelation> = {}): FaitRevelation => ({
    genre: 'revelation',
    phase: 'Reveal Encounter Cards',
    round_id: 1,
    joueur: 0,
    joueur_nom: '★Colossus',
    carte: 'Bombe à retardement',
    carte_id: 88,
    ...extra,
  })

  /** Une phase complete, telle que le moteur la publie desormais. */
  const phaseComplete = (): FaitMechant[] => [
    faitMenace(),
    attaque({ round_id: 1, auteur: 'Klaw', auteur_id: 50, cible: 'Colossus', cible_id: 12 }),
    attaque({ round_id: 1, auteur: 'Drone', auteur_id: 60, cible: 'Colossus', cible_id: 12 }),
    faitDistribution(),
    faitRevelation(),
  ]

  it('produit les cinq temps SANS aucune entree de journal', () => {
    const etapes = etapesDeroule(phaseComplete(), [], 1, new Set([50]))
    expect(etapes.map((e) => e.temps)).toEqual([
      'menace',
      'mechant',
      'sbires',
      'distribution',
      'revelation',
    ])
  })

  it('rend le MEME cartouche apres un rechargement, journal vide', () => {
    // Le rechargement de page, simule : le monde revient avec ses faits (ils
    // voyagent avec lui), le journal local repart de zero. C'est exactement
    // ce que F4 decrivait, et le cartouche ne doit plus rien y perdre.
    const avant = etapesDeroule(phaseComplete(), [entree()], 1, new Set([50]))
    const apres = etapesDeroule(phaseComplete(), [], 1, new Set([50]))
    expect(apres).toEqual(avant)
  })

  it('lit la menace sur le fait : manigance, montant, compteur et seuil', () => {
    const [etape] = etapesDeroule([faitMenace()], [], 1, AUCUN_MECHANT)
    expect(etape.temps).toBe('menace')
    expect(etape.cibleNom).toBe('L’Effraction !')
    expect(etape.cibleId).toBe(20)
    expect(etape.montant).toBe(2)
    expect(etape.restant).toBe(5)
    expect(etape.plafond).toBe(8)
    // La menace est une REGLE du jeu : personne ne l'inflige, donc pas d'auteur
    // a mettre en avant.
    expect(etape.carteId).toBeUndefined()
  })

  it('fait une etape de DISTRIBUTION par joueur, nommee par son heros', () => {
    // Le temps qui n'avait jamais d'etape (M3) : la chronologie affichait
    // « DISTRIBUTION (Aucun) » barre a presque toutes les phases.
    const etapes = etapesDeroule(
      [faitDistribution(), faitDistribution({ joueur: 1, joueur_nom: '★Spider-Man' })],
      [],
      1,
      AUCUN_MECHANT
    )
    const distributions = etapes.filter((e) => e.temps === 'distribution')
    expect(distributions).toHaveLength(2)
    // Prefixe decoratif retire, comme partout ailleurs sur le plateau.
    expect(distributions.map((e) => e.auteurNom)).toEqual(['Colossus', 'Spider-Man'])
    // Une carte chacun.
    expect(distributions.map((e) => e.montant)).toEqual([1, 1])
    // La carte est FACE CACHEE : rien ne la nomme, et rien ne la met en avant
    // sur la table.
    expect(distributions[0].cibleNom).toBeUndefined()
    expect(distributions[0].carteId).toBeUndefined()
    expect(distributions[0].cibleId).toBeUndefined()
  })

  it('groupe en UNE etape les deux cartes d un meme joueur (Heroique)', () => {
    const etapes = etapesDeroule(
      [
        faitDistribution(),
        faitDistribution({ joueur: 1, joueur_nom: '★Spider-Man' }),
        faitDistribution(),
        faitDistribution({ joueur: 1, joueur_nom: '★Spider-Man' }),
      ],
      [],
      1,
      AUCUN_MECHANT
    )
    const distributions = etapes.filter((e) => e.temps === 'distribution')
    expect(distributions).toHaveLength(2)
    expect(distributions.map((e) => e.auteurNom)).toEqual(['Colossus', 'Spider-Man'])
    expect(distributions.map((e) => e.montant)).toEqual([2, 2])
  })

  it('ne fond PAS deux distributions dont le siege est inconnu', () => {
    // Deux cartes anonymes ne sont pas forcement pour le meme joueur : les
    // regrouper inventerait un fait que personne n'a enregistre.
    const etapes = etapesDeroule(
      [
        faitDistribution({ joueur: null, joueur_nom: null }),
        faitDistribution({ joueur: null, joueur_nom: null }),
      ],
      [],
      1,
      AUCUN_MECHANT
    )
    const distributions = etapes.filter((e) => e.temps === 'distribution')
    expect(distributions).toHaveLength(2)
    expect(distributions.map((e) => e.montant)).toEqual([1, 1])
  })

  it('range les distributions groupees dans l ordre du tour', () => {
    const etapes = etapesDeroule(
      [
        faitDistribution({ joueur: 0, joueur_nom: 'Heros0' }),
        faitDistribution({ joueur: 1, joueur_nom: 'Heros1' }),
        faitDistribution({ joueur: 1, joueur_nom: 'Heros1' }),
      ],
      [],
      1,
      AUCUN_MECHANT,
      undefined,
      1,
      ['Heros0', 'Heros1']
    )
    const distributions = etapes.filter((e) => e.temps === 'distribution')
    expect(distributions.map((e) => e.auteurNom)).toEqual(['Heros1', 'Heros0'])
    expect(distributions.map((e) => e.montant)).toEqual([2, 1])
  })

  it('lit la revelation sur le fait : le heros, la carte et son identifiant', () => {
    const [etape] = etapesDeroule([faitRevelation()], [], 1, AUCUN_MECHANT)
    expect(etape.temps).toBe('revelation')
    expect(etape.auteurNom).toBe('Colossus')
    expect(etape.cibleNom).toBe('Bombe à retardement')
    expect(etape.carteId).toBe(88)
  })

  it('range les revelations dans l ordre du tour, comme les entrees du journal', () => {
    const etapes = etapesDeroule(
      [
        faitRevelation({ joueur: 0, joueur_nom: 'Heros0', carte: 'Carte A', carte_id: 1 }),
        faitRevelation({ joueur: 1, joueur_nom: 'Heros1', carte: 'Carte B', carte_id: 2 }),
      ],
      [],
      1,
      AUCUN_MECHANT,
      undefined,
      1,
      ['Heros0', 'Heros1']
    )
    const revelations = etapes.filter((e) => e.temps === 'revelation')
    expect(revelations.map((e) => e.cibleNom)).toEqual(['Carte B', 'Carte A'])
  })

  // IDENTITE DES ETAPES. La cle venait d'un rang dans une liste RETRIEE par
  // ordre du tour : un Deferlement (une revelation de plus pour un autre
  // joueur) reordonnait la liste, la cle de l'etape en cours de lecture
  // changeait, son minuteur d'avance repartait, et une etape qui s'inserait en
  // amont faisait reculer le joueur d'un cran (constat F3 de l'audit, et
  // Important 3 de la relecture d'A2).
  it('garde la cle d une revelation quand une autre s insere avant elle', () => {
    const deja = faitRevelation({ joueur: 1, joueur_nom: 'Heros1', carte: 'Carte B', carte_id: 2 })
    const tard = faitRevelation({ joueur: 0, joueur_nom: 'Heros0', carte: 'Carte A', carte_id: 1 })
    const noms = ['Heros0', 'Heros1']
    const avant = etapesDeroule([deja], [], 1, AUCUN_MECHANT, undefined, 0, noms)
    const apres = etapesDeroule([deja, tard], [], 1, AUCUN_MECHANT, undefined, 0, noms)
    // La revelation arrivee en dernier passe DEVANT (ordre du tour)...
    expect(apres.map((e) => e.cibleNom)).toEqual(['Carte A', 'Carte B'])
    // ... et pourtant celle que le joueur lisait garde sa cle.
    expect(apres[1].cle).toBe(avant[0].cle)
  })

  it('garde la cle d une distribution quand une autre s insere avant elle', () => {
    const deja = faitDistribution({ joueur: 1, joueur_nom: 'Heros1' })
    const tard = faitDistribution({ joueur: 0, joueur_nom: 'Heros0' })
    const noms = ['Heros0', 'Heros1']
    const avant = etapesDeroule([deja], [], 1, AUCUN_MECHANT, undefined, 0, noms)
    const apres = etapesDeroule([deja, tard], [], 1, AUCUN_MECHANT, undefined, 0, noms)
    expect(apres.map((e) => e.auteurNom)).toEqual(['Heros0', 'Heros1'])
    expect(apres[1].cle).toBe(avant[0].cle)
  })

  it('tire le rang de la cle des faits du monde, pas du tableau filtre', () => {
    // Un fait d'un AUTRE round precede l'activation : il est ecarte du round
    // demande, mais il occupe bel et bien le rang 0 de `faits_mechant`. La cle
    // de repli (moteur sans identifiant d'activation) doit le refleter, sans
    // quoi elle changerait au gre de ce que le filtre laisse passer.
    const [etape] = etapesDeroule(
      [faitMenace({ round_id: 0 }), attaque({ round_id: 1, auteur_id: 50 })],
      [],
      1,
      new Set([50])
    )
    expect(etape.cle).toBe('fait:1:50')
  })

  it('ne lit PAS le journal quand les faits couvrent le genre', () => {
    // Le doublon que la double source produisait : la meme menace vue une fois
    // par le moteur et une fois par la comparaison de photos.
    const etapes = etapesDeroule([faitMenace()], [entree()], 1, AUCUN_MECHANT)
    expect(etapes.filter((e) => e.temps === 'menace')).toHaveLength(1)
    expect(etapes[0].cibleNom).toBe('L’Effraction !')
  })

  it('ne lit PAS le journal pour les cartes quand un SEUL des deux genres est la', () => {
    // Une phase ou personne ne revele encore : le fait de distribution suffit a
    // dire que le moteur sait tenir ce journal, donc on ne repasse pas par la
    // reconstruction locale.
    const etapes = etapesDeroule(
      [faitDistribution()],
      [entree({ cle: 'c1', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Sonic Boom' })],
      1,
      AUCUN_MECHANT
    )
    expect(etapes.filter((e) => e.temps === 'revelation')).toHaveLength(0)
    expect(etapes.filter((e) => e.temps === 'distribution')).toHaveLength(1)
  })

  // ⚠ REPLI TEMPORAIRE. Un moteur pas encore mis a jour, ou une sauvegarde
  // plus ancienne, ne porte aucun de ces trois genres : le cartouche relit
  // alors le journal local, exactement comme avant. Ces deux cas disparaitront
  // avec le repli lui-meme.
  it('replie sur le journal quand AUCUN fait de menace n existe pour le round', () => {
    const etapes = etapesDeroule([attaque({ round_id: 1 })], [entree()], 1, AUCUN_MECHANT)
    const menaces = etapes.filter((e) => e.temps === 'menace')
    expect(menaces).toHaveLength(1)
    expect(menaces[0].cibleNom).toBe('L’Effraction !')
  })

  it('replie sur le journal quand AUCUN fait de carte n existe pour le round', () => {
    const etapes = etapesDeroule(
      [faitMenace()],
      [entree({ cle: 'c1', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Sonic Boom' })],
      1,
      AUCUN_MECHANT
    )
    const revelations = etapes.filter((e) => e.temps === 'revelation')
    expect(revelations).toHaveLength(1)
    expect(revelations[0].cibleNom).toBe('Sonic Boom')
  })

  it('ne replie pas sur les faits d un AUTRE round', () => {
    // Le repli se juge round par round : un fait de menace du round 1 ne doit
    // pas fermer le repli du round 2, qui n'en a pas encore.
    const etapes = etapesDeroule(
      [faitMenace({ round_id: 1 })],
      [entree({ round: 2 })],
      2,
      AUCUN_MECHANT
    )
    const menaces = etapes.filter((e) => e.temps === 'menace')
    expect(menaces).toHaveLength(1)
    expect(menaces[0].cibleNom).toBe('L’Effraction !')
    // Et c'est bien l'entree du journal du round 2, pas le fait du round 1.
    expect(menaces[0].restant).toBe(5)
    expect(menaces[0].cle.startsWith('menace:k1')).toBe(true)
  })
})

describe('le bilan de fin de phase', () => {
  // Le moment ou le joueur decide de son tour : ce que la phase vient de lui
  // couter, en deux lignes, sans remonter le journal.
  //
  // Les totaux se lisent sur les etapes, qui tiennent leurs nombres des faits
  // du moteur : jamais d'une comparaison entre deux photos du monde. Meme
  // arbitrage que RecapPhaseMechant, pour la meme raison.

  it('groupe en UNE ligne les coups portes sur la meme cible', () => {
    // LE piege du comptage : le vilain et deux sbires frappent tous Colossus.
    // Cela fait une ligne « Colossus a pris 6 degats », pas trois.
    const etapes = etapesDeroule(
      [
        attaque({ auteur: 'Ultron', auteur_id: 50, cible: 'Colossus', cible_id: 12, subi: 3, restant: 11 }),
        attaque({ auteur: 'Drone', auteur_id: 60, cible: 'Colossus', cible_id: 12, subi: 2, restant: 9 }),
        attaque({ auteur: 'Drone', auteur_id: 61, cible: 'Colossus', cible_id: 12, subi: 1, restant: 8 }),
      ],
      [],
      1,
      new Set([50])
    )
    const lignes = lignesBilan(etapes)
    expect(lignes).toHaveLength(1)
    expect(lignes[0].cibleNom).toBe('Colossus')
    expect(lignes[0].total).toBe(6)
    // Le compteur retenu est celui du DERNIER coup : c'est l'etat courant de
    // la cible, pas celui d'apres le premier coup.
    expect(lignes[0].restant).toBe(8)
  })

  it('fait une ligne par cible touchee', () => {
    const etapes = etapesDeroule(
      [
        attaque({ auteur_id: 60, cible: 'Colossus', cible_id: 12, subi: 3 }),
        attaque({ auteur_id: 61, cible: 'Thor', cible_id: 13, subi: 2 }),
      ],
      [],
      1,
      AUCUN_MECHANT
    )
    expect(lignesBilan(etapes).map((l) => [l.cibleNom, l.total])).toEqual([
      ['Colossus', 3],
      ['Thor', 2],
    ])
  })

  it('distingue les degats de la menace : une attaque et une menace font deux lignes', () => {
    const etapes = etapesDeroule(
      [attaque({ auteur_id: 60, cible: 'Colossus', cible_id: 12, subi: 3 })],
      [entree({ nomCarte: 'L’Effraction !', valeur: 3, restant: 6, plafond: 8 })],
      1,
      AUCUN_MECHANT
    )
    const lignes = lignesBilan(etapes)
    expect(lignes).toHaveLength(2)
    expect(lignes.map((l) => l.genre)).toEqual(['menaces', 'degats'])
    expect(lignes.find((l) => l.genre === 'menaces')).toMatchObject({
      cibleNom: 'L’Effraction !',
      total: 3,
      restant: 6,
      plafond: 8,
    })
  })

  it('additionne la menace posee et celle d une manigance sur la meme carte', () => {
    // Le point 1 vient du journal (qui donne un nom), la manigance d'un fait :
    // sans regroupement par nom, la meme manigance ressortirait deux fois.
    const etapes = etapesDeroule(
      [
        attaque({
          genre: 'manigance',
          auteur: 'Drone',
          auteur_id: 60,
          cible: 'L’Effraction !',
          cible_id: 77,
          subi: 2,
          restant: 7,
        }),
      ],
      [entree({ nomCarte: 'L’Effraction !', valeur: 1, restant: 5, plafond: 8 })],
      1,
      AUCUN_MECHANT
    )
    const lignes = lignesBilan(etapes)
    expect(lignes).toHaveLength(1)
    expect(lignes[0].total).toBe(3)
    // Le fait n'apporte pas de plafond : celui de l'entree de menace tient.
    expect(lignes[0]).toMatchObject({ restant: 7, plafond: 8 })
  })

  it('affiche les PV maximum quand l appelant les connait', () => {
    // Les PV maximum ne sont nulle part dans les faits du moteur : c'est
    // board.tsx qui les releve sur le monde et les passe ici, par nom.
    const etapes = etapesDeroule(
      [attaque({ auteur_id: 60, cible: 'Colossus', cible_id: 12, subi: 3, restant: 11 })],
      [],
      1,
      AUCUN_MECHANT
    )
    const lignes = lignesBilan(etapes, new Map([['Colossus', 14]]))
    expect(lignes[0]).toMatchObject({ restant: 11, plafond: 14 })
  })

  it('laisse les PV nus quand le maximum est inconnu', () => {
    // Un plafond invente serait pire qu'un chiffre nu : sans entree pour cette
    // cible, la ligne reste sans plafond.
    const etapes = etapesDeroule(
      [attaque({ auteur_id: 60, cible: 'Colossus', cible_id: 12, subi: 3, restant: 11 })],
      [],
      1,
      AUCUN_MECHANT
    )
    expect(lignesBilan(etapes, new Map([['Thor', 12]]))[0].plafond).toBeUndefined()
    expect(lignesBilan(etapes)[0].plafond).toBeUndefined()
  })

  it('n ecrase pas le seuil d une manigance avec un PV maximum homonyme', () => {
    // Le seuil d'une manigance vient de son entree de journal, et il date du
    // coup lui-meme : il fait foi.
    const etapes = etapesDeroule(
      [],
      [entree({ nomCarte: 'L’Effraction !', valeur: 3, restant: 6, plafond: 8 })],
      1,
      AUCUN_MECHANT
    )
    expect(lignesBilan(etapes, new Map([['L’Effraction !', 99]]))[0].plafond).toBe(8)
  })

  it('porte les PV maximum jusqu au bilan de fin de phase', () => {
    const etapes = etapesDeroule(
      [attaque({ auteur_id: 60, cible: 'Colossus', cible_id: 12, subi: 3, restant: 11 })],
      [],
      1,
      AUCUN_MECHANT
    )
    const bilan = avecBilan(etapes, new Map([['Colossus', 14]])).at(-1)
    expect(bilan?.bilan?.[0]).toMatchObject({ restant: 11, plafond: 14 })
  })

  it('ne compte pas une carte revelee, qui n encaisse rien', () => {
    const etapes = etapesDeroule(
      [],
      [
        entree({
          cle: 'c1',
          type: 'card',
          phase: 'Reveal Encounter Cards',
          titre: 'Icy Grip révélée',
          cibleId: 77,
        }),
      ],
      1,
      AUCUN_MECHANT
    )
    expect(etapes).toHaveLength(1)
    expect(lignesBilan(etapes)).toEqual([])
  })

  it('ne compte pas un coup sans montant, ni un retrait de menace', () => {
    const etapes = etapesDeroule(
      [attaque({ auteur_id: 60, subi: 0 })],
      [entree({ valeur: -1 })],
      1,
      AUCUN_MECHANT
    )
    expect(lignesBilan(etapes)).toEqual([])
  })

  describe('avecBilan', () => {
    it('met le bilan en DERNIER, quel que soit l ordre d arrivee des faits', () => {
      // Les faits arrivent ici a l'envers de l'ordre de la carte de reference :
      // une revelation, puis un sbire, puis le vilain. Le bilan reste dernier.
      const etapes = etapesDeroule(
        [
          attaque({ phase: 'Reveal Encounter Cards', auteur_id: 60 }),
          attaque({ auteur_id: 61 }),
          attaque({ auteur_id: 50 }),
        ],
        [entree()],
        1,
        new Set([50])
      )
      const avec = avecBilan(etapes)
      expect(avec.map((e) => e.temps)).toEqual([
        'menace',
        'mechant',
        'sbires',
        'revelation',
        'bilan',
      ])
      expect(avec[avec.length - 1].bilan).toBeDefined()
    })

    it('n ajoute rien a une liste vide : hors phase, il n y a pas de fin a annoncer', () => {
      expect(avecBilan([])).toEqual([])
    })

    it('donne un bilan VIDE, et non absent, a une phase qui n a rien coute', () => {
      // Une carte revelee sans effet chiffre : la phase a bien eu lieu, elle
      // n'a rien coute. Le bilan doit le dire, pas disparaitre.
      const etapes = etapesDeroule(
        [],
        [
          entree({
            cle: 'c1',
            type: 'card',
            phase: 'Reveal Encounter Cards',
            titre: 'Icy Grip révélée',
            cibleId: 77,
          }),
        ],
        1,
        AUCUN_MECHANT
      )
      const dernier = avecBilan(etapes).at(-1)
      expect(dernier?.temps).toBe('bilan')
      expect(dernier?.bilan).toEqual([])
    })

    it('ne compte pas l etape de bilan elle-meme', () => {
      // Le bilan porte des nombres, mais ce n'est pas un coup : le recompter
      // doublerait les totaux si la liste lui repassait sous le nez.
      const etapes = etapesDeroule(
        [attaque({ auteur_id: 60, cible: 'Colossus', cible_id: 12, subi: 3 })],
        [],
        1,
        AUCUN_MECHANT
      )
      expect(lignesBilan(avecBilan(etapes))).toEqual(lignesBilan(etapes))
    })
  })
})

// Un heros qui tombe au milieu de la phase. C'est le moment le plus important
// d'une partie, et le seul ou le deroule s'arrete net.
//
// La marque ne se devine pas : elle exige DEUX accords, l'un sur le monde
// (le moteur a bien elimine ce joueur, `WorldPlayer.is_eliminated`), l'autre
// sur le coup lui-meme (`restant` tombe a zero). Annoncer une defaite qui n'a
// pas eu lieu serait pire que de ne rien annoncer.
describe('la defaite d un heros', () => {
  // L'identite de Colossus, telle que board.tsx la donne : la carte de heros
  // d'un joueur que le monde declare elimine.
  const COLOSSUS_TOMBE = new Set([12])

  const activation = (etapes: EtapeDeroule[]) =>
    etapes.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')

  it('marque le coup qui met le heros a terre', () => {
    const [etape] = activation(
      etapesDeroule(
        [attaque({ cible: 'Colossus', cible_id: 12, subi: 6, restant: 0 })],
        [],
        1,
        AUCUN_MECHANT,
        COLOSSUS_TOMBE
      )
    )
    expect(etape.defaite).toBe(true)
  })

  // LE cas negatif, le plus important de la serie : une marque posee trop
  // largement s'afficherait a tort sans que rien ne le signale.
  it('ne marque AUCUNE etape ordinaire', () => {
    const etapes = etapesDeroule(
      [
        // Le meme heros, encore debout : le monde le dira tombe plus tard,
        // ce coup-ci ne l'a pas mis a terre.
        attaque({ cible: 'Colossus', cible_id: 12, subi: 3, restant: 5 }),
        // Une manigance : sa menace « restante » monte, elle ne tombe pas.
        attaque({ genre: 'manigance', cible: 'L’Effraction !', cible_id: 90, restant: 3 }),
      ],
      [entree()],
      1,
      AUCUN_MECHANT,
      COLOSSUS_TOMBE
    )
    for (const etape of etapes) expect(etape.defaite).toBeUndefined()
  })

  it('ne marque pas une cible a zero qui n est pas un heros', () => {
    // Un sbire abattu par son propre defenseur tombe lui aussi a zero. Sans
    // l'accord du monde, chaque sbire mort aurait coupe le deroule.
    const [etape] = activation(
      etapesDeroule(
        [attaque({ cible: 'Drone', cible_id: 88, restant: 0 })],
        [],
        1,
        AUCUN_MECHANT,
        COLOSSUS_TOMBE
      )
    )
    expect(etape.defaite).toBeUndefined()
  })

  it('ne marque pas un heros elimine dont CE coup ne dit pas la chute', () => {
    // Le monde le declare tombe, mais ce fait-la porte un compteur intact :
    // c'est un coup precedent qui l'a eu, pas celui-ci.
    const [etape] = activation(
      etapesDeroule(
        [attaque({ cible: 'Colossus', cible_id: 12, restant: undefined })],
        [],
        1,
        AUCUN_MECHANT,
        COLOSSUS_TOMBE
      )
    )
    expect(etape.defaite).toBeUndefined()
  })

  it('ne marque rien quand l appelant ne dit rien du monde', () => {
    // Le cinquieme argument est optionnel : sans lui, aucune defaite. C'est le
    // repli sur : ne rien annoncer plutot qu'annoncer a tort.
    const [etape] = activation(
      etapesDeroule([attaque({ cible_id: 12, restant: 0 })], [], 1, AUCUN_MECHANT)
    )
    expect(etape.defaite).toBeUndefined()
  })

  describe('arreterSurDefaite', () => {
    const coup = (cle: string, defaite?: true, cibleId = 12): EtapeDeroule => ({
      cle,
      temps: 'sbires',
      titre: 'attaque',
      regle: 'regle:activations',
      cibleId,
      boosts: [],
      ...(defaite ? { defaite } : {}),
    })

    it('garde l etape de defaite et coupe tout ce qui suit', () => {
      const coupe = arreterSurDefaite([coup('a'), coup('b', true), coup('c'), coup('d')])
      expect(coupe.map((e) => e.cle)).toEqual(['a', 'b'])
    })

    it('ne touche a rien sans defaite', () => {
      const liste = [coup('a'), coup('b')]
      expect(arreterSurDefaite(liste)).toBe(liste)
    })

    it('emporte aussi le bilan de fin de phase', () => {
      // La defaite gagne sur le bilan : le deroule s'arrete a la chute, donc
      // il n'y a plus de fin de phase a raconter derriere.
      const coupe = arreterSurDefaite(avecBilan([coup('a', true), coup('b')]))
      expect(coupe.some((e) => e.temps === 'bilan')).toBe(false)
      expect(coupe.map((e) => e.cle)).toEqual(['a'])
    })

    it('laisse une liste vide vide', () => {
      expect(arreterSurDefaite([])).toEqual([])
    })

    // MULTIJOUEUR : la phase continue pour les autres. Le deroule ne s'arrete
    // que chez le joueur dont le heros est tombe ; ailleurs, la chute est une
    // etape marquee de plus, et le cartouche montre l'attaque suivante — celle
    // que ce joueur-la a subie (constat F5).
    it('ne coupe pas chez un joueur dont le heros n est pas tombe', () => {
      const liste = [coup('a'), coup('b', true, 77), coup('c')]
      expect(arreterSurDefaite(liste, new Set([12]))).toBe(liste)
    })

    it('coupe chez le joueur dont le heros est tombe', () => {
      const coupe = arreterSurDefaite([coup('a'), coup('b', true, 77), coup('c')], new Set([77]))
      expect(coupe.map((e) => e.cle)).toEqual(['a', 'b'])
    })

    // Sans siege connu (solo, previsualisation, appelant qui ne lit pas le
    // monde), toute defaite est traitee comme la notre : c'est le comportement
    // d'avant, et le seul sur lequel on puisse se replier sans mentir.
    it('traite toute defaite comme la notre quand le siege est inconnu', () => {
      const coupe = arreterSurDefaite([coup('a'), coup('b', true, 77), coup('c')])
      expect(coupe.map((e) => e.cle)).toEqual(['a', 'b'])
      expect(
        arreterSurDefaite([coup('a'), coup('b', true, 77)], new Set<number>()).map((e) => e.cle)
      ).toEqual(['a', 'b'])
    })
  })
})

// ---------------------------------------------------------------------- A3 --
// L'ANNONCE avant la resolution : une activation ennemie produit deux faits.
//
// Avant la tache A3, une etape naissait d'un fait que le moteur avait DEJA
// resolu (`subi`, `defense`, `restant`) : il n'existait a aucun moment un etat
// « le mechant va attaquer » que le cartouche puisse montrer, et la fenetre ou
// le joueur peut defendre ou repondre passait sans qu'il la voie venir
// (constat F1 de l'audit du 06/09/2026).
describe("l'annonce d'une activation, puis sa resolution", () => {
  const annonce = (extra: Partial<FaitActivationAnnonce> = {}): FaitActivationAnnonce => ({
    genre: 'attaque',
    etat: 'annonce',
    activation_id: 1,
    phase: 'Enemy Activation',
    round_id: 1,
    auteur: 'Klaw',
    auteur_id: 50,
    cible: 'Colossus',
    cible_id: 12,
    base: 4,
    ...extra,
  })

  const resolution = (extra: Partial<FaitActivationResolue> = {}): FaitActivationResolue =>
    attaque({
      etat: 'resolu',
      activation_id: 1,
      round_id: 1,
      auteur: 'Klaw',
      auteur_id: 50,
      cible: 'Colossus',
      cible_id: 12,
      base: 4,
      boost: 0,
      defense: 0,
      inflige: 4,
      subi: 4,
      restant: 8,
      ...extra,
    })

  const activationsDe = (etapes: EtapeDeroule[]) =>
    etapes.filter((e) => e.temps === 'mechant' || e.temps === 'sbires')

  it("montre l'intention comme une etape, sans montant ni compteur", () => {
    const etapes = activationsDe(etapesDeroule([annonce()], [], 1, new Set([50])))
    expect(etapes).toHaveLength(1)
    expect(etapes[0]?.etat).toBe('annonce')
    expect(etapes[0]?.auteurNom).toBe('Klaw')
    expect(etapes[0]?.cibleNom).toBe('Colossus')
    // La valeur IMPRIMEE, et rien de ce qui n'existe pas encore.
    expect(etapes[0]?.valeurAnnoncee).toBe(4)
    expect(etapes[0]?.montant).toBeUndefined()
    expect(etapes[0]?.restant).toBeUndefined()
    expect(etapes[0]?.boosts).toEqual([])
  })

  // LE point de la tache : l'etape se COMPLETE, elle ne se remplace pas. Une
  // cle ou un index qui bougeraient feraient reculer le joueur d'une etape a
  // chaque coup resolu.
  it("complete l'etape sans changer ni sa cle ni son index quand la resolution arrive", () => {
    const avant = etapesDeroule([annonce()], [], 1, new Set([50]))
    const apres = etapesDeroule([resolution()], [], 1, new Set([50]))
    const iAvant = avant.findIndex((e) => e.etat === 'annonce')
    const iApres = apres.findIndex((e) => e.etat === 'resolu')
    expect(iAvant).toBeGreaterThanOrEqual(0)
    expect(iApres).toBe(iAvant)
    expect(apres[iApres]?.cle).toBe(avant[iAvant]?.cle)
    expect(apres[iApres]?.montant).toBe(4)
    expect(apres[iApres]?.restant).toBe(8)
  })

  // La cle vient de l'identifiant d'activation, pas d'un rang dans un tableau
  // filtre : c'est ce qui la rend insensible a ce que la phase produit par
  // ailleurs entre les deux temps.
  it("tire la cle de l'identifiant d'activation", () => {
    const [etape] = activationsDe(etapesDeroule([annonce({ activation_id: 7 })], [], 1, new Set([50])))
    expect(etape?.cle).toContain('7')
    const [autre] = activationsDe(etapesDeroule([annonce({ activation_id: 8 })], [], 1, new Set([50])))
    expect(autre?.cle).not.toBe(etape?.cle)
  })

  it("garde l'ancienne cle pour un fait sans identifiant (moteur anterieur)", () => {
    const ancien = attaque({ round_id: 1, auteur_id: 50 })
    const [etape] = activationsDe(etapesDeroule([ancien], [], 1, new Set([50])))
    expect(etape?.cle).toBe('fait:0:50')
    // Un fait sans `etat` est une RESOLUTION : c'est ce qu'il a toujours ete.
    expect(etape?.etat).toBe('resolu')
    expect(etape?.montant).toBe(5)
  })

  it("marque l'activation annulee, sans montant", () => {
    const [etape] = activationsDe(
      etapesDeroule([annonce({ etat: 'annule' })], [], 1, new Set([50]))
    )
    expect(etape?.etat).toBe('annule')
    expect(etape?.montant).toBeUndefined()
    expect(etape?.valeurAnnoncee).toBe(4)
  })

  // Une annonce n'a rien coute : elle ne doit rien peser dans le bilan de fin
  // de phase, sans quoi la meme activation compterait deux fois.
  it('ne fait entrer ni une annonce ni une annulation dans le bilan', () => {
    const etapes = etapesDeroule(
      [annonce({ activation_id: 1 }), annonce({ activation_id: 2, etat: 'annule' })],
      [],
      1,
      new Set([50])
    )
    expect(lignesBilan(etapes)).toEqual([])
  })

  it('ne compte le coup qu\'une fois quand la resolution a remplace son annonce', () => {
    const etapes = etapesDeroule([resolution()], [], 1, new Set([50]))
    expect(lignesBilan(etapes)).toEqual([
      { cle: 'degats:Colossus', genre: 'degats', cibleNom: 'Colossus', total: 4, restant: 8, plafond: undefined },
    ])
  })

  // Une activation annoncee ne peut pas porter la defaite : rien n'a encore
  // ete subi. Annoncer une chute qui n'a pas eu lieu serait le pire des faux
  // positifs (voir EtapeDeroule.defaite).
  it('ne marque jamais la defaite sur une annonce', () => {
    const [etape] = activationsDe(
      etapesDeroule([annonce({ cible_id: 12 })], [], 1, new Set([50]), new Set([12]))
    )
    expect(etape?.defaite).toBeUndefined()
  })
})

describe('un sbire qui entre en jeu en pleine phase', () => {
  const entreeEnJeu = (extra: Partial<FaitEntree> = {}): FaitEntree =>
    ({
      genre: 'entree',
      phase: 'Enemy Activation',
      carte: 'Drone',
      carte_id: 66,
      type: 'sbire',
      cause: 'Ultron',
      cause_id: 50,
      round_id: 1,
      ...extra,
    }) as FaitEntree

  it('devient une etape a lui seul, la carte en avant, sa cause dessous', () => {
    const [etape] = etapesDeroule([entreeEnJeu()], [], 1, new Set([50]))
    expect(etape?.titre).toBe('entree')
    expect(etape?.regle).toBe('regle:entree')
    expect(etape?.carteId).toBe(66)
    expect(etape?.cibleNom).toBe('Drone')
    expect(etape?.cause).toBe('Ultron')
    expect(etape?.cibleId).toBeUndefined()
  })

  it('se range apres l activation du vilain qui l a fait entrer, et avant les sbires', () => {
    const faits: FaitMechant[] = [
      attaque({ auteur: 'Ultron', auteur_id: 50, activation_id: 1 }),
      entreeEnJeu(),
      attaque({ auteur: 'Drone', auteur_id: 66, activation_id: 2 }),
    ]
    const etapes = etapesDeroule(faits, [], 1, new Set([50]))
    expect(etapes.map((e) => [e.temps, e.titre])).toEqual([
      ['mechant', 'attaque'],
      ['mechant', 'entree'],
      ['sbires', 'attaque'],
    ])
  })

  it('arrive au milieu des sbires quand c est le boost d un sbire qui le fait entrer', () => {
    const faits: FaitMechant[] = [
      attaque({ auteur: 'Ultron', auteur_id: 50, activation_id: 1 }),
      attaque({ auteur: 'Goblin Knight', auteur_id: 70, activation_id: 2 }),
      entreeEnJeu({ carte: 'Goblin Thrall', carte_id: 71, cause: 'Goblin Knight', cause_id: 70 }),
    ]
    const etapes = etapesDeroule(faits, [], 1, new Set([50]))
    expect(etapes.map((e) => [e.temps, e.titre])).toEqual([
      ['mechant', 'attaque'],
      ['sbires', 'attaque'],
      ['sbires', 'entree'],
    ])
  })

  it('avant toute activation, il tombe au point 1, sous la menace', () => {
    const [etape] = etapesDeroule([entreeEnJeu({ phase: 'Main Scheme Place Threat' })], [], 1, new Set([50]))
    expect(etape?.temps).toBe('menace')
  })
})

describe('les cartes de statut de la phase du mechant', () => {
  const statut = (extra: Partial<FaitStatut> = {}): FaitStatut =>
    ({
      genre: 'statut',
      phase: 'Enemy Activation',
      statut: 'Stunned',
      cible: 'Klaw',
      cible_id: 97,
      round_id: 1,
      ...extra,
    }) as FaitStatut

  it('devient une etape, rangee sous le MECHANT quand il porte le statut', () => {
    const [etape] = etapesDeroule([statut()], [], 1, new Set([97]))
    expect(etape?.titre).toBe('statut')
    expect(etape?.statut).toBe('Stunned')
    expect(etape?.cibleId).toBe(97)
    expect(etape?.temps).toBe('mechant')
  })

  it('se range sous les SBIRES quand ni le porteur ni la source ne sont le vilain', () => {
    const [etape] = etapesDeroule([statut({ cible: 'Colossus', cible_id: 12 })], [], 1, new Set([97]))
    expect(etape?.temps).toBe('sbires')
  })

  it('suit la source quand c est le vilain qui pose le statut sur un heros', () => {
    const [etape] = etapesDeroule(
      [statut({ cible: 'Colossus', cible_id: 12, cause: 'Klaw', cause_id: 97 })],
      [],
      1,
      new Set([97])
    )
    expect(etape?.temps).toBe('mechant')
  })

  it('suit la phase que le fait porte, quand elle la designe', () => {
    const [etape] = etapesDeroule([statut({ phase: 'Reveal Encounter Cards' })], [], 1, new Set([97]))
    expect(etape?.temps).toBe('revelation')
  })

  it('garde sa place dans la chronologie, entre deux activations', () => {
    // Les trois faits doivent tomber dans le MEME temps, sinon c'est le tri
    // par temps qui decide et non la chronologie : le vilain attaque, recoit
    // son statut, puis attaque a nouveau.
    const duVilain = attaque({ auteur: 'Klaw', auteur_id: 97 })
    const etapes = etapesDeroule([duVilain, statut(), duVilain], [], 1, new Set([97]))
    expect(etapes.map((e) => e.temps)).toEqual(['mechant', 'mechant', 'mechant'])
    expect(etapes.map((e) => e.titre)).toEqual(['attaque', 'statut', 'attaque'])
  })

  it('le bilan de fin de phase en fait une ligne, une par statut', () => {
    const etapes = etapesDeroule(
      [statut(), statut({ statut: 'Tough' }), statut()],
      [],
      1,
      new Set([97])
    )
    const lignes = lignesBilan(etapes)
    expect(lignes.map((l) => [l.genre, l.statut, l.total])).toEqual([
      ['statuts', 'Stunned', 2],
      ['statuts', 'Tough', 1],
    ])
  })
})
