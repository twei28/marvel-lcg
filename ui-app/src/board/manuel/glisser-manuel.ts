// glisser-manuel.ts — le glisser-déposer du mode manuel, comme sur OCTGN.
//
// Même forme que les réglages du glisser ordinaire (`ReglagesGlisser`) : le
// plateau ne change pas, seule la politique change. Lot 2 du 06/10/2026
// (spec `2026-10-06-mode-manuel-comme-octgn-design.md` §D.2) : comme sur
// OCTGN, lâcher une carte SUR LA TABLE la met en jeu, selon son type
// (`poser-en-jeu.ts`). Le moteur ne vérifie aucune règle : coût, limite et
// cible restent l'affaire du joueur.
//
// ⚠ AUCUN ÉCRIT DIRECT AU JOURNAL. Le geste passe TOUJOURS par `emettreGeste`
// (`CoucheTriche.tsx`, tâche 4 ter) : lui seul sait retarder la ligne jusqu'au
// rendu qui connaît l'issue réelle (`world.manuel_refus`). Écrire ici sur le
// seul succès du dépôt HTTP réintroduirait le défaut qu'on a mis deux rondes
// à corriger — un geste refusé par le moteur affiché comme réussi.
import type { ReglagesGlisser } from '../Board'
import type { CibleSurvolee } from '../glisser/useGlisser'
import { t } from '../langue'
import { libellePile } from '../MenuTriche'
import { attacher, deplacerVers } from '../triche'
import { CLE_PILE_ENGAGES, type CleEmplacement } from '../zones'
import {
  poserEnJeu,
  TYPES_MANIGANCE,
  TYPES_QUI_S_ATTACHENT,
  type CibleAmelioration,
  type ContexteDePose,
  type Origine,
  type Pose,
} from './poser-en-jeu'

/**
 * Les zones où une carte lâchée est vraiment DESSINÉE — jamais un
 * représentant de pile ou de pile fondue (`zones.ts`, `piles`/`pileFondue`),
 * dont l'attache serait invisible : elle rejoindrait un objet que le
 * plateau ne dessine nulle part. C'est une liste POSITIVE, choisie plutôt
 * que son exclusion (I1, correction finale) : une zone de pile ajoutée plus
 * tard sans y figurer est refusée par défaut, jamais acceptée par accident.
 */
const zonesAttachablesListe: CleEmplacement[] = [
  'terrain-combat',
  'terrain-soutien',
  'rencontre',
  'complot-principal',
  'complots-secondaires',
]
const ZONES_ATTACHABLES: ReadonlySet<string> = new Set(zonesAttachablesListe)

/** Les zones de manigance : elles n'acceptent plus que les manigances (D.2, règle 3). */
const ZONES_MANIGANCE: Record<string, string> = {
  'complot-principal': 'MainSchemesArea',
  'complots-secondaires': 'SideSchemesArea',
}

/**
 * La pile dessinée par le plateau (`zones.ts`, `unite.pile`), et son nom côté
 * moteur (`RunPuzzle.ZONES_JOUEUR`/`ZONES_MONDE`, `puzzle.py`).
 *
 * ⚠ CHAQUE ENTRÉE VÉRIFIÉE UNE PAR UNE (voir task-5-report.md) : une pile
 * moteur ne doit apparaître qu'une fois, et sous la clé qui la désigne SANS
 * AMBIGUÏTÉ. Volontairement ABSENTES, plutôt que devinées :
 * `'annexes-visibles'` / `'annexes-cachees'`, FONDUES à l'affichage
 * (`zones.ts`, `pileFondue`) : aucune n'est désignable sans ambiguïté.
 */
export const PILE_PAR_ZONE: Record<string, string> = {
  // Un emplacement qui n'a qu'UN SEUL contenu : pas de pile fine à poser,
  // `data-zone` (le nom de l'emplacement) suffit à désigner la pile.
  main: 'HandsArea',
  reserve: 'ReserveArea',
  // AJOUT (pack wave) : meme forme que 'reserve' juste au-dessus (un seul
  // contenu, `posees()` sans pile fine).
  'rising-tide': 'RisingTideArea',
  ...ZONES_MANIGANCE,

  // Les piles fines de `zones.ts` (`unite.pile`), un deck ou une défausse
  // parmi d'autres dans le même emplacement.
  'rencontre-encounter-deck': 'EncounterDeck',
  'rencontre-encounter-discard': 'EncounterDiscardPile',
  'joueur-deck': 'PlayerDeck',
  'joueur-defausse': 'DiscardPile',
  'soutien-deck': 'AdditionalDeck',
  // Ronde de correction 1 (19/09/2026) : `AdditionalDiscardPile` a rejoint
  // `RunPuzzle.ZONES_JOUEUR` (`puzzle.py`).
  'soutien-defausse': 'AdditionalDiscardPile',
}

