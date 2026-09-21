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
// domaine public placé devant les tables.
//
// ⚠ ET LA TENTATION, PARTOUT ICI, EST DE RÉDUIRE À DEUX CE QUI EN FAIT TROIS.
// « C'est fermé / ce n'est pas fermé » est faux : le site révoque le mot de
// passe et lance l'extinction AVANT de répondre, donc son silence ne prouve
// rien — sinon qu'on ne sait pas. Chaque fonction de ce fichier garde donc
// une troisième issue, et refuse d'affirmer sur elle.

/** L'adresse publique du site, et si on la connaît seulement. */
export type Site = {
  /** Faux tant que la lecture n'a pas abouti. Ce n'est PAS « aucun site ». */
  connu: boolean
  /** Vide quand le moteur tourne sans site, ou quand on ne sait pas. */
  url: string
}

/**
 * Au-delà, on cesse d'attendre l'adresse du site.
 *
 * ⚠ ELLE EST LUE DANS LE CHEMIN D'UN CLIC. Sans plafond, un moteur qui traîne
 * laisse le `fetch` pendu, la fenêtre de confirmation ne s'ouvre jamais, et le
 * bouton « Menu » paraît mort — au moment précis où ça rame, qui est souvent
 * celui où l'on cherche à partir.
 */
export const PLAFOND_LECTURE_SITE_MS = 2000

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

/**
 * L'accueil du site, déduit de l'adresse courante.
 *
 * Le plateau est servi depuis `pN.<domaine>` : on retire le sous-domaine et
 * l'on obtient le site. C'est le dernier recours quand personne n'a su nous
 * dire où aller — et le seul qui marche encore quand le moteur est mort.
 */
export function lienAccueil(): string {
  const morceaux = window.location.hostname.split('.')
  const parent = morceaux.length > 2 ? morceaux.slice(1).join('.') : window.location.hostname
  return `${window.location.protocol}//${parent}/`
}

/**
 * Lit l'adresse publique du site auprès du moteur.
 *
 * Le moteur la connaît (`site_url`, renseignée par l'orchestrateur) et la rend
 * à tous les joueurs : ce n'est ni un privilège ni un secret, c'est l'adresse
 * par laquelle tout le monde est entré. Elle ne change pas de la vie d'une
 * page : on la lit une fois, au montage.
 *
 * ⚠ UN ÉCHEC N'EST PAS « AUCUN SITE ». Les confondre rétablissait le défaut
 * d'origine en silence : un hoquet réseau faisait passer l'hôte pour un joueur
 * local, il voyait l'ancienne fenêtre, partait, et la table restait debout
 * avec l'ancienne partie dedans. Personne n'aurait pu le savoir.
 */
export async function lireLeSite(plafondMs = PLAFOND_LECTURE_SITE_MS): Promise<Site> {
  const arret = new AbortController()
  const minuterie = window.setTimeout(() => arret.abort(), plafondMs)
  try {
    const reponse = await fetch('/get_site_url', { signal: arret.signal })
    if (!reponse.ok) return { connu: false, url: '' }
    const lu = (await reponse.json()) as { url?: unknown }
    return { connu: true, url: typeof lu?.url === 'string' ? lu.url : '' }
  } catch {
    return { connu: false, url: '' }
  } finally {
    window.clearTimeout(minuterie)
  }
}

/** Ce que la fenêtre de confirmation doit annoncer. */
export type Nature =
  /** La table va disparaître, avec les autres joueurs dedans. */
  | 'fermeture'
  /** Elle va peut-être disparaître : on n'a pas pu le vérifier. */
  | 'incertain'
  /** Ce joueur ne ferme rien : il change d'écran, comme avant. */
  | 'simple'

/**
 * Ce clic va-t-il faire DISPARAÎTRE la table ?
 *
 * ⚠ CE N'EST PAS UNE AUTORISATION, c'est ce qu'on ANNONCE. L'autorisation est
 * dans le moteur, cookie de siège en main (`/quitter_la_table`, réservée au
 * siège 0). Ici on choisit seulement le texte de la confirmation : promettre
 * la fermeture à un invité serait un mensonge, et lui annoncer les autres
 * joueurs déconnectés, une frayeur pour rien.
 *
 * ⚠ ET « JE NE SAIS PAS » EST UNE RÉPONSE À PART ENTIÈRE. `site.connu` faux ne
 * veut pas dire « partie locale » : il veut dire que la lecture n'a pas
 * abouti. Le joueur mérite de l'apprendre plutôt que de partir sur une
 * apparence de normalité.
 */
export function natureDuDepart({
  siege,
  spectateur,
  site,
}: {
  siege: number
  spectateur: boolean
  site: Site
}): Nature {
  if (spectateur || siege !== 0) return 'simple'
  if (!site.connu) return 'incertain'
  // Le moteur a répondu « pas de site » : c'est la partie locale, où personne
  // ne tient d'emplacement et où `/prepare.html` reste vivant.
  return site.url === '' ? 'simple' : 'fermeture'
}

/** Ce qu'il est advenu de la table. */
export type Depart = {
  issue:
    /** Le site a confirmé, et a dit où aller. */
    | 'fermee'
    /** Il n'y avait rien à fermer : partie locale. Rien n'a bougé. */
    | 'sans-site'
    /** Le moteur a dit non : ce siège n'est pas celui de l'hôte. Rien n'a bougé. */
    | 'refusee'
    /** On ne sait pas. ⚠ Surtout ne rien affirmer là-dessus. */
    | 'inconnue'
  /** Où aller, quand quelqu'un a su le dire. */
  url: string
}

/**
 * Demande au moteur de fermer la table, et rend ce qu'il en est.
 *
 * ⚠ L'ISSUE INCONNUE EST LA RAISON D'ÊTRE DE CETTE FONCTION. Écrire « rien
 * n'a été détruit » sur un silence serait affirmer le faux : `/api/eteindre`
 * révoque le mot de passe et lance l'extinction AVANT de répondre, et il n'y a
 * aucun chemin d'abandon de son côté. Passé le plafond de dix secondes du
 * moteur, la table disparaît quand même. Proposer alors « rester sur la
 * partie » enverrait le joueur sur un moteur condamné.
 *
 * ⚠ ET UNE FERMETURE SANS ADRESSE N'EST PAS UNE FERMETURE ANNONCÉE : c'est
 * une issue inconnue de plus. Pas de destination, pas d'affirmation.
 */
export async function fermerLaTable(): Promise<Depart> {
  try {
    const reponse = await fetch('/quitter_la_table', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: '{}',
    })
    // 403 : le seul cas où le moteur nous dit lui-même que rien n'a bougé.
    if (!reponse.ok) return { issue: 'refusee', url: '' }
    const lu = (await reponse.json()) as { issue?: unknown; url?: unknown }
    const url = typeof lu?.url === 'string' ? lu.url : ''
    if (lu?.issue === 'sans-site') return { issue: 'sans-site', url: '' }
    if (lu?.issue === 'fermee' && url) return { issue: 'fermee', url }
    return { issue: 'inconnue', url }
  } catch {
    // Moteur injoignable. Il a très bien pu relayer l'appel avant de mourir :
    // on n'en sait rien, et c'est exactement ce qu'on rend.
    return { issue: 'inconnue', url: '' }
  }
}
