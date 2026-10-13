// LES PIRES CAS DES QUESTIONS DE LA BOITE (essai, 13/10/2026).
//
// Signale par l'utilisateur : une question a cinq cibles (Maitres du Chaos)
// rognait ses boutons dans la boite de la phase du mechant. Ce fichier monte
// chaque SORTE de question, avec le plus de choix qu'une vraie partie pose (8 cartes en
// main ou 8 cibles, 4 defenseurs : heros et trois allies, 4 reponses) et un long texte, dans la
// vraie boite (CartouchePhase, essai), verifie qu'elle s'y loge, et ecrit son
// HTML dans le dossier temporaire du systeme. Le garde
// `ui-check/scripts/garde-boite-questions.mjs` (lance par ui-app/deployer.sh)
// les monte ensuite dans Chromium avec la vraie feuille de style construite,
// sur quatre tailles de fenetre : aucun bouton rogne, rien hors de la boite.
import { cleanup, render } from '@testing-library/react'
import fs from 'node:fs'
import os from 'node:os'
import path from 'node:path'
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest'
import type { ScanCardProps } from '../components/ScanCard'
import type { Demande, Option } from './ask'
import { CartouchePhase } from './CartouchePhase'
import type { EtapeDeroule } from './deroule-phase'
import type { AssistantInteraction, EtatInteractif, Interaction } from './interaction'
import type { QuestionDuMoteur } from './sous-cadre'
import type { WorldCard } from './world'

export const DOSSIER_PIRES_CAS = path.join(os.tmpdir(), 'marvel-boite-questions')

class RO {
  observe() {}
  unobserve() {}
  disconnect() {}
}
beforeAll(() => {
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = RO
  fs.mkdirSync(DOSSIER_PIRES_CAS, { recursive: true })
})
afterEach(() => cleanup())

const NOMS = ['L’Homme-Radioactif', 'Le Tourbillon', 'Le Fondeur', 'Le Requin-Tigre', 'Trafiquant d’Armes', 'Garde Blindé', 'Mercenaire d’Hydra', 'Shocker', 'Black Widow', 'Hulk']
const carte = (id: number, name: string, extra: Partial<WorldCard> = {}): WorldCard => ({
  id, is_ready: true, is_face_up: true, visible_for_players: [], bind_object_id: 0, name, info: { defense: 2 }, traits: {}, buffs: {},
  card_id: `c${id}`, pic_id: `c${id}`, down_card_ids: [], card_type: 'Minion', cost: 0, resources: [], ...extra,
})
const IDS = NOMS.map((_, i) => 100 + i)
const CARTES = new Map<number, WorldCard>(IDS.map((id, i) => [id, carte(id, NOMS[i])]))
CARTES.set(1, carte(1, 'Captain America', { card_type: 'Hero' }))
const LONG = 'Une fois révélée : chaque sbire Maîtres du Mal attaque le héros engagé avec lui. Si aucune attaque n’est effectuée par cet effet, cherchez un sbire Maîtres du Mal dans le deck Rencontre ou la pile de défausse Rencontre et mettez-le en jeu, engagé avec vous. Ensuite, mélangez le deck Rencontre.'

const option = (id: number, name: string, bind_id: number, extra: Partial<Option> = {}): Option => ({
  id, name, bind_id, bind_player_id: 0, all_legal_targets: [], target_num_range: [0, 0], target_payment: {}, select_rule: '',
  target_must_include_traits: [], failure_reason: '', is_search: false, ...extra,
})
const demande = (options: Option[], extra: Partial<Demande> = {}): Demande => ({
  options, refus: [], prompt_text: `Maîtres du Chaos · ${LONG}`, event_name: 'AfterDamage', show_cancel: true, ability_type: 'Response', ...extra,
})
const assistant = (extra: Partial<AssistantInteraction> = {}): AssistantInteraction => ({
  etape: 'action', titre: '', cibleMinimum: 0, cibleMaximum: 0, cibleNombre: 0, ciblePossibles: 0, cibleRepetable: false, coutPaye: 0,
  coutSlots: [], coutRegles: [], ...extra,
})
const interaction = (options: Option[], extra: Partial<Interaction> = {}): Interaction => ({
  cibles: [], ressources: [], options, defocaliser: vi.fn(), focaliserCarte: vi.fn(), focaliserCible: vi.fn(), cartes: new Map(),
  ciblesHorsTable: [], raison: '', prete: false, coutAffiche: '', surpaiementRecompense: false, ciblesRestantes: 0, assistant: assistant(),
  choisirOption: vi.fn(), abandonnerOption: vi.fn(), valider: vi.fn(), annuler: vi.fn(), paiementAutoChoix: 'pas-demande',
  basculerPaiementAuto: vi.fn(), ...extra,
})
const scan = (id: number): ScanCardProps => ({ id: String(id), name: CARTES.get(id)?.name ?? `#${id}`, kind: 'minion', imageUrl: '' })
const question = (d: Demande, i: Interaction = interaction(d.options)): QuestionDuMoteur => ({
  demande: d, interaction: i, cartesParId: CARTES, choisirOption: vi.fn(), survolerOption: vi.fn(), nomPorteur: (id) => CARTES.get(id)?.name,
  texteCapacite: () => LONG, estEnMain: () => false, carteScene: (id) => scan(id),
})
const cibles = (n: number, role: EtatInteractif['role'] = 'cible') =>
  new Map<number, EtatInteractif>(IDS.slice(0, n).map((id) => [id, { role, choisie: false, agir: vi.fn() }]))

