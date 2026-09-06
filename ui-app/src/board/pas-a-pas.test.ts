// Ce que le pas à pas doit garantir, et les pièges qu'on a déjà rencontrés.
import { describe, expect, it } from 'vitest'
import {
  bornerDelai,
  decisionAccuse,
  evenementAMontrer,
  lireModePhaseMechant,
  DELAI_PAS_A_PAS_DEFAUT,
  DELAI_PAS_A_PAS_MAX,
  DELAI_PAS_A_PAS_MIN,
  PHASES_DU_MECHANT,
  CLE_MODE_PHASE,
  CLE_PHASE_RAPIDE,
} from './moteur'
import { estBienVisible, montrerEtape, texteFlottant } from './pas-a-pas'
import { pointDeLaPhase } from './CouchePasAPas'
import type { EntreeHistorique } from './HistoriquePartie'
import type { World } from './world'

const monde = (p: Partial<World>): World => p as World

function entree(p: Partial<EntreeHistorique>): EntreeHistorique {
  return { cle: 'k', type: 'damage', renderId: 1, round: 1, phase: '', titre: '', ...p }
}

describe('le délai', () => {
  it('reste dans les bornes', () => {
    expect(bornerDelai(50)).toBe(DELAI_PAS_A_PAS_MIN)
    expect(bornerDelai(99999)).toBe(DELAI_PAS_A_PAS_MAX)
    expect(bornerDelai(1200)).toBe(1200)
  })

  // Un NaN venu d'un localStorage corrompu rendrait le setTimeout immédiat,
  // donc la phase de nouveau illisible — le défaut est le seul repli sûr.
  it('retombe sur le défaut quand la valeur n’est pas un nombre', () => {
    expect(bornerDelai(Number.NaN)).toBe(DELAI_PAS_A_PAS_DEFAUT)
  })
})

describe('le mode', () => {
  it('migre l’ancienne case décochée vers « manuel »', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_PHASE_RAPIDE, 'off')
    expect(lireModePhaseMechant()).toBe('manuel')
  })

  // Celui qui avait coché « rapide » subissait précisément le défaut qu'on
  // corrige : on le fait atterrir sur « pas-a-pas », pas sur « instantane ».
  it('migre l’ancienne case cochée vers « pas à pas »', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_PHASE_RAPIDE, 'on')
    expect(lireModePhaseMechant()).toBe('pas-a-pas')
  })

  it('préfère le réglage explicite quand il existe', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_PHASE_RAPIDE, 'off')
    window.localStorage.setItem(CLE_MODE_PHASE, 'instantane')
    expect(lireModePhaseMechant()).toBe('instantane')
  })

  // Depuis le mode « detaille », c'est lui le defaut d'une installation neuve
  // (voir mode-detaille.test.ts) : « pas-a-pas » reste un choix disponible,
  // plus le defaut.
  it('vaut « detaille » sur une installation neuve', () => {
    window.localStorage.clear()
    expect(lireModePhaseMechant()).toBe('detaille')
  })
})

describe('les événements montrés', () => {
  it('retient les statuts, que le mode manuel ignorait', () => {
    expect(evenementAMontrer(monde({ event_name: 'AfterUnitGainStatus' }))).toBe(true)
    expect(evenementAMontrer(monde({ event_name: 'AfterUnitLostStatus' }))).toBe(true)
  })

  it('retient les dégâts, la menace et les révélations', () => {
    expect(evenementAMontrer(monde({ prompt: 'Gorr subit 5 dégât(s)' }))).toBe(true)
    expect(evenementAMontrer(monde({ prompt: 'gagne 1 menace' }))).toBe(true)
    expect(evenementAMontrer(monde({ prompt: 'is being revealed' }))).toBe(true)
  })

  // Sans ce filtre, chaque déplacement de carte deviendrait une étape et la
  // phase durerait des minutes : c'est le « trop d'infos » d'avant.
  it('laisse filer les étapes techniques', () => {
    expect(evenementAMontrer(monde({ prompt: 'cards were placed on table' }))).toBe(false)
    expect(evenementAMontrer(undefined)).toBe(false)
  })
})

describe('les phases concernées', () => {
  it('couvre les quatre points de la carte de référence', () => {
    for (const phase of [
      'Main Scheme Place Threat',
      'Enemy Activation',
      'Deal Encounter Cards',
      'Reveal Encounter Cards',
    ]) {
      expect(PHASES_DU_MECHANT.has(phase)).toBe(true)
      expect(pointDeLaPhase(phase)).toBeDefined()
    }
  })

  it('ne déborde pas sur le tour du joueur', () => {
    expect(PHASES_DU_MECHANT.has('Player 1 Turn')).toBe(false)
    expect(pointDeLaPhase('Player 1 Turn')).toBeUndefined()
    expect(pointDeLaPhase(undefined)).toBeUndefined()
  })
})

describe('le chiffre flottant', () => {
  it('garde le signe de la variation', () => {
    expect(texteFlottant(entree({ type: 'damage', valeur: -3 }))).toBe('−3 ♥')
    expect(texteFlottant(entree({ type: 'heal', valeur: 2 }))).toBe('+2 ♥')
    expect(texteFlottant(entree({ type: 'threat', valeur: 1 }))).toBe('+1 ⚠')
  })

  it('ne dit rien quand il n’y a pas de nombre', () => {
    expect(texteFlottant(entree({ type: 'card', valeur: undefined }))).toBeUndefined()
    expect(texteFlottant(entree({ type: 'damage', valeur: 0 }))).toBeUndefined()
  })
})

