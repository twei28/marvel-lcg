// Les ESSAIS : ce qui est livré en production mais réservé à un seul compte.
//
// Décidé le 14/09/2026 : « tu peux les déployer, mais actuellement ce n'est que
// pour moi. Si je valide la phase du méchant et après les nouvelles animations,
// tu pourras déployer pour tout le monde. »
//
// ⚠ C'EST LE SERVEUR QUI DÉCIDE, JAMAIS LE CLIENT. `/get_site_admin` ne rend
// une adresse que si `site_admin_url` est renseignée, ce que l'orchestrateur ne
// fait que pour la table de l'administrateur, et seulement si le client tient
// le siège 0. Même garde que `lien-admin.js` et que la page de relevé des
// illustrations, en service depuis le 14/09/2026.
//
// ⚠ ET C'EST UN CONFORT, PAS UNE SÉCURITÉ. Ce drapeau n'ouvre que des choix
// d'AFFICHAGE. Quelqu'un qui le forcerait ne verrait qu'un écran en chantier,
// sans rien casser ni lire quoi que ce soit de privé. À ne pas confondre avec
// `save_images_cartes`, dont l'écriture, elle, devait vraiment être fermée : là
// le serveur refuse (403), ici il se contente de ne pas proposer.
//
// ⚠ UNE SEULE REQUÊTE PAR PAGE. Le plateau se redessine à chaque rendu du
// moteur (plusieurs fois par seconde en pleine phase) : demander à chaque fois
// noierait le serveur pour une réponse qui ne change jamais de la partie.

/** La réponse, retenue pour toute la vie de la page. */
let promesse: Promise<boolean> | undefined

async function demander(): Promise<boolean> {
  try {
    const reponse = await fetch('/get_site_admin', { cache: 'no-store' })
    if (!reponse.ok) return false
    // ⚠ Le moteur a une route fourre-tout qui sert une IMAGE pour tout chemin
    // inconnu : une réponse 200 ne prouve donc pas que la route existe. Sur un
    // serveur d'avant cette route, `json()` échouerait sur un JPEG ; le `catch`
    // en dessous répond alors « pas d'essais », ce qui est le bon repli.
    const donnees = (await reponse.json()) as { url?: string }
    return Boolean(donnees?.url)
  } catch {
    // Moteur lancé à la main, hors ligne, route absente : pas d'essais. Le jeu
    // n'en dépend pas, il garde son comportement habituel.
    return false
  }
}

/**
 * Les essais sont-ils ouverts pour ce client ?
 *
 * Rend toujours la MÊME promesse : la question n'est posée qu'une fois.
 */
export function essaisOuverts(): Promise<boolean> {
  promesse ??= demander()
  return promesse
}

/** Pour les tests seulement : oublie la réponse retenue. */
export function oublierEssais(): void {
  promesse = undefined
}
