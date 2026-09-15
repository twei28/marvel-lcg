// LE TEMPS D'ARRÊT SUR LA FACE A DE LA MANIGANCE PRINCIPALE.
//
// Le moteur pose une vraie question avant de retourner une face A
// (`World.ConfirmMainSchemeReveal`, world.py). Elle voyage comme n'importe
// quelle question, avec UNE option nommée `Reveal_Main_Scheme`.
//
// ⚠ CE MODULE EST PUR. Aucune lecture du DOM, aucun rendu : de quoi vérifier
// la règle de reconnaissance sans navigateur.

import type { Demande, Option } from './ask'
import type { World, WorldCard } from './world'

/**
 * Le nom TECHNIQUE de l'option, tel que le moteur le publie. Il ne s'affiche
 * jamais : le panneau pose son propre libellé traduit.
 *
 * ⚠ SANS ESPACE. Le moteur remplace les espaces par des underscores dans les
 * noms d'options publiés : un nom à espaces ne s'apparierait jamais.
 */
export const NOM_OPTION_MANIGANCE = 'Reveal_Main_Scheme'

/**
 * Le même moment, pour une manigance ANNEXE que le SCÉNARIO met en jeu
 * (`World.CONFIRM_SIDE_SCHEME_OPTION`, avenant du 15/09/2026).
 *
 * ⚠ ELLE NE SE RETOURNE PAS. Une annexe n'a qu'une face : le panneau la montre
 * et attend le OK, il n'y a rien à retourner. C'est la seule différence de
 * traitement entre les deux, et elle vit dans le panneau.
 *
 * ⚠ Le moteur ne pose cette question QUE pour ce que le scénario impose : une
 * manigance-joueur jouée depuis la main n'en déclenche aucune, le joueur vient
 * de la lire et de la choisir.
 */
export const NOM_OPTION_ANNEXE = 'Reveal_Side_Scheme'

/** Les deux questions que ce panneau prend en charge. */
const NOMS_PRIS = [NOM_OPTION_MANIGANCE, NOM_OPTION_ANNEXE]

/**
 * La question de la manigance, ou `undefined` si ce n'est pas ce moment-là.
 *
 * ⚠ EXIGE QU'ELLE SOIT SEULE. Si le moteur propose autre chose en même temps,
 * le joueur a un vrai choix à faire et le panneau n'a pas à s'en emparer.
 */
export function questionDeLaManigance(demande: Demande | undefined): Option | undefined {
  if (!demande) return undefined
  if (demande.options.length !== 1) return undefined
  const seule = demande.options[0]
  return seule && NOMS_PRIS.includes(seule.name) ? seule : undefined
}

/**
 * La manigance à montrer en grand : celle que LA QUESTION DÉSIGNE.
 *
 * Au moment de la question, le moteur n'a pas encore retourné la carte : la
 * zone porte donc la face A. On ne déduit pas son identifiant, on lit la table.
 *
 * ⚠ ON NE DEVINE PLUS AVEC L'INDEX 0. Défaut trouvé en relecture le
 * 15/09/2026 : à la mise en place, le moteur boucle sur TOUTES les manigances
 * principales (world.py:546) et pose donc une question par manigance. Dès la
 * seconde, l'index 0 porte la carte déjà retournée, et le panneau montrait la
 * mauvaise carte sur sa face B. Le mode Bataille (21098a) met bien deux
 * manigances principales en jeu ensemble.
 *
 * `bind_id` est renseigné par le moteur avec l'objet qui porte l'effet
 * (`effect.py:600`, `bind_id = the_effect.this.card.object_id`), et notre
 * capacité est construite sur `GameRule(scheme)` (`world.py:930`) : `bind_id`
 * EST donc la manigance en cours de retournement. Vérifié dans le moteur le
 * 15/09/2026 le long de la chaîne complète (`ChooseAbilities` →
 * `WhenPlayerChooseAbility.by_effect` → `Effect.Render` → `CardDescriptor.id`,
 * qui est le même `object_id`).
 *
 * Repli assumé sur la première carte de la zone quand `bind_id` ne désigne
 * aucune carte connue : mieux vaut la mauvaise carte qu'aucun panneau, qui
 * laisserait le moteur attendre une réponse sans bouton pour la donner.
 */
