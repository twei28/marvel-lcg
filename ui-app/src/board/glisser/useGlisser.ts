/**
 * Le geste : prendre une carte, la promener, la lacher.
 *
 * ⚠ POINTER EVENTS, JAMAIS L'API HTML5 DE GLISSER-DEPOSER. L'ancien plateau
 * (`public/js/marvel/draggable.js`) tenait sur `mousedown` seul, ce qui le
 * rendait inerte au tactile ; l'API HTML5, elle, ne marche pas du tout au
 * doigt et impose son image fantome. Les Pointer Events couvrent les deux avec
 * le meme code, le jour ou le tactile viendra.
 *
 * ⚠ LE CLIC DOIT SURVIVRE INTACT. C'est la condition posee au chantier : le
 * glisser s'ajoute, il ne remplace rien. D'ou le SEUIL : tant que le pointeur
 * n'a pas franchi quelques pixels, il ne se passe RIEN, et le clic part comme
 * avant. Et quand le glisser a bien eu lieu, `onPointerUp` rend `true` pour
 * que l'appelant n'enchaine pas le clic par-dessus.
 */
import { useCallback, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent } from 'react'

/** Distance a franchir avant qu'un appui devienne un glisser, en pixels. */
export const SEUIL_GLISSER = 6

/** Ce qui se trouve sous le pointeur : une carte, une zone du plateau, rien. */
export type CibleSurvolee = { carteId?: number; zone?: string; secteur?: string }

export type EtatGlisser = {
  sourceId: number
  /** Position du pointeur, en coordonnees ecran. */
  x: number
  y: number
  cible: CibleSurvolee
}

type Reglages = {
  /** Cette carte peut-elle etre soulevee ? */
  estSource: (id: number) => boolean
  /** Ce qui se trouve sous ce point de l'ecran. */
  cibleSous: (x: number, y: number) => CibleSurvolee
  /** Appele au lacher, seulement si un glisser a vraiment eu lieu. */
  onDepot: (sourceId: number, cible: CibleSurvolee, point: { x: number; y: number }) => void
}

export function useGlisser({ estSource, cibleSous, onDepot }: Reglages) {
  const [glisse, setGlisse] = useState<EtatGlisser | null>(null)
  const depart = useRef<{
    id: number
    x: number
    y: number
    pointerId: number
    element: HTMLElement
  } | null>(null)
  const commence = useRef(false)

  const oublier = useCallback(() => {
    const debut = depart.current
    if (debut) {
      // La capture peut avoir ete refusee ou deja rendue : on ne bruite pas.
      try {
        debut.element.releasePointerCapture(debut.pointerId)
      } catch {
        /* rien a rendre */
      }
    }
    depart.current = null
    commence.current = false
    setGlisse(null)
  }, [])

  const onPointerDown = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      // Bouton droit et bouton du milieu ne prennent pas de carte.
      if (evenement.pointerType === 'mouse' && evenement.button !== 0) return
      const sous = evenement.target
      if (!(sous instanceof HTMLElement)) return
      // Un bouton posé SUR une carte garde son clic : les piles, les tiroirs.
      if (sous.closest('button, a, input, select, textarea')) return
      const element = sous.closest<HTMLElement>('.scan-card')
      const id = Number(element?.dataset.cardId)
      if (!element || !Number.isFinite(id) || !estSource(id)) return
      depart.current = {
        id,
        x: evenement.clientX,
        y: evenement.clientY,
        pointerId: evenement.pointerId,
        element: evenement.currentTarget,
      }
      commence.current = false
    },
    [estSource]
  )

  const onPointerMove = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      const debut = depart.current
      if (!debut) return
      const dx = evenement.clientX - debut.x
      const dy = evenement.clientY - debut.y
      if (!commence.current) {
        if (Math.hypot(dx, dy) < SEUIL_GLISSER) return
        commence.current = true
        // ⚠ ON EFFACE LA SELECTION DU NAVIGATEUR. Bouton enfonce, le navigateur
        // SELECTIONNE ce qu'il survole, exactement comme sur une page de texte,
        // et peint les images et les mots en bleu. C'est ce bleu-la que
        // l'utilisateur a signale trois fois le 08/09/2026, et il n'avait rien
        // a voir avec les couleurs du plateau : « comme si il selectionnait les
        // images et le texte quand on reste appuye ».
        //
        // Le `user-select: none` pose sur le cadre (glisser.css) empeche les
        // selections SUIVANTES ; celle-ci a pu commencer pendant les six pixels
        // du seuil, avant qu'on sache que c'etait un glisser. On la retire donc
        // ici, une fois, au moment ou le geste est reconnu.
        try {
          window.getSelection()?.removeAllRanges()
        } catch {
          /* pas de selection a effacer */
        }
        // La capture garde le geste vivant quand le pointeur sort du cadre :
        // sans elle, sortir du plateau relachait la carte en silence.
        try {
          debut.element.setPointerCapture(debut.pointerId)
        } catch {
          /* le navigateur refuse : on suit le pointeur sans capture */
        }
      }
      setGlisse({
        sourceId: debut.id,
        x: evenement.clientX,
        y: evenement.clientY,
        cible: cibleSous(evenement.clientX, evenement.clientY),
      })
    },
    [cibleSous]
  )

  /** Rend `true` si un glisser s'achevait : l'appelant n'enchaine pas le clic. */
  const onPointerUp = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>): boolean => {
      const debut = depart.current
      const aGlisse = commence.current
      const cible = aGlisse ? cibleSous(evenement.clientX, evenement.clientY) : undefined
      const source = debut?.id
      const point = { x: evenement.clientX, y: evenement.clientY }
      oublier()
      if (!aGlisse || source === undefined || !cible) return false
      onDepot(source, cible, point)
      return true
    },
    [cibleSous, oublier, onDepot]
  )

  return {
    glisse,
    gestes: { onPointerDown, onPointerMove, onPointerUp, onPointerCancel: oublier },
  }
}

