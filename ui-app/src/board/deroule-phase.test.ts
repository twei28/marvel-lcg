// Le decoupage de la phase du mechant en ETAPES a valider une par une.
//
// La source n'est pas une relecture du monde : le moteur envoie deja ses
// activations resolues (`FaitMechant`), avec la composition du coup (base,
// boost, defense) qu'aucune deduction ne saurait reconstituer. Le journal
// complete pour ce que les faits ne couvrent pas.
import { describe, expect, it } from 'vitest'
import { etapesDeroule } from './deroule-phase'
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
    ...extra,
  }) as EntreeHistorique

describe('etapesDeroule', () => {
  it('fait une etape par activation du moteur', () => {
    const etapes = etapesDeroule([attaque(), attaque({ auteur: 'Drone', auteur_id: 60 })], [], 1)
    const activations = etapes.filter((e) => e.temps === 'activations')
    expect(activations).toHaveLength(2)
  })

  it('met la carte qui agit en avant et retient sa cible', () => {
    const [etape] = etapesDeroule([attaque()], [], 1).filter((e) => e.temps === 'activations')
    expect(etape.carteId).toBe(50)
    expect(etape.cibleId).toBe(12)
  })

  it('porte les boosts de l activation, dans l ordre', () => {
    const etapes = etapesDeroule(
      [attaque({ boosts: [{ nom: 'Boost A', id: 91, apport: 1 }, { nom: 'Boost B', id: 92, apport: 1 }] })],
      [],
      1
    )
    const [etape] = etapes.filter((e) => e.temps === 'activations')
    expect(etape.boosts.map((b) => b.nom)).toEqual(['Boost A', 'Boost B'])
    expect(etape.boosts.map((b) => b.cle)).toEqual(['boost:0:91', 'boost:1:92'])
  })

  it('range une activation declenchee par une carte revelee sous la revelation', () => {
    // Un vilain peut frapper une seconde fois hors de l'etape des activations :
    // le fait porte sa propre phase, on la suit plutot que de tout ranger sous
    // « activations ».
    const etapes = etapesDeroule([attaque({ phase: 'Reveal Encounter Cards' })], [], 1)
    expect(etapes.filter((e) => e.temps === 'revelation')).toHaveLength(1)
    expect(etapes.filter((e) => e.temps === 'activations')).toHaveLength(0)
  })

  it('fait une etape de menace a partir du journal', () => {
    const etapes = etapesDeroule([], [entree()], 1)
    expect(etapes.filter((e) => e.temps === 'menace')).toHaveLength(1)
  })

  it('donne une cle stable et unique a chaque etape', () => {
    const etapes = etapesDeroule([attaque(), attaque({ auteur_id: 60 })], [entree()], 1)
    const cles = etapes.map((e) => e.cle)
    expect(new Set(cles).size).toBe(cles.length)
  })

  it('rend les etapes dans l ordre des quatre temps', () => {
    const etapes = etapesDeroule(
      [attaque(), attaque({ phase: 'Reveal Encounter Cards', auteur_id: 60 })],
      [entree()],
      1
    )
    expect(etapes.map((e) => e.temps)).toEqual(['menace', 'activations', 'revelation'])
  })

  it('ne rend aucune etape quand la phase n a rien produit', () => {
    expect(etapesDeroule([], [], 1)).toEqual([])
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
    ], 1)
    const revelations = etapes.filter((e) => e.temps === 'revelation')
    expect(revelations).toHaveLength(1)
    expect(revelations[0].carteId).toBe(77)
  })

  it('garde le texte brut du moteur quand le fait n a pas de phrase', () => {
    // Une carte fan-made a l'effet inattendu : mieux vaut un texte technique
    // qu'un silence. On voit au moins qu'il s'est passe quelque chose.
    const etapes = etapesDeroule([], [
      entree({
        cle: 'c2',
        type: 'text',
        phase: 'Reveal Encounter Cards',
        titre: '',
        brut: '[(50,01113) Klaw] would deal 2 damage',
      }),
    ], 1)
    // Assertion sur la liste complete, pas un some() : celui-ci restait vert
    // meme si le code produisait en plus une etape parasite.
    expect(etapes).toHaveLength(1)
    expect(etapes[0]?.brut).toBe('[(50,01113) Klaw] would deal 2 damage')
  })

  it('ne fait pas d etape d une narration deja mise en phrase ailleurs', () => {
    // Le type `text` sans `brut` est la narration interne du moteur : elle a sa
    // place dans le journal, pas dans un deroule qu'on lit etape par etape.
    const etapes = etapesDeroule([], [
      entree({ cle: 'c3', type: 'text', phase: 'Reveal Encounter Cards', titre: 'Main scheme phase start' }),
    ], 1)
    expect(etapes).toEqual([])
  })

  it('marque la narration technique comme defilant seule', () => {
    const etapes = etapesDeroule([], [
      entree({ cle: 'c9', type: 'text', phase: 'Reveal Encounter Cards', titre: '', brut: '[(50,01113) Klaw] would deal 2 damage' }),
    ], 1)
    expect(etapes[0]?.auto).toBe(true)
  })

  it('ne fait pas defiler seule une carte revelee', () => {
    const etapes = etapesDeroule([], [
      entree({ cle: 'c8', type: 'card', phase: 'Reveal Encounter Cards', titre: 'Icy Grip revelee', cibleId: 77 }),
    ], 1)
    expect(etapes[0]?.auto).toBeFalsy()
  })

  describe('le round', () => {
    // L'historique accumule TOUTE la partie, pas seulement la phase en cours.
    // Sans filtre, la phase du round 4 ferait revoir les cartes des rounds
    // precedents. Et il empile la plus recente EN TETE : sans inversion, ces
    // vieilles cartes s'afficheraient en plus a l'envers.
    const journalTroisRounds: EntreeHistorique[] = [
      // Le plus recent d'abord, comme le fait vraiment historique.entrees.
      entree({ cle: 'r3-b', round: 3, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R3-B', cibleId: 3 }),
      entree({ cle: 'r3-a', round: 3, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R3-A', cibleId: 2 }),
      entree({ cle: 'r2', round: 2, type: 'card', phase: 'Reveal Encounter Cards', titre: 'Carte R2', cibleId: 1 }),
      entree({ cle: 'r1', round: 1, type: 'threat', phase: 'Main Scheme Place Threat', titre: 'Menace R1' }),
    ]

    it('ne rend que les etapes du round demande', () => {
      const etapes = etapesDeroule([], journalTroisRounds, 3)
      expect(etapes.map((e) => e.titre)).toEqual(['Carte R3-A', 'Carte R3-B'])
    })

    it('rend ces etapes dans l ordre chronologique, pas l ordre du journal', () => {
      // Le journal les stocke la plus recente en tete (r3-b avant r3-a) : le
      // deroule doit les montrer dans l'ordre ou elles ont eu lieu.
      const etapes = etapesDeroule([], journalTroisRounds, 3)
      expect(etapes.map((e) => e.cle)).toEqual(['carte:r3-a', 'carte:r3-b'])
    })

    it('ne melange pas un autre round dans le decompte', () => {
      const etapes1 = etapesDeroule([], journalTroisRounds, 1)
      expect(etapes1.map((e) => e.titre)).toEqual(['menace'])
      const etapes2 = etapesDeroule([], journalTroisRounds, 2)
      expect(etapes2.map((e) => e.titre)).toEqual(['Carte R2'])
    })

    // Defaut 2 (voir brief) : les FAITS ne portaient aucun round, seul le
    // journal etait filtre. Le cartouche rouvrait donc au round suivant, en
    // plein tour du joueur, sur une manigance deja vaincue.
    it('ne rend que les faits du round demande', () => {
      const faitsDeuxRounds = [
        attaque({ round_id: 1, auteur: 'Ultron', auteur_id: 50 }),
        attaque({ round_id: 2, auteur: 'Drone', auteur_id: 60 }),
      ]
      const etapes = etapesDeroule(faitsDeuxRounds, [], 2)
      const activations = etapes.filter((e) => e.temps === 'activations')
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
      const etapes1 = etapesDeroule([faitSansRound], [], 1)
      const etapes5 = etapesDeroule([faitSansRound], [], 5)
      expect(etapes1.filter((e) => e.temps === 'activations')).toHaveLength(1)
      expect(etapes5.filter((e) => e.temps === 'activations')).toHaveLength(1)
    })
  })
})
