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

/**
 * @param silence Le voile d'ouverture est EN PLACE : on ne joue rien.
 *
 * ⚠ LE SILENCE DE L'OUVERTURE VAUT AUSSI POUR LES SONS (spec du 15/09/2026,
 * « aucun son pendant la mise en place »). Le plateau appelle ce hook avant
 * son retour anticipe du voile — il le faut, les hooks ne se sautent pas — et
 * chaque trame de mise en place portant un `sound_name` etait donc jouee
 * derriere le voile. Parametre OPTIONNEL : les autres appelants ne changent
 * pas.
 *
 * ⚠ La porte est posee APRES `dernierRenderJoue`, comme celle d'`actif` : une
 * trame avalee sous le voile est avalee pour de bon, et ne repart pas en
 * rafale au moment ou la table apparait.
 */
export function useSons(
  monde: World | undefined,
  actif: boolean,
  joueurInterroge: boolean,
  silence = false
) {
  useEffect(() => {
    if (!monde || monde.render_id === dernierRenderJoue) return
    dernierRenderJoue = monde.render_id

    if (!actif) return
    if (silence) return
    if (document.visibilityState !== 'visible') return

    const nom = monde.sound_name
    if (!nom) return
    // Comme l'original : pas de son pendant qu'on attend NOTRE decision (le
    // rendu se repete tant que la question est ouverte), sauf le gong de phase.
    if (joueurInterroge && nom !== 'phase') return
    jouer(nom)
  }, [monde, monde?.render_id, actif, joueurInterroge, silence])
}
