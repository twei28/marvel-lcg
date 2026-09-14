// OÙ S'AFFICHE LA QUESTION DU MOTEUR.
//
// Extrait de `board.tsx` le 14/09/2026, pour la même raison que
// `cartouche-a-jour.ts` : c'est une règle invisible. Quand elle se trompe,
// rien ne plante et rien ne rougit — le moteur attend une réponse, et RIEN à
// l'écran ne dit où la donner.
//
// ⚠ CE FICHIER EXISTE À CAUSE DU DÉFAUT MESURÉ EN JEU LE 14/09/2026.
// L'utilisateur : « en mode détaillé il n'indique même plus quand on peut
// défendre, il fait cliquer sur la carte sans rien indiquer. »
//
// Ce qui se passait, relevé dans une vraie partie (Rhino / Spider-Man, mode
// Détaillé) : le moteur pose « Spider-Man est attaqué par Shocker · Défendre /
// Passer » PENDANT que l'animation des dégâts de l'attaque précédente est
// encore à l'écran (`effetEnCours`, 1,7 s par effet). Le panneau central cède
// la place à l'animation — c'est voulu — mais la SCÈNE du mode Détaillé cédait
// avec lui, parce que les deux lisaient la même condition. Or en mode
// Détaillé, pendant la phase du méchant, la scène est le SEUL endroit où
// répondre : la question disparaissait, le cartouche se repliait sur « tu peux
// défendre ou répondre » SANS UN SEUL BOUTON, et il ne restait au joueur que
// le menu d'une carte de la table.
//
// LA RÈGLE, EN UNE PHRASE : le panneau central cède la place à toute autre
// façon de répondre (un ciblage, le menu d'une carte) ET à une animation en
// cours ; la scène ne cède qu'aux autres FAÇONS DE RÉPONDRE, jamais à une
// animation, parce qu'il n'y a rien derrière elle.

export type EtatDeLaQuestion = {
  /** Le moteur attend une réponse du joueur LOCAL (voir moteurAttendUneReponse). */
  moteurAttendLeJoueur: boolean
  /** Le client connaît la demande (`etat.demande`). */
  demandePresente: boolean
  /** Une animation d'effet est à l'écran (dégâts, soin, menace, statut). */
  effetEnCours: boolean
  /** Un ciblage est ouvert : le joueur répond en cliquant la table. */
  ciblage: boolean
  /** Le menu d'une carte est ouvert : il porte déjà les réponses. */
  menuCarte: boolean
  /** Mode « Détaillé » : la phase du méchant se joue dans une scène centrale. */
  sceneCentrale: boolean
  /** Le moteur est dans une des quatre phases du méchant. */
  phaseMechantEnCours: boolean
}

/**
 * LA QUESTION SE JOUE-T-ELLE DANS LA SCÈNE DU MODE DÉTAILLÉ ?
 *
 * ⚠ `effetEnCours` N'ENTRE PAS DANS CETTE RÈGLE, et c'est tout le correctif.
 * Une animation n'est pas une façon de répondre : la faire passer avant la
 * question laissait le joueur sans aucun bouton pendant 1,7 s par effet, à
 * chaque attaque qui suit un dégât.
 */
export function questionDansLaScene(e: EtatDeLaQuestion): boolean {
  if (!e.sceneCentrale || !e.phaseMechantEnCours) return false
  if (!e.moteurAttendLeJoueur || !e.demandePresente) return false
  // Les deux seules autres façons de répondre à la MÊME question : le ciblage
  // se joue sur la table (la scène se replie pour la laisser cliquable), et le
  // menu d'une carte porte déjà les options.
  return !e.ciblage && !e.menuCarte
}

/**
 * LE PANNEAU CENTRAL AUTONOME (`DemandeCentrale`) s'affiche-t-il ?
 *
 * Il cède la place à tout le reste, animation comprise : hors de la scène, le
 * joueur garde la barre du bas et le menu des cartes pour répondre.
 */
export function questionDansLePanneau(e: EtatDeLaQuestion): boolean {
  if (!e.moteurAttendLeJoueur || !e.demandePresente) return false
  if (e.effetEnCours || e.ciblage || e.menuCarte) return false
  // La scène et le panneau ne s'affichent JAMAIS ensemble : c'est la même
  // question, et deux panneaux au centre est le défaut n°2 du 14/09/2026.
  return !questionDansLaScene(e)
}

/**
 * LA NARRATION CENTRALE (`EvenementCentrale`) s'affiche-t-elle ?
 *
 * `evenementImportant` : un moment narré digne d'être montré pendant
 * l'activation ennemie. Elle se tait devant une question, où qu'elle soit
 * posée — sans quoi la narration se poserait AU CENTRE, par-dessus la scène
 * qui porte les boutons.
 */
export function narrationAuCentre(
  e: EtatDeLaQuestion,
  contexte: { connecte: boolean; evenementImportant: boolean }
): boolean {
  if (!contexte.connecte) return false
  if (!e.effetEnCours && !contexte.evenementImportant) return false
  if (e.ciblage || e.menuCarte) return false
  return !questionDansLePanneau(e) && !questionDansLaScene(e)
}
