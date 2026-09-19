// MenuTriche.tsx — le menu qui s'ouvre au clic droit, en mode Bac à sable.
//
// Un seul geste pour tout le mode : clic droit. Sur une carte du plateau, il
// ouvre ses interventions ; sur une pile, il ouvre son contenu (voir
// PileTriche). Le clic GAUCHE reste le jeu normal, sans exception — c'est ce
// qui permet de tricher au milieu d'une partie sans jamais se tromper de geste.
//
// Le menu se ferme dès qu'on agit : enchaîner deux interventions sur la même
// carte demande deux clics droits. C'est volontaire — un menu qui reste ouvert
// masque le plateau, or on veut justement VOIR l'effet de ce qu'on vient de
// faire.

import { useEffect, useRef, useState } from 'react'
import { t } from './langue'
import * as triche from './triche'

export type CibleTriche = {
  id: number
  nom: string
  /** Une manigance : on propose la menace plutôt que les points de vie. */
  estManigance?: boolean
  /** Un personnage : points de vie, inclinaison, états. */
  estPersonnage?: boolean
}

/**
 * Les piles atteignables depuis « Déplacer vers », nommées comme côté moteur
 * (`DeckType`, `RunPuzzle.ZONES_JOUEUR`/`ZONES_MONDE`). PURE DONNÉE : elle ne
 * change pas avec la langue, contrairement à son libellé (`libellePile`).
 */
export const ZONES_MANUELLES: readonly string[] = [
  'HandsArea',
  'PlayerDeck',
  'DiscardPile',
  'AlliesArea',
  'SupportsArea',
  'EngagedEnemiesArea',
  'EncounterDeck',
  'EncounterDiscardPile',
  'SideSchemesArea',
  'VillainArea',
  'RemovedArea',
  'VictoryDisplay',
  'AsideDeck',
]

/**
 * Le libellé affiché d'une pile atteignable.
 *
 * ⚠ UNE FONCTION, JAMAIS UNE CONSTANTE DE MODULE : la langue est choisie au
 * chargement de l'appli, une table bâtie avec `t()` au niveau du module la
 * figerait avant qu'elle ne soit connue. `t()` ne doit s'exécuter qu'à
 * l'affichage, donc dans le composant.
 *
 * ⚠ `AsideDeck` EST PRÉCISÉ. Plusieurs piles moteur portent le type
 * `AsideDeck` (côté joueur, côté monde) ; celle visée par ce menu est
 * `set_aside_nemesis_sets` (voir `triche.ts`, `RunPuzzle.ZONES_JOUEUR` côté
 * moteur) — le set némésis du héros, déjà nommé ainsi dans `zones.ts`. Un
 * libellé « Cartes écartées » sans plus de précision ferait déplacer des
 * cartes dans une pile qu'on ne regarde jamais.
 */
export function libellePile(zone: string): string {
  switch (zone) {
    case 'HandsArea': return t('Main')
    case 'PlayerDeck': return t('Deck du héros')
    case 'DiscardPile': return t('Pile de défausse')
    case 'AlliesArea': return t('Alliés')
    case 'SupportsArea': return t('Soutiens')
    case 'EngagedEnemiesArea': return t('Ennemis engagés')
    case 'EncounterDeck': return t('Deck Rencontre')
    case 'EncounterDiscardPile': return t('Défausse Rencontre')
    case 'SideSchemesArea': return t('Manigances annexes')
    case 'VillainArea': return t('Zone du vilain')
    case 'RemovedArea': return t('Retirées de la partie')
    case 'VictoryDisplay': return t('Pile de victoire')
    // MÊME CLÉ QUE `zones.ts` (`t('Set némésis')`), PAS UNE NOUVELLE. C'est le
    // même objet — `set_aside_nemesis_sets` — déjà nommé ainsi ailleurs sur le
    // plateau. Deux libellés pour une seule pile serait une hésitation que le
    // joueur paierait, sans lever l'ambiguïté avec les AUTRES piles moteur qui
    // portent aussi le type `AsideDeck` (côté monde) : celles-là ne sont pas
    // dans ce menu, donc pas de collision ici.
    case 'AsideDeck': return t('Set némésis')
    default: return zone
  }
}

