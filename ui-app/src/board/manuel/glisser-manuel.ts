// glisser-manuel.ts — glisser n'importe quelle carte vers n'importe quelle
// pile, ou n'importe quelle autre carte.
//
// Même forme que les réglages du glisser ordinaire (`ReglagesGlisser`), et
// c'est tout l'intérêt : le plateau ne change pas, seule la politique change.
// Ici il n'y a aucune politique : tout se soulève, tout s'accueille, rien ne
// s'allume. Une cible mise en valeur voudrait dire « c'est ici qu'il faut
// poser », et le mode manuel ne sait rien de ce qu'il faut.
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
import { attacher, deplacerVers, engager } from '../triche'
import { CLE_PILE_ENGAGES } from '../zones'

/**
 * La pile dessinée par le plateau (`zones.ts`, `unite.pile`), et son nom côté
 * moteur (`RunPuzzle.ZONES_JOUEUR`/`ZONES_MONDE`, `puzzle.py`).
 *
 * ⚠ CHAQUE ENTRÉE VÉRIFIÉE UNE PAR UNE (voir task-5-report.md) : une pile
 * moteur ne doit apparaître qu'une fois, et sous la clé qui la désigne SANS
 * AMBIGUÏTÉ. Deux zones du plateau qui se ressemblent (le deck du héros et le
 * deck spécial, tous deux appelés « deck » côté `zones.ts` avant préfixage)
 * ne doivent JAMAIS pointer vers la même pile moteur — c'est exactement le
 * défaut que la table du brief faisait (« nemesis » et « set-aside-scenario »
 * pointaient tous deux vers `'AsideDeck'`, qui ne désigne QUE le set némésis
 * du joueur).
 *
 * Volontairement ABSENTES, plutôt que devinées :
 *  - `'annexes-visibles'` / `'annexes-cachees'` : ces piles sont FONDUES à
 *    l'affichage (`zones.ts`, `pileFondue`) — victoire, retirées, mises de
 *    côté du scénario, etc. partagent un seul dos de carte. Aucune n'est
 *    désignable sans ambiguïté depuis ce seul dos ; `zones.ts` ne leur pose
 *    donc pas de `pile`, et un lâcher dessus retombe sur `data-zone`
 *    (`'annexes'`), lui aussi absent d'ici : refus poli, jamais un geste au
 *    hasard parmi les trois.
 */
export const PILE_PAR_ZONE: Record<string, string> = {
  // Un emplacement qui n'a qu'UN SEUL contenu : pas de pile fine à poser,
  // `data-zone` (le nom de l'emplacement) suffit à désigner la pile.
  main: 'HandsArea',
  reserve: 'ReserveArea',
  'complot-principal': 'MainSchemesArea',
  'complots-secondaires': 'SideSchemesArea',

  // Les piles fines de `zones.ts` (`unite.pile`), un deck ou une défausse
  // parmi d'autres dans le même emplacement.
  'rencontre-encounter-deck': 'EncounterDeck',
  'rencontre-encounter-discard': 'EncounterDiscardPile',
  'joueur-deck': 'PlayerDeck',
  'joueur-defausse': 'DiscardPile',
  'soutien-deck': 'AdditionalDeck',
  // Ronde de correction 1 (19/09/2026) : `AdditionalDiscardPile` a rejoint
  // `RunPuzzle.ZONES_JOUEUR` (`puzzle.py`) — cette entrée était refusée
  // jusque-là, faute de pile moteur à viser.
  'soutien-defausse': 'AdditionalDiscardPile',
  'annexes-nemesis': 'AsideDeck',
}

export function reglagesGlisserManuel(
  /**
   * Dépose un geste sans écrire sa ligne : celle de `useTriche`
   * (`CoucheTriche.tsx`), la même que le menu de triche et le clavier
   * utilisent déjà.
   */
  emettreGeste: (libelle: string, deposer: () => Promise<boolean>) => Promise<void>,
  /**
   * Maj enfoncée au moment du lâcher : la carte va SOUS la pile. On le
   * demande à l'appelant plutôt que de poser une seconde écoute clavier —
   * `board.tsx` relit `useTriche().estToucheEnfoncee('Shift')`, l'unique
   * écoute du mode manuel (tâche 4).
   */
  sousLaPile: () => boolean = () => false
): ReglagesGlisser {
  return {
    estSource: () => true,
    ciblesLegales: () => new Set<number>(),
    zonesLegales: () => new Set([...Object.keys(PILE_PAR_ZONE), CLE_PILE_ENGAGES]),
    libelle: (_sourceId: number, cible: CibleSurvolee) => {
      if (cible.zone === CLE_PILE_ENGAGES) return t('Engager')
      const pile = cible.zone ? PILE_PAR_ZONE[cible.zone] : undefined
      if (pile) return `${t('Déplacer vers')} ${libellePile(pile)}`
      if (cible.carteId !== undefined) return t('Attacher')
      return undefined
    },
    onDepot: (sourceId: number, cible: CibleSurvolee) => {
      // Un sbire lâché sur les ennemis engagés du joueur s'engage
      // (`Puzzle.Engage`), pas un déplacement de pile ordinaire : c'est lui
      // qui fait le va-et-vient engagé/désengagé, et l'aire n'est pas une
      // pile qu'on pourrait viser par `MoveTo`.
      if (cible.zone === CLE_PILE_ENGAGES) {
        void emettreGeste(t('Engager'), () => engager(sourceId))
        return undefined
      }
      // La pile l'emporte sur la carte : une pile se dessine avec une carte
      // (son dessus), et lâcher dessus doit rester un déplacement de pile,
      // jamais une tentative d'attache sur ce dessus.
      const pile = cible.zone ? PILE_PAR_ZONE[cible.zone] : undefined
      if (pile) {
        void emettreGeste(`${t('Déplacer vers')} ${libellePile(pile)}`, () =>
          deplacerVers(sourceId, pile, sousLaPile() ? 'Bottom' : 'Top')
        )
        return undefined
      }
      // Lâchée sur une autre carte (ni une pile, ni elle-même) : on attache.
      if (cible.carteId !== undefined && cible.carteId !== sourceId) {
        const cibleId = cible.carteId
        void emettreGeste(t('Attacher'), () => attacher(sourceId, cibleId))
        return undefined
      }
      return t('Lâche la carte sur une pile')
    },
  }
}
