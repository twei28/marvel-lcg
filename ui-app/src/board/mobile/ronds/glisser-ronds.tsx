// LE GLISSER AU DOIGT sur le plateau en ronds (decisions 78 a 82, 24/10/2026).
//
// On ne reecrit PAS les regles : le plateau PC les a deja (`ReglagesGlisser`, board.tsx : quelles cartes se soulevent, ce
// qu'elles visent, ce que le lacher declenche : heros sur mechant = attaquer, plusieurs actions = le menu de ciblage...).
// Ce module n'apporte que le GESTE, adapte aux ronds et a la main :
//   - un rond (heros, allie, soutien pret...) : des que le doigt bouge de quelques pixels, il se leve et suit le doigt ;
//   - une carte de la main : glisser vers le HAUT la leve ; de cote, la main defile (touch-action: pan-x) ;
//   - pendant le geste, les cibles legales s'allument en jaune, les autres s'assombrissent ;
//   - au lacher, `glisser.onDepot` decide. Une raison de refus (lacher a vide, mauvaise cible) est dite en bulle et la
//     carte retourne la ou elle etait (rien n'est joue).
// Un toucher simple n'est pas touche : le clic qui suit un glisser est avale, jamais l'inverse.
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type CSSProperties, type PointerEvent as ReactPointerEvent, type ReactElement } from 'react'
import type { ReglagesGlisser } from '../../Board'
import { BulleRefus } from '../../glisser/CoucheGlisser'
import type { CibleSurvolee } from '../../glisser/useGlisser'

/** Distance (px) avant qu'un appui sur un rond devienne un glisser. */
export const SEUIL_ROND = 8
/** Pour la main : montee minimale (px), et plus verticale qu'horizontale. */
export const SEUIL_MAIN = 18

/** Les zones du plateau PC que visent les zones des ronds (cles d'emplacement de `zones.ts`). */
const EMPLACEMENT_DE_ZONE: Record<string, string> = {
  vilain: 'rencontre',
  manigances: 'complot-principal',
  allies: 'terrain-combat',
  sbires: 'terrain-combat',
  heros: 'terrain-soutien',
  enJeu: 'terrain-soutien',
}

export type GlisseRond = {
  sourceId: number
  x: number
  y: number
  fond: string
  /** Cadrage du rond d'origine (taille et position du fond), pour que le fantome montre le meme dessin. */
  cadrage?: { taille: string; position: string }
  libelle?: string
  refuse: boolean
}

type Contexte = { glisse: GlisseRond | null; cibles: Set<number>; estSource: (id: number) => boolean; clicAvale: () => boolean }
export const ContexteGlisse = createContext<Contexte>({ glisse: null, cibles: new Set(), estSource: () => false, clicAvale: () => false })

/** Un rond lit ici s'il est une cible allumee, ou s'il doit s'assombrir. */
/** Ce que le glisser en cours dit de ce rond, et si on peut le glisser. */
export function useEtatGlisse(id: number): { etat: 'cible' | 'assombri' | 'source' | undefined; glissable: boolean; clicAvale: () => boolean } {
  const { glisse, cibles, estSource, clicAvale } = useContext(ContexteGlisse)
  const glissable = estSource(id)
  const etat = etatDe(id, glisse, cibles)
  return { etat, glissable, clicAvale }
}

function etatDe(id: number, glisse: GlisseRond | null, cibles: Set<number>): 'cible' | 'assombri' | 'source' | undefined {
  if (!glisse) return undefined
  if (glisse.sourceId === id) return 'source'
  return cibles.has(id) ? 'cible' : 'assombri'
}

export function cibleSousLeRond(x: number, y: number): CibleSurvolee {
  const sous = document.elementFromPoint(x, y)
  // Element, pas HTMLElement : l'anneau d'un rond est un SVG, et c'est lui qui est touche.
  if (!(sous instanceof Element)) return {}
  const rond = sous.closest<HTMLElement>('.rond[data-card-id]')
  const id = Number(rond?.dataset.cardId)
  const zone = sous.closest<HTMLElement>('.ronds-zone')?.dataset.zone
  return {
    carteId: rond && Number.isFinite(id) ? id : undefined,
    zone: zone ? EMPLACEMENT_DE_ZONE[zone] : undefined,
  }
}

function fondDe(element: HTMLElement): { fond: string; cadrage?: { taille: string; position: string } } {
  const art = element.querySelector<HTMLElement>('.rond-art')
  if (art) {
    const image = art.querySelector('img')
    if (image) return { fond: `url(${image.src})`, cadrage: { taille: '230%', position: '88% 55%' } }
    const style = getComputedStyle(art)
    return { fond: style.backgroundImage, cadrage: { taille: style.backgroundSize, position: style.backgroundPosition } }
  }
  // Une carte de la main : son illustration, cadree en haut comme un rond.
  const image = element.querySelector('img')
  // Le fantome est un jeton : l'illustration anglaise, sans filigrane (comme les ronds).
  const sansFiligrane = image ? image.src.replace(/(\/(?:scan|vignette)\/)fr_/, '$1') : ''
  return { fond: image ? `url(${sansFiligrane})` : 'none', cadrage: { taille: '190% auto', position: '48% 24%' } }
}

/**
 * Le geste. `racine` est l'element qui recoit les evenements (la table et la main) ; chaque source est un descendant
 * portant `data-card-id` (un `.rond`, ou la carte d'une `.main-portrait-carte`).
 */
