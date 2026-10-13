// Le decoupage de la phase du mechant en ETAPES a valider une par une.
//
// La source n'est pas une relecture du monde : le moteur envoie deja ses
// activations resolues (`FaitMechant`), avec la composition du coup (base,
// boost, defense) qu'aucune deduction ne saurait reconstituer. Le journal
// complete pour ce que les faits ne couvrent pas.
import { describe, expect, it } from 'vitest'
import { etapeEnLangue } from './etape-en-langue'
import {
  arreterSurDefaite,
  avecBilan,
  entreesPourRepli,
  etapesDeroule,
  etapesHorsPhase,
  tempsDeLaQuestion,
  lignesBilan,
  rangDansLeTemps,
  compteurDeLEtape,
  type EtapeDeroule,
} from './deroule-phase'
import type {
  FaitActivationAnnonce,
  FaitActivationBoosts,
  FaitActivationResolue,
  FaitDistribution,
  FaitEntree,
  FaitMechant,
  FaitMenace,
  FaitRevelation,
  FaitStatut,
} from './world'
import type { EntreeHistorique } from './HistoriquePartie'
import { coupsDe } from './frise-phase'

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
        cle: 'c1:77:revealed',
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
        [entree({ cle: 'c1:revealed', type: 'card', phase: 'Deal Encounter Cards', nomCarte: 'Sonic Boom', cibleId: 77 })],
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
          entree({ cle: 'a:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 }),
          entree({ cle: 'c:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte C', joueur: 2 }),
          entree({ cle: 'b:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte B', joueur: 1 }),
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
          entree({ cle: 'a:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 }),
          entree({ cle: 'b:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte B', joueur: 1 }),
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
        [entree({ cle: 'a:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 })],
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
        [entree({ cle: 'a:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Bombe à retardement', joueur: 0 })],
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
          entree({ cle: 'b:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte B', joueur: 1 }),
          entree({ cle: 'a:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Carte A', joueur: 0 }),
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
      entree({ cle: 'r3-b:revealed', round: 3, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R3-B', nomCarte: 'Carte R3-B', cibleId: 3 }),
      entree({ cle: 'r3-a:revealed', round: 3, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R3-A', nomCarte: 'Carte R3-A', cibleId: 2 }),
      entree({ cle: 'r2:revealed', round: 2, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R2', nomCarte: 'Carte R2', cibleId: 1 }),
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
      expect(etapes.map((e) => e.cle)).toEqual(['carte:r3-a:revealed', 'carte:r3-b:revealed'])
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

  it('distribution et revelation portent le siege du joueur concerne (couleur du cadre, 12/10/2026)', () => {
    const etapes = etapesDeroule(
      [faitDistribution({ joueur: 1 }), faitRevelation({ joueur: 1 })],
      [],
      1,
      new Set([50])
    )
    expect(etapes.filter((e) => e.temps === 'distribution' || e.temps === 'revelation').map((e) => e.joueur)).toEqual([1, 1])
  })

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

  // Signalement Yarro n27 (28/09/2026) : une carte enchainee par Renfort
  // (Surge) doit porter la marque `parSurge`, pour que le cartouche la
  // distingue d'une revelation ordinaire du point 3.
  it('porte parSurge quand le fait vient d un Renfort, absent sinon', () => {
    const [surge] = etapesDeroule([faitRevelation({ par_surge: true })], [], 1, AUCUN_MECHANT)
    expect(surge.parSurge).toBe(true)
    const [ordinaire] = etapesDeroule([faitRevelation({ par_surge: false })], [], 1, AUCUN_MECHANT)
    expect(ordinaire.parSurge).toBeUndefined()
    const [absent] = etapesDeroule([faitRevelation()], [], 1, AUCUN_MECHANT)
    expect(absent.parSurge).toBeUndefined()
  })

  // Decision du 03/10/2026 : la carte enchainee porte le nom de celle dont le
  // Renfort l'a revelee (« Renfort de X » en surtitre), et la precedente sait
  // qu'un Renfort la suit. Chaine maillon par maillon.
  it('relie chaque Renfort a la carte qui l a declenche, maillon par maillon', () => {
    const etapes = etapesDeroule(
      [
        faitRevelation({ carte: 'Carte A', carte_id: 1 }),
        faitRevelation({ carte: 'Carte B', carte_id: 2, par_surge: true }),
        faitRevelation({ carte: 'Carte C', carte_id: 3, par_surge: true }),
      ],
      [],
      1,
      AUCUN_MECHANT
    )
    expect(etapes.map((e) => e.renfortDe)).toEqual([undefined, 'Carte A', 'Carte B'])
    expect(etapes.map((e) => e.suivieDUnRenfort)).toEqual([true, true, undefined])
  })

  // Capture du 12/10/2026 : « Renfort de Caught Off Guard » dans une partie en
  // francais. Le nom de la carte d'origine doit passer par la traduction des
  // noms, comme le titre de la carte revelee.
  it('traduit le nom de la carte d origine du Renfort', () => {
    const etapes = etapesDeroule(
      [
        faitRevelation({ carte: 'Caught Off Guard', carte_id: 11 }),
        faitRevelation({ carte: 'Weapons Runner', carte_id: 12, par_surge: true }),
      ],
      [],
      1,
      AUCUN_MECHANT
    )
    const noms: Record<number, string> = { 11: 'Pris par Surprise', 12: "Trafiquant d'Armes" }
    const lue = etapeEnLangue(etapes[1], (id) => noms[id])
    expect(lue.renfortDe).toBe('Pris par Surprise')
    expect(lue.cibleNom).toBe("Trafiquant d'Armes")
  })

  it('porte qui a annule une activation ou une carte revelee (04/10/2026)', () => {
    const [carte] = etapesDeroule(
      [faitRevelation({ annulee_par: 'Spider-Man', annulee_par_id: 1 })], [], 1, AUCUN_MECHANT
    )
    expect(carte).toMatchObject({ annuleePar: 'Spider-Man', annuleeParId: 1 })
    const [activation] = etapesDeroule(
      [{ genre: 'attaque', etat: 'annule', activation_id: 3, round_id: 1, phase: 'Enemy Activation',
         auteur: 'Rhino', auteur_id: 50, cible: 'Shuri', cible_id: 12, annule_par: 'Stunned', annule_par_id: 89 }],
      [], 1, new Set([50])
    )
    expect(activation).toMatchObject({ etat: 'annule', annuleePar: 'Stunned', annuleeParId: 89 })
  })

  it('un changement de stade en pleine phase est une etape a part (04/10/2026)', () => {
    const etapes = etapesDeroule(
      [
        faitMenace(),
        { genre: 'stade', quoi: 'manigance', phase: 'Main Scheme Place Threat', round_id: 1,
          avant: 'The Break-In!', carte: 'Countdown', carte_id: 49 },
      ],
      [], 1, AUCUN_MECHANT
    )
    const stade = etapes.find((e) => e.titre === 'stade')
    expect(stade).toMatchObject({ temps: 'menace', carteId: 49, cibleNom: 'Countdown', auteurNom: 'The Break-In!', stade: 'manigance' })
  })

  it('garde la marque ★ des boosts publies par le moteur', () => {
    const [coup] = etapesDeroule(
      [attaque({ round_id: 1, boosts: [{ nom: 'Venom Blast', id: 81, apport: 1, etoile: true }] })], [], 1, new Set([50])
    )
    expect(coup.boosts[0].etoile).toBe(true)
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
      [entree({ cle: '118:card:Sonic Boom révélée:61:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Sonic Boom' })],
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
      [entree({ cle: '118:card:Sonic Boom révélée:61:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Sonic Boom' })],
      1,
      AUCUN_MECHANT
    )
    const revelations = etapes.filter((e) => e.temps === 'revelation')
    expect(revelations).toHaveLength(1)
    expect(revelations[0].cibleNom).toBe('Sonic Boom')
  })

  it('le repli ne prend jamais une carte du joueur jouee ou defaussee pour une carte rencontre', () => {
    const etapes = etapesDeroule(
      [faitMenace()],
      [
        entree({ cle: '124:card:Quinjet défaussé:39:discard', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Quinjet' }),
        entree({ cle: '124:card:Frappe héroïque joué:13:play', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Frappe héroïque' }),
        entree({ cle: '124:card:Sonic Boom révélée:61:revealed', type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Sonic Boom' }),
      ],
      1,
      AUCUN_MECHANT
    )
    expect(etapes.filter((e) => e.temps === 'revelation').map((e) => e.cibleNom)).toEqual(['Sonic Boom'])
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

describe('le journal de repli apres un Undo', () => {
  // Signalement Yarro n42 (02/10/2026). L'Undo rejoue la partie depuis zero :
  // le monde revient SANS aucun fait du mechant, mais le journal du navigateur
  // garde la phase du mechant d'avant, au meme round. Relu par le repli, il
  // rouvrait le cartouche en plein tour du joueur.
  const phaseDAvant = [entree({ round: 1 })]

  it('hors phase du mechant, le journal ne nourrit rien', () => {
    const etapes = etapesDeroule([], entreesPourRepli(phaseDAvant, false), 1, AUCUN_MECHANT)
    expect(etapes).toHaveLength(0)
  })

  it('pendant la phase du mechant, le repli relit toujours le journal', () => {
    const etapes = etapesDeroule([], entreesPourRepli(phaseDAvant, true), 1, AUCUN_MECHANT)
    expect(etapes.filter((e) => e.temps === 'menace')).toHaveLength(1)
  })

  // Signalement du 13/10/2026 : un « Annuler » en pleine phase ramene le monde
  // au rendu 79, le journal garde la version annulee (rendus 118 a 124), et
  // l'etape 3 montrait des cartes du joueur jamais revelees.
  it('apres un Annuler, le repli ne lit pas les lignes d un futur annule', () => {
    const futur = [
      entree({ cle: '124:card:Quinjet révélée:39:revealed', renderId: 124, type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Quinjet' }),
      entree({ cle: 'm', renderId: 70 }),
    ]
    const etapes = etapesDeroule([], entreesPourRepli(futur, true, 79), 1, AUCUN_MECHANT)
    expect(etapes.filter((e) => e.temps === 'revelation')).toHaveLength(0)
    expect(etapes.filter((e) => e.temps === 'menace')).toHaveLength(1)
  })

  it('une ligne du rendu affiche lui-meme reste lisible', () => {
    const lignes = [entree({ cle: '79:card:Sonic Boom révélée:61:revealed', renderId: 79, type: 'card', phase: 'Reveal Encounter Cards', nomCarte: 'Sonic Boom' })]
    expect(entreesPourRepli(lignes, true, 79)).toHaveLength(1)
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
          cle: 'c1:77:revealed',
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
            cle: 'c1:77:revealed',
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
      // ⚠ `cibleId` depuis le 15/09/2026 : la ligne porte l'identifiant moteur
      // de sa cible pour que son nom puisse etre traduit (le bilan disait
      // « The Break-In! » sous un cartouche qui ecrivait « L'Effraction ! »).
      // Le groupement, lui, reste sur le nom anglais : c'est la clef.
      {
        cle: 'degats:Colossus',
        genre: 'degats',
        cibleNom: 'Colossus',
        cibleId: 12,
        total: 4,
        restant: 8,
        plafond: undefined,
      },
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

describe('les cascades sous leur carte revelee (rapport Yarro n46)', () => {
  // Psionic Slash est revelee et fait manigancer Bloody Mary, avec Hit List en
  // boost. Avant : une etape « Bloody Mary manigance » A PART, affichee AVANT
  // la revelation qui la provoquait.
  const revelation: FaitRevelation = {
    genre: 'revelation',
    phase: 'Reveal Encounter Cards',
    round_id: 4,
    joueur: 0,
    joueur_nom: 'Echo',
    carte: 'Psionic Slash',
    carte_id: 54,
    effets: [
      { genre: 'menace', cible: 'Stop the Presses!', cible_id: 48, montant: 4, restant: 6 },
      { genre: 'degats', cible: 'Echo', cible_id: 1, montant: 1, restant: 8 },
    ],
  }
  const manigance = attaque({
    genre: 'manigance',
    phase: 'Reveal Encounter Cards',
    round_id: 4,
    auteur: 'Bloody Mary',
    auteur_id: 49,
    cible: 'Stop the Presses!',
    cible_id: 48,
    base: 1,
    boost: 3,
    defense: 0,
    inflige: 4,
    subi: 4,
    restant: 6,
    boosts: [{ nom: 'Hit List', id: 77, apport: 3 }],
    cause: 'Psionic Slash',
  })
  const mechants = new Set([49])

  it('la manigance declenchee se range SOUS la carte, plus d etape a part', () => {
    const etapes = etapesDeroule([revelation, manigance], [], 4, mechants)
    const revelees = etapes.filter((e) => e.temps === 'revelation')
    expect(revelees).toHaveLength(1)
    expect(revelees[0].titre).toBe('revelation')
    expect(revelees[0].consequences?.map((c) => c.titre)).toEqual(['manigance'])
    expect(revelees[0].consequences?.[0].auteurNom).toBe('Bloody Mary')
  })

  it('le meme ordre des faits ne change rien (activation inscrite avant la revelation)', () => {
    const etapes = etapesDeroule([manigance, revelation], [], 4, mechants)
    expect(etapes.filter((e) => e.temps === 'revelation').map((e) => e.titre)).toEqual(['revelation'])
  })

  it('l effet mesure sur la meme cible est retire, les autres restent', () => {
    const [etape] = etapesDeroule([revelation, manigance], [], 4, mechants).filter((e) => e.titre === 'revelation')
    expect(etape.effets).toEqual([{ genre: 'degats', cible: 'Echo', cible_id: 1, montant: 1, restant: 8 }])
  })

  it('⚠ TEMOIN : une activation causee par autre chose reste une etape a part', () => {
    const autre = { ...manigance, cause: 'Ultron' }
    const etapes = etapesDeroule([revelation, autre], [], 4, mechants)
    expect(etapes.filter((e) => e.temps === 'revelation').map((e) => e.titre)).toEqual(['manigance', 'revelation'])
  })
})

describe("l'onglet d'une question posee par le moteur", () => {
  it('pendant les activations, suit l attaquant : le mechant (2a) ou un sbire (2b)', () => {
    expect(tempsDeLaQuestion('Enemy Activation', true)).toBe('mechant')
    expect(tempsDeLaQuestion('Enemy Activation', false)).toBe('sbires')
    expect(tempsDeLaQuestion('Enemy Activation', undefined)).toBe('mechant')
  })

  it('ailleurs, la phase du moteur suffit', () => {
    expect(tempsDeLaQuestion('Main Scheme Place Threat', undefined)).toBe('menace')
    expect(tempsDeLaQuestion('Reveal Encounter Cards', undefined)).toBe('revelation')
    expect(tempsDeLaQuestion('Player Turn', undefined)).toBeUndefined()
  })
})

// Decision du 03/10/2026 : HORS PHASE du mechant (tour du joueur), une attaque
// ou une manigance du mechant ouvre le cartouche pour ce seul coup. Le moteur
// la date du tour (« Player 1 Turn ») : elle ne doit pas se glisser dans la
// phase du mechant du meme round.
describe('les activations hors phase', () => {
  const horsPhase = attaque({ round_id: 2, phase: 'Player 1 Turn', auteur_id: 50 })
  it('ne font pas partie de la phase du mechant', () => {
    expect(etapesDeroule([horsPhase], [], 2, new Set([50]))).toEqual([])
  })
  it('forment leurs propres etapes, marquees hors phase', () => {
    const [coup] = etapesHorsPhase([horsPhase], 2, new Set([50]))
    expect(coup).toMatchObject({ titre: 'attaque', horsPhase: true, auteurNom: 'Ultron', montant: 5 })
    expect(etapesHorsPhase([horsPhase], 3, new Set([50]))).toEqual([])
    expect(etapesHorsPhase([attaque({ round_id: 2 })], 2, new Set([50]))).toEqual([])
  })
})

// LE CARTOUCHE DU BAS (refonte du 04/10/2026) lit des faits enrichis : le fait
// intermediaire `boosts` (defenseur et boosts retournes avant les degats), le
// heros vise et le defenseur sur le resolu, la decomposition de la menace, les
// stats d'un stade, le type d'une carte revelee. Chaque cle est OPTIONNELLE :
// un moteur plus ancien, une sauvegarde ou une fixture donnent l'etape
// d'avant, sans rien inventer.
describe('les faits enrichis du cartouche', () => {
  const fait = (f: FaitMechant): FaitMechant => f
  const annonceRhino = fait({
    genre: 'attaque',
    etat: 'annonce',
    activation_id: 3,
    round_id: 1,
    phase: 'Enemy Activation',
    auteur: 'Rhino',
    auteur_id: 12,
    cible: 'Spider-Man',
    cible_id: 40,
    base: 2,
  })
  const boostsRhino: FaitActivationBoosts = {
    genre: 'attaque',
    etat: 'boosts',
    activation_id: 3,
    round_id: 1,
    phase: 'Enemy Activation',
    auteur: 'Rhino',
    auteur_id: 12,
    cible: 'Spider-Man',
    cible_id: 40,
    defenseur: 'Spider-Man',
    defenseur_id: 40,
    defense: 3,
    boosts: [
      { nom: 'Charge', id: 77, apport: 1 },
      { nom: 'Sweeping Swoop', id: 78, apport: 0, etoile: true },
    ],
    boost: 1,
    total_avant_defense: 3,
    base_imprimee: 2,
  }

  it('un fait etat boosts donne une etape annonce sous la meme cle, enrichie', () => {
    const [annonce] = etapesDeroule([annonceRhino], [], 1, new Set([12]))
    const [etape] = etapesDeroule([boostsRhino], [], 1, new Set([12]))
    expect(etape?.cle).toBe(annonce?.cle)
    expect(etape?.cle).toBe('activation:3')
    expect(etape).toMatchObject({
      etat: 'annonce',
      temps: 'mechant',
      titre: 'attaque',
      defenseurId: 40,
      defenseurNom: 'Spider-Man',
      defense: 3,
      totalAvantDefense: 3,
      baseImprimee: 2,
      valeurAnnoncee: 2,
    })
    expect(etape?.boosts).toHaveLength(2)
    expect(etape?.boosts[1]).toMatchObject({ nom: 'Sweeping Swoop', cibleId: 78, apport: 0, etoile: true })
    // Rien n'est encore subi : ni montant, ni compteur, ni defaite.
    expect(etape?.montant).toBeUndefined()
    expect(etape?.restant).toBeUndefined()
    expect(etape?.defaite).toBeUndefined()
  })

  it('un fait boosts sans defenseur reste une annonce sans defenseur', () => {
    const sansDefense: FaitActivationBoosts = { ...boostsRhino, defenseur: null, defenseur_id: null, defense: 0 }
    const [etape] = etapesDeroule([sansDefense], [], 1, new Set([12]))
    expect(etape?.etat).toBe('annonce')
    expect(etape?.defenseurId).toBeUndefined()
    expect(etape?.defenseurNom).toBeUndefined()
  })

  it('les cles nouvelles sont portees quand le fait les a', () => {
    const resolu = attaque({
      etat: 'resolu',
      activation_id: 4,
      round_id: 1,
      auteur: 'Rhino',
      auteur_id: 12,
      cible: 'Black Widow',
      cible_id: 41,
      base: 2,
      boost: 1,
      defense: 1,
      inflige: 2,
      subi: 1,
      restant: 1,
      defenseur: 'Black Widow',
      defenseur_id: 41,
      cible_annoncee: 'Spider-Man',
      cible_annoncee_id: 40,
      base_imprimee: 2,
      cause: 'Stampede',
      cause_id: 88,
    })
    const manigance = attaque({
      genre: 'manigance',
      activation_id: 5,
      round_id: 1,
      auteur: 'Rhino',
      auteur_id: 12,
      cible: 'Effraction',
      cible_id: 9,
      subi: 2,
      restant: 6,
      plafond: 7,
    })
    const menace = fait({
      genre: 'menace',
      round_id: 1,
      phase: 'Main Scheme Place Threat',
      cible: 'Effraction',
      cible_id: 9,
      montant: 2,
      restant: 4,
      plafond: 7,
      escalade: 1,
      acceleration: 1,
      joueurs: 1,
    })
    const revelation = fait({
      genre: 'revelation',
      round_id: 1,
      phase: 'Reveal Encounter Cards',
      carte: 'Stampede',
      carte_id: 88,
      type: 'Treachery',
    })
    const stade = fait({
      genre: 'stade',
      round_id: 1,
      phase: 'Enemy Activation',
      quoi: 'mechant',
      avant: 'Rhino',
      carte: 'Rhino',
      carte_id: 13,
      avant_id: 12,
      stats_avant: { pv_max: 14, atq: 2, man: 1 },
      stats_apres: { pv_max: 15, atq: 3, man: 1 },
    })
    const etapes = etapesDeroule([menace, resolu, manigance, stade, revelation], [], 1, new Set([12]))
    const parCle = (debut: string) => etapes.find((e) => e.cle.startsWith(debut))
    expect(parCle('activation:4')).toMatchObject({
      inflige: 2,
      defenseurId: 41,
      defenseurNom: 'Black Widow',
      cibleAnnonceeId: 40,
      baseImprimee: 2,
      causeId: 88,
    })
    expect(parCle('activation:5')?.plafond).toBe(7)
    expect(parCle('menace:')).toMatchObject({ escalade: 1, acceleration: 1, joueurs: 1 })
    expect(parCle('revelation:')?.typeCarte).toBe('Treachery')
    expect(parCle('stade:')).toMatchObject({
      stadeAvantId: 12,
      statsAvant: { pv_max: 14, atq: 2, man: 1 },
      statsApres: { pv_max: 15, atq: 3, man: 1 },
    })
  })

  it('un fait ancien sans ces champs : l etape ne les porte pas', () => {
    const etapes = etapesDeroule(
      [
        fait({ genre: 'menace', round_id: 1, phase: 'Main Scheme Place Threat', cible: 'Effraction', cible_id: 9, montant: 1 }),
        attaque({ activation_id: 4, round_id: 1, auteur_id: 12 }),
        attaque({ genre: 'manigance', activation_id: 5, round_id: 1, auteur_id: 12 }),
        fait({ genre: 'stade', round_id: 1, phase: 'Enemy Activation', quoi: 'mechant', avant: 'Rhino', carte: 'Rhino', carte_id: 13 }),
        fait({ genre: 'revelation', round_id: 1, phase: 'Reveal Encounter Cards', carte: 'Stampede', carte_id: 88 }),
      ],
      [],
      1,
      new Set([12])
    )
    for (const etape of etapes) {
      expect(etape.defenseurId).toBeUndefined()
      expect(etape.defenseurNom).toBeUndefined()
      expect(etape.cibleAnnonceeId).toBeUndefined()
      expect(etape.baseImprimee).toBeUndefined()
      expect(etape.totalAvantDefense).toBeUndefined()
      expect(etape.escalade).toBeUndefined()
      expect(etape.acceleration).toBeUndefined()
      expect(etape.joueurs).toBeUndefined()
      expect(etape.typeCarte).toBeUndefined()
      expect(etape.stadeAvantId).toBeUndefined()
      expect(etape.statsAvant).toBeUndefined()
      expect(etape.statsApres).toBeUndefined()
      expect(etape.causeId).toBeUndefined()
    }
    expect(etapes.find((e) => e.titre === 'manigance')?.plafond).toBeUndefined()
    // `inflige` est publie depuis toujours : il est porte, meme par un fait ancien.
    expect(etapes.find((e) => e.titre === 'attaque')?.inflige).toBe(5)
  })

  it('etapesHorsPhase avecRevelations garde une revelation datee du tour d un joueur, pas sans l option', () => {
    const revelation = fait({
      genre: 'revelation',
      round_id: 2,
      phase: 'Player 1 Turn',
      carte: 'Stampede',
      carte_id: 88,
      type: 'Treachery',
      par_surge: false,
      joueur: 0,
      joueur_nom: 'Spider-Man',
    })
    const [carte] = etapesHorsPhase([revelation], 2, new Set([12]), { avecRevelations: true })
    expect(carte).toMatchObject({ titre: 'revelation', horsPhase: true, carteId: 88, typeCarte: 'Treachery' })
    expect(etapesHorsPhase([revelation], 2, new Set([12]))).toEqual([])
    // Elle n'entre jamais dans la phase du mechant du meme round.
    expect(etapesDeroule([revelation], [], 2, new Set([12]))).toEqual([])
  })
})

// L'ACTIVATION ANNULEE PAR SONNE (decision du 05/10/2026, etat 04 du
// cartouche) : le moteur publie un fait `sonne`, l'etape le raconte. Le total
// des sbires (`rang_sbire` / `total_sbires`) voyage sur les faits d'un sbire.
describe('le fait Sonne et le total des sbires', () => {
  const sonneRhino: FaitMechant = {
    genre: 'sonne',
    round_id: 1,
    phase: 'Enemy Activation',
    temps: 'attaque',
    type: 'mechant',
    joueur: 0,
    auteur: 'Rhino',
    auteur_id: 12,
    cible: 'Spider-Man',
    cible_id: 40,
    statut_retire: true,
    annule_par: 'Stunned',
    annule_par_id: 99,
    fait_id: 'sonne:1:12',
  }

  it('un ennemi sonne donne une etape sonne, rangee sous le mechant, sans etape d attaque', () => {
    const etapes = etapesDeroule([sonneRhino], [], 1, new Set([12]))
    expect(etapes).toHaveLength(1)
    expect(etapes[0]).toMatchObject({
      temps: 'mechant',
      titre: 'sonne',
      carteId: 12,
      auteurNom: 'Rhino',
      sonneTemps: 'attaque',
      statutRetire: true,
    })
    expect(etapes[0]?.cibleId).toBeUndefined()
  })

  it('un sbire sonne se range sous les sbires, et une manigance se dit manigance', () => {
    const [etape] = etapesDeroule(
      [{ ...sonneRhino, type: 'sbire', temps: 'manigance', auteur_id: 31, auteur: 'Drone' }],
      [],
      1,
      new Set([12])
    )
    expect(etape).toMatchObject({ temps: 'sbires', titre: 'sonne', carteId: 31, sonneTemps: 'manigance' })
  })

  it('un ennemi Constant ne perd pas Sonne : statutRetire reste faux', () => {
    const [etape] = etapesDeroule([{ ...sonneRhino, statut_retire: false }], [], 1, new Set([12]))
    expect(etape?.statutRetire).toBe(false)
  })

  it('une etape sonne ne compte ni degats ni menaces dans le bilan', () => {
    const etapes = etapesDeroule([sonneRhino], [], 1, new Set([12]))
    expect(coupsDe(etapes[0] as EtapeDeroule)).toEqual([])
  })

  it('rang_sbire et total_sbires passent du fait a l etape (activation et sonne)', () => {
    const attaqueDrone: FaitMechant = {
      genre: 'attaque',
      etat: 'annonce',
      activation_id: 5,
      round_id: 1,
      phase: 'Enemy Activation',
      auteur: 'Drone',
      auteur_id: 31,
      cible: 'Spider-Man',
      cible_id: 40,
      base: 1,
      rang_sbire: 1,
      total_sbires: 2,
    }
    const [attaque, sonne] = etapesDeroule(
      [attaqueDrone, { ...sonneRhino, type: 'sbire', auteur_id: 32, rang_sbire: 2, total_sbires: 2 }],
      [],
      1,
      new Set([12])
    )
    expect(attaque).toMatchObject({ rangSbire: 1, totalSbires: 2 })
    expect(sonne).toMatchObject({ rangSbire: 2, totalSbires: 2 })
  })

  it('sans rang_sbire (moteur ancien), l etape n en porte pas', () => {
    const [etape] = etapesDeroule([sonneRhino], [], 1, new Set([12]))
    expect(etape?.rangSbire).toBeUndefined()
    expect(etape?.totalSbires).toBeUndefined()
  })

  it('compteurDeLEtape : le total annonce par le moteur des la premiere etape, repli sur le compte des etapes', () => {
    const sbire = (cle: string, rangSbire?: number, totalSbires?: number): EtapeDeroule => ({
      cle,
      temps: 'sbires',
      titre: 'attaque',
      regle: '',
      boosts: [],
      rangSbire,
      totalSbires,
    })
    // Une seule etape connue, mais le moteur annonce deux sbires.
    expect(compteurDeLEtape([sbire('a', 1, 2)], 0)).toEqual({ rang: 1, total: 2 })
    expect(compteurDeLEtape([sbire('a', 1, 2), sbire('b', 2, 2)], 1)).toEqual({ rang: 2, total: 2 })
    // Un seul sbire : « 1 sur 1 » n'apprend rien.
    expect(compteurDeLEtape([sbire('a', 1, 1)], 0)).toBeUndefined()
    // Sans rang, l'ancien compte.
    expect(compteurDeLEtape([sbire('a'), sbire('b')], 1)).toEqual({ rang: 2, total: 2 })
    expect(compteurDeLEtape([sbire('a')], 0)).toBeUndefined()
  })
})

describe('la carte de remplacement (rapports Yarro n71 et n72, 09/10/2026)', () => {
  // Partie n72 : Weapons Runner (Surge) revele Klaw's Vengeance, annulee par
  // Stepford Cuckoos qui part a la defausse (dernier psi) et revele Sonic Boom.
  const base = { genre: 'revelation' as const, phase: 'Reveal Encounter Cards', round_id: 3, joueur: 0, joueur_nom: 'Storm' }
  const runner: FaitRevelation = { ...base, carte: 'Weapons Runner', carte_id: 65, type: 'Minion' }
  const vengeance: FaitRevelation = {
    ...base, carte: "Klaw's Vengeance", carte_id: 66, par_surge: true,
    annulee_par: 'Stepford Cuckoos', annulee_par_id: 32, annulee_par_sort: 'defaussee',
  }
  const sonicBoom: FaitRevelation = {
    ...base, carte: 'Sonic Boom', carte_id: 69, revelee_par: 'Stepford Cuckoos', revelee_par_id: 32,
  }
  const attaqueKlaw = attaque({
    phase: 'Reveal Encounter Cards', round_id: 3, auteur: 'Klaw', auteur_id: 57, cible: 'Storm', cible_id: 1,
    base: 2, boost: 0, defense: 0, inflige: 2, subi: 2, restant: 8, boosts: [],
    cause: 'Sonic Boom', cause_id: 69,
  })

  it('lit revelee_par, et relie la carte annulee a sa remplacante', () => {
    const etapes = etapesDeroule([runner, vengeance, sonicBoom], [], 3, new Set([57]))
    const [r, v, s] = etapes.filter((e) => e.titre === 'revelation')
    expect(r.suivieDUnRenfort).toBe(true)
    expect(v).toMatchObject({ parSurge: true, renfortDe: 'Weapons Runner', annuleePar: 'Stepford Cuckoos', annuleeParSort: 'defaussee', suivieDUnRemplacement: true })
    expect(s).toMatchObject({ reveleePar: 'Stepford Cuckoos', reveleeParId: 32 })
    expect(s.parSurge).toBeUndefined()
    expect(s.renfortDe).toBeUndefined()
  })

  it('l attaque causee par la carte de remplacement se range sous elle, pas sous l annulee', () => {
    const etapes = etapesDeroule([runner, vengeance, sonicBoom, attaqueKlaw], [], 3, new Set([57]))
    const revelees = etapes.filter((e) => e.titre === 'revelation')
    expect(revelees.find((e) => e.cibleNom === 'Sonic Boom')?.consequences?.map((c) => c.titre)).toEqual(['attaque'])
    expect(revelees.find((e) => e.cibleNom === "Klaw's Vengeance")?.consequences).toBeUndefined()
  })

  it('⚠ TEMOIN : sans annulation par la meme carte, aucun lien de remplacement', () => {
    const autre = { ...vengeance, annulee_par: 'Black Widow', annulee_par_id: 41 }
    const etapes = etapesDeroule([runner, autre, sonicBoom], [], 3, new Set([57]))
    expect(etapes.some((e) => e.suivieDUnRemplacement)).toBe(false)
  })
})
