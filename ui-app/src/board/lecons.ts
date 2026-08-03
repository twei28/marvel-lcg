// lecons.ts — le contenu du mode Découverte, et rien d'autre.
//
// Module PUR : aucun DOM, aucun React, aucun composant importé. Il se teste
// sous Node (ui-app/outils/verifier-lecons.mjs), comme libelles-cible.ts.
//
// ⚠️ Les leçons NOMMENT des cartes précises parce que la partie est FIGÉE
// (Spider-Man contre Rhino, seed 42). Ce postulat est protégé par
// `tools/test_seed_tutoriel.py`. Si ce test tombe, ce sont les textes d'ici
// qu'il faut relire, avant de toucher aux valeurs attendues du test.
//
// Une leçon ne désigne JAMAIS une carte par sa position dans la main : l'ordre
// d'affichage dépend de ce que le joueur a déjà joué.

import { t } from './langue'
import type { World, WorldCard } from './world'

/** Ce qu'on retient au DÉBUT d'une leçon, pour mesurer une variation. */
export type Repere = {
  pvVilain: number
  menacePrincipale: number
  pvIdentite: number
  round: number
  cartesEnMain: string[]
}

export type Lecon = {
  id: string
  titre: string
  texte: string
  /** Vrai si la mission ne se détecte pas et s'enchaîne au clic. */
  manuelle?: boolean
  /** Vrai quand la mission est remplie. Lit l'état, ne modifie rien. */
  accomplie: (monde: World, repere: Repere) => boolean
}

const nombre = (valeur: unknown): number => (typeof valeur === 'number' ? valeur : 0)

/* ---------------- Lectures de l'état ---------------- */
// Toutes tolèrent des zones absentes : au tout début d'une partie, plusieurs
// d'entre elles sont encore vides.

function identite(monde: World): WorldCard | undefined {
  return monde?.players?.[0]?.area_hero?.[0]
}

function pvVilain(monde: World): number {
  return nombre(monde?.area_villain?.[0]?.info?.health)
}

function menacePrincipale(monde: World): number {
  return nombre(monde?.area_schemes_main?.[0]?.info?.k_threat)
}

function pvIdentite(monde: World): number {
  return nombre(identite(monde)?.info?.health)
}

function mainCartes(monde: World): string[] {
  return (monde?.players?.[0]?.hand_cards ?? []).map((carte) => carte.card_id)
}

export function prendreRepere(monde: World): Repere {
  return {
    pvVilain: pvVilain(monde),
    menacePrincipale: menacePrincipale(monde),
    pvIdentite: pvIdentite(monde),
    round: nombre(monde?.round_id),
    cartesEnMain: mainCartes(monde),
  }
}

/* ---------------- Les leçons ---------------- */

export const LECONS: Lecon[] = [
  {
    id: 'forme-heros',
    titre: t('Deviens Spider-Man'),
    texte: t('Tu commences en Peter Parker, ton identité civile. En civil on récupère et on prépare, mais on ne se bat pas. Clique sur ta carte d’identité, puis choisis de changer de forme.'),
    accomplie: (monde) => identite(monde)?.card_type === 'Hero',
  },
  {
    id: 'jouer-carte',
    titre: t('Joue ta première carte'),
    texte: t('Joue « Coup de pied volant ». Pour la payer, tu défausses d’autres cartes de ta main : chaque carte vaut une ressource, quelle qu’elle soit. Tout se paie comme ça dans ce jeu.'),
    accomplie: (monde, repere) =>
      repere.cartesEnMain.includes('01005') && !mainCartes(monde).includes('01005'),
  },
  {
    id: 'attaquer',
    titre: t('Frappe Rhino'),
    texte: t('Ton héros peut attaquer une fois par tour. Clique sur Spider-Man, choisis Attaque, puis Rhino. Ta carte s’incline : c’est le signe qu’elle a déjà servi ce tour-ci.'),
    accomplie: (monde, repere) => pvVilain(monde) < repere.pvVilain,
  },
  {
    id: 'contrer',
    titre: t('Retire 2 menaces'),
    texte: t('La manigance principale monte à chaque tour. Si elle se remplit, la partie est perdue, même si Rhino est au plus mal. Contre-la pour faire redescendre la menace.'),
    accomplie: (monde, repere) => menacePrincipale(monde) <= repere.menacePrincipale - 2,
  },
  {
    id: 'finir-tour',
    titre: t('Termine ton tour'),
    texte: t('Regarde bien ce qui suit : Rhino t’attaque, la manigance monte, et une carte Rencontre t’est distribuée. C’est la phase du méchant, et elle arrive à chaque tour.'),
    accomplie: (monde, repere) => nombre(monde?.round_id) > repere.round,
  },
  {
    id: 'allie',
    titre: t('Appelle un allié'),
    texte: t('Les alliés attaquent et contrent à ta place, sans t’incliner. Ils encaissent un dégât chaque fois qu’ils agissent : ils sont là pour être dépensés, pas pour être gardés.'),
    accomplie: (monde) => (monde?.players?.[0]?.allies ?? []).length > 0,
  },
  {
    id: 'recuperer',
    titre: t('Reprends ton souffle'),
    texte: t('Repasse en Peter Parker et récupère des points de vie. Tu ne pourras plus attaquer ce tour-ci, mais Rhino ne t’attaquera pas non plus : il ira comploter à la place.'),
    accomplie: (monde, repere) =>
      identite(monde)?.card_type === 'AlterEgo' && pvIdentite(monde) > repere.pvIdentite,
  },
  {
    id: 'apercu',
    titre: t('Lis une carte'),
    texte: t('Survole n’importe quelle carte : elle s’agrandit sur le côté, avec ses mots-clés expliqués. Garde, Renfort, Déferlement : tout y est défini, tu n’as rien à retenir par cœur.'),
    manuelle: true,
    accomplie: () => false,
  },
  {
    id: 'reglages',
    titre: t('Le panneau ⚙'),
    texte: t('En haut à droite : animations, sons, musique, météo, succès. Tout est débrayable, rien ne t’est imposé.'),
    manuelle: true,
    accomplie: () => false,
  },
  {
    id: 'annuler',
    titre: t('Annuler une erreur'),
    texte: t('La touche U annule le dernier coup. Tu peux essayer sans crainte : rien n’est définitif tant que tu n’as pas terminé ton tour.'),
    manuelle: true,
    accomplie: () => false,
  },
  {
    id: 'historique',
    titre: t('L’historique'),
    texte: t('En bas, tout ce qui s’est passé est rejoué ligne à ligne. Quand tu ne comprends pas pourquoi quelque chose est arrivé, la réponse est là.'),
    manuelle: true,
    accomplie: () => false,
  },
]
