// LES REGLAGES DU PLATEAU, GARDES SUR LE COMPTE (14/11/2026, demande des
// joueurs : retrouver ses reglages sur un autre appareil). Chaque reglage est
// une cle du localStorage, rangee TELLE QUELLE dans les preferences du compte
// (`/get_preferences`, `/save_preferences`). Contrat, cle par cle :
//   - le compte a la cle : il fait foi, le navigateur prend sa valeur ;
//   - le compte ne l'a pas, le navigateur si : le navigateur la VERSE au
//     compte (c'est ainsi que les reglages d'avant cette mise a jour sont
//     recuperes, a la premiere visite) ;
//   - invite, hors site ou cadre de spectateur : le navigateur reste seul.
// Ensuite chaque changement fait dans le navigateur part vers le compte.
// La liste est FERMEE et doit rester identique a `REGLAGES_CLES` du serveur
// (server_get.py) : reglages-compte.test.ts compare les deux.
import { estCadre } from './cadre-joueur'

export const REGLAGES_DU_COMPTE: readonly string[] = [
  'marvel-board-action-mode',
  'marvel-board-animations',
  'marvel-board-annuler-explique',
  'marvel-board-auto-cible',
  'marvel-board-avance-auto',
  'marvel-board-curseurs',
  'marvel-board-delai-pas-a-pas',
  'marvel-board-dos-cartes',
  'marvel-board-facon-de-jouer',
  'marvel-board-fin-tour-auto',
  'marvel-board-meteo',
  'marvel-board-mode-phase-mechant',
  'marvel-board-musique',
  'marvel-board-paiement-auto',
  'marvel-board-phase-auto',
  'marvel-board-phase-rapide',
  'marvel-board-piste-phases',
  'marvel-board-revelation',
  'marvel-board-sauvegarde-auto',
  'marvel-board-scans-fr',
  'marvel-board-sons',
  'marvel-board-tutoriel',
  'marvel-board-validation-courte',
  'marvel-board-volume-musique',
  'marvel-board-volume-sons',
  'marvel-encoche-gauche',
  'marvel-tel-aide-debut',
  'marvel-tel-colonnes-zones',
  'marvel-tel-plateau',
  'marvel-tel-plateau-choisi',
  'marvel-tel-plateau-memorise',
  'marvel-tel-taille-texte',
  'marvel-tel-verrou-portrait',
  'marvel-tel-vibrations',
  'marvel-tel-visite-piles',
  'mc_aide_bulle_table',
  'mc_ameliorations_chevauchement',
  'mc_ameliorations_cote',
  'mc_apercu_zoom',
  'mc_barre_avantage',
  'mc_card_art_v1',
  'mc_etiquettes_table',
  'mc_noms_zones_v1',
  'mc_phase_bis',
  'mc_phase_presentation',
  'mc_piles_inversees',
  'mc_resource_art_v1',
  'mc_traits_pastilles',
]

/** Meme borne que le serveur : au-dela, la valeur reste dans le navigateur. */
export const REGLAGE_LONGUEUR_MAX = 2000
/** Le serveur refuse plus de 60 changements par appel. */
const CHANGEMENTS_PAR_APPEL = 60

type Reglages = Record<string, string>
type Changements = Record<string, string | null>

/** Le serveur garderait-il cette valeur ? (texte court, sans caractere de controle) */
export function reglageValide(valeur: unknown): valeur is string {
  // eslint-disable-next-line no-control-regex
  return typeof valeur === 'string' && valeur.length <= REGLAGE_LONGUEUR_MAX && !/[\x00-\x1f\x7f]/.test(valeur)
}

/** Les reglages du navigateur que le compte peut garder. */
export function lireReglages(stockage: Storage = window.localStorage): Reglages {
  const reglages: Reglages = {}
  try {
    for (const cle of REGLAGES_DU_COMPTE) {
      const valeur = stockage.getItem(cle)
      if (reglageValide(valeur)) reglages[cle] = valeur
    }
  } catch {
    // Stockage refuse : rien a garder.
  }
  return reglages
}

