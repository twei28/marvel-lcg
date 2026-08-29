// La bascule 🌐 doit emmener TOUT le plateau dans la nouvelle langue. Les
// images des cartes ont leur propre reglage (« Scans en francais ») : tant
// qu'il restait en arriere, passer en anglais donnait une interface anglaise
// sur des cartes francaises — ce qui se lit comme un bug, pas comme un choix.
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { basculerLangue, langueActuelle } from './langue'
import { CLE_SCANS_FR } from './scans-fr'

const CLE_LANGUE = 'marvel-langue'

/** location.reload() n'existe pas dans jsdom, et fetch viserait le moteur. */
function isoler() {
  vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(new Response(''))))
  const reload = vi.fn()
  vi.stubGlobal('location', { ...window.location, reload })
  return reload
}

beforeEach(() => {
  window.localStorage.clear()
  vi.unstubAllGlobals()
})

describe('basculerLangue', () => {
  it('coupe les scans francais en passant en anglais', async () => {
    isoler()
    await basculerLangue()
    expect(window.localStorage.getItem(CLE_LANGUE)).toBe('en')
    expect(window.localStorage.getItem(CLE_SCANS_FR)).toBe('off')
  })

  it('rallume les scans francais en revenant au francais', async () => {
    isoler()
    window.localStorage.setItem(CLE_LANGUE, 'en')
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    await basculerLangue()
    expect(langueActuelle()).toBe('fr')
    expect(window.localStorage.getItem(CLE_SCANS_FR)).toBe('on')
  })

  it('previent le moteur et recharge la page', async () => {
    const reload = isoler()
    await basculerLangue()
    expect(fetch).toHaveBeenCalledWith('/set_language?en')
    expect(reload).toHaveBeenCalledOnce()
  })
})
