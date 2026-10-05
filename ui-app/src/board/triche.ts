// triche.ts — le canal du mode Bac à sable.
//
// Toutes les interventions passent par `/sandbox_command`, qui n'accepte que
// des appels `Puzzle.<methode>` : le serveur rejette tout le reste à l'analyse
// syntaxique, donc aucun code arbitraire ne circule.
//
// LES CARTES SONT VISÉES PAR IDENTIFIANT D'OBJET, jamais par nom. Le moteur
// accepte les deux (`FindOrCreateFace`), mais viser par nom a deux défauts :
// deux cartes homonymes sont indiscernables, et un nom introuvable fait
// FABRIQUER une carte détachée au lieu d'échouer — ce qui produisait des
// doublons fantômes dans l'ancienne console. L'identifiant, lui, désigne
// exactement la carte qu'on a sous les yeux.

/** Une intervention envoyée, telle qu'on la raconte dans l'historique. */
export type Intervention = {
  /** Ce qu'on lit dans le journal : « Soigne 3 sur Rhino ». */
  libelle: string
  /** Vrai si le moteur a accepté. */
  reussi: boolean
}

async function envoyer(commandes: string[]): Promise<boolean> {
  try {
    const reponse = await fetch('/sandbox_command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ commands: commandes }),
    })
    return reponse.ok
  } catch {
    return false
  }
}

/** Échappe une chaîne pour l'insérer dans une commande Python. */
function texte(valeur: string): string {
  return `'${valeur.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}'`
}

// --- Interventions sur une carte -------------------------------------------

export const soigner = (id: number, valeur: number) =>
  envoyer([`Puzzle.Heal(${id}, ${valeur})`])

export const blesser = (id: number, valeur: number) =>
  envoyer([`Puzzle.Damage(${id}, ${valeur})`])

export const redresser = (id: number) => envoyer([`Puzzle.Ready(${id})`])
export const incliner = (id: number) => envoyer([`Puzzle.Exhaust(${id})`])
export const defausser = (id: number) => envoyer([`Puzzle.Discard(${id})`])
export const retirer = (id: number) => envoyer([`Puzzle.Remove(${id})`])
export const retourner = (id: number) => envoyer([`Puzzle.Flip(${id})`])

export const rendreConfus = (id: number) => envoyer([`Puzzle.Confuse(${id})`])
export const assommer = (id: number) => envoyer([`Puzzle.Stun(${id})`])
export const rendreCoriace = (id: number) => envoyer([`Puzzle.Tough(${id})`])

export const poserMenace = (id: number, valeur: number) =>
  envoyer([`Puzzle.PlaceThreat(${id}, ${valeur})`])

export const fixerMenace = (id: number, valeur: number) =>
  envoyer([`Puzzle.SetThreat(${id}, ${valeur})`])

export const poserCompteur = (id: number, nom: string, taille: number) =>
  envoyer([`Puzzle.Counter(${id}, ${texte(nom)}, ${taille})`])

/** Pose (valeur positive) ou retire (négative) des jetons d'accélération. */
export const poserAcceleration = (id: number, valeur: number) =>
  envoyer([`Puzzle.Token(${id}, 'acceleration_token', ${valeur})`])

// --- Depuis les piles ------------------------------------------------------

/** Deck ou défausse du joueur -> la main. */
export const envoyerEnMain = (id: number) => envoyer([`Puzzle.Gain(${id})`])

/**
 * Pile Rencontre -> le plateau.
 *
 * `PutIntoPlay` laisse le MOTEUR décider de la destination : un sbire s'engage
 * avec le joueur, une manigance annexe se pose, une amélioration s'attache.
 * C'est le comportement voulu par défaut ; « placer ailleurs » passe par
 * `Reveal`, qui suit le cheminement normal d'une carte Rencontre révélée.
 */
export const mettreEnJeu = (id: number) => envoyer([`Puzzle.PutIntoPlay(${id})`])
export const reveler = (id: number) => envoyer([`Puzzle.Reveal(${id})`])

/** Remet une carte sur le dessus du deck du joueur. */
export const remettreDansLeDeck = (id: number) => envoyer([`Puzzle.PutIntoDeck(${id})`])

// --- Les gestes du mode manuel ---------------------------------------------
//
// Le mode manuel n'a plus de moteur pour conduire la partie : ces gestes sont
// l'échappatoire qui couvre tout ce que les gestes ci-dessus, pensés pour le
// bac à sable, ne visaient pas — n'importe quelle carte vers n'importe quelle
// pile, sans aucune vérification de règle. Les noms de pile sont ceux de
// `DeckType` côté moteur (`Puzzle.MoveTo`, `Puzzle.Shuffle`).

/** Envoie une carte dans n'importe quelle pile, sans aucune vérification. */
export const deplacerVers = (
  id: number,
  zone: string,
  position: 'Top' | 'Bottom' = 'Top'
) => envoyer([`Puzzle.MoveTo(${id}, ${texte(zone)}, ${texte(position)})`])

