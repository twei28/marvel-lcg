// Le monde minimal pour demander au plateau CE QU'IL DESSINE d'un état donné.
//
// Pourquoi ce fichier existe (09/09/2026). `tools/test_capacites.py` prouve ce
// que le moteur FAIT ; il ne voit rien de ce que le joueur REGARDE. Superior
// Spider-Man l'a montré : `su001b` Master Planner glissait bien une carte face
// cachée sous `su012` Contingency Plan — le moteur était vert, 32 cas sur 32 —
// et la carte n'apparaissait NULLE PART sur la table, parce que `enUnites` ne
// lisait les attachements que des racines. Un pack peut donc être livré, testé,
// et injouable à l'œil.
//
// Ce module est la moitié manquante : on pose un état de table à la main, on
// demande la liste de ce qui est dessiné, et on affirme dessus. Voir
// `docs/reference/PROCESSUS-CARTE.md` étape 8 bis.
import { catalogueVide } from './catalogue'
import type { ScanCardProps } from '../components/ScanCard'
import { construirePlateau } from './zones'
import type { World, WorldCard, WorldPlayer } from './world'

/** Une carte posée sur la table. `bind` = l'`id` de la carte qui la porte. */
export function carteSurTable(
  id: number,
  cardId: string,
  type: string,
  nom: string,
  surcharge: Partial<WorldCard> = {}
): WorldCard {
  return {
    id,
    card_id: cardId,
    pic_id: cardId,
    card_type: type,
    name: nom,
    is_ready: true,
    is_face_up: true,
    visible_for_players: [0],
    bind_object_id: 0,
    down_card_ids: [],
    resources: [],
    info: {},
    traits: {},
    buffs: {},
    cost: 0,
    ...surcharge,
  } as WorldCard
}

/** Un siège vide, à remplir zone par zone (`area_hero`, `supports`...). */
export function siege(surcharge: Partial<WorldPlayer> = {}): WorldPlayer {
  return {
    area_hero: [],
    allies: [],
    supports: [],
    player_deck: [],
    player_discard_pile: [],
    hand_cards: [],
    engaged_enemies: [],
    obligations_area: [],
    environment_area: [],
    set_aside_deck: [],
    set_aside_nemesis_sets: [],
    additional_deck: [],
    additional_discard_pile: [],
    resources: '',
    is_eliminated: false,
    ...surcharge,
  } as unknown as WorldPlayer
}

/** Un monde à un siège, plus les zones communes qu'on veut peupler. */
export function tableAvec(joueur: WorldPlayer, communes: Partial<World> = {}): World {
  return { render_id: 1, players: [joueur], ...communes } as unknown as World
}

/** Ce qui est réellement dessiné : un élément par carte, attachées comprises. */
export type CarteDessinee = {
  id: number
  /** Zone du plateau où elle atterrit (`terrain-heros`, `piles-rencontre`...). */
  zone: string
  /**
   * `id` de la RACINE de l'unité où elle est dessinée, 0 si elle est
   * elle-même cette racine.
   *
   * ⚠ Ce n'est pas forcément son `bind_object_id` : la cascade d'améliorations
   * est à plat derrière le porteur racine (`Board.tsx`, `.plateau-unite`), donc
   * une carte glissée sous une amélioration remonte à la racine. Ce qui dit
   * « sous QUI » elle est posée, c'est son RANG dans `cartesDessinees` : elle
   * suit immédiatement la carte à laquelle le moteur l'attache.
   */
  portePar: number
  /** Posée face cachée sur la table, mais visible par son propriétaire. */
  peeking: boolean
  /** Face cachée ET invisible pour ce siège : on ne voit que le dos. */
  facedown: boolean
  /** Complot principal verrouillé : nom de la manigance annexe à Crise. */
  crise?: string
  /**
   * La face réellement dessinée (`card.card_id`, ex. `01097a` vs `01097b`),
   * telle que `toScanCard` la publie sous `codeCarte`. Absente si la carte est
   * `facedown` : dans ce cas le plateau ne montre que le dos, pas la face.
   */
  codeCarte?: string
  /** Carte d'une paire jumelle posée en panorama (`panorama-jumelles.ts`). */
  panorama?: 'gauche' | 'droite'
  /** Carte grisee (vilain en attente, ou d'un autre territoire de La ville). */
  inactif?: boolean
  /** Inclinée (épuisée) : la carte est dessinée couchée. */
  exhausted: boolean
  /** Genre d'affichage (`status`, `upgrade`, `enemy`...), tel que `toScanCard` le publie. */
  kind: string
  /** Compteurs dessinés sur la carte : nom français -> valeur (rage, temps...). */
  compteurs: Record<string, number>
  /** Jeton de menace posé sur la carte (manigance), absent si 0. */
  menace?: number
  /** Pour une pile (deck, défausse) : nombre de cartes qu'elle représente. */
  pileCount?: number
}

function detailsDessines(carte: ScanCardProps) {
  const compteurs: Record<string, number> = {}
  for (const c of carte.counters ?? []) compteurs[c.cle ?? c.label] = c.value
  return {
    exhausted: !!carte.exhausted,
    kind: carte.kind,
    compteurs,
    pileCount: carte.pileCount,
    menace: carte.jetonMenace,
  }
}

/**
 * Tout ce que le plateau dessine, à plat, quelle que soit la zone.
 *
 * Une carte ABSENTE de cette liste n'est nulle part à l'écran : c'est la seule
 * assertion qui aurait attrapé le défaut de Contingency Plan.
 */
export function cartesDessinees(world: World, playerId = 0): CarteDessinee[] {
  const plateau = construirePlateau(world, { playerId, catalogue: catalogueVide })
  const vues: CarteDessinee[] = []
  for (const emplacement of plateau.emplacements) {
    for (const groupe of emplacement.groupes) {
      for (const unite of groupe) {
        const racine = Number(unite.carte.id)
        vues.push({
          id: racine,
          zone: emplacement.cle,
          portePar: 0,
          peeking: !!unite.carte.peeking,
          facedown: !!unite.carte.facedown,
          crise: unite.carte.crise,
          panorama: unite.panorama,
          inactif: unite.carte.inactif,
          codeCarte: unite.carte.codeCarte,
          ...detailsDessines(unite.carte),
        })
        for (const attachee of unite.attachees) {
          vues.push({
            id: Number(attachee.id),
            zone: emplacement.cle,
            portePar: racine,
            peeking: !!attachee.peeking,
            facedown: !!attachee.facedown,
            codeCarte: attachee.codeCarte,
            ...detailsDessines(attachee),
          })
        }
      }
    }
  }
  return vues
}

/** La carte dessinée portant cet `id`, ou `undefined` si elle est invisible. */
export function dessinee(world: World, id: number, playerId = 0): CarteDessinee | undefined {
  return cartesDessinees(world, playerId).find((c) => c.id === id)
}
