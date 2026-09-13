// « Mise a jour dans 7 minutes : sauvegarde ta partie. »
//
// Un deploiement fait `systemctl restart narwhal` : l'orchestrateur du site
// emporte tous ses moteurs avec lui, et TOUTE PARTIE EN COURS EST PERDUE.
// Jusqu'ici, le joueur decouvrait l'ardoise vide sans rien avoir vu venir. Ce
// bandeau lui donne le temps d'appuyer sur 💾 Save.
//
// ⚠ IL PASSE, IL NE S'INSTALLE PAS (demande de l'utilisateur, 13/09/2026).
// Une bande discrete en coin se regarde une fois puis ne se voit plus : c'est
// exactement ce qu'il ne faut pas pour un avertissement qu'on ne peut pas
// rattraper. Il prend donc TOUTE LA LARGEUR et le dixieme superieur de
// l'ecran, deux secondes, toutes les trente secondes. Entre deux passages
// l'ecran est entierement libre.
//
// Et il ne gene JAMAIS le jeu : `pointer-events: none` dans la feuille de
// style. Un clic le traverse et atteint la carte qui est dessous.
//
// Le texte vient du site, ecrit a la main dans /admin. Le DECOMPTE, lui, est
// calcule ici : le serveur n'envoie que les secondes restantes, jamais une
// heure absolue, parce que le navigateur d'un joueur n'est pas a l'heure du
// serveur et afficherait un compte a rebours faux.

import { t } from './langue'

export type BandeauAnnonceProps = {
  /** Le message, tel que le site l'a ecrit. */
  texte: string
  /** Secondes restantes avant l'echeance, deja decomptees par l'appelant. */
  secondes: number
}

/** « 7 minutes », « moins d'une minute ». Jamais « 0 minute », qui se lirait
 *  comme « c'est deja fini » alors qu'il reste quelques secondes pour agir. */
export function delaiLisible(secondes: number): string {
  const minutes = Math.floor(Math.max(0, secondes) / 60)
  if (minutes < 1) return t('moins d’une minute')
  if (minutes === 1) return t('1 minute')
  return `${minutes} ${t('minutes')}`
}

export function BandeauAnnonce({ texte, secondes }: BandeauAnnonceProps) {
  return (
    <div className="bandeau-annonce" role="alert">
      <span className="bandeau-annonce-delai">{delaiLisible(secondes)}</span>
      <span className="bandeau-annonce-texte">{texte}</span>
    </div>
  )
}