/** Remet toute une défausse dans son deck, puis mélange le deck (OCTGN : « Shuffle discard into deck »). */
export const remelangerDansLeDeck = (ids: number[], zoneDeck: string) =>
  envoyer([...ids.map((id) => `Puzzle.MoveTo(${id}, ${texte(zoneDeck)}, 'Top')`), `Puzzle.Shuffle(${texte(zoneDeck)})`])

/** Mélange une pile. */
export const melanger = (zone: string) => envoyer([`Puzzle.Shuffle(${texte(zone)})`])

/** Pose une amélioration ou un soutien sur une carte précise. */
export const attacher = (id: number, cible: number) =>
  envoyer([`Puzzle.Attach(${id}, ${cible})`])

/** Engage un sbire avec le joueur, ou l'en désengage s'il y est déjà. */
export const engager = (id: number) => envoyer([`Puzzle.Engage(${id})`])

/**
 * Fait apparaître sur la table une carte du catalogue qui n'était pas dans
 * la partie (tâche 6 du plan).
 *
 * MÊME COMMANDE que `deplacerVers(id, 'ProcessingArea')`, le geste qui sort
 * une carte d'une pile du MONDE (voir `CoucheTriche.tsx`, cas `'piocher'`) :
 * `Puzzle.MoveTo` fabrique la carte elle-même (`FindOrCreateFace`) quand le
 * nom ne désigne encore rien, donc un seul appel crée ET pose. Elle arrive en
 * zone de RÉSOLUTION, jamais « en jeu » directement — le brief proposait
 * `Puzzle.PutIntoPlay`, qui laisse le MOTEUR choisir la destination selon le
 * type de carte ; contraire à tout ce mode, où le moteur ne décide rien.
 * C'est au joueur de la déplacer ensuite avec les gestes qu'il a déjà.
 */
export const creerCarte = (cardId: string) =>
  envoyer([`Puzzle.MoveTo(${texte(cardId)}, ${texte('ProcessingArea')}, ${texte('Top')})`])

/**
 * Déclare la fin d'une partie manuelle : le moteur ne surveille plus rien, il
 * ne peut donc constater ni un vilain vaincu ni un complot débordé — c'est au
 * joueur de le faire à sa place (tâche 7 du plan).
 *
 * `Puzzle.Win()` / `Puzzle.Lose()`, PAS `Puzzle.End(message)` — le brief de
 * cette tâche proposait ce dernier, mais il ne fait que publier une ligne
 * dans le journal du moteur (`Notify.Game`, `game/puzzle/puzzle.py`) : il ne
 * touche jamais `world.game_over`. `Win`/`Lose` (ajoutés le 19/09/2026, même
 * fichier) passent par `Worlds.SetGameOver`, LE MÊME chemin qu'une vraie
 * victoire de scénario : `game_over`, `players_won` s'écrivent, le carnet de
 * campagne s'ouvre comme d'habitude, et surtout `World.ManualLoop`
 * (`while not self.is_game_over`, `game/world/world.py`) rend enfin la main —
 * rien d'autre ne fait sortir cette boucle.
 *
 * Aucune confirmation ici : elle est déjà passée, côté `FinManuelle`, avant
 * l'appel.
 *
 * ⚠ CE GESTE SE RATTRAPE (correction ronde 1, contrairement à ce qu'un
 * commentaire précédent affirmait ici même) : le Ctrl+Z du mode rejoue la
 * partie moins son dernier geste, fin de partie déclarée comprise — voir
 * `annulerDernierGeste` ci-dessous et le test qui le prouve dans
 * `CoucheTriche.test.tsx`. La confirmation de `FinManuelle` ne protège donc
 * pas d'un geste irréversible ; elle évite seulement de déclencher par
 * mégarde le rejeu complet (une à deux secondes) qui permettrait d'y
 * revenir.
 */
export const declarerFin = (gagne: boolean) => envoyer([`Puzzle.${gagne ? 'Win' : 'Lose'}()`])

/** « Vaincre ce stade » (OCTGN) : le méchant passe au stade suivant, par le moteur. */
export const avancerLeMechant = () => envoyer(['Puzzle.AdvanceVillain()'])

/** « Manigance terminée » (OCTGN) : la manigance principale passe à l'étape suivante. */
export const avancerLaManigance = () => envoyer(['Puzzle.AdvanceMainScheme()'])

/**
 * Ctrl+Z : retire le dernier geste et rejoue la partie sans lui.
 *
 * Route distincte de `/sandbox_command` : ce n'est pas une commande
 * `Puzzle.*`, mais une reconstruction complète (mise en place puis rejeu de
 * tous les gestes moins le dernier), qui prend une à deux secondes. Rend 409
 * hors partie manuelle ou quand il n'y a rien à annuler — un refus, pas une
 * panne, mais le canal ne distingue de toute façon que « accepté » ou pas.
 */
