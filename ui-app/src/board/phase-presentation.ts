// La PRÉSENTATION de la phase du méchant, parmi les trois qui partagent le rythme
// « Étape par étape » (mode `detaille`, voir moteur.ts) : 16/10/2026.
//
//  - `etape`      : « Étape par étape », le cartouche d'origine, au centre ;
//  - `bis`        : « Étape par étape bis », la nouvelle phase du méchant (essai) ;
//  - `dynamique`  : « Phase dynamique », la quatrième présentation (essai) : le même
//                   cartouche détaillé, posé en panneau à DROITE de la table, la
//                   table restant jouable (cartouche-dynamique.css).
//
// ⚠ CE N'EST PAS UN MODE DU MOTEUR. `ModePhaseMechant` ne bouge pas (`detaille`,
// `sur-table`, `instantane`) : la présentation ne change que la mise en scène, le
// moteur retient et relâche ses trames exactement de la même façon. Les comptes
// qui n'ont pas l'essai (`essais.ts`) ne voient jamais que `etape`.
//
// Depuis le 19/10/2026 (soir) seuls « Guidée » (`tris`), « Plateau animé » (`sur-table`) et « Accéléré » (`instantane`) sont proposés à tous (voir plus bas).
//
// Le choix vit dans le navigateur. Il remplace `mc_phase_bis` (oui/non, du matin du
// 16/10/2026), toujours lu s'il n'y a pas encore de choix : `non` donne `etape`,
// tout le reste donne `bis`, le défaut d'alors. Aucun réglage n'est perdu.

export type PresentationPhase = 'etape' | 'bis' | 'tris' | 'dynamique'

export const PRESENTATIONS: readonly PresentationPhase[] = ['etape', 'bis', 'tris', 'dynamique']

export const CLE_PRESENTATION_PHASE = 'mc_phase_presentation'
const CLE_ANCIENNE_PHASE_BIS = 'mc_phase_bis'
const EVENEMENT = 'mc-phase-presentation'

// LES TROIS CHOIX DE LA PHASE DU MÉCHANT (19/10/2026, demande de l'utilisateur) : « Étape par étape bis »,
// « Sur la table » et « D'un coup », dans cet ordre. Les deux autres présentations sont CACHÉES, pas
// supprimées : remettre un drapeau à `true` suffit à les montrer de nouveau (réglages, et lecture).
/** « Étape par étape », le cartouche d'origine (présentation `etape`) : caché. */
export const PHASE_ETAPE_VISIBLE = false
/** « Phase dynamique » (présentation `dynamique`) : cachée (commit 52bd46d6). */
export const PHASE_DYNAMIQUE_VISIBLE = false
/**
 * « Étape par étape bis » pour TOUT LE MONDE : sans l'essai « nouvelle phase » coché dans /admin
 * (`essaiPhaseMechant`, qui reste en place). Remettre `false` pour la réserver de nouveau aux comptes d'essai.
 */
export const PHASE_BIS_POUR_TOUS = true
/** « Étape par étape bis » (présentation `bis`) : cachée depuis le 19/10/2026 (soir), remplacée par « Guidée » (`tris`). */
export const PHASE_BIS_VISIBLE = false
/**
 * « Guidée » (présentation `tris`) pour TOUT LE MONDE, y compris en ligne. Avant, elle n'existait que sur
 * localhost (test d'hôte retiré). Remettre `false` la rend de nouveau invisible hors de la machine locale.
 */
export const PHASE_TRIS_POUR_TOUS = true
/** Cette variante `tris` est-elle utilisable ici ? (drapeau, sinon hôte local seulement.) */
export function phaseTrisUtilisable(hote: string = globalThis.location?.hostname ?? ''): boolean {
  return PHASE_TRIS_POUR_TOUS || ['localhost', '127.0.0.1', '[::1]'].includes(hote)
}

/** Cette présentation est-elle proposée au joueur ? */
export function presentationProposee(presentation: PresentationPhase): boolean {
  if (presentation === 'etape') return PHASE_ETAPE_VISIBLE
  if (presentation === 'dynamique') return PHASE_DYNAMIQUE_VISIBLE
  if (presentation === 'bis') return PHASE_BIS_VISIBLE
  return phaseTrisUtilisable()
}

