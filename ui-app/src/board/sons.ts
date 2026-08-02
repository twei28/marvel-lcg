// Sons du moteur.
//
// Le moteur nomme un son par rendu (`world.sound_name` : "activate", "token",
// "phase"...). Les fichiers .wav correspondants sont servis a la racine
// (`/<nom>.wav`, resolus dans assets/sounds/ par le serveur). Le client
// original les joue a volume 0.2, uniquement quand l'onglet est visible et
// qu'aucun joueur n'est interroge — memes regles ici.
//
// L'autoplay navigateur peut refuser un son avant la premiere interaction :
// l'echec est silencieux (catch), le son suivant passera.

import { useEffect } from 'react'
import type { World } from './world'

const VOLUME = 0.2

/** Cache module : un element audio par fichier, rejoue depuis le debut. */
const cache = new Map<string, HTMLAudioElement>()
let dernierRenderJoue = -1

function jouer(nom: string) {
  let audio = cache.get(nom)
  if (!audio) {
    audio = new Audio(`/${nom}.wav`)
    audio.volume = VOLUME
    cache.set(nom, audio)
  }
  audio.currentTime = 0
  void audio.play().catch(() => undefined)
}

export function useSons(monde: World | undefined, actif: boolean, joueurInterroge: boolean) {
  useEffect(() => {
    if (!monde || monde.render_id === dernierRenderJoue) return
    dernierRenderJoue = monde.render_id

    if (!actif) return
    if (document.visibilityState !== 'visible') return

    const nom = monde.sound_name
    if (!nom) return
    // Comme l'original : pas de son pendant qu'on attend NOTRE decision (le
    // rendu se repete tant que la question est ouverte), sauf le gong de phase.
    if (joueurInterroge && nom !== 'phase') return
    jouer(nom)
  }, [monde, monde?.render_id, actif, joueurInterroge])
}
