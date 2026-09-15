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
 * La question de la manigance, ou `undefined` si ce n'est pas ce moment-là.
 *
 * ⚠ EXIGE QU'ELLE SOIT SEULE. Si le moteur propose autre chose en même temps,
 * le joueur a un vrai choix à faire et le panneau n'a pas à s'en emparer.
 */
export function questionDeLaManigance(demande: Demande | undefined): Option | undefined {
  if (!demande) return undefined
  if (demande.options.length !== 1) return undefined
  const seule = demande.options[0]
  return seule && seule.name === NOM_OPTION_MANIGANCE ? seule : undefined
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
  const zone = monde?.area_schemes_main
  if (!Array.isArray(zone)) return undefined
  const designee = bindId !== undefined ? zone.find((carte) => carte.id === bindId) : undefined
  return designee ?? zone[0]
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
