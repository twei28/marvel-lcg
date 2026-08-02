// Bannière des hauts faits débloqués en cours de partie.
//
// À ne pas confondre avec CoucheSucces, qui affiche les séries de K.O. du
// moteur (« Achievement: DOUBLE_KILL ») repérées dans la narration. Ici il
// s'agit des 48 hauts faits de game/achievements.py, annoncés par Notify.Game
// et acheminés dans notify_texts. Moteur.enregistrerHautsFaits() les accumule ;
// cette couche présente les nouveaux venus, un par un.
//
// Une file d'attente, pas un simple « dernier arrivé » : franchir un palier de
// round peut en débloquer plusieurs d'un coup, et un remplacement immédiat n'en
// laisserait lire aucun.

import { useEffect, useRef, useState } from 'react'
import { t } from './langue'

const DUREE_BANNIERE = 3600

export function CoucheHautsFaits({ hautsFaits }: { hautsFaits: string[] }) {
  const [courant, setCourant] = useState<string | undefined>(undefined)
  const file = useRef<string[]>([])
  const traites = useRef(0)
  const minuteur = useRef<number | undefined>(undefined)

  // Seuls les titres AJOUTÉS depuis le dernier passage entrent dans la file.
  useEffect(() => {
    if (hautsFaits.length <= traites.current) {
      // La liste a été remise à zéro (nouvelle partie) : on repart de son état.
      traites.current = hautsFaits.length
      return
    }
    file.current.push(...hautsFaits.slice(traites.current))
    traites.current = hautsFaits.length
    setCourant((actuel) => actuel ?? file.current.shift())
  }, [hautsFaits])

  // Défilement de la file : chaque bannière tient l'écran puis cède la place.
  useEffect(() => {
    if (courant === undefined) return
    minuteur.current = window.setTimeout(() => {
      setCourant(file.current.shift())
    }, DUREE_BANNIERE)
    return () => {
      if (minuteur.current !== undefined) window.clearTimeout(minuteur.current)
    }
  }, [courant])

  if (courant === undefined) return null

  return (
    <div className="banniere-succes est-haut-fait" role="status" key={courant}>
      <span aria-hidden="true">{'\u{1F396}'}</span>
      <span className="banniere-succes-eyebrow">{t('Haut fait')}</span>
      <strong>{courant}</strong>
    </div>
  )
}
