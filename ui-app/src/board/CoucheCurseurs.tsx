// CoucheCurseurs — voir la souris des autres joueurs, et celle du joueur
// qu'on REGARDE.
//
// Chaque client envoie sa position normalisée (0..1) par rapport à la scène
// du plateau (POST /set_cursor, throttle 150 ms) et lit celles des autres
// (GET /get_cursors, toutes les 700 ms, périmées en 5 s côté serveur).
// Purement cosmétique, désactivable (localStorage marvel-board-curseurs,
// actif par défaut).
//
// ⚠ LE SPECTATEUR REGARDE, IL N'ÉMET PAS (17/09/2026). Il était exclu deux
// fois : la couche ne s'allumait qu'à plusieurs joueurs, donc jamais sur une
// partie solo regardée. Et si on l'avait simplement allumée, il aurait envoyé
// SA souris au moteur : son curseur serait apparu sur l'écran du joueur, alors
// que tout le mode spectateur est bâti pour qu'il reste invisible.
import { useEffect, useState } from 'react'
import { t } from './langue'
import { estSpectateur } from './moteur'

export const CLE_CURSEURS = 'marvel-board-curseurs'

export function lireCurseursActifs(): boolean {
  try {
    return window.localStorage.getItem(CLE_CURSEURS) !== 'off'
  } catch {
    return true
  }
}

const COULEURS = ['#4da3ff', '#ffd45a', '#7fd77f', '#ff7a7a']

type Curseurs = Record<string, { x: number; y: number; survol?: string }>

/** La carte sous le pointeur, ou '' s'il n'y en a pas.
 *
 *  ⚠ `elementFromPoint` PLUTOT QU'UN ECOUTEUR PAR CARTE : les cartes se
 *  redessinent a chaque trame, et poser un `mouseenter` sur chacune ferait
 *  autant d'abonnements a recreer. On demande au navigateur ce qu'il y a sous
 *  le doigt, une fois tous les 150 ms, au moment ou on envoie de toute facon. */
function carteSousLePointeur(x: number, y: number): string {
  const cible = document.elementFromPoint(x, y)
  const porteur = cible?.closest?.('[data-card-id]') as HTMLElement | null
  return porteur?.dataset?.cardId ?? ''
}

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
    // Un spectateur ne montre rien de lui : voir l'en-tête.
    if (estSpectateur()) return
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
      const survol = carteSousLePointeur(evenement.clientX, evenement.clientY)
      void fetch('/set_cursor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ p: monJoueur, x, y, survol }),
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

  // ⚠ LE HALO EST POSE SUR LA CARTE ELLE-MEME, PAS DESSINE PAR-DESSUS. Une
  // boite superposee serait calee sur la position d'un instant, et glisserait
  // des que le plateau se redessine ou defile. Une classe sur la carte suit
  // la carte, quoi qu'il arrive.
  useEffect(() => {
    if (!actif) return
    const vises = Object.entries(curseurs)
      .filter(([p]) => Number(p) !== monJoueur)
      .map(([, position]) => position.survol)
      .filter((carte): carte is string => typeof carte === 'string' && carte !== '')
    const poses: Element[] = []
    for (const carte of vises) {
      for (const noeud of document.querySelectorAll(`[data-card-id="${CSS.escape(carte)}"]`)) {
        noeud.classList.add('carte-survolee-par-un-autre')
        poses.push(noeud)
      }
    }
    return () => poses.forEach((n) => n.classList.remove('carte-survolee-par-un-autre'))
  }, [actif, curseurs, monJoueur])

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
