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
import { useEffect, useRef, useState } from 'react'
import { t } from './langue'
import { estSpectateur } from './moteur'
import { lecteurActif } from './relecture/lecteur'

export const CLE_CURSEURS = 'marvel-board-curseurs'

export function lireCurseursActifs(): boolean {
  try {
    return window.localStorage.getItem(CLE_CURSEURS) !== 'off'
  } catch {
    return true
  }
}

export const COULEURS_JOUEURS = ['#4da3ff', '#ffd45a', '#7fd77f', '#ff7a7a']

type Curseurs = Record<string, { x: number; y: number; survol?: string; clic?: number }>

type Onde = { cle: string; x: number; y: number; joueur: number }

const DUREE_ONDE_MS = 700

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
  monJoueur: monSiege,
  nomsJoueurs,
}: {
  actif: boolean
  monJoueur: number
  nomsJoueurs: string[]
}) {
  // ⚠ UN SPECTATEUR N'EST AUCUN JOUEUR. Son siege vaut 0 par defaut : sans cela
  // il se filtrait lui-meme et ne voyait jamais le curseur du joueur 0, donc
  // jamais celui d'une partie solo (mesure du 07/10/2026, deux clients).
  const monJoueur = estSpectateur() ? -1 : monSiege
  const [curseurs, setCurseurs] = useState<Curseurs>({})
  const [ondes, setOndes] = useState<Onde[]>([])
  const clicsVus = useRef<Record<string, number> | null>(null)

  // Émission : position de MA souris, normalisée sur la scène.
  useEffect(() => {
    if (!actif) return
    // Un spectateur ne montre rien de lui : voir l'en-tête.
    if (estSpectateur()) return
    let dernierEnvoi = 0
    const envoyer = (evenement: MouseEvent, clic?: number) => {
      const scene = sceneDuPlateau()
      if (!scene) return
      const zone = scene.getBoundingClientRect()
      if (zone.width === 0 || zone.height === 0) return
      const x = (evenement.clientX - zone.left) / zone.width
      const y = (evenement.clientY - zone.top) / zone.height
      const survol = carteSousLePointeur(evenement.clientX, evenement.clientY)
      void fetch('/set_cursor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ p: monJoueur, x, y, survol, ...(clic === undefined ? {} : { clic }) }),
      }).catch(() => undefined)
    }
    const surSouris = (evenement: MouseEvent) => {
      const maintenant = Date.now()
      if (maintenant - dernierEnvoi < 150) return
      dernierEnvoi = maintenant
      envoyer(evenement)
    }
    // Un clic part tout de suite, hors du plafond des 150 ms : sinon un clic
    // juste apres un mouvement n'arriverait jamais au spectateur.
    const surClic = (evenement: MouseEvent) => {
      dernierEnvoi = Date.now()
      envoyer(evenement, dernierEnvoi)
    }
    document.addEventListener('mousemove', surSouris)
    document.addEventListener('mousedown', surClic, true)
    return () => {
      document.removeEventListener('mousemove', surSouris)
      document.removeEventListener('mousedown', surClic, true)
    }
  }, [actif, monJoueur])

  // Réception : les curseurs des autres.
  useEffect(() => {
    if (!actif) {
      setCurseurs({})
      return
    }
    // Relecture : les curseurs viennent du fichier, au temps de la lecture.
    const lecteur = lecteurActif()
    if (lecteur) {
      const lireFichier = () => {
        const donnees = lecteur.curseursA(lecteur.tempsCourant())
        if (clicsVus.current === null) {
          clicsVus.current = Object.fromEntries(Object.entries(donnees).map(([p, c]) => [p, c.clic]))
        }
        setCurseurs(donnees)
      }
      const minuteurFichier = window.setInterval(lireFichier, 100)
      return () => window.clearInterval(minuteurFichier)
    }
    const minuteur = window.setInterval(() => {
      fetch('/get_cursors')
        .then((reponse) => (reponse.ok ? reponse.json() : {}))
        .then((donnees: Curseurs) => {
          // Premiere lecture : elle fixe la base des clics deja faits.
          if (clicsVus.current === null) {
            clicsVus.current = Object.fromEntries(Object.entries(donnees).map(([p, c]) => [p, c.clic ?? 0]))
          }
          setCurseurs(donnees)
        })
        .catch(() => undefined)
    }, 700)
    return () => window.clearInterval(minuteur)
  }, [actif])

  // Une onde par clic nouveau. La premiere lecture ne fait qu'enregistrer : un
  // clic d'avant notre arrivee n'est pas un clic a rejouer.
  useEffect(() => {
    if (!actif) {
      clicsVus.current = null
      return
    }
    const vus = clicsVus.current
    if (vus === null) return
    const suivant: Record<string, number> = {}
    const nouvelles: Onde[] = []
    for (const [p, position] of Object.entries(curseurs)) {
      const clic = position.clic ?? 0
      suivant[p] = clic
      // Un joueur qu'on voit pour la premiere fois n'a que son dernier clic
      // d'avant (le serveur le garde apres la peremption) : on le retient sans
      // le rejouer.
      if (vus[p] !== undefined && clic !== 0 && clic !== vus[p] && Number(p) !== monJoueur) {
        nouvelles.push({ cle: `${p}-${clic}`, x: position.x, y: position.y, joueur: Number(p) })
      }
    }
    clicsVus.current = suivant
    if (nouvelles.length === 0) return
    setOndes((courantes) => [...courantes, ...nouvelles])
    const cles = new Set(nouvelles.map((o) => o.cle))
    // Pas de nettoyage : chaque lecture (700 ms) relance cet effet et
    // annulerait le retrait avant son terme.
    window.setTimeout(
      () => setOndes((courantes) => courantes.filter((o) => !cles.has(o.cle))),
      DUREE_ONDE_MS
    )
  }, [actif, curseurs, monJoueur])

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
                '--couleur': COULEURS_JOUEURS[joueur % COULEURS_JOUEURS.length],
              } as React.CSSProperties}
            >
              <span className="curseur-pointe" />
              <span className="curseur-nom">{nomsJoueurs[joueur] ?? `${t('Joueur')} ${joueur}`}</span>
            </div>
          )
        })}
      {ondes.map((onde) => (
        <span
          key={onde.cle}
          className="curseur-onde"
          style={{
            left: zone.left + onde.x * zone.width,
            top: zone.top + onde.y * zone.height,
            '--couleur': COULEURS_JOUEURS[onde.joueur % COULEURS_JOUEURS.length],
          } as React.CSSProperties}
        />
      ))}
    </div>
  )
}
