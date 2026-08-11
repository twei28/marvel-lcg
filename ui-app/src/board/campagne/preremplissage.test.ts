// L'ordre des sources est la seule chose que ce fichier protege, et c'est la
// seule chose qui compte : une suggestion du moteur DOIT battre un detecteur,
// parce que le moteur connait son propre etat et que le detecteur le redevine.
// Sauf si elle vient d'un AUTRE scenario : le moteur n'efface jamais son
// carnet sortant, donc une estampille absente ou differente doit tout ignorer.
import { describe, expect, it } from 'vitest'
import type { World } from '../world'
import type { ChampVictoire } from './detecteurs'
import { assainirCarnet, preRemplir } from './preremplissage'

const CHAMP_AUTO: ChampVictoire = {
  cle: 'Tech Upgrade',
  type: 'auto',
  format: 'liste',
  detection: 'cartes_en_jeu',
  options: ['04155'],
  libelle: 'Amélioration technologique',
}

const CHAMP_CHOIX: ChampVictoire = {
  cle: 'Weapon',
  type: 'choix',
  format: 'liste',
  libelle: 'Arme',
}

/** Un drapeau côté moteur : auto, format int, sans détecteur (les 9 clés de mts.json). */
const CHAMP_DRAPEAU: ChampVictoire = {
  cle: 'Campaign Pool: Cosmo',
  type: 'auto',
  format: 'int',
  libelle: 'Cosmo rallié',
}

/** Un vrai compteur côté moteur : auto, format int, AVEC détecteur. 0 y est légitime. */
const CHAMP_COMPTEUR: ChampVictoire = {
  cle: 'Remaining hit points',
  parJoueur: true,
  type: 'auto',
  format: 'int',
  detection: 'pv_restants',
  libelle: 'PV restants',
}

/** Monde minimal : 04155 en jeu, un héros vivant, ce qui suffit aux détecteurs. */
const monde = (): World =>
  ({
    area_schemes_side: [
      { id: 1, card_id: '04155', card_type: 'Upgrade', name: '04155', bind_object_id: 0 },
    ],
    players: [
      {
        is_eliminated: false,
        area_hero: [
          {
            id: 2,
            card_id: '03001b',
            card_type: 'AlterEgo',
            name: 'hero',
            bind_object_id: 0,
            info: { health: 11, max_health: 11 },
          },
        ],
      },
    ],
  }) as unknown as World

/** Monde à deux joueurs, tous deux vivants. */
const mondeDeuxJoueurs = (): World =>
  ({
    area_schemes_side: [
      { id: 1, card_id: '04155', card_type: 'Upgrade', name: '04155', bind_object_id: 0 },
    ],
    players: [
      {
        is_eliminated: false,
        area_hero: [
          {
            id: 2,
            card_id: '03001b',
            card_type: 'AlterEgo',
            name: 'hero1',
            bind_object_id: 0,
            info: { health: 11, max_health: 11 },
          },
        ],
      },
      {
        is_eliminated: false,
        area_hero: [
          {
            id: 3,
            card_id: '05001b',
            card_type: 'AlterEgo',
            name: 'hero2',
            bind_object_id: 0,
            info: { health: 9, max_health: 9 },
          },
        ],
      },
    ],
  }) as unknown as World

/** Monde à deux joueurs, le second éliminé. */
const mondeHerosElimine = (): World =>
  ({
    area_schemes_side: [
      { id: 1, card_id: '04155', card_type: 'Upgrade', name: '04155', bind_object_id: 0 },
    ],
    players: [
      {
        is_eliminated: false,
        area_hero: [
          {
            id: 2,
            card_id: '03001b',
            card_type: 'AlterEgo',
            name: 'hero1',
            bind_object_id: 0,
            info: { health: 11, max_health: 11 },
          },
        ],
      },
      {
        is_eliminated: true,
        area_hero: [
          {
            id: 3,
            card_id: '05001b',
            card_type: 'AlterEgo',
            name: 'hero2',
            bind_object_id: 0,
            info: { health: 0, max_health: 9 },
          },
        ],
      },
    ],
  }) as unknown as World

