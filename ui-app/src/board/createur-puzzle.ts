// createur-puzzle.ts — la logique du mode « Puzzle » du plateau (24/10/2026) : de la capture du plateau au puzzle publie.
//
// Le createur lance une partie normale (assistant de preparation, mode « Puzzle »), arrange le plateau a la main avec les outils du bac
// a sable / de la table manuelle, puis « Enregistrer le puzzle » : le moteur rend le plateau en puzzle v2 (`GET /puzzle_capture`), on
// y ajoute les details de la fenetre (titre, histoire, objectifs...) et on le publie sur le site (`/api/puzzle/publier`). Memes
// limites que le moteur (`puzzle_validation.py`) : refusees ICI avant l'envoi, avec une phrase claire.

export const MAX_TITRE = 80
export const MAX_HISTOIRE = 2000
export const MAX_INDICES = 10
export const MAX_INDICE = 500
export const MAX_OBJECTIFS = 6
export const MAX_SOLUTION = 4000
export const MAX_TEXTE_OBJECTIF = 300
export const MAX_PSEUDO = 30

export type GenreObjectif = 'defeat_villain' | 'survive' | 'complete_scheme' | 'free_text'
export type Objectif = { kind: GenreObjectif; target: string; text: string }
export type PhaseDeDepart = '' | 'player' | 'villain' | 'end_round'

/** Ce que remplit le createur dans la fenetre « Enregistrer le puzzle ». */
export type DetailsPuzzle = {
  titre: string
  histoire: string
  difficulte: number
  indices: string[]
  objectifs: Objectif[]
  /** `all` : tous les objectifs sont requis ; `any` : un seul suffit. */
  modeObjectifs: 'all' | 'any'
  phaseDeDepart: PhaseDeDepart
  premierJoueur: number
  solution: string
  visibiliteSolution: 'after' | 'always' | 'never'
  pseudo: string
}

export type Capture = { puzzle: Record<string, unknown>; avertissements: string[] }

export const DETAILS_VIDES: DetailsPuzzle = {
  titre: '',
  histoire: '',
  difficulte: 0,
  indices: [],
  objectifs: [{ kind: 'defeat_villain', target: '', text: '' }],
  modeObjectifs: 'all',
  phaseDeDepart: '',
  premierJoueur: 0,
  solution: '',
  visibiliteSolution: 'after',
  pseudo: '',
}

/** Les erreurs qui empechent d'enregistrer (une phrase par probleme). Vide = on peut publier. */
export function erreursDesDetails(d: DetailsPuzzle, nombreDeJoueurs: number): string[] {
  const erreurs: string[] = []
  if (!d.titre.trim()) erreurs.push('Donne un titre au puzzle.')
  if (d.titre.length > MAX_TITRE) erreurs.push(`Titre trop long (${MAX_TITRE} caractères au plus).`)
  if (d.histoire.length > MAX_HISTOIRE) erreurs.push(`Histoire trop longue (${MAX_HISTOIRE} caractères au plus).`)
  if (d.indices.length > MAX_INDICES) erreurs.push(`${MAX_INDICES} indices au plus.`)
  if (d.indices.some((i) => i.length > MAX_INDICE)) erreurs.push(`Un indice est trop long (${MAX_INDICE} caractères au plus).`)
  if (d.objectifs.length < 1) erreurs.push('Ajoute au moins un objectif.')
  if (d.objectifs.length > MAX_OBJECTIFS) erreurs.push(`${MAX_OBJECTIFS} objectifs au plus.`)
  for (const [i, o] of d.objectifs.entries()) {
    if (o.kind === 'complete_scheme' && !o.target.trim()) erreurs.push(`Objectif ${i + 1} : indique le complot visé.`)
    if (o.kind === 'free_text' && !o.text.trim()) erreurs.push(`Objectif ${i + 1} : écris l’objectif libre.`)
    if (o.text.length > MAX_TEXTE_OBJECTIF) erreurs.push(`Objectif ${i + 1} : texte trop long (${MAX_TEXTE_OBJECTIF} caractères au plus).`)
  }
  if (d.solution.length > MAX_SOLUTION) erreurs.push(`Solution trop longue (${MAX_SOLUTION} caractères au plus).`)
  if (d.premierJoueur < 0 || d.premierJoueur >= Math.max(1, nombreDeJoueurs)) erreurs.push('Ce joueur n’existe pas.')
  return erreurs
}

/** Le puzzle capture + les details de la fenetre = le puzzle a publier (format 2). Ne modifie pas la capture. */
export function assemblerPuzzle(capture: Record<string, unknown>, d: DetailsPuzzle): Record<string, unknown> {
  const solution = d.solution.trim()
  const indices = d.indices.map((i) => i.trim()).filter(Boolean)
  return {
    ...capture,
    format: 2,
    author: d.pseudo.trim(),
    comment: d.titre.trim(),
    title: d.titre.trim(),
    description: d.histoire.trim(),
    difficulty: d.difficulte,
    hints: indices,
    objectives: d.objectifs.map((o) => ({
      kind: o.kind,
      target: o.kind === 'complete_scheme' ? o.target.trim() : '',
      text: o.kind === 'free_text' ? o.text.trim() : '',
    })),
    objectives_mode: d.modeObjectifs,
    start_phase: d.phaseDeDepart,
    start_step: '',
    first_player: d.premierJoueur,
    solution_visibility: d.visibiliteSolution,
    solution_text: solution,
    has_solution: solution !== '',
  }
}

