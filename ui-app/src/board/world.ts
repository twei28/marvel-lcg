// Le contrat de /get_world, releve sur les 34 etats enregistres du jeu
// (public/js/fixtures/) et sur le runtime historique qui les consomme
// (public/js/marvel/descriptor.js). Rien n'est suppose ici.
//
// Ces types ne decrivent pas tout le descripteur : seulement ce que le plateau
// lit. Les champs absents restent absents, pas devines.

/** Une carte, telle que le moteur la decrit. Meme forme dans toutes les zones. */
export type WorldCard = {
  /** Identifiant d'objet de partie (« object_id » cote runtime). */
  id: number
  /** false = carte engagee (le runtique la penche). */
  is_ready: boolean
  /** false = posee face cachee sur la table (ou en main). */
  is_face_up: boolean
  /** Numeros de joueurs autorises a voir la face. Vide = personne. */
  visible_for_players: number[]
  /** != 0 : cette carte est attachee a la carte portant cet id. */
  bind_object_id: number
  name: string
  /** Compteurs et statistiques courants. Cles variables selon le type. */
  info: Partial<Record<string, number>>
  traits: Partial<Record<string, number>>
  buffs: Partial<Record<string, string>>
  card_id: string
  /** Identifiant d'image. Voir scanUrl() dans card-model.ts. */
  pic_id: string
  /** Images de dos possibles. Le runtime n'utilise que la premiere. */
  down_card_ids: string[]
  card_type: string
  cost: number
  /**
   * Identifiants des effets de RESSOURCE que porte cette carte. C'est par eux
   * qu'on paie : une option d'action liste les effets de ressource acceptes
   * (EffectDescriptor.target_payment[cible].payment), et cliquer une carte qui
   * porte l'un d'eux le depense. Voir ask.ts.
   */
  resources: number[]
}

/** Les zones qui appartiennent a un joueur. */
export type WorldPlayer = {
  /** Identite (Hero ou AlterEgo) puis ses ameliorations attachees. */
  area_hero: WorldCard[]
  allies: WorldCard[]
  supports: WorldCard[]
  player_deck: WorldCard[]
  player_discard_pile: WorldCard[]
  dealt_encounter_cards: WorldCard[]
  hand_cards: WorldCard[]
  /**
   * Zone Réserve du pack Brawn : hors jeu, 3 cartes au plus, mais jouables et
   * dépensables comme la main. Absente des sauvegardes d'avant le pack, et vide
   * pour tout autre héros : toujours la lire avec `?? []`.
   */
  reserve?: WorldCard[]
  /**
   * Les cartes de CE joueur en cours de résolution : un événement joué, une
   * traîtrise qu'il subit, le temps que son texte s'applique.
   *
   * ⚠ ABSENTE DES MOTEURS ANTÉRIEURS AU 15/09/2026, et c'est pour ça qu'elle
   * est optionnelle. Avant cette date le moteur fusionnait la zone de
   * résolution de chaque joueur avec celle du monde dans le seul
   * `World.area_processing`, et le plateau, ne sachant plus à qui la carte
   * était, la dessinait chez le méchant. Défaut signalé en jeu : « les cartes
   * que je joue se placent derrière le méchant avant d'aller à la défausse ».
   */
  area_processing?: WorldCard[]
  engaged_enemies: WorldCard[]
  set_aside_nemesis_sets: WorldCard[]
  set_aside_deck: WorldCard[]
  additional_deck: WorldCard[]
  additional_discard_pile: WorldCard[]
  obligations_area: WorldCard[]
  environment_area: WorldCard[]
  /** Chaine, et non liste : mesure faite sur une partie reelle (valeur ''). */
  resources: string
  is_eliminated: boolean
}

/**
 * Ce que TOUT fait du méchant porte, quel que soit son genre.
 *
 * Le journal du moteur (`WorldStat.RecordFaitMechant`, côté Python) raconte la
 * phase du méchant point par point : la menace du point 1, les activations du
 * point 2, la distribution du point 3, les révélations du point 4. Un fait par
 * événement, inscrit là où le moteur le produit.
 */
