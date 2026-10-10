// UNE CARTE, PLUSIEURS EFFETS AU CHOIX (signalé en jeu le 10/10/2026, Tower
// Defense) : l'Interruption forcée de Proxima Midnight (21092) demande « 1 dégât
// à la tour des Avengers » OU « +2 ATQ pour cette attaque ». Le cartouche posait
// deux vignettes identiques de Proxima, le même texte de carte sous chacune, et
// « Proxima Minuit peut réagir » : rien ne disait quel clic faisait quoi. Même
// rendu attendu en « Étape par étape » et en « Étape par étape Bis ».
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render } from '@testing-library/react'
import { CartouchePhase, type CartouchePhaseProps } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'
import type { ScanCardProps } from '../components/ScanCard'
import type { Demande, Option } from './ask'
import type { Interaction } from './interaction'
import type { QuestionDuMoteur } from './sous-cadre'
import type { WorldCard } from './world'

class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeEach(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})
afterEach(() => cleanup())

const PROXIMA = 56
const SPIDER = 12
const TOUR = 84

const scan = (id: number): ScanCardProps => ({ id: String(id), name: `carte ${id}`, kind: 'villain', imageUrl: `/scan/${id}` })

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
  card_type: 'Villain',
  cost: 0,
  resources: [],
  ...extra,
})

const CARTES = new Map<number, WorldCard>([
  [PROXIMA, carte(PROXIMA, 'Proxima Midnight', { info: { attack: 2 } })],
  [SPIDER, carte(SPIDER, 'Spider-Man', { card_type: 'Hero', info: { defense: 3 } })],
  [TOUR, carte(TOUR, 'Avengers Tower', { card_type: 'Environment' })],
])
const NOMS_FR: Record<number, string> = { [PROXIMA]: 'Proxima Minuit', [SPIDER]: 'Spider-Man', [TOUR]: 'Tour des Avengers' }

const option = (id: number, name: string, extra: Partial<Option> = {}): Option => ({
  id,
  name,
  bind_id: PROXIMA,
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

// Ce que le moteur envoie (get_ask, 10/10/2026) : deux options portées par Proxima.
const versLaTour = option(1, 'deal_1_damage_to_Avengers_Tower', { all_legal_targets: [TOUR], target_num_range: [1, 1] })
const plusDeux = option(2, 'Proxima_Midnight_gets_+2_ATK_for_this_attack')
const demande: Demande = {
  options: [versLaTour, plusDeux],
  refus: [],
  prompt_text: '',
  event_name: 'WhenPlayerChooseAbility',
  show_cancel: false,
  ability_type: 'ForcedInterrupt',
}

const interaction = (): Interaction => ({
  cibles: [],
  ressources: [],
  options: demande.options,
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
  assistant: {
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
  },
  choisirOption: vi.fn(),
  abandonnerOption: vi.fn(),
  valider: vi.fn(),
  annuler: vi.fn(),
  paiementAutoChoix: 'pas-demande',
  basculerPaiementAuto: vi.fn(),
})

const question = (): QuestionDuMoteur => ({
  demande,
  interaction: interaction(),
  cartesParId: CARTES,
  choisirOption: vi.fn(),
  survolerOption: vi.fn(),
  nomPorteur: (id) => NOMS_FR[id],
  // Le texte complet de la carte : c'est lui qui se répétait sous chaque vignette.
  texteCapacite: () => '★ Interruption forcée : quand Proxima Minuit vous attaque, choisissez : soit…',
  estEnMain: () => false,
  carteScene: scan,
})

const attaque: EtapeDeroule = {
  cle: 'activation:4',
  temps: 'mechant',
  titre: 'attaque',
  regle: '',
  etat: 'annonce',
  carteId: PROXIMA,
  cibleId: SPIDER,
  auteurNom: 'Proxima Minuit',
  cibleNom: 'Spider-Man',
  valeurAnnoncee: 2,
  boosts: [],
}

function monter(bis: boolean) {
  const q = question()
  const props: CartouchePhaseProps = {
    refCartouche: () => {},
    gestes: { onPointerDown: () => {}, onPointerMove: () => {}, onPointerUp: () => {}, onPointerCancel: () => {} },
    etape: attaque,
    etapes: [attaque],
    index: 0,
    efface: false,
    questionAuJoueur: true,
    questionDuMoteur: q,
    avancer: vi.fn(),
    enAttente: false,
    attendUnAutreJoueur: false,
    defaiteLocale: false,
    boostsMontres: 99,
    tempsParDecision: 0,
    cartesDistribuees: 0,
    carteScene: scan,
    pvMaxParNom: new Map([['Spider-Man', 10]]),
    bis,
  }
  render(<CartouchePhase {...props} />)
  return q
}

const choix = () => [...document.querySelectorAll<HTMLButtonElement>('button[data-choix]')]

describe.each([
  ['Étape par étape', false],
  ['Étape par étape Bis', true],
])('%s : Proxima Minuit propose deux effets', (_mode, bis) => {
  it('un bouton par effet, nommé par ce qu’il fait', () => {
    monter(bis)
    expect(choix().map((b) => b.getAttribute('aria-label'))).toEqual([
      'Infliger 1 dégât à la tour des Avengers',
      'Proxima Minuit gagne +2 ATQ pour cette attaque',
    ])
  })

  it('ni la carte ni son texte répétés sous chaque bouton', () => {
    monter(bis)
    for (const bouton of choix()) {
      expect(bouton.querySelector('.deroule-vignette-carte')).toBeNull()
      expect(bouton.textContent).not.toContain('Interruption forcée')
    }
  })

  it('« choisis un effet » : une interruption forcée ne « peut » pas réagir', () => {
    monter(bis)
    const texte = document.body.textContent ?? ''
    expect(texte).toContain('Proxima Minuit : choisis un effet')
    expect(texte).not.toContain('peut réagir')
  })

  it('les boutons d\u2019effet forment une colonne de même hauteur', () => {
    monter(bis)
    const conteneur = choix()[0]!.parentElement!
    expect(conteneur.classList.contains('est-textes')).toBe(true)
    for (const bouton of choix()) expect(bouton.classList.contains('est-texte')).toBe(true)
  })

  it('le numéro et le libellé sont deux voisins du même bouton', () => {
    monter(bis)
    for (const bouton of choix()) {
      const enfants = [...bouton.children].map((e) => e.className)
      expect(enfants.slice(0, 2)).toEqual(['deroule-chiffre', 'deroule-choix-nom'])
    }
  })

  it('pendant le choix, les cartes du panneau restent en couleur', () => {
    monter(bis)
    expect(document.querySelector('.deroule-rangee.est-grisee, .deroule-revelee.est-grisee')).toBeNull()
    expect(document.querySelector('.deroule-rangee')).not.toBeNull()
  })

  it('chaque clic active SON effet', () => {
    const q = monter(bis)
    fireEvent.click(choix()[1]!)
    expect(q.choisirOption).toHaveBeenCalledWith(plusDeux)
  })
})
