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

import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { t } from './langue'
import { useGlisserPanneau } from './placement/useGlisserPanneau'
import * as triche from './triche'

export type CibleTriche = {
  id: number
  nom: string
  /** Une manigance : on propose la menace plutôt que les points de vie. */
  estManigance?: boolean
  /** Un personnage : points de vie, inclinaison, états. */
  estPersonnage?: boolean
  /**
   * Le siège visé par une pile de JOUEUR (lot 5 du 06/10/2026) : celui du
   * propriétaire de la carte. Sans lui, la pile visait le premier joueur du
   * moment.
   */
  siege?: number
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
  // Tâche 5, ronde de correction 1 (19/09/2026) : ces trois piles étaient
  // atteignables par GLISSER (`glisser-manuel.ts`, `PILE_PAR_ZONE`) mais
  // absentes d'ici. `ReserveArea` et `MainSchemesArea` disparaissent du
  // plateau dès que leur emplacement est vide (`zones.ts`, `emplacement()`
  // ne dessine pas un groupe vide) : sans une entrée ici, une pile alors
  // invisible au plateau devenait DÉFINITIVEMENT inatteignable (ni glisser,
  // ni clic droit). Voir le test qui généralise ce contrôle,
  // `board/manuel/glisser-manuel.test.ts`.
  'ReserveArea',
  // AJOUT (pack wave) : la Rising Tide area, meme famille que ReserveArea
  // juste au-dessus, atteignable par le glisser (`PILE_PAR_ZONE`,
  // glisser-manuel.ts) mais qui manquait ici.
  'RisingTideArea',
  'MainSchemesArea',
  'AdditionalDeck',
  // La défausse du deck spécial : le moteur ne l'exposait à AUCUNE des deux
  // voies avant cette même ronde (`RunPuzzle.ZONES_JOUEUR`, `puzzle.py`).
  'AdditionalDiscardPile',
  // I2 (revue finale) : ces deux piles du MONDE (`RunPuzzle.ZONES_MONDE`,
  // `puzzle.py`) n'étaient atteignables par AUCUN geste. Le glisser ne peut
  // pas les viser : leurs cartes sont fondues à l'affichage dans « Cartes
  // visibles » (`zones.ts`, `pileFondue`, zone `annexes`), qui ne pose pas
  // de `data-pile` pour rester ambiguë entre victoire/retirées/mises de
  // côté. Le menu, lui, n'a pas ce problème : il vise la pile par NOM, pas
  // par carte dessinée.
  'AsideScenario',
  'AsideModular',
  // Suite de la revue finale (20/09/2026) : la même famille de trou que
  // AsideScenario/AsideModular juste au-dessus, trouvée en vérifiant à la
  // main le reste de `RunPuzzle.ZONES_JOUEUR`/`ZONES_MONDE` (`puzzle.py`).
  // Aucune des cinq n'est visée par le glisser (aucune entrée dans
  // `PILE_PAR_ZONE`, `glisser-manuel.ts`) : le menu est le SEUL geste qui
  // les atteigne, comme pour les deux précédentes. Voir le test de
  // propriété étendu, `MenuTriche.test.tsx`.
  'HeroArea',
  'ResourcesArea',
  'ObligationsArea',
  'EnvironmentArea',
  'ProcessingArea',
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
    // Tache 5 (glisser-depose) : le deck SPECIAL du heros (Invocation,
    // Reserve...) devient une cible atteignable par glisser, la ou ce menu
    // ne l'offrait pas encore. Meme repli que `nomDeckSpecial` (zones.ts)
    // quand aucun nom plus precis n'est connu ici.
    case 'AdditionalDeck': return t('Deck spécial')
    // Ronde de correction 1 (19/09/2026) : ces trois manquaient au menu alors
    // que le glisser les atteignait déjà. Voir `ZONES_MANUELLES`.
    case 'AdditionalDiscardPile': return t('Défausse du deck spécial')
    case 'ReserveArea': return t('Ta réserve')
    // AJOUT (pack wave) : même clé que `zones.ts` (`emplacement('rising-tide',
    // t('Ta marée montante'), ...)`), même objet (`player.rising_tide`).
    case 'RisingTideArea': return t('Ta marée montante')
    case 'MainSchemesArea': return t('Manigance principale')
    // I2 (revue finale) : MÊME CLÉ que `zones.ts` pour « Mises de côté du
    // scénario » (`t('Mises de côté du scénario')`, groupe de la pile
    // fondue « Cartes visibles ») — c'est la même pile, `world.aside_deck`.
    case 'AsideScenario': return t('Mises de côté du scénario')
    case 'AsideModular': return t('Mises de côté modulaires')
    // Suite de la revue finale (20/09/2026) : mêmes clés que celles déjà
    // posées ailleurs sur le plateau pour le même objet (`zones.ts`,
    // `t('Héros')`/`t('Environnement')`), jamais un second nom.
    case 'HeroArea': return t('Héros')
    case 'ResourcesArea': return t('Ressources')
    case 'ObligationsArea': return t('Obligations')
    case 'EnvironmentArea': return t('Environnement')
    case 'ProcessingArea': return t('En cours de résolution')
    // Lot 2 du 06/10/2026 : un événement posé à la main reste à côté de SON
    // héros (`player.area_processing`), distinct de la résolution du scénario.
    case 'PlayerProcessingArea': return t('À côté de ton héros')
    default: return zone
  }
}