describe('preRemplir', () => {
  it('prend la valeur du moteur quand elle existe et vient du bon scénario', () => {
    const sortie = preRemplir({
      champs: [CHAMP_AUTO],
      monde: monde(),
      suggestions: { 'Tech Upgrade': '04156' },
      scenarioSuggestions: 'ebony_maw',
      scenarioActuel: 'ebony_maw',
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04156')
  })

  it('retombe sur le détecteur quand le moteur ne dit rien', () => {
    const sortie = preRemplir({
      champs: [CHAMP_AUTO],
      monde: monde(),
      suggestions: {},
      scenarioSuggestions: null,
      scenarioActuel: 'ebony_maw',
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04155')
  })

  it('retombe sur le carnet existant quand ni moteur ni détecteur ne répondent', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, options: ['09999'] }],
      monde: monde(),
      carnet: { 'Tech Upgrade': '04150' },
      suggestions: {},
      scenarioSuggestions: null,
      scenarioActuel: 'ebony_maw',
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04150')
  })

  it('laisse un champ de type choix au joueur, même si le moteur a une valeur', () => {
    const sortie = preRemplir({
      champs: [CHAMP_CHOIX],
      monde: monde(),
      suggestions: { Weapon: '04072' },
      scenarioSuggestions: 'ebony_maw',
      scenarioActuel: 'ebony_maw',
      total: 1,
    })
    expect(sortie.Weapon).toBeUndefined()
  })

  it('préfixe la clé par joueur quand le champ est parJoueur', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, parJoueur: true }],
      monde: monde(),
      suggestions: { 'Player 1 Tech Upgrade': '04157' },
      scenarioSuggestions: 'ebony_maw',
      scenarioActuel: 'ebony_maw',
      total: 1,
    })
    expect(sortie['Player 1 Tech Upgrade']).toBe('04157')
  })

  it("ignore le carnet moteur EN BLOC quand il vient d'un autre scénario (défaut 1)", () => {
    // Un joueur termine "ebony_maw" (mts), le moteur écrit son carnet sortant.
    // Rien ne l'efface : si le joueur enchaîne ensuite sur "crossbones"
    // (trors), ce carnet resterait au fichier et serait présenté comme
    // "relevé par le jeu" pour un scénario qu'il ne concerne pas.
    const sortie = preRemplir({
      champs: [CHAMP_AUTO],
      monde: monde(),
      suggestions: { 'Tech Upgrade': '04156' },
      scenarioSuggestions: 'ebony_maw',
      scenarioActuel: 'crossbones',
      total: 1,
    })
    // Ignoré : on retombe sur le détecteur, pas sur la valeur contaminée.
    expect(sortie['Tech Upgrade']).toBe('04155')
  })

  it('prend le carnet moteur quand son estampille correspond au scénario en cours', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, options: ['09999'] }],
      monde: monde(),
      suggestions: { 'Tech Upgrade': '04156' },
      scenarioSuggestions: 'crossbones',
      scenarioActuel: 'crossbones',
      total: 1,
    })
    expect(sortie['Tech Upgrade']).toBe('04156')
  })

  it('pré-remplit chaque joueur séparément à deux héros', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, parJoueur: true }],
      monde: mondeDeuxJoueurs(),
      suggestions: { 'Player 1 Tech Upgrade': '04157', 'Player 2 Tech Upgrade': '04158' },
      scenarioSuggestions: 'ebony_maw',
      scenarioActuel: 'ebony_maw',
      total: 2,
    })
    expect(sortie['Player 1 Tech Upgrade']).toBe('04157')
    expect(sortie['Player 2 Tech Upgrade']).toBe('04158')
  })

  it('un héros éliminé ne participe à aucune étape de victoire (livret p17)', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_AUTO, parJoueur: true }],
      monde: mondeHerosElimine(),
      suggestions: { 'Player 1 Tech Upgrade': '04157', 'Player 2 Tech Upgrade': '04158' },
      scenarioSuggestions: 'ebony_maw',
      scenarioActuel: 'ebony_maw',
      total: 2,
    })
    expect(sortie['Player 1 Tech Upgrade']).toBe('04157')
    expect(sortie['Player 2 Tech Upgrade']).toBeUndefined()
  })
})

