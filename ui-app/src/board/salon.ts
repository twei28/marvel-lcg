// Le canal du tchat, vu depuis la table.
//
// Le navigateur du plateau est servi depuis `p<N>.<domaine>` et le site depuis
// `<domaine>` : un appel direct serait croise, et le cookie de session du site
// ne voyagerait pas. On parle donc au MOTEUR, qui relaie en 127.0.0.1 avec le
// jeton de la partie (voir `_appeler_site` dans server_get.py).
//
// ⚠ RIEN ICI NE DOIT POUVOIR INTERROMPRE UNE PARTIE. Site injoignable, moteur
// sans site derriere, siege qui n'est pas celui du titulaire du compte : tous
// ces cas rendent `actif: false` et le panneau se tait. Aucune exception ne
// remonte au plateau.

/** Un message du tchat des comptes. */
export type MessageSalon = {
  id: number
  pseudo: string
  texte: string
  /**
   * L'heure telle que le SERVEUR l'a ecrite, en UTC (« 21:30 »).
   * ⚠ NE PAS L'AFFICHER : le serveur tourne en UTC, le joueur non. Passer par
   * `heureLocale()`, qui se sert de `quandTs`. Ce champ ne reste que parce que
   * d'anciens clients le lisent encore.
   */
  quand: string
  /**
   * Le meme instant, en secondes depuis l'epoque. Absent des serveurs d'avant
   * le 14/09/2026 : `heureLocale()` retombe alors sur `quand`.
   */
  quandTs?: number
}

/**
 * L'heure d'un message, dans le fuseau de CELUI QUI LIT.
 *
 * ⚠ Personne d'autre que le navigateur ne connait ce fuseau. Le serveur tourne
 * en `Etc/UTC` : afficher son heure telle quelle montrait 05:26 a quelqu'un
 * dont la montre disait 07:26 (constate le 14/09/2026). On ne corrige pas d'un
 * decalage fixe non plus : ce serait juste pour la Belgique et faux ailleurs.
 *
 * Sans instant (vieux serveur), on rend la chaine brute plutot que rien : une
 * heure decalee reste plus utile qu'une absence d'heure.
 */
export function heureLocale(message: MessageSalon, langue = 'fr-FR'): string {
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

export type VueSalon = {
  /** Faux = pas de tchat ici : pas de site derriere, ou siege sans compte. */
  actif: boolean
  /** Notre propre pseudo, pour distinguer nos messages de ceux des autres. */
  pseudo?: string
  messages: MessageSalon[]
  /** Identifiant du dernier message lu, a repasser au prochain appel. */
  dernier: number
}

const MUET = (depuis: number): VueSalon => ({ actif: false, messages: [], dernier: depuis })

function estUnMessage(brut: unknown): brut is MessageSalon {
  if (typeof brut !== 'object' || brut === null) return false
  const o = brut as Record<string, unknown>
  return (
    typeof o.id === 'number' &&
    typeof o.pseudo === 'string' &&
    typeof o.texte === 'string' &&
    typeof o.quand === 'string'
  )
}

/**
 * Les messages arrives APRES `depuis`. Le moteur ne renvoie que la suite : le
 * fil n'est pas reconstruit a chaque tour.
 */
export async function lireSalon(depuis: number): Promise<VueSalon> {
  try {
    const reponse = await fetch(`/get_salon_joueurs?depuis=${depuis}`, { cache: 'no-store' })
    if (!reponse.ok) return MUET(depuis)
    const brut: unknown = await reponse.json()
    if (typeof brut !== 'object' || brut === null) return MUET(depuis)
    const o = brut as Record<string, unknown>
    if (o.actif !== true) return MUET(depuis)
    // ⚠ Le site nomme le champ `quand_ts`, le plateau `quandTs` : on traduit
    // ICI, une fois, pour que personne en aval n'ait a connaitre les deux noms.
    // Absent sur un serveur d'avant le 14/09/2026, et c'est pris en charge par
    // `heureLocale`.
    const messages = (Array.isArray(o.messages) ? o.messages.filter(estUnMessage) : [])
      .map((m) => {
        const brut = (m as unknown as Record<string, unknown>).quand_ts
        return typeof brut === 'number' && isFinite(brut) && brut > 0
          ? { ...m, quandTs: brut }
          : m
      })
    return {
      actif: true,
      pseudo: typeof o.pseudo === 'string' ? o.pseudo : undefined,
      messages,
      // Le curseur ne recule jamais : sans lui, on relirait tout le fil.
      dernier: typeof o.dernier === 'number' ? o.dernier : depuis,
    }
  } catch {
    return MUET(depuis)
  }
}

/** Envoie un message dans le tchat general. Rend faux si rien n'est parti. */
export async function direSalon(texte: string): Promise<boolean> {
  if (!texte.trim()) return false
  try {
    const reponse = await fetch('/post_salon_message', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texte }),
    })
    return reponse.ok
  } catch {
    return false
  }
}
