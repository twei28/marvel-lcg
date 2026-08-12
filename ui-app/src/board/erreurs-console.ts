// Les erreurs console récentes, gardées pour le rapport de bug.
//
// Une exception de rendu s'affiche une fois dans la console et disparaît avec
// l'onglet. Quand l'utilisateur signale « ça s'est bloqué », c'est souvent la
// seule trace qui existe. On la garde donc en mémoire, plafonnée, sans jamais
// empêcher la console de faire son travail : le module s'INSÈRE devant
// console.error, il ne le remplace pas.

/** Plafond volontairement bas : au-delà, ce sont des répétitions. */
const MAX_ERREURS = 20

let erreurs: string[] = []
let installee = false

function enTexte(valeur: unknown): string {
  if (valeur instanceof Error) return `${valeur.name}: ${valeur.message}`
  if (typeof valeur === 'string') return valeur
  try {
    return JSON.stringify(valeur) ?? String(valeur)
  } catch {
    // Une valeur circulaire ou un objet hostile ne doit pas casser la collecte.
    return String(valeur)
  }
}

function noter(texte: string): void {
  erreurs = [...erreurs, texte].slice(-MAX_ERREURS)
}

/** Les erreurs relevées, de la plus ANCIENNE à la plus récente. */
export function erreursRecentes(): string[] {
  return [...erreurs]
}

/**
 * Vide le relevé. N'existe que pour les tests : en production, la collecte
 * démarre avec la page et s'arrête avec elle.
 */
export function viderErreurs(): void {
  erreurs = []
}

/**
 * Installe la collecte. Rend la fonction qui la désinstalle et remet la console
 * exactement telle qu'elle était. Un second appel sans désinstallation est sans
 * effet : sinon deux montages empileraient deux relais, et chaque erreur serait
 * comptée deux fois.
 */
export function installerCollecteErreurs(): () => void {
  if (installee) return () => undefined
  installee = true

  const originale = console.error
  console.error = (...args: unknown[]) => {
    noter(args.map(enTexte).join(' '))
    originale.apply(console, args as Parameters<typeof console.error>)
  }

  const surErreur = (evenement: ErrorEvent) =>
    noter(`${evenement.message} (${evenement.filename}:${evenement.lineno})`)
  const surRejet = (evenement: PromiseRejectionEvent) =>
    noter(`Promesse rejetée : ${enTexte(evenement.reason)}`)

  window.addEventListener('error', surErreur)
  window.addEventListener('unhandledrejection', surRejet)

  return () => {
    console.error = originale
    window.removeEventListener('error', surErreur)
    window.removeEventListener('unhandledrejection', surRejet)
    installee = false
  }
}
