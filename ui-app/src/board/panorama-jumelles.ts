// REGISTRE des cartes jumelles a illustration continue (decision du 16/10/2026).
//
// Deux cartes dont les scans se raccordent bord a bord (ex. `tl011` 14/15 et
// `tl012` 15/15, Katana de Leonardo) sont posees COTE A COTE, 14 a gauche et
// 15 a droite, a cote de la carte qui les porte (jamais glissees dessous),
// quel que soit l'ordre dans lequel le moteur les a mises en jeu. Elles restent
// deux cartes distinctes : etat, clic, cible et paiement propres a chacune.
//
// Ce sont des DONNEES, pas de la logique par carte : declarer une paire, c'est
// ajouter UNE ligne ci-dessous. Ne declarer que les paires dont l'image se
// raccorde reellement ET que l'utilisateur a confirmees une a une.
import type { ScanCardProps } from '../components/ScanCard'
import type { UniteAffichee } from './zones'
import type { WorldCard } from './world'

export type PaireJumelle = {
  /** Code de la carte dessinee a gauche (la 14). */
  gauche: string
  /** Code de la carte dessinee a droite (la 15). */
  droite: string
}

export const PAIRES_JUMELLES: readonly PaireJumelle[] = [
  { gauche: 'tl011', droite: 'tl012' }, // Katana de Leonardo (14/15 + 15/15)
  { gauche: 'tm011', droite: 'tm012' }, // Nunchuck de Michelangelo (14/15 + 15/15), confirmee le 16/10/2026
  { gauche: 'tr011', droite: 'tr012' }, // Sai de Raphael (14/15 + 15/15), confirmee le 16/10/2026
  { gauche: 'td011', droite: 'td012' }, // Bo et Shell de Donatello (14/15 + 15/15), confirmee le 16/10/2026
  { gauche: 'ta009', droite: 'ta010' }, // Kama d'Alopex (14/16 + 15/16), confirmee le 16/10/2026
  { gauche: 'tj009', droite: 'tj010' }, // Tekko-Kagi de Jennika (14/16 + 15/16), confirmee le 16/10/2026
  { gauche: 'pu005', droite: 'pu006' }, // The City + Never Sleeps (La ville ne dort jamais), confirmee le 23/10/2026 : deux ENVIRONNEMENTS posees sur la table, images recollees (.planning/mcdc-punisher/panorama-city.py)
]

/** Cote ou se dessine cette carte dans son panneau, ou `undefined` si elle n'est dans aucune paire. */
export type CotePanorama = 'gauche' | 'droite'

/**
 * La premiere paire declaree dont les DEUX cartes sont dans la liste (ce que
 * porte une meme carte). Une seule des deux : `undefined`, rendu normal.
 */
export function trouverPaire(cartes: readonly WorldCard[]): { gauche: WorldCard; droite: WorldCard } | undefined {
  for (const paire of PAIRES_JUMELLES) {
    const gauche = cartes.find((c) => c.card_id === paire.gauche)
    const droite = cartes.find((c) => c.card_id === paire.droite)
    if (gauche && droite) return { gauche, droite }
  }
  return undefined
}

/**
 * Decision du 20/10/2026 : au survol d'une moitie de paire jumelle SUR LA TABLE, quand les deux moities sont en
 * jeu, l'apercu agrandi montre les deux, collees bord a bord, avec leur libelle et leur encadre de regle. Faux =
 * ancien comportement (apercu d'UNE carte). Le code de l'ancien comportement reste en place derriere ce drapeau.
 */
export const APERCU_JUMELLES_DOUBLE = true

/** Une moitie telle que l'apercu double la dessine. */
export type ApercuJumelle = {
  carte: ScanCardProps
  panorama: CotePanorama
  statuts?: ScanCardProps[]
  raisons?: string[]
}

/**
 * Les deux moities (gauche puis droite) a montrer dans l'apercu de la carte `id`, ou `undefined` pour l'apercu d'UNE
 * carte. Lit la table TELLE QUE DESSINEE : seules les unites marquees `panorama` par `zones.ts` (les deux moities en
 * jeu, hors main) comptent. Une seule moitie en jeu, la main, une pile (defausse...), le constructeur ou la
 * galerie ne portent aucune unite panorama : `undefined`, apercu inchange.
 */
export function jumellesPourApercu(
  emplacements: readonly { groupes: readonly (readonly UniteAffichee[])[] }[],
  id: string
): [{ carte: ScanCardProps; panorama: 'gauche' }, { carte: ScanCardProps; panorama: 'droite' }] | undefined {
  for (const emplacement of emplacements) {
    for (const groupe of emplacement.groupes) {
      for (let rang = 0; rang + 1 < groupe.length; rang++) {
        const g = groupe[rang]
        const d = groupe[rang + 1]
        if (g.panorama !== 'gauche' || d.panorama !== 'droite') continue
        if (g.carte.id !== id && d.carte.id !== id) continue
        return [
          { carte: g.carte, panorama: 'gauche' },
          { carte: d.carte, panorama: 'droite' },
        ]
      }
    }
  }
  return undefined
}

/**
 * Cartes attachées qui se posent À CÔTÉ de leur porteur, en entier, au lieu de se glisser dessous (23/10/2026, demande de l'utilisateur :
 * une carte dont le compteur décide de la partie ne doit jamais être à moitié cachée). Même principe que les paires jumelles, pour UNE carte.
 * Creeping Corruption (Shadowland, sl072a/b) : ses compteurs « corruption » font perdre le joueur à 5.
 */
export const CARTES_A_COTE: readonly string[] = ['sl072a', 'sl072b']
