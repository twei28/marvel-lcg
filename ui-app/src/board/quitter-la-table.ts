// quitter-la-table.ts — « Quitter la partie » ferme la table, pour de bon.
//
// Pourquoi ce module existe (21/09/2026). Le bouton « Menu » du plateau ne
// faisait que `window.location.href = '/prepare.html'` : il ne disait rien au
// moteur, qui gardait son monde chargé et son emplacement pris. Or le salon
// des invités bascule vers le plateau dès que la table porte UNE partie,
// quelle qu'elle soit (`public/js/salon/app.js`) — son commentaire énonce
// l'hypothèse « la table est vide avant que l'hôte lance », et rien ne la
// rendait vraie. Les invités étaient donc expédiés sur l'ANCIENNE partie
// avant d'avoir choisi leur héros, et y restaient bloqués : deux soirées
// perdues les 19 et 20/09/2026, avec des amis qui attendaient.
//
// Fermer la table rend cette hypothèse vraie. Décision de l'auteur, énoncée
// telle quelle : la table disparaît, moteur éteint, emplacement rendu, mot de
// passe révoqué, invités déconnectés — quitte à rouvrir une table depuis le
// site pour rejouer.
//
// ⚠ LE DANGER DE CE GESTE EST LA PAGE MORTE. Une seconde après la fermeture,
// le moteur n'existe plus : `/prepare.html` et toute autre adresse qu'il sert
// meurent avec lui. C'est le SITE qui dit où atterrir, et lui seul connaît le
// domaine public placé devant les tables. Pas d'adresse, pas de fermeture
// annoncée (voir `fermerLaTable`).

/**
 * Quitte la page.
 *
 * Isolée ici pour une seule raison : c'est le seul geste du départ qui n'a
 * rien à décider, et le seul qu'un test ne peut pas laisser s'exécuter (jsdom
 * ne navigue pas). Le remplacer permet d'AFFIRMER sur la destination, ce qui
 * est justement ce qui casse quand la table s'éteint.
 */
export function atterrir(url: string): void {
  window.location.href = url
}

/** Ce que devient le joueur qui vient de cliquer. */
export type Depart = {
  /** La table a-t-elle vraiment été fermée ? */
  eteinte: boolean
  /** Où atterrir. Jamais une page du moteur qu'on vient d'éteindre. */
  url: string
}

const RIEN: Depart = { eteinte: false, url: '' }

/**
 * Ce clic va-t-il faire DISPARAÎTRE la table ?
 *
 * ⚠ CE N'EST PAS UNE AUTORISATION, c'est ce qu'on ANNONCE. L'autorisation est
 * dans le moteur, cookie de siège en main (`/quitter_la_table`, réservée au
 * siège 0). Ici on choisit seulement le texte de la confirmation : promettre
 * la fermeture à un invité serait un mensonge, et lui annoncer les autres
 * joueurs déconnectés, une frayeur pour rien.
 *
 * `urlSite` vide veut dire « aucun site derrière » : c'est la partie locale,
 * où personne ne tient d'emplacement et où `/prepare.html` reste vivant.
 */
export function laTableVaSeFermer({
  siege,
  spectateur,
  urlSite,
}: {
  siege: number
  spectateur: boolean
  urlSite: string
}): boolean {
  return !spectateur && siege === 0 && urlSite !== ''
}

/**
 * L'adresse publique du site, ou une chaîne vide s'il n'y en a pas.
 *
 * Le moteur la connaît (`site_url`, renseignée par l'orchestrateur) et la rend
 * à tous les joueurs : ce n'est ni un privilège ni un secret, c'est l'adresse
 * par laquelle tout le monde est entré.
 */
export async function urlDuSite(): Promise<string> {
  try {
    const reponse = await fetch('/get_site_url')
    if (!reponse.ok) return ''
    const lu = (await reponse.json()) as { url?: unknown }
    return typeof lu?.url === 'string' ? lu.url : ''
  } catch {
    // Un réseau qui hoquette ne doit pas laisser le joueur sans réponse : il
    // verra la confirmation prudente, et rien ne sera détruit.
    return ''
  }
}

/**
 * Demande au moteur de fermer la table, et rend l'endroit où aller.
 *
 * ⚠ LA GATE EST ICI : on ne déclare RIEN fermé sans adresse où atterrir. Le
 * moteur ne répond `eteinte` qu'avec l'adresse que le site lui a donnée ;
 * cette vérification-ci est le garde-fou du plateau, celui qui empêche
 * d'envoyer le joueur nulle part si la réponse arrivait tronquée. Pas de repli
 * inventé : un départ sans destination n'est pas un départ.
 */
export async function fermerLaTable(): Promise<Depart> {
  try {
    const reponse = await fetch('/quitter_la_table', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    })
    if (!reponse.ok) return RIEN
    const lu = (await reponse.json()) as { eteinte?: unknown; url?: unknown }
    const url = typeof lu?.url === 'string' ? lu.url : ''
    if (lu?.eteinte !== true || !url) return RIEN
    return { eteinte: true, url }
  } catch {
    // Moteur injoignable : rien n'a été détruit, et le plateau le dira.
    return RIEN
  }
}
