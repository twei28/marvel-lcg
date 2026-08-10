// « Cette campagne est-elle perdue ? »
//
// Les six livrets portent la même règle, à la dernière page des instructions du
// scénario final, et le jeu ne l'appliquait pas : elle était affichée au joueur
// à la création de la campagne et nulle part ailleurs.
//
//   trors     « Expert Campaign Only: If the players lose this game, Red Skull
//               conquers the world and the players lose the campaign. »
//   mts       … Loki exerts his rule over all the universe …
//   sm        … Venom Goblin takes control of New York City …
//   mut_gen   … Magneto rules the world with an iron fist …
//   next_evol … Stryfe escapes into the past …
//
// AoA est la seule qui s'en écarte, et sur les DEUX points : sa condition n'est
// pas la défaite mais la mission, et elle ne porte pas la mention « Expert
// Campaign Only » :
//
//   « If the Protect the Professor MISSION side scheme was defeated, the
//     players saved Professor X and win the campaign! If [it] was not
//     defeated, the players failed to save Professor X and lose the campaign. »
//
// D'où deux conditions et pas une. Elles sont déclarées dans
// `data/campagnes/<code>.json`, sur le scénario final, et jamais en dur ici :
// c'est le même parti pris que les récompenses.
//
// Ce module ne connaît ni le DOM, ni le réseau, ni le monde du moteur. Il prend
// des faits et rend une décision, pour qu'elle soit lisible et éprouvable sans
// jouer cinq scénarios.

/** Ce que le scénario final déclare comme condition de défaite de campagne. */
export type RegleDefaite = {
  /**
   * `partie_perdue` : perdre ce scénario perd la campagne.
   * `cle_absente`   : la campagne est perdue si `cle` manque au carnet, que la
   *                   partie soit gagnée ou perdue.
   */
  quand: 'partie_perdue' | 'cle_absente'
  /** Clé du carnet, pour `cle_absente` uniquement. */
  cle?: string
  /** La règle ne vaut qu'en campagne experte (vrai partout sauf aoa). */
  expert_seulement?: boolean
  /** Ce que le livret raconte, montré au joueur. */
  texte?: string
}

export type FaitsDeFin = {
  /** Le scénario qui vient d'être joué est-il le dernier de la campagne ? */
  final: boolean
  /** La règle déclarée par ce scénario, s'il en porte une. */
  regle?: RegleDefaite | null
  /** Les joueurs ont-ils gagné la partie ? */
  gagne: boolean
  /** La campagne est-elle jouée en mode expert ? */
  expert: boolean
  /** Le carnet tel qu'il sera enregistré, relevé compris. */
  carnet: Record<string, string>
}

export type Verdict = {
  perdue: boolean
  /** Le texte du livret à montrer, vide si la campagne n'est pas perdue. */
  texte: string
}

const RIEN: Verdict = { perdue: false, texte: '' }

/**
 * Une campagne ne se perd qu'au dernier scénario, et seulement si ce scénario
 * porte une règle. Un scénario intermédiaire perdu se rejoue, c'est tout le
 * principe : `tentatives` le compte, `termines` ne bouge pas.
 */
export function verdictDeCampagne(faits: FaitsDeFin): Verdict {
  const { regle } = faits
  if (!faits.final || !regle) return RIEN
  if (regle.expert_seulement && !faits.expert) return RIEN

  const texte = regle.texte ?? ''
  if (regle.quand === 'partie_perdue') {
    return faits.gagne ? RIEN : { perdue: true, texte }
  }
  if (regle.quand === 'cle_absente') {
    // Pas de clé déclarée : on ne devine pas, et surtout on ne perd pas une
    // campagne sur une définition incomplète.
    if (!regle.cle) return RIEN
    const valeur = faits.carnet[regle.cle]
    const tenue = valeur !== undefined && valeur !== '' && valeur !== '0'
    return tenue ? RIEN : { perdue: true, texte }
  }
  return RIEN
}
