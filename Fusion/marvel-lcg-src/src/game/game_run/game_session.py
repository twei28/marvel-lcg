from core import *
from core.lib import Time
from game.world import *
from game.scene import *
from game.game_run.game_new import NewGameDescriptor
from game.game_run.game_state import GameState
from engine.lib import Ver, Random, Json
from engine.log import Log
# from engine.task.condition import Condition
from engine.file import FileManager
from engine.controller import *
from engine.log import Notify
from game import *
from engine.config import ConfigVariables
from game.statistics.session_statistics import SessionStatistics

CATEGORY_NAME = "SESSION"

REPLAY_FOLDERS = ConfigVariables.Folders('replay_folders')

class GameSession:

    def __init__(self, game: 'Game') -> None:
        self.scene: Scene|None = None
        self.game_id = 0 # Undo will not update it
        # Ajout local : identifiant UNIQUE d'une partie a l'autre.
        #
        # `game_id` ne l'est pas : il repart de zero dans chaque processus, et
        # le serveur allume un moteur par partie. Deux parties successives
        # portaient donc le meme numero, et le plateau, qui s'en sert pour
        # savoir si son journal appartient encore a la partie affichee, gardait
        # celui de la partie precedente. Tire une fois, a la mise en place.
        self.game_uid = ""
        self.timeout = 0
        self.cheat = False
        self.version: Ver
        self.world: 'World|None' = None
        self.game = game
        # self.condition = Condition("State")

    def Restart(self, seed: int|None) -> None:
        assert self.scene
        self.SetScene(self.scene, 'New')
        if seed:
            self.scene.SetSeed(seed)

    def NewGame(self, new_game: 'NewGameDescriptor') -> None:
        from game.scene.loader import SceneLoader
        scene = SceneLoader.NewFromJson(
            new_game.campaign_json, new_game.encounter_set_names, new_game.hero_json,
            new_game.seed, new_game.rules, new_game.campaign_log,
            campaign_json_2=new_game.campaign_json_2,
            encounter_set_names_2=(new_game.encounter_set_names_2 or None),
            teams=new_game.teams,
        )
        self.SetScene(scene, 'New')
        assert self.scene
        self.timeout = new_game.timeout

        self.scene.campaign.SetChallenge(*new_game.challenges)
        # self.scene.campaign.custom_script = new_game.custom_script

    def SetScene(self, scene: 'Scene', state: 'GameState.START_STATE'):
        self.scene = scene
        self.version = Ver(scene.version)
        self.game_id += 1
        self.start_time = Time.GetTime()
        # Pris ICI et nulle part ailleurs : `start_time` ne ferait pas l'affaire,
        # GetPlayTime et Undo le reecrivent en cours de partie.
        self.game_uid = "%x" % int(self.start_time * 1000)
        self.game.state.SetStartState(state)

    ################################################################################
    #
    def GameSetup(self, controller_manager: 'ControllerManager', state: 'GameState') -> bool:
        from game.message import Message

        Message.TextLog(f"\n--- Game Start ---")
        self.statistics = SessionStatistics()

        max_timeout = self.timeout
        scene = self.scene
        assert scene

        player_num = len(scene.players)

        controller_manager.Setup(player_num, max_timeout, scene, state.start_state)
        state.ResetStartState()

        # self.condition.NotifyAll()

        if scene.seed == -1:
            scene.SetSeed(Random.RandomSeed())
        else:
            Random.SetSeed(scene.seed)

        from_undo = state.exit_state.is_undo_exit

        from game.test import Test
        if not Test.IsInTesting() and not from_undo:
            campaign = scene.campaign
            Log.DebugInfo(CATEGORY_NAME, f"Replay:      {scene.name}")
            Log.DebugInfo(CATEGORY_NAME, f"File:        {scene.path}")
            Log.DebugInfo(CATEGORY_NAME, f"Seed:        {scene.seed}")
            Log.DebugInfo(CATEGORY_NAME, f"Timeout:     {max_timeout}")
            Log.DebugInfo(CATEGORY_NAME, f"Scene:       {scene.campaign.name}")
            Log.DebugInfo(CATEGORY_NAME, f"Expert:      {campaign.expert}")
            Log.DebugInfo(CATEGORY_NAME, f"Modular:     {campaign.encounter_sets}")
            # Log.DebugInfo(CATEGORY_NAME, f"Script:    {campaign.custom_script}")
            Log.DebugInfo(CATEGORY_NAME, f"Challenge:   {campaign.challenges}")
            Log.DebugInfo(CATEGORY_NAME, f"Rule:        {scene.rules}")
            Log.DebugInfo(CATEGORY_NAME, f"Campaign Log:{scene.campaign.campaign_log}")

        if scene.is_puzzle:
            self.version.CheckPuzzle()
        else:
            self.version.VerifyVersion()

        self.world = World(scene, controller_manager.controllers)
        self.world.rule.SetRule(scene.rules, scene.is_puzzle, scene.seed)

        state.SetRunningState(True)

        if not Test.IsInTesting():
            controller_manager.WaitConnect()

        Log.ResetTime()

        self.world.Initialize()

        if self.world.scene.is_puzzle:
            from game.puzzle import PuzzleHelper
            PuzzleHelper.Exec(self.world.scene.puzzle, self.world)

        if self.world.rule.mode_manuel:
            # Le silence commence ICI, avant le rejeu : les gestes ont ete
            # appliques porte fermee, ils doivent se rejouer porte fermee,
            # sinon l'etat rechargé diverge de l'etat sauvegarde.
            self.world.manuel_actif = True
            if self.world.scene.manuel_commands:
                from game.puzzle import PuzzleHelper
                # CORRECTIF (revue finale du 18/09/2026, constat 4) : chaque
                # geste est rejoue INDIVIDUELLEMENT, sous try/except. Le
                # rejeu EN DIRECT (dans `World.ManualLoop`, via
                # `DeviceManager.DrainSandboxCommands`) est deja protege ;
                # celui-ci, a la mise en place, ne l'etait pas. Un geste qui
                # levait au RECHARGEMENT (une carte corrigee entre-temps, par
                # exemple) faisait remonter l'exception hors de `GameSetup` :
                # la sauvegarde devenait inouvrable, et l'annulation - qui
                # passe par ce meme chemin - inutilisable avec elle. Une
                # table legerement fausse se corrige a la main ; une
                # sauvegarde inouvrable ne se corrige pas du tout.
                for geste in self.world.scene.manuel_commands:
                    try:
                        PuzzleHelper.Exec([geste], self.world)
                    except Exception as exc:
                        Log.Warn(CATEGORY_NAME,
                                 f"rejeu du geste manuel echoue, ignore : {geste!r} "
                                 f"({type(exc).__name__}: {exc})")

        return not self.world.is_game_over

    ################################################################################
    #
    def GetPlayTime(self, scene: 'Scene') -> float:
        playtime = Time.GetTime() - self.start_time + scene.playtime
        self.start_time = Time.GetTime()
        return playtime

    ################################################################################
    #
    def DumpSave(self, report: str|None=None, clients: List[str]|None=None) -> str:
        scene = self.scene
        assert scene

        playtime = self.GetPlayTime(scene)
        scene.PrepareSave(self.game, playtime=playtime, report=report, clients=clients)

        data = Json.SaveString(scene, ignore_check_sum=False)
        return data

    def SaveScene(self, name: str|None=None, *, ex_save_name: str|None=None, delete_old: bool) -> str|None:
        from game.test import Test

        scene = self.scene
        assert scene

        old_file_path = None
        save_ok = False

        # We just move, not delete
        if delete_old:
            old_file_path = scene.path
            if scene.comment != "DONT_AUTO_SAVE_THIS":
                ver = scene.version
                FileManager.MoveFile(old_file_path, f"./replays_{ver}")
                Log.Info(CATEGORY_NAME, f"Moved: {old_file_path}")

        if name == None:
            replays_folder = FileManager.GetDirName(scene.path)
            if replays_folder == "." or replays_folder == "":
                replays_folder = REPLAY_FOLDERS.value[0]
            save_name = f'{scene.GetSaveFileName()}.json'
            file_name = FileManager.JoinPath(f'{replays_folder}', save_name)
        else:
            file_name = name

        if not Test.IsInTesting():
            playtime = self.GetPlayTime(scene)
        else:
            playtime = None

        if scene.Save(file_name, self.game, playtime=playtime):
            save_ok = True
            if ex_save_name != None:
                scene.Save(ex_save_name, self.game, playtime=playtime)

        if save_ok:
            return file_name
        else:
            return None

    ################################################################################
    #
    def Seed(self, num: int = -1):
        if self.scene:
            self.scene.SetSeed(num)

    def SkipTo(self, index: int|Literal["Round", "Turn", "Phase"]):
        self.game.controller_manager.skip.SetSkipTo(index)
        self.game.controller_manager.skip.SetIsSkipping(True)

    def StepTo(self, index: int):
        self.game.controller_manager.skip.SetSkipTo(index)

    ################################################################################
    #
    def Undo(self, undo: int):
        if self.world:
            self.world.game_over.SetUndo()
        self.ExitWait()
        skip_to = self.game.controller_manager.replay.current_step_id - undo
        self.game.ApplyHistoryInput()
        self.game.controller_manager.skip.SetSkipTo(skip_to)
        self.game.controller_manager.replay.Clear()
        self.game.state.SetStartState('Undo')
        self.start_time = Time.GetTime()
        # game.controller_manager.replay.SetIsSkipping()

    def AnnulerDernierGeste(self) -> bool:
        """Retire le dernier geste manuel et rejoue la partie sans lui.

        ⚠ Rien a voir avec `Undo`, qui rejoue les ENTREES du joueur : en mode
        manuel il n'y en a aucune. Ici on rejoue la mise en place, puis la
        liste des gestes amputee de son dernier element.

        Rend faux s'il n'y a rien a annuler, pour que l'appelant puisse le dire
        au joueur au lieu de relancer une partie pour rien.
        """
        scene = self.scene
        if scene is None or not scene.manuel_commands:
            return False
        scene.manuel_commands.pop()
        # CORRECTIF (revue finale du 18/09/2026, constat 1) : sans cet appel,
        # `scene.inputs` reste tel quel (vide, sur une partie jamais
        # sauvegardee) et `LoadScene` -> `GameSetup` rejoue la mise en place
        # en REDEMANDANT chaque question au joueur au lieu de rejouer les
        # reponses deja donnees. `Undo` (juste au-dessus) fait deja cet appel
        # avant de recharger : meme geste ici.
        self.game.ApplyHistoryInput()
        # DEUXIEME MOITIE DU MEME CORRECTIF, constatee a l'execution : peupler
        # `scene.inputs` NE SUFFIT PAS. `ControllerManager.InitializeSkip`
        # (engine/controller/manager.py:70) n'active le rejeu SILENCIEUX des
        # entrees, pour l'etat "Load", que si `skip.skip_to` est deja NEGATIF
        # au moment de l'appel (il calcule alors
        # `len(scene.inputs) + 1 + skip_to`) - c'est la MEME convention que
        # `GameSession.Load` utilise deja pour un chemin de sauvegarde suffixe
        # `:-1` (rejouer jusqu'au bout sans redemander). Sans elle,
        # `skip.skip_to` restait a 0 (jamais negatif dans une partie live) et
        # CHAQUE question de la mise en place repassait par `DoGetInput`, meme
        # avec l'historique correctement repeuple : un temoin qui compte les
        # questions posees (pas seulement l'etat final de la carte) le voit
        # immediatement.
        self.LoadScene(scene, -1, "Load")
        return True

    def Load(self, json_path: str, skip_to: int|None, state: Literal["Replay", "Load"]):

        if json_path == "":
            return

        if state == "Load":
            self.ExitWait()

        break_on: List[int] = []

        def extract_info(input_string: str) -> Tuple[str, List[int]]:
            parts = input_string.split(':')

            path = parts[0]
            start_id = 1
            if len(path) == 1:
                path += ":" + parts[1]
                start_id += 1

            numbers = [int(num) for num in parts[start_id:]]
            return path, numbers

        import re
        if re.match(r".*?:-?\d+$", json_path):
            json_path, skip_to_list = extract_info(json_path)
            break_on = skip_to_list
            if skip_to == None:
                skip_to = skip_to_list[0]

        file_path = FileManager.FindJsonPath('Replay', json_path, nullable=True)
        if file_path:
            scene = SceneLoader.Load(file_path)
            if scene:
                self.LoadScene(scene, skip_to, state, break_on)
                Notify.Command(f"Load: {file_path}")

    def LoadScene(self, scene: 'Scene', skip_to: int|None, state: 'GameState.START_STATE', break_on: List[int]=[]):
        if self.game.state.is_running and self.world:
            self.world.game_over.SetExit()

        self.SetScene(scene, state)
        # Load scene will not update timeout
        # game.scene.timeout = 0
        self.ExitWait()

        if skip_to:
            self.game.controller_manager.skip.SetSkipTo(skip_to)
        self.game.controller_manager.replay.Clear()
        self.game.controller_manager.replay.SetBreakOn(break_on)
        self.game.state.SetStartState(state)

    def ExitWait(self):
        from game.test import Test
        Test.Exit()
        self.game.controller_manager.device_manager.ExitWait()

    # def WaitUntilGameInitialize(self):
    #     def check():
    #         return self.game.state.start_state == ''

    #     self.condition.Wait(check)