/**
 * Ce qui se trouve sous un point de l'ecran : la carte d'abord, sa zone sinon.
 *
 * ⚠ `elementFromPoint` ET NON UN CALCUL DE RECTANGLES : le navigateur connait
 * deja l'empilement, les chevauchements de cartes et l'echelle de la scene.
 * La couche visuelle interne d'une carte (`.scan-visuel`) est en
 * `pointer-events: none`, donc c'est bien `.scan-card` qui est touchee, a sa
 * taille normale et non a son agrandissement au survol.
 */
export function cibleSousLePoint(x: number, y: number): CibleSurvolee {
  const sous = document.elementFromPoint(x, y)
  if (!(sous instanceof HTMLElement)) return {}
  const carte = sous.closest<HTMLElement>('.scan-card')
  const id = Number(carte?.dataset.cardId)
  const carteId = carte && Number.isFinite(id) ? id : undefined
  // ⚠ DEUX FAMILLES DE `data-pile`, DEUX CHAMPS DISTINCTS (tache 5, mode
  // manuel — corrige la ronde de correction 2, constat C1) :
  //  - une PILE, posee sur SA PROPRE unite (`.plateau-unite`, un deck, une
  //    defausse...) : elle ne compte QUE si on touche vraiment SA carte, et
  //    rejoint `zone` comme avant. Sinon la marge de son unite retomberait
  //    sur cette pile precise. `carte?.closest` et non `sous.closest` :
  //    l'unite qui compte est celle de la CARTE trouvee, pas celle, plus
  //    proche du point, d'une unite VOISINE sans rapport.
  //  - un SECTEUR, pose sur le GROUPE entier (`.plateau-groupe`, ex.
  //    « ennemis engages ») : il compte MEME hors carte (le mode manuel en a
  //    besoin pour engager un sbire lache dans l'espace vide du secteur),
  //    mais NE DOIT JAMAIS ecraser `zone`. `terrain-combat-engages` se
  //    dessine dans TOUTES les parties, y compris ordinaires ; le mode
  //    ORDINAIRE ne connait que l'emplacement LARGE (`board.tsx` batit ses
  //    zones sur `emplacement.cle`, jamais sur une pile ou un secteur fins),
  //    et un lacher sans carte au milieu du secteur (les quelques pixels
  //    entre deux sbires engages) rendait `terrain-combat-engages` au lieu
  //    de `terrain-combat` : la carte s'y voyait refusee a tort. Le secteur
  //    vit donc dans son PROPRE champ, que seul le mode manuel lit.
  // ⚠ UNE PILE VIDE N'A PAS DE CARTE (22/09/2026, correctif du geste manuel
  // sur les piles vides). `Board.tsx` la dessine comme un `.plateau-unite`
  // SANS `.scan-card` dedans (un simple encadré en pointillés) : `carte`
  // vaut alors `undefined`, et la ligne du dessus ne trouverait donc jamais
  // sa pile — un lâcher dessus retombait sur `[data-zone]`, la zone LARGE
  // (« piles-joueur »), absente de `PILE_PAR_ZONE`, et le dépôt était
  // refusé (« Lâche la carte sur une pile », sur la pile elle-même). Sans
  // carte, l'ambiguïté de marge que `carte?.closest` évite plus haut ne se
  // pose pas : l'encadré EST la pile, ses bords en sont la frontière.
  const uniteVide = !carte ? sous.closest<HTMLElement>('.plateau-unite.pile-vide') : null
  const pile = carte?.closest<HTMLElement>('.plateau-unite')?.dataset.pile || uniteVide?.dataset.pile
  const secteur = sous.closest<HTMLElement>('.plateau-groupe')?.dataset.pile
  const zone = pile || sous.closest<HTMLElement>('[data-zone]')?.dataset.zone
  return {
    carteId,
    zone: zone || undefined,
    secteur: secteur || undefined,
  }
}