/** L'adresse du site qui garde les puzzles, ou null hors ligne (meme regle que `puzzle-client.js` cote preparation). */
export function urlSitePuzzles(loc: Pick<Location, 'hostname' | 'protocol' | 'port' | 'host'> | undefined = globalThis.location): string | null {
  const surcharge = (globalThis as { MC_SITE_PUZZLES?: string }).MC_SITE_PUZZLES
  if (surcharge) return String(surcharge).replace(/\/+$/, '')
  if (!loc || !loc.hostname) return null
  const m = /^(?:p\d+|play|discord)\.(.+\..+)$/.exec(loc.hostname)
  if (m) return `${loc.protocol}//${m[1]}${loc.port ? ':' + loc.port : ''}`
  if (/^(127\.0\.0\.1|localhost|\[::1\])$/.test(loc.hostname)) return null
  return `${loc.protocol}//${loc.host}`
}

/** Le plateau courant en puzzle v2, demande au moteur. Leve une erreur lisible si la table refuse. */
export async function capturerLePlateau(f: typeof fetch = globalThis.fetch): Promise<Capture> {
  let reponse: Response
  try {
    reponse = await f('/puzzle_capture', { cache: 'no-store' })
  } catch {
    throw new Error('Le moteur ne répond pas.')
  }
  if (!reponse.ok) {
    let raison = ''
    try {
      raison = String(((await reponse.json()) as { error?: string }).error ?? '')
    } catch {
      /* corps vide */
    }
    if (raison === 'setup not finished') throw new Error('Termine d’abord la mise en place (mulligans, choix), puis enregistre.')
    throw new Error(reponse.status === 409 ? 'Cette table n’est pas une table de création de puzzle.' : 'Le moteur a refusé la capture du plateau.')
  }
  const donnees = (await reponse.json()) as Partial<Capture>
  if (!donnees.puzzle) throw new Error('Le moteur n’a rien renvoyé.')
  return { puzzle: donnees.puzzle, avertissements: donnees.avertissements ?? [] }
}

export type Publication = { code: string; cle: string; expire_le?: number }

/** Publie sur le site. Les raisons de refus du site (liste) sont rendues telles quelles dans `Error.message`, separees par « ; ». */
export async function publierSurLeSite(
  puzzle: Record<string, unknown>,
  pseudo: string,
  { site = urlSitePuzzles(), f = globalThis.fetch }: { site?: string | null; f?: typeof fetch } = {}
): Promise<Publication> {
  if (!site) throw new Error('Les puzzles publiés demandent une connexion au site (indisponible hors ligne).')
  let reponse: Response
  try {
    reponse = await f(`${site}/api/puzzle/publier`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ puzzle, pseudo }),
      credentials: 'omit',
    })
  } catch {
    throw new Error('Le site ne répond pas.')
  }
  let donnees: { code?: string; cle?: string; expire_le?: number; erreur?: string[] | string } = {}
  try {
    donnees = await reponse.json()
  } catch {
    /* corps vide */
  }
  if (!reponse.ok) {
    const raisons = Array.isArray(donnees.erreur) ? donnees.erreur.join(' ; ') : donnees.erreur
    throw new Error(raisons || `Erreur ${reponse.status}`)
  }
  if (!donnees.code || !donnees.cle) throw new Error('Le site n’a pas renvoyé de code.')
  return { code: donnees.code, cle: donnees.cle, expire_le: donnees.expire_le }
}

const CLE_MES_PUZZLES = 'mc-puzzles-crees'

/** Garde le puzzle dans « Mes puzzles » de ce navigateur (meme format que `memoriserPuzzle` de la preparation). */
export function memoriserMonPuzzle(
  entree: { code: string; cle: string; titre: string; expire_le?: number },
  stockage: Pick<Storage, 'getItem' | 'setItem'> = globalThis.localStorage
): boolean {
  try {
    const actuelle = JSON.parse(stockage.getItem(CLE_MES_PUZZLES) || '[]')
    const liste = (Array.isArray(actuelle) ? actuelle : []).filter((x: { code?: string }) => x.code !== entree.code)
    liste.unshift({ code: entree.code, cle: entree.cle, titre: entree.titre, cree: Date.now(), expire_le: entree.expire_le || 0, brouillon: null })
    stockage.setItem(CLE_MES_PUZZLES, JSON.stringify(liste.slice(0, 200)))
    return true
  } catch {
    return false
  }
}