type FaitMechantCommun = {
  /**
   * Round auquel le fait a eu lieu. Absent des faits enregistrés par un
   * moteur pas encore mis à jour (ou d'une sauvegarde plus ancienne) : dans ce
   * cas, `etapesDeroule` garde le fait plutôt que de le jeter, quel que soit le
   * round demandé (mieux vaut une étape de trop qu'un déroulé muet).
   */
  round_id?: number
  /**
   * L'étape de la phase du méchant où le fait a eu lieu, dans les mêmes
   * termes que `World.phase`.
   *
   * Un vilain ne s'active pas qu'à l'étape des activations : une carte de
   * rencontre révélée peut le faire frapper une seconde fois. Sans cette
   * précision, cette attaque-là se rangeait sous « activations » et il
   * paraissait attaquer deux fois sans raison.
   */
  phase?: string
}

/**
 * Ce qu'une activation ennemie porte à ses DEUX temps.
 *
 * Une activation s'annonce avant de se résoudre : le moteur inscrit d'abord
 * une INTENTION à la déclaration (`etat: 'annonce'`), puis sa RÉSOLUTION
 * (`etat: 'resolu'`), qui remplace la première sous le même `activation_id`.
 * Entre les deux se tient la fenêtre où le joueur peut défendre ou jouer une
 * interruption : sans ce premier temps, le cartouche ne pouvait raconter qu'un
 * passé déjà résolu et le joueur ne voyait jamais le coup venir.
 */
type FaitActivationCommun = FaitMechantCommun & {
  genre: 'attaque' | 'manigance'
  /**
   * Le numéro de l'activation dans le round (`WorldStat.NouvelleActivation`).
   * Il LIE l'intention à sa résolution, et c'est lui qui donne son identité
   * stable à l'étape du cartouche : l'étape se complète sous les yeux du
   * joueur au lieu de changer de clé.
   *
   * Absent des faits d'un moteur pas encore mis à jour (ou d'une sauvegarde
   * plus ancienne) : l'étape retombe alors sur son ancienne identité.
   */
  activation_id?: number
  /** Carte qui a déclenché l'activation, vide quand c'est l'ennemi lui-même. */
  cause?: string
  auteur: string
  auteur_id: number
  cible: string
  cible_id: number
}

/**
 * L'INTENTION : « Klaw va attaquer Colossus ».
 *
 * Elle ne porte QUE ce que le moteur sait avant le coup. `subi`, `defense`,
 * `restant`, les boosts : aucun n'existe encore quand elle part, et les cartes
 * de boost ne sont même pas retournées. Un fait `annule` a exactement la même
 * forme : l'activation n'a pas eu lieu, donc elle n'a rien produit non plus.
 */
export type FaitActivationAnnonce = FaitActivationCommun & {
  etat: 'annonce' | 'annule'
  /**
   * Attaque (ou manigance) IMPRIMÉE, avant les cartes de boost et avant tout ce
   * qui renforce l'activation après la déclaration : c'est ce que le moteur
   * sait au moment où il annonce, et rien d'autre.
   *
   * Optionnelle, parce qu'une activation ANNULÉE n'en porte pas : la clôture
   * (`CanAttack.AnnulerActivation`) n'inscrit que de quoi identifier
   * l'activation qui n'a pas eu lieu. Le type l'exigeait, et mentait donc sur
   * la moitié des faits de cette forme.
   */
  base?: number
}

/**
 * La RÉSOLUTION, décomposée par le moteur au moment où il la calcule.
 *
 * `inflige = base + boost - defense`, et `subi` peut être plus petit encore
 * quand la cible absorbe autrement (résistance, PV insuffisants).
 *
 * `etat` est absent des faits d'un moteur antérieur aux deux temps : un fait
 * d'activation sans état est une résolution, ce qui est exactement ce qu'il
 * était.
 */
