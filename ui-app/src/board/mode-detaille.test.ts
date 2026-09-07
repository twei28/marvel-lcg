// Le mode « Detaille » existe, et c'est celui qu'on a en arrivant.
//
// Il remplace « manuel » comme defaut : la phase du mechant se deroule
// desormais etape par etape a moins qu'on ne demande explicitement d'aller
// plus vite. Les anciens modes « manuel » et « pas-a-pas » ont disparu : il ne
// reste que « detaille » (avec son reglage « avance auto ») et « instantane ».
import { describe, expect, it } from 'vitest'
import {
  lireAvanceAuto,
  libelleModePhase,
  lireModePhaseMechant,
  lireTrame,
  MODES,
} from './moteur'

describe('mode detaille', () => {
  it('figure dans la liste des modes', () => {
    expect(MODES).toContain('detaille')
  })

  it('est le mode par defaut, sans rien de memorise', () => {
    window.localStorage.clear()
    expect(lireModePhaseMechant()).toBe('detaille')
  })

  // L'avance auto est ETEINTE par defaut : ce joueur cliquait pour avancer, il
  // continue de cliquer. La migration depuis l'ancienne case a cocher
  // (« marvel-board-phase-rapide ») ne se joue plus ici : cette cle n'est plus
  // lue du tout depuis 56c0e530, et c'est pas-a-pas.test.ts qui prouve qu'elle
  // ne reveille plus rien.
  it('n allume pas l avance auto par defaut', () => {
    window.localStorage.clear()
    expect(lireModePhaseMechant()).toBe('detaille')
    expect(lireAvanceAuto()).toBe(false)
  })

  // Ne garde plus que DEUX positions : « manuel » et « pas-a-pas » ont
  // disparu (le premier n'apportait rien que « detaille » ne fasse deja
  // mieux, le second est devenu le reglage « avance auto »).
  it('ne garde que deux positions', () => {
    expect(MODES).toEqual(['detaille', 'instantane'])
  })

  it('affiche son propre libelle, pas celui d un autre mode', () => {
    // Le panneau Options affichait « Instantane » pour le mode detaille,
    // pourtant le defaut : un ternaire a trois branches sans branche pour lui.
    expect(libelleModePhase('detaille')).toBe('Détaillé')
    expect(libelleModePhase('instantane')).toBe('Instantané')
  })
})

// L'HYPOTHESE DU MODE DETAILLE, ET CE QUI LA CASSE.
//
// Le mode suppose que le moteur ne produit rien tant qu'on ne lui a pas
// repondu : `DoWaitSync` et `DoGetInput` attendent alors sans limite. C'est
// vrai tant que « Temps par decision » vaut 0 (le defaut de la preparation de
// mission). Non nul, les deux attentes EXPIRENT et le moteur poursuit seul,
// sans notre accuse ni notre reponse. La trame le publie sous `max_timeout`,
// en secondes : c'est la seule chose que le plateau peut en savoir.
describe('le temps par decision publie par la trame', () => {
  const trame = (extra: Record<string, unknown> = {}) =>
    lireTrame({ render_id: 7, game_id: 1, ask_players: [], ...extra })

  it('vaut zero par defaut, c est-a-dire sans limite', () => {
    expect(trame()?.maxTimeout).toBe(0)
    expect(trame({ max_timeout: 0 })?.maxTimeout).toBe(0)
  })

  it('rend le delai regle a la preparation', () => {
    expect(trame({ max_timeout: 30 })?.maxTimeout).toBe(30)
  })

  // Un moteur ancien, ou un champ abime : on retombe sur « sans limite »
  // plutot que sur une mention qui ne serait pas vraie.
  it('retombe sur zero devant une valeur qui n est pas un nombre', () => {
    expect(trame({ max_timeout: '30' })?.maxTimeout).toBe(0)
    expect(trame({ max_timeout: null })?.maxTimeout).toBe(0)
  })
})
