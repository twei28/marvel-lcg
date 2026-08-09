// Le hook qui pose un panneau flottant sans recouvrir ce dont il parle.
//
// Il ne fait que relier les deux moitiés : boites.ts mesure l'écran, placer.ts
// décide. Ici, le quand et le comment de l'application.
//
// DEUX RÈGLES qui comptent plus que le calcul lui-même :
//
// 1. On mesure en `useLayoutEffect`, donc AVANT peinture : le panneau n'est
//    jamais vu à sa position par défaut avant de sauter à la bonne.
// 2. Le placement est FIGÉ tant que la signature ne change pas. Un panneau qui
//    se replacerait à chaque rendu du monde — donc au moindre survol, à la
//    moindre animation — serait plus pénible que celui qui cache une carte.
import { useLayoutEffect, useMemo, useState, type CSSProperties, type RefObject } from 'react'
import { boitesDesCartes, boitesDesPanneaux } from './boites'
import { MARGE_PAR_DEFAUT, placer, type Ancre, type Placement } from './placer'

// L'ordre de pose. Un panneau contourne tous ceux des groupes qui le précèdent,
// jamais l'inverse : c'est ce qui évite d'avoir à orchestrer l'ordre de montage
// des composants.
//
//   1. le panneau décisionnel (un seul à la fois)  -> évite les cartes
//   2. l'assistant pas-à-pas                       -> + évite le décisionnel
//   3. l'événement central                         -> + évite l'assistant
//
// L'aperçu au survol, lui, N'ESQUIVE RIEN : il est fixé à droite, une seule
// position candidate. Essayé dans l'autre sens, et c'était pénible — un
// agrandissement s'ouvre à chaque passage de souris, et le voir changer de coin
// selon ce qui est libre oblige l'œil à le rechercher chaque fois. Esquiver est
// bon pour une décision, rare et bloquante ; mauvais pour un geste réflexe.
// Voir CarteApercu dans Board.tsx.

/** Le panneau qui porte la décision en cours. */
export const PANNEAUX_DECISION = [
  '.demande-centrale',
  '.menu-actions-carte',
  '.actions-flottantes',
]

/** Tout ce qui porte une décision ou une consigne : l'aperçu leur cède la place. */
export const PANNEAUX_PRIORITAIRES = [
  ...PANNEAUX_DECISION,
  '.assistant-action',
  '.evenement-centrale',
]

export type OptionsPlacement = {
  /** Identifiants des cartes que ce panneau ne doit pas recouvrir. */
  cartes?: readonly number[]
  /** Sélecteurs des panneaux déjà posés à contourner. */
  panneaux?: readonly string[]
  /**
   * Ce qui justifie de recalculer. Doit changer quand la DÉCISION change, pas
   * quand le monde se redessine — c'est toute la différence entre un panneau
   * stable et un panneau qui gigote.
   */
  signature: string
  /** Position de repli et référence de distance. Défaut : le centre. */
  preferee?: Ancre
  /**
   * Positions autorisées. Une seule = le panneau ne bouge JAMAIS, et c'est un
   * réglage utile : ce qui s'ouvre à chaque survol doit rester où l'œil
   * l'attend, même au prix d'un recouvrement. Voir CarteApercu.
   */
  candidats?: readonly Ancre[]
  /**
   * Sélecteurs dont le bord GAUCHE borne le panneau à droite : il restera
   * entièrement à leur gauche. Sert à tenir l'aperçu d'une carte seule hors de
   * la colonne de droite de la table, qu'il n'a pas besoin de recouvrir.
   * Aucun élément trouvé = aucune borne, on ne devine pas une géométrie absente.
   */
  borneDroite?: readonly string[]
  /** Faux = on laisse la position du CSS (panneau masqué ou non concerné). */
  actif?: boolean
}

export type ResultatPlacement = {
  /** À poser sur le panneau. Vide tant que la première mesure n'a pas eu lieu. */
  style: CSSProperties
  /** Le panneau recouvre encore quelque chose : à alléger visuellement. */
  genant: boolean
}

const VIDE: ResultatPlacement = { style: {}, genant: false }

