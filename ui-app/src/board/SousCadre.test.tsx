// LE SOUS-CADRE DU CARTOUCHE DU BAS (lot 4 de la refonte du 04/10/2026,
// decisions D4, D5, D6, D31, D32, D37) : ce qu'il dessine, et SURTOUT ce qu'il
// appelle. Il ne retient rien (piege 26) et ne parle jamais au moteur en
// direct (piege 27) : une vignette d'option passe par `q.choisirOption`, une
// cible ou une carte de la main par son `agir`, « Confirmer » et « Jouer » par
// `interaction.valider`, le refus par `interaction.annuler`.
//
// La loupe (D29) est posee sur la section du cartouche, pas ici : ses cas
// vivent dans CartouchePhase.test.tsx.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render } from '@testing-library/react'
import type { ScanCardProps } from '../components/ScanCard'
import type { Demande, Option } from './ask'
import type { AssistantInteraction, EtatInteractif, Interaction } from './interaction'
import { SousCadre } from './SousCadre'
import { vueSousCadre, type QuestionDuMoteur } from './sous-cadre'
import type { WorldCard } from './world'
import { ecran as screen } from '../test-textes'

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
  [12, carte(12, 'Rhino', { card_type: 'Villain' })],
  [40, carte(40, 'Spider-Man')],
  [41, carte(41, 'Black Widow', { card_type: 'Ally' })],
  [50, carte(50, 'Hulk', { card_type: 'Ally' })],
  [60, carte(60, 'Hydra Mercenary', { card_type: 'Minion' })],
  [61, carte(61, 'Shocker', { card_type: 'Minion' })],
  [90, carte(90, 'Backflip', { card_type: 'Event' })],
  [91, carte(91, 'Energy', { card_type: 'Resource' })],
  [92, carte(92, 'Strength', { card_type: 'Resource' })],
])

