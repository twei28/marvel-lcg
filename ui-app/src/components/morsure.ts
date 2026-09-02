// Marqueur de MORSURE : l'ennemi tenu par un heros qui s'accroche (Alligator
// Loki, Lock Jaws). Le moteur le dit par `info.held_by_hero` (numero du
// joueur, 0 = personne) sur l'ennemi et `info.attached_to_enemy` sur le heros.
//
// L'illustration est fournie par l'utilisateur (02/09/2026) : l'alligator
// tete en bas, contour vert fluo, qu'on accroche au bord DROIT de la carte
// mordue. Elle est rognee et ramenee a 189x600 (21 ko) : elle s'affiche haute
// d'environ 1,15 largeur de carte, donc 600 px de source suffisent a rester
// nette en ecran haute densite.
//
// ⚠ ELLE DOIT ETRE INLINEE. Le serveur du jeu ne sert que .html / .js / .css
// (liste blanche de web_server.py) : un .png depose dans public/app renvoie
// silencieusement une image « no image ». `assetsInlineLimit: () => true`
// (vite.config.ts) transforme donc cet import en data URI, et
// `npm run verifier-sortie` echoue si un fichier image sortait quand meme.
import morsure from './morsure/morsure.png'

export const IMAGE_MORSURE: string | null = morsure
