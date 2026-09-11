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

    def QueueSandboxCommands(self, commands: List[str]) -> None:
        """Depose des commandes Puzzle.* ; appele depuis le fil du serveur web."""
        self.sandbox_commands += commands
        # Reveille le fil du jeu, qui dort dans DoGetInput.
        self.notify.input.NotifyAll()

    def DrainSandboxCommands(self) -> bool:
        """Execute les commandes en attente. A n'appeler QUE depuis le fil du jeu."""
        if not self.sandbox_commands or self.sandbox_executor is None:
            return False
        commands, self.sandbox_commands = self.sandbox_commands, []
        try:
            self.sandbox_executor(commands)
            self.sandbox_last_error = ""
        except Exception as exc:
            self.sandbox_last_error = f"{type(exc).__name__}: {exc}"
            Log.Print(f"[sandbox] {self.sandbox_last_error}")
        return True

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

            return check()

        no_time_out = self.notify.input.Wait(check_fn, wait)
        if not no_time_out:
            self.asking_players.remove(player_id)

        # On execute ICI, hors du predicat d'attente (donc sans tenir le verrou
        # de la condition) mais bien sur le fil du jeu. Puis on rend la main :
        # aucune entree joueur n'est arrivee, l'appelant redemandera.
        if self.DrainSandboxCommands():
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

