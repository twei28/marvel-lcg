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
const VOLUME = 0.25

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

export function useMusique(world: World | undefined, active: boolean): void {
  const lecteur = useRef<HTMLAudioElement | null>(null)
  const sourceEnCours = useRef<string>('')
  const slug = slugMechant(world)

  useEffect(() => {
    if (!active) {
      lecteur.current?.pause()
      lecteur.current = null
      sourceEnCours.current = ''
      return
    }
    let annule = false
    const candidats = [slug ? `/musique-${slug}.mp3` : '', '/musique-plateau.mp3'].filter(Boolean)

    // On NE teste PLUS l'existence par un fetch avant de lire. Le test envoyait
    // `Range: bytes=0-1`, mais la route .mp3 du moteur (web_server.ReadFile)
    // ignore les requêtes partielles : elle charge le fichier ENTIER en mémoire
    // et le renvoie en bloc. Sur une bande son d'une heure, cela faisait
    // télécharger le morceau complet juste pour savoir s'il était là — puis une
    // seconde fois pour l'écouter. C'est donc l'élément <audio> lui-même qui
    // sert de test : il se déclare en erreur si le fichier manque, et on passe
    // alors au candidat suivant. Un seul téléchargement, quoi qu'il arrive.
    const essayer = (index: number) => {
      const url = candidats[index]
      if (annule || url === undefined) return
      if (sourceEnCours.current === url) return
      lecteur.current?.pause()
      const audio = new Audio(url)
      audio.loop = true
      audio.volume = VOLUME
      audio.addEventListener('error', () => {
        if (annule) return
        sourceEnCours.current = ''
        essayer(index + 1)
      })
      lecteur.current = audio
      sourceEnCours.current = url
      // L'autoplay peut être refusé tant que la page n'a pas été cliquée :
      // dans ce cas on retentera au prochain monde reçu.
      audio.play().catch(() => {
        sourceEnCours.current = ''
      })
    }
    essayer(0)
    return () => {
      annule = true
    }
  }, [slug, active, world])

  useEffect(
    () => () => {
      lecteur.current?.pause()
      lecteur.current = null
    },
    [],
  )
}