/**
 * Les piles où « sous la pile » a un sens : un deck ORDONNÉ, où le dessous
 * diffère du dessus. Côté moteur (`puzzle.py`, `MoveTo`), `position='Bottom'`
 * n'est traité différemment que si `pile.flags.is_deck` ou
 * `is_dealt_encounter` est vrai (`game/deck/deck_type.py`) : c'est le cas de
 * ces quatre-là, et d'aucune autre zone de `ZONES_MANUELLES`. Sur les neuf
 * autres (des zones EN JEU, face visible, sans dessus/dessous), `MoveTo`
 * pose la carte normalement quelle que soit la position demandée : le bouton
 * y ferait exactement la même chose que le bouton principal, deux fois le
 * même geste. NE PAS L'AJOUTER AILLEURS sans vérifier ce drapeau côté moteur.
 */
const ZONES_ORDONNEES: ReadonlySet<string> = new Set([
  'PlayerDeck',
  'DiscardPile',
  'EncounterDeck',
  'EncounterDiscardPile',
])

export type MenuTricheProps = {
  cible: CibleTriche
  /** Position du clic, en pixels écran. */
  x: number
  y: number
  onFermer: () => void
  /** Raconte l'intervention à l'historique de partie. */
  onIntervention: (libelle: string) => void
}

/** Une entrée du menu. `valeur` ouvre une saisie de nombre avant d'agir. */
type Entree = {
  libelle: string
  agir: (valeur: number) => Promise<boolean>
  valeur?: number
  danger?: boolean
}

