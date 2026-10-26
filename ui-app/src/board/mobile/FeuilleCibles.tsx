// LA FEUILLE DE CHOIX DE CIBLE, au telephone (maquette approuvee par l'utilisateur, 26/10/2026).
//
// Avant : une boite pleine largeur qui couvrait le plateau, sans AUCUNE cible dedans (le joueur devait viser les ronds derriere), avec une
// poignee « ⋮ » inerte. Maintenant :
//  - elle se GLISSE au doigt par la poignee ET le titre, et se cale sur trois positions : reduite (poignee, titre, compteur), basse
//    (tout, boutons compris) et haute (la rangee passe a la ligne : toutes les cibles d'un coup d'oeil) ;
//  - elle montre les cibles possibles DEDANS : les memes ronds que sur la table (`Rond`), avec leurs PV, leurs statuts et leurs ATQ / MNG ;
//    un toucher choisit, un deuxieme retire ; la cible choisie s'allume aussi sur la table derriere (meme etat d'interaction) ;
//  - sa position est gardee tant que la question dure, oubliee a la suivante.
//
// ⚠ LE GESTE EST SUIVI SUR LA FENETRE, PAS SEULEMENT SUR LA POIGNEE (meme lecon que `useGlisserPanneau`, 01/10/2026) : une poignee
// mince est quittee par le doigt avant le seuil, et la feuille ne bougerait plus.
import { useCallback, useEffect, useLayoutEffect, useRef, useState, type KeyboardEvent as ReactKeyboardEvent, type PointerEvent as ReactPointerEvent } from 'react'
import { t } from '../langue'
import type { UniteAffichee } from '../zones'
import { borner, caler, positionsFeuille, type PositionFeuille, type PositionsFeuille } from './calage-feuille'
import { Rond, type DecorRonds } from './ronds/Rond'
import type { UniteRond } from './ronds/repartir-ronds'
import './feuille-cibles.css'

export type MesuresFeuille = {
  /** Hauteur visible en position haute (plein cadre). */
  haute: number
  /** Hauteur visible en position basse : tout le contenu, boutons compris. */
  basse: number
  /** Hauteur visible en position reduite : poignee, titre, compteur. */
  reduite: number
}

export type FeuilleCiblesProps = {
  /** Change a chaque nouvelle question : la position choisie est alors oubliee. */
  signature: string
  /** Le nom de la carte qui pose la question (« Marrow »). */
  source: string
  /** La consigne (« Choisis la cible »). */
  consigne: string
  /** Ou on en est (« 0/1 requise(s) · 2 possible(s) »). */
  compte: string
  /** Une ligne d'aide, quand une meme carte se choisit plusieurs fois. */
  indice?: string
  unites: UniteAffichee[]
  decor: DecorRonds
  prete: boolean
  libelleValider: string
  libelleAnnuler: string
  annuler: () => void
  valider: () => void
  /** Classe de tonalite de l'action (couleur de l'en-tete). */
  tonalite?: string
  /** Les hauteurs de chaque position ; mesurees dans le DOM quand elles ne sont pas fournies (les tests n'ont pas de mise en page). */
  mesures?: () => MesuresFeuille
}

const SEUIL_GLISSER = 6
const VITESSE_MAX = 40
const ORDRE: PositionFeuille[] = ['reduite', 'basse', 'haute']

function mesurerLeDom(feuille: HTMLElement): MesuresFeuille {
  const enfants = Array.from(feuille.children) as HTMLElement[]
  const bordures = feuille.offsetHeight - feuille.clientHeight
  const naturel = enfants.reduce((somme, enfant) => somme + enfant.offsetHeight, 0) + Math.max(0, bordures)
  const hauteurDe = (selecteur: string) => (feuille.querySelector(selecteur) as HTMLElement | null)?.offsetHeight ?? 0
  const reduite = hauteurDe('.feuille-poignee') + hauteurDe('.feuille-entete') + hauteurDe('.feuille-compte') + Math.max(0, bordures)
  const pleinCadre = Math.min(Math.round(window.innerHeight * 0.86), 760)
  return { haute: Math.max(naturel, pleinCadre), basse: Math.min(naturel, pleinCadre), reduite }
}

