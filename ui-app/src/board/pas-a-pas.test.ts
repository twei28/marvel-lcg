// Ce que le pas à pas doit garantir, et les pièges qu'on a déjà rencontrés.
import { describe, expect, it } from 'vitest'
import {
  bornerDelai,
  decisionAccuse,
  ecrireModePhaseMechant,
  lireAvanceAuto,
  lireModePhaseMechant,
  migrerReglagesPhase,
  DELAI_FILET_ANTI_BLOCAGE_CLIC_MS,
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
  // L'ancienne case a cocher (avant meme les quatre modes) ne connaissait que
  // deux etats : decochee -> un Continue a chaque fois (l'ancien « manuel »),
  // cochee -> tout defile (l'ancien « pas-a-pas »). Les deux atterrissent
  // desormais sur « detaille », seule l'avance auto les distingue encore.
  // La migration est EXPLICITE (`migrerReglagesPhase`) : les lecteurs ne
  // devinent plus rien tout seuls, voir le describe suivant pour la raison.
  it('migre l’ancienne case décochée : detaille, sans avance auto', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_PHASE_RAPIDE, 'off')
    migrerReglagesPhase()
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lireAvanceAuto()).toBe(false)
  })

  // Celui qui avait coché « rapide » subissait précisément le défaut qu'on
  // corrige : on le fait atterrir sur l'avance auto, pas sur « instantane ».
  it('migre l’ancienne case cochée : detaille, AVEC avance auto', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_PHASE_RAPIDE, 'on')
    migrerReglagesPhase()
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lireAvanceAuto()).toBe(true)
  })

  it('préfère le réglage explicite quand il existe', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_PHASE_RAPIDE, 'off')
    window.localStorage.setItem(CLE_MODE_PHASE, 'instantane')
    migrerReglagesPhase()
    expect(lireModePhaseMechant()).toBe('instantane')
  })

  it('vaut « detaille » sur une installation neuve, sans avance auto', () => {
    window.localStorage.clear()
    migrerReglagesPhase()
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lireAvanceAuto()).toBe(false)
  })

  // Migration plus recente : un joueur deja passe par les QUATRE anciens
  // modes avait pu enregistrer « manuel » ou « pas-a-pas » directement sous
  // la cle actuelle (CLE_MODE_PHASE). Meme regle que la case a cocher, lue
  // sur la cle qui l'a remplacee.
  it('migre l’ancien mode « manuel » stocké : detaille, sans avance auto', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_MODE_PHASE, 'manuel')
    migrerReglagesPhase()
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lireAvanceAuto()).toBe(false)
  })

  it('migre l’ancien mode « pas-a-pas » stocké : detaille, AVEC avance auto', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_MODE_PHASE, 'pas-a-pas')
    migrerReglagesPhase()
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lireAvanceAuto()).toBe(true)
  })
})