const etapeRevelation: EtapeDeroule = { cle: 'revelation:1', temps: 'revelation', titre: 'revelation', regle: '', carteId: 99, cibleNom: 'Maîtres du Chaos', boosts: [] }
const etapeAnnonce: EtapeDeroule = { cle: 'activation:1', temps: 'mechant', titre: 'attaque', regle: '', etat: 'annonce', carteId: 1, cibleId: 1, auteurNom: 'Klaw', cibleNom: 'Captain America', valeurAnnoncee: 3, boosts: [] }

type Cas = { nom: string; etape: EtapeDeroule; q: QuestionDuMoteur; classe: string }

function lesCas(): Cas[] {
  const viser = option(9, 'Response', 1, { all_legal_targets: IDS.slice(0, 8), target_num_range: [1, 1] })
  const payer = option(4, 'Play', 1)
  const ordre = option(10, 'Minion_Activates_Order', 0, { all_legal_targets: IDS.slice(0, 8), target_num_range: [8, 8] })
  const reponses = IDS.slice(0, 4).map((id, i) => option(20 + i, 'Response', id))
  const effets = IDS.slice(0, 4).map((_, i) => option(40 + i, `Effet ${i + 1}`, 100))
  const defenses = IDS.slice(0, 4).map((id, i) => option(60 + i, 'Defense', id, { all_legal_targets: [1], target_num_range: [1, 1] }))
  // Multijoueur : « Demander à X de défendre » s'ajoute aux defenseurs (13/10/2026).
  const demanderAide = option(70, 'Ask', IDS[0], { all_legal_targets: [1], target_num_range: [1, 1] })
  return [
    { nom: 'cibles-8', classe: 'est-cibles', etape: etapeRevelation, q: question(demande([viser]), interaction([viser], { option: viser, cartes: cibles(8), raison: 'Choisis encore 1 cible', assistant: assistant({ etape: 'target', cibleMinimum: 1, cibleMaximum: 1 }) })) },
    { nom: 'paiement-8', classe: 'est-paiement', etape: etapeRevelation, q: question(demande([payer], { ability_type: 'Interrupt' }), interaction([payer], { option: payer, cartes: cibles(8, 'ressource'), assistant: assistant({ etape: 'payment', titre: 'Payer le coût', detail: '0/3 payé', coutRequis: 3, coutSlots: [{ index: 0, rempli: false }, { index: 1, rempli: false }, { index: 2, rempli: false }] }) })) },
    { nom: 'ordre-8', classe: 'est-ordre', etape: etapeAnnonce, q: question(demande([ordre], { show_cancel: false, ability_type: 'Normal', event_name: 'WhenChooseOrder' }), interaction([ordre], { option: ordre, cartes: cibles(8), assistant: assistant({ etape: 'target' }) })) },
    { nom: 'reponses-4', classe: 'est-reponses', etape: etapeAnnonce, q: question(demande(reponses, { event_name: 'WhenDamage' })) },
    { nom: 'choix-carte-4', classe: 'deroule-question-carte, .est-choix-carte', etape: etapeRevelation, q: question(demande(effets, { event_name: 'WhenPlayerChooseAbility' })) },
    { nom: 'confirmer', classe: 'est-confirmer', etape: etapeRevelation, q: question(demande([payer], { ability_type: 'Interrupt' }), interaction([payer], { option: payer, prete: true, assistant: assistant({ etape: 'confirm' }) })) },
    { nom: 'defense-4', classe: 'essai-choix-defense', etape: etapeAnnonce, q: question(demande([...defenses, demanderAide], { event_name: 'WhenEnemyAttack' })) },
  ]
}

const g = { onPointerDown: () => {}, onPointerMove: () => {}, onPointerUp: () => {}, onPointerCancel: () => {} }

describe('les pires cas des questions de la boite', () => {
  for (const cas of lesCas()) {
    it(`${cas.nom} : se loge dans la boite, et s ecrit pour le garde`, () => {
      const { container } = render(
        <CartouchePhase refCartouche={() => {}} gestes={g} etape={cas.etape} etapes={[cas.etape]} index={0} efface={false} questionAuJoueur
          avancer={vi.fn()} enAttente={false} attendUnAutreJoueur={false} defaiteLocale={false} boostsMontres={99} tempsParDecision={0}
          cartesDistribuees={0} questionDuMoteur={cas.q} tempsQuestion={cas.etape.temps} essai />
      )
      // La bonne sorte de question, sinon le garde mesurerait autre chose.
      expect(container.querySelector(`.${cas.classe}`), cas.nom).not.toBeNull()
      fs.writeFileSync(path.join(DOSSIER_PIRES_CAS, `${cas.nom}.html`), container.innerHTML)
    })
  }
})
