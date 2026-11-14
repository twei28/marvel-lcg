import { t } from './langue'

// UNE RECHERCHE S'OUVRE PAR SA PILE sur la table du PC (17/10/2026) : le deck ou la defausse ou sont les cartes cherchees
// brille avec ce qu'on y fait (« Chercher dans le paquet rencontre »), et c'est le clic sur la pile qui ouvre la fenetre.
//
// ⚠ SUR TELEPHONE, cette porte est introuvable (rapport du 26/10/2026, Safe House #30 du Winter Soldier) : le plateau en
// bandes ne dessine pas le deck de rencontre, qui est dans le tiroir « Piles ». Le joueur valide l'action, ne voit aucune
// porte, ne choisit aucun sbire : rien ne se passe, sans un mot. Quand UNE SEULE pile porte les cartes cherchees, on
// l'ouvre donc d'office sur telephone ; sur la table du PC, la regle du 17/10/2026 reste telle quelle. Avec plusieurs
// piles, le choix de la pile reste au joueur.

export type EntreePileAuto = {
  telephone: boolean
  /** Une action attend ses cibles ou sa confirmation. */
  rechercheEnCours: boolean
  /** Les piles qui portent des cartes cherchees : representant -> libelle. */
  piles: ReadonlyMap<number, string>
  /** La pile deja ouverte, s'il y en a une. */
  pileOuverte: number | undefined
}

/** La pile a ouvrir d'office, ou `undefined` quand il faut laisser le joueur la choisir. */
export function pileAOuvrirSeule({ telephone, rechercheEnCours, piles, pileOuverte }: EntreePileAuto): number | undefined {
  if (!telephone || !rechercheEnCours || pileOuverte !== undefined) return undefined
  if (piles.size !== 1) return undefined
  return piles.keys().next().value
}

/**
 * Rapport du 26/10/2026 (Suit Up de Laura Kinney, telephone) : « cherchez dans votre deck ET pile de defausse ». Des qu'un allie
 * est en defausse, DEUX piles portent des cartes cherchees ; la porte de chacune est cachee dans le tiroir « Piles », rien ne
 * s'ouvre et l'action est payee pour rien. Sur telephone, on ouvre donc TOUTES les cartes d'un coup, rangees par pile
 * (`groupeDeLaPile`). La table du PC garde sa regle du 17/10/2026 : c'est le clic sur la pile qui ouvre la fenetre.
 */
export function pilesToutesALaFois({ telephone, rechercheEnCours, piles, pileOuverte }: EntreePileAuto): boolean {
  return telephone && rechercheEnCours && pileOuverte === undefined && piles.size > 1
}

/** La nature d'une pile : ce qui la distingue pour le joueur, avant toute traduction. */
export type SorteDePile = 'deck' | 'defausse' | 'rencontre' | 'defausse-rencontre' | 'autre'

/** L'intitule d'un groupe de cartes dans le selecteur : un mot, la pile d'ou elles viennent. */
export function groupeDeLaPile(sorte: SorteDePile): string {
  switch (sorte) {
    case 'deck':
      return t('Deck')
    case 'defausse':
      return t('Défausse')
    case 'rencontre':
      return t('Paquet rencontre')
    case 'defausse-rencontre':
      return t('Défausse rencontre')
    default:
      return t('Pile de cartes')
  }
}

/**
 * Demande de l'utilisateur (26/10/2026) : quand l'action peut choisir dans PLUSIEURS piles (deck + defausse), cliquer sur
 * UNE d'elles ouvre la MEME fenetre, qui contient toutes les piles concernees. Avec une seule pile, c'est la pile cliquee.
 */
export function ouvertureDePile(piles: ReadonlyMap<number, string>, clic: number): { pile: number | undefined; toutes: boolean } {
  if (piles.size > 1) return { pile: undefined, toutes: true }
  return { pile: clic, toutes: false }
}

/**
 * Fermeture accidentelle (telephone) : la fenetre de choix se REDUIT sans annuler l'action. Tant que la recherche court et que la
 * fenetre est fermee, le choix est « en attente » : l'onglet « Piles » clignote et un bandeau propose de rouvrir.
 */
export function choixEnAttente({ rechercheEnCours, reduit }: { rechercheEnCours: boolean; reduit: boolean }): boolean {
  return rechercheEnCours && reduit
}

/** Pour chaque pile (cle), le nombre de cartes qu'on peut y choisir ; les piles sans carte choisissable sont omises. */
export function pilesChoisissables(
  piles: ReadonlyArray<{ cle: string; ids: ReadonlyArray<number> }>,
  idsChoisissables: ReadonlySet<number>
): Map<string, number> {
  const comptes = new Map<string, number>()
  for (const { cle, ids } of piles) {
    const n = ids.filter((id) => idsChoisissables.has(id)).length
    if (n > 0) comptes.set(cle, n)
  }
  return comptes
}
