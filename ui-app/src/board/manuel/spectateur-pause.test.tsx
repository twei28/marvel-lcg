// spectateur-pause.test.tsx — I2 (revue finale, 20/09/2026), côté PLATEAU.
//
// ⚠ LA GARANTIE N'EST PAS ICI, elle est dans le moteur : `SpectateurPeutEcrire`
// ferme toutes les routes POST à un spectateur (`web_server.py`), et les
// routes `manuel_pause` / `manuel_passer` exigent en plus un siège
// (`tools/test_mode_manuel.py`, cas `post_ferme_au_spectateur` et
// `pause_refusee_au_spectateur`). Une garde qui ne vivrait que dans
// l'interface n'est pas une garde.
//
// Ce que ce fichier mesure est la POLITESSE : un écran qui ne promet rien
// qu'il ne peut tenir. Pendant une pause, `useTriche` s'armait sur le seul
// `leMoteurSeTait` — donc AUSSI chez le spectateur, qui récupérait le clic
// droit et le clavier du mode manuel sur la partie d'autrui.
import { renderHook } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { useTriche } from '../CoucheTriche'
import { mondeDeTest } from './fixture-monde'

/** Une partie ORDINAIRE en pause : la règle est fausse, l'état est vrai. */
const EN_PAUSE = mondeDeTest({ mode_manuel: false, manuel_actif: true })

const adresse = (recherche: string) =>
  window.history.replaceState({}, '', `/app/board.html${recherche}`)

afterEach(() => adresse(''))

describe('le spectateur ne récupère pas les gestes manuels de la pause (I2)', () => {
  it('n’arme RIEN pendant une pause quand le plateau est celui d’un spectateur', () => {
    adresse('?p=1&spectateur=1')
    const { result } = renderHook(() => useTriche(EN_PAUSE, 0, undefined))
    expect(result.current.actif).toBe(false)
    expect(result.current.manuel).toBe(false)
  })

  it('arme bien les gestes pour un joueur assis (témoin de contrôle)', () => {
    adresse('?p=1')
    const { result } = renderHook(() => useTriche(EN_PAUSE, 0, undefined))
    expect(result.current.actif).toBe(true)
    expect(result.current.manuel).toBe(true)
  })

  it('n’arme pas davantage le bac à sable pour un spectateur', () => {
    adresse('?p=1&spectateur=1')
    const bacASable = mondeDeTest({ mode_sandbox: true })
    const { result } = renderHook(() => useTriche(bacASable, 0, undefined))
    expect(result.current.actif).toBe(false)
  })
})
