// noms-cartes-fr.ts — le nom francais des cartes, a l'AFFICHAGE seulement.
//
// Defaut signale par l'utilisateur le 11/09/2026 : la carte montrait
// « L'Effraction ! » sur son illustration francaise et « THE BREAK-IN! » en
// titre juste a cote.
//
// REGLE : le titre suit la langue des SCANS, pas celle de l'interface, et
// c'est le meme reglage qui commande les deux (scansFrActifs, pose par la
// bascule 🌐 et par le menu Options). Le joueur qui coupe les scans francais a
// la carte anglaise sous les yeux : lui ecrire un titre francais recreerait le
// meme desaccord, dans l'autre sens.
//
// PIEGE, et c'est la raison d'etre de ce module : `carte.name` est aussi une
// CLE DE LOGIQUE. Le moteur et le plateau comparent dessus, en anglais et en
// dur (« Taunting Presence », « Brute Force Barricade », « Light at the End »
// dans MenuActionsCarte.tsx, la recherche par nom dans zones.ts). Traduire
// `carte.name` a la source casserait ces comparaisons en silence. On ne touche
// donc JAMAIS au champ : on traduit au dernier moment, au rendu.
import { NOMS_FR } from './noms-fr'
import { scansFrActifs } from './scans-fr'

/** Ce que nomAffiche() a besoin de lire. Volontairement plus petit qu'un
    WorldCard : les piles et les apercus n'en fabriquent pas toujours un. */
export type CarteNommee = {
  card_id?: string
  name?: string
}

/**
 * Le nom a ECRIRE pour cette carte.
 *
 * Retombe sur le nom du moteur, sans bruit, dans les trois cas ou il n'y a
 * rien de mieux : scans francais coupes, carte fan-made (marvelcdb ne la
 * connait pas), ou VF identique a la VO (« Rhino », « Baron Zemo » ne sont pas
 * dans le dictionnaire, justement parce qu'il n'y a rien a traduire).
 */
export function nomAffiche(carte: CarteNommee): string {
  const brut = carte.name ?? ''
  if (!carte.card_id || !scansFrActifs()) return brut
  return NOMS_FR[carte.card_id] ?? brut
}
