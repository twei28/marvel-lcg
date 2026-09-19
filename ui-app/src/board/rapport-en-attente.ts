// rapport-en-attente.ts — le signalement qui n'est pas parti, gardé pour plus tard.
//
// Pourquoi ce module existe (19/09/2026) : un joueur a signalé un bug, et il
// n'en restait AUCUNE trace, ni chez lui ni sur le serveur. Le panneau dit
// pourtant quand un envoi échoue, mais dire ne suffit pas : l'onglet se ferme,
// la table s'éteint, et le texte est perdu avec. Ce qu'on a écrit une fois ne
// doit pas être à réécrire.
//
// ⚠ TOUT PASSE PAR try/catch. En navigation privée, dans une iframe bac à
// sable, ou avec les données de site bloquées, le stockage local LÈVE au lieu
// de rendre null. Un signalement raté ne doit pas, en plus, casser le plateau.

const CLE = 'marvel-rapport-en-attente'

export type RapportEnAttente = {
  nom: string
  description: string
  /** Vide quand la capture n'a pas pu être gardée, jamais absent. */
  capture: string
}

/** Ce qui a pu être mis de côté. */
export type Garde = 'tout' | 'sans-capture' | 'rien'

export function garder(rapport: RapportEnAttente): Garde {
  // Premier essai avec la capture. Elle pèse jusqu'à quatre mégaoctets en
  // base64 et le stockage en tient environ cinq : c'est elle, et elle seule,
  // qui peut faire déborder.
  try {
    window.localStorage.setItem(CLE, JSON.stringify(rapport))
    return 'tout'
  } catch {
    /* on retente sans elle */
  }
  try {
    window.localStorage.setItem(CLE, JSON.stringify({ ...rapport, capture: '' }))
    return 'sans-capture'
  } catch {
    // Stockage interdit : on ne peut rien garder, et c'est à l'appelant de le
    // dire au joueur plutôt que de lui laisser croire que c'est en sûreté.
    return 'rien'
  }
}

export function lire(): RapportEnAttente | undefined {
  let brut: string | null = null
  try {
    brut = window.localStorage.getItem(CLE)
  } catch {
    return undefined
  }
  if (!brut) return undefined
  try {
    const lu = JSON.parse(brut) as Partial<RapportEnAttente>
    // Un contenu illisible ou tronqué ne doit pas ressusciter un demi-rapport :
    // sans description il n'y a rien à renvoyer.
    if (!lu || typeof lu.description !== 'string' || !lu.description) return undefined
    return {
      nom: typeof lu.nom === 'string' ? lu.nom : '',
      description: lu.description,
      capture: typeof lu.capture === 'string' ? lu.capture : '',
    }
  } catch {
    return undefined
  }
}

export function oublier(): void {
  try {
    window.localStorage.removeItem(CLE)
  } catch {
    /* rien à oublier si on ne peut pas y toucher */
  }
}