export type FaitActivationResolue = FaitActivationCommun & {
  etat?: 'resolu'
  /**
   * La valeur RÉELLEMENT calculée par le moteur avant la défense, boosts
   * déduits — jamais la valeur imprimée annoncée, qui ignore tout ce qui
   * renforce l'activation entre la déclaration et la résolution.
   */
  base: number
  /** Apport total des cartes de boost. */
  boost: number
  defense: number
  /** Ce qui a été porté, défense déduite. */
  inflige: number
  /** Ce que la cible a réellement encaissé. */
  subi: number
  /** PV ou menace de la cible après coup. Absent si la cible n'en a pas. */
  restant?: number | null
  boosts: { nom: string; id: number; apport: number }[]
}

export type FaitActivation = FaitActivationAnnonce | FaitActivationResolue

/**
 * La menace du POINT 1, posée par la règle du jeu sur une manigance principale.
 *
 * Elle n'a pas d'auteur : aucun personnage ne l'inflige, c'est la phase qui la
 * pose. D'où l'absence de `auteur` et de `boosts`, que les activations
 * portent toutes les deux.
 *
 * Enregistrée côté moteur par `MainScheme.Phase()`
 * (game/card/face/card_type/scheme_main.py), le seul appelé par l'étape 1.
 */
export type FaitMenace = FaitMechantCommun & {
  genre: 'menace'
  /** Nom de la manigance visée, tel que le moteur le connaît à cet instant. */
  cible: string
  cible_id: number
  /** La menace RÉELLEMENT posée, après remplacements et modificateurs. */
  montant: number
  /** Menace portée par la manigance après la pose. */
  restant?: number | null
  /** Son seuil (`target_threat`), absent quand la manigance n'en affiche pas. */
  plafond?: number | null
}

/**
 * Une carte rencontre distribuée à un joueur au POINT 3, face cachée.
 *
 * Le fait ne dit pas LAQUELLE : elle est face cachée, et l'annoncer ici
 * révélerait au joueur ce que la règle lui cache. Il dit à qui.
 *
 * Enregistré côté moteur par `PlayerAction.DealEncounterCard`
 * (game/player/action/player_action.py), une fois par carte distribuée.
 */
export type FaitDistribution = FaitMechantCommun & {
  genre: 'distribution'
  /**
   * Indice de SIÈGE du joueur, celui de `World.players`. `null` quand le
   * moteur n'a pas su le déterminer : on n'invente pas un siège.
   */
  joueur?: number | null
  /** Son identité au moment du fait, alter ego compris. */
  joueur_nom?: string | null
}

/**
 * Une carte rencontre révélée par un joueur au POINT 4.
 *
 * Enregistré côté moteur par `PlayerAction.RevealEncounterCards`, AVANT la
 * révélation elle-même : une carte qui met le héros à terre en se révélant
 * doit avoir son étape, et c'est même le coup que le joueur veut voir.
 */
export type FaitRevelation = FaitMechantCommun & {
  genre: 'revelation'
  /** Indice de siège du joueur qui révèle. Voir `FaitDistribution.joueur`. */
  joueur?: number | null
  joueur_nom?: string | null
  /** Nom NU de la carte révélée. */
  carte: string
  /** Son identifiant d'objet, pour la mise en scène sur la table. */
  carte_id: number
  /**
   * Ce que la carte a CHANGÉ en se révélant, mesuré par le moteur entre une
   * photo de la table avant et après (`PlayerAction._EffetsDeLaRevelation`).
   * Absent sur un moteur ancien, ou quand la carte n'a rien changé de
   * mesurable : la scène se tait plutôt que d'inventer.
   */
  effets?: EffetRevelation[]
}

/** Un changement mesuré par le moteur à la révélation d'une carte rencontre. */
export type EffetRevelation =
  | { genre: 'menace'; cible: string; cible_id: number; montant: number; restant?: number | null }
  | { genre: 'degats'; cible: string; cible_id: number; montant: number; restant?: number | null }
  | { genre: 'entree'; carte: string; carte_id: number; type: 'sbire' | 'manigance' | 'environnement' | string }

/**
 * Un fait de la phase du méchant, tel que le MOTEUR l'a enregistré.
 *
 * Union discriminée par `genre` : chaque genre porte ses propres champs, et
 * rien d'autre. Un lecteur qui oublie un genre ne compile pas, ce qui est tout
 * l'intérêt — c'est ce qui a manqué quand le cartouche lisait deux sources.
 */