const TEXTES: Record<string, string> = {
  'Spider-Sense': '« Sens d’Araignée » \u2014 Interruption : quand un ennemi attaque Spider-Man, il gagne 1 DÉF.',
  Response: 'Response: Deal 1 damage to an enemy.',
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
  event_name: 'AfterDamage',
  show_cancel: true,
  ability_type: 'Response',
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

const question = (d: Demande, i: Interaction = interaction(d.options)): QuestionDuMoteur => ({
  demande: d,
  interaction: i,
  cartesParId: CARTES,
  choisirOption: vi.fn(),
  survolerOption: vi.fn(),
  nomPorteur: (id) => CARTES.get(id)?.name,
  texteCapacite: (o) => TEXTES[o.name],
  estEnMain: (id) => id === 90,
  carteScene: (id) => scan(id),
})

function monter(q: QuestionDuMoteur) {
  const vue = vueSousCadre(q, {})
  if (vue.genre === 'defense' || vue.genre === 'pendant-defense') throw new Error(`hors du sous-cadre : ${vue.genre}`)
  return render(<SousCadre vue={vue} q={q} />)
}

const choix = () => [...document.querySelectorAll<HTMLButtonElement>('button.deroule-vignette[data-choix]')]
const refus = () => document.querySelector<HTMLButtonElement>('button.bh-bouton[data-refus]')

afterEach(() => cleanup())

describe('D4, D31, D32 : les reponses', () => {
  const sens = option(3, 'Spider-Sense', 40)
  const hulk = option(5, 'Response', 50)

  it('une vignette par reponse, numerotee, son texte dessous ; un clic la joue', () => {
    const q = question(demande([sens, hulk]))
    monter(q)
    const sous = document.querySelector('.deroule-sous-cadre')
    expect(sous?.classList.contains('est-reponses')).toBe(true)
    expect(choix().map((b) => b.dataset.choix)).toEqual(['1', '2'])
    expect(choix()[0]?.textContent).toContain('(1)')
    expect(choix()[1]?.textContent).toContain('Deal 1 damage to an enemy.')
    fireEvent.click(choix()[1]!)
    expect(q.choisirOption).toHaveBeenCalledWith(hulk)
    expect(q.interaction.annuler).not.toHaveBeenCalled()
  })

  it('« Aucune réponse » a droite est le refus : il annule, sans rien choisir', () => {
    const q = question(demande([sens, hulk]))
    monter(q)
    expect(refus()?.textContent).toBe('Aucune réponse')
    fireEvent.click(refus()!)
    expect(q.interaction.annuler).toHaveBeenCalledTimes(1)
    expect(q.choisirOption).not.toHaveBeenCalled()
  })

  it('une seule reponse : le titre dit le nom de la carte puis son texte (moteur si pas de francais)', () => {
    monter(question(demande([hulk])))
    expect(screen.getByText('Réponse de Hulk · Deal 1 damage to an enemy.')).toBeInTheDocument()
  })

  it('une question forcee n a pas de refus', () => {
    monter(question(demande([sens], { show_cancel: false })))
    expect(refus()).toBeNull()
  })

  it('une option indisponible garde son numero, ne se joue pas, et dit pourquoi', () => {
    const q = question(demande([{ ...sens, failure_reason: 'Exhausted' }, hulk]))
    monter(q)
    const premiere = choix()[0]!
    expect(premiere.getAttribute('aria-disabled')).toBe('true')
    fireEvent.click(premiere)
    expect(q.choisirOption).not.toHaveBeenCalled()
    expect(screen.getByText('Exhausted')).toBeInTheDocument()
  })
})

describe('D5 : le ciblage', () => {
  function ciblage(prete: boolean) {
    const explosion = option(9, 'Response', 50, { all_legal_targets: [12, 41], target_num_range: [1, 2] })
    const agir12 = vi.fn()
    const agir41 = vi.fn()
    const agirHors = vi.fn()
    const cartes = new Map<number, EtatInteractif>([
      [12, { role: 'cible', choisie: true, fois: 1, agir: agir12 }],
      [41, { role: 'cible', choisie: false, agir: agir41 }],
      [50, { role: 'porteur', choisie: false }],
    ])
    const i = interaction([explosion], {
      option: explosion,
      cibles: [12],
      cartes,
      ciblesHorsTable: [{ props: { id: '200', name: 'Carte du deck', kind: 'unknown', imageUrl: '' }, choisie: false, agir: agirHors }],
      raison: 'Choisis encore 1 cible',
      prete,
      assistant: assistant({ etape: 'target', cibleMinimum: 1, cibleMaximum: 2 }),
    })
    const q = question(demande([explosion]), i)
    monter(q)
    return { q, agir12, agir41, agirHors }
  }

  it('les cibles de la table et hors table en vignettes ; un clic agit sur la carte', () => {
    const { agir41, agirHors } = ciblage(false)
    expect(document.querySelector('.deroule-sous-cadre')?.classList.contains('est-cibles')).toBe(true)
    expect(choix()).toHaveLength(3)
    expect(choix()[0]?.getAttribute('aria-pressed')).toBe('true')
    fireEvent.click(choix()[1]!)
    expect(agir41).toHaveBeenCalledTimes(1)
    fireEvent.click(choix()[2]!)
    expect(agirHors).toHaveBeenCalledTimes(1)
    expect(screen.getByText('1 / 2 (min 1)')).toBeInTheDocument()
  })

  it('« Confirmer » attend que la reponse soit prete, puis valide ; « Annuler » annule', () => {
    const { q } = ciblage(false)
    const confirmer = screen.getByRole('button', { name: 'Confirmer' })
    expect(confirmer).toBeDisabled()
    expect(screen.getByText('Choisis encore 1 cible')).toBeInTheDocument()
    fireEvent.click(refus()!)
    expect(refus()?.textContent).toBe('Annuler')
    expect(q.interaction.annuler).toHaveBeenCalledTimes(1)
    cleanup()
    const pret = ciblage(true)
    fireEvent.click(screen.getByRole('button', { name: 'Confirmer' }))
    expect(pret.q.interaction.valider).toHaveBeenCalledTimes(1)
  })
})

describe('D6 : le paiement, avec les cartes de la main', () => {
  function paiement(prete: boolean) {
    const backflip = option(4, 'Play', 90)
    const agir91 = vi.fn()
    const cartes = new Map<number, EtatInteractif>([
      [90, { role: 'porteur', choisie: false }],
      [91, { role: 'ressource', choisie: false, agir: agir91 }],
      [92, { role: 'ressource', choisie: true, fois: 1, agir: vi.fn() }],
      [12, { role: 'indisponible', choisie: false }],
    ])
    const i = interaction([backflip], {
      option: backflip,
      cartes,
      prete,
      assistant: assistant({
        etape: 'payment',
        titre: 'Payer le coût',
        detail: '1/2 payé',
        coutRequis: 2,
        coutSlots: [
          { index: 0, rempli: true, type: 'R' },
          { index: 1, rempli: false },
        ],
      }),
    })
    const q = question(demande([backflip], { ability_type: 'Interrupt' }), i)
    monter(q)
    return { q, agir91 }
  }

  it('les seules cartes qui paient, en vignettes ; un clic les depense', () => {
    const { agir91 } = paiement(false)
    expect(document.querySelector('.deroule-sous-cadre')?.classList.contains('est-paiement')).toBe(true)
    expect(choix().map((b) => b.dataset.carteId)).toEqual(['91', '92'])
    fireEvent.click(choix()[0]!)
    expect(agir91).toHaveBeenCalledTimes(1)
  })

  it('les pastilles du cout se remplissent, « Jouer Backflip » valide quand c est pret', () => {
    paiement(false)
    const pastilles = [...document.querySelectorAll('.deroule-cout-pastille')]
    expect(pastilles).toHaveLength(2)
    expect(pastilles.map((p) => p.classList.contains('est-rempli'))).toEqual([true, false])
    expect(screen.getByText('1/2 payé')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Jouer Backflip' })).toBeDisabled()
    cleanup()
    const { q } = paiement(true)
    fireEvent.click(screen.getByRole('button', { name: 'Jouer Backflip' }))
    expect(q.interaction.valider).toHaveBeenCalledTimes(1)
  })

  it('aucun assistant d action a cote : le sous-cadre porte tout', () => {
    paiement(false)
    expect(document.querySelector('.assistant-action')).toBeNull()
  })
})

describe('l ordre d activation des sbires', () => {
  const ordre = option(10, 'Minion_Activates_Order', 0, { all_legal_targets: [60, 61], target_num_range: [2, 2] })
  const d = demande([ordre], { show_cancel: false, ability_type: 'Normal', event_name: 'WhenChooseOrder' })

  it('« Choisir l’ordre », les numeros d ordre, aucun refus (question forcee)', () => {
    const agir61 = vi.fn()
    const cartes = new Map<number, EtatInteractif>([
      [60, { role: 'cible', choisie: true, ordre: 1, agir: vi.fn() }],
      [61, { role: 'cible', choisie: false, agir: agir61 }],
    ])
    const i = interaction([ordre], { option: ordre, cibles: [60], cartes, assistant: assistant({ etape: 'target' }) })
    monter(question(d, i))
    expect(screen.getByText('Choisir l’ordre')).toBeInTheDocument()
    expect(document.querySelector('.deroule-ordre')?.textContent).toBe('1')
    expect(refus()).toBeNull()
    fireEvent.click(choix()[1]!)
    expect(agir61).toHaveBeenCalledTimes(1)
  })

  it('pas encore engagee : un clic engage l ordre en commencant par ce sbire', () => {
    const q = question(d)
    monter(q)
    fireEvent.click(choix()[1]!)
    expect(q.choisirOption).toHaveBeenCalledWith(ordre, [61])
  })
})

describe('la confirmation', () => {
  it('« Confirmer » valide, « Annuler » annule', () => {
    const backflip = option(4, 'Play', 90)
    const i = interaction([backflip], { option: backflip, prete: true, assistant: assistant({ etape: 'confirm' }) })
    const q = question(demande([backflip], { ability_type: 'Interrupt' }), i)
    monter(q)
    expect(document.querySelector('.deroule-sous-cadre')?.classList.contains('est-confirmer')).toBe(true)
    fireEvent.click(screen.getByRole('button', { name: 'Confirmer' }))
    expect(q.interaction.valider).toHaveBeenCalledTimes(1)
    fireEvent.click(refus()!)
    expect(q.interaction.annuler).toHaveBeenCalledTimes(1)
  })
})
