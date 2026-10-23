from core import *
from game.render import *
from game.render.descriptor.card import CardDescriptor

@dataclass
class WorldDescriptor:
    # world
    render_id: int = field(default=0)
    round_id: int = field(default=0)
    phase: str = field(default='')
    prompt: str = field(default='')
    event_name: str = field(default='')
    prompt_last_text: str = field(default='')
    sound_name: str = field(default='')
    max_card_object_id: int = field(default=0)
    # Le plateau en a besoin pour afficher le bandeau et autoriser le
    # clic droit. Transmis a chaque rendu : il survit donc au
    # rechargement de page et au chargement d'une sauvegarde.
    mode_sandbox: bool = field(default=False)
    # La REGLE : cette partie a ete lancee comme un scenario de CAMPAGNE
    # (`mode_campaign` de la liste `rules` de /new). C'est le seul critere
    # fiable pour savoir si une victoire doit s'ouvrir sur les recompenses
    # d'une campagne : la cle du navigateur et le `partieEnCours` du serveur
    # sont des etats durables qu'une partie ordinaire n'efface pas. Transmis a
    # chaque rendu a TOUS les sieges : il survit au rechargement de page et au
    # chargement d'une sauvegarde.
    mode_campaign: bool = field(default=False)
    # La REGLE : cette partie EST manuelle. Vraie des la creation de la
    # partie, mise en place comprise -- NE DIT PAS si le moteur s'est deja
    # tu. Reserve a ce qui decrit la NATURE de la partie et ne depend pas du
    # moment (refus d'enregistrer un haut fait, mention au rapport de bug,
    # journal de campagne). Transmis a chaque rendu : il survit au
    # rechargement de page et au chargement d'une sauvegarde.
    mode_manuel: bool = field(default=False)
    # L'ETAT : le moteur S'EST TU. Faux pendant toute la mise en place (la
    # partie se comporte normalement, le joueur repond aux questions dont le
    # mulligan), vrai seulement une fois la boucle manuelle entree
    # (`World.ManualLoop`, apres la mise en place). Distinct de
    # `mode_manuel` par construction (tache 8 bis) : le plateau doit se
    # regler sur CE champ-ci pour masquer les couches du moteur et activer
    # les gestes manuels -- se regler sur `mode_manuel` masquerait le
    # panneau de mulligan pendant la mise en place et bloquerait la partie
    # pour toujours, le moteur attendant une reponse qu'aucune couche ne
    # permettrait plus de donner.
    manuel_actif: bool = field(default=False)
    # Le plateau tient son voile d'ouverture jusqu'a la question de la face A.
    # Il doit donc savoir s'il y a une question a attendre : une sauvegarde
    # ancienne ou un puzzle ne porte pas la regle, et n'en posera jamais.
    confirm_main_scheme: bool = field(default=False)
    # Meme chose pour une manigance annexe imposee par le scenario : le
    # plateau sait qu'un panneau la montrera, sa mise en place pas a pas ne
    # la presente donc pas une seconde fois.
    confirm_side_scheme: bool = field(default=False)
    # Les faces A se montrent dans l'ordre du livret (avant leurs capacites) :
    # le plateau ne joue alors plus le retournement dans le panneau.
    confirm_scheme_setup_order: bool = field(default=False)
    # Le motif du DERNIER geste manuel refuse, vide quand tout va bien.
    #
    # Lu depuis `device_manager.sandbox_last_error` (pose par
    # `DrainSandboxCommands`, engine/device/manager/base.py) : la trace du
    # refus existait deja cote moteur mais n'etait consommee nulle part.
    # Transmis a chaque rendu, comme `mode_manuel` : une fois publie et vu, il
    # ne repart a vide qu'au PROCHAIN geste qui reussit (le moteur ne le
    # remet pas a vide tout seul entre deux). Voir le rapport de la tache
    # 4 ter pour ce que ca implique cote plateau.
    manuel_refus: str = field(default='')
    # LA MARQUE « corrigee a la main » (tache 2, pose Scene.corrigee_a_la_main
    # ci-dessous). Contrairement a `manuel_actif`, elle ne redevient jamais
    # fausse une fois publiee a vrai -- c'est une TRACE de la partie, pas un
    # etat du moteur. Transmise a chaque rendu, comme `mode_manuel` : elle
    # survit au rechargement de page et au chargement d'une sauvegarde.
    corrigee_a_la_main: bool = field(default=False)
    # LA PAUSE EN COURS (tache 3). Qui l'a posee (vide = aucun pseudo n'a
    # voyage, `BandeauPause` dit « quelqu'un ») et depuis quand
    # (`Time.Format()`, une chaine a afficher telle quelle). Lus sur la SCENE
    # (`Scene.pause_par` / `Scene.pause_a`), pas sur `world` : c'est elle qui
    # survit a la sauvegarde. ⚠ EFFACES A LA REPRISE, contrairement a
    # `corrigee_a_la_main` juste au-dessus : ces deux champs decrivent la
    # pause EN COURS, pas la partie entiere.
    pause_par: str = field(default="")
    pause_a: str = field(default="")
    # En secondes depuis l'epoque, 0 hors pause : le plateau en tire une
    # DUREE avec sa propre horloge, la ou `pause_a` ne lui donne qu'une heure
    # murale du serveur. Voir `Scene.pause_epoch`.
    pause_epoch: float = field(default=0.0)
    # play
    area_schemes_main: List[CardDescriptor] = field(default_factory=lambda: [])
    main_schemes_deck: List[CardDescriptor] = field(default_factory=lambda: [])
    area_schemes_side: List[CardDescriptor] = field(default_factory=lambda: [])
    additional_decks: List[Sequence[CardDescriptor]] = field(default_factory=lambda: [])
    additional_discard_piles: List[Sequence[CardDescriptor]] = field(default_factory=lambda: [])

    area_villain: List[CardDescriptor] = field(default_factory=lambda: [])
    villain_deck: List[CardDescriptor] = field(default_factory=lambda: [])
    encounter_deck: List[CardDescriptor] = field(default_factory=lambda: [])
    encounter_discard_pile: List[CardDescriptor] = field(default_factory=lambda: [])

    area_boost: List[CardDescriptor] = field(default_factory=lambda: [])
    area_environment: List[CardDescriptor] = field(default_factory=lambda: [])
    area_evidence: List[CardDescriptor] = field(default_factory=lambda: [])
    area_rule: List[CardDescriptor] = field(default_factory=lambda: [])
    area_processing: List[CardDescriptor] = field(default_factory=lambda: [])
    area_revealing: List[CardDescriptor] = field(default_factory=lambda: [])
    area_resources: List[CardDescriptor] = field(default_factory=lambda: [])
    area_removed: List[CardDescriptor] = field(default_factory=lambda: [])
    area_insert: List[CardDescriptor] = field(default_factory=lambda: [])
    area_set_aside: List[CardDescriptor] = field(default_factory=lambda: [])
    victory_display: List[CardDescriptor] = field(default_factory=lambda: [])
    area_status_cards: List[CardDescriptor] = field(default_factory=lambda: [])
    # Activations ennemies du round en cours (ajout local, lu par ui-app).
    #
    # Le bilan de la phase du mechant les lit telles quelles, au lieu de les
    # deduire en comparant deux photos du monde : une deduction voit le
    # resultat (« 5 degats ») mais jamais sa composition (« 3 de base + 2 de
    # boost »), et compte plusieurs fois ce que le moteur rend plusieurs fois.
    #
    # Dictionnaires plutot qu'une dataclasse : ce journal ne sert qu'a
    # l'affichage, il traverse le meme JSON que le reste, et lui donner une
    # forme figee obligerait a la maintenir des deux cotes pour rien.
    faits_mechant: List[Dict[str, Any]] = field(default_factory=lambda: [])
    # Les choix a UNE SEULE option resolus d'office (voir WorldStat.choix_uniques) : l'interface en affiche un bandeau.
    choix_uniques: List[Dict[str, Any]] = field(default_factory=lambda: [])
    # LA VILLE (campagne MC×DC 2026 « La ville ne dort jamais », 22/10/2026) : la grille de lieux, le CAPO de chaque rangee, la case de chaque
    # joueur, les sbires attaches, les compteurs des pistes et les limites « une fois par round » deja utilisees. Dictionnaire VIDE hors de la
    # ville : l'onglet « Ville » de l'interface ne s'ouvre alors pas. Forme : `ToDescriptor.Ville` (to_descriptor.py).
    ville: Dict[str, Any] = field(default_factory=lambda: {})
    # L'ASSEMBLEE de Kingsfall multi-tables (22/10/2026) : code, cette table, groupes (nom, joueurs, etat), total de Longue vie et seuil, degats / menace
    # du Roi, verdict. Dictionnaire VIDE hors assemblee. Forme : `ToDescriptor.Assemblee`.
    assemblee: Dict[str, Any] = field(default_factory=lambda: {})
    # Fin de partie exposee au client (ajout local, lu par ui-app)
    game_over: bool = field(default=False)
    players_won: bool = field(default=False)
    game_over_reason: str = field(default='')
    # Mode competitif : le meme ecran de fin sert aux deux tables, il faut donc
    # dire QUI a gagne et a quel camp appartient chaque siege. -1 = pas de camp
    # gagnant (partie ordinaire, deux camps perdants, egalite parfaite) ; la
    # liste est vide hors mode competitif.
    winning_team: int = field(default=-1)
    teams: List[int] = field(default_factory=lambda: [])
    # Statistiques de la partie, publiees une fois la partie finie (ecran de fin,
    # onglet Stats, 10/10/2026). Vide tant que la partie continue. Forme :
    # to_descriptor.py, `stats_de_partie`.
    stats_partie: Dict[str, Any] = field(default_factory=lambda: {})
    # player
    @dataclass
    class PlayerDescriptor:
        area_hero: List[CardDescriptor] = field(default_factory=lambda: [])
        allies: List[CardDescriptor] = field(default_factory=lambda: [])
        supports: List[CardDescriptor] = field(default_factory=lambda: [])
        player_deck: List[CardDescriptor] = field(default_factory=lambda: [])
        player_discard_pile: List[CardDescriptor] = field(default_factory=lambda: [])
        dealt_encounter_cards: List[CardDescriptor] = field(default_factory=lambda: [])
        # La zone de resolution DE CE JOUEUR (correctif du 15/09/2026). Elle
        # existe depuis toujours cote moteur (`player.area_processing`), mais
        # `to_descriptor` la fusionnait avec celle du monde dans le seul
        # `WorldDescriptor.area_processing` : le client ne savait plus a qui la
        # carte appartenait et la dessinait chez le mechant. La liste fusionnee
        # reste publiee telle quelle, l'ancien client la lit.
        area_processing: List[CardDescriptor] = field(default_factory=lambda: [])
        hand_cards: List[CardDescriptor] = field(default_factory=lambda: [])
        reserve: List[CardDescriptor] = field(default_factory=lambda: []) # CORRECTIF (pack brawn)
        rising_tide: List[CardDescriptor] = field(default_factory=lambda: []) # AJOUT (pack wave)
        engaged_enemies: List[CardDescriptor] = field(default_factory=lambda: [])
        set_aside_nemesis_sets: List[CardDescriptor] = field(default_factory=lambda: [])
        set_aside_deck: List[CardDescriptor] = field(default_factory=lambda: [])

        additional_deck: List[CardDescriptor] = field(default_factory=lambda: [])
        additional_discard_pile: List[CardDescriptor] = field(default_factory=lambda: [])
        obligations_area: List[CardDescriptor] = field(default_factory=lambda: [])
        environment_area: List[CardDescriptor] = field(default_factory=lambda: [])

        resources: str = field(default='')
        is_eliminated: bool = field(default=False)
        # AJOUT du 04/10/2026 : la taille de main ACTUELLE de l'identite. Le
        # plateau l'ecrit dans la consigne de fin de tour (« tu repioches
        # jusqu'a 6 ») : elle varie selon le heros, sa forme et ses cartes.
        hand_size: int = field(default=0)
        has_finished_turn_this_round: bool = field(default=False)
    players: List[PlayerDescriptor] = field(default_factory=lambda: [])
    # player_id: int = field(default=0)
    # Other
    active_card_ids: List[int] = field(default_factory=lambda: [])

