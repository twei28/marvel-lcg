// Le tchat, vu depuis la table : trois fils (general, table, prive), un seul
// transport reseau. Remplace salon.ts (un seul fil, sans UI, retire le
// 12/09/2026) — chantier du 06/11/2026.
//
// ⚠ RIEN ICI NE DOIT POUVOIR INTERROMPRE UNE PARTIE, meme regle que salon.ts :
// site injoignable, moteur sans site derriere, siege sans compte rendent tous
// `actif: false` et le panneau se tait. Aucune exception ne remonte au plateau.

/** Un message d'un des trois fils. */
export type MessageTchat = {
  id: number
  pseudo: string
  texte: string
  /** L'heure telle que le SERVEUR l'a ecrite, en UTC. Voir `heureLocale`. */
  quand: string
  /** Le meme instant, en secondes depuis l'epoque. Absent sur un vieux serveur. */
  quandTs?: number
  /** Les drapeaux de l'AUTEUR au moment de l'envoi, ex. "fr,en". Voir `DRAPEAUX_LANGUES`. */
  langues?: string
}

/**
 * Liste COURTE ET FIXE (decision utilisateur, chantier du 06/11/2026) :
 * code ISO 639-1 -> emoji. Doit rester le miroir exact de `LANGUES_TCHAT`
 * cote serveur (site/orchestrateur.py) — un code absent d'un des deux cotes
 * serait simplement ignore par l'autre, sans planter.
 */
export const DRAPEAUX_LANGUES: Record<string, string> = {
  fr: '🇫🇷', en: '🇬🇧', es: '🇪🇸', de: '🇩🇪', it: '🇮🇹', pt: '🇵🇹',
}

/** Les drapeaux d'un message, prets a afficher ("" si aucun). */
export function drapeauxDuMessage(message: MessageTchat): string {
  if (!message.langues) return ''
  return message.langues
    .split(',')
    .map((code) => DRAPEAUX_LANGUES[code.trim()])
    .filter(Boolean)
    .join('')
}

