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

    const essayer = async () => {
      for (const url of candidats) {
        if (annule) return
        if (sourceEnCours.current === url) return
        try {
          const reponse = await fetch(url, { method: 'GET', headers: { Range: 'bytes=0-1' } })
          if (!reponse.ok) continue
          if (annule) return
          lecteur.current?.pause()
          const audio = new Audio(url)
          audio.loop = true
          audio.volume = VOLUME
          lecteur.current = audio
          sourceEnCours.current = url
          // L'autoplay peut être refusé tant que la page n'a pas été cliquée :
          // dans ce cas on retentera au prochain monde reçu.
          audio.play().catch(() => {
            sourceEnCours.current = ''
          })
          return
        } catch {
          /* fichier absent : candidat suivant */
        }
      }
    }
    void essayer()
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
