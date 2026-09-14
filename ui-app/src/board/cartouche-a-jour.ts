// QUAND LE CARTOUCHE RELÂCHE LA TRAME DU MOTEUR.
//
// Extrait de `DeroulePhase` le 14/09/2026 pour une raison précise : c'est la
// seule règle qui décide du rythme de toute la phase du méchant, et une erreur
// dedans ne se voit pas. Elle ne plante pas, elle ne rougit pas : la phase
// défile toute seule, ou elle se fige.
//
// ⚠ CE FICHIER EXISTE PARCE QUE LE DÉFAUT EST REVENU TROIS FOIS. L'utilisateur,
// le 14/09/2026, après la troisième : « je te l'ai dit mille fois, pourquoi
// est-ce que ça continue tout seul sans que moi je mette suivant ? Ça ne
// devrait pas arriver. » Les deux premières causes étaient ailleurs (un réglage
// grisé qui s'appliquait quand même, puis le mode lui-même) ; la troisième est
// ici, et elle a désormais sa gate.

export type EtatDuCartouche = {
  /** La phase est finie et racontée : plus rien à retenir. */
  termine: boolean
  /** La partie est finie : plus rien n'arrive après. */
  partieFinie: boolean
  /** Le cartouche n'a aucune étape à montrer. */
  sansEtape: boolean
  /** Le moteur pose une question au joueur local. */
  questionAuJoueur: boolean
  /** Le cartouche est arrivé au bout des étapes qu'il connaît. */
  surLaDerniereEtape: boolean
  /** Le joueur a cliqué « Suivant » sur cette étape. */
  etapeValidee: boolean
  /** L'étape courante est une ANNONCE (« Klaw va attaquer Jessica Jones »). */
  etapeEstAnnonce: boolean
  /** Présentation « Sur la table » : un clic à chaque étape, annonce comprise. */
  surTable: boolean
}

/**
 * Le cartouche a-t-il fini son travail sur la trame courante ?
 *
 * ⚠ VRAI VEUT DIRE « LE MOTEUR PEUT REPARTIR ». C'est donc le seul endroit où
 * se décide si le joueur doit cliquer ou non.
 *
 * ⚠ ET L'ANNONCE EST LE PIÈGE. En mode « Détaillé », une annonce acquitte toute
 * seule : c'est la décision 7 de la spec du 07/09/2026, « pas de clic sur va
 * attaquer ». En mode « Sur la table », l'utilisateur a décidé EXACTEMENT
 * L'INVERSE (14/09/2026) : deux clics par attaque, et c'est l'annonce qui porte
 * le premier, « parce que c'est là aussi où on peut choisir de défendre ».
 * Sans la garde `!surTable`, chaque annonce relâchait la trame et toute la
 * phase défilait sans un clic.
 */
export function cartoucheEstAJour(e: EtatDuCartouche): boolean {
  if (e.termine || e.partieFinie || e.sansEtape) return true
  // Retenir pendant une question ne protège de rien : le moteur ne produit
  // plus rien tant qu'on ne lui a pas répondu, et c'est notre accusé qui lui
  // permet d'ARRIVER à sa question. Ne pas acquitter ici bloquerait la partie
  // jusqu'au filet anti-blocage.
  if (e.questionAuJoueur) return true
  if (!e.surLaDerniereEtape) return false
  if (e.etapeValidee) return true
  return e.etapeEstAnnonce && !e.surTable
}