export function maniganceAMontrer(
  monde: World | undefined,
  bindId: number | undefined
): WorldCard | undefined {
  const principales = Array.isArray(monde?.area_schemes_main) ? monde.area_schemes_main : []
  // ⚠ LES DEUX ZONES, depuis l'avenant du 15/09/2026 : une manigance ANNEXE
  // vit dans `area_schemes_side`, pas avec les principales.
  const annexes = Array.isArray(monde?.area_schemes_side) ? monde.area_schemes_side : []
  const zone = [...principales, ...annexes]
  if (zone.length === 0) return undefined
  const designee = bindId !== undefined ? zone.find((carte) => carte.id === bindId) : undefined
  return designee ?? zone[0]
}

/** Ce que le panneau de la manigance tient, quand il tient la question. */
export type PriseDuPanneauManigance = {
  /** La question du moteur, à qui il faut répondre. */
  question: Option
  /** La carte à montrer en grand, sur sa face A. */
  carte: WorldCard
}

/**
 * LE PANNEAU PREND-IL LA QUESTION ? UNE SEULE RÉPONSE, POUR TOUT LE MONDE.
 *
 * ⚠ DÉFAUT TROUVÉ EN RELECTURE, 15/09/2026, ET IL REND UNE PARTIE INJOUABLE.
 * La REVENDICATION (« cette question est prise, que personne d'autre ne
 * l'affiche ») et le MONTAGE du panneau étaient deux conditions différentes :
 * la première ne regardait que la question, la seconde exigeait aussi la
 * carte. Quand `area_schemes_main` est vide ou absente, `maniganceAMontrer`
 * rend `undefined` : le panneau ne paraissait pas, mais la barre du bas, le
 * panneau central et la scène se taisaient tous les trois. Il ne restait plus
 * un seul bouton à l'écran, et le moteur attendait pour toujours.
 *
 * ⚠ UNE GATE, PAS UN REPLI. Le panneau ne revendique la question QUE s'il est
 * capable de la montrer ; sinon il rend la main aux panneaux ordinaires, qui
 * savent afficher n'importe quelle question. Et c'est la MÊME fonction des
 * deux côtés : revendication et montage ne peuvent plus diverger.
 */
export function priseDuPanneauManigance(
  demande: Demande | undefined,
  monde: World | undefined
): PriseDuPanneauManigance | undefined {
  const question = questionDeLaManigance(demande)
  if (!question) return undefined
  const carte = maniganceAMontrer(monde, question.bind_id)
  if (!carte) return undefined
  return { question, carte }
}

/**
 * LA DEMANDE TELLE QUE LA TABLE DOIT LA LIRE : sans la question du panneau.
 *
 * ⚠ DÉFAUT TROUVÉ EN RELECTURE, 15/09/2026. `ou-va-la-question.ts` avait fermé
 * le panneau central, la scène et la barre du bas, mais PAS le menu d'une
 * carte. `Reveal_Main_Scheme` porte `bind_id` = la manigance principale : la
 * table lui posait donc son halo (`interaction.ts`) et son menu offrait
 * l'option sous son libellé technique brut. Pire, en mode Détaillé une carte
 * qui n'a qu'une seule action disponible la DÉCLENCHE au clic : cliquer la
 * manigance répondait à la question.
 *
 * Et ce chemin-là n'est pas théorique. Pendant les 400 ms du retournement,
 * `board.css` met l'overlay du panneau en `pointer-events: none` et la table
 * redevient cliquable : le clic contournait la garde « un seul envoi » du
 * panneau et pouvait répondre à la question SUIVANTE.
 *
 * ⚠ LA RÈGLE N'EST PAS DUPLIQUÉE : c'est `priseDuPanneauManigance` ci-dessus,
 * et elle seule : la table ne perd la question que si le panneau la prend
 * VRAIMENT, carte comprise. Quand la question n'est
 * pas celle du panneau, la MÊME référence ressort, sans aucun objet neuf,
 * donc sans aucune dépendance de hook invalidée à chaque rendu.
 */