describe('la migration ne se refait pas a chaque lecture', () => {
  // Le défaut trouvé en revue : `CLE_MODE_PHASE` est réécrite par l'usage
  // normal (les boutons Détaillé/Instantané), et perd alors la trace de
  // l'ancien réglage. Une lecture croisée qui retente sa chance à chaque
  // appel de `lireAvanceAuto` retombe donc sur le défaut dès que le joueur
  // change de mode sans jamais toucher à la case « Avance auto » : elle
  // affichait déjà ce qu'il voulait, il n'y a pas touché. La migration doit
  // donc être faite UNE FOIS, tôt, et écrire les DEUX clés.
  it('garde l’avance auto migrée après un aller-retour Instantané -> Détaillé (pas-a-pas)', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_MODE_PHASE, 'pas-a-pas')
    migrerReglagesPhase()
    expect(lireAvanceAuto()).toBe(true)
    ecrireModePhaseMechant('instantane')
    ecrireModePhaseMechant('detaille')
    expect(lireAvanceAuto()).toBe(true)
  })

  // Cas symétrique : l'ancien « manuel » ne doit pas se remettre à cocher
  // l'avance auto pour autant.
  it('garde l’absence d’avance auto après un aller-retour Instantané -> Détaillé (manuel)', () => {
    window.localStorage.clear()
    window.localStorage.setItem(CLE_MODE_PHASE, 'manuel')
    migrerReglagesPhase()
    expect(lireAvanceAuto()).toBe(false)
    ecrireModePhaseMechant('instantane')
    ecrireModePhaseMechant('detaille')
    expect(lireAvanceAuto()).toBe(false)
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

  // « Avance toute seule » n'est PAS l'affaire du moteur : c'est le cartouche
  // qui s'avance lui-meme (DeroulePhase, prop `avanceAuto`) et relache la
  // trame par le meme chemin que le clic « Suivant ». Le moteur, lui, attend
  // toujours ce relachement : il n'a plus d'horloge propre. Il en avait une
  // (`attendre-delai`), et les deux divergeaient a la premiere etape : le
  // joueur lisait la menace, le mechant et ses sbires avaient deja frappe.
  it('ne rend jamais « attendre-delai » en detaille : l’avance auto ne le regarde pas', () => {
    for (const phase of PHASES_DU_MECHANT) {
      const m = monde({ phase, prompt: 'subit 3 dégât(s)' })
      expect(decisionAccuse('detaille', m)).toBe('attendre-clic')
    }
  })

  // Le type lui-meme ne connait plus que deux valeurs : le moteur attend un
  // clic du cartouche, ou n'attend pas. Ce test ne compile que tant que c'est
  // vrai.
  it('ne connait que deux decisions : immediat ou attendre-clic', () => {
    const decisions: Record<ReturnType<typeof decisionAccuse>, true> = {
      immediat: true,
      'attendre-clic': true,
    }
    expect(Object.keys(decisions)).toHaveLength(2)
  })

  it('attend un clic en detaille sans avance auto, sur les quatre phases', () => {
    // Decision explicite du proprietaire : le mode detaille retient l'accuse
    // de reception, sinon le moteur resout la phase a pleine vitesse et le
    // cartouche etape par etape ne fait que raconter un passe. Il differe de
    // l'avance auto sur un seul point : il attend un CLIC (la validation
    // « Suivant » du cartouche), pas un delai automatique.
    for (const phase of PHASES_DU_MECHANT) {
      const m = monde({ phase, prompt: 'subit 3 dégât(s)' })
      expect(decisionAccuse('detaille', m)).toBe('attendre-clic')
    }
  })

  // Il n'y a plus de « laissez passer » pour toute la phase (l'ancien
  // `phaseSautee`, pose par Echap) : Echap fait defiler le cartouche, qui
  // acquitte une trame a la fois. Le moteur ne peut donc plus partir devant.

  it('n’attend jamais en instantané, même en pleine phase du méchant', () => {
    expect(decisionAccuse('instantane', degats)).toBe('immediat')
  })

  // Le filtre `evenementAMontrer` a été RETIRÉ, et c'est le cœur de la
  // correction du rythme. Un micro-événement « technique » fait quand même
  // grandir le journal, donc il fabrique une étape du cartouche : le laisser
  // filer, c'était laisser le moteur prendre de l'avance sur ce que le joueur
  // a lu. Mesuré en partie réelle : menace, activation, accomplissement de la
  // manigance principale et défaite exécutés pendant que le cartouche en était
  // à sa deuxième étape.
  //
  // Retenir cette trame ne coûte rien : le cartouche l'acquitte aussitôt si
  // elle ne lui fabrique aucune étape (DeroulePhase, `cartoucheAJour`).
  it('retient aussi les trames « techniques » de la phase du méchant', () => {
    expect(
      decisionAccuse(
        'detaille',
        monde({ phase: 'Enemy Activation', prompt: 'cards were placed on table' })
      )
    ).toBe('attendre-clic')
  })

  // Une trame sans prompt ni event_name ne dit rien du tout : elle est retenue
  // comme les autres, tant qu'elle appartient à la phase du méchant.
  it('retient une trame muette de la phase du méchant', () => {
    expect(decisionAccuse('detaille', monde({ phase: 'Enemy Activation' }))).toBe('attendre-clic')
  })

  // Le monde n'est pas encore chargé : aucune phase, donc rien à retenir.
  it('ne retient rien sans monde', () => {
    expect(decisionAccuse('detaille', undefined)).toBe('immediat')
  })

  // Le tour du joueur ne doit JAMAIS être ralenti : c'est lui qui agit.
  it('laisse filer le tour du joueur', () => {
    const tour = monde({ phase: 'Player 1 Turn', prompt: 'subit 3 dégât(s)' })
    expect(decisionAccuse('detaille', tour)).toBe('immediat')
  })
})

// Défaut 1 (voir brief) : le filet anti-blocage (6s) était plus court que le
// temps de lire une étape du cartouche, un joueur attentif se faisait donc
// doubler par son propre garde-fou.
describe('le filet anti-blocage', () => {
  // Le moteur n'attend jamais qu'un CLIC du cartouche : le filet n'a plus
  // qu'une seule durée (l'ancien délai court de 6 s accompagnait un minuteur
  // de lecture que le moteur ne tient plus).
  it('laisse largement le temps de lire une étape avant de doubler le joueur', () => {
    // De l'ordre de la minute et demie, largement au-dessus du temps de
    // lecture d'une étape.
    expect(DELAI_FILET_ANTI_BLOCAGE_CLIC_MS).toBeGreaterThanOrEqual(60_000)
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
