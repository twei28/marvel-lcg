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
  /**
   * Les BONUS d'ATQ et de DEF, chacun avec la carte qui le donne :
   * `{ ATK: [[nom, id, valeur], ...], DEF: [...] }` (moteur du 04/10/2026,
   * `CardFace.BonusParSource`). Absent sur un moteur plus ancien.
   */
  bonus?: Partial<Record<string, [string, number, number][]>>
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
  /**
   * Taille de main ACTUELLE de l'identite (AJOUT moteur du 04/10/2026), pour
   * la consigne de fin de tour. Absente d'un moteur plus ancien, 0 sans
   * identite : ne jamais l'afficher dans ces deux cas.
   */
  hand_size?: number
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
   * Rising Tide area du pack Wave : hors jeu, cartes posées individuellement,
   * face visible ou cachée selon `is_face_up`. Absente des sauvegardes
   * d'avant le pack, et vide pour tout autre héros : toujours la lire avec
   * `?? []`.
   */
  rising_tide?: WorldCard[]
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
  /**
   * Ce héros a-t-il déjà bouclé son tour ce round ? (24/09/2026, pour griser
   * son onglet dans le sélecteur de vue). Optionnel : une sauvegarde ou un
   * moteur plus ancien n'a pas ce champ, et les fixtures de test qui
   * construisent un `WorldPlayer` à la main n'ont pas à le fournir.
   */
  has_finished_turn_this_round?: boolean
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
  /**
   * Le sbire en cours dans l'ordre des activations, et le NOMBRE de sbires qui
   * vont s'activer (05/10/2026) : le moteur l'annonce des le premier fait d'un
   * sbire, ce que le plateau ne peut pas compter avant d'avoir tout reçu.
   * Absents du vilain et d'un moteur plus ancien.
   */
  rang_sbire?: number
  total_sbires?: number
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
  /** Refonte, lot 5b (decision 43) : l'activation vient de Rapide (Quickstrike). */
  rapide?: boolean
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
  /**
   * Son identifiant d'objet, quand le moteur le connaît (04/10/2026) : il range
   * la conséquence sous sa carte révélée sans comparer des noms. Absent sur un
   * moteur plus ancien.
   */
  cause_id?: number | null
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
  /**
   * Sur une annulation : la carte dont l'effet a REMPLACÉ l'activation (« Stunned »,
   * une carte de joueur), pour « → Annulée par X » (04/10/2026). Absent si inconnue.
   */
  annule_par?: string
  annule_par_id?: number
}

/** Un boost retourné, tel que le moteur le publie (`_BoostsPublies`). */
export type BoostPublie = { nom: string; id: number; apport: number; etoile?: boolean }

/**
 * LE TEMPS INTERMÉDIAIRE (04/10/2026) : le défenseur est choisi, les boosts
 * sont retournés, les dégâts ne sont pas encore portés. Il remplace l'annonce
 * sous le même `activation_id`, et la résolution le remplace à son tour.
 *
 * Il ne porte JAMAIS `subi` ni `inflige` : rien n'a encore été encaissé. Toutes
 * ses clés sont optionnelles, pour qu'une fixture partielle reste lisible.
 */
export type FaitActivationBoosts = FaitActivationCommun & {
  etat: 'boosts'
  /** Le personnage qui défend, `null` sans défense. */
  defenseur?: string | null
  defenseur_id?: number | null
  /** La DÉF du défenseur, 0 sans défense. */
  defense?: number
  boosts?: BoostPublie[]
  /** Apport total des boosts. */
  boost?: number
  /** Ce qui sera porté avant la défense : imprimé, bonus et boosts. */
  total_avant_defense?: number
  /** La valeur IMPRIMÉE annoncée, la même que `base` sur l'annonce. */
  base_imprimee?: number
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
  /** `etoile` : le boost porte une capacite Boost (★), 04/10/2026. */
  boosts: BoostPublie[]
  /**
   * Le DÉFENSEUR, nommé à part (04/10/2026) : `cible` est déjà lui quand
   * quelqu'un défend, et le héros visé disparaissait de l'étape. `null` sans
   * défense ; absent sur un moteur plus ancien.
   */
  defenseur?: string | null
  defenseur_id?: number | null
  /** La cible ANNONCÉE (le héros visé), même quand un autre a défendu. */
  cible_annoncee?: string
  cible_annoncee_id?: number
  /** La valeur IMPRIMÉE annoncée, avant tout bonus (celle de l'annonce). */
  base_imprimee?: number
  /** Sur une manigance : le seuil de la manigance visée, `null` sans seuil. */
  plafond?: number | null
  /** Sur une manigance : la menace AVANT la pose (une manigance au seuil peut se vider aussitôt). */
  avant?: number | null
  /** Refonte, lot 5b (12/10/2026) : ce que Perçant, Robuste et Déferlement ont fait sur ce coup. */
  mots_cles?: MotsClesDuCoup
  /** Refonte, lot 5b : la Riposte de la carte touchée contre l'attaquant. */
  riposte?: RiposteDuCoup
}