/**
 * Les piles où « sous la pile » a un sens : un deck ORDONNÉ, où le dessous
 * diffère du dessus. Côté moteur (`puzzle.py`, `MoveTo`), `position='Bottom'`
 * n'est traité différemment que si `pile.flags.is_deck` ou
 * `is_dealt_encounter` est vrai (`game/deck/deck_type.py`) : c'est le cas des
 * six zones ci-dessous, et d'aucune autre zone de `ZONES_MANUELLES`. Sur les
 * onze autres (des zones EN JEU, face visible, sans dessus/dessous), `MoveTo`
 * pose la carte normalement quelle que soit la position demandée : le bouton
 * y ferait exactement la même chose que le bouton principal, deux fois le
 * même geste. NE PAS L'AJOUTER AILLEURS sans vérifier ce drapeau côté moteur.
 */
const ZONES_ORDONNEES: ReadonlySet<string> = new Set([
  'PlayerDeck',
  'DiscardPile',
  'EncounterDeck',
  'EncounterDiscardPile',
  // Ronde de correction 1 (19/09/2026) : `AdditionalDeck` et
  // `AdditionalDiscardPile` portent bien `is_deck = True`
  // (`game/deck/deck_type.py`, `DeckTypeFlags.AdditionalDeck`/
  // `AdditionalDiscardPile`) — deux decks ORDONNÉS au même titre que les
  // quatre premiers, oubliés ici quand ils manquaient encore à
  // `ZONES_MANUELLES`. `ReserveArea` et `MainSchemesArea`, eux,
  // `is_deck = False` : volontairement absents.
  'AdditionalDeck',
  'AdditionalDiscardPile',
])

export type MenuTricheProps = {
  cible: CibleTriche
  /** Position du clic, en pixels écran. */
  x: number
  y: number
  onFermer: () => void
  /**
   * Dépose un geste sans écrire sa ligne tout de suite : l'issue réelle
   * (accepté ou refusé par le moteur) n'est connue qu'au rendu suivant.
   * Correction du 19/09/2026 (revue de la tâche 4 ter) : ce menu écrivait
   * directement une ligne « faite » sur le seul succès du DÉPÔT HTTP, qui ne
   * dit rien de l'exécution réelle côté moteur — voir `useTriche` (`CoucheTriche.tsx`).
   */
  emettreGeste: (libelle: string, deposer: () => Promise<boolean>) => Promise<void>
  /**
   * I4 (revue finale, 20/09/2026) : ce même menu s'ouvre en bac à sable ET en
   * mode manuel (`CoucheTriche.tsx`, `leMoteurSeTait`). La marque « Triche »
   * n'a de sens que dans le premier — une partie qui se joue encore aux
   * règles, truquée sciemment ; en manuel, c'est le SEUL moyen de jouer, rien
   * n'est truqué. Absent = bac à sable, pour ne rien changer aux appelants
   * existants (les tests de ce fichier compris).
   */
  manuel?: boolean
  /**
   * Une carte EN MAIN, en mode manuel : « Poser en jeu » la pose selon son
   * type, le même geste que le glisser sur la table et le double-clic (lot 3
   * du 06/10/2026). Absent pour toute autre carte.
   */
  /** Carte en main : pas de compteurs, personne ne les verrait (voir `executerGeste`). */
  enMain?: boolean
  poserEnJeu?: () => void
  /** Une carte EN MAIN : « Échanger avec le dessus du deck » (lot 6, `switchCard` d'OCTGN). */
  echangerAvecLeDessus?: () => void
}

/** Une entrée du menu. `valeur` ouvre une saisie de nombre avant d'agir. */
type Entree = {
  libelle: string
  agir: (valeur: number) => Promise<boolean>
  valeur?: number
  danger?: boolean
}

