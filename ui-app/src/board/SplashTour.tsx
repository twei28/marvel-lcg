// « A qui le tour », en grand, juste avant que le tour commence.
//
// Le plateau ne l'annonce que dans le bandeau du haut, en petit : a plusieurs,
// on rate le changement et on joue le tour de quelqu'un d'autre. Ce splash le
// rejoue sur toute la table, deux secondes, puis s'efface.
//
// Il ne prend JAMAIS le pointeur (pointer-events: none cote CSS) : un panneau
// plein ecran qui avale les clics pendant deux secondes coute plus cher qu'il
// ne rapporte. Un clic ou une touche l'escamote tout de suite.
//
// Le moteur ne connait pas d'etat « phase du mechant » : il la decoupe en
// etapes (Main Scheme Place Threat, Enemy Activation, Deal Encounter Cards...).
// On ne declenche donc que sur la PREMIERE, sans quoi le splash reviendrait
// quatre fois de suite. Valeurs : game/world/phase.py, Phase.State.

import { useEffect, useRef, useState } from 'react'
import { t } from './langue'
import type { World } from './world'

const DUREE_MS = 2200

/** Premiere etape de la phase du mechant : Phase.State.PlaceThreat. */
const DEBUT_PHASE_MECHANT = 'Main Scheme Place Threat'

type Tour = {
  cle: string
  camp: 'heros' | 'mechant'
  surtitre: string
  titre: string
  soustitre?: string
}

/** Le moteur prefixe les identites d'un marqueur (« ✦ Gwenpool »). */
function nomPropre(nom: string | undefined): string | undefined {
  const propre = nom?.replace(/^\W*/, '').trim()
  return propre ? propre : undefined
}

function tourCourant(monde: World | undefined, annonceMechantAilleurs: boolean): Tour | undefined {
  if (!monde) return undefined

  const surtitre = `${t('Round')} ${monde.round_id}`
  const cle = `${monde.round_id}:${monde.phase}`

  const joueur = monde.phase.match(/^Player (\d+) Turn$/)
  if (joueur) {
    const numero = Number(joueur[1])
    const heros = nomPropre(monde.players?.[numero - 1]?.area_hero?.[0]?.name)
    return {
      cle,
      camp: 'heros',
      surtitre,
      titre: heros ?? `${t('Joueur')} ${numero}`,
      soustitre: heros ? `${t('Joueur')} ${numero}` : undefined,
    }
  }

  if (monde.phase === DEBUT_PHASE_MECHANT) {
    // Cette branche est la SEULE que `annonceMechantAilleurs` neutralise : en
    // mode detaille, BandeauPhase.tsx annonce deja la phase du mechant, sur ce
    // meme declencheur, avec un effet plus fort. Sans ce garde-fou, les deux
    // annonces se superposaient a chaque round. Le tour d'un joueur, ci-dessus,
    // n'a pas d'equivalent ailleurs : il n'est jamais concerne.
    if (annonceMechantAilleurs) return undefined

    return {
      cle,
      camp: 'mechant',
      surtitre,
      titre: t('Phase du méchant'),
      soustitre: nomPropre(monde.area_villain?.[0]?.name),
    }
  }

  return undefined
}

export function SplashTour({
  monde,
  annonceMechantAilleurs = false,
}: {
  monde: World | undefined
  /**
   * Neutralise la seule branche « phase du mechant » de ce splash. Sert
   * quand une autre annonce prend deja le relais sur le meme declencheur
   * (le bandeau du mode detaille, plus fort) : sans ce garde-fou, les deux
   * s'affichaient en meme temps et leurs textes se chevauchaient. Le splash
   * du tour d'un joueur reste toujours affiche, dans tous les modes.
   */
  annonceMechantAilleurs?: boolean
}) {
  const tour = tourCourant(monde, annonceMechantAilleurs)
  const [affiche, setAffiche] = useState<Tour | undefined>(undefined)
  const dernier = useRef<string | undefined>(undefined)

  // Ce qui est affiche est COPIE dans l'etat, au lieu d'etre lu sur la phase
  // courante. La phase du mechant ne s'attarde pas sur sa premiere etape : elle
  // enchaine sur Enemy Activation en quelques dixiemes de seconde. Tant que
  // l'affichage suivait la phase, le splash du mechant disparaissait aussitot —
  // un tour de joueur, lui, dure assez longtemps pour que rien ne se voie.
  useEffect(() => {
    if (!tour || tour.cle === dernier.current) return
    dernier.current = tour.cle
    setAffiche(tour)
  }, [tour?.cle])

  // Le minuteur appartient a ce qui est affiche, pas au monde : un changement de
  // phase ne peut plus l'annuler avant terme.
  useEffect(() => {
    if (!affiche) return

    const minuteur = window.setTimeout(() => setAffiche(undefined), DUREE_MS)
    const escamoter = () => setAffiche(undefined)
    document.addEventListener('pointerdown', escamoter)
    document.addEventListener('keydown', escamoter)

    return () => {
      window.clearTimeout(minuteur)
      document.removeEventListener('pointerdown', escamoter)
      document.removeEventListener('keydown', escamoter)
    }
  }, [affiche])

  if (!affiche) return null

  return (
    <div className={`splash-tour est-${affiche.camp}`} aria-live="polite" key={affiche.cle}>
      <div className="splash-tour-carte">
        <span className="splash-tour-surtitre">{affiche.surtitre}</span>
        <strong className="splash-tour-titre">{affiche.titre}</strong>
        {affiche.soustitre ? <span className="splash-tour-soustitre">{affiche.soustitre}</span> : null}
      </div>
    </div>
  )
}