export type MotsClesDuCoup = {
  percant?: boolean
  robuste?: boolean
  overkill?: { cible: string; cible_id: number; degats: number }
}

export type RiposteDuCoup = { degats: number; restant?: number | null; vaincu?: boolean }

export type FaitActivation = FaitActivationAnnonce | FaitActivationBoosts | FaitActivationResolue

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
  /**
   * LA DÉCOMPOSITION de `montant` (04/10/2026) : l'escalade imprimée de la
   * manigance, ce que l'accélération (icônes et jetons) y ajoute, et le nombre
   * de joueurs qui multiplie l'escalade. Absents sur un moteur plus ancien.
   */
  escalade?: number
  acceleration?: number
  joueurs?: number
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
  /** Refonte, lot 5c (décision 42) : pourquoi cette carte est distribuée, et par quelle carte. */
  raison?: RaisonDistribution
  source?: string
  /** Sur la première carte de l'étape 3 d'un joueur : celles qu'il a déjà reçues plus tôt dans la phase. */
  deja?: Array<{ raison?: RaisonDistribution; source?: string }>
}

/** Pourquoi une carte rencontre est distribuée (lot 5c) : la règle, un Danger, un Renfort ou une carte. */
export type RaisonDistribution = 'base' | 'danger' | 'renfort' | 'carte'

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
   * Cette carte a été révélée par un Renfort (Surge) déclenché par la
   * précédente, pas par la distribution ordinaire du point 3. Signalement
   * Yarro n27 (28/09/2026) : sans ce marqueur, une DEUXIÈME carte enchaînée
   * par Renfort se lisait comme la SUITE du même événement, et un joueur qui
   * venait d'annuler la première (Spider-Tingle) croyait son effet en échec.
   * Absent sur un moteur ancien : traité comme `false`.
   */
  par_surge?: boolean
  /**
   * Le TYPE de la carte, nom de classe du moteur (« Treachery », « Minion »,
   * « Attachment », « SideScheme », « Environment », « Obligation »),
   * 04/10/2026. Absent sur un moteur plus ancien.
   */
  type?: string
  /**
   * Les recherches rencontre faites par la carte (13/10/2026, moteur
   * `PlayerAction.NoterRecherche`) : ce qu'elle a trouvé (vide : rien), et si
   * le paquet rencontre a été fouillé, donc remélangé. Absent sur un moteur plus ancien.
   */
  recherches?: Array<{ trouve: string[]; paquet: boolean }>
  /** Son effet « Une fois révélée » a été ANNULÉ, par cette carte (04/10/2026). */
  annulee_par?: string
  annulee_par_id?: number
  /** La carte qui a annulé a quitté le jeu en le faisant (Stepford Cuckoos à son dernier psi). */
  annulee_par_sort?: 'defaussee' | 'hors_jeu'
  /**
   * Carte révélée PAR UNE AUTRE carte pendant la phase du méchant (Black
   * Widow, Stepford Cuckoos : « révèle une autre carte »), rapports Yarro n71
   * et n72 (09/10/2026).
   */
  revelee_par?: string
  revelee_par_id?: number
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
  | {
      genre: 'entree'
      carte: string
      carte_id: number
      type: 'sbire' | 'manigance' | 'environnement' | string
      /** Un sbire : l'identite du heros avec qui il s'engage (« Sur la table » v3, Q22). */
      engage_avec_id?: number
    }

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

/**
 * Une activation ANNULÉE PAR SONNÉ (05/10/2026, `JournaliserActivationEmpechee`).
 * Le moteur s'arrête avant l'annonce : sans ce fait, l'étape disparaissait
 * sans un mot.
 */
export type FaitSonne = FaitMechantCommun & {
  genre: 'sonne'
  /** Ce qui a été empêché. */
  temps: 'attaque' | 'manigance'
  type: 'mechant' | 'sbire'
  joueur?: number | null
  auteur: string
  auteur_id: number
  cible?: string | null
  cible_id?: number | null
  /** Faux pour un ennemi Constant : il garde Sonné. */
  statut_retire: boolean
  annule_par?: string
  annule_par_id?: number | null
  fait_id?: string
}

/**
 * Un CHANGEMENT DE STADE en pleine phase du méchant (04/10/2026) : la manigance
 * principale ou le méchant passe au stade suivant (`WorldStat.RecordStade`).
 */
export type FaitStade = FaitMechantCommun & {
  genre: 'stade'
  quoi: 'manigance' | 'mechant'
  /** Le nom de la carte d'avant. */
  avant: string
  /** La NOUVELLE carte, montrée en grand. */
  carte: string
  carte_id: number
  /** L'identifiant de la carte d'avant (04/10/2026), absent sur un moteur plus ancien. */
  avant_id?: number
  /**
   * Les stats IMPRIMÉES d'avant et d'après (04/10/2026). Jamais les PV courants
   * de l'ancienne carte : le moteur l'a déjà retirée quand il écrit le fait.
   */
  stats_avant?: StatsStade
  stats_apres?: StatsStade
}

