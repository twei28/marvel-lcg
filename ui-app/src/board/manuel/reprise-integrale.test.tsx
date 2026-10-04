// reprise-integrale.test.tsx — TACHE 4 du plan de pause : la reprise rend
// bien tout ce que la pause avait retire.
//
// `plateau-muet.test.tsx` prouve que le mode manuel DECLARE masque le
// moteur -- mais une partie manuelle declaree ne redevient JAMAIS
// automatique (`world.rule.mode_manuel` reste vraie a vie), donc personne
// n'a jamais eu besoin de faire REAPPARAITRE quoi que ce soit. La pause EN
// COURS DE PARTIE (tache 3, route `/manuel_pause`) est le premier endroit ou
// `manuel_actif` repasse a FAUX apres avoir ete vrai : c'est ce
// retournement-la, et seulement lui, que ce fichier verifie.
//
// UN SEUL SCENARIO CONCEPTUEL (vrai/faux/vrai sur `manuel_actif`, partie
// ORDINAIRE -- `mode_manuel` reste faux tout du long), decoupe en plusieurs
// `it()` : les couches a prouver vivent derriere des reglages MUTUELLEMENT
// EXCLUSIFS du plateau (le recapitulatif ne s'affiche qu'en mode
// « Instantane », le bandeau/deroule seulement HORS de ce mode ; la barre
// des actions n'existe qu'en affichage « Detaille »), impossible de les
// montrer toutes dans un seul rendu. Chaque `it()` reprend neanmoins
// EXACTEMENT le meme geste : un mount, `manuel_actif` a vrai, puis a faux,
// sur la MEME instance montee -- c'est cette continuite-la qui debusque un
// composant qui ne se redessine pas.
import { act, fireEvent, render } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { MoteurFaux, etatInitial } from '../moteur-faux'
import type { EtatMoteur } from '../moteur'
import { CLE_MODE_PHASE } from '../moteur'
import type { Demande, Option } from '../ask'
import { catalogueVide } from '../catalogue'
import { mondeDeTest, mondeDeuxJoueurs } from './fixture-monde'

vi.mock('../moteur', async (original) => ({
  ...(await original<typeof import('../moteur')>()),
  Moteur: MoteurFaux,
}))

const { PagePartie } = await import('../../board')

function monter(modeActions: 'simple' | 'detailed' = 'simple') {
  return render(
    <PagePartie
      playerId={0}
      catalogue={catalogueVide}
      modeActions={modeActions}
      changerModeActions={() => {}}
    />
  )
}

/** Emet une trame vers l'ecran monte, sur l'etat d'ouverture par defaut. */
async function emettre(trame: Partial<EtatMoteur>) {
  await act(async () => {
    MoteurFaux.derniere?.emettre({ ...etatInitial(), connecte: true, ...trame })
  })
}

// jsdom n'implemente pas ResizeObserver : le plateau observe son cadre pour
// calculer l'echelle. Meme bouchon que plateau-muet.test.tsx.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

beforeEach(() => {
  MoteurFaux.derniere = undefined
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
  window.localStorage.clear()
})

afterEach(() => {
  window.localStorage.clear()
})

function option(surcharge: Partial<Option> = {}): Option {
  return {
    id: 1,
    name: 'Keep_hand',
    bind_id: 0,
    bind_player_id: 0,
    all_legal_targets: [],
    target_num_range: [0, 0],
    target_payment: {},
    select_rule: '',
    target_must_include_traits: [],
    failure_reason: '',
    is_search: false,
    ...surcharge,
  } as unknown as Option
}

/** La question du mulligan : deux options, aucune annulation possible. */
function demandeMulligan(): Demande {
  return {
    options: [option({ id: 1, name: 'Keep_hand' }), option({ id: 2, name: 'Mulligan' })],
    refus: [],
    prompt_text: '',
    event_name: 'WhenPlayerResolveMulligans',
    show_cancel: false,
    ability_type: 'Normal',
  } as unknown as Demande
}

/**
 * UNE SEULE option, nommee "Mulligan" : `interaction.ts` (`optionDemarreAuto`)
 * la choisit TOUTE SEULE des qu'elle est l'unique option de la demande, sans
 * qu'aucun clic ne soit necessaire. C'est le seul moyen d'obtenir
 * `interaction.option` rempli via `emettre()` seul, sans avoir a rejouer tout
 * le routage d'un clic sur une carte reelle du plateau -- `AssistantAction`
 * n'a besoin que de cet etat-la pour s'afficher.
 */
function demandeMulliganAutoSelectionnee(): Demande {
  return {
    options: [option({ id: 7, name: 'Mulligan', target_num_range: [0, 0] })],
    refus: [],
    prompt_text: '',
    event_name: 'WhenPlayerResolveMulligans',
    show_cancel: false,
    ability_type: 'Normal',
  } as unknown as Demande
}

