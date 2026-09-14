// Le mode « Sur la table » : même rythme que « Détaillé », autre mise en scène.
//
// ⚠ LE CAS QUI COMPTE LE PLUS est `il RETIENT la trame comme « détaillé' »`.
// Les deux modes attendent un clic par étape ; ils ne diffèrent que par
// l'endroit où l'étape est racontée. Écrire la règle du rythme sur le seul nom
// « detaille » ferait défiler toute la phase d'un coup, sans un clic : c'est
// exactement le défaut mesuré en partie réelle le 07/09/2026 et corrigé dans
// `setModePhaseMechant`.
//
// ⚠ ET L'INVERSE COMPTE AUTANT : un mode qui retient sans afficher de
// cartouche bloque la partie jusqu'au filet anti-blocage de 90 secondes,
// puisque le cartouche est le SEUL à relâcher les trames retenues. C'est la
// raison pour laquelle `unCartouche` (board.tsx) inclut « sur-table ».
import { beforeEach, describe, expect, it } from 'vitest'
import {
  CLE_MODE_PHASE,
  decisionAccuse,
  lireModePhaseMechant,
  MODE_SUR_TABLE_OUVERT,
  libelleModePhase,
  MODES,
  PHASES_DU_MECHANT,
  type ModePhaseMechant,
} from './moteur'
import type { World } from './world'

const monde = (phase: string) => ({ phase }) as unknown as World

describe('le rythme du mode « Sur la table »', () => {
  it('retient la trame sur les QUATRE phases du méchant, comme « Détaillé »', () => {
    for (const phase of PHASES_DU_MECHANT) {
      expect(decisionAccuse('sur-table', monde(phase)), phase).toBe('attendre-clic')
    }
  })

  it('exactement la même décision que « Détaillé », phase par phase', () => {
    // Le test qui tient la promesse du mode : « je ne veux pas que ça se
    // déroule seul » (utilisateur, 14/09/2026). Si un jour les deux divergent,
    // c'est ici qu'on l'apprend.
    for (const phase of [...PHASES_DU_MECHANT, 'Player Turn', 'Setup', '']) {
      expect(decisionAccuse('sur-table', monde(phase)), phase).toBe(
        decisionAccuse('detaille', monde(phase))
      )
    }
  })

  it('ne retient rien hors de la phase du méchant', () => {
    expect(decisionAccuse('sur-table', monde('Player Turn'))).toBe('immediat')
  })

  it('un monde absent ne fait rien retenir', () => {
    // Première trame, monde pas encore reçu : retenir ici bloquerait la partie
    // avant même qu'elle commence.
    expect(decisionAccuse('sur-table', undefined)).toBe('immediat')
  })
})

describe('sa place parmi les modes', () => {
  it('figure dans la liste, entre « Détaillé » et « Instantané »', () => {
    expect(MODES).toEqual(['detaille', 'sur-table', 'instantane'])
  })

  it('porte son propre libellé', () => {
    expect(libelleModePhase('sur-table')).toBe('Sur la table')
  })

  it('les trois modes ont chacun un libellé distinct', () => {
    // Un `switch` sans branche pour un mode rendait autrefois le libellé d'un
    // autre, et le panneau Options affichait « Instantané » pour « Détaillé ».
    const libelles = MODES.map((m: ModePhaseMechant) => libelleModePhase(m))
    expect(new Set(libelles).size).toBe(MODES.length)
  })
})

describe('le mode est FERMÉ pendant le chantier', () => {
  // ⚠ Retiré le 14/09/2026 à la demande de l'utilisateur, après la première
  // partie jouée dedans : « je le retire jusqu'à ce que ce soit prêt ».
  //
  // ⚠ LE CAS QUI COMPTE est `celui qui l'avait choisi ne reste pas coincé`.
  // Le mode ne paraît plus dans les Réglages : s'il restait actif dans le
  // stockage, le joueur continuerait de jouer un mode en chantier sans aucun
  // moyen d'en sortir.
  beforeEach(() => window.localStorage.clear())

  it('l’interrupteur est bien fermé', () => {
    expect(MODE_SUR_TABLE_OUVERT).toBe(false)
  })

  it('un stockage qui porte « sur-table » retombe sur « Détaillé »', () => {
    window.localStorage.setItem(CLE_MODE_PHASE, 'sur-table')
    expect(lireModePhaseMechant()).toBe('detaille')
  })

  it('les deux autres modes ne sont pas touchés', () => {
    window.localStorage.setItem(CLE_MODE_PHASE, 'instantane')
    expect(lireModePhaseMechant()).toBe('instantane')
    window.localStorage.setItem(CLE_MODE_PHASE, 'detaille')
    expect(lireModePhaseMechant()).toBe('detaille')
  })

  it('le code du mode reste en place : c’est un interrupteur, pas une suppression', () => {
    // `decisionAccuse` sait toujours le traiter, et le type le connaît encore.
    expect(MODES).toContain('sur-table')
    expect(decisionAccuse('sur-table', monde('Enemy Activation'))).toBe('attendre-clic')
  })
})