export function demandeHorsPanneauManigance(
  demande: Demande | undefined,
  monde: World | undefined
): Demande | undefined {
  return priseDuPanneauManigance(demande, monde) ? undefined : demande
}

/** Ce qu'il faut savoir pour décider si l'ouverture reste voilée. */
export type EtatOuverture = {
  /** Le monde dit qu'une question de face A est attendue (`confirm_main_scheme`). */
  confirmAttendue: boolean
  /** `round_id` : 0 pendant la mise en place, 1 au premier round. */
  round: number
  /** La question de la manigance est à l'écran. */
  questionArrivee: boolean
  /** Le voile a déjà été levé une fois dans cette partie. */
  dejaLevee: boolean
  /** Le moteur pose une demande au joueur de ce siège, quelle qu'elle soit. */
  demandePresente: boolean
  /** Le moteur déclare la partie finie (`monde.game_over`, voir fin-partie.ts). */
  partieFinie: boolean
}

/**
 * Le voile d'ouverture : la table n'apparaît qu'une fois montée.
 *
 * ⚠ AUCUNE MINUTERIE DE SECOURS, et c'est voulu. Le repli « au bout de N
 * secondes on affiche quand même » masquerait un vrai défaut le jour où la
 * question ne vient pas. La porte est explicite : on ne voile QUE si le monde
 * dit qu'une question est attendue.
 */
export function ouvertureEncoreVoilee(etat: EtatOuverture): boolean {
  if (etat.dejaLevee) return false
  // ⚠ UNE PARTIE FINIE LÈVE LE VOILE, TOUJOURS.
  //
  // Défaut trouvé en relecture le 15/09/2026, et il rend une partie
  // injouable. `confirm_main_scheme` est un drapeau de RÈGLE, vrai pour toute
  // la partie, pas un « une confirmation est en attente ». Si le moteur
  // termine la partie pendant la mise en place (`is_game_over` aux étapes 11,
  // 12 et 13 de `world.py`), `round_id` reste 0, aucune demande n'arrive, et
  // le retour anticipé du voile passe AVANT l'écran de fin de partie :
  // l'affichage restait sur « Connexion à la partie… » pour toujours.
  //
  // Ce n'est pas une minuterie de secours : c'est une porte sur un fait du
  // monde, `monde.game_over`, la même source que l'écran de fin
  // (`afficherFinDePartie`, fin-partie.ts).
  if (etat.partieFinie) return false
  if (!etat.confirmAttendue) return false
  if (etat.round > 0) return false
  // ⚠ SI LE MOTEUR POSE UNE QUESTION AU JOUEUR, LE JOUEUR DOIT POUVOIR VOIR SA
  // TABLE POUR Y RÉPONDRE. Ce n'est pas une minuterie de secours : c'est une
  // porte sur un fait du monde, et elle couvre tout ce que la seule arrivée de
  // `Reveal_Main_Scheme` laissait bloqué.
  //
  // Défaut trouvé en relecture le 15/09/2026 : un rechargement de page entre
  // le OK et le premier round figeait la partie pour de bon. `round_id` vaut
  // encore 0 pendant tout le mulligan (world.py:573), le verrou « déjà levée »
  // repart à faux au remontage, et la question a été consommée : le voile ne
  // se levait plus jamais, sur « Connexion à la partie… », pendant que le
  // moteur attendait une réponse au mulligan. Même blocage pour un second
  // siège qui ouvre sa page après le OK : la question de la manigance est
  // réservée au premier joueur, elle ne lui arrive jamais.
  //
  // Conséquence assumée : une capacité de mise en place qui interroge le
  // joueur AVANT notre question lèvera le voile plus tôt, et on verra un bout
  // de table se monter. Une partie jouable qui montre trop vaut mieux qu'une
  // partie bloquée.
  if (etat.demandePresente) return false
  return !etat.questionArrivee
}
