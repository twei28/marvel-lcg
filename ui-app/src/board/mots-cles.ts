// Mots-cles du jeu et leurs definitions, pour les tooltips de l'apercu.
//
// Vocabulaire OFFICIEL de la traduction francaise FFG/Asmodee, verifie sur le
// Guide de Reference FR et le texte des cartes FR (fr.marvelcdb) le 2/8/2026.
// Attention aux faux-amis officiels : Surge = « Renfort », Overkill =
// « Deferlement », Stalwart = « Robuste », Steady = « Solide ».

import { t } from './langue'

export type MotCle = { nom: string; definition: string }

/** Cles de `desc` (cards.json) -> nom officiel FR + definition. */
const DEPUIS_DESC: Record<string, { nom: string; definition: string }> = {
  Guard: { nom: 'Garde', definition: 'Tant que ce sbire est engagé avec vous, vous ne pouvez pas attaquer le Méchant.' },
  Patrol: { nom: 'Patrouille', definition: 'Tant que ce sbire est engagé avec vous, vous ne pouvez pas contrer la manigance principale.' },
  Crisis: { nom: 'Crise', definition: 'Tant que cette manigance annexe est en jeu, les joueurs ne peuvent pas retirer de menace de la manigance principale.' },
  Hazard: { nom: 'Aléa', definition: 'Pendant la phase du Méchant, une carte Rencontre supplémentaire est attribuée par icône d’aléa en jeu.' },
  Acceleration: { nom: 'Accélération', definition: 'Ajoute de la menace supplémentaire sur la manigance principale pendant la phase du Méchant.' },
  Amplify: { nom: 'Amplification', definition: 'Chaque carte de boost retournée pendant une activation ennemie gagne une icône de boost par icône d’amplification en jeu.' },
  Peril: { nom: 'Péril', definition: 'En résolvant cette carte, vous ne pouvez pas demander l’aide des autres joueurs : résolvez-la seul.' },
  Surge: { nom: 'Renfort', definition: 'Après avoir résolu cette carte, le joueur s’attribue une carte Rencontre supplémentaire.' },
  Toughness: { nom: 'Ténacité', definition: 'Entre en jeu avec une carte d’état Tenace (les prochains dégâts sont prévenus).' },
  Steady: { nom: 'Solide', definition: 'Il faut DEUX cartes d’état du même type à ce personnage pour être réellement sonné ou désorienté.' },
  Stalwart: { nom: 'Robuste', definition: 'Ce personnage ne peut être ni sonné ni désorienté.' },
  Quickstrike: { nom: 'Coup Rapide', definition: 'Cet ennemi attaque le joueur dès qu’il s’engage avec lui (si ce joueur est en forme de héros).' },
  Retaliate: { nom: 'Riposte', definition: 'Après que ce personnage a été attaqué, il inflige X dégâts à l’attaquant.' },
  Villainous: { nom: 'Vilenie', definition: 'Quand ce sbire s’active, donnez-lui une carte de boost, comme au Méchant.' },
  Incite: { nom: 'Incitation', definition: 'Retournée comme carte de boost, ajoute X menaces sur la manigance principale.' },
  Restricted: { nom: 'Restreint', definition: 'Un joueur ne peut contrôler que deux cartes Restreint à la fois.' },
  Permanent: { nom: 'Permanent', definition: 'Commence en jeu et ne peut pas quitter le jeu.' },
  Victory: { nom: 'Victoire', definition: 'Une fois vaincue/déjouée, cette carte rejoint la pile de victoire et vaut ses points de victoire.' },
  Hinder: { nom: 'Entrave', definition: 'Entre en jeu avec X menaces par joueur posées dessus.' },
  Setup: { nom: 'Mise en place', definition: 'Commence la partie en jeu.' },
  Teamwork: { nom: 'Collaboration', definition: 'Deux personnages désignés peuvent s’incliner ensemble pour déclencher cette capacité.' },
  Alliance: { nom: 'Alliance', definition: 'N’importe quel joueur peut aider à payer cette carte.' },
}

/** Mots-cles qui vivent dans le TEXTE de la carte, pas dans `desc`. */
const DEPUIS_TEXTE: Record<string, { nom: string; definition: string }> = {
  Piercing: { nom: 'Perçant', definition: 'Cette attaque défausse TOUTES les cartes Tenace de la cible avant d’infliger les dégâts.' },
  Overkill: { nom: 'Déferlement', definition: 'Les dégâts en excès de cette attaque sont infligés au Méchant (depuis un sbire) ou à votre identité (depuis un allié).' },
  Ranged: { nom: 'À Distance', definition: 'Cette attaque ignore Riposte.' },
  Uses: { nom: 'Utilisations', definition: 'Entre en jeu avec X jetons ; quand le dernier est dépensé, défaussez cette carte.' },
  // Mot-cle MAISON du pack fan-made viv_vision (Rainy), imprime sur vv003
  // « Just a Phase » et sur aucune carte officielle. L'auteur ne le definit
  // nulle part : sans cette entree, le joueur lit un mot qui n'existe pas.
  // Definition de la liste communautaire « Marvel Champions Home Brew Master
  // List » ; detail complet dans docs/reference/mots-cles/breakthrough.md.
  Breakthrough: { nom: 'Percée', definition: 'Comme Déferlement, mais pour la menace : quand cette menée vide une manigance, la menée en excès est retirée d’une autre manigance de votre choix.' },
}

const REGEX_TEXTE: Array<[RegExp, string]> = Object.keys(DEPUIS_TEXTE).map((nom) => [
  new RegExp(`\\b${nom.toLowerCase()}\\b`),
  nom,
])

/**
 * Mots-cles d'une carte, depuis ses cles `desc` et son texte imprime.
 * Renvoie une liste ordonnee et dedoublonnee de {nom, definition}.
 */
export function motsClesDeCarte(
  desc: Partial<Record<string, string>> | undefined,
  texte: string | undefined
): MotCle[] {
  const trouves: MotCle[] = []
  const vus = new Set<string>()
  const pousser = (cle: string, nom: string, definition: string, valeur?: string) => {
    if (vus.has(cle)) return
    vus.add(cle)
    const suffixe = valeur && valeur !== '1' ? ` ${valeur}` : ''
    // Traduction au point de sortie : les données ci-dessus restent la source
    // FR, et le suffixe numérique (« Utilisations 2 ») reste hors du dictionnaire.
    trouves.push({ nom: `${t(nom)}${suffixe}`, definition: t(definition) })
  }

  for (const [cle, mot] of Object.entries(DEPUIS_DESC)) {
    const valeur = desc?.[cle]
    if (valeur !== undefined) pousser(cle, mot.nom, mot.definition, valeur)
  }
  if (desc?.Uses !== undefined) {
    pousser('Uses', DEPUIS_TEXTE.Uses.nom, DEPUIS_TEXTE.Uses.definition, desc.Uses.split(',')[0])
  }

  const minuscule = (texte ?? '').toLowerCase()
  if (minuscule) {
    for (const [regex, cle] of REGEX_TEXTE) {
      if (regex.test(minuscule)) pousser(cle, DEPUIS_TEXTE[cle].nom, DEPUIS_TEXTE[cle].definition)
    }
  }
  return trouves
}
