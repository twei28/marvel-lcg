// CoucheCurseurs — voir la souris des autres joueurs en multijoueur.
//
// Chaque client envoie sa position normalisée (0..1) par rapport à la scène
// du plateau (POST /set_cursor, throttle 150 ms) et lit celles des autres
// (GET /get_cursors, toutes les 700 ms, périmées en 5 s côté serveur).
// Purement cosmétique, actif seulement à plusieurs joueurs, désactivable
// (localStorage marvel-board-curseurs, actif par défaut).
import { useEffect, useState } from 'react'
import { t } from './langue'

export const CLE_CURSEURS = 'marvel-board-curseurs'

export function lireCurseursActifs(): boolean {
  try {
    return window.localStorage.getItem(CLE_CURSEURS) !== 'off'
  } catch {
    return true
  }
}

const COULEURS = ['#4da3ff', '#ffd45a', '#7fd77f', '#ff7a7a']

type Curseurs = Record<string, { x: number; y: number }>

function sceneDuPlateau(): HTMLElement | null {
  return document.querySelector('.plateau-scene')
}

export function CoucheCurseurs({
  actif,
  monJoueur,
  nomsJoueurs,
}: {
  actif: boolean
  monJoueur: number
  nomsJoueurs: string[]
}) {
  const [curseurs, setCurseurs] = useState<Curseurs>({})

  // Émission : position de MA souris, normalisée sur la scène.
  useEffect(() => {
    if (!actif) return
    let dernierEnvoi = 0
    const surSouris = (evenement: MouseEvent) => {
      const maintenant = Date.now()
      if (maintenant - dernierEnvoi < 150) return
      const scene = sceneDuPlateau()
      if (!scene) return
      const zone = scene.getBoundingClientRect()
      if (zone.width === 0 || zone.height === 0) return
      dernierEnvoi = maintenant
      const x = (evenement.clientX - zone.left) / zone.width
      const y = (evenement.clientY - zone.top) / zone.height
      void fetch('/set_cursor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ p: monJoueur, x, y }),
      }).catch(() => undefined)
    }
    document.addEventListener('mousemove', surSouris)
    return () => document.removeEventListener('mousemove', surSouris)
  }, [actif, monJoueur])

  // Réception : les curseurs des autres.
  useEffect(() => {
    if (!actif) {
      setCurseurs({})
      return
    }
    const minuteur = window.setInterval(() => {
      fetch('/get_cursors')
        .then((reponse) => (reponse.ok ? reponse.json() : {}))
        .then((donnees: Curseurs) => setCurseurs(donnees))
        .catch(() => undefined)
    }, 700)
    return () => window.clearInterval(minuteur)
  }, [actif])

  if (!actif) return null
  const scene = sceneDuPlateau()
  if (!scene) return null
  const zone = scene.getBoundingClientRect()

  return (
    <div className="couche-curseurs" aria-hidden="true">
      {Object.entries(curseurs)
        .filter(([p]) => Number(p) !== monJoueur)
        .map(([p, position]) => {
          const joueur = Number(p)
          return (
            <div
              key={p}
              className="curseur-joueur"
              style={{
                left: zone.left + position.x * zone.width,
                top: zone.top + position.y * zone.height,
                '--couleur': COULEURS[joueur % COULEURS.length],
              } as React.CSSProperties}
            >
              <span className="curseur-pointe" />
              <span className="curseur-nom">{nomsJoueurs[joueur] ?? `${t('Joueur')} ${joueur}`}</span>
            </div>
          )
        })}
    </div>
  )
}
