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
  /**
   * Mode « Sur la table » (v3, Q17, 10/10/2026) : pendant la phase, la bulle
   * porte la question à la place du panneau central. Absent : faux.
   */
  bulleSurTable?: boolean
  /**
   * La question posée est celle de la face A de la manigance principale
   * (`Reveal_Main_Scheme`, voir `manigance-face-a.ts`). Elle a son propre
   * panneau : personne d'autre ne l'affiche.
   */
  questionDeLaManigance: boolean
  /**
   * Le carre de la phase est a l'ecran, au milieu (refonte du 04/10/2026,
   * revirement du 05/10, scene PC). Pendant la phase, il porte tout : la
   * question, et ce que la narration centrale racontait. Absent : faux.
   */
  cartoucheEnBas?: boolean
  /**
   * HORS PHASE, une attaque du mechant annoncee pendant le tour du joueur a
   * ouvert le cartouche « Pendant ton tour » (D26) : c'est lui qui porte la
   * defense. Absent : faux.
   */
  coupHorsPhaseEnScene?: boolean
  /**
   * HORS PHASE, un cartouche du bas est a l'ecran (« Pendant ton tour » sur un
   * coup, ou la relecture du journal) : il raconte, la narration centrale se
   * tait (planche du lot 5). Absent : faux.
   */
  cartoucheHorsPhaseAffiche?: boolean
}

/**
 * LA QUESTION DE LA MANIGANCE N'APPARTIENT QU'À SON PANNEAU.
 *
 * ⚠ DÉFAUT TROUVÉ EN RELECTURE, 15/09/2026. Le chantier de la face A n'avait
 * pas touché ce fichier : `DemandeCentrale` ET `BarreAction` affichaient donc
 * la même question sous le voile, avec le libellé brut « Reveal Main Scheme »
 * que `dico-en.ts` ne connaît pas. Et pendant les 400 ms du retournement, le
 * panneau passe en `pointer-events: none` : ce bouton-là redevenait cliquable,
 * contournait la garde du panneau (« un seul envoi ») et pouvait répondre à la
 * question SUIVANTE à la place du joueur.
 */
function priseParLePanneauManigance(e: EtatDeLaQuestion): boolean {
  return e.questionDeLaManigance
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
  if (priseParLePanneauManigance(e)) return false
  if (!e.sceneCentrale && !(e.bulleSurTable && e.phaseMechantEnCours)) return false
  // Hors phase, la scene ne prend la question que si le cartouche « Pendant
  // ton tour » est ouvert sur une annonce : sinon rien ne la porterait.
  if (!e.phaseMechantEnCours && e.coupHorsPhaseEnScene !== true) return false
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
  if (priseParLePanneauManigance(e)) return false
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
  // Elle se tait aussi devant le panneau de la manigance. Sans cette ligne, la
  // porte ci-dessus (la question n'est plus ni dans le panneau ni dans la
  // scène) laisserait la narration se poser au centre, par-dessus la carte
  // montrée en grand — exactement ce que le silence de l'ouverture refuse.
  if (priseParLePanneauManigance(e)) return false
  // Sous le cartouche du bas, pendant la phase, la narration se tait : le
  // cartouche raconte deja chaque etape, et la narration se poserait au centre
  // de la table pour redire ce qu'il dit (« plus aucun panneau hors du
  // cartouche », decisions du 04/10/2026).
  if (e.cartoucheEnBas === true && e.phaseMechantEnCours) return false
  // Hors phase, meme regle tant qu'un cartouche du bas est a l'ecran : sinon
  // « Spider-Man subit 4 dégâts » se posait au centre pendant que « Pendant
  // ton tour » montrait la meme attaque.
  if (e.cartoucheEnBas === true && e.cartoucheHorsPhaseAffiche === true) return false
  if (!e.effetEnCours && !contexte.evenementImportant) return false
  if (e.ciblage || e.menuCarte) return false
  return !questionDansLePanneau(e) && !questionDansLaScene(e)
}