/**
 * Une carte de STATUT posée sur un personnage pendant la phase du méchant :
 * Sonné, Désorienté, Robuste.
 *
 * Le moteur ne l'inscrit que pendant cette phase (`IsVillainPhase`,
 * sender_unit.py) : un statut posé en phase joueur n'a rien à faire dans ce
 * cartouche. Signalé en jeu le 09/09/2026 : « quand des cartes de statut sont
 * données au méchant, aux sbires ou aux joueurs, cela ne se voit pas ».
 */
export type FaitStatut = FaitMechantCommun & {
  genre: 'statut'
  /** « Stunned », « Confused », « Tough », tels que le moteur les nomme. */
  statut: string
  /** Le PORTEUR du statut. */
  cible: string
  cible_id: number
  /** La carte qui l'a posé, vide quand ce n'est pas une source distincte. */
  cause?: string
  /**
   * Son identifiant d'objet, qui sert à ranger l'étape sous « Méchant » ou
   * sous « Sbires » quand la phase seule ne tranche pas (activations).
   */
  cause_id?: number | null
}

/**
 * Un SBIRE entré en jeu EN PLEINE PHASE du méchant (points 1 et 2 seulement :
 * aux points 3 et 4, c'est la révélation qui raconte l'entrée, par ses
 * `effets`). Le Drone que met en jeu l'attaque d'Ultron, le Goblin Thrall
 * sorti par un boost : le sbire apparaissait sur la table sans une ligne, et
 * seule son attaque faisait une étape. Ajouté le 12/09/2026
 * (`AfterCardEnterPlay`, sender_card.py).
 */
export type FaitEntree = FaitMechantCommun & {
  genre: 'entree'
  /** Nom NU de la carte entrée en jeu. */
  carte: string
  carte_id: number
  /** « sbire » aujourd'hui ; le moteur n'inscrit que les sbires. */
  type: string
  /** La carte qui l'a fait entrer (Ultron, un boost…), vide si inconnue. */
  cause?: string
  cause_id?: number | null
}

export type FaitMechant =
  | FaitActivation
  | FaitMenace
  | FaitDistribution
  | FaitRevelation
  | FaitStatut
  | FaitEntree

