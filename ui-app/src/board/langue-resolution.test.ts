// La langue du jeu suit le site, puis le navigateur (decision du 26/10/2026) : jumeau TypeScript de
// Fusion/marvel-lcg-src/public/js/prepare/langue-resolution.js. Les deux doivent donner les MEMES resultats sur les memes cas.
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { basculerLangue, langueActuelle } from './langue'
import { cookieLangue, domaineParentCookie, lireCookieLangue, resoudreLangue, type EntreesLangue } from './langue-resolution'
import { CLE_SCANS_FR, scansFrActifs } from './scans-fr'

const nav = (language: string) => ({ language, languages: [language] })

const CAS: [string, EntreesLangue, 'fr' | 'en'][] = [
  ['rien du tout', { stockage: '', cookie: '', navigateur: null }, 'fr'],
  ['navigateur en-US', { stockage: '', cookie: '', navigateur: nav('en-US') }, 'en'],
  ['navigateur fr-FR', { stockage: '', cookie: '', navigateur: nav('fr-FR') }, 'fr'],
  ['navigateur de', { stockage: '', cookie: '', navigateur: nav('de-DE') }, 'fr'],
  ['cookie fr + navigateur en', { stockage: '', cookie: 'nc_langue=fr', navigateur: nav('en-US') }, 'fr'],
  ['cookie en + navigateur fr', { stockage: '', cookie: 'a=1; nc_langue=en; b=2', navigateur: nav('fr-FR') }, 'en'],
  ['stockage en + cookie fr', { stockage: 'en', cookie: 'nc_langue=fr', navigateur: nav('fr-FR') }, 'en'],
  ['stockage fr + cookie en', { stockage: 'fr', cookie: 'nc_langue=en', navigateur: nav('en-US') }, 'fr'],
  ['cookie invalide', { stockage: '', cookie: 'nc_langue=klingon', navigateur: nav('en-GB') }, 'en'],
  ['stockage invalide', { stockage: 'triangles', cookie: 'nc_langue=en', navigateur: nav('fr-FR') }, 'en'],
  ['cookie d\'un autre nom', { stockage: '', cookie: 'langue=en', navigateur: nav('fr-FR') }, 'fr'],
  ['languages[0] seul', { stockage: '', cookie: '', navigateur: { languages: ['en-AU'] } }, 'en'],
]

const HOTES: [string, string][] = [
  ['p1.narwhalchampions.com', '.narwhalchampions.com'],
  ['p12.narwhalchampions.com:443', '.narwhalchampions.com'],
  ['play.narwhalchampions.com', '.narwhalchampions.com'],
  ['www.narwhalchampions.com', '.narwhalchampions.com'],
  ['narwhalchampions.com', '.narwhalchampions.com'],
  ['localhost', ''],
  ['localhost:2345', ''],
  ['127.0.0.1', ''],
  ['192.168.1.20:8080', ''],
  ['[::1]:2345', ''],
  ['', ''],
  ['machin.exemple.org', ''],
]

describe('resoudreLangue (TypeScript)', () => {
  for (const [nom, entrees, attendu] of CAS) {
    it(nom, () => expect(resoudreLangue(entrees)).toBe(attendu))
  }
  it('lireCookieLangue : seulement fr / en, au bon nom', () => {
    expect(lireCookieLangue('nc_langue=en')).toBe('en')
    expect(lireCookieLangue('x=1;nc_langue=fr;y=2')).toBe('fr')
    expect(lireCookieLangue('nc_langue=EN')).toBe('')
    expect(lireCookieLangue('xnc_langue=en')).toBe('')
    expect(lireCookieLangue('')).toBe('')
  })
  it('cookieLangue : memes attributs que le site', () => {
    expect(cookieLangue('en', 'p3.narwhalchampions.com', 'https:')).toBe(
      'nc_langue=en; Path=/; Max-Age=31536000; SameSite=Lax; Domain=.narwhalchampions.com; Secure'
    )
    expect(cookieLangue('fr', 'localhost:2345', 'http:')).toBe('nc_langue=fr; Path=/; Max-Age=31536000; SameSite=Lax')
  })
})

