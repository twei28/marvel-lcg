from core import *
from engine.device import *
from engine.controller import *
from engine.log import Log

CATEGORY_NAME = "DEVICE_MANAGER"

@dataclass
class AskOptionPayload:
    options_json    : str # json
    ability_type    : str
    event_name      : str
    prompt_text     : str
    show_cancel     : bool
    replay_input    : str
    input_json      : str = field(default="{}") # client input result

    # LES REFUS (ajout du 10/09/2026) : les effets ECARTES de cette question,
    # au meme format que `options_json`, chacun avec sa `failure_reason`.
    #
    # ⚠ CANAL SEPARE, ET C'EST TOUT L'INTERET. `options_json` ne bouge pas :
    # le pilote d'autoplay, le harnais des cas et le plateau existant
    # continuent de ne voir que le jouable. Ce champ n'existe que pour
    # repondre a « pourquoi je ne peux pas jouer cette carte ? », et rien
    # d'autre ne doit s'en servir pour decider quoi que ce soit.
    refus_json      : str = field(default="[]") # json, meme forme que options_json

class DeviceManager:

    def __init__(self) -> None:
        from engine.device.manager.timer import Timer
        from engine.device.manager.notifier import SynchronizationNotifier
        self.timer = Timer()

        self.asking_players: List[int] = [] # 0,1,2,3
        self.ask_options: Dict[int, AskOptionPayload] = {}

        self.notify = SynchronizationNotifier()

        self.controllers: List['Controller'] = []

        # Mode bac a sable : commandes deposees par le serveur web (donc par un
        # AUTRE fil) et executees par le fil du JEU, au moment ou il attend une
        # entree joueur. Muter le monde depuis le fil HTTP est impossible : le
        # gestionnaire de taches du moteur n'accepte plus de travail a ce
        # moment-la (« cannot schedule new futures after shutdown »).
        self.sandbox_commands: List[str] = []
        self.sandbox_executor: 'Callable[[List[str]], None]|None' = None
        self.sandbox_last_error: str = ""

        # Pause manuelle (tache 1, ronde de correction 1) : une bascule de
        # `World.BasculerPauseManuelle` reste a PUBLIER (un rendu doit sortir
        # avec le nouvel etat) une fois posee. Sans ce marqueur, reveiller
        # `notify.input` seul ne suffit pas : le predicat de `DoGetInput.Wait`
        # (plus bas) ne teste ni une vraie entree, ni une sortie demandee, ni
        # des commandes en attente -- rien de ce qu'une bascule pose -- et le
        # fil se rendort aussitot, predicat toujours faux. `check_fn` teste
        # CE marqueur au meme titre que `sandbox_commands`.
        self.pause_a_publier: bool = False

        # Tache 8 : la RAISON du `None` que `DoGetInput` rend, pas le fait
        # qu'il en rende un. `DoGetInput` rend `None` pour QUATRE raisons
        # tres differentes -- une bascule de pause, un geste manuel draine,
        # une entree arrivee pour un AUTRE joueur, une sortie d'attente
        # demandee (console, rejeu, arret) -- et seules les DEUX PREMIERES
        # ont change l'etat du monde sans qu'aucun rendu ne le publie. Ce
        # marqueur les distingue, pour que `Controller.ChoiceOne` ne force un
        # rendu QUE dans ces deux cas-la : forcer a chaque `None` changerait
        # le rythme de rendu de chemins etrangers a la pause (une expiration
        # de minuterie, un rejeu), ce que ce chantier n'a pas a faire.
        #
        # ⚠ SEPARE DE `pause_a_publier` A DESSEIN, et ce n'est pas un
        # doublon : les deux marqueurs ont des consommateurs differents.
        # `pause_a_publier` est consomme par `DoGetInput` lui-meme (« un
        # reveil et un seul »), celui-ci par `ChoiceOne` UNE FOIS REMONTE de
        # `DoGetInput` (« un rendu force et un seul »). Les fondre ferait que
        # le premier a consommer aveuglerait le second.
        self.rendu_a_forcer: bool = False

    def ConsommerRenduAForcer(self) -> bool:
        """Rend vrai UNE SEULE FOIS par cause, et remet le marqueur a plat.

        Appele par `Controller.ChoiceOne` quand `GetInput` a rendu `None`,
        pour savoir s'il doit forcer un rendu avant de laisser l'appelant
        reposer sa question. Consommer ICI (et pas seulement lire) garantit
        qu'une bascule ou un drainage produit AU PLUS un rendu force, jamais
        un rendu a chaque tour de la boucle de re-pose.
        """
        if not self.rendu_a_forcer:
            return False
        self.rendu_a_forcer = False
        return True

    def QueueSandboxCommands(self, commands: List[str]) -> None:
        """Depose des commandes Puzzle.* ; appele depuis le fil du serveur web."""
        self.sandbox_commands += commands
        # Reveille le fil du jeu, qui dort dans DoGetInput.
        self.notify.input.NotifyAll()

    def SignalerPauseAPublier(self) -> None:
        """Marque qu'une bascule de pause reste a publier, et reveille le fil
        du jeu -- MEME reveil que `QueueSandboxCommands` (`notify.input`),
        appele depuis le MEME fil HTTP par `World.BasculerPauseManuelle`.

        Rien a executer ici (a la difference d'une commande bac a sable) :
        juste un rendu a produire au prochain reveil de `DoGetInput`, qui
        rendra la main sans entree et laissera l'appelant reposer sa
        question -- ce qui produit ce rendu.

        ⚠ CORRECTIF (tache 8) : « ce qui produit ce rendu » etait FAUX pour
        toutes les questions sauf celles du tour de heros. La re-pose ne
        passe que par `SenderPlayer.PlayerOnEvent_Text`, qui n'appelle
        `Present` que pour un `Message.WhenPlayerInTurn` : sur le mulligan ou
        une fenetre d'interruption, la question etait bien re-posee mais
        AUCUN rendu n'avait lieu entre les deux, et `/get_world` continuait
        de servir la trame precedente avec `manuel_actif` a faux. D'ou
        `rendu_a_forcer` : c'est desormais `Controller.ChoiceOne` qui force
        le rendu, au lieu de compter sur un rendu qui n'existait pas.
        """
        self.pause_a_publier = True
        self.rendu_a_forcer = True
        self.notify.input.NotifyAll()

    def PasserQuestionCourante(self) -> str:
        """Passe la question EN COURS pour le joueur interroge (tache 5,
        dernier recours de la pause manuelle : la QUESTION est fautive, pas
        la table -- la pause seule n'en libere pas, puisque le fil du jeu la
        reposerait a l'identique a la reprise).

        APPELEE DEPUIS LE FIL HTTP (route POST /manuel_passer), au meme
        titre que `QueueSandboxCommands`/`SignalerPauseAPublier` ci-dessus --
        et ce N'EST PAS un troisieme mecanisme. C'est EXACTEMENT le chemin
        qu'un clic normal sur le bouton « Passer »/« Annuler » emprunte deja
        (`interaction.ts::annuler` -> `envoyerReponse(id, null)` -> corps
        `"{}"` -> `POST /post` -> `GameServerSync.handle_post` ->
        `WhenInput`, DEJA appele depuis ce meme fil HTTP aujourd'hui). Cette
        methode ne fait qu'emprunter ce chemin a la place du joueur, jamais
        un chemin nouveau : `WhenInput` ne touche a rien du MONDE, seulement
        a la comptabilite du `DeviceManager` lui-meme (`ask_options`,
        `asking_players`) plus un reveil de `notify` -- rien de ce que l'en-
        tete de `__init__` interdit au fil HTTP.

        ⚠ N'INVENTE JAMAIS UNE REPONSE QUE LE MOTEUR N'A PAS OFFERTE. Une
        question FORCEE (`AskOptionPayload.show_cancel` faux, pose par
        `is_forced == False` en `controller.py:353`) n'offre AUCUNE sortie :
        le moteur EXIGE une reponse. Lui envoyer quand meme "{}" romprait la
        partie bien plus surement que le bug que le joueur essayait de
        contourner (voir `controller.py:388-390` : sur une question a
        plusieurs options FORCEE, un id absent viole l'assertion qui
        n'accepte id=0 que pour une question a UNE SEULE option). Le refus
        dit pourquoi, il ne fabrique rien.

        Rend un CODE STABLE, jamais une phrase -- meme convention que
        `Controller.NormaliserLeMotif`/`raisons-refus.ts` cote plateau, qui
        ecrivent la phrase dans la langue du joueur :
        - "ok"              : la question a ete passee (WhenInput appele).
        - "aucune_question" : personne n'est interroge en ce moment.
        - "question_forcee" : une question EST en attente mais n'offre pas
          d'annulation -- au joueur d'y repondre, pas de la contourner.
        """
        if not self.asking_players:
            return "aucune_question"
        # ⚠ PORTE, PAS UN REPLI (ronde de correction 1) : au plus UNE entree
        # dans `asking_players` est un INVARIANT du moteur, pas une
        # supposition de confort. Preuve etablie par le relecteur en lisant
        # le code HORS de ce diff : le seul appel a `GetInput`/`DoGetInput`
        # de tout le moteur est `Controller.ChoiceOne` (controller.py:346),
        # synchrone et bloquant sur l'UNIQUE fil de jeu, et le seul `.append`
        # sur `asking_players` est celui que `DoGetInput` fait lui-meme
        # (plus bas dans ce fichier) -- deux questions reelles simultanees
        # sont donc impossibles aujourd'hui. Si cet invariant se rompait un
        # jour, prendre `asking_players[0]` en silence passerait la question
        # d'UN AUTRE joueur a sa place : un defaut bien pire, et bien plus
        # dur a detecter, qu'un plantage net ici.
        assert len(self.asking_players) == 1, (
            f"invariant rompu : {len(self.asking_players)} joueurs "
            f"interroges a la fois ({self.asking_players!r}) -- "
            "PasserQuestionCourante ne sait viser qu'UNE question, et "
            "refuse de deviner laquelle plutot que de risquer de passer "
            "celle d'un autre joueur"
        )
        player_id = self.asking_players[0]
        if not self.ask_options[player_id].show_cancel:
            return "question_forcee"
        self.WhenInput("{}", player_id)
        return "ok"

    def DrainSandboxCommands(self) -> List[str]:
        """Execute les commandes en attente, UNE PAR UNE. A n'appeler QUE depuis
        le fil du jeu.

        CORRECTIF (revue finale du 18/09/2026, constats 2 et 3) : rend la
        liste des commandes REELLEMENT appliquees au monde, dans l'ordre. Une
        commande qui leve arrete le lot tout de suite ; celles deja
        appliquees avant elle restent dans la liste rendue, les suivantes ne
        sont jamais tentees. Avant ce correctif, un lot execute EN UN SEUL
        APPEL a `sandbox_executor` pouvait laisser la premiere commande
        appliquee au monde mais l'exception de la seconde faisait perdre les
        DEUX a l'appelant (aucune trace pour la sauvegarde), et un instantane
        de `sandbox_commands` pris avant l'appel pouvait aussi manquer une
        commande deposee par le fil HTTP entre les deux. La liste rendue ici
        est desormais la SEULE source de verite : plus d'instantane a cote.

        ⚠ Une liste vide est fausse et une liste pleine est vraie en Python :
        l'appelant historique (`DoGetInput`, plus bas) qui testait l'ancien
        booleen garde le meme sens - "rien n'a ete traite" vs "quelque chose
        a ete traite", meme quand ce "quelque chose" a echoue des la
        premiere commande.
        """
        if not self.sandbox_commands or self.sandbox_executor is None:
            return []
        commands, self.sandbox_commands = self.sandbox_commands, []
        appliquees: List[str] = []
        erreur = ""
        for commande in commands:
            try:
                self.sandbox_executor([commande])
            except Exception as exc:
                erreur = f"{type(exc).__name__}: {exc}"
                Log.Print(f"[sandbox] {erreur}")
                break
            appliquees.append(commande)
        self.sandbox_last_error = erreur
        return appliquees

    ################################################################################
    #
    def CreateDevices(self, controller: 'Controller') -> Tuple['OutputDevice', 'InputDevice']:
        ...

    def AddController(self, controller: 'Controller'):
        self.controllers.append(controller)

    ################################################################################
    #
    def OnNewGame(self):
        Log.DebugSilent(CATEGORY_NAME, "DeviceManager new game")
        self.ExitWait()
        self.notify.RefreshExitWait()

    def OnRestart(self):
        Log.DebugSilent(CATEGORY_NAME, "DeviceManager restart")
        self.ExitWait()

    def OnShutdown(self):
        Log.DebugSilent(CATEGORY_NAME, "DeviceManager Shutdown")
        self.ExitWait()

    ################################################################################
    #
    def ExitWait(self):
        self.asking_players = []
        self.notify.ExitWait()

    def WhenInput(self, post_json: str, player_id: int):
        self.asking_players.remove(player_id)
        self.ask_options[player_id].options_json = ""
        self.ask_options[player_id].input_json = post_json
        self.notify.WhenInput()

    def AfterSync(self):
        self.notify.RefreshExitWait()

    ################################################################################
    #
    def DoWaitConnect(self, player_id: int, check: Callable[[], bool]):
        def check_fn():
            if self.notify.should_exit_wait:
                return True
            return check()

        self.notify.connect.Wait(check_fn, None)
        # Log.Info(CATEGORY_NAME, f"[Client] Player {self.player_id} Connect")
        return

    def DoGetInput(self, data: 'AskOptionPayload', player_id: int, check: Callable[[], bool]):
        from core.lib import Time

        self.notify.RefreshExitWait()
        self.ask_options[player_id] = data
        self.asking_players.append(player_id)
        self.notify.has_client_input = False

        wait = self.timer.max_timeout
        if wait <= 0:
            wait = None
        self.timer.start_time = Time.GetTime()

        def check_fn():
            if self.notify.should_exit_wait:
                return True
            if self.asking_players == []:
                return True
            ask_option = self.ask_options[player_id]
            if ask_option.input_json != "{}":
                return True
            # Bac a sable : une commande en attente reveille aussi le fil du jeu.
            if self.sandbox_commands:
                return True
            # Pause manuelle (tache 1, ronde de correction 1) : une bascule en
            # attente de publication reveille aussi le fil du jeu, au meme
            # titre qu'une commande en attente -- sans cette ligne, le reveil
            # que pose `SignalerPauseAPublier` ne produit RIEN : le predicat
            # reste faux et le fil se rendort aussitot.
            if self.pause_a_publier:
                return True

            return check()

        no_time_out = self.notify.input.Wait(check_fn, wait)
        if not no_time_out:
            self.asking_players.remove(player_id)

        # On execute ICI, hors du predicat d'attente (donc sans tenir le verrou
        # de la condition) mais bien sur le fil du jeu. Puis on rend la main :
        # aucune entree joueur n'est arrivee, l'appelant redemandera.
        if self.DrainSandboxCommands():
            # Tache 8, meme famille que la pause ci-dessous : un geste manuel
            # applique au monde PENDANT une question ouverte n'est publie par
            # personne sur ce chemin (la re-pose de la question ne rend que
            # pour un `WhenPlayerInTurn`). `ManualLoop`, elle, force deja son
            # rendu apres chaque drainage -- c'est pourquoi le marqueur est
            # pose ICI, dans la branche qui REND LA MAIN a `ChoiceOne`, et
            # non dans `DrainSandboxCommands` que `ManualLoop` appelle aussi
            # (elle l'armerait sans que personne ne vienne le consommer).
            self.rendu_a_forcer = True
            self.timer.start_time = None
            self.notify.has_client_input = False
            if player_id in self.asking_players:
                self.asking_players.remove(player_id)
            return None

        # Meme protocole que ci-dessus, pour la pause : rien a executer (le
        # booleen est deja pose par `World.BasculerPauseManuelle`), juste la
        # main a rendre SANS entree pour que l'appelant reposant sa question
        # produise le rendu qui publie le nouvel etat. Consommee ICI (une
        # bascule = au plus un reveil force), jamais un reveil permanent.
        if self.pause_a_publier:
            self.pause_a_publier = False
            self.timer.start_time = None
            self.notify.has_client_input = False
            if player_id in self.asking_players:
                self.asking_players.remove(player_id)
            return None

        self.timer.start_time = None
        self.notify.has_client_input = False

        if player_id in self.asking_players:
            self.asking_players.remove(player_id)
            # When anyone has inputted, process it first
            return None

        input_json = self.ask_options[player_id].input_json
        return input_json

    def DoWaitSync(self, player_id: int, check: Callable[[], bool]):
        from core.lib import Time
        Log.DebugSilent("SYNC", f"WaitSync start")
        wait = self.timer.max_timeout
        if wait <= 0:
            wait = None
        self.timer.start_time = Time.GetTime()

        def check_fn():
            if self.notify.should_exit_wait:
                Log.DebugSilent("SYNC", f"WaitSync Exit: Force")
                return True
            return check()

        self.notify.sync.Wait(check_fn, wait)

        self.timer.start_time = None
        self.notify.has_client_input = False
        Log.DebugSilent("SYNC", f"WaitSync end")

