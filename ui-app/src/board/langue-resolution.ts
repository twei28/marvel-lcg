// langue-resolution.ts — la langue du jeu, de façon PURE (sans DOM, sans stockage).
//
// Jumeau de Fusion/marvel-lcg-src/public/js/prepare/langue-resolution.js : mêmes règles, mêmes résultats (comparés par
// langue-resolution.test.ts). Décision du 26/10/2026 : sur une table en ligne (p<N>.<domaine>, autre origine que le site), la
// langue suit, dans cet ordre : le choix déjà fait dans le jeu (« marvel-langue »), le cookie « nc_langue » posé par le site
// (Domain=.<domaine>), la langue du navigateur (« en… » = anglais), le français. Le jeu écrit aussi ce cookie quand le joueur
// change de langue.

export type LangueResolue = 'fr' | 'en'

export interface EntreesLangue {
  stockage?: string | null
  cookie?: string | null
  navigateur?: { language?: string; languages?: readonly string[] } | null
}

export const COOKIE_LANGUE = 'nc_langue'
const DUREE_COOKIE_S = 31536000 // un an, comme le site

/** « en » ou « fr » ; tout le reste → ''. */
export function langueValide(valeur: unknown): LangueResolue | '' {
  return valeur === 'en' || valeur === 'fr' ? valeur : ''
}

/** La langue portée par le cookie nc_langue d'un `document.cookie`, ou ''. */
export function lireCookieLangue(cookie: string | null | undefined): LangueResolue | '' {
  for (const morceau of String(cookie || '').split(';')) {
    const i = morceau.indexOf('=')
    if (i < 0) continue
    if (morceau.slice(0, i).trim() === COOKIE_LANGUE) {
      const valeur = morceau.slice(i + 1).trim()
      if (valeur === 'en' || valeur === 'fr') return valeur
    }
  }
  return ''
}

/** « en » si le navigateur est en anglais, sinon « fr ». */
export function langueDuNavigateur(navigateur: EntreesLangue['navigateur']): LangueResolue {
  const l = String((navigateur && (navigateur.language || (navigateur.languages && navigateur.languages[0]))) || '').toLowerCase()
  return l.startsWith('en') ? 'en' : 'fr'
}

/** { stockage, cookie, navigateur } → « fr » | « en ». */
export function resoudreLangue(entrees?: EntreesLangue | null): LangueResolue {
  const e = entrees || {}
  const stockee = langueValide(e.stockage)
  if (stockee) return stockee
  const cookie = lireCookieLangue(e.cookie)
  if (cookie) return cookie
  return langueDuNavigateur(e.navigateur)
}

/** Le « Domain= » du cookie de langue pour cet hôte (le domaine PARENT, comme le site), ou '' (pas de Domain). */
export function domaineParentCookie(hote: string | null | undefined): string {
  const brut = String(hote || '').trim().toLowerCase()
  if (!brut) return ''
  if (brut.startsWith('[')) return '' // IPv6
  const sansPort = brut.replace(/:\d+$/, '')
  if (!sansPort || sansPort.includes(':')) return ''
  if (/^\d+(\.\d+){3}$/.test(sansPort)) return '' // IPv4
  const etiquettes = sansPort.split('.')
  if (etiquettes.length < 2 || etiquettes.some((x) => !x)) return ''
  if (etiquettes.length >= 3 && /^(p\d+|play|www)$/.test(etiquettes[0])) return '.' + etiquettes.slice(1).join('.')
  if (etiquettes.length === 2) return '.' + sansPort
  return ''
}

/** La valeur à écrire dans `document.cookie` : mêmes attributs que le site. */
export function cookieLangue(langue: string, hote: string, protocole: string): string {
  const l = langue === 'en' ? 'en' : 'fr'
  let cookie = `${COOKIE_LANGUE}=${l}; Path=/; Max-Age=${DUREE_COOKIE_S}; SameSite=Lax`
  const domaine = domaineParentCookie(hote)
  if (domaine) cookie += `; Domain=${domaine}`
  if (protocole === 'https:') cookie += '; Secure'
  return cookie
}