/** Ce que le plateau sait d'une carte, lu dans la trame par l'appelant. */
export type ContexteGlisserManuel = {
  /** `faceCachee` : jamais nommée, et rien ne trahit son type (spec D.8). */
  carte: (id: number) => { type: string; nom: string; faceCachee?: boolean } | undefined
  origine: (id: number) => Origine | undefined
  /**
   * Le joueur chez qui la carte arrive (lot 5, question 6) : le siège du
   * groupe visé s'il est donné, sinon le héros affiché.
   */
  contexte: (siege?: number) => ContexteDePose
  /** Le siège à qui est la carte (`proprietaire.ts`) : lâchée dans le vide, elle rentre chez lui. */
  proprietaire: (id: number) => number | undefined
  /** Question 14 : en ligne, chacun ne bouge que ses cartes ; les cartes Rencontre sont à tous. */
  peutBouger: (id: number) => boolean
  /** Vrai si la carte est déjà engagée avec ce joueur (D.2, règle 1). */
  dejaEngage: (id: number) => boolean
  /** Question 3 : plusieurs cartes peuvent recevoir l'amélioration, le joueur choisit. */
  choisirCible: (sourceId: number, nom: string, cibles: CibleAmelioration[]) => void
}

const CONTEXTE_VIDE: ContexteGlisserManuel = {
  carte: () => undefined,
  origine: () => undefined,
  contexte: (siege) => ({ siege: siege ?? 0, ciblesAmelioration: [] }),
  proprietaire: () => undefined,
  peutBouger: () => true,
  dejaEngage: () => false,
  choisirCible: () => undefined,
}

const REFUS_HORS_TABLE = 'Lâche la carte sur la table ou sur une pile'
const REFUS_CACHEE = 'Carte face cachée : retourne-la (Ctrl+F) ou glisse-la sur une pile'

export type Decision =
  | { genre: 'geste'; libelle: string; executer: () => void }
  | { genre: 'rien' }
  | { genre: 'refus'; raison: string }

type Emettre = (libelle: string, deposer: () => Promise<boolean>) => Promise<void>

/**
 * Une pose selon le type (`poser-en-jeu.ts`), en geste, en choix ou en refus.
 * Partagée par le glisser (règle 5) et le double-clic en main (question 8 du
 * 06/10/2026) : les deux gestes posent la carte au même endroit, avec la même
 * ligne de journal.
 */
export function gesteDePose(
  sourceId: number,
  pose: Pose,
  outils: {
    nomDe: (id: number) => string
    emettreGeste: Emettre
    choisirCible: (sourceId: number, nom: string, cibles: CibleAmelioration[]) => void
    /**
     * Carte face cachée (le dessus d'un deck) : l'étiquette ne dit ni son nom
     * ni sa destination, et un refus reste générique, sans quoi le geste
     * trahirait son type avant qu'elle soit retournée (spec D.8).
     */
    cachee?: boolean
    /** Lot 6 du 06/10/2026 : Maj pendant le glisser, la carte arrive face cachée (OCTGN). */
    poserFaceCachee?: boolean
  }
): Decision {
  const nom = outils.nomDe(sourceId)
  const prefixe = t('Poser en jeu')
  if (outils.cachee) {
    if (pose.genre === 'refus') return { genre: 'refus', raison: t(REFUS_CACHEE) }
    const libelle = `${prefixe} : ${nom}`
    if (pose.genre === 'choisir') {
      return { genre: 'geste', libelle, executer: () => outils.choisirCible(sourceId, nom, pose.cibles) }
    }
    const deposer =
      pose.genre === 'deplacer'
        ? () => deplacerVers(sourceId, pose.zone, 'Top', pose.siege)
        : () => attacher(sourceId, pose.cible)
    return { genre: 'geste', libelle, executer: () => void outils.emettreGeste(libelle, deposer) }
  }
  const geste = (libelle: string, deposer: () => Promise<boolean>): Decision => ({
    genre: 'geste',
    libelle,
    executer: () => void outils.emettreGeste(libelle, deposer),
  })
  switch (pose.genre) {
    case 'deplacer':
      if (outils.poserFaceCachee) {
        return geste(`${t('Poser face cachée')} : ${nom} (${libellePile(pose.zone)})`, () =>
          deplacerVers(sourceId, pose.zone, 'Top', pose.siege, true)
        )
      }
      return geste(`${prefixe} : ${nom} (${libellePile(pose.zone)})`, () =>
        deplacerVers(sourceId, pose.zone, 'Top', pose.siege)
      )
    case 'attacher':
      return geste(`${prefixe} : ${nom} (${t('sous')} ${outils.nomDe(pose.cible)})`, () =>
        attacher(sourceId, pose.cible)
      )
    case 'choisir':
      return {
        genre: 'geste',
        libelle: `${prefixe} : ${nom} (${t('choisis la carte qui la reçoit')})`,
        executer: () => outils.choisirCible(sourceId, nom, pose.cibles),
      }
    case 'refus':
      return { genre: 'refus', raison: t(pose.raison) }
  }
}