/** L'heure d'un message, dans le fuseau de CELUI QUI LIT (voir salon.ts : meme piege UTC). */
export function heureLocale(message: MessageTchat, langue = 'fr-FR'): string {
  if (typeof message.quandTs !== 'number' || !isFinite(message.quandTs) || message.quandTs <= 0) {
    return message.quand
  }
  try {
    return new Date(message.quandTs * 1000).toLocaleTimeString(langue, {
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch {
    return message.quand
  }
}

export type FilTchat = 'general' | 'table' | 'prive'

export type VueTchat = {
  /** Faux = pas de tchat ici : pas de site derriere, siege sans compte, ou pas a cette table. */
  actif: boolean
  /** Notre propre pseudo cote compte, absent pour un siege sans compte (table, invite). */
  pseudo?: string
  messages: MessageTchat[]
  /** Identifiant du dernier message lu, a repasser au prochain appel. */
  dernier: number
  /** Pour chaque correspondant prive, l'identifiant du dernier message echange (fil general seulement). */
  prives?: Record<string, number>
  /** Les drapeaux enregistres au PROFIL du compte ("" si anonyme ou aucun choix). */
  mesLangues?: string
}

export type TransportTchat = {
  lire: (fil: FilTchat, depuis: number, avec?: string) => Promise<VueTchat>
  dire: (fil: FilTchat, texte: string, a?: string, langues?: string) => Promise<boolean>
}

const MUET = (depuis: number): VueTchat => ({ actif: false, messages: [], dernier: depuis })

function estUnMessage(brut: unknown): brut is MessageTchat {
  if (typeof brut !== 'object' || brut === null) return false
  const o = brut as Record<string, unknown>
  return (
    typeof o.id === 'number' &&
    typeof o.pseudo === 'string' &&
    typeof o.texte === 'string' &&
    typeof o.quand === 'string'
  )
}

function messagesDepuisBrut(brut: unknown): MessageTchat[] {
  return (Array.isArray(brut) ? brut.filter(estUnMessage) : []).map((m) => {
    // ⚠ Le site nomme le champ `quand_ts`, le plateau `quandTs` : traduit ICI,
    // une fois, pour que personne en aval n'ait a connaitre les deux noms.
    const o = m as unknown as Record<string, unknown>
    const ts = o.quand_ts
    const avecTs = typeof ts === 'number' && isFinite(ts) && ts > 0 ? { ...m, quandTs: ts } : m
    return typeof o.langues === 'string' && o.langues ? { ...avecTs, langues: o.langues } : avecTs
  })
}

function privesDepuisBrut(brut: unknown): Record<string, number> | undefined {
  if (typeof brut !== 'object' || brut === null) return undefined
  const o: Record<string, number> = {}
  for (const [cle, valeur] of Object.entries(brut as Record<string, unknown>)) {
    if (typeof valeur === 'number') o[cle] = valeur
  }
  return o
}

/** Le numero de siege de CE client, lu dans l'URL (`?p=`) — 0 par defaut (l'hote). */
function siegeCourant(): number {
  const brut = new URLSearchParams(window.location.search).get('p')
  const n = brut === null ? 0 : Number(brut)
  return Number.isFinite(n) ? n : 0
}

/**
 * Les pseudos actuellement connectes au site (chantier « creer une table
 * depuis le tchat », 06/11/2026) — reutilise `/get_connectes`, deja ecrit
 * pour l'invitation d'un connecte (13/10/2026) et deja reserve au siege 0
 * titulaire du compte cote serveur. Tolerant aux pannes comme le reste de ce
 * fichier : jamais d'exception, liste vide si indisponible.
 */
export async function listerConnectes(): Promise<string[]> {
  try {
    const reponse = await fetch('/get_connectes', { cache: 'no-store' })
    if (!reponse.ok) return []
    const brut: unknown = await reponse.json()
    if (typeof brut !== 'object' || brut === null) return []
    const o = brut as Record<string, unknown>
    if (o.actif !== true || !Array.isArray(o.connectes)) return []
    return o.connectes.filter((p): p is string => typeof p === 'string')
  } catch {
    return []
  }
}

/**
 * Le transport depuis le PLATEAU : parle au moteur (`get_salon_joueurs`,
 * `post_salon_message`), qui relaie au site en 127.0.0.1 avec le jeton de la
 * partie — voir le commentaire de `_appeler_site` cote serveur. Le fil de
 * table passe aussi par ici (il n'existe que depuis le moteur).
 */
export function transportMoteur(): TransportTchat {
  return {
    async lire(fil, depuis, avec = '') {
      try {
        const params = new URLSearchParams({ depuis: String(depuis) })
        if (fil === 'table') params.set('salon', 'table')
        else if (avec) params.set('avec', avec)
        const reponse = await fetch(`/get_salon_joueurs?${params}`, { cache: 'no-store' })
        if (!reponse.ok) return MUET(depuis)
        const brut: unknown = await reponse.json()
        if (typeof brut !== 'object' || brut === null) return MUET(depuis)
        const o = brut as Record<string, unknown>
        if (o.actif !== true) return MUET(depuis)
        const messages = messagesDepuisBrut(o.messages)
        return {
          actif: true,
          pseudo: typeof o.pseudo === 'string' ? o.pseudo : undefined,
          messages,
          dernier: typeof o.dernier === 'number' ? o.dernier : depuis,
          prives: privesDepuisBrut(o.prives),
          mesLangues: typeof o.mes_langues === 'string' ? o.mes_langues : undefined,
        }
      } catch {
        return MUET(depuis)
      }
    },
    async dire(fil, texte, a = '', langues = '') {
      if (!texte.trim()) return false
      try {
        const corps: Record<string, unknown> = { texte, langues }
        if (fil === 'table') {
          corps.salon = 'table'
          corps.siege = siegeCourant()
        } else if (a) {
          corps.a = a
        }
        const reponse = await fetch('/post_salon_message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(corps),
        })
        return reponse.ok
      } catch {
        return false
      }
    },
  }
}

/**
 * Le transport depuis PLAY (chantier du 06/11/2026) : Play n'a pas de moteur
 * derriere lui (le moteur tourne dans le navigateur, Pyodide) donc pas de
 * relais possible vers `/get_salon_joueurs` — on appelle directement le SITE
 * PRINCIPAL (`/tchat/vue`, `/tchat/dire`), avec un pseudo tape une seule fois
 * par le visiteur (Play n'a pas de compte) et garde par l'appelant — voir
 * `lirePseudoPlay`/`ecrirePseudoPlay` ci-dessous. Cote serveur, ces deux
 * routes acceptent deja un visiteur sans compte (`pseudo_anonyme_valide`) et
 * portent les en-tetes CORS/CORP necessaires pour une autre origine
 * (`_entetes_tchat_play`, orchestrateur.py).
 *
 * ⚠ NI FIL DE TABLE NI MESSAGES PRIVES ICI. Un visiteur anonyme n'a pas de
 * table partagee par ce chemin (« Coop en ligne » passe par le site, pas par
 * ce transport), et le serveur refuse deja les MP sans compte — inutile de
 * tenter l'appel pour echouer a chaque fois.
 */
export function transportSiteDirect(origine: string, pseudo: () => string): TransportTchat {
  return {
    async lire(fil, depuis) {
      if (fil !== 'general') return MUET(depuis)
      const moi = pseudo()
      if (!moi) return MUET(depuis)
      try {
        const params = new URLSearchParams({ depuis: String(depuis), pseudo: moi })
        const reponse = await fetch(`${origine}/tchat/vue?${params}`, { cache: 'no-store', credentials: 'omit' })
        if (!reponse.ok) return MUET(depuis)
        const brut: unknown = await reponse.json()
        if (typeof brut !== 'object' || brut === null) return MUET(depuis)
        const o = brut as Record<string, unknown>
        return {
          actif: true,
          pseudo: typeof o.pseudo === 'string' ? o.pseudo : moi,
          messages: messagesDepuisBrut(o.messages),
          dernier: typeof o.dernier === 'number' ? o.dernier : depuis,
        }
      } catch {
        return MUET(depuis)
      }
    },
    async dire(fil, texte, a = '', langues = '') {
      if (fil !== 'general' || a || !texte.trim()) return false
      const moi = pseudo()
      if (!moi) return false
      try {
        const corps = new URLSearchParams({ texte, langues, pseudo: moi })
        const reponse = await fetch(`${origine}/tchat/dire`, {
          method: 'POST',
          credentials: 'omit',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: corps,
        })
        return reponse.ok
      } catch {
        return false
      }
    },
  }
}

const CLE_PSEUDO_PLAY = 'marvel-tchat-pseudo-play'

/** Le pseudo choisi par CE visiteur de Play, "" si jamais demande/stockage indisponible. */
export function lirePseudoPlay(): string {
  try {
    return window.localStorage.getItem(CLE_PSEUDO_PLAY) || ''
  } catch {
    return ''
  }
}

export function ecrirePseudoPlay(pseudo: string): void {
  try {
    window.localStorage.setItem(CLE_PSEUDO_PLAY, pseudo)
  } catch {
    // stockage indisponible : la demande reapparaitra au prochain essai, rien de plus grave.
  }
}

const CLE_LANGUES_CHOISIES = 'marvel-tchat-langues'

/** Les drapeaux choisis par CE navigateur, "" si aucun/stockage indisponible. */
export function lireLanguesChoisies(): string {
  try {
    return window.localStorage.getItem(CLE_LANGUES_CHOISIES) || ''
  } catch {
    return ''
  }
}

export function ecrireLanguesChoisies(langues: string): void {
  try {
    window.localStorage.setItem(CLE_LANGUES_CHOISIES, langues)
  } catch {
    // stockage indisponible (navigation privee...) : le choix ne survivra
    // pas au rechargement, rien de plus grave.
  }
}

const CLE_CONVERSATIONS_FERMEES = 'marvel-tchat-fermees'

/**
 * Conversations privees fermees par CE navigateur (demande du 06/11/2026) :
 * pseudo -> identifiant du dernier message connu au moment de la fermeture.
 * Rien n'est efface cote serveur, seul l'onglet disparait ICI tant qu'aucun
 * message plus recent que cet identifiant n'arrive (voir VoletTchat.tsx).
 */
export function lireConversationsFermees(): Record<string, number> {
  try {
    const brut = window.localStorage.getItem(CLE_CONVERSATIONS_FERMEES)
    if (!brut) return {}
    const o: unknown = JSON.parse(brut)
    if (typeof o !== 'object' || o === null) return {}
    const net: Record<string, number> = {}
    for (const [pseudo, id] of Object.entries(o as Record<string, unknown>)) {
      if (typeof id === 'number') net[pseudo] = id
    }
    return net
  } catch {
    return {}
  }
}

export function ecrireConversationsFermees(fermees: Record<string, number>): void {
  try {
    window.localStorage.setItem(CLE_CONVERSATIONS_FERMEES, JSON.stringify(fermees))
  } catch {
    // stockage indisponible : la fermeture ne survivra pas au rechargement.
  }
}
