// Le geste sur une carte, en portrait : TAP pour lire, RE-TAP pour fermer,
// APPUI LONG pour jouer.
//
// Choix de l'utilisateur le 11/09/2026. Le tap est reversible et n'engage
// rien : sur un telephone, une carte de 96 px se joue autrement du doigt qu'a
// la souris, et ouvrir pour lire doit rester gratuit. Le jeu, lui, demande une
// intention — d'ou l'appui long, que `useAppuiLong` porte deja.
//
// La bascule est isolee ici, pure, parce que c'est la seule regle qu'on peut
// se tromper sans qu'un test de composant ne le voie.

/** Ce que porte le geste : quelle carte est ouverte, et comment la taper. */
export type GesteCarte = {
  ouverte: string | undefined
  taper: (id: string) => void
  fermer: () => void
}

/** L'identifiant ouvert apres un tap sur `tapee`. */
export function prochaineOuverte(ouverte: string | undefined, tapee: string): string | undefined {
  return ouverte === tapee ? undefined : tapee
}
