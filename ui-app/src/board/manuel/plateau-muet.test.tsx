// Le plateau manuel ne montre RIEN de ce que le moteur disait.
//
// On vise les classes CSS plutot que les composants : c'est ce que le joueur
// voit, et ca ne bouge pas quand un composant est renomme.
//
// ⚠ CORRECTION AU BRIEF (voir task-2-report.md). Le brief visait un attribut
// `data-pile` qui n'existe pas encore : il n'arrive qu'a la tache 5. On vise
// ici ce qui marque REELLEMENT la main aujourd'hui : `data-zone="main"`
// (Board.tsx, `Emplacement`) et la classe `main-visible-forcee` qui decide si
// elle se montre sans avoir besoin d'un survol (board.css).
//
// Le montage est calque sur `PagePartie.test.tsx`, qui monte deja cette page
// avec un moteur remplace (`MoteurFaux`) : on ne reecrit pas un second
// montage a cote.
import { act, render } from '@testing-library/react'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { MoteurFaux, etatInitial } from '../moteur-faux'
import type { EtatMoteur } from '../moteur'
import type { Demande, Option } from '../ask'
import { catalogueVide } from '../catalogue'
import { mondeDeTest } from './fixture-monde'

vi.mock('../moteur', async (original) => ({
  ...(await original<typeof import('../moteur')>()),
  Moteur: MoteurFaux,
}))

const { PagePartie } = await import('../../board')

function monter() {
  return render(
    <PagePartie
      playerId={0}
      catalogue={catalogueVide}
      modeActions="simple"
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
// calculer l'echelle. Meme bouchon que PagePartie.test.tsx.
class ResizeObserverBouchon {
  observe() {}
  unobserve() {}
  disconnect() {}
}

beforeEach(() => {
  MoteurFaux.derniere = undefined
  ;(globalThis as { ResizeObserver?: unknown }).ResizeObserver = ResizeObserverBouchon
})

describe('le plateau manuel se tait', () => {
  it('ne montre pas le bandeau de phase', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: true, manuel_actif: true }) })
    expect(container.querySelector('.bandeau-phase')).toBeNull()
  })

  it('ne montre pas le deroule de phase', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: true, manuel_actif: true }) })
    expect(container.querySelector('.deroule-phase')).toBeNull()
  })

  it('montre encore ces reperes en partie ordinaire', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({}) })
    expect(container.querySelector('.bandeau-phase')).not.toBeNull()
    expect(container.querySelector('.deroule-phase')).not.toBeNull()
  })
})

// TACHE 8 BIS. Le moteur distingue la REGLE (`mode_manuel`, vraie des la
// creation de la partie) de l'ETAT (`manuel_actif`, vrai seulement une fois
// la boucle manuelle entree, apres la mise en place). Le plateau doit se
// regler sur L'ETAT pour tout ce qui masque une couche du moteur : pendant
// la mise en place d'une partie manuelle, le moteur pose encore ses
// questions (mulligan compris), et la reponse doit rester ATTEIGNABLE.
//
// ⚠ LE DEFAUT QUE CE CAS REPRODUIT : avant ce correctif, le plateau se
// reglait sur `mode_manuel` (donc sur `estModeManuel`) pour masquer
// `DemandeCentrale`/`AssistantAction` — les DEUX panneaux qui portent le
// mulligan (« Garder cette main » / « Annuler »). Une partie manuelle fraiche
// masquait donc sa PROPRE question de mulligan des la mise en place, avant
// meme que la boucle manuelle n'existe : le joueur se retrouvait devant sa
// main sans rien a cliquer, et la partie ne demarrait jamais.
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

describe('le plateau manuel reste normal PENDANT LA MISE EN PLACE', () => {
  it('montre encore la demande centrale (le mulligan) : la regle est deja vraie, '
    + 'la boucle manuelle n\'a pas encore pris la main',
  async () => {
    const { container } = monter()
    await emettre({
      monde: mondeDeTest({ mode_manuel: true, manuel_actif: false }),
      demande: demandeMulligan(),
      aNous: true,
    })
    expect(container.querySelector('.demande-centrale')).not.toBeNull()
  })

  it('la masque bien une fois la boucle manuelle entree (manuel_actif)', async () => {
    const { container } = monter()
    await emettre({
      monde: mondeDeTest({ mode_manuel: true, manuel_actif: true }),
      demande: demandeMulligan(),
      aNous: true,
    })
    expect(container.querySelector('.demande-centrale')).toBeNull()
  })
})

// LA MAIN DE CHAQUE HEROS (etape 5 du brief). Le plateau ne dessine
// aujourd'hui QUE la main du joueur regarde (zones.ts, `notre?.hand_cards`) :
// il n'y a pas plusieurs zones « main » a compter, une seule, cachee derriere
// un survol (board.css, `.zone-main:hover`). En manuel, un seul operateur
// manipule tous les heros : cette main doit rester visible SANS survol.
describe('le plateau manuel montre la main sans avoir besoin d\'un survol', () => {
  it('force la main visible', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: true, manuel_actif: true }) })
    expect(container.querySelectorAll('[data-zone="main"]').length).toBeGreaterThan(0)
    expect(container.querySelector('.plateau.main-visible-forcee')).not.toBeNull()
  })

  it('ne la force pas en partie ordinaire, hors interaction', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({}) })
    expect(container.querySelectorAll('[data-zone="main"]').length).toBeGreaterThan(0)
    expect(container.querySelector('.plateau.main-visible-forcee')).toBeNull()
  })

  // TACHE 3 (correctif). `mainVisibleForcee` se reglait sur `leMoteurSeTait`
  // seul (`manuel`), qui vaut aussi vrai pendant une PAUSE d'une partie
  // ORDINAIRE (route `/manuel_pause`) -- pas seulement en mode manuel
  // DECLARE. Une table EN LIGNE mise en pause aurait alors montre les mains
  // de TOUS les joueurs a TOUS les ecrans, exactement la fuite d'information
  // que l'arbitrage du plan interdit. `board.tsx` doit se regler sur
  // `estModeManuel` pour ce seul champ.
  it('ne force PAS la main pendant une pause d\'une partie ORDINAIRE (correctif tache 3)', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: false, manuel_actif: true }) })
    expect(container.querySelector('.plateau.main-visible-forcee')).toBeNull()
  })
})

// LE BOUTON « Fin du tour » (signale par la tache 8 sans etre teste, corrige
// ici : tache 8 bis). Il n'a plus aucun sens en mode manuel — il n'y a plus
// de tour a finir, le moteur ne conduit plus rien — mais la barre generique
// qui le porte reste affichee dans tous les modes (Menu/Annuler/Sauver/
// Partie/Reglages/FR restent legitimes). Seul CE bouton doit disparaitre.
describe('le bouton Fin du tour disparait en mode manuel', () => {
  it('reste affiche en partie ordinaire', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({}) })
    expect(container.querySelector('.bh-fin-tour')).not.toBeNull()
  })

  it('disparait une fois la boucle manuelle entree (manuel_actif)', async () => {
    const { container } = monter()
    await emettre({ monde: mondeDeTest({ mode_manuel: true, manuel_actif: true }) })
    expect(container.querySelector('.bh-fin-tour')).toBeNull()
  })
})