export type World = {
  /** Change a chaque rendu du moteur : sert a ne redessiner que si besoin. */
  render_id: number
  round_id: number
  phase: string
  /** Texte de l'evenement en cours, avec des references « [(id,card_id) Nom] ». */
  prompt: string
  prompt_last_text?: string
  sound_name?: string
  /**
   * Mode Bac à sable. Posé par la règle `mode_sandbox` du descripteur de
   * partie, donc conservé dans la sauvegarde : le plateau le retrouve après un
   * rechargement de page comme après le chargement d'une sauvegarde, et l'on
   * saura toujours si une victoire comptait.
   */
  mode_sandbox?: boolean
  /**
   * La RÈGLE : cette partie EST manuelle. Vraie dès la création de la partie,
   * mise en place comprise — NE DIT PAS si le moteur s'est déjà tu. Réservé à
   * ce qui décrit la NATURE de la partie et ne dépend pas du moment (refus
   * d'enregistrer un haut fait, mention au rapport de bug, journal de
   * campagne). Voir `manuel_actif` pour ce qui se règle sur le SILENCE du
   * moteur (tâche 8 bis) : masquage des couches du moteur, gestes manuels.
   */
  mode_manuel?: boolean
  /**
   * L'ÉTAT : le moteur S'EST TU. Faux pendant toute la mise en place (la
   * partie se comporte normalement, le joueur répond aux questions dont le
   * mulligan), vrai seulement une fois la boucle manuelle entrée
   * (`World.ManualLoop`, côté moteur). Distinct de `mode_manuel` par
   * construction (tâche 8 bis) : c'est CE champ que le plateau doit lire
   * pour masquer les couches du moteur et activer les gestes manuels — se
   * régler sur `mode_manuel` masquerait le panneau de mulligan pendant la
   * mise en place et bloquerait la partie pour toujours.
   */
  manuel_actif?: boolean
  /**
   * Le moteur s'arrête-t-il sur la face A de la manigance ? Posé par les
   * parties neuves seulement : une sauvegarde antérieure au 15/09/2026 ne
   * porte pas la règle, et le voile d'ouverture ne doit pas l'attendre.
   */
  confirm_main_scheme?: boolean
  /**
   * Motif du dernier geste manuel refusé, vide quand tout va bien. Posé par
   * `WorldDescriptor.manuel_refus` (tâche 4 ter), lui-même lu depuis
   * `device_manager.sandbox_last_error` (`DrainSandboxCommands`,
   * engine/device/manager/base.py) : la trace existait déjà côté moteur,
   * mais rien ne la consommait avant cette tâche.
   *
   * ⚠ NE REPART À VIDE QU'AU PROCHAIN GESTE QUI RÉUSSIT, pas tout seul entre
   * deux : un lecteur doit se caler sur `render_id` pour ne réagir qu'une
   * fois par refus, voir `CoucheTriche.tsx`.
   *
   * ⚠ C'est un MOTIF TECHNIQUE (`"KeyError: 'zone inconnue : ...'"`), pas un
   * texte pour le joueur : ne jamais l'afficher tel quel à l'écran.
   */
  manuel_refus?: string
  /**
   * La TRACE : quelqu'un est intervenu à la main au moins une fois dans
   * cette partie. Posée par `Scene.corrigee_a_la_main` côté moteur, dès la
   * première pause manuelle (`world.py`), et JAMAIS éteinte ensuite — y
   * compris après une reprise, contrairement à `pause_par` / `pause_a`
   * juste dessous, qui décrivent la pause EN COURS et s'effacent à la
   * reprise. Optionnel : une sauvegarde antérieure à la tâche 2 n'a jamais
   * connu ce champ et doit rester lisible (absent = jamais corrigée).
   *
   * ⚠ NE PAS CONFONDRE avec `mode_manuel` (la RÈGLE : cette partie EST
   * manuelle dès sa création) ni `manuel_actif` (l'ÉTAT : le moteur se tait
   * en ce moment). Cette marque-ci dit qu'une intervention a eu lieu, sur
   * une partie qui n'a pas forcément été déclarée manuelle : c'est elle,
   * et elle seule, qui doit apparaître dans un rapport de bug pour que
   * l'auteur du jeu distingue une partie ordinaire d'une partie retouchée.
   */
  corrigee_a_la_main?: boolean
  /**
   * Qui a posé la pause EN COURS (tâche 3), vide hors pause. Le moteur ne
   * connaît aucun pseudo : ce champ n'est renseigné que si l'appelant de
   * `POST /manuel_pause` a fourni un `qui` non vide. Absent ou vide →
   * `BandeauPause` dit « quelqu'un ».
   *
   * ⚠ EFFACÉ À LA REPRISE, contrairement à `corrigee_a_la_main` juste
   * dessous : ce champ décrit la pause EN COURS, pas la partie entière.
   */
  pause_par?: string
  /**
   * Depuis quand la pause EN COURS dure (tâche 3), vide hors pause. Horodatage
   * tel que le moteur l'a formaté (`Scene.pause_a`, même `Time.Format()` que
   * le reste de la sauvegarde) : une chaîne à afficher telle quelle, jamais à
   * recalculer côté client (le serveur tourne en UTC, voir `salon.ts`).
   *
   * ⚠ EFFACÉ À LA REPRISE, même précaution que `pause_par`.
   */
  pause_a?: string
  event_name: string
  /**
   * Les activations ennemies du round en cours, telles que le MOTEUR les a
   * résolues (voir WorldStat.RecordFaitMechant côté serveur).
   *
   * Le bilan de la phase du méchant les lit au lieu de les déduire en comparant
   * deux photos du monde. Une déduction voit le résultat mais jamais sa
   * composition — elle ne peut pas dire « 5 dégâts = 3 de base + 2 de boost » —
   * et elle compte plusieurs fois ce que le moteur rend plusieurs fois autour
   * d'une seule résolution.
   *
   * Absent des sauvegardes anciennes et des moteurs non mis à jour : tout
   * lecteur doit tenir le cas où la liste manque.
   */
  faits_mechant?: FaitMechant[]
  area_schemes_main: WorldCard[]
  main_schemes_deck: WorldCard[]
  area_schemes_side: WorldCard[]
  /**
   * ATTENTION, au pluriel ce sont des LISTES DE DECKS, pas des listes de cartes :
   * une entree = un deck supplementaire entier. Les 34 etats enregistres avaient
   * tous ces deux zones vides, le piege ne s'y voit pas. Mesure faite sur une
   * partie reelle (scenario a decks supplementaires) : additional_decks[0] est un
   * tableau de 3 cartes.
   * Les equivalents SINGULIERS cote joueur (additional_deck,
   * additional_discard_pile) sont, eux, de simples listes de cartes.
   */
  additional_decks: WorldCard[][]
  additional_discard_piles: WorldCard[][]
  area_villain: WorldCard[]
  villain_deck: WorldCard[]
  encounter_deck: WorldCard[]
  encounter_discard_pile: WorldCard[]
  area_boost: WorldCard[]
  area_environment: WorldCard[]
  area_evidence: WorldCard[]
  area_rule: WorldCard[]
  area_processing: WorldCard[]
  area_revealing: WorldCard[]
  area_resources: WorldCard[]
  area_removed: WorldCard[]
  area_insert: WorldCard[]
  area_set_aside: WorldCard[]
  victory_display: WorldCard[]
  area_status_cards: WorldCard[]
  players: WorldPlayer[]
  /** Cartes citees par l'evenement en cours : le runtime les met en avant. */
  active_card_ids: number[]
  /** Partie terminee par une vraie victoire/defaite (pas Exit/Undo). */
  game_over?: boolean
  players_won?: boolean
  /** Texte du moteur : « The Final Stage of the Villain was Defeated »... */
  game_over_reason?: string
  /**
   * Mode Bataille : le camp gagnant (-1 s'il n'y en a pas) et le camp de
   * chaque siege. Le meme ecran de fin sert aux deux tables : sans eux, il
   * annoncerait la meme chose au vainqueur et au vaincu. Absents hors Bataille.
   */
  winning_team?: number
  teams?: number[]
}