export function MenuTriche({
  cible,
  x,
  y,
  onFermer,
  emettreGeste,
  manuel = false,
  enMain = false,
  poserEnJeu,
  echangerAvecLeDessus,
}: MenuTricheProps) {
  const [saisie, setSaisie] = useState<Entree | undefined>(undefined)
  const [nombre, setNombre] = useState(1)
  // Le sous-menu « Déplacer vers » : une liste de piles plutôt qu'une saisie
  // de nombre, donc un état à part de `saisie`.
  const [deplacer, setDeplacer] = useState(false)
  const boite = useRef<HTMLDivElement | null>(null)

  // Le menu est placé au curseur, mais ramené dans l'écran s'il déborde : un
  // clic droit près du bord bas ouvrait sinon un menu PARTIELLEMENT INVISIBLE,
  // sans scroll ni moyen d'atteindre le bas (signalé en jeu le 22/09/2026, sur
  // le menu d'un PERSONNAGE — bien plus long qu'une carte ordinaire ; l'ancien
  // calcul devinait une hauteur fixe de 340px, qui ne suffisait qu'aux petits
  // menus). On mesure la VRAIE hauteur RENDUE au lieu de la deviner, et on
  // recalcule à chaque changement de contenu : le sous-menu « Déplacer vers »
  // n'a pas la même hauteur que le menu principal.
  const [position, setPosition] = useState({ left: x, top: y })
  useLayoutEffect(() => {
    const el = boite.current
    if (!el) return
    const { width, height } = el.getBoundingClientRect()
    const marge = 8
    setPosition({
      left: Math.max(marge, Math.min(x, window.innerWidth - width - marge)),
      top: Math.max(marge, Math.min(y, window.innerHeight - height - marge)),
    })
  }, [x, y, deplacer, saisie])
  // Deplacement volontaire, a la poignee -- meme mecanisme que
  // `DemandeCentrale`/`AssistantAction` (demande de l'utilisateur, 28/09/2026,
  // « toutes les fenetres, tous les panneaux »). Signature sur `x|y` : un
  // NOUVEAU clic droit (nouvelle position d'origine) repart de zero, changer
  // de sous-vue (saisie, deplacer) dans le MEME menu garde le glisser.
  const { decalage, gestes: gestesGlisser } = useGlisserPanneau(`${x}|${y}`)

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

  if (!enMain) {
    entrees.push({ libelle: t('Ajouter des compteurs'), valeur: 1,
      agir: (n) => triche.poserCompteur(cible.id, 'counter', n) })
  }
  entrees.push(
    { libelle: t('Défausser'), agir: () => triche.defausser(cible.id), danger: true },
    { libelle: t('Retirer de la partie'), agir: () => triche.retirer(cible.id), danger: true },
  )

  const executer = async (entree: Entree, valeur: number) => {
    const chiffre = entree.valeur !== undefined ? ` ${valeur}` : ''
    await emettreGeste(`${entree.libelle}${chiffre} — ${cible.nom}`, () => entree.agir(valeur))
    onFermer()
  }

  const executerDeplacement = async (zone: string, position: 'Top' | 'Bottom') => {
    const suite = position === 'Bottom' ? ` (${t('Sous la pile')})` : ''
    await emettreGeste(
      `${t('Déplacer vers')} ${libellePile(zone)}${suite} — ${cible.nom}`,
      () => triche.deplacerVers(cible.id, zone, position, cible.siege)
    )
    onFermer()
  }

  return (
    <div
      className="menu-triche"
      style={{ left: position.left + decalage.dx, top: position.top + decalage.dy }}
      ref={boite}
      role="menu"
    >
      <header
        className="menu-triche-titre poignee-glisser"
        onPointerDown={gestesGlisser.onPointerDown}
        onPointerMove={gestesGlisser.onPointerMove}
        onPointerUp={gestesGlisser.onPointerUp}
        onPointerCancel={gestesGlisser.onPointerCancel}
      >
        <span>{cible.nom}</span>
        <span className="menu-triche-marque">{manuel ? t('Geste manuel') : t('Triche')}</span>
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
          {poserEnJeu ? (
            <li>
              <button
                type="button"
                onClick={() => {
                  poserEnJeu()
                  onFermer()
                }}
              >
                {t('Poser en jeu')}
              </button>
            </li>
          ) : null}
          {echangerAvecLeDessus ? (
            <li>
              <button
                type="button"
                onClick={() => {
                  echangerAvecLeDessus()
                  onFermer()
                }}
              >
                {t('Échanger avec le dessus du deck')}
              </button>
            </li>
          ) : null}
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
