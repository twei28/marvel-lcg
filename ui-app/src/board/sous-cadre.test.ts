// LE SOUS-CADRE DU CARTOUCHE DU BAS (decisions D4 a D8, D18, D31, D32 du
// 04/10/2026) : la question du moteur, mise en DONNEES. Le composant n'a plus
// qu'a dessiner et a appeler `q.choisirOption`, `interaction.valider()`,
// `interaction.annuler()` ou `agir` d'une carte.
import { describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import type { Demande, Option } from './ask'
import type { EtapeDeroule } from './deroule-phase'
import type { AssistantInteraction, EtatInteractif, Interaction } from './interaction'
import { phraseDeReaction } from './DemandeCentrale'
import { titreReponse, vueSousCadre, type QuestionDuMoteur } from './sous-cadre'
import type { WorldCard } from './world'

const carte = (id: number, name: string, extra: Partial<WorldCard> = {}): WorldCard => ({
  id,
  is_ready: true,
  is_face_up: true,
  visible_for_players: [],
  bind_object_id: 0,
  name,
  info: {},
  traits: {},
  buffs: {},
  card_id: `c${id}`,
  pic_id: `c${id}`,
  down_card_ids: [],
  card_type: 'Hero',
  cost: 0,
  resources: [],
  ...extra,
})

const CARTES = new Map<number, WorldCard>([
  [12, carte(12, 'Rhino', { card_type: 'Villain', info: { attack: 2 } })],
  [40, carte(40, 'Spider-Man', { info: { defense: 3 } })],
  [41, carte(41, 'Black Widow', { card_type: 'Ally', info: { defense: 1 } })],
  [50, carte(50, 'Hulk', { card_type: 'Ally' })],
  [90, carte(90, 'Backflip', { card_type: 'Event' })],
  [91, carte(91, 'Energy', { card_type: 'Resource' })],
])

const NOMS_FR: Record<number, string> = { 40: 'Spider-Man', 41: 'Black Widow', 50: 'Hulk', 90: 'Backflip', 12: 'Rhino' }

const TEXTES: Record<string, string> = {
  'Spider-Sense': '« Sens d’Araignée » \u2014 Interruption : quand un ennemi attaque Spider-Man, il gagne 1 DÉF.',
  Response: 'Response: Deal 1 damage to an enemy.',
  Play: 'Interruption : quand tu devrais subir des dégâts, annule-les.',
}

const option = (id: number, name: string, bind_id: number, extra: Partial<Option> = {}): Option => ({
  id,
  name,
  bind_id,
  bind_player_id: 0,
  all_legal_targets: [],
  target_num_range: [0, 0],
  target_payment: {},
  select_rule: '',
  target_must_include_traits: [],
  failure_reason: '',
  is_search: false,
  ...extra,
})

const demande = (options: Option[], extra: Partial<Demande> = {}): Demande => ({
  options,
  refus: [],
  prompt_text: '',
  event_name: 'WhenUnitBeingAttack',
  show_cancel: true,
  ability_type: 'Interrupt',
  ...extra,
})

const assistant = (extra: Partial<AssistantInteraction> = {}): AssistantInteraction => ({
  etape: 'action',
  titre: '',
  cibleMinimum: 0,
  cibleMaximum: 0,
  cibleNombre: 0,
  ciblePossibles: 0,
  cibleRepetable: false,
  coutPaye: 0,
  coutSlots: [],
  coutRegles: [],
  ...extra,
})

const interaction = (options: Option[], extra: Partial<Interaction> = {}): Interaction => ({
  cibles: [],
  ressources: [],
  options,
  defocaliser: vi.fn(),
  focaliserCarte: vi.fn(),
  focaliserCible: vi.fn(),
  cartes: new Map(),
  ciblesHorsTable: [],
  raison: '',
  prete: false,
  coutAffiche: '',
  surpaiementRecompense: false,
  ciblesRestantes: 0,
  assistant: assistant(),
  choisirOption: vi.fn(),
  abandonnerOption: vi.fn(),
  valider: vi.fn(),
  annuler: vi.fn(),
  paiementAutoChoix: 'pas-demande',
  basculerPaiementAuto: vi.fn(),
  ...extra,
})

const scan = (id: number): ScanCardProps => ({ id: String(id), name: CARTES.get(id)?.name ?? `#${id}`, kind: 'unknown', imageUrl: `scan/${id}.jpg` })

const question = (d: Demande, i: Interaction = interaction(d.options), extra: Partial<QuestionDuMoteur> = {}): QuestionDuMoteur => ({
  demande: d,
  interaction: i,
  cartesParId: CARTES,
  choisirOption: vi.fn(),
  survolerOption: vi.fn(),
  nomPorteur: (id) => NOMS_FR[id],
  texteCapacite: (o) => TEXTES[o.name],
  estEnMain: (id) => id === 90,
  carteScene: (id) => scan(id),
  ...extra,
})

const defenseSM = option(1, 'Defense', 40, { all_legal_targets: [12], target_num_range: [1, 1] })
const defenseBW = option(2, 'Defense', 41, { all_legal_targets: [12], target_num_range: [1, 1] })
const sensAraignee = option(3, 'Spider-Sense', 40)

describe('D7 : la question de defense', () => {
  it('donne la rangee de defense, MEME si la demande est une fenetre de reaction (piege 35)', () => {
    const q = question(demande([defenseSM, defenseBW, sensAraignee]), undefined, { ligneSansDefense: 'ATQ 2 + 1 carte boost' })
    const vue = vueSousCadre(q, {})
    expect(vue.genre).toBe('defense')
    if (vue.genre !== 'defense') return
    expect(vue.attaquantId).toBe(12)
    expect(vue.defenseurs.map((d) => [d.optionId, d.chiffre, d.nom, d.carteId])).toEqual([
      [1, 1, 'Défendre avec Spider-Man (DÉF 3)', 40],
      [2, 2, 'Défendre avec Black Widow (DÉF 1)', 41],
    ])
    expect(vue.defenseurs[0]?.scan?.id).toBe('40')
    // La capacite offerte dans la meme demande suit, numerotee a la suite.
    expect(vue.autres.map((a) => [a.optionId, a.chiffre, a.nom])).toEqual([[3, 3, 'Sens d’Araignée']])
    expect(vue.refus).toBe('Ne pas défendre (ATQ 2 + 1 carte boost)')
  })

  it('sans detail d attaque connu, le refus se dit seul', () => {
    const vue = vueSousCadre(question(demande([defenseSM])), {})
    expect(vue.genre === 'defense' && vue.refus).toBe('Ne pas défendre')
  })

  it('une option indisponible garde son numero et dit pourquoi', () => {
    const vue = vueSousCadre(question(demande([{ ...defenseSM, failure_reason: 'Exhausted' }, defenseBW])), {})
    expect(vue.genre === 'defense' && vue.defenseurs.map((d) => [d.chiffre, d.indisponible])).toEqual([
      [1, 'Exhausted'],
      [2, undefined],
    ])
  })
})

describe('D8 : pendant la defense, les cartes jouables dans la rangee', () => {
  const annonce: EtapeDeroule = {
    cle: 'activation:3', temps: 'mechant', titre: 'attaque', etat: 'annonce', regle: '', boosts: [],
    carteId: 12, cibleId: 40, defenseurId: 40,
  }
  const backflip = option(4, 'Play', 90)

  it('le defenseur est connu : pendant-defense, refus « Continuer sans rien jouer »', () => {
    const vue = vueSousCadre(question(demande([backflip], { event_name: 'WhenDamage' })), { etape: annonce })
    expect(vue.genre).toBe('pendant-defense')
    if (vue.genre !== 'pendant-defense') return
    expect(vue.options.map((o) => [o.optionId, o.chiffre, o.nom, o.carteId])).toEqual([[4, 1, 'Backflip', 90]])
    expect(vue.refus).toBe('Continuer sans rien jouer')
  })

  it('sans defenseur connu (fait boosts absent) : le sous-cadre des reponses', () => {
    const vue = vueSousCadre(question(demande([backflip], { event_name: 'WhenDamage' })), {
      etape: { ...annonce, defenseurId: undefined },
    })
    expect(vue.genre).toBe('reponses')
  })
})

describe('D4, D31, D32 : les reponses dans le sous-cadre', () => {
  it('une seule reponse : nom de la capacite et son texte FR, refus « Ne pas utiliser … »', () => {
    const vue = vueSousCadre(question(demande([sensAraignee])), {})
    expect(vue.genre).toBe('reponses')
    if (vue.genre !== 'reponses') return
    expect(vue.titre).toBe('Sens d’Araignée · quand un ennemi attaque Spider-Man, il gagne 1 DÉF.')
    // Le titre porte deja le texte : le redire sous la vignette l'ecrivait
    // deux fois (planche du lot 6, etat 11a).
    expect(vue.choix.map((c) => [c.optionId, c.chiffre, c.nom, c.sousTexte])).toEqual([
      [3, 1, 'Sens d’Araignée', undefined],
    ])
    expect(vue.refus).toBe('Ne pas utiliser Sens d’Araignée')
  })

  it('une carte en main : « Ne pas jouer … »', () => {
    const vue = vueSousCadre(question(demande([option(4, 'Play', 90)], { event_name: 'WhenDamage' })), {})
    expect(vue.genre === 'reponses' && vue.refus).toBe('Ne pas jouer Backflip')
  })

  it('plusieurs reponses possibles : une vignette chacune, « Aucune réponse »', () => {
    const hulk = option(5, 'Response', 50)
    const vue = vueSousCadre(question(demande([sensAraignee, hulk], { ability_type: 'Response', event_name: 'AfterDamage' })), {})
    expect(vue.genre).toBe('reponses')
    if (vue.genre !== 'reponses') return
    expect(vue.choix.map((c) => c.chiffre)).toEqual([1, 2])
    // Plusieurs reponses : chacune garde son texte dessous (D32).
    expect(vue.choix[0]?.sousTexte).toBe('quand un ennemi attaque Spider-Man, il gagne 1 DÉF.')
    expect(vue.refus).toBe('Aucune réponse')
  })

  it('une question forcee (sans refus possible) n offre aucun refus', () => {
    const vue = vueSousCadre(question(demande([sensAraignee], { show_cancel: false })), {})
    expect(vue.genre === 'reponses' && vue.refus).toBeUndefined()
  })
})

describe('D31 : titreReponse, le nom de la carte d abord', () => {
  it('capacite sans nom propre : « Réponse de Hulk », puis le texte du moteur quand il n y a pas de francais', () => {
    const hulk = option(5, 'Response', 50)
    const q = question(demande([hulk], { ability_type: 'Response' }))
    expect(titreReponse(hulk, q)).toBe('Réponse de Hulk · Deal 1 damage to an enemy.')
  })

  it('« Interruption de X » pour une interruption', () => {
    const backflip = option(4, 'Play', 90)
    expect(titreReponse(backflip, question(demande([backflip])))).toBe(
      'Interruption de Backflip · quand tu devrais subir des dégâts, annule-les.'
    )
  })

  it('sans texte du tout : le nom seul', () => {
    const muet = option(6, 'Response', 50)
    const q = question(demande([muet], { ability_type: 'Response' }), undefined, { texteCapacite: () => undefined })
    expect(titreReponse(muet, q)).toBe('Réponse de Hulk')
  })
})

describe('D18 : le choix pose par une carte revelee', () => {
  it('se lit a droite de la carte, pas dans un sous-cadre', () => {
    const subir = option(7, 'Take_2_damage', 0)
    const defausser = option(8, 'Discard_2_cards', 0)
    const d = demande([subir, defausser], {
      event_name: 'WhenPlayerChooseAbility',
      ability_type: 'Normal',
      prompt_text: 'Chantage : choisis',
      show_cancel: false,
    })
    const vue = vueSousCadre(question(d), { tempsQuestion: 'revelation' })
    expect(vue.genre).toBe('choix-carte')
    if (vue.genre !== 'choix-carte') return
    expect(vue.intitule).toBe('Chantage : choisis')
    expect(vue.choix.map((c) => [c.optionId, c.chiffre])).toEqual([[7, 1], [8, 2]])
    expect(vue.refus).toBeUndefined()
    // Le meme choix hors des cartes rencontre : le sous-cadre des reponses.
    expect(vueSousCadre(question(d), { tempsQuestion: 'mechant' }).genre).toBe('reponses')
  })

  // Planche du lot 4, etat 10 (Poseur de Bombe d'Hydra, 01110) : les deux
  // choix portent la carte REVELEE (`bind_id`) ; les nommer par leur porteur
  // ecrivait deux fois « Poseur de Bombe d'Hydra » sous deux fois la meme
  // carte, et le joueur ne savait plus lequel subissait les degats.
  it('chaque choix se dit par son texte, sans la carte qui le porte (la carte est deja en grand)', () => {
    const subir = option(7, 'Take_2_damage', 50)
    const placer = option(8, 'Place_1_threat_on_the_main_scheme', 50)
    const d = demande([subir, placer], { event_name: 'WhenPlayerChooseAbility', ability_type: 'Normal', show_cancel: false })
    const vue = vueSousCadre(question(d), { tempsQuestion: 'revelation' })
    expect(vue.genre).toBe('choix-carte')
    if (vue.genre !== 'choix-carte') return
    expect(vue.choix.map((c) => [c.chiffre, c.nom, c.scan])).toEqual([
      [1, 'Subir 2 dégâts', undefined],
      [2, 'Placer 1 menace sur la manigance principale', undefined],
    ])
  })
})

// Signalé en jeu le 10/10/2026 (Tower Defense) : l'Interruption forcée de
// Proxima Midnight (21092) posait deux vignettes identiques de Proxima, avec
// le même texte de carte, sous « Proxima Minuit peut réagir ».
describe('une carte qui propose plusieurs effets au choix', () => {
  const proxima = carte(60, 'Proxima Midnight', { card_type: 'Villain' })
  const cartes = new Map(CARTES).set(60, proxima)
  const tour = option(11, 'deal 1 damage to Avengers Tower', 60)
  const atq = option(12, 'Proxima Midnight gets +2 ATK for this attack', 60)
  const d = demande([tour, atq], {
    event_name: 'WhenPlayerChooseAbility',
    ability_type: 'ForcedInterrupt',
    show_cancel: false,
  })
  const q = question(d, interaction(d.options), {
    cartesParId: cartes,
    nomPorteur: (id) => (id === 60 ? 'Proxima Minuit' : NOMS_FR[id]),
  })

  it('un bouton par effet, nommé par son texte, sans répéter la carte', () => {
    const vue = vueSousCadre(q, { tempsQuestion: 'mechant' })
    expect(vue.genre).toBe('choix-carte')
    if (vue.genre !== 'choix-carte') return
    expect(vue.intitule).toBe('Proxima Minuit : choisis un effet')
    expect(vue.choix.map((c) => [c.chiffre, c.nom, c.scan, c.sousTexte])).toEqual([
      [1, 'Infliger 1 dégât à la tour des Avengers', undefined, undefined],
      [2, 'Proxima Minuit gagne +2 ATQ pour cette attaque', undefined, undefined],
    ])
    // Interruption forcée : rien à refuser.
    expect(vue.refus).toBeUndefined()
  })

  it('une capacité forcée ne « peut » pas réagir : elle choisit un effet', () => {
    const noms = (id: number) => (id === 60 ? 'Proxima Minuit' : undefined)
    expect(phraseDeReaction([tour, atq], cartes, noms, true)).toBe('Proxima Minuit : choisis un effet')
    expect(phraseDeReaction([tour, atq], cartes, noms)).toBe('Proxima Minuit peut réagir')
  })

  it('des options de cartes différentes restent des réponses', () => {
    const autre = option(13, 'Response', 50)
    const vue = vueSousCadre(question(demande([tour, autre], { event_name: 'WhenPlayerChooseAbility' }), undefined, { cartesParId: cartes }), {
      tempsQuestion: 'mechant',
    })
    expect(vue.genre).toBe('reponses')
  })
})

describe('D5 : le ciblage dans le sous-cadre', () => {
  it('cibles de la table et hors table, choisies, compteur, pret', () => {
    const explosion = option(9, 'Response', 50, { all_legal_targets: [12, 41], target_num_range: [1, 2] })
    const cartes = new Map<number, EtatInteractif>([
      [12, { role: 'cible', choisie: true, fois: 1, agir: vi.fn() }],
      [41, { role: 'cible', choisie: false, agir: vi.fn() }],
      [50, { role: 'porteur', choisie: false }],
    ])
    const i = interaction([explosion], {
      option: explosion,
      cibles: [12],
      cartes,
      ciblesHorsTable: [{ props: { id: '200', name: 'Carte du deck', kind: 'unknown', imageUrl: '' }, choisie: false, agir: vi.fn() }],
      raison: 'Choisis encore 1 cible',
      prete: false,
      assistant: assistant({ etape: 'target', cibleMinimum: 1, cibleMaximum: 2 }),
    })
    const vue = vueSousCadre(question(demande([explosion], { ability_type: 'Response' }), i), {})
    expect(vue.genre).toBe('cibles')
    if (vue.genre !== 'cibles') return
    expect(vue.cibles.map((c) => [c.carteId, c.choisie, c.horsTable, c.fois])).toEqual([
      [12, true, false, 1],
      [41, false, false, undefined],
      [200, false, true, undefined],
    ])
    expect(vue.cibles[0]?.nom).toBe('Rhino')
    expect([vue.choisies, vue.minimum, vue.maximum, vue.prete, vue.raison]).toEqual([1, 1, 2, false, 'Choisis encore 1 cible'])
    expect(vue.titre).toBe('Réponse de Hulk · Deal 1 damage to an enemy.')
  })
})

describe('D6 : le paiement dans le sous-cadre', () => {
  it('les cartes au role ressource seulement, les pastilles du cout, « Jouer X »', () => {
    const backflip = option(4, 'Play', 90, { target_payment: { 0: { cost: '1', payment: [], rule: [] } } })
    const cartes = new Map<number, EtatInteractif>([
      [90, { role: 'porteur', choisie: false }],
      [91, { role: 'ressource', choisie: false, pulse: true, agir: vi.fn() }],
      [41, { role: 'ressource', choisie: true, fois: 1, agir: vi.fn() }],
      [12, { role: 'indisponible', choisie: false }],
    ])
    const i = interaction([backflip], {
      option: backflip,
      cartes,
      prete: false,
      assistant: assistant({
        etape: 'payment',
        titre: 'Payer 1',
        detail: '0 / 1 payé',
        coutRequis: 1,
        coutSlots: [{ index: 0, rempli: false }],
      }),
    })
    const vue = vueSousCadre(question(demande([backflip]), i), {})
    expect(vue.genre).toBe('paiement')
    if (vue.genre !== 'paiement') return
    expect(vue.cartesMain.map((c) => [c.carteId, c.choisie, c.pulse])).toEqual([
      [91, false, true],
      [41, true, undefined],
    ])
    expect(vue.coutSlots).toEqual([{ index: 0, rempli: false }])
    expect([vue.consigne, vue.phraseEtat, vue.prete, vue.libelleJouer]).toEqual(['Payer 1', '0 / 1 payé', false, 'Jouer Backflip'])
  })

  it('a la confirmation : « Confirmer », pret ou non', () => {
    const backflip = option(4, 'Play', 90)
    const i = interaction([backflip], { option: backflip, prete: true, assistant: assistant({ etape: 'confirm' }) })
    const vue = vueSousCadre(question(demande([backflip]), i), {})
    expect(vue).toMatchObject({ genre: 'confirmer', prete: true, raison: '' })
  })
})

describe('l ordre d activation des sbires (forced, pas de refus)', () => {
  const ordre = option(10, 'Minion_Activates_Order', 0, { all_legal_targets: [60, 61], target_num_range: [2, 2] })
  const d = demande([ordre], { show_cancel: false, ability_type: 'Normal', event_name: 'WhenChooseOrder' })

  it('option engagee : « Choisir l’ordre », les sbires numerotes dans l ordre de clic', () => {
    const cartes = new Map<number, EtatInteractif>([
      [60, { role: 'cible', choisie: true, ordre: 1, agir: vi.fn() }],
      [61, { role: 'cible', choisie: false, agir: vi.fn() }],
    ])
    const i = interaction([ordre], { option: ordre, cibles: [60], cartes, assistant: assistant({ etape: 'target' }) })
    const vue = vueSousCadre(question(d, i), {})
    expect(vue.genre).toBe('ordre')
    if (vue.genre !== 'ordre') return
    expect(vue.titre).toBe('Choisir l’ordre')
    expect(vue.cibles.map((c) => [c.carteId, c.ordre])).toEqual([[60, 1], [61, undefined]])
    expect(vue.prete).toBe(false)
  })

  it('pas encore engagee : les memes sbires, aucun choisi', () => {
    const vue = vueSousCadre(question(d), {})
    expect(vue.genre === 'ordre' && vue.cibles.map((c) => [c.carteId, c.choisie])).toEqual([[60, false], [61, false]])
  })
})

describe('lot 6 : l ordre des JOUEURS (activations simultanees, decision 47)', () => {
  const ordre = option(11, 'Players_Activation_Order', 0, { all_legal_targets: [1, 2], target_num_range: [2, 2] })
  const d = demande([ordre], { show_cancel: false, ability_type: 'Normal', event_name: 'WhenChooseOrder' })

  it('la meme rangee a ordonner, titree pour les joueurs', () => {
    const vue = vueSousCadre(question(d), {})
    expect(vue.genre).toBe('ordre')
    if (vue.genre !== 'ordre') return
    expect(vue.titre).toBe('Choisis l’ordre des joueurs')
    expect(vue.cibles.map((c) => c.carteId)).toEqual([1, 2])
  })
})

describe('les donnees seules : aucune closure dans la vue', () => {
  it('JSON aller-retour egale la vue', () => {
    const vue = vueSousCadre(question(demande([defenseSM, defenseBW, sensAraignee])), {})
    expect(JSON.parse(JSON.stringify(vue))).toEqual(vue)
  })
})
