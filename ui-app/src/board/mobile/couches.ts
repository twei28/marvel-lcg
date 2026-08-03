// Les couches ouvertes par-dessus la vue d'etat, de la plus ancienne a la plus
// recente. Le retour d'Android ferme la couche du SOMMET, une a la fois : c'est
// pour cela qu'on tient une pile et pas un booleen par couche.
//
// La partie pure est ici et testee ; le hook ci-dessous la relie a l'historique
// du navigateur.

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import type { CleBande } from './bandes'

export type Couche =
  | { sorte: 'focus'; bande: CleBande }
  | { sorte: 'carte'; id: string }
  | { sorte: 'selecteur' }

function memeCouche(a: Couche, b: Couche): boolean {
  return cleCouche(a) === cleCouche(b)
}

/** Identite d'une couche, en une chaine : deux couches de meme cle sont la meme. */
export function cleCouche(couche: Couche): string {
  if (couche.sorte === 'focus') return `focus:${couche.bande}`
  if (couche.sorte === 'carte') return `carte:${couche.id}`
  return 'selecteur'
}

/**
 * Les couches que board.tsx dessine lui-meme (le menu d'actions d'une carte et
 * le selecteur de cibles hors table), par opposition a la feuille de focus qui
 * appartient a l'arbre mobile. Il n'y en a JAMAIS deux a la fois : le menu se
 * cache des qu'une option est en cours de ciblage, et c'est justement le
 * selecteur qui prend sa place.
 */
function estExterne(couche: Couche): boolean {
  return couche.sorte === 'carte' || couche.sorte === 'selecteur'
}

export function sommet(pile: Couche[]): Couche | undefined {
  return pile[pile.length - 1]
}

/** Empiler la couche deja au sommet ne fait rien : un double tap ne cree pas deux feuilles. */
export function empiler(pile: Couche[], couche: Couche): Couche[] {
  const haut = sommet(pile)
  if (haut && memeCouche(haut, couche)) return pile
  return [...pile, couche]
}

export function depiler(pile: Couche[]): Couche[] {
  return pile.slice(0, -1)
}

/**
 * Echange la couche du sommet contre une autre, SANS toucher a l'historique :
 * la profondeur ne bouge pas, donc l'entree deja poussee reste la bonne. C'est
 * ce qu'il faut quand une couche laisse la place a une autre sans que les deux
 * soient visibles ensemble (le menu d'une carte -> le selecteur de cibles) :
 * empiler donnerait deux entrees pour une seule feuille a l'ecran, et il
 * faudrait deux Retour pour la fermer.
 */
export function remplacerSommet(pile: Couche[], couche: Couche): Couche[] {
  const haut = sommet(pile)
  if (!haut || memeCouche(haut, couche)) return pile
  return [...pile.slice(0, -1), couche]
}

/**
 * Relie la pile a l'historique du navigateur : une entree par couche ouverte,
 * pour que le bouton retour d'Android ferme la feuille du dessus au lieu de
 * quitter la partie.
 *
 * Les effets de bord sur history NE VIVENT PAS dans les fonctions passees a
 * setPile. En StrictMode (developpement), React invoque deux fois la fonction
 * d'un setState fonctionnel pour verifier sa purete ; un pushState() loge la
 * dedans partirait donc deux fois pour une seule ouverture, et la pile se
 * desynchroniserait de l'historique (le mal que cette pile existe pour
 * eviter). On lit donc l'etat courant depuis le closure du gestionnaire
 * d'evenement (rendu a chaque changement de pile), on calcule la pile
 * suivante avec les fonctions pures ci-dessus, on effectue l'effet de bord
 * une seule fois, puis on pose la valeur deja calculee dans setPile.
 */
