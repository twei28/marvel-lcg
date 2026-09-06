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
import type { FaitMechant } from './world'
import type { EntreeHistorique } from './HistoriquePartie'

const attaque = (extra: Partial<FaitMechant> = {}): FaitMechant => ({
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
    // generique, puis la liste des consequences. Une etape par manigance dit
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
    const coup = (cle: string, defaite?: true): EtapeDeroule => ({
      cle,
      temps: 'sbires',
      titre: 'attaque',
      regle: 'regle:activations',
      boosts: [],
      consequences: [],
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
  })
})