export function usePlacement(
  ref: RefObject<HTMLElement | null>,
  options: OptionsPlacement
): ResultatPlacement {
  const [place, setPlace] = useState<(Placement & { w: number; h: number }) | undefined>(undefined)

  const { signature, preferee, actif = true } = options
  const clesCandidats = (options.candidats ?? []).join(',')
  const clesBorne = (options.borneDroite ?? []).join(',')

  // Les identifiants sont triés puis joints : deux rendus qui désignent les
  // mêmes cartes dans un ordre différent ne doivent pas passer pour un
  // changement.
  const clesCartes = useMemo(
    () => [...new Set(options.cartes ?? [])].sort((a, b) => a - b).join(','),
    [options.cartes]
  )
  const clesPanneaux = useMemo(() => (options.panneaux ?? []).join(','), [options.panneaux])

  useLayoutEffect(() => {
    if (!actif) {
      setPlace(undefined)
      return
    }
    const element = ref.current
    if (!element) return

    const mesurer = () => {
      const taille = { w: element.offsetWidth, h: element.offsetHeight }
      // Un panneau pas encore dimensionné (police en cours de chargement, image
      // sans hauteur) donnerait un placement faux : on attend le rendu suivant.
      if (taille.w === 0 || taille.h === 0) return

      const cartes = clesCartes ? clesCartes.split(',').map(Number) : []
      const aEviter = [
        ...boitesDesCartes(cartes),
        ...boitesDesPanneaux(clesPanneaux ? clesPanneaux.split(',') : [], element),
      ]

      // Bord gauche le plus à gauche parmi les éléments visés : le panneau
      // restera entièrement à sa gauche, avec le même écart que la marge.
      let borneDroite: number | undefined
      for (const selecteur of clesBorne ? clesBorne.split(',') : []) {
        for (const el of document.querySelectorAll(selecteur)) {
          const r = el.getBoundingClientRect()
          if (r.width > 0) borneDroite = Math.min(borneDroite ?? Infinity, r.left - MARGE_PAR_DEFAUT)
        }
      }

      const suivant = {
        ...placer({
          taille,
          aEviter,
          viewport: { w: window.innerWidth, h: window.innerHeight },
          preferee,
          candidats: clesCandidats ? (clesCandidats.split(',') as Ancre[]) : undefined,
          borneDroite,
        }),
        ...taille,
      }
      // On ne réécrit l'état que si la position change VRAIMENT. Sans cette
      // garde, le ResizeObserver et le rendu qu'il provoque s'entretiendraient
      // l'un l'autre — et un panneau qui se redessine en boucle coûte plus cher
      // que celui qu'on est venu réparer.
      setPlace((ancien) =>
        ancien &&
        ancien.x === suivant.x &&
        ancien.y === suivant.y &&
        ancien.w === suivant.w &&
        ancien.h === suivant.h &&
        ancien.genant === suivant.genant
          ? ancien
          : suivant
      )
    }

    mesurer()
    window.addEventListener('resize', mesurer)

    // Le panneau grandit APRÈS le premier rendu : les scans de cartes n'ont pas
    // encore leur hauteur, une police peut finir de charger. Mesuré sur
    // l'aperçu d'une carte recto-verso : 897 px au montage, 934 px une fois les
    // images arrivées — placé sur l'ancienne largeur, il sortait de l'écran.
    // On observe donc sa taille réelle plutôt que de croire la première mesure.
    const observateur = new ResizeObserver(mesurer)
    observateur.observe(element)

    return () => {
      window.removeEventListener('resize', mesurer)
      observateur.disconnect()
    }
  }, [ref, actif, signature, clesCartes, clesPanneaux, clesCandidats, clesBorne, preferee])

  return useMemo(() => {
    if (!place) return VIDE
    // On rend le CENTRE du panneau, pas son coin : les règles CSS gardent leur
    // `transform: translate(-50%, -50%)`, et c'est indispensable — l'animation
    // d'apparition de `.evenement-centrale` anime justement le transform. Le
    // JavaScript n'y touche jamais.
    return {
      style: {
        left: `${Math.round(place.x + place.w / 2)}px`,
        top: `${Math.round(place.y + place.h / 2)}px`,
        right: 'auto',
        bottom: 'auto',
      },
      genant: place.genant,
    }
  }, [place])
}

/** Les cartes concernées par une option : celle qui agit et ses cibles légales. */
export function cartesDeLOption(option: {
  bind_id: number
  all_legal_targets: readonly number[]
}): number[] {
  return [option.bind_id, ...option.all_legal_targets]
}
