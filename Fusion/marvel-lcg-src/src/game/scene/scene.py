from core import *
from core.lib import Time
from game.scene.replay import *
from engine.lib import Json, Ver
from engine.log import Log
from engine.file import FileManager
from engine.config import ConfigVariables
from game import *

CATEGORY_NAME = "SCENE"

# These rules will be added for testing file, use when change some new rules as default
TEST_RULES = ConfigVariables.ListStr('test_rules', [])

METADATA_KEY_LIST = Literal[
    "step", "clients"
]

METADATA_KEY_BOOL = Literal[
    "is_puzzle"
]

METADATA_KEY_INT = Literal[
    "seed"
]

METADATA_KEY_STR = Literal[
    "time", "path", "comment", "cover", "report", "sign"
]

METADATA_KEY_FLOAT = Literal[
    "playtime"
]

METADATA_KEY = METADATA_KEY_LIST | METADATA_KEY_BOOL | METADATA_KEY_INT | METADATA_KEY_STR | METADATA_KEY_FLOAT

@dataclass
class Scene:
    version: str = field(default_factory=lambda: "")
    metadata: Dict[METADATA_KEY, Union[str, int, bool]] = field(default_factory=lambda: {})
    rules: List[str] = field(default_factory=lambda: [])

    campaign: CampaignDescriptor = field(default_factory=lambda: CampaignDescriptor())
    # SECONDE TABLE. Vide en partie ordinaire. En mode competitif, chaque
    # equipe apporte SON scenario et affronte celui de l'autre (mc56 p.14,
    # etape 4) : `campaign` est pose devant l'equipe 0, `campaign_2` devant
    # l'equipe 1. Champ a defaut, donc les sauvegardes existantes se
    # rechargent sans changer de sens.
    campaign_2: CampaignDescriptor = field(default_factory=lambda: CampaignDescriptor())
    players: Sequence[HeroDescriptor] = field(default_factory=lambda: [])

    puzzle: List[str] = field(default_factory=lambda: [])

    # LES GESTES DU MODE MANUEL (spec du 18/09/2026), dans l'ordre ou le joueur
    # les a faits. Rejoues a la mise en place, comme `puzzle` l'est pour une
    # partie Puzzle.
    #
    # ⚠ CHAMP SEPARE de `puzzle`, et c'est deliberé : les deux usages ne
    # doivent pas se melanger, et un champ a defaut vide laisse les
    # sauvegardes existantes se recharger sans changer de sens.
    manuel_commands: List[str] = field(default_factory=lambda: [])

    # LE RANG DE CHAQUE GESTE (constat C1 de la ronde de correction 1 du
    # 20/09/2026) : le nombre d'entrees joueur deja jouees quand le geste a
    # ete fait (`InputModule.current_step_id`). MEME INDEX que
    # `manuel_commands` ci-dessus -- deux listes paralleles, tenues
    # ensemble par `EnregistrerGestesManuels` / `RetirerDernierGesteManuel`
    # plus bas, qui sont les SEULES a avoir le droit d'y toucher.
    #
    # ⚠ A QUOI CA SERT, ET POURQUOI CE N'EST PAS UN LUXE. Une sauvegarde
    # n'est pas un instantane : `GameSetup` REJOUE les entrees. Rejouer tous
    # les gestes a l'instant 0, comme on le faisait, ne perd pas seulement
    # une correction, ca fausse la table entiere -- un `Shuffle`, un `Draw`,
    # un `Reveal` ou un `Boost` consomme trop tot DECALE tout le flux
    # aleatoire (la rencontre du round 2 n'est plus la meme), un
    # `CreateCard`/`PutIntoPlay` fait naitre des objets qui volent les
    # identifiants que le rejeu attribuera ensuite a d'autres cartes (un
    # geste suivant vise alors la mauvaise carte, SANS erreur), et un
    # `Puzzle.Win()` rejoue a l'instant 0 rend la sauvegarde inouvrable.
    # Le rang remet chaque geste a SA place dans le rejeu.
    #
    # ⚠ CHAMP A DEFAUT VIDE, et une liste plus COURTE que `manuel_commands`
    # est un cas NORMAL, pas une incoherence : c'est ce que porte toute
    # sauvegarde ecrite avant ce champ. Un rang inconnu vaut « a la fin du
    # rejeu », qui est exactement ou ces gestes-la etaient rejoues.
    manuel_commands_step: List[int] = field(default_factory=lambda: [])

    # LA MARQUE « corrigee a la main » (tache 2 du chantier pause manuelle,
    # 20/09/2026). Posee par `World.BasculerPauseManuelle` a la PREMIERE
    # pause d'une partie ORDINAIRE, et JAMAIS remise a faux -- CE N'EST PAS
    # UN ETAT (comme `manuel_actif`, qui repasse a faux a la reprise) MAIS
    # UNE TRACE : une partie qu'on a arretee pour corriger la table a la main
    # l'a ete, meme si on a repris ensuite, meme apres un aller-retour de
    # sauvegarde. Sert a ne jamais laisser planer le doute sur la regularite
    # d'une victoire, et a le signaler dans un rapport de bug.
    #
    # ⚠ CHAMP A DEFAUT FAUX, meme precaution que `manuel_commands` juste
    # au-dessus : les sauvegardes existantes se rechargent sans changer de
    # sens.
    corrigee_a_la_main: bool = field(default=False)

    # LA PAUSE EN COURS (tache 3 du chantier pause manuelle, 20/09/2026).
    # Qui l'a posee (pseudo, ou vide -- le moteur ne connait aucun pseudo, il
    # ne fait que relayer ce que `POST /manuel_pause` a fourni) et depuis
    # quand (`Time.Format()`, meme format que `metadata['time']` plus haut).
    #
    # ⚠ DISTINCTS de `corrigee_a_la_main` juste au-dessus, et c'est
    # deliberé : ces deux champs decrivent la pause EN COURS, pas la partie
    # entiere -- `World.BasculerPauseManuelle` les EFFACE a la reprise
    # (repassent a la chaine vide), alors que `corrigee_a_la_main` ne
    # s'eteint jamais. Sans cette info, un joueur d'une table EN LIGNE voit
    # sa partie s'arreter sans savoir qui l'a arretee ni depuis quand, et
    # croit a une panne -- exactement le defaut que le bandeau de pause
    # existe pour eviter.
    #
    # ⚠ CHAMPS A DEFAUT CHAINE VIDE, meme precaution que les champs
    # ci-dessus : une sauvegarde ANTERIEURE a ces champs se recharge sans
    # changer de sens, c'est-a-dire jamais en pause.
    #
    # ⚠ MIS A JOUR LE 20/09/2026 (constat C1 de la revue finale) : ces deux
    # champs ne servent plus seulement au bandeau. `GameSession.GameSetup`
    # lit `pause_en_cours` (juste en dessous) pour reposer `manuel_actif` au
    # montage : une partie SAUVEGARDEE EN PAUSE se recharge donc desormais EN
    # PAUSE, et un « Annuler » ne la fait plus reprendre en silence. La
    # phrase precedente disait « jamais en pause au chargement » : elle
    # n'etait vraie que des sauvegardes d'avant ces champs, et elle decrivait
    # le defaut, pas la regle.
    pause_par: str = field(default="")
    pause_a: str = field(default="")
    # DEPUIS QUAND, EN SECONDES DEPUIS L'EPOQUE (revue finale, 20/09/2026).
    #
    # ⚠ DOUBLON ASSUME AVEC `pause_a` JUSTE AU-DESSUS, et la raison est le
    # LECTEUR. `pause_a` est un `Time.Format()` : une heure MURALE, celle du
    # serveur (« 2026-09-20 17-12 »), affichee sous le mot « depuis ». Un
    # joueur a l'autre bout du pays y lisait une heure qui n'est pas la
    # sienne, et le format se lit mal comme une duree. Une valeur d'epoque,
    # elle, ne depend d'aucun fuseau : le plateau en tire « depuis 12 min »
    # avec sa PROPRE horloge (`BandeauPause`, `dureeDepuis`).
    #
    # `pause_a` reste, et n'est pas remplace : c'est lui que `pause_en_cours`
    # interroge (donc la memoire de la pause a travers une sauvegarde et un
    # « Annuler »), et les sauvegardes anterieures a ce champ-ci n'en portent
    # aucun. Zero = aucune pause en cours, comme la chaine vide a cote.
    pause_epoch: float = field(default=0.0)

    # LA REPRISE EN AUTOMATIQUE d'une partie DECLAREE manuelle : la phase ou
    # le moteur a repris la main ("heros", "mechant" ou "tour"), vide tant que
    # la partie est restee manuelle. Posee par `World.ReprendreEnAuto`, c'est
    # la memoire durable de la reprise (le `World` est reconstruit a chaque
    # chargement ou annulation) : `World.OnGameLoop` la relit pour ne plus
    # entrer dans `ManualLoop` et reprendre la meme phase au rejeu.
    # Champ a defaut vide : une sauvegarde anterieure se recharge inchangee.
    reprise_auto: str = field(default="")

    inputs: List[OperationDescriptor] = field(default_factory=lambda: [])

    @property
    def pause_en_cours(self) -> bool:
        """Une pause manuelle est EN COURS sur cette partie.

        ⚠ L'ETAT, PAS LA TRACE. `corrigee_a_la_main` (plus haut) dit
        « quelqu'un est intervenu au moins une fois » et ne s'eteint jamais ;
        ceci dit « le moteur s'est tu EN CE MOMENT » et s'eteint a la
        reprise. Les confondre a deja rendu ce mode inutilisable une fois.

        DERIVE, SANS CHAMP SUPPLEMENTAIRE : `World.BasculerPauseManuelle` est
        le seul endroit qui ecrit ces deux champs, et elle pose `pause_a` a
        la pause puis le vide a la reprise -- l'invariant tient donc en un
        seul endroit. `pause_par` ne ferait pas l'affaire : il est
        legitimement VIDE quand le siege n'est pas identifie (le bandeau dit
        alors « quelqu'un »).
        """
        return bool(self.pause_a)

    def EnregistrerGestesManuels(self, gestes: List[str], rang: int) -> None:
        """Ajoute des gestes manuels APPLIQUES, avec le rang ou ils l'ont ete.

        LE SEUL endroit qui ajoute a `manuel_commands`, avec
        `RetirerDernierGesteManuel` juste en dessous pour l'autre sens : deux
        listes paralleles ne tiennent que si un seul endroit les fait bouger
        ensemble. Les deux chemins de drainage du moteur passent par ici --
        `World.ManualLoop` (partie manuelle DECLAREE) et
        `Controller.ChoiceOne` (pause de partie ORDINAIRE).

        `rang` : `InputModule.current_step_id` au moment de l'application,
        c'est-a-dire le nombre d'entrees joueur deja jouees. Voir
        `manuel_commands_step` pour ce que le rejeu en fait.
        """
        if not gestes:
            return
        self.manuel_commands += gestes
        self.manuel_commands_step += [rang] * len(gestes)

    def RetirerDernierGesteManuel(self) -> bool:
        """Retire le dernier geste manuel ET son rang. Rend faux s'il n'y a
        rien a retirer, pour que l'appelant puisse le dire au joueur."""
        if not self.manuel_commands:
            return False
        self.manuel_commands.pop()
        # Liste plus COURTE = sauvegarde d'avant ce champ, cas normal.
        if len(self.manuel_commands_step) > len(self.manuel_commands):
            self.manuel_commands_step.pop()
        return True

    def GestesARejouer(self) -> List[Tuple[int|None, str]]:
        """Les gestes a rejouer au montage, dans l'ordre, chacun avec son rang.

        Rang `None` = inconnu, donc « a la fin du rejeu » : c'est ce que
        portent les sauvegardes ecrites avant `manuel_commands_step`, et
        c'est exactement l'endroit ou elles etaient rejouees.
        """
        rangs = self.manuel_commands_step
        return [(rangs[i] if i < len(rangs) else None, geste)
                for i, geste in enumerate(self.manuel_commands)]

    def GetSaveFileName(self, use_comment: bool=True) -> str:
        return f"[{Ver.version}]-{self.GetName(use_comment)}"

    @property
    def name(self) -> str:
        return self.GetName()

    def GetName(self, use_comment: bool=True) -> str:
        from engine import Engine
        game = Engine.game

        name = ''

        if self.is_puzzle:
            name = 'puzzle-'

        if use_comment and self.comment:
            name += f"{self.comment}"
        else:
            for player in self.players:
                name += f'{player.name}-'
            name += f'{self.campaign.name}'
            if self.campaign.challenges:
                name += '-' + f'-'.join(self.campaign.challenges)
            elif self.campaign.expert:
                name += f'-expert'

            if game.world and game.world.rule.mode_campaign.val:
                name += f'-campaign'

        inputs = game.controller_manager.replay.history_inputs
        name += f'-({len(inputs)})'

        if game.session.world:
            for test_card_id in sorted(game.session.world.cheat.test_cards):
                if test_card_id not in ["01088", "01089", "01090"]:
                    name += f'-{test_card_id}'

        for input in inputs:
            if input.effect.GetDebugCommand():
                name += f'-debug'
                break

        if self.seed != 0:
            name += f'-({str(self.seed)})'

        return FileManager.SanitizeFilename(name.lower())

    def UpdateInputs(self, game: 'Game'):
        self.inputs = game.controller_manager.replay.history_inputs

    def PrepareSave(self, game: 'Game', *, playtime: float|None, report: str|None=None, clients: List[str]|None=None):
        from engine.user.user_info import UserInfo

        self.UpdateInputs(game)

        if self.sign == "":
            self.SetMetadataStr("sign", UserInfo.fingerprint)

        if self.time == "":
            self.SetMetadataStr("time", Time.Format())

        data = self
        if self.is_puzzle:
            for input in data.inputs:
                delattr(input, 'step')
                delattr(input, 'event')
                delattr(input, 'crc')

        if playtime:
            self.SetMetadataFloat("playtime", playtime)

        # Abandoned
        for key in ["undo_count", "goto_count"]:
            self.metadata.pop(key, None) # type: ignore

        if report:
            self.SetMetadataStr("report", report)
        if clients:
            self.SetMetadataList("clients", clients)

        # Sort by key
        ordered_keys = ['sign'] + [key for key in self.metadata if key not in ['sign', 'clients', 'report', 'step']] + ['report', 'clients', 'step']
        sorted_metadata: Dict[METADATA_KEY, Union[str, int, bool]] = {key: self.metadata[key] for key in ordered_keys if key in self.metadata}
        self.metadata = sorted_metadata

    def Save(self, file_path: str, game: 'Game', *, playtime: float|None=None) -> bool:
        if self.is_puzzle:
            return False

        # if self.is_puzzle:
        #     if 'path' in self.metadata:
        #         del self.metadata['path']
        #     if 'time' in self.metadata:
        #         del self.metadata['time']
        #     # if 'rule' in self.metadata:
        #     #     del self.metadata['rule']
        self.PrepareSave(game, playtime=playtime)

        path = FileManager.GetDirName(file_path)
        FileManager.MakeDir(path)
        # import copy
        # if min:
        #     data = copy.deepcopy(self)
        #     for input in data.inputs:
        #         del input.index
        #         del input.controller_id
        #         del input.event
        #         del input.effect.name
        #         del input.effect.card.name
        #         for target in input.effect.targets:
        #             del target.name
        #         for resource in input.effect.resources:
        #             del resource.name
        # else:
        #     data = self

        # Version 6
        # for input in self.inputs:
        #     del input.effect.name
        #     del input.hash

        data = self
        # DebugBreak()
        Json.Save(data, file_path, ignore_check_sum=False)
        Log.Info(CATEGORY_NAME, f"Saved: {file_path}")
        return True

    # Call follow `Json.LoadAs` 
    def UpdateVersion(self):
        if "mode_skirmish" in self.metadata: # type: ignore
            self.rules.append("mode_skirmish")
            self.metadata.pop("mode_skirmish") # type: ignore
        if "mode_heroic" in self.metadata: # type: ignore
            mode_heroic = self.metadata["mode_heroic"] # type: ignore
            self.rules.append(f"mode_heroic_{mode_heroic}")
            self.metadata.pop("mode_heroic") # type: ignore
        if "rule" in self.metadata: # type: ignore
            rule = self.metadata["rule"] # type: ignore
            if rule == "1.5":
                self.rules.append(f"rule_15")
            self.metadata.pop("rule") # type: ignore
        if not Ver(self.version).IsCreateHeroDeckFirst():
            self.rules.append("create_player_deck_first")
        if not Ver(self.version).IsDeadpoolsEncounter():
            if "crisis_of_infinite_deadpools" in self.rules:
                self.rules.remove("crisis_of_infinite_deadpools")
            else:
                self.rules.append("no_crisis_of_infinite_deadpools")
        else:
            if "crisis_of_infinite_deadpools" in self.rules:
                self.rules.remove("crisis_of_infinite_deadpools")

        if not Ver(self.version).IsFixSurge() and \
            'fix_surge' not in self.rules:
            self.rules.append("no_fix_surge")

        if not Ver(self.version).IsFixTreachery() and \
            'fix_treachery' not in self.rules:
            self.rules.append("no_fix_treachery")

        if "encounter_cards_ignore_crisis" in self.rules:
            self.rules.remove("encounter_cards_ignore_crisis")

        del self.campaign.modular_sets
        self.rules = list(sorted(set(self.rules)))

    def HackTestRule(self):
        # from engine import Engine
        # if "rule_15" in self.rules:
        #     self.rules.remove("rule_15")
        # else:
        #     self.rules += TEST_RULES.value
        #     self.rules = list(set(self.rules))
        pass

    def SetMetadataList(self, key: METADATA_KEY_LIST, value: List[str]):
        str_list = Types.ListToStrList(value)
        self.metadata[key] = str_list

    def SetMetadataBool(self, key: METADATA_KEY_BOOL, value: bool):
        self.metadata[key] = value

    def SetMetadataInt(self, key: METADATA_KEY_INT, value: int):
        self.metadata[key] = value

    def SetMetadataStr(self, key: METADATA_KEY_STR, value: str):
        self.metadata[key] = value

    def SetMetadataFloat(self, key: METADATA_KEY_FLOAT, value: float):
        self.metadata[key] = f"{value:.1f}"

    def SetSeed(self, value: int):
        self.SetMetadataInt("seed", value)

    ################################################################################
    #
    def GetMetadataList(self, key: METADATA_KEY_LIST) -> List[str]:
        str_list = str(self.metadata.get(key, ""))
        return Types.StrListToList(str_list)

    def GetMetadataBool(self, key: METADATA_KEY_BOOL) -> bool:
        return bool(self.metadata.get(key, False))

    def GetMetadataInt(self, key: METADATA_KEY_INT) -> int:
        return int(self.metadata.get(key, 0))

    def GetMetadataStr(self, key: METADATA_KEY_STR) -> str:
        return str(self.metadata.get(key, ""))

    def GetMetadataFloat(self, key: METADATA_KEY_FLOAT) -> float:
        return float(self.metadata.get(key, 0))

    ################################################################################
    #
    @property
    def time(self) -> str:
        return self.GetMetadataStr("time")

    @property
    def path(self) -> str:
        return self.GetMetadataStr("path")

    @property
    def seed(self) -> int:
        return self.GetMetadataInt("seed") # -1 means random

    @property
    def comment(self) -> str:
        return self.GetMetadataStr("comment")

    @property
    def is_puzzle(self) -> bool:
        return self.GetMetadataBool("is_puzzle")

    @property
    def cover(self) -> str:
        return self.GetMetadataStr("cover")

    @property
    def playtime(self) -> float:
        return self.GetMetadataFloat("playtime")

    @property
    def step(self) -> List[str]:
        return self.GetMetadataList("step")

    @property
    def sign(self) -> str:
        return self.GetMetadataStr("sign")