/** Familles de types, reprises telles quelles de descriptor.js. */
const UNIT_TYPES = ['Ally', 'Minion', 'EncounterVillain', 'Hero', 'AlterEgo']
const SCHEME_TYPES = ['MainScheme', 'EncounterSideScheme', 'PlayerSideScheme']

/**
 * Est-ce bien une carte ?
 *
 * Le contrat de /get_world n'est connu que par mesure, et il reserve des
 * surprises : `additional_decks` contient des DECKS la ou tout le reste contient
 * des cartes. Une zone d'une forme inattendue ne doit pas vider le plateau
 * entier, juste manquer a l'appel, et se compter (voir Plateau.nombreIgnore).
 */
export function estUneCarte(valeur: unknown): valeur is WorldCard {
  if (typeof valeur !== 'object' || valeur === null) return false
  const carte = valeur as Partial<WorldCard>
  return (
    typeof carte.id === 'number' &&
    typeof carte.card_type === 'string' &&
    typeof carte.pic_id === 'string' &&
    Array.isArray(carte.visible_for_players) &&
    Array.isArray(carte.down_card_ids)
  )
}

/** Un personnage : il a des points de vie. */
export function isUnit(card: WorldCard): boolean {
  return UNIT_TYPES.includes(card.card_type)
}

/** Un complot : il porte de la menace, et se pose en paysage. */
export function isScheme(card: WorldCard): boolean {
  return SCHEME_TYPES.includes(card.card_type)
}

/**
 * Avons-nous le droit de voir la face de cette carte ?
 * Reprend isVisible() du runtime, sans les reglages de debogage (siege partage,
 * mode spectateur, « montrer toutes les mains ») qui n'existent pas ici.
 */
export function isVisibleFor(card: WorldCard, playerId: number): boolean {
  return card.visible_for_players.includes(playerId)
}
