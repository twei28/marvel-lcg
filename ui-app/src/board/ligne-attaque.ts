// Sous « Ne pas défendre » : CE QUI EST CONNU de l'attaque au moment de
// choisir, jamais un total.
//
// Rules Reference v1.8, « Attack (Enemy Activation) » : la carte boost est
// donnee face cachee AVANT la declaration du defenseur (etape 1) et retournee
// APRES (etape 3). L'utilisateur, 04/10/2026 : « le joueur ne sait pas le
// nombre de dégâts final avant de défendre ». D'ou « ATQ 3 + 1 carte boost ».
//
// ⚠ Un sbire AVEC Villainous recoit lui aussi un boost : on ne decide donc
// rien sur le type d'attaquant, on COMPTE les cartes face cachee qui lui sont
// attachees (`boostable`, publie par `ToDescriptor.Card` a la suite de
// l'ennemi, `bind_object_id` = l'ennemi).
import type { Option } from './ask'
import { t } from './langue'
import type { WorldCard } from './world'

type Bonus = [string, number, number]

/**
 * « ATQ 2 + 3 Charge + 1 carte boost » : la valeur IMPRIMEE (la valeur actuelle
 * moins ses bonus), puis chaque bonus avec sa carte, puis ce qui reste
 * inconnu. Decision du 04/10/2026 : deux bonus nommes au plus ; au-dela, leurs
 * points restants en « + N autres » (`abreger` faux : tout le detail, pour le
 * survol). Jamais un total : le boost n'est pas encore retourne.
 */
function detailCaracteristique(
  sigle: string,
  actuelle: number,
  bonus: Bonus[],
  suite: string,
  nomFr?: (id: number) => string | undefined,
  abreger = true
): string {
  const somme = bonus.reduce((total, [, , valeur]) => total + valeur, 0)
  const morceau = ([nom, id, valeur]: Bonus) =>
    `${valeur < 0 ? '−' : '+'} ${Math.abs(valeur)} ${nomFr?.(id) ?? nom}`
  const nommes = abreger ? bonus.slice(0, 2) : bonus
  const reste = abreger ? bonus.slice(2).reduce((total, [, , valeur]) => total + valeur, 0) : 0
  const autres = reste !== 0 ? [`${reste < 0 ? '−' : '+'} ${Math.abs(reste)} ${t('autres')}`] : []
  return [`${t(sigle)} ${actuelle - somme}`, ...nommes.map(morceau), ...autres].join(' ') + suite
}

function attaquantEtBoosts(options: Option[], cartesParId: Map<number, WorldCard>) {
  const defense = options.find((option) => option.name === 'Defense')
  const idAttaquant = defense?.all_legal_targets?.[0]
  const attaquant = idAttaquant !== undefined ? cartesParId.get(idAttaquant) : undefined
  const atq = attaquant?.info?.attack
  if (!attaquant || typeof atq !== 'number') return undefined
  let boosts = 0
  for (const carte of cartesParId.values()) {
    if (carte.bind_object_id === attaquant.id && !carte.is_face_up) boosts += 1
  }
  const suite = boosts > 0 ? ` + ${boosts} ${boosts > 1 ? t('cartes boost') : t('carte boost')}` : ''
  return { atq, bonus: attaquant.bonus?.ATK ?? [], suite }
}

export function ligneAttaqueConnue(
  options: Option[],
  cartesParId: Map<number, WorldCard>,
  nomFr?: (id: number) => string | undefined
): string | undefined {
  const a = attaquantEtBoosts(options, cartesParId)
  return a ? detailCaracteristique('ATQ', a.atq, a.bonus, a.suite, nomFr) : undefined
}

/** Le meme detail sans abreger, pour le survol du bouton. */
export function detailAttaqueComplet(
  options: Option[],
  cartesParId: Map<number, WorldCard>,
  nomFr?: (id: number) => string | undefined
): string | undefined {
  const a = attaquantEtBoosts(options, cartesParId)
  return a ? detailCaracteristique('ATQ', a.atq, a.bonus, a.suite, nomFr, false) : undefined
}

/** « DÉF 2 + 1 Bouclier » : la defense du personnage qui defendrait. */
export function ligneDefense(
  carte: WorldCard | undefined,
  nomFr?: (id: number) => string | undefined,
  abreger = true
): string | undefined {
  const def = carte?.info?.defense
  if (!carte || typeof def !== 'number') return undefined
  return detailCaracteristique('DÉF', def, carte.bonus?.DEF ?? [], '', nomFr, abreger)
}