describe('jumeau JavaScript identique (public/js/prepare/langue-resolution.js)', () => {
  // vitest refuse d'importer un fichier hors du projet : on lit le texte du module (sans ses « export ») et on l'evalue.
  const chemin = resolve(process.cwd(), '../Fusion/marvel-lcg-src/public/js/prepare/langue-resolution.js')
  const source = readFileSync(chemin, 'utf8').replace(/^export /gm, '')
  const J = new Function(
    `${source}\nreturn { resoudreLangue, domaineParentCookie, cookieLangue, lireCookieLangue }`
  )() as {
    resoudreLangue: (e: EntreesLangue) => string
    domaineParentCookie: (h: string) => string
    cookieLangue: (l: string, h: string, p: string) => string
    lireCookieLangue: (c: string) => string
  }
  it('memes resultats sur les memes cas (langue, domaine parent, cookie)', () => {
    for (const [, entrees] of CAS) expect(J.resoudreLangue(entrees)).toBe(resoudreLangue(entrees))
    for (const [hote] of HOTES) {
      expect(J.domaineParentCookie(hote)).toBe(domaineParentCookie(hote))
      expect(J.cookieLangue('en', hote, 'https:')).toBe(cookieLangue('en', hote, 'https:'))
    }
    for (const c of ['nc_langue=en', 'x=1;nc_langue=fr', 'nc_langue=EN', '', 'nc_langue=klingon']) {
      expect(J.lireCookieLangue(c)).toBe(lireCookieLangue(c))
    }
  })
  it('domaine parent : les memes hotes donnent les memes domaines', () => {
    for (const [hote, attendu] of HOTES) expect(domaineParentCookie(hote)).toBe(attendu)
  })
})

function viderCookies(): void {
  for (const morceau of document.cookie.split(';')) {
    const nom = morceau.split('=')[0].trim()
    if (nom) document.cookie = `${nom}=; Max-Age=0; Path=/`
  }
}

function langueNavigateur(valeur: string): void {
  vi.spyOn(window.navigator, 'language', 'get').mockReturnValue(valeur)
  vi.spyOn(window.navigator, 'languages', 'get').mockReturnValue([valeur])
}

describe('langueActuelle() du plateau', () => {
  beforeEach(() => {
    window.localStorage.clear()
    viderCookies()
  })
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('sans rien : francais', () => {
    langueNavigateur('fr-FR')
    expect(langueActuelle()).toBe('fr')
  })
  it('navigateur en anglais, rien de memorise : anglais', () => {
    langueNavigateur('en-US')
    expect(langueActuelle()).toBe('en')
  })
  it('cookie nc_langue=en du site, navigateur en francais : anglais', () => {
    langueNavigateur('fr-FR')
    document.cookie = 'nc_langue=en; Path=/'
    expect(langueActuelle()).toBe('en')
  })
  it('le choix fait dans le jeu gagne sur le cookie et sur le navigateur', () => {
    langueNavigateur('en-US')
    document.cookie = 'nc_langue=en; Path=/'
    window.localStorage.setItem('marvel-langue', 'fr')
    expect(langueActuelle()).toBe('fr')
  })
  it('stockage bloque (navigation privee) : le cookie puis le navigateur decident encore', () => {
    langueNavigateur('fr-FR')
    document.cookie = 'nc_langue=en; Path=/'
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => {
      throw new Error('bloque')
    })
    expect(langueActuelle()).toBe('en')
  })
})

describe('basculerLangue() ecrit aussi le cookie nc_langue', () => {
  beforeEach(() => {
    window.localStorage.clear()
    viderCookies()
    vi.stubGlobal('fetch', vi.fn(() => Promise.resolve(new Response(''))))
    vi.stubGlobal('location', { ...window.location, reload: vi.fn(), hostname: 'localhost', host: 'localhost', protocol: 'http:' })
  })
  afterEach(() => {
    vi.restoreAllMocks()
    vi.unstubAllGlobals()
  })

  it('passer en anglais pose nc_langue=en (le site et les autres tables suivent)', async () => {
    langueNavigateur('fr-FR')
    await basculerLangue()
    expect(document.cookie).toContain('nc_langue=en')
    expect(window.localStorage.getItem('marvel-langue')).toBe('en')
  })
  it('revenir au francais pose nc_langue=fr', async () => {
    langueNavigateur('en-US')
    window.localStorage.setItem('marvel-langue', 'en')
    await basculerLangue()
    expect(document.cookie).toContain('nc_langue=fr')
  })
})

describe('les scans francais suivent la langue quand rien n\'a ete regle', () => {
  beforeEach(() => {
    window.localStorage.clear()
    viderCookies()
  })
  afterEach(() => vi.restoreAllMocks())

  it('navigateur anglais, aucun reglage : scans francais coupes (interface anglaise = cartes anglaises)', () => {
    langueNavigateur('en-US')
    expect(scansFrActifs()).toBe(false)
  })
  it('navigateur francais, aucun reglage : scans francais actifs (comme avant)', () => {
    langueNavigateur('fr-FR')
    expect(scansFrActifs()).toBe(true)
  })
  it('un reglage explicite gagne toujours', () => {
    langueNavigateur('en-US')
    window.localStorage.setItem(CLE_SCANS_FR, 'on')
    expect(scansFrActifs()).toBe(true)
    langueNavigateur('fr-FR')
    window.localStorage.setItem(CLE_SCANS_FR, 'off')
    expect(scansFrActifs()).toBe(false)
  })
})