/** Les piles moteur d'un JOUEUR (`ZONES_JOUEUR`, `puzzle.py`) : elles se visent par siège. */
const PILES_DU_JOUEUR: ReadonlySet<string> = new Set([
  'HandsArea', 'ReserveArea', 'RisingTideArea', 'PlayerDeck', 'DiscardPile', 'AdditionalDeck', 'AdditionalDiscardPile',
])

export function reglagesGlisserManuel(
  /**
   * Dépose un geste sans écrire sa ligne : celle de `useTriche`
   * (`CoucheTriche.tsx`), la même que le menu de triche et le clavier
   * utilisent déjà.
   */
  emettreGeste: Emettre,
  /**
   * Maj enfoncée au moment du lâcher : la carte va SOUS la pile, ou se pose
   * FACE CACHÉE sur la table (lot 6 du 06/10/2026, comme OCTGN). On le
   * demande à l'appelant plutôt que de poser une seconde écoute clavier —
   * `board.tsx` relit `useTriche().estToucheEnfoncee('Shift')`, l'unique
   * écoute du mode manuel (tâche 4).
   */
  sousLaPile: () => boolean = () => false,
  monde: ContexteGlisserManuel = CONTEXTE_VIDE
): ReglagesGlisser {
  const estCachee = (id: number) => monde.carte(id)?.faceCachee === true
  const nomDe = (id: number) => (estCachee(id) ? t('carte face cachée') : (monde.carte(id)?.nom ?? t('carte')))
  const typeDe = (id: number) => monde.carte(id)?.type ?? ''
  /** Le type tel que le JOUEUR le connaît : inconnu tant que la carte est cachée. */
  const typeVisible = (id: number) => (estCachee(id) ? '' : typeDe(id))
  const geste = (libelle: string, deposer: () => Promise<boolean>): Decision => ({
    genre: 'geste',
    libelle,
    executer: () => void emettreGeste(libelle, deposer),
  })

  const decider = (sourceId: number, cible: CibleSurvolee): Decision => {
    const origine = monde.origine(sourceId)
    const type = typeDe(sourceId)
    // Question 6 : chez le héros du groupe visé ; dans le vide, chez celui
    // d'où vient la carte ; une carte à personne, chez le héros affiché.
    const contexte = monde.contexte(cible.siege ?? monde.proprietaire(sourceId))
    const affiche = monde.contexte()

    // Règle 1 : le secteur des ennemis engagés. `MoveTo` et non `Engage`, qui
    // BASCULE (`puzzle.py`) : un sbire déjà engagé relâché sur son secteur ne
    // doit plus se désengager, il ne se passe rien.
    if (cible.secteur === CLE_PILE_ENGAGES) {
      if (monde.dejaEngage(sourceId)) return { genre: 'rien' }
      return geste(`${t('Engager')} — ${nomDe(sourceId)}`, () =>
        deplacerVers(sourceId, 'EngagedEnemiesArea', 'Top', affiche.siege)
      )
    }

    // Règle 2 : une pile fine ou une zone-pile (main, réserve, marée
    // montante). La pile l'emporte sur la carte : une pile se dessine avec une
    // carte (son dessus), et lâcher dessus reste un déplacement de pile.
    const zoneManigance = cible.zone ? ZONES_MANIGANCE[cible.zone] : undefined
    const pile = cible.zone && !zoneManigance ? PILE_PAR_ZONE[cible.zone] : undefined
    if (pile) {
      const dessous = sousLaPile()
      const suite = dessous ? ` (${t('Sous la pile')})` : ''
      return geste(`${t('Déplacer vers')} ${libellePile(pile)}${suite} — ${nomDe(sourceId)}`, () =>
        // Les piles dessinées sont celles du héros affiché. Sans siège, une
        // pile de joueur visait le premier joueur du moment (lot 5).
        deplacerVers(sourceId, pile, dessous ? 'Bottom' : 'Top', PILES_DU_JOUEUR.has(pile) ? affiche.siege : undefined)
      )
    }

    // Règle 3 : les zones de manigance n'acceptent que les manigances.
    if (zoneManigance && TYPES_MANIGANCE.has(type)) {
      if (origine === 'jeu' && cible.carteId === undefined) return { genre: 'rien' }
      return geste(`${t('Déplacer vers')} ${libellePile(zoneManigance)} — ${nomDe(sourceId)}`, () =>
        deplacerVers(sourceId, zoneManigance, 'Top')
      )
    }

    // Règle 4 : sur une carte en jeu, seule une amélioration ou un
    // attachement s'attache (question 2) ; une autre carte suit la règle 5.
    // UNIQUEMENT sur une zone EN JEU connue (I1) : sans cette gate, une carte
    // lâchée sur le représentant d'une pile fondue s'y attachait et
    // disparaissait de la table.
    const surUneCarte =
      cible.carteId !== undefined &&
      cible.carteId !== sourceId &&
      cible.zone !== undefined &&
      ZONES_ATTACHABLES.has(cible.zone)
    if (surUneCarte && TYPES_QUI_S_ATTACHENT.has(type) && cible.carteId !== undefined) {
      const hote = cible.carteId
      return geste(`${t('Attacher')} — ${nomDe(sourceId)} (${t('sous')} ${nomDe(hote)})`, () =>
        attacher(sourceId, hote)
      )
    }

    // Règle 5 : ailleurs sur la table, la carte se pose selon son type.
    // Règle 0 (question 13) : une carte DÉJÀ en jeu relâchée sur la table ne
    // fait rien, aucun geste, rien au journal.
    if (cible.surLaTable) {
      if (origine === 'jeu') return { genre: 'rien' }
      return gesteDePose(sourceId, poserEnJeu({ id: sourceId, type }, contexte), {
        nomDe,
        emettreGeste,
        choisirCible: monde.choisirCible,
        cachee: estCachee(sourceId),
        poserFaceCachee: sousLaPile(),
      })
    }

    // Règle 6 : hors du plateau (journal, barre).
    return { genre: 'refus', raison: t(REFUS_HORS_TABLE) }
  }

  return {
    estSource: (id: number) => monde.peutBouger(id),
    ciblesLegales: (sourceId: number) =>
      TYPES_QUI_S_ATTACHENT.has(typeVisible(sourceId))
        ? new Set(monde.contexte().ciblesAmelioration.map((c) => c.id))
        : new Set<number>(),
    zonesLegales: (sourceId: number) => {
      const zones = new Set([...Object.keys(PILE_PAR_ZONE), CLE_PILE_ENGAGES])
      if (!TYPES_MANIGANCE.has(typeVisible(sourceId))) {
        for (const zone of Object.keys(ZONES_MANIGANCE)) zones.delete(zone)
      }
      return zones
    },
    auDoigt: true,
    accueilleLaTable: (sourceId: number) =>
      monde.origine(sourceId) !== 'jeu' &&
      (estCachee(sourceId) || poserEnJeu({ id: sourceId, type: typeDe(sourceId) }, monde.contexte()).genre !== 'refus'),
    accepte: (sourceId: number, cible: CibleSurvolee) => decider(sourceId, cible).genre !== 'refus',
    libelle: (sourceId: number, cible: CibleSurvolee) => {
      const decision = decider(sourceId, cible)
      return decision.genre === 'geste' ? decision.libelle : undefined
    },
    onDepot: (sourceId: number, cible: CibleSurvolee) => {
      const decision = decider(sourceId, cible)
      if (decision.genre === 'refus') return decision.raison
      if (decision.genre === 'geste') decision.executer()
      return undefined
    },
  }
}
