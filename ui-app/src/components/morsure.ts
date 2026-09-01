// Marqueur de MORSURE : l'ennemi tenu par un heros qui s'accroche (Alligator
// Loki, Lock Jaws). Le moteur le dit par `info.held_by_hero` (numero du
// joueur, 0 = personne) sur l'ennemi et `info.attached_to_enemy` sur le heros.
//
// L'image est PLUGGABLE : tant qu'aucun PNG n'est fourni, ScanCard dessine une
// pastille texte « Mordu ». Pour brancher l'illustration (une carte / un
// visuel a poser sur la carte mordue), deposer le fichier dans
// `src/components/morsure/morsure.png` et remplacer les deux lignes ci-dessous
// par :
//
//   import morsure from './morsure/morsure.png'
//   export const IMAGE_MORSURE: string | null = morsure
//
// Rien d'autre a toucher : ScanCard bascule seul du texte a l'image.
export const IMAGE_MORSURE: string | null = null
