// « Faut-il tout re-préparer avant de rejouer ce scénario ? »
//
// Une seule boîte le demande : Agents of S.H.I.E.L.D., livret p.19, encart
// DEFEAT du scénario 5, campagne STANDARD uniquement.
//
//   To replay this scenario, do the following:
//   » Prepare the evidence as if you are starting a new campaign.
//   » Gain one evidence card from the S.H.I.E.L.D. envelope for each scenario
//     in which you had at least one Board Member environment with no secret
//     counters on it.
//
// C'est l'exact miroir de la règle de défaite : en EXPERT le même encart perd
// la campagne, en STANDARD il la fait repartir. Les deux ne peuvent donc jamais
// s'appliquer ensemble, et c'est `standard_seulement` qui le dit ici comme
// `expert_seulement` le dit là-bas.
//
// Ce qui se passe ensuite n'est pas une remise à zéro anodine : la combinaison
// de la taupe est RETIRÉE, donc toute la grille de déduction est à refaire. Le
// joueur doit le savoir avant de relancer, d'où le texte porté par la règle.
//
// Comme `defaite-campagne.ts`, ce module ne connaît ni le DOM, ni le réseau, ni
// le moteur : il prend des faits et rend une décision.

/** Ce que le scénario final déclare comme règle de reprise après défaite. */
export type RegleReprise = {
  /** Seule valeur pour l'instant : perdre ce scénario déclenche la reprise. */
  quand: 'partie_perdue'
  /** La règle ne vaut qu'en campagne standard (en expert, la campagne est perdue). */
  standard_seulement?: boolean
  /** Clé du carnet qui compte les scénarios méritant une preuve. */
  cle_compte?: string
  /** Clé du carnet qui porte les preuves obtenues. */
  cle_preuves?: string
  /** Titre montré au joueur. */
  titre?: string
  /** Ce que le livret raconte, et ce que la reprise va coûter. */
  texte?: string
}

export type FaitsDeReprise = {
  /** Le scénario qui vient d'être joué est-il le dernier de la campagne ? */
  final: boolean
  /** La règle déclarée par ce scénario, s'il en porte une. */
  regle?: RegleReprise | null
  /** Les joueurs ont-ils gagné la partie ? */
  gagne: boolean
  /** La campagne est-elle jouée en mode expert ? */
  expert: boolean
  /** La campagne est-elle déjà perdue par ailleurs ? */
  perdue: boolean
}

export type Reprise = {
  applicable: boolean
  titre: string
  texte: string
}

const RIEN: Reprise = { applicable: false, titre: '', texte: '' }

export function repriseDeCampagne(faits: FaitsDeReprise): Reprise {
  const { regle } = faits
  if (!faits.final || !regle) return RIEN
  // Une campagne perdue ne se rejoue pas : le verdict de défaite prime, sans
  // quoi on proposerait de repartir sur une campagne qui vient de s'arrêter.
  if (faits.perdue) return RIEN
  if (regle.standard_seulement && faits.expert) return RIEN
  if (regle.quand !== 'partie_perdue') return RIEN
  if (faits.gagne) return RIEN
  return { applicable: true, titre: regle.titre ?? '', texte: regle.texte ?? '' }
}