export function useGlisserAuDoigt(glisser: ReglagesGlisser | undefined) {
  const actif = glisser !== undefined && glisser.auDoigt !== true
  const [glisse, setGlisse] = useState<GlisseRond | null>(null)
  const [refus, setRefus] = useState<{ x: number; y: number; texte: string } | null>(null)
  const depart = useRef<{ id: number; x: number; y: number; deLaMain: boolean; pointerId: number; racine: HTMLElement; fond: string; cadrage?: { taille: string; position: string } } | null>(null)
  const commence = useRef(false)
  const avaleClic = useRef(false)
  const minuteurRefus = useRef<number | undefined>(undefined)
  const cibles = useMemo(() => (glisse && glisser ? glisser.ciblesLegales(glisse.sourceId) : new Set<number>()), [glisse?.sourceId, glisser]) // eslint-disable-line react-hooks/exhaustive-deps

  const oublier = useCallback(() => {
    const debut = depart.current
    if (debut) {
      try {
        debut.racine.releasePointerCapture(debut.pointerId)
      } catch {
        /* rien a rendre */
      }
    }
    depart.current = null
    commence.current = false
    setGlisse(null)
  }, [])
  useEffect(() => () => window.clearTimeout(minuteurRefus.current), [])

  const surAppui = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      if (!actif || !glisser) return
      if (evenement.pointerType === 'mouse' && evenement.button !== 0) return
      const sous = evenement.target
      if (!(sous instanceof Element)) return
      const source = sous.closest<HTMLElement>('[data-card-id]')
      const id = Number(source?.dataset.cardId)
      if (!source || !Number.isFinite(id) || !glisser.estSource(id)) return
      depart.current = {
        id,
        x: evenement.clientX,
        y: evenement.clientY,
        deLaMain: source.closest('.main-dock') !== null,
        pointerId: evenement.pointerId,
        racine: evenement.currentTarget,
        ...fondDe(source),
      }
      commence.current = false
    },
    [actif, glisser]
  )

  const surMouvement = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      const debut = depart.current
      if (!debut || !glisser) return
      const dx = evenement.clientX - debut.x
      const dy = evenement.clientY - debut.y
      if (!commence.current) {
        // Une carte de la main : vers le haut seulement (de cote, la main defile) ; un rond : n'importe quelle direction.
        const assez = debut.deLaMain ? -dy >= SEUIL_MAIN && -dy > Math.abs(dx) * 1.2 : Math.hypot(dx, dy) >= SEUIL_ROND
        if (!assez) return
        commence.current = true
        try {
          window.getSelection()?.removeAllRanges()
          debut.racine.setPointerCapture(debut.pointerId)
        } catch {
          /* pas de capture : on suit quand meme le pointeur */
        }
      }
      const cible = cibleSousLeRond(evenement.clientX, evenement.clientY)
      setGlisse({
        sourceId: debut.id,
        x: evenement.clientX,
        y: evenement.clientY,
        fond: debut.fond,
        cadrage: debut.cadrage,
        libelle: glisser.libelle(debut.id, cible),
        refuse: cible.carteId !== undefined && !glisser.ciblesLegales(debut.id).has(cible.carteId),
      })
    },
    [glisser]
  )

  const surRelache = useCallback(
    (evenement: ReactPointerEvent<HTMLElement>) => {
      const debut = depart.current
      const aGlisse = commence.current
      oublier()
      if (!aGlisse || !debut || !glisser) return
      // Le clic que le navigateur envoie apres le relachement ne doit pas ouvrir la feuille de la carte.
      avaleClic.current = true
      window.setTimeout(() => {
        avaleClic.current = false
      }, 350)
      const raison = glisser.onDepot(debut.id, cibleSousLeRond(evenement.clientX, evenement.clientY))
      window.clearTimeout(minuteurRefus.current)
      if (!raison) {
        setRefus(null)
        return
      }
      setRefus({ x: evenement.clientX, y: evenement.clientY, texte: raison })
      minuteurRefus.current = window.setTimeout(() => setRefus(null), 2600)
    },
    [glisser, oublier]
  )

  /** A poser sur le onClick des ronds : vrai si le clic suit un glisser et doit etre avale. */
  const clicAvale = useCallback(() => avaleClic.current, [])

  return {
    actif,
    glisse,
    cibles,
    refus,
    clicAvale,
    gestes: { onPointerDown: surAppui, onPointerMove: surMouvement, onPointerUp: surRelache, onPointerCancel: oublier },
    valeur: { glisse, cibles, estSource: (id: number) => actif && glisser !== undefined && glisser.estSource(id), clicAvale } as Contexte,
  }
}

/** Le rond fantome qui suit le doigt, son etiquette, et la bulle d'un refus. Ne capte jamais le pointeur. */
export function CoucheGlisseRonds({ glisse, refus }: { glisse: GlisseRond | null; refus: { x: number; y: number; texte: string } | null }): ReactElement {
  return (
    <>
      {glisse ? (
        <div className="glisse-rond-couche" aria-hidden="true">
          <span
            className={`glisse-rond-fantome${glisse.refuse ? ' est-refuse' : ''}`}
            style={
              {
                left: glisse.x,
                top: glisse.y,
                backgroundImage: glisse.fond,
                backgroundSize: glisse.cadrage?.taille,
                backgroundPosition: glisse.cadrage?.position,
              } as CSSProperties
            }
          />
          {glisse.libelle ? (
            <span className={`glisse-rond-libelle${glisse.refuse ? ' est-refuse' : ''}`} style={{ left: Math.min(Math.max(glisse.x, 96), (typeof window === 'undefined' ? 390 : window.innerWidth) - 96), top: Math.max(glisse.y - 56, 8) }}>
              {glisse.libelle}
            </span>
          ) : null}
        </div>
      ) : null}
      {refus ? <BulleRefus x={refus.x} y={refus.y} texte={refus.texte} /> : null}
    </>
  )
}