/**
 * Rapproche le compte et le navigateur, cle par cle : ce que le navigateur doit
 * prendre du compte, et ce qu'il doit lui verser (les cles que le compte n'a pas).
 */
export function rapprocher(compte: Record<string, unknown>, navigateur: Reglages): { versNavigateur: Reglages; versCompte: Reglages } {
  const versNavigateur: Reglages = {}
  const versCompte: Reglages = {}
  for (const cle of REGLAGES_DU_COMPTE) {
    const duCompte = compte[cle]
    if (reglageValide(duCompte)) {
      if (navigateur[cle] !== duCompte) versNavigateur[cle] = duCompte
    } else if (cle in navigateur) {
      versCompte[cle] = navigateur[cle]
    }
  }
  return { versNavigateur, versCompte }
}

/** Ce qui a change entre deux releves du navigateur (`null` = reglage efface). */
export function changementsDepuis(avant: Reglages, apres: Reglages): Changements {
  const changements: Changements = {}
  for (const cle of REGLAGES_DU_COMPTE) {
    if (avant[cle] === apres[cle]) continue
    changements[cle] = cle in apres ? apres[cle] : null
  }
  return changements
}

function envoyer(changements: Changements, enPartant = false): void {
  const cles = Object.keys(changements)
  for (let i = 0; i < cles.length; i += CHANGEMENTS_PAR_APPEL) {
    const lot: Changements = {}
    for (const cle of cles.slice(i, i + CHANGEMENTS_PAR_APPEL)) lot[cle] = changements[cle]
    void fetch('/save_preferences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ changements: lot }),
      keepalive: enPartant,
    }).catch(() => undefined)
  }
}

/** Le navigateur prend les valeurs du compte, et le dit a ceux qui ecoutent `storage`. */
function poserDansLeNavigateur(reglages: Reglages): void {
  for (const [cle, valeur] of Object.entries(reglages)) {
    try {
      const ancienne = window.localStorage.getItem(cle)
      window.localStorage.setItem(cle, valeur)
      window.dispatchEvent(new StorageEvent('storage', { key: cle, oldValue: ancienne, newValue: valeur }))
    } catch {
      // Stockage refuse : le reglage du compte ne vaut que pour cette visite.
    }
  }
}

const RELEVE_MS = 4000
let suivi = false

/** Surveille le navigateur : tout reglage change part vers le compte. */
function suivre(): void {
  if (suivi) return
  suivi = true
  let releve = lireReglages()
  const relever = (enPartant = false) => {
    const maintenant = lireReglages()
    const changements = changementsDepuis(releve, maintenant)
    releve = maintenant
    if (Object.keys(changements).length) envoyer(changements, enPartant)
  }
  window.setInterval(relever, RELEVE_MS)
  window.addEventListener('pagehide', () => relever(true))
}

/**
 * Au chargement du plateau : rapproche le navigateur et le compte, puis suit
 * les changements. La promesse se resout des que le navigateur a les reglages
 * du compte, ou apres `delaiMs` (le plateau n'attend pas un serveur lent : les
 * reglages arrives ensuite sont poses quand meme, et vus par ceux qui ecoutent).
 */
export function chargerReglagesDuCompte(delaiMs = 1500): Promise<void> {
  if (typeof window === 'undefined' || estCadre()) return Promise.resolve()
  const rapprochement = (async () => {
    try {
      const reponse = await fetch('/get_preferences', { cache: 'no-store' })
      if (!reponse.ok) return
      const corps = (await reponse.json()) as { compte?: boolean; preferences?: Record<string, unknown> }
      if (!corps || !corps.compte) return
      const { versNavigateur, versCompte } = rapprocher(corps.preferences ?? {}, lireReglages())
      poserDansLeNavigateur(versNavigateur)
      if (Object.keys(versCompte).length) envoyer(versCompte)
      suivre()
    } catch {
      // Hors ligne, hors site : le navigateur reste la reference.
    }
  })()
  return Promise.race([rapprochement, new Promise<void>((fin) => window.setTimeout(fin, delaiMs))])
}