function visibleEn(position: PositionFeuille, mesures: MesuresFeuille): number {
  if (position === 'haute') return mesures.haute
  if (position === 'basse') return Math.min(mesures.basse, mesures.haute)
  return Math.min(mesures.reduite, mesures.haute)
}

function zoneDuRond(unite: UniteAffichee): 'allies' | 'sbires' {
  return unite.carte.camp === 'player' ? 'allies' : 'sbires'
}

export function FeuilleCibles({
  signature,
  source,
  consigne,
  compte,
  indice,
  unites,
  decor,
  prete,
  libelleValider,
  libelleAnnuler,
  annuler,
  valider,
  tonalite,
  mesures: fournies,
}: FeuilleCiblesProps) {
  const feuille = useRef<HTMLElement | null>(null)
  // La position est celle de CETTE question : une nouvelle `signature` repart de la position basse.
  const [etat, setEtat] = useState<{ signature: string; position: PositionFeuille }>({ signature, position: 'basse' })
  if (etat.signature !== signature) setEtat({ signature, position: 'basse' })
  const position = etat.signature === signature ? etat.position : 'basse'
  const [mesures, setMesures] = useState<MesuresFeuille | null>(() => fournies?.() ?? null)
  const [glissee, setGlissee] = useState(false)

  // Mesures reelles : a chaque changement de contenu et de taille d'ecran. Jamais pendant un geste.
  const mesurer = useCallback(() => {
    if (fournies) return setMesures(fournies())
    const element = feuille.current
    if (!element) return
    // Le contenu naturel se lit hors position haute (la rangee y passe a la ligne et change de hauteur).
    setMesures((avant) => {
      const mesure = mesurerLeDom(element)
      return avant && avant.haute === mesure.haute && avant.basse === mesure.basse && avant.reduite === mesure.reduite ? avant : mesure
    })
  }, [fournies])
  useLayoutEffect(mesurer, [mesurer, unites.length, compte, consigne, indice, position === 'haute'])
  useEffect(() => {
    window.addEventListener('resize', mesurer)
    window.addEventListener('orientationchange', mesurer)
    return () => {
      window.removeEventListener('resize', mesurer)
      window.removeEventListener('orientationchange', mesurer)
    }
  }, [mesurer])

  const positions: PositionsFeuille | undefined = mesures
    ? positionsFeuille({ hauteur: mesures.haute, basse: mesures.basse, reduite: mesures.reduite })
    : undefined

  // --- Le geste -------------------------------------------------------------------------------------------------
  const geste = useRef<{
    y0: number
    h0: number
    commence: boolean
    yPrec: number
    tPrec: number
    vitesse: number
    hauteur: number
  } | null>(null)
  const ecouteurs = useRef<{ bouge: (e: PointerEvent) => void; fin: (e: PointerEvent) => void } | null>(null)
  const mesuresCourantes = useRef<MesuresFeuille | null>(mesures)
  mesuresCourantes.current = mesures

  const retirerEcouteurs = useCallback(() => {
    const courants = ecouteurs.current
    if (!courants) return
    window.removeEventListener('pointermove', courants.bouge)
    window.removeEventListener('pointerup', courants.fin)
    window.removeEventListener('pointercancel', courants.fin)
    ecouteurs.current = null
  }, [])
  useEffect(() => retirerEcouteurs, [retirerEcouteurs])

  const surAppui = (evenement: ReactPointerEvent<HTMLElement>) => {
    if (evenement.pointerType === 'mouse' && evenement.button !== 0) return
    const courantes = mesuresCourantes.current
    if (!courantes) return
    retirerEcouteurs()
    const h0 = feuille.current?.offsetHeight || visibleEn(position, courantes)
    geste.current = { y0: evenement.clientY, h0, commence: false, yPrec: evenement.clientY, tPrec: performance.now(), vitesse: 0, hauteur: h0 }
    const bouge = (e: PointerEvent) => {
      const g = geste.current
      const m = mesuresCourantes.current
      if (!g || !m) return
      const dy = e.clientY - g.y0
      if (!g.commence) {
        if (Math.abs(dy) < SEUIL_GLISSER) return
        g.commence = true
        setGlissee(true)
      }
      const p = positionsFeuille({ hauteur: m.haute, basse: m.basse, reduite: m.reduite })
      // `dy` > 0 : le doigt descend, la feuille aussi (sa hauteur visible diminue).
      const decalage = borner(m.haute - (g.h0 - dy), p)
      g.hauteur = m.haute - decalage
      const maintenant = performance.now()
      const duree = Math.max(8, maintenant - g.tPrec)
      g.vitesse = Math.max(-VITESSE_MAX, Math.min(VITESSE_MAX, ((e.clientY - g.yPrec) / duree) * 16))
      g.yPrec = e.clientY
      g.tPrec = maintenant
      feuille.current?.style.setProperty('--feuille-h', `${Math.round(g.hauteur)}px`)
    }
    const fin = () => {
      const g = geste.current
      const m = mesuresCourantes.current
      geste.current = null
      retirerEcouteurs()
      setGlissee(false)
      if (!g || !m || !g.commence) return
      const p = positionsFeuille({ hauteur: m.haute, basse: m.basse, reduite: m.reduite })
      const decalage = m.haute - g.hauteur
      setEtat({ signature, position: caler(decalage, g.vitesse, p) })
    }
    ecouteurs.current = { bouge, fin }
    window.addEventListener('pointermove', bouge)
    window.addEventListener('pointerup', fin)
    window.addEventListener('pointercancel', fin)
  }

  // Le clavier : les fleches montent et descendent d'un cran.
  const surTouche = (evenement: ReactKeyboardEvent<HTMLElement>) => {
    const rang = ORDRE.indexOf(position)
    if (evenement.key === 'ArrowUp') {
      evenement.preventDefault()
      setEtat({ signature, position: ORDRE[Math.min(ORDRE.length - 1, rang + 1)]! })
    } else if (evenement.key === 'ArrowDown') {
      evenement.preventDefault()
      setEtat({ signature, position: ORDRE[Math.max(0, rang - 1)]! })
    } else if (evenement.key === 'Enter' || evenement.key === ' ') {
      evenement.preventDefault()
      setEtat({ signature, position: position === 'haute' ? 'basse' : position === 'basse' ? 'haute' : 'basse' })
    }
  }

  const hauteurAuRepos = mesures ? `${Math.round(visibleEn(position, mesures))}px` : undefined
  const decorFeuille = decor
  const etiquettePoignee = t('Déplacer la fenêtre (flèches haut et bas)')
  return (
    <aside
      ref={feuille}
      role="dialog"
      aria-label={consigne}
      aria-live="polite"
      data-position={position}
      className={`assistant-action est-feuille-cible${tonalite ? ` ${tonalite}` : ''}${glissee ? ' est-glissee' : ''}`}
      style={hauteurAuRepos && !glissee ? ({ ['--feuille-h' as string]: hauteurAuRepos } as React.CSSProperties) : undefined}
    >
      <div
        className="feuille-poignee"
        data-geste="feuille"
        role="button"
        tabIndex={0}
        aria-label={etiquettePoignee}
        onPointerDown={surAppui}
        onKeyDown={surTouche}
      >
        <i aria-hidden="true" />
      </div>
      <div className="feuille-entete" data-geste="feuille" onPointerDown={surAppui}>
        <small>{source}</small>
        <h2>{consigne}</h2>
      </div>
      <div className="feuille-compte">{compte}</div>
      <div className="feuille-cibles" data-defile={position === 'haute' ? 'vertical' : 'horizontal'}>
        {unites.map((unite) => (
          <Rond key={unite.cle} unite={unite as UniteRond} zone={zoneDuRond(unite)} decor={decorFeuille} />
        ))}
      </div>
      {indice ? <p className="feuille-indice">{indice}</p> : null}
      <div className="feuille-actions">
        <button type="button" className="assistant-annuler" onClick={annuler}>
          {libelleAnnuler}
        </button>
        <button type="button" className="assistant-confirmer" disabled={!prete} onClick={valider}>
          {libelleValider}
        </button>
      </div>
    </aside>
  )
}