describe('le recentrage', () => {
  // Recentrer à chaque étape donne le mal de mer et fait rater ce qu'on veut
  // montrer : on ne bouge que si la carte est vraiment sortie de l'écran.
  it('ne bouge pas pour une carte déjà lisible', () => {
    const rect = { top: 300, bottom: 500, left: 400, right: 600 } as DOMRect
    expect(estBienVisible(rect, 1000, 1600)).toBe(true)
  })

  it('recentre une carte hors champ ou collée au bord', () => {
    expect(estBienVisible({ top: -50, bottom: 120, left: 400, right: 600 } as DOMRect, 1000, 1600)).toBe(false)
    expect(estBienVisible({ top: 300, bottom: 500, left: 1500, right: 1700 } as DOMRect, 1000, 1600)).toBe(false)
  })
})

describe('qui retient l’accusé de réception', () => {
  const degats = monde({ phase: 'Enemy Activation', prompt: 'Doom subit 3 dégât(s)' })

  it('attend le délai en pas à pas, sur les quatre phases', () => {
    for (const phase of PHASES_DU_MECHANT) {
      const m = monde({ phase, prompt: 'subit 3 dégât(s)' })
      expect(decisionAccuse('pas-a-pas', m, false)).toBe('attendre-delai')
    }
  })

  // « Tout passer » ne vaut que pour LA phase en cours : sans ce drapeau, le
  // joueur qui saute une phase les sauterait toutes.
  it('n’attend plus rien quand la phase a été sautée', () => {
    expect(decisionAccuse('pas-a-pas', degats, true)).toBe('immediat')
  })

  it('n’attend jamais en instantané', () => {
    expect(decisionAccuse('instantane', degats, false)).toBe('immediat')
  })

  it('attend un clic en detaille, sur les quatre phases', () => {
    // Decision explicite du proprietaire : le mode detaille doit lui aussi
    // retenir l'accuse de reception, sinon le moteur resout la phase a pleine
    // vitesse et le cartouche etape par etape ne fait que raconter un passe.
    // Il differe de « pas-a-pas » sur un seul point : il attend un CLIC (la
    // validation « Suivant » du cartouche), pas un delai automatique.
    for (const phase of PHASES_DU_MECHANT) {
      const m = monde({ phase, prompt: 'subit 3 dégât(s)' })
      expect(decisionAccuse('detaille', m, false)).toBe('attendre-clic')
    }
  })

  it('n’attend plus rien en detaille quand la phase a ete sautee', () => {
    expect(decisionAccuse('detaille', degats, true)).toBe('immediat')
  })

  it('n’attend rien en detaille hors evenement a montrer', () => {
    expect(
      decisionAccuse('detaille', monde({ phase: 'Enemy Activation', prompt: 'cards were placed on table' }), false)
    ).toBe('immediat')
  })

  it('attend un clic en manuel, et seulement sur les activations', () => {
    expect(decisionAccuse('manuel', degats, false)).toBe('attendre-clic')
    expect(
      decisionAccuse('manuel', monde({ phase: 'Deal Encounter Cards', prompt: 'subit 3 dégât(s)' }), false)
    ).toBe('immediat')
  })

  // Le tour du joueur ne doit JAMAIS être ralenti : c'est lui qui agit.
  it('laisse filer le tour du joueur dans tous les modes', () => {
    const tour = monde({ phase: 'Player 1 Turn', prompt: 'subit 3 dégât(s)' })
    expect(decisionAccuse('pas-a-pas', tour, false)).toBe('immediat')
    expect(decisionAccuse('manuel', tour, false)).toBe('immediat')
  })
})

describe('la mise en lumière', () => {
  function poserCarte(id: number): HTMLElement {
    document.body.innerHTML = '<div class="plateau-scene"></div>'
    const el = document.createElement('div')
    el.className = 'scan-card'
    el.setAttribute('data-card-id', String(id))
    el.getBoundingClientRect = () => ({ top: 300, bottom: 500, left: 400, right: 600 }) as DOMRect
    document.querySelector('.plateau-scene')!.appendChild(el)
    return el
  }

  it('pose le halo teinté et le chiffre sur la bonne carte', () => {
    const el = poserCarte(42)
    const nettoyer = montrerEtape(entree({ cibleId: 42, type: 'damage', valeur: -3 }))
    expect(el.classList.contains('pas-a-pas-halo')).toBe(true)
    expect(el.classList.contains('pas-a-pas-degats')).toBe(true)
    expect(el.querySelector('.pas-a-pas-chiffre')?.textContent).toBe('−3 ♥')
    nettoyer?.()
    expect(el.classList.contains('pas-a-pas-halo')).toBe(false)
    expect(el.querySelector('.pas-a-pas-chiffre')).toBeNull()
  })

  // Une entrée « text » n'a rien de visuel à dire : la mettre en lumière
  // ferait clignoter une carte au hasard à chaque ligne de narration.
  it('ne fait rien pour un type sans teinte, ni sans cible', () => {
    poserCarte(42)
    expect(montrerEtape(entree({ cibleId: 42, type: 'text' }))).toBeUndefined()
    expect(montrerEtape(entree({ cibleId: undefined, type: 'damage', valeur: -3 }))).toBeUndefined()
  })

  it('ne plante pas quand la carte n’est plus sur le plateau', () => {
    poserCarte(42)
    expect(montrerEtape(entree({ cibleId: 999, type: 'damage', valeur: -1 }))).toBeUndefined()
  })
})