describe('tout revient a la reprise (tache 4) : bandeau et deroule de phase', () => {
  it('disparaissent pendant la pause puis reapparaissent a la reprise, sur la MEME partie', async () => {
    const { container } = monter()
    // Avant : partie ordinaire, phase du mechant engagee (fixture).
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
    expect(container.querySelector('.deroule-phase')).not.toBeNull()

    // Pendant : la pause (route /manuel_pause) pose manuel_actif a vrai SANS
    // jamais declarer mode_manuel -- c'est la distinction meme de `estEnPause`.
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: true }) })
    expect(container.querySelector('.bandeau-phase')).toBeNull()
    expect(container.querySelector('.deroule-phase')).toBeNull()

    // Apres : la reprise repose manuel_actif a faux. C'EST LE CAS QUE PERSONNE
    // N'AVAIT JAMAIS EU BESOIN D'EXERCER (voir l'en-tete de ce fichier).
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
    expect(container.querySelector('.deroule-phase')).not.toBeNull()
  })
})

describe('tout revient a la reprise (tache 4) : demande centrale (le mulligan)', () => {
  it('disparait pendant la pause puis reapparait a la reprise', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }), demande: demandeMulligan(), aNous: true })
    expect(container.querySelector('.demande-centrale')).not.toBeNull()

    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: true }), demande: demandeMulligan(), aNous: true })
    expect(container.querySelector('.demande-centrale')).toBeNull()

    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }), demande: demandeMulligan(), aNous: true })
    expect(container.querySelector('.demande-centrale')).not.toBeNull()
  })
})

describe("tout revient a la reprise (tache 4) : l'assistant d'action", () => {
  it('disparait pendant la pause puis reapparait a la reprise', async () => {
    const { container } = monter()
    // Au tour du joueur : en phase du mechant, un ciblage se joue dans la
    // scene du deroule et l'assistant se tait (AssistantAction, 04/10/2026).
    const demande = demandeMulliganAutoSelectionnee()

    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false, phase: 'Player Turn' }), demande, aNous: true })
    expect(container.querySelector('.assistant-action')).not.toBeNull()

    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: true, phase: 'Player Turn' }), demande, aNous: true })
    expect(container.querySelector('.assistant-action')).toBeNull()

    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false, phase: 'Player Turn' }), demande, aNous: true })
    expect(container.querySelector('.assistant-action')).not.toBeNull()
  })
})

describe('tout revient a la reprise (tache 4) : la barre des actions (mode Detaille)', () => {
  it('disparait pendant la pause puis reapparait a la reprise', async () => {
    const { container } = monter('detailed')
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })
    expect(container.querySelector('.plateau-action')).not.toBeNull()

    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: true }) })
    expect(container.querySelector('.plateau-action')).toBeNull()

    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })
    expect(container.querySelector('.plateau-action')).not.toBeNull()
  })
})

describe('tout revient a la reprise (tache 4) : le recapitulatif de la phase du mechant', () => {
  it('disparait pendant la pause puis reapparait a la reprise, bilan compris', async () => {
    // Le recapitulatif ne se montre QU'EN MODE INSTANTANE (board.tsx,
    // `RecapPhaseMechant actif={!unCartouche}`) : c'est l'oppose du reglage
    // qu'exige le bandeau/deroule ci-dessus. Pose AVANT le montage : le
    // plateau lit `lireModePhaseMechant()` a chaque rendu.
    window.localStorage.setItem(CLE_MODE_PHASE, 'instantane')

    const { container } = monter()
    // Phase du mechant EN COURS : aucun bilan encore (rien a raconter tant
    // qu'on n'en est pas sorti).
    await emettre({
      monde: mondeDeTest({ mode_manuel: false, manuel_actif: false, phase: 'Main Scheme Place Threat' }),
    })
    expect(container.querySelector('.recap-mechant')).toBeNull()

    // Sortie de la phase, MEME round : c'est la transition qui fabrique le
    // bilan (voir RecapPhaseMechant, `dansLaPhaseAvant`).
    await emettre({
      monde: mondeDeTest({ mode_manuel: false, manuel_actif: false, phase: 'PlayerWindow', round_id: 2 }),
    })
    expect(container.querySelector('.recap-mechant')).not.toBeNull()

    // Pendant la pause : masque.
    await emettre({
      monde: mondeDeTest({ mode_manuel: false, manuel_actif: true, phase: 'PlayerWindow', round_id: 2 }),
    })
    expect(container.querySelector('.recap-mechant')).toBeNull()

    // A LA REPRISE : le bilan deja constitue doit revenir, SANS qu'aucune
    // nouvelle transition de phase ne se reproduise (le monde n'a pas bouge).
    await emettre({
      monde: mondeDeTest({ mode_manuel: false, manuel_actif: false, phase: 'PlayerWindow', round_id: 2 }),
    })
    expect(container.querySelector('.recap-mechant')).not.toBeNull()
  })
})