export function useCouches(): {
  pile: Couche[]
  ouvrir: (couche: Couche) => void
  remplacer: (couche: Couche) => void
  fermer: () => void
  toutFermer: () => void
} {
  const [pile, setPile] = useState<Couche[]>([])

  // Limite connue : ouvrir lit "pile" depuis la fermeture de useCallback. Deux
  // appels synchrones dans le meme tick (avant le prochain rendu) liraient
  // tous les deux la meme valeur pre-mise-a-jour, et le second calculerait son
  // pushState contre un etat perime. Aucun appelant actuel ne fait deux
  // ouvertures dans le meme tick ; qui branche ce hook (taches 7 et 8) doit
  // garder un seul appel par interaction utilisateur.
  const ouvrir = useCallback(
    (couche: Couche) => {
      const suivante = empiler(pile, couche)
      if (suivante === pile) return
      window.history.pushState({ couche: suivante.length }, '')
      setPile(suivante)
    },
    [pile]
  )

  // Aucun effet de bord sur l'historique ici, et c'est voulu : la profondeur
  // de la pile ne change pas, l'entree deja poussee vaut pour la nouvelle
  // couche comme elle valait pour l'ancienne.
  const remplacer = useCallback(
    (couche: Couche) => {
      const suivante = remplacerSommet(pile, couche)
      if (suivante === pile) return
      setPile(suivante)
    },
    [pile]
  )

  // Fermer se fait TOUJOURS par history.back() : le gestionnaire de popstate
  // ci-dessous est alors le seul endroit qui retire une couche, et la pile ne
  // peut pas se desynchroniser de l'historique.
  const fermer = useCallback(() => {
    window.history.back()
  }, [])

  // toutFermer vide la pile TOUT DE SUITE, en synchrone, plutot que d'attendre
  // les popstate qui suivront le history.go(-n). Un saut de n crans ne
  // declenche pas forcement n evenements popstate (souvent un seul, coalesce
  // par le navigateur) : si on comptait dessus pour depiler un cran a la
  // fois, la pile resterait a moitie pleine. depiler sur une pile deja vide
  // est un no-op, donc un popstate tardif et isole reste sans danger.
  const toutFermer = useCallback(() => {
    if (pile.length === 0) return
    window.history.go(-pile.length)
    setPile([])
  }, [pile])

  useEffect(() => {
    const surRetour = () => setPile((precedente) => depiler(precedente))
    window.addEventListener('popstate', surRetour)
    return () => window.removeEventListener('popstate', surRetour)
  }, [])

  return { pile, ouvrir, remplacer, fermer, toutFermer }
}

export type Couches = ReturnType<typeof useCouches>

/**
 * Relie a la pile les couches que board.tsx dessine LUI-MEME : le menu
 * d'actions d'une carte, et le selecteur de cibles hors table.
 *
 * Ces deux panneaux n'appartiennent pas a l'arbre mobile ; ils naissent de
 * l'etat d'interaction de board.tsx. Sans ce pont, seule la feuille de focus
 * etait empilee, et le Retour d'Android sur un menu de carte ou en plein
 * ciblage sortait de la partie, c'est-a-dire exactement ce que cette pile
 * existe pour empecher (spec S6 : « les couches empilees (focus, menu
 * d'actions, selecteur) sont gerees par history.pushState, une entree par
 * couche »).
 *
 * UN SEUL pont pour les deux, et non un hook par panneau : ils se relaient
 * (choisir une capacite a cibles ferme le menu et ouvre le selecteur dans le
 * MEME rendu). Deux ponts independants auraient fait un history.back() et un
 * pushState dans le meme tick, or back() est asynchrone : la pile et
 * l'historique se seraient croises et le popstate suivant aurait ferme la
 * mauvaise couche. Ici la transition menu -> selecteur est un REMPLACEMENT sur
 * place : une seule couche est visible, donc une seule entree d'historique.
 * Le Retour abandonne alors le ciblage, board.tsx redonne le menu, qui pousse
 * sa propre entree : le compte reste juste a chaque etape.
 *
 * Le pont marche dans les deux sens :
 *  - un panneau s'ouvre -> on empile ;
 *  - le Retour retire la couche -> on demande a board.tsx de le fermer ;
 *  - board.tsx le ferme autrement (bouton Fermer, action jouee) -> on depile,
 *    pour que l'historique reste aligne sur ce qui est affiche.
 *
 * `dejaOuverte` retient l'identifiant deja empile : sans lui, une seconde
 * invocation de l'effet avec la meme pile (StrictMode, ou deux rendus avant
 * que setPile ne soit applique) pousserait deux entrees d'historique pour une
 * seule ouverture, et il faudrait deux Retour pour fermer un seul menu.
 */
