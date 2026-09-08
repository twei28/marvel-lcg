/**
 * Le calcul du glisser-deposer, cote SOURCE.
 *
 * Le plateau savait deja repondre a « pour cette CIBLE, quelles actions ? »
 * (`optionsDisponiblesVersCible`, board.tsx) : c'est ce dont le clic a besoin.
 * Le glisser pose la question dans l'autre sens, et c'est le seul calcul neuf
 * de tout le chantier : « je souleve cette carte, ou puis-je la poser ? »
 *
 * ⚠ TOUT VIENT DU MOTEUR, RIEN N'EST DEVINE. Chaque option qu'il propose porte
 * `all_legal_targets` (les cibles legales) et `target_num_range` (combien il en
 * faut). On lit, on filtre, on ne juge jamais a la place des regles.
 *
 * ⚠ CE MODULE NE TOUCHE NI AU DOM NI A REACT, a dessein : c'est la partie qui
 * se teste sans navigateur, et c'est aussi celle qui porte les regles.
 */
import type { Option } from '../ask'

/** Une option est offerte si le moteur ne l'a pas refusee d'avance. */
function offerte(option: Option): boolean {
  return option.failure_reason === ''
}

/**
 * Les options portees par la carte qu'on souleve.
 *
 * ⚠ `bind_id === 0` DESIGNE LES ACTIONS GENERALES (celles qui n'appartiennent
 * a aucune carte : changer de forme, finir le tour...). Elles sont rattachees
 * a l'IDENTITE, comme le fait deja le mode simple au clic : sans cela, glisser
 * son heros ne proposerait que ses capacites imprimees.
 */
export function optionsDeLaSource(
  options: Option[],
  sourceId: number,
  identiteId?: number
): Option[] {
  return options.filter(
    (option) =>
      option.bind_id === sourceId ||
      (option.bind_id === 0 && identiteId !== undefined && sourceId === identiteId)
  )
}

/**
 * Peut-on soulever cette carte ? Oui des qu'une action offerte en part.
 *
 * On n'exige PAS qu'elle ait des cibles : une carte qui se joue sans cible
 * (un allie, un soutien) se glisse vers sa zone, voir `zonesDeLaSource`.
 */
export function estSourceGlissable(
  options: Option[],
  sourceId: number,
  identiteId?: number
): boolean {
  return optionsDeLaSource(options, sourceId, identiteId).some(offerte)
}

/**
 * Les cartes sur lesquelles cette source peut etre lachee.
 *
 * ⚠ ON N'EN RETIENT QUE CE QUI EST DESSINE. Une cible legale peut etre enfouie
 * dans une pile : le clic la propose dans un selecteur a part, mais on ne peut
 * pas glisser vers ce qu'on ne voit pas. Elle reste donc au clic, et le
 * plateau ne l'allume pas.
 */
export function ciblesDeLaSource(
  options: Option[],
  sourceId: number,
  idsAffiches: ReadonlySet<number>,
  identiteId?: number
): Set<number> {
  const cibles = new Set<number>()
  for (const option of optionsDeLaSource(options, sourceId, identiteId)) {
    if (!offerte(option)) continue
    if (option.target_num_range[1] <= 0) continue
    for (const cible of option.all_legal_targets) {
      if (idsAffiches.has(cible)) cibles.add(cible)
    }
  }
  cibles.delete(sourceId)
  return cibles
}

/**
 * Les options qui s'appliquent VRAIMENT au couple (source, cible) lache.
 *
 * Zero option : le lacher est refuse, voir `raisonDuRefus`.
 * Une seule : elle part, cible deja remplie.
 * Plusieurs : le plateau ouvre son menu de ciblage, comme au clic.
 */
export function optionsDuDepot(
  options: Option[],
  sourceId: number,
  cibleId: number,
  identiteId?: number
): Option[] {
  return optionsDeLaSource(options, sourceId, identiteId).filter(
    (option) =>
      offerte(option) &&
      option.target_num_range[1] > 0 &&
      option.all_legal_targets.includes(cibleId)
  )
}

/**
 * Ce que la source peut faire SANS cible : jouer un allie, poser un soutien.
 * Ces options se lachent dans une zone du plateau, pas sur une carte.
 */
export function optionsSansCible(
  options: Option[],
  sourceId: number,
  identiteId?: number
): Option[] {
  return optionsDeLaSource(options, sourceId, identiteId).filter(
    (option) => offerte(option) && option.target_num_range[1] <= 0
  )
}

/**
 * Pourquoi ce lacher est refuse, dans les mots du moteur.
 *
 * ⚠ ON PREFERE TOUJOURS UNE RAISON DU MOTEUR A UNE PHRASE INVENTEE. Quand une
 * option de cette source nomme bien la cible mais porte un `failure_reason`,
 * c'est exactement le refus qu'il faut montrer (« un Gardien vous en
 * empeche »). Ce n'est qu'a defaut qu'on rend `undefined`, et l'appelant dit
 * alors quelque chose de general.
 */
export function raisonDuRefus(
  options: Option[],
  sourceId: number,
  cibleId: number,
  identiteId?: number
): string | undefined {
  for (const option of optionsDeLaSource(options, sourceId, identiteId)) {
    if (offerte(option)) continue
    if (option.all_legal_targets.includes(cibleId)) return option.failure_reason
  }
  for (const option of optionsDeLaSource(options, sourceId, identiteId)) {
    if (!offerte(option)) return option.failure_reason
  }
  return undefined
}

/**
 * Les ZONES du plateau qui acceptent la carte qu'on souleve, et la cible que
 * chacune designe.
 *
 * ⚠ ON NE DEVINE PLUS LA ZONE D'APRES LE TYPE DE CARTE, ET C'EST UNE LECON DE
 * PARTIE REELLE (08/09/2026). On croyait qu'un allie se jouait « sans cible »
 * et atterrissait dans la ligne de combat. Le moteur dit autre chose : jouer
 * une carte de la main est une option qui VISE l'identite (`Play`, plage
 * [1, 1], cible = l'identite). Une regle ecrite sur le type de carte se serait
 * donc trompee sur toutes les cartes de la main.
 *
 * La regle vraie est plus simple, et elle vient du moteur : une zone accepte la
 * carte quand elle contient une cible legale, et lacher dans la zone revient a
 * lacher sur cette cible. Concretement, on jette un allie dans l'aire de son
 * heros, la ou vit l'identite qu'il rejoint.
 *
 * ⚠ EXACTEMENT UNE CIBLE, PAS DEUX. Une zone qui en contiendrait plusieurs
 * serait ambigue : on laisse alors le joueur viser la carte precise, et la zone
 * n'est pas proposee.
 */
export function zonesDeLaSource(
  options: Option[],
  sourceId: number,
  zoneDeLaCarte: (id: number) => string | undefined,
  identiteId?: number
): Map<string, number> {
  const parZone = new Map<string, Set<number>>()
  for (const option of optionsDeLaSource(options, sourceId, identiteId)) {
    if (!offerte(option)) continue
    if (option.target_num_range[1] <= 0) continue
    for (const cible of new Set(option.all_legal_targets)) {
      if (cible === sourceId) continue
      const zone = zoneDeLaCarte(cible)
      if (!zone) continue
      const deja = parZone.get(zone)
      if (deja) deja.add(cible)
      else parZone.set(zone, new Set([cible]))
    }
  }
  const seules = new Map<string, number>()
  for (const [zone, cibles] of parZone) {
    if (cibles.size === 1) seules.set(zone, [...cibles][0]!)
  }
  return seules
}