describe('preRemplir — un champ cumulatif (piste de réputation de sm)', () => {
  /**
   * La piste de sm se recalcule à la fin de CHAQUE scénario et s'AJOUTE aux
   * nœuds déjà marqués. Le détecteur rend ce que la partie vient de gagner ; le
   * total, lui, ne peut se faire qu'ici, où le carnet est connu.
   */
  const CHAMP_CUMULATIF: ChampVictoire = {
    cle: 'Reputation Track',
    type: 'auto',
    format: 'int',
    detection: 'conditions_reputation',
    cumulatif: true,
    libelle: 'Piste de Réputation',
  }

  it('ajoute ce que la partie a gagné aux nœuds déjà marqués', () => {
    const sortie = preRemplir({
      champs: [CHAMP_CUMULATIF],
      monde: monde(),
      carnet: { 'Reputation Track': '8' },
      suggestions: {},
      scenarioSuggestions: null,
      scenarioActuel: 'sandman',
      total: 1,
    })
    // Le monde de ce fichier n'a ni sbire, ni annexe, ni menace, ni accélération,
    // ni identité vaincue : cinq conditions, plus rien en pile de victoire.
    expect(sortie['Reputation Track']).toBe('13')
  })

  it('part de zéro quand le carnet est vide', () => {
    const sortie = preRemplir({
      champs: [CHAMP_CUMULATIF],
      monde: monde(),
      suggestions: {},
      scenarioSuggestions: null,
      scenarioActuel: 'sandman',
      total: 1,
    })
    expect(sortie['Reputation Track']).toBe('5')
  })

  it("n'additionne PAS ce que le moteur relève : son collecteur cumule déjà", () => {
    const sortie = preRemplir({
      champs: [CHAMP_CUMULATIF],
      monde: monde(),
      carnet: { 'Reputation Track': '8' },
      suggestions: { 'Reputation Track': '11' },
      scenarioSuggestions: 'sandman',
      scenarioActuel: 'sandman',
      total: 1,
    })
    expect(sortie['Reputation Track']).toBe('11')
  })

  it('ignore un total illisible au carnet plutôt que de rendre NaN', () => {
    const sortie = preRemplir({
      champs: [CHAMP_CUMULATIF],
      monde: monde(),
      carnet: { 'Reputation Track': 'douze' },
      suggestions: {},
      scenarioSuggestions: null,
      scenarioActuel: 'sandman',
      total: 1,
    })
    expect(sortie['Reputation Track']).toBe('5')
  })

  it('un champ NON cumulatif remplace, il n additionne pas', () => {
    const sortie = preRemplir({
      champs: [{ ...CHAMP_CUMULATIF, cumulatif: false }],
      monde: monde(),
      carnet: { 'Reputation Track': '8' },
      suggestions: {},
      scenarioSuggestions: null,
      scenarioActuel: 'sandman',
      total: 1,
    })
    expect(sortie['Reputation Track']).toBe('5')
  })
})

describe('assainirCarnet', () => {
  it('retire un drapeau corrigé à 0 (défaut 3 : "0" reste non vide pour InPool/LogSet)', () => {
    const sortie = assainirCarnet([CHAMP_DRAPEAU], { 'Campaign Pool: Cosmo': '0' }, 1)
    expect(sortie['Campaign Pool: Cosmo']).toBeUndefined()
  })

  it('retire un drapeau laissé vide', () => {
    const sortie = assainirCarnet([CHAMP_DRAPEAU], { 'Campaign Pool: Cosmo': '' }, 1)
    expect(sortie['Campaign Pool: Cosmo']).toBeUndefined()
  })

  it('conserve un drapeau à 1', () => {
    const sortie = assainirCarnet([CHAMP_DRAPEAU], { 'Campaign Pool: Cosmo': '1' }, 1)
    expect(sortie['Campaign Pool: Cosmo']).toBe('1')
  })

  it("conserve un vrai compteur à 0, parce qu'il a un détecteur (0 PV restants est légitime)", () => {
    const sortie = assainirCarnet([CHAMP_COMPTEUR], { 'Player 1 Remaining hit points': '0' }, 1)
    expect(sortie['Player 1 Remaining hit points']).toBe('0')
  })

  it('ne touche pas aux champs qui ne sont pas concernés', () => {
    const sortie = assainirCarnet([CHAMP_AUTO, CHAMP_CHOIX], { 'Tech Upgrade': '04155', Weapon: '04072' }, 1)
    expect(sortie).toEqual({ 'Tech Upgrade': '04155', Weapon: '04072' })
  })
})