/** Les stats d'une carte de stade, chacune `null` quand la carte n'en a pas. */
export type StatsStade = {
  pv_max?: number | null
  atq?: number | null
  man?: number | null
  menace?: number | null
  seuil?: number | null
}

/**
 * Le paquet rencontre s'est vidé PENDANT la phase (13/10/2026, encadré ②) : la
 * défausse est remélangée et un jeton d'accélération posé sur la manigance
 * principale (moteur : scenario.py, `process_after_shuffle`).
 */
export type FaitPaquetVide = FaitMechantCommun & {
  genre: 'paquet_vide'
  cible: string
  cible_id: number
  /** Ses jetons d'accélération APRÈS la pose. */
  jetons?: number
}

export type FaitMechant =
  | FaitPaquetVide
  | FaitStade
  | FaitActivation
  | FaitMenace
  | FaitDistribution
  | FaitRevelation
  | FaitStatut
  | FaitEntree
  | FaitSonne

/** Un effet refusé en silence, et pourquoi (voir `refus-effets.tsx`). */
export type RefusEffet = {
  /** Numéro croissant dans la partie : le plateau ne montre que les nouveaux. */
  n: number
  genre: 'statut'
  /** « Stunned », « Confused », « Tough » : le nom moteur de la carte d'état. */
  statut: string
  /** robuste : Stalwart ; deja : le statut y est déjà ; immunite : « ne peut pas être… ». */
  motif: 'robuste' | 'deja' | 'immunite'
  cible_id: number
  cible: string
  cible_code?: string
  /** La carte responsable (la Lance de Drang), vide si inconnue. */
  source?: string
  source_code?: string
}

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
   * La RÈGLE : cette partie a été lancée comme un scénario de campagne
   * (`mode_campaign`). Seul critère fiable pour ouvrir le panneau de
   * récompenses : la clé du navigateur et le `partieEnCours` du serveur
   * survivent à une partie ordinaire. Absent d'un descripteur ancien : traité
   * comme faux.
   */
  mode_campaign?: boolean
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
  /** Même rôle pour une manigance annexe imposée par le scénario. */
  confirm_side_scheme?: boolean
  /** Faces A montrées dans l'ordre du livret, avant leurs capacités (10/10/2026). */
  confirm_scheme_setup_order?: boolean
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
   * ⚠ N'EST PLUS CE QU'ON AFFICHE (revue finale, 20/09/2026) : c'est une
   * heure MURALE, celle du serveur, qu'un joueur distant lisait comme la
   * sienne — et qui se lit mal comme une durée sous le mot « depuis ». Le
   * bandeau préfère `pause_epoch` juste en dessous, et ne retombe sur cette
   * chaîne que face à un moteur plus ancien qui ne la publie pas.
   *
   * ⚠ EFFACÉ À LA REPRISE, même précaution que `pause_par`.
   */
  pause_a?: string
  /**
   * Le même instant, en SECONDES DEPUIS L'ÉPOQUE (`Scene.pause_epoch`), zéro
   * hors pause. Sans fuseau : le plateau en tire une DURÉE avec sa propre
   * horloge (« depuis 12 min »), ce qu'aucune heure murale ne permet.
   *
   * ⚠ EFFACÉ À LA REPRISE, même précaution que `pause_par`.
   */
  pause_epoch?: number
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
  /**
   * Effets REFUSES en silence par le moteur (`WorldStat.RecordRefusEffet`) :
   * « Drang n'est pas sonné, il est Robuste ». Numérotés (`n`) pour que le
   * plateau n'affiche que les nouveaux. Absent des moteurs non mis à jour.
   */
  refus_effets?: RefusEffet[]
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
  /** Statistiques de la partie, publiees une fois la partie finie (onglet Stats). */
  stats_partie?: StatsPartie
}

/** Une carte des « plus » ou « moins » jouees de l'ecran de fin. */
export type CarteStat = {
  card_id: string
  nom: string
  n: number
  piochee: number
  jouee: number
}

/** Ce que le moteur MESURE pour un joueur (to_descriptor.py, stats_de_partie). */
export type StatsJoueur = {
  siege: number
  heros: string
  heros_id: string
  aspects: string[]
  pv?: number | null
  pv_max?: number | null
  compteurs: Partial<Record<CompteurStat, number>>
  plus_jouees: CarteStat[]
  moins_jouees: CarteStat[]
}

export type CompteurStat =
  | 'degats_mechant'
  | 'degats_sbires'
  | 'menace_principale'
  | 'menace_annexes'
  | 'degats_subis'
  | 'degats_evites'
  | 'attaques_defendues'
  | 'cartes_jouees'
  | 'ressources_depensees'

export type StatsPartie = {
  /** Duree de la partie en secondes. */
  temps: number
  rounds: number
  joueurs: StatsJoueur[]
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