/** Le choix de départ, et le repli de tout choix qui n'est plus proposé. */
export const PRESENTATION_PAR_DEFAUT: PresentationPhase = 'tris'

/**
 * PASSAGE UNIQUE AUX TROIS CHOIX (19/10/2026) : jumeau de `migrerPhaseTroisChoix` de la préparation
 * (public/js/prepare/phase-mode-choix.js), même clé de passage, même version. Qui était sur l'ancien
 * « Étape par étape » (présentation `etape`, ou l'ancien `mc_phase_bis` à « non ») ou sur « Phase dynamique »
 * passe sur « tris » (« Guidée »). Version `2026-10-19b` : ceux déjà passés sur « bis » le sont une seconde fois. Le mode (`detaille`, `sur-table`, `instantane`) n'est jamais touché : « Sur la table » et
 * « D'un coup » sont conservés. Le choix vit dans le navigateur seulement (rien n'est rangé sur le compte).
 */
export const CLE_MIGRATION_PHASE = 'mc_phase_trois_choix_migre'
export const VERSION_MIGRATION_PHASE = '2026-10-19b'
export function migrerPhaseTroisChoix(stockage: Pick<Storage, 'getItem' | 'setItem'> | null | undefined): boolean {
  try {
    if (!stockage || stockage.getItem(CLE_MIGRATION_PHASE) === VERSION_MIGRATION_PHASE) return false
    const stocke = stockage.getItem(CLE_PRESENTATION_PHASE)
    const ancienNon = stocke === null && stockage.getItem(CLE_ANCIENNE_PHASE_BIS) === 'non'
    if (ancienNon || (stocke !== null && stocke !== 'tris')) stockage.setItem(CLE_PRESENTATION_PHASE, PRESENTATION_PAR_DEFAUT)
    stockage.setItem(CLE_MIGRATION_PHASE, VERSION_MIGRATION_PHASE)
    return true
  } catch {
    return false
  }
}

// Fait AVANT toute lecture du choix rangé (la préparation l'a peut-être déjà fait : alors rien).
try {
  migrerPhaseTroisChoix(globalThis.localStorage)
} catch {
  /* stockage indisponible */
}

export function lirePresentationPhase(): PresentationPhase {
  try {
    const stocke = globalThis.localStorage?.getItem(CLE_PRESENTATION_PHASE)
    if (stocke && (PRESENTATIONS as readonly string[]).includes(stocke)) {
      // Un choix qui n'est plus proposé (caché derrière un drapeau) retombe sur « tris », sans être effacé.
      return presentationProposee(stocke as PresentationPhase) ? (stocke as PresentationPhase) : PRESENTATION_PAR_DEFAUT
    }
    const ancien = globalThis.localStorage?.getItem(CLE_ANCIENNE_PHASE_BIS) === 'non' ? 'etape' : PRESENTATION_PAR_DEFAUT
    return presentationProposee(ancien) ? ancien : PRESENTATION_PAR_DEFAUT
  } catch {
    return PRESENTATION_PAR_DEFAUT
  }
}

export function ecrirePresentationPhase(presentation: PresentationPhase): void {
  try {
    globalThis.localStorage?.setItem(CLE_PRESENTATION_PHASE, presentation)
  } catch {
    /* stockage refuse : le choix vaudra pour la page */
  }
  globalThis.dispatchEvent?.(new CustomEvent(EVENEMENT, { detail: presentation }))
}

/** Suit le choix (Réglages ouverts dans la même page). Rend de quoi se désabonner. */
export function suivrePresentationPhase(rappel: (presentation: PresentationPhase) => void): () => void {
  const ecoute = (e: Event) => rappel((e as CustomEvent<PresentationPhase>).detail)
  globalThis.addEventListener?.(EVENEMENT, ecoute)
  return () => globalThis.removeEventListener?.(EVENEMENT, ecoute)
}