export function MenuTriche({ cible, x, y, onFermer, onIntervention }: MenuTricheProps) {
  const [saisie, setSaisie] = useState<Entree | undefined>(undefined)
  const [nombre, setNombre] = useState(1)
  // Le sous-menu « Déplacer vers » : une liste de piles plutôt qu'une saisie
  // de nombre, donc un état à part de `saisie`.
  const [deplacer, setDeplacer] = useState(false)
  const boite = useRef<HTMLDivElement | null>(null)

  // Fermeture au clic extérieur et à Échap : sans ça, un menu oublié reste
  // par-dessus le plateau et intercepte les clics de jeu.
  useEffect(() => {
    const dehors = (evenement: MouseEvent) => {
      if (boite.current && !boite.current.contains(evenement.target as Node)) onFermer()
    }
    const touche = (evenement: KeyboardEvent) => {
      if (evenement.key === 'Escape') onFermer()
    }
    document.addEventListener('mousedown', dehors)
    document.addEventListener('keydown', touche)
    return () => {
      document.removeEventListener('mousedown', dehors)
      document.removeEventListener('keydown', touche)
    }
  }, [onFermer])

  const entrees: Entree[] = []

  if (cible.estManigance) {
    entrees.push(
      { libelle: t('Poser de la menace'), valeur: 1, agir: (n) => triche.poserMenace(cible.id, n) },
      { libelle: t('Retirer de la menace'), valeur: 1, agir: (n) => triche.poserMenace(cible.id, -n) },
      { libelle: t('Fixer la menace à'), valeur: 0, agir: (n) => triche.fixerMenace(cible.id, n) },
    )
  } else {
    entrees.push(
      { libelle: t('Soigner'), valeur: 3, agir: (n) => triche.soigner(cible.id, n) },
      { libelle: t('Infliger des dégâts'), valeur: 3, agir: (n) => triche.blesser(cible.id, n) },
    )
  }

  if (cible.estPersonnage !== false) {
    entrees.push(
      { libelle: t('Redresser'), agir: () => triche.redresser(cible.id) },
      { libelle: t('Incliner'), agir: () => triche.incliner(cible.id) },
      { libelle: t('Rendre désorienté'), agir: () => triche.rendreConfus(cible.id) },
      { libelle: t('Rendre sonné'), agir: () => triche.assommer(cible.id) },
      // ECART CORRIGE le 14/09/2026 : ce menu disait « coriace » la ou la carte,
      // les mots-cles et les textes FR officiels disent tous « Tenace ». Le nom
      // interne `rendreCoriace` n'est pas touche : il n'est vu par personne.
      { libelle: t('Rendre tenace'), agir: () => triche.rendreCoriace(cible.id) },
    )
  }

  entrees.push(
    { libelle: t('Ajouter des compteurs'), valeur: 1,
      agir: (n) => triche.poserCompteur(cible.id, 'counter', n) },
    { libelle: t('Défausser'), agir: () => triche.defausser(cible.id), danger: true },
    { libelle: t('Retirer de la partie'), agir: () => triche.retirer(cible.id), danger: true },
  )

  const executer = async (entree: Entree, valeur: number) => {
    const reussi = await entree.agir(valeur)
    const chiffre = entree.valeur !== undefined ? ` ${valeur}` : ''
    onIntervention(
      `${entree.libelle}${chiffre} — ${cible.nom}${reussi ? '' : ` (${t('refusé')})`}`
    )
    onFermer()
  }

  const executerDeplacement = async (zone: string, position: 'Top' | 'Bottom') => {
    const reussi = await triche.deplacerVers(cible.id, zone, position)
    const suite = position === 'Bottom' ? ` (${t('Sous la pile')})` : ''
    onIntervention(
      `${t('Déplacer vers')} ${libellePile(zone)}${suite} — ${cible.nom}` +
        `${reussi ? '' : ` (${t('refusé')})`}`
    )
    onFermer()
  }

  // Le menu est placé au curseur, mais ramené dans l'écran s'il déborde : un
  // clic droit près du bord bas ouvrait sinon un menu partiellement invisible.
  const style = {
    left: Math.min(x, window.innerWidth - 240),
    top: Math.min(y, window.innerHeight - 340),
  }

  return (
    <div className="menu-triche" style={style} ref={boite} role="menu">
      <header className="menu-triche-titre">
        <span>{cible.nom}</span>
        <span className="menu-triche-marque">{t('Triche')}</span>
      </header>

      {saisie ? (
        <div className="menu-triche-saisie">
          <label>
            {saisie.libelle}
            <input
              type="number"
              value={nombre}
              autoFocus
              onChange={(e) => setNombre(Number(e.target.value))}
              onKeyDown={(e) => {
                if (e.key === 'Enter') void executer(saisie, nombre)
              }}
            />
          </label>
          <div className="menu-triche-boutons">
            <button type="button" onClick={() => setSaisie(undefined)}>{t('Retour')}</button>
            <button type="button" onClick={() => void executer(saisie, nombre)}>
              {t('Appliquer')}
            </button>
          </div>
        </div>
      ) : deplacer ? (
        <div className="menu-triche-deplacer">
          <ul className="menu-triche-liste">
            {ZONES_MANUELLES.map((zone) => (
              <li key={zone} className="menu-triche-deplacer-ligne">
                <button type="button" onClick={() => void executerDeplacement(zone, 'Top')}>
                  {libellePile(zone)}
                </button>
                {ZONES_ORDONNEES.has(zone) ? (
                  <button
                    type="button"
                    className="menu-triche-sous"
                    onClick={() => void executerDeplacement(zone, 'Bottom')}
                  >
                    {t('Sous la pile')}
                  </button>
                ) : null}
              </li>
            ))}
          </ul>
          <div className="menu-triche-boutons">
            <button type="button" onClick={() => setDeplacer(false)}>{t('Retour')}</button>
          </div>
        </div>
      ) : (
        <ul className="menu-triche-liste">
          <li>
            <button type="button" onClick={() => setDeplacer(true)}>
              {t('Déplacer vers')}
              <span className="menu-triche-suite">…</span>
            </button>
          </li>
          {entrees.map((entree) => (
            <li key={entree.libelle}>
              <button
                type="button"
                className={entree.danger ? 'est-danger' : undefined}
                onClick={() => {
                  if (entree.valeur !== undefined) {
                    setNombre(entree.valeur)
                    setSaisie(entree)
                  } else {
                    void executer(entree, 0)
                  }
                }}
              >
                {entree.libelle}
                {entree.valeur !== undefined ? <span className="menu-triche-suite">…</span> : null}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
