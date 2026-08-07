// Contexte de campagne du plateau — « cette partie appartient-elle à une
// campagne, et si oui laquelle ? »
//
// Le plateau n'a aucun moyen de le déduire tout seul : la partie qu'il affiche
// ressemble à n'importe quelle autre. C'est l'écran des campagnes qui le lui
// dit, en déposant une clé avant de rediriger — même mécanique que le coach du
// mode Découverte (voir CoucheCoach). La clé est effacée dès que les
// récompenses sont validées, pour qu'une partie hors campagne lancée ensuite
// n'hérite pas du contexte de la précédente.
import type { ChampVictoire } from './detecteurs'

/** Clé posée par public/js/campagne/app.js juste avant de lancer un scénario. */
export const CLE_CAMPAGNE = 'mc-campagne-partie'

export type ContexteCampagne = {
  /** Identifiant de la campagne côté serveur. */
  id: string
  /** Identifiant du scénario en cours (« crossbones »). */
  scenario: string
}

export type ScenarioCampagne = {
  id: string
  numero: number
  nom: string
  nom_fr?: string
  resume?: string
  enjeu?: string
  final?: boolean
  pages?: { intro?: string[]; regles?: string[]; epilogue?: string[] }
  victoire?: ChampVictoire[]
}

export type DefinitionCampagne = {
  code: string
  nom: string
  nom_en?: string
  cle_extension: string
  scenarios: ScenarioCampagne[]
  /** Champs présentés à CHAQUE victoire, sauf le scénario final. */
  victoire_commune?: ChampVictoire[]
  victoire_commune_expert?: ChampVictoire[]
  expert?: { pv_persistants?: boolean; obligations?: string[] }
}

export type Campagne = {
  id: string
  code: string
  nom: string
  difficulte?: 'standard' | 'expert'
  equipe?: Array<{ heros?: string; nomHeros?: string; identite?: string[]; deck?: unknown }>
  termines?: string[]
  carnet?: Record<string, string>
  tentatives?: Record<string, number>
  partieEnCours?: { scenario: string; depuis: string } | null
}

export function lireContexte(): ContexteCampagne | null {
  try {
    const brut = window.localStorage.getItem(CLE_CAMPAGNE)
    if (!brut) return null
    const valeur = JSON.parse(brut) as Partial<ContexteCampagne>
    if (!valeur || !valeur.id || !valeur.scenario) return null
    return { id: valeur.id, scenario: valeur.scenario }
  } catch {
    return null
  }
}

export function effacerContexte(): void {
  try {
    window.localStorage.removeItem(CLE_CAMPAGNE)
  } catch {
    // Rien à faire : au pire le panneau se represente une fois, et revalider
    // écrit les mêmes valeurs.
  }
}

async function lireJson<T>(url: string): Promise<T> {
  const reponse = await fetch(url, { cache: 'no-store' })
  if (!reponse.ok) throw new Error(`HTTP ${reponse.status} sur ${url}`)
  return (await reponse.json()) as T
}

async function posterJson<T>(url: string, corps: unknown): Promise<T> {
  const reponse = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(corps),
  })
  if (!reponse.ok) throw new Error(`HTTP ${reponse.status} sur ${url}`)
  return (await reponse.json()) as T
}

export const chargerCampagne = (id: string): Promise<Campagne> =>
  lireJson<Campagne>(`/get_campagne?${encodeURIComponent(id)}`)

export const chargerDefinition = (code: string): Promise<DefinitionCampagne> =>
  lireJson<DefinitionCampagne>(`/get_campagne_definition?${encodeURIComponent(code)}`)

/** Le carnet que le MOTEUR a relevé à la dernière fin de partie sur cette place. */
export type CarnetSuggere = {
  /**
   * Scénario qui a produit `suggestions` (estampille posée par le moteur côté
   * `WriteCampaignLogAtGameOver`), ou `null` si le fichier est absent ou vide.
   * Rien n'efface jamais ce fichier entre deux parties : sans cette valeur,
   * le carnet d'un scénario A resterait lisible comme suggestion valide pour
   * un scénario B totalement différent joué plus tard sur la même place.
   */
  scenario: string | null
  suggestions: Record<string, string>
}

/**
 * Vide pour trors et sm, qui n'ont pas de collecteur côté moteur : le panneau
 * retombe alors sur ses détecteurs, exactement comme avant cette route.
 */
export const chargerCarnetSuggere = async (): Promise<CarnetSuggere> => {
  try {
    const brut = await lireJson<{ scenario?: string | null; suggestions?: Record<string, string> }>(
      '/get_carnet_suggere'
    )
    return { scenario: brut.scenario ?? null, suggestions: brut.suggestions ?? {} }
  } catch {
    // Une route indisponible ne doit pas empêcher de valider ses récompenses :
    // sans suggestion, les détecteurs reprennent la main.
    return { scenario: null, suggestions: {} }
  }
}

export const enregistrerCampagne = (campagne: Campagne): Promise<{ campagne: Campagne }> =>
  posterJson<{ campagne: Campagne }>('/save_campagne', { campagne })

/**
 * Les champs à présenter pour ce scénario, dans l'ordre d'affichage.
 *
 * Trois couches, dans cet ordre : ce que rapporte CE scénario, puis ce que la
 * campagne demande à chaque victoire (la piste de Réputation de Sinister
 * Motives et ses récompenses, reportées d'un scénario au suivant), puis les
 * conséquences de la campagne experte.
 *
 * Les deux dernières couches sautent le scénario FINAL : elles n'existent que
 * pour être relues au scénario suivant, et il n'y en a plus.
 */
export function champsDuScenario(
  definition: DefinitionCampagne,
  scenario: ScenarioCampagne,
  difficulte: string | undefined
): ChampVictoire[] {
  const champs = [...(scenario.victoire ?? [])]
  if (!scenario.final) {
    champs.push(...(definition.victoire_commune ?? []))
    if (difficulte === 'expert') champs.push(...(definition.victoire_commune_expert ?? []))
  }
  return champs
}