export function useCouchesBoard(
  carteFocalisee: number | undefined,
  selecteurOuvert: boolean,
  couches: Couches,
  onFermerCarte?: () => void,
  onFermerSelecteur?: () => void
): void {
  const { pile, ouvrir, remplacer, fermer } = couches

  // Ce que board.tsx affiche en ce moment. Le selecteur passe devant : quand
  // il est la, board.tsx a deja cache le menu. useMemo pour que l'objet garde
  // son identite d'un rendu a l'autre, sinon l'effet repartirait a chaque fois.
  const coucheVoulue = useMemo<Couche | undefined>(() => {
    if (selecteurOuvert) return { sorte: 'selecteur' }
    if (carteFocalisee === undefined) return undefined
    return { sorte: 'carte', id: String(carteFocalisee) }
  }, [selecteurOuvert, carteFocalisee])
  const cleVoulue = coucheVoulue ? cleCouche(coucheVoulue) : undefined

  const externe = pile.filter(estExterne)
  const cleEmpilee = externe.length > 0 ? cleCouche(externe[externe.length - 1]) : undefined
  const auSommet = externe.length > 0 && externe[externe.length - 1] === sommet(pile)
  const etaitEmpilee = useRef<string | undefined>(undefined)
  const dejaOuverte = useRef<string | undefined>(undefined)

  useEffect(() => {
    const avant = etaitEmpilee.current
    etaitEmpilee.current = cleEmpilee

    if (coucheVoulue === undefined || cleVoulue === undefined) {
      dejaOuverte.current = undefined
      if (cleEmpilee !== undefined) fermer()
      return
    }

    if (cleEmpilee === undefined) {
      // La couche vient de disparaitre alors que le panneau est encore
      // ouvert : c'est le Retour d'Android. C'est lui qui ferme, pas nous.
      if (avant !== undefined) {
        dejaOuverte.current = undefined
        if (avant === 'selecteur') onFermerSelecteur?.()
        else onFermerCarte?.()
        return
      }

      if (dejaOuverte.current === cleVoulue) return
      dejaOuverte.current = cleVoulue
      ouvrir(coucheVoulue)
      return
    }

    // Une couche externe est empilee, mais ce n'est plus celle qui est a
    // l'ecran : un panneau a laisse la place a l'autre. On echange en place.
    // Si elle n'est pas au sommet (cas qui ne se produit pas : ces panneaux
    // couvrent l'ecran, on ne peut pas ouvrir une feuille de focus par-dessus),
    // on ne touche a rien : une couche mal nommee vaut mieux qu'un historique
    // desynchronise.
    if (cleEmpilee !== cleVoulue && auSommet) {
      dejaOuverte.current = cleVoulue
      remplacer(coucheVoulue)
    }
  }, [
    coucheVoulue,
    cleVoulue,
    cleEmpilee,
    auSommet,
    ouvrir,
    remplacer,
    fermer,
    onFermerCarte,
    onFermerSelecteur,
  ])
}

/** Le pont ci-dessus quand seul le menu d'actions existe (aucun selecteur). */
export function useCoucheCarte(
  carteFocalisee: number | undefined,
  couches: Couches,
  onFermerCarte?: () => void
): void {
  useCouchesBoard(carteFocalisee, false, couches, onFermerCarte)
}