export async function annulerDernierGeste(): Promise<boolean> {
  try {
    const reponse = await fetch('/manuel_undo', { method: 'POST' })
    return reponse.ok
  } catch {
    return false
  }
}

// --- La pause manuelle EN COURS DE PARTIE (tâche 3) -------------------------

/**
 * Bascule la pause manuelle EN COURS DE PARTIE, route `POST /manuel_pause`.
 *
 * Route DISTINCTE de `/sandbox_command` : on n'appelle donc pas `envoyer()`,
 * qui n'accepte que des `Puzzle.<methode>` — mais on reprend le même moule
 * (fetch, try/catch, retour booléen) pour ne pas ouvrir un second style
 * d'appel réseau dans ce fichier.
 *
 * ⚠ AUCUN CHAMP « QUI » (ronde de correction 1, tâche 3). Une version
 * précédente envoyait `qui: ''` : le SEUL endroit qui connaît le pseudo du
 * joueur courant côté plateau, `salon.ts` (`lireSalon().pseudo`), n'a plus
 * aucun consommateur depuis que le tchat a quitté la table (commit
 * bb0c8051, 12/09/2026, demande explicite de l'utilisateur), et un champ
 * que l'appelant enverrait TOUJOURS vide est un chemin mort : le bandeau ne
 * dirait alors jamais que « quelqu'un ». Le SERVEUR détermine désormais
 * lui-même qui a parlé, à partir du siège que la requête prouve tenir
 * (`nom_du_heros_qui_parle`, `server_base.py`), et pose le nom du héros de
 * ce siège — il dit plus aux autres joueurs qu'un pseudo de toute façon
 * hors d'atteinte ici.
 */
export async function basculerPause(actif: boolean): Promise<boolean> {
  try {
    const reponse = await fetch('/manuel_pause', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ actif }),
    })
    return reponse.ok
  } catch {
    return false
  }
}

// --- Passer la question fautive EN COURS DE PARTIE (tâche 5) ---------------

/**
 * Résultat de `passerLaQuestion` : soit la question a été passée, soit le
 * moteur l'a refusé avec un CODE STABLE (jamais une phrase -- même
 * convention que `failure_reason`/`NormaliserLeMotif`, controller.py : le
 * moteur ne parle pas la langue du joueur, `BandeauPause.tsx` écrit la
 * phrase). `'reseau'` distingue un ECHEC DE LA REQUÊTE ELLE-MÊME (offline...)
 * d'un refus DÉLIBÉRÉ du moteur -- les deux s'affichent, mais rien ne doit
 * les confondre dans un rapport de bug.
 */
export type ResultatPasser = { ok: true } | { ok: false; code: string }

/**
 * Passe la question EN COURS que le moteur reposerait à l'identique après
 * une pause, route `POST /manuel_passer` (échappatoire de dernier recours,
 * tâche 5) -- sur le modèle exact de `basculerPause` ci-dessus (aucun corps,
 * comme `/manuel_undo`).
 *
 * ⚠ N'INVENTE RIEN ICI NON PLUS : cette fonction ne fait que relayer le
 * verdict du serveur (`DeviceManager.PasserQuestionCourante`,
 * engine/device/manager/base.py), qui lui-même n'accepte que ce que le
 * moteur offrait déjà (`show_cancel`). Un échec réseau rend `'reseau'`,
 * jamais un succès silencieux.
 */
export async function passerLaQuestion(): Promise<ResultatPasser> {
  try {
    const reponse = await fetch('/manuel_passer', { method: 'POST' })
    if (reponse.ok) return { ok: true }
    const corps = (await reponse.json().catch(() => ({}))) as { error?: string }
    return { ok: false, code: corps.error ?? 'inconnu' }
  } catch {
    return { ok: false, code: 'reseau' }
  }
}

// --- Reprendre en Auto une partie COMMENCEE en manuel ------------------------

/** Où le moteur reprend la main après une partie commencée en manuel. */
export type PhaseDeReprise = 'heros' | 'mechant' | 'tour'

/**
 * Rend la table au moteur, à la phase indiquée, route `POST /manuel_reprise`.
 * Même moule que `passerLaQuestion` : un refus du moteur rend son CODE STABLE
 * (jamais une phrase), un échec de la requête rend `'reseau'`.
 */
export async function reprendreEnAuto(phase: PhaseDeReprise): Promise<ResultatPasser> {
  try {
    const reponse = await fetch('/manuel_reprise', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phase }),
    })
    if (reponse.ok) return { ok: true }
    const corps = (await reponse.json().catch(() => ({}))) as { error?: string }
    return { ok: false, code: corps.error ?? 'inconnu' }
  } catch {
    return { ok: false, code: 'reseau' }
  }
}