describe('tout revient a la reprise (tache 4) : le selecteur de vue « Auto »', () => {
  it("ne disparait JAMAIS pendant une pause de partie ORDINAIRE (arbitrage du plan, pas le selecteur de heros)", async () => {
    const { container } = monter()
    // Le selecteur de vue n'existe qu'a PLUSIEURS joueurs (board.tsx).
    await emettre({ monde: mondeDeuxJoueurs({ mode_manuel: false, manuel_actif: false }) })
    expect(container.querySelector('.bh-vue')).not.toBeNull()

    // PENDANT la pause : il doit RESTER, contrairement a toutes les couches
    // ci-dessus. Le masquer serait perdre TOUT selecteur de vue sur une table
        // a plusieurs heros mise en pause (voir manuel/mode.ts, `estEnPause`).
    await emettre({ monde: mondeDeuxJoueurs({ mode_manuel: false, manuel_actif: true }) })
    expect(container.querySelector('.bh-vue')).not.toBeNull()

    // Apres la reprise : toujours la.
    await emettre({ monde: mondeDeuxJoueurs({ mode_manuel: false, manuel_actif: false }) })
    expect(container.querySelector('.bh-vue')).not.toBeNull()

    // ⚠ `SelecteurHeros` (mode manuel DECLARE) partage la MEME classe
    // `.bh-vue` que ce selecteur de vue « Auto » -- il ne peut donc pas se
    // distinguer par selecteur CSS. Il ne peut de toute facon jamais
    // apparaitre ici : sa condition de montage est `modeManuelDeclare`
    // (board.tsx), qui reste FAUSSE tout du long de ce scenario (partie
    // ORDINAIRE, `mode_manuel` jamais vrai). Un seul `.bh-vue` doit donc
    // exister a tout instant -- exactement ce qu'on vient de verifier trois
    // fois ci-dessus, jamais deux montes en meme temps.
    expect(container.querySelectorAll('.bh-vue')).toHaveLength(1)
  })
})

describe('tout revient a la reprise (tache 4) : les gestes manuels (clic droit, clavier)', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: true }) as Response))
  })

  it('le clic droit dans le vide ouvre le menu de table PENDANT la pause, plus APRES la reprise', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })
    // Avant la pause : partie ordinaire, le clic droit ne doit RIEN ouvrir
    // (le menu manuel n'a pas sa place hors pause/mode manuel).
    fireEvent.contextMenu(document.body)
    expect(container.querySelector('[role="menu"]')).toBeNull()

    // Pendant la pause : le clic droit dans le vide ouvre le menu de TABLE.
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: true }) })
    fireEvent.contextMenu(document.body)
    expect(container.querySelector('[role="menu"]')).not.toBeNull()

    // A la reprise : le geste ne doit plus rien ouvrir.
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })
    fireEvent.contextMenu(document.body)
    expect(container.querySelector('[role="menu"]')).toBeNull()
  })

  it('le clavier (F = retourner) parle au moteur PENDANT la pause, plus APRES la reprise', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })

    const carte = container.querySelector('[data-card-id="1"]')
    expect(carte).not.toBeNull()

    // Avant la pause : le clavier manuel ne mord pas en partie ordinaire.
    // ⚠ PAS `expect(fetch).not.toHaveBeenCalled()` : PagePartie sonde deja
    // `/get_annonce` et `/get_rapport_actif` en tache de fond, sans rapport
    // avec ce geste -- seul l'APPEL PRECIS du geste manuel compte ici.
    fireEvent.pointerMove(carte as Element)
    fireEvent.keyDown(document, { key: 'f' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalledWith('/sandbox_command', expect.anything())

    // Pendant la pause : il repond.
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: true }) })
    fireEvent.pointerMove(carte as Element)
    fireEvent.keyDown(document, { key: 'f' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).toHaveBeenCalledWith('/sandbox_command', expect.objectContaining({
      body: JSON.stringify({ commands: ['Puzzle.Flip(1)'] }),
    }))

    // A la reprise : il ne doit plus repondre.
    ;(fetch as ReturnType<typeof vi.fn>).mockClear()
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: false }) })
    fireEvent.pointerMove(carte as Element)
    fireEvent.keyDown(document, { key: 'f' })
    await act(async () => { await Promise.resolve() })
    expect(fetch).not.toHaveBeenCalledWith('/sandbox_command', expect.anything())
  })
})
