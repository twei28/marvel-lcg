// musique.ts — musique d'ambiance par scénario (optionnelle, OFF par défaut).
//
// Aucun fichier audio n'est livré : le hook cherche simplement
// `/musique-<slug-du-mechant>.mp3` puis `/musique-plateau.mp3` (résolus par le
// serveur dans assets/sounds/, route .mp3 de web_server.py). Il suffit donc de
// déposer par exemple assets/sounds/musique-rhino.mp3 pour que Rhino ait son
// thème, et musique-plateau.mp3 comme thème générique. Rien trouvé = silence.
// Activable au choix (localStorage marvel-board-musique, INACTIF par défaut,
// car il faut un geste utilisateur pour l'autoplay de toute façon).
import { useEffect, useRef } from 'react'
import type { World } from './world'

export const CLE_MUSIQUE = 'marvel-board-musique'
/** Le volume de la musique, en %, réglé dans Réglages > Son (comme celui des bruitages). */
export const CLE_VOLUME_MUSIQUE = 'marvel-board-volume-musique'
export const VOLUME_MUSIQUE_PAR_DEFAUT = 25
const EVENEMENT_VOLUME = 'marvel-board-volume-musique-change'

export function lireVolumeMusique(): number {
  try {
    const brut = window.localStorage.getItem(CLE_VOLUME_MUSIQUE)
    if (brut === null) return VOLUME_MUSIQUE_PAR_DEFAUT
    const valeur = Number(brut)
    return Number.isFinite(valeur) ? Math.min(100, Math.max(0, valeur)) : VOLUME_MUSIQUE_PAR_DEFAUT
  } catch {
    return VOLUME_MUSIQUE_PAR_DEFAUT
  }
}

/** Enregistre le volume ET le répercute tout de suite sur la musique qui joue. */
export function ecrireVolumeMusique(volume: number): void {
  try {
    window.localStorage.setItem(CLE_VOLUME_MUSIQUE, String(Math.round(Math.min(100, Math.max(0, volume)))))
  } catch {
    // Stockage refusé : le réglage vaut pour cette page seulement.
  }
  window.dispatchEvent(new Event(EVENEMENT_VOLUME))
}

export function lireMusiqueActive(): boolean {
  try {
    return window.localStorage.getItem(CLE_MUSIQUE) === 'on'
  } catch {
    return false
  }
}

function slugMechant(world: World | undefined): string | undefined {
  const nom = world?.area_villain?.[0]?.name
  if (!nom) return undefined
  const slug = nom
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
  return slug || undefined
}

function attendreUnGeste(rappel: () => void): void {
  const evenements = ['pointerdown', 'keydown']
  const une = () => {
    evenements.forEach((e) => window.removeEventListener(e, une, true))
    rappel()
  }
  evenements.forEach((e) => window.addEventListener(e, une, true))
}

export function useMusique(world: World | undefined, active: boolean): void {
  const lecteur = useRef<HTMLAudioElement | null>(null)
  const sourceEnCours = useRef<string>('')
  const slug = slugMechant(world)

  // IMPORTANT : cet effet ne dépend PAS de `world`. Il dépendait de `world` avant le
  // correctif « musique coupée » : à chaque nouveau monde (incliner, redresser, changer
  // de mode...), le nettoyage marquait la passe précédente comme « annulée ». Or le
  // morceau propre au méchant n'existe presque jamais : son <audio> se déclare en erreur
  // un instant plus tard, et cette erreur, tombée dans une passe annulée, était ignorée.
  // Le repli sur musique-plateau.mp3 n'avait donc jamais lieu et la musique se taisait
  // jusqu'à un décochage/recochage. Les mondes n'ont rien à faire ici : seuls le méchant
  // (slug) et l'interrupteur (active) changent ce qu'on joue.
  useEffect(() => {
    if (!active) {
      lecteur.current?.pause()
      lecteur.current = null
      sourceEnCours.current = ''
      return
    }
    let annule = false
    const candidats = [slug ? `/musique-${slug}.mp3` : '', '/musique-plateau.mp3'].filter(Boolean)

    // On NE teste PLUS l'existence par un fetch avant de lire (la route .mp3 du moteur
    // renvoie le fichier entier). C'est l'élément <audio> lui-même qui sert de test : il
    // se déclare en erreur si le fichier manque, et on passe au candidat suivant.
    const essayer = (index: number) => {
      const url = candidats[index]
      if (annule || url === undefined) return
      if (sourceEnCours.current === url) return
      lecteur.current?.pause()
      const audio = new Audio(url)
      audio.loop = true
      audio.volume = lireVolumeMusique() / 100
      audio.addEventListener('error', () => {
        if (annule) return
        sourceEnCours.current = ''
        essayer(index + 1)
      })
      lecteur.current = audio
      sourceEnCours.current = url
      audio.play().catch(() => {
        // Autoplay refusé : on retentera au premier geste de l'utilisateur.
        if (lecteur.current === audio && !annule) {
          attendreUnGeste(() => {
            if (annule || lecteur.current !== audio) return
            void audio.play().catch(() => undefined)
          })
        }
      })
    }
    essayer(0)
    return () => {
      annule = true
    }
  }, [slug, active])

  // Le curseur du volume agit en direct sur la musique qui joue.
  useEffect(() => {
    const surVolume = () => {
      if (lecteur.current) lecteur.current.volume = lireVolumeMusique() / 100
    }
    window.addEventListener(EVENEMENT_VOLUME, surVolume)
    return () => window.removeEventListener(EVENEMENT_VOLUME, surVolume)
  }, [])

  useEffect(
    () => () => {
      lecteur.current?.pause()
      lecteur.current = null
    },
    [],
  )
}
