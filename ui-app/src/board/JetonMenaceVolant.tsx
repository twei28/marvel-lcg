// Le jeton de menace qui part du MILIEU DE L'ÉCRAN vers la manigance visée.
//
// Demande de l'utilisateur, 14/09/2026, sur le point 1 de la phase du méchant :
// « on voit le nom de manigance qui se met sur la manigance principale dans la
// phrase et on voit le jeton qui va vers la carte de la manigance où ça va se
// mettre. » Et sur son point de départ : « le jeton part du milieu de l'écran »,
// là où il vient de lire la phrase.
//
// Sur son allure, parmi trois formes proposées : « le jeton avec son nombre
// dessus ». Il porte « +1 » pendant tout son vol, pour qu'on sache combien
// arrive sans attendre que le compteur de la manigance monte.
//
// ⚠ C'EST LE VRAI JETON DU JEU, pas un rond dessiné. Première version : un
// disque jaune. Constat de l'utilisateur, 14/09/2026 : « qu'il ait déjà la même
// forme que le triangle là. Pourquoi tu me fais un rond ? » L'image existait
// déjà et servait à la scène du mode Détaillé (`components/jetons/menace.png`,
// le triangle de menace) : il n'y avait rien à dessiner, seulement à s'en
// servir.
//
// ⚠ IL NE REMPLACE PAS LE COMPTEUR, il l'annonce. C'est le moteur qui pose la
// menace ; ce jeton-ci est un récit, il ne change rien à la partie.
//
// ⚠ ET IL NE VOLE QU'UNE FOIS PAR ÉTAPE. Le plateau se redessine plusieurs fois
// par seconde pendant la phase : sans la clé de l'étape en dépendance, le vol
// repartirait à zéro à chaque trame et le jeton resterait collé au départ.

import { useEffect, useLayoutEffect, useState } from 'react'
import jetonMenaceImage from '../components/jetons/menace.png'
import { boiteDeCarte, cadreDuPlateau } from './mesures-plateau'
import type { Boite } from './places-rencontre'

/** Le temps du vol. Assez lent pour suivre le jeton des yeux. */
export const DUREE_VOL_MS = 700

export function JetonMenaceVolant({
  cibleId,
  montant,
  cle,
  actif,
}: {
  /** La manigance visée, telle que l'étape la porte. */
  cibleId: number | undefined
  /** Combien de menace arrive. Le jeton le porte pendant son vol. */
  montant: number | undefined
  /** L'étape en cours : c'est elle qui déclenche un vol, et un seul. */
  cle: string | undefined
  actif: boolean
}) {
  const [vol, setVol] = useState<{ depart: Boite; arrivee: Boite } | undefined>(undefined)
  const [arrive, setArrive] = useState(false)

  useLayoutEffect(() => {
    if (!actif || cibleId === undefined) {
      setVol(undefined)
      return
    }
    const cadre = cadreDuPlateau()
    if (!cadre) return
    const cible = boiteDeCarte(cibleId, cadre)
    // La manigance n'est plus sur la table : on ne fait pas voler un jeton vers
    // un point inventé. La phrase et le compteur disent déjà ce qui se passe.
    if (!cible) {
      setVol(undefined)
      return
    }
    // La taille du jeton posé sur une manigance, pour qu'il arrive à la bonne
    // échelle plutôt que de rapetisser en se posant.
    const TAILLE = 52
    setArrive(false)
    setVol({
      depart: {
        x: cadre.boite.x + cadre.boite.w / 2 - TAILLE / 2,
        y: cadre.boite.y + cadre.boite.h / 2 - TAILLE / 2,
        w: TAILLE,
        h: TAILLE,
      },
      arrivee: {
        x: cible.x + cible.w / 2 - TAILLE / 2,
        y: cible.y + cible.h / 2 - TAILLE / 2,
        w: TAILLE,
        h: TAILLE,
      },
    })
  }, [actif, cibleId, cle])

  // Le vol : on pose le jeton au départ, puis on le déplace au rendu suivant.
  // Deux rendus, sinon le navigateur n'a aucune position de départ à animer et
  // le jeton apparaît directement à l'arrivée.
  useEffect(() => {
    if (!vol) return
    const image = window.requestAnimationFrame(() => setArrive(true))
    return () => window.cancelAnimationFrame(image)
  }, [vol])

  if (!vol) return null
  const ou = arrive ? vol.arrivee : vol.depart
  // PLUSIEURS JETONS VISIBLES (v3, Q14) : un par menace posee, jusqu'a six,
  // partis l'un apres l'autre ; le premier porte le total.
  const nombre = Math.min(6, Math.max(1, montant ?? 1))

  return (
    <>
      {Array.from({ length: nombre }, (_, rang) => (
        <span
          key={rang}
          className={`jeton-menace-volant${arrive ? ' est-arrive' : ''}`}
          style={{
            left: `${ou.x + (rang % 3) * 8 - 8}px`,
            top: `${ou.y - Math.floor(rang / 3) * 8}px`,
            width: `${ou.w}px`,
            height: `${ou.h}px`,
            backgroundImage: `url(${jetonMenaceImage})`,
            transitionDelay: `${rang * 120}ms`,
          }}
          aria-hidden="true"
        >
          {rang === 0 && montant !== undefined ? `+${montant}` : ''}
        </span>
      ))}
    </>
  )
}
