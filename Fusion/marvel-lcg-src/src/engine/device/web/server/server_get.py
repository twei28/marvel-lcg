from core import *
from engine.lib import Json
from engine.file import FileManager
from engine.device import *

from aiohttp import web
from engine.device.web.server.server_base import GameServerBase
from engine.config import ConfigVariables

READ_ONLY_FIRST_REPLAY_FOLDER   = ConfigVariables.Bool('read_only_first_replay_folder', True)
CARDS_JSON_FILE         = ConfigVariables.File('cards_json_file')
REPLAY_FOLDERS          = ConfigVariables.Folders('replay_folders')
# La fiche du mode Legacy, separee par place comme l'historique et les hauts
# faits : la progression appartient au compte, pas au serveur.
LEGACY_FILE             = ConfigVariables.File('legacy_file', '../legacy.json')
# Les arts alternatifs de heros choisis par le titulaire de la table : meme
# cle que le stockage du navigateur (`mc_hero_art_v1`), mais portee par le
# compte pour suivre le joueur d'un appareil a l'autre.
ARTS_HEROS_FILE         = ConfigVariables.File('arts_heros_file', '../arts-heros.json')
DECK_FOLDERS            = ConfigVariables.Folders('deck_folders')
STARTER_DECK_FOLDER     = ConfigVariables.Folder('starter_deck_folder')
ENCOUNTER_SETS_FOLDERS  = ConfigVariables.Folders('encounter_sets_folders')
SCENARIOS_FOLDERS       = ConfigVariables.Folders('scenarios_folders')
CUSTOM_SCENARIOS_FOLDER = ConfigVariables.Folder('custom_scenario_folder')
PUZZLE_FOLDER           = ConfigVariables.Folder('puzzle_folder')
PUZZLE_TEST_FOLDER      = ConfigVariables.Folder('puzzle_test_folder')

# Livrets de regles et carnets de campagne. Hors de public/ a dessein : 169 Mo
# que l'archive de deploiement n'a pas a reexpedier a chaque fois. deployer.ps1
# les exclut du code et les synchronise a part, comme les scans de cartes.
DOSSIER_DOCUMENTS = './assets/docs'

class GameServerGet(GameServerBase):

    def ListFile(self, *folders: str, ext: str|None=None) -> web.Response:
        return web.json_response(FileManager.ListFiles(*folders, ext=ext))

    async def list_file(self, request: web.Request) -> web.Response:
        return self.ListFile(request.path)

    async def list_scenarios(self, request: web.Request) -> web.Response:
        return self.ListFile(*SCENARIOS_FOLDERS.value, CUSTOM_SCENARIOS_FOLDER.value)

    async def list_encounter_sets(self, request: web.Request) -> web.Response:
        return self.ListFile(*ENCOUNTER_SETS_FOLDERS.value)

    async def list_deck(self, request: web.Request) -> web.Response:
        return self.ListFile(*DECK_FOLDERS.value, ext=".json")

    async def save_deck(self, request: web.Request) -> web.Response:
        # Sauvegarde d'un deck construit dans l'editeur web (deck-builder.html).
        # Ecrit un JSON au meme format que deck/starter/*.json dans le premier
        # dossier de deck_folders : il devient alors visible via /list_deck et
        # chargeable via /get_hero_json (FindJsonPath('Hero') couvre ce dossier).
        import os
        import re
        import json as json_lib
        data = await request.json()
        deck = data.get('deck', None)
        if (type(deck) is not dict) or (not deck.get('hero')):
            return web.json_response({'error': 'Invalid deck'}, status=400)
        raw_name = str(data.get('file_name', '') or deck.get('name', '') or 'deck')
        file_name = re.sub('[^a-zA-Z0-9_-]+', '_', raw_name).strip('_')[:60] or 'deck'
        folder = (DECK_FOLDERS.value[0] if DECK_FOLDERS.value else './deck/custom/')
        os.makedirs(folder, exist_ok=True)
        path = FileManager.JoinPath(folder, f'{file_name}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json_lib.dump(deck, f, ensure_ascii=False, indent=4)
        return web.json_response({'result': 'saved', 'file': path})

    async def delete_deck(self, request: web.Request) -> web.Response:
        # Supprime un deck ecrit par /save_deck. Meme dossier, meme nettoyage du
        # nom : on ne peut donc viser ni un deck de base ni le dossier commun.
        import os
        import re
        data = await request.json()
        raw_name = str(data.get('file_name', '') or '')
        file_name = re.sub('[^a-zA-Z0-9_-]+', '_', raw_name).strip('_')[:60]
        if not file_name:
            return web.json_response({'error': 'Invalid name'}, status=400)
        folder = (DECK_FOLDERS.value[0] if DECK_FOLDERS.value else './deck/custom/')
        path = FileManager.JoinPath(folder, f'{file_name}.json')
        if not os.path.isfile(path):
            return web.json_response({'error': 'Deck not found'}, status=404)
        os.remove(path)
        return web.json_response({'result': 'deleted'})

    async def sandbox_command(self, request: web.Request) -> web.Response:
        # Mode bac a sable : execute une commande Puzzle.* sur la partie EN COURS.
        # Le moteur sait deja poser une carte en jeu, regler des PV, une menace,
        # un statut... via l'API Puzzle ; on l'expose ici plutot que de reecrire
        # ces mecaniques. Puzzle.Exec n'autorise QUE les appels `Puzzle.<methode>`
        # (il rejette tout le reste a l'analyse syntaxique), donc pas d'execution
        # de code arbitraire.
        from game.puzzle.puzzle import PuzzleHelper

        # ⚠ AGIR EXIGE UN SIEGE (ronde de correction 1 de la tache 10,
        # 20/09/2026). Cette route ECRIT SUR LA PARTIE EN COURS, et elle
        # n'avait aucune garde : tout client qui detient le mot de passe de la
        # TABLE, sans tenir le moindre siege, pouvait y deposer des `Puzzle.*`.
        #
        # ⚠ POURQUOI C'EST DE CE CHANTIER. Avant la pause, cette surface ne
        # s'ouvrait qu'en bac a sable ou en mode manuel DECLARE -- deux
        # parties qu'on choisit. La pause la rend vivante sur N'IMPORTE QUELLE
        # table ordinaire : c'est nous qui l'ouvrons, c'est a nous de la
        # refermer. Meme garde, meme refus (403) que `/manuel_pause` et
        # `/manuel_passer` plus bas ; le spectateur, lui, est deja arrete en
        # amont par `SpectateurPeutEcrire` (`web_server.py`).
        if not self.prouve_un_siege(request):
            return web.json_response({'error': 'aucun siege'}, status=403)

        data = await request.json()
        commands = data.get('commands', None)
        if isinstance(commands, str):
            commands = [commands]
        if not isinstance(commands, list) or not all(isinstance(c, str) for c in commands):
            return web.json_response({'error': 'commands must be a string or a list of strings'},
                                     status=400)

        world = self.game.world
        if world is None:
            return web.json_response({'error': 'no game in progress'}, status=409)

        # Validation syntaxique TOUT DE SUITE, pour repondre une erreur utile au
        # client : Exec refuse tout ce qui n'est pas un appel `Puzzle.<methode>`.
        import ast
        for command in commands:
            try:
                arbre = ast.parse(command)
            except SyntaxError as exc:
                return web.json_response({'error': f'SyntaxError: {exc}'}, status=400)
            for noeud in ast.walk(arbre):
                if not isinstance(noeud, ast.Call):
                    continue
                cible = noeud.func
                if not (isinstance(cible, ast.Attribute)
                        and isinstance(cible.value, ast.Name)
                        and cible.value.id == 'Puzzle'):
                    return web.json_response(
                        {'error': "only 'Puzzle.<method>(...)' calls are allowed"},
                        status=400)

        # L'execution revient au fil du JEU : on ne fait que deposer.
        jeu = self.game
        manager = self.device_manager
        manager.sandbox_executor = lambda cmds: PuzzleHelper.Exec(cmds, jeu.world)
        manager.QueueSandboxCommands(commands)

        return web.json_response({'result': 'queued', 'count': len(commands)})

    async def puzzle_objectif(self, request: web.Request) -> web.Response:
        """Le joueur coche un objectif LIBRE d'un puzzle (E3, 23/10/2026).

        Route dediee, et non `/sandbox_command` : un puzzle publie ne doit pas ouvrir toute l'API `Puzzle.*` a celui qui le resout. Elle
        n'accepte que `{"index": n}` sur une partie de puzzle, pour un objectif de type `free_text`, et depose la seule commande
        `Puzzle.ValidateObjective(n)`.
        """
        from game.puzzle.puzzle import PuzzleHelper

        if not self.prouve_un_siege(request):
            return web.json_response({'error': 'aucun siege'}, status=403)
        data = await request.json()
        index = data.get('index', None)
        if not isinstance(index, int) or isinstance(index, bool):
            return web.json_response({'error': 'index must be an integer'}, status=400)
        world = self.game.world
        if world is None:
            return web.json_response({'error': 'no game in progress'}, status=409)
        if not world.scene.is_puzzle:
            return web.json_response({'error': 'not a puzzle'}, status=409)
        objectifs = world.puzzle_objectives.items
        if not 0 <= index < len(objectifs) or objectifs[index].get('kind') != 'free_text':
            return web.json_response({'error': 'not a free objective'}, status=400)
        jeu = self.game
        manager = self.device_manager
        manager.sandbox_executor = lambda cmds: PuzzleHelper.Exec(cmds, jeu.world)
        manager.QueueSandboxCommands([f"Puzzle.ValidateObjective({index})"])
        return web.json_response({'result': 'queued'})

    async def manuel_pause(self, request: web.Request) -> web.Response:
        """Bascule la pause manuelle EN COURS DE PARTIE (tache 1).

        Refus : 403 a qui ne tient aucun siege (spectateur compris, arrete
        des `AddPostSecurity`), 409 sur une partie DECLAREE manuelle -- voir
        les deux gardes en tete du corps.

        Corps : {"actif": true|false}. AUCUN champ `qui` (ronde de
        correction 1, tache 3) : un champ que le plateau ne peut de toute
        facon pas renseigner honnetement (aucun pseudo atteignable, voir
        `triche.basculerPause`) est un chemin mort, et le bandeau ne dirait
        jamais que « quelqu'un » -- l'inverse du but de la tache. Le SERVEUR
        determine lui-meme qui a parle, a partir du siege que la requete
        PROUVE tenir (`nom_du_heros_qui_parle`, `server_base.py`), et pose le
        NOM DU HEROS de ce siege -- il dit plus aux autres joueurs qu'un
        pseudo. Siege indetermine (table locale sans sieges proteges,
        typiquement) : chaine vide, le bandeau dit « quelqu'un » comme avant.

        Ne fait qu'un seul appel a `World.BasculerPauseManuelle` -- ce fil
        (HTTP) ne doit toucher a RIEN d'autre du monde, cf. le commentaire en
        tete de `engine/device/manager/base.py` et celui de
        `BasculerPauseManuelle`. La resolution du nom ci-dessus est une
        LECTURE (descripteur deja rendu), pas une ecriture : elle ne viole
        pas cette regle.
        """
        # ⚠ AGIR EXIGE UN SIEGE (I2 de la revue finale, 20/09/2026). Cette
        # route ARRETE OU REPREND LA PARTIE DE TOUTE LA TABLE : un client qui
        # ne tient aucun siege n'a pas a le faire. Meme refus que `/post`
        # (403), obtenu du meme `allowed_seats`. Le spectateur est deja arrete
        # en amont par `SpectateurPeutEcrire` (`web_server.py`) : ceci est le
        # second verrou, pas le premier.
        if not self.prouve_un_siege(request):
            return web.json_response({'error': 'aucun siege'}, status=403)

        data = await request.json()
        actif = data.get('actif', None)
        if not isinstance(actif, bool):
            return web.json_response({'error': 'actif must be a boolean'}, status=400)

        world = self.game.world
        if world is None:
            return web.json_response({'error': 'no game in progress'}, status=409)

        # ⚠ LA GARDE SYMETRIQUE DE `/manuel_passer` (revue finale, 20/09/2026).
        # Cette route ne concerne QUE les parties ORDINAIRES : une partie
        # DECLAREE manuelle est tenue muette par `World.ManualLoop`, qui pose
        # `manuel_actif` une fois pour toutes et ne le REPOSE JAMAIS. Un
        # `{"actif": false}` sur une telle partie eteindrait donc l'etat pour
        # de bon : le plateau redeviendrait bavard (demande centrale, bandeau
        # de phase, assistant) sur une partie que le moteur ne conduit plus,
        # et aucun bouton ne permettrait d'y revenir -- `BandeauPause` ne
        # s'affiche pas sur une partie declaree (`estEnPause`, `mode.ts`), et
        # « Mettre en pause » y est masque (`board.tsx`, `!modeManuelDeclare`).
        # Injoignable au clic, ferme quand meme : la route est publique.
        # Une fois repartie en automatique (`scene.reprise_auto`), elle est
        # redevenue ordinaire : la pause s'y pose et s'y leve comme ailleurs.
        if world.rule.mode_manuel and not world.scene.reprise_auto:
            return web.json_response({'error': 'partie declaree manuelle'}, status=409)

        qui = self.nom_du_heros_qui_parle(request) if actif else ''
        en_pause = world.BasculerPauseManuelle(actif, qui)
        return web.json_response({'result': 'en pause' if en_pause else 'repris'})

    async def manuel_reprise(self, request: web.Request) -> web.Response:
        """Rend la main au moteur sur une partie DECLAREE manuelle.

        Corps : {"phase": "heros"|"mechant"|"tour"} (voir
        `World.ReprendreEnAuto`). 403 sans siege ; 409 avec un code stable
        (`pas_manuel`, `phase_inconnue`, `mise_en_place_non_finie`) que le
        plateau traduit. Ne fait qu'un appel a `World.ReprendreEnAuto` : des
        affectations et un reveil, le travail se fait sur le fil du jeu.
        Pour une partie ordinaire mise en pause, c'est `/manuel_pause` qui
        reprend.
        """
        if not self.prouve_un_siege(request):
            return web.json_response({'error': 'aucun siege'}, status=403)

        data = await request.json()
        phase = data.get('phase', None)

        world = self.game.world
        if world is None:
            return web.json_response({'error': 'no game in progress'}, status=409)
        if not world.rule.mode_manuel or world.scene.reprise_auto:
            return web.json_response({'error': 'pas_manuel'}, status=409)
        if phase not in world.PHASES_DE_REPRISE:
            return web.json_response({'error': 'phase_inconnue'}, status=409)
        if not self.game.session.mise_en_place_finie:
            return web.json_response({'error': 'mise_en_place_non_finie'}, status=409)

        world.ReprendreEnAuto(phase)
        return web.json_response({
            'result': 'repris',
            'phase': phase,
            'par': self.nom_du_heros_qui_parle(request),
        })

    async def manuel_passer(self, request: web.Request) -> web.Response:
        """Passe la question fautive EN COURS DE PARTIE (tache 5) : l'echappatoire
        de dernier recours quand ce n'est pas la table qui bloque mais la
        QUESTION elle-meme -- la pause seule n'en libere pas puisqu'elle
        repose la meme question, a l'identique, a la reprise.

        Aucun corps de requete, sur le modele de `/manuel_undo` : il n'y a
        qu'une seule question EN COURS, celle que le moteur attend.

        Reserve a qui TIENT UN SIEGE (403 sinon : elle repond a la place du
        joueur interroge, c'est la plus grave des deux routes de pause) et a
        une partie EN PAUSE (`world.manuel_actif`) -- exactement le moment ou
        `BandeauPause` (le seul endroit qui appelle cette route) est visible. Hors pause, une question a `show_cancel` vrai est une
        DECISION DE JEU ORDINAIRE (« joue cette carte ou passe ») ; cette
        route n'est pas un raccourci pour la sauter a la place du joueur.

        ⚠ N'INVENTE JAMAIS UNE REPONSE. Voir `DeviceManager.PasserQuestionCourante`
        (engine/device/manager/base.py) : cette route ne fait que lire l'etat
        du `DeviceManager` et lui deleguer la decision -- elle ne touche
        JAMAIS a `self.game.world` au-dela de la LECTURE de `manuel_actif`,
        comme `manuel_pause` juste au-dessus.

        Le code de refus (`aucune_question`, `question_forcee`) est un CODE
        STABLE, jamais une phrase : c'est le PLATEAU qui l'ecrit en francais
        ou en anglais (meme convention que `failure_reason`/`raisons-refus.ts`,
        voir `Controller.NormaliserLeMotif`) -- le moteur ne parle pas la
        langue du joueur.
        """
        # ⚠ AGIR EXIGE UN SIEGE (I2, 20/09/2026) : celle-ci REPOND A LA PLACE
        # du joueur que le moteur interroge -- c'est la plus grave des deux.
        # Voir `manuel_pause` juste au-dessus pour le detail des deux verrous.
        if not self.prouve_un_siege(request):
            return web.json_response({'error': 'aucun siege'}, status=403)

        world = self.game.world
        if world is None:
            return web.json_response({'error': 'no game in progress'}, status=409)
        if not world.manuel_actif:
            return web.json_response({'error': 'pas en pause'}, status=409)

        code = self.device_manager.PasserQuestionCourante()
        if code != 'ok':
            return web.json_response({'error': code}, status=409)
        return web.json_response({'result': 'passe'})

    async def manuel_undo(self, request: web.Request) -> web.Response:
        """Ctrl+Z du mode manuel : retire le dernier geste et rejoue sans lui.

        Aucun corps de requete : il n'y a qu'un seul geste annulable, le
        dernier. Le plateau n'a donc rien a envoyer, et rien a tenir a jour de
        son cote.

        Refus : 403 a qui ne tient aucun siege (spectateur compris, arrete
        des `AddPostSecurity`), 409 hors pause ou sans rien a annuler.

        ⚠ L'ETAT, PAS LA REGLE -- et c'est un correctif (constat I3 de la
        ronde de correction 1 du 20/09/2026). Cette garde testait
        `rule.mode_manuel`, donc n'ouvrait qu'aux parties manuelles
        DECLAREES. Tant que les gestes d'une pause ORDINAIRE disparaissaient
        au rechargement, un `Puzzle.Damage(49, 300)` tape de travers finissait
        par s'effacer tout seul ; maintenant qu'ils SURVIVENT, il serait
        permanent et reapplique a chaque montage, sans aucune echappatoire.
        On ouvre donc la meme porte que `/manuel_passer` quatre methodes plus
        haut : `world.manuel_actif`, qui est vrai dans les DEUX cas (une
        partie declaree l'a pose une fois pour toutes apres sa mise en place)
        et faux hors pause -- ou annuler un geste n'aurait aucun sens.
        """
        # Meme garde de siege que `/sandbox_command` et les deux routes de
        # pause (ronde de correction 1, tache 10) : « Ctrl+Z » defait le
        # dernier geste DE LA TABLE, pas celui de qui le demande.
        if not self.prouve_un_siege(request):
            return web.json_response({'error': 'aucun siege'}, status=403)

        world = self.game.world
        if world is None or not world.manuel_actif:
            return web.json_response({'error': 'pas une partie manuelle'}, status=409)
        if not self.game.session.AnnulerDernierGeste():
            return web.json_response({'error': 'rien a annuler'}, status=409)
        return web.json_response({
            'result': 'annule',
            'restants': len(self.game.scene.manuel_commands),
        })

    async def list_starter_deck(self, request: web.Request) -> web.Response:
        return self.ListFile(STARTER_DECK_FOLDER.value)

    def _dossiers_replay_autorises(self) -> list[str]:
        return [REPLAY_FOLDERS.value[0]] if READ_ONLY_FIRST_REPLAY_FOLDER.value else list(REPLAY_FOLDERS.value)

    async def list_replay_files(self, request: web.Request) -> web.Response:
        return web.json_response(FileManager.ListFiles(*self._dossiers_replay_autorises()))

    async def delete_replay(self, request: web.Request) -> web.Response:
        # Suppression manuelle depuis "Reprendre une partie" (24/09/2026,
        # demande de l'utilisateur : la liste s'accumulait sans moyen de la
        # nettoyer). `nom` doit etre EXACTEMENT une entree de la liste que le
        # serveur vient de rendre -- pas un chemin reconstruit a partir de
        # morceaux envoyes par le client -- pour qu'aucune requete ne puisse
        # faire effacer un fichier hors des dossiers de replay autorises.
        donnees = await request.json()
        nom = str(donnees.get('nom') or '')
        if nom not in FileManager.ListFiles(*self._dossiers_replay_autorises()):
            return web.json_response({'error': f'sauvegarde introuvable : {nom}'}, status=404)
        import os
        os.remove(nom)
        return web.json_response({'result': 'deleted', 'nom': nom})

    async def list_puzzle_files(self, request: web.Request) -> web.Response:
        return self.ListFile(PUZZLE_FOLDER.value)

    async def list_puzzle_test_files(self, request: web.Request) -> web.Response:
        return self.ListFile(PUZZLE_TEST_FOLDER.value)

    def ReadReplayFile(self, file_path: str) -> web.Response:
        from game.scene.scene import Scene
        from cards.database import CardsDB
        replay, checksum = Json.LoadAsInternal(file_path, Scene)
        # ⚠⚠ NOM LISIBLE, PAS L'IDENTIFIANT BRUT (23/09/2026, demande de
        # l'utilisateur, capture a l'appui : « on comprend rien »). Cette
        # reponse alimentait jusqu'ici la liste "Resume a game" de l'assistant
        # avec des `card_id` tels quels ("01113", "03001a,03001b") -- illisible
        # pour un joueur. `CardsDB.FindCardPaper` PLANTE (`assert False`) sur
        # un id absent de la base courante : une sauvegarde d'une version
        # anterieure du moteur ne doit jamais faire echouer cette route pour
        # autant (meme principe que `charger_partie_interrompue`, qui ne leve
        # jamais). Repli sur l'id lui-meme si la carte est introuvable.
        def nom_lisible(card_id: str) -> str:
            # Le « * » en tete du nom imprime (carte unique) est un marqueur
            # de donnees, pas du texte a montrer : meme nettoyage que
            # `cleanName` cote assistant (public/js/prepare/catalog.js).
            #
            # `card_id` peut porter un id COMBINE recto/verso ("03001a,03001b")
            # : c'est le format que `HeroDescriptor.hero[0]` porte deja pour
            # une identite a deux faces, et que public/js/prepare/catalog.js
            # decoupe au meme endroit (`.split(",")[0]`, lignes ~101 et ~219).
            # Oublier ce decoupage ici faisait planter `FindCardPaper` (id
            # introuvable tel quel) et retomber sur l'id brut affiche cru dans
            # "Resume a game" (24/09/2026, capture a l'appui).
            id_seul = card_id.split(",")[0]
            try:
                return CardsDB.FindCardPaper(id_seul).name.lstrip("*").strip()
            except Exception:
                return card_id
        villain_id = replay.campaign.villain[0] if replay.campaign.villain else replay.campaign.schemes[0]
        return web.json_response({
            "version": replay.version,
            "is_puzzle": replay.is_puzzle,
            "time": replay.time,
            "cover": replay.cover,
            "path": replay.path,
            "comment": replay.comment,
            "villain": nom_lisible(villain_id),
            "players": [nom_lisible(x.hero[0]) for x in replay.players],
            "seed": replay.seed,
            "checksum": checksum == "Ok",
            "author": "",
            "step": len(replay.inputs),
        })

    def ReadPuzzleFile(self, file_path: str) -> web.Response:
        from engine.device.web.server.server_new_game import PuzzleData
        puzzle, checksum = Json.LoadAsInternal(file_path, PuzzleData)
        return web.json_response({
            "version": puzzle.version,
            "is_puzzle": True,
            "time": "",
            "cover": puzzle.cover,
            "path": file_path,
            "comment": puzzle.comment,
            "villain": puzzle.villain[0],
            "players": [puzzle.players[0].identities[0]],
            "seed": puzzle.seed,
            "checksum": checksum == "Ok",
            "author": puzzle.author,
            "step": 0,
        })

    async def read_file(self, request: web.Request) -> web.Response:
        file = request.rel_url.query_string
        return self.ReadJsonFile(file)

    async def get_encounter_set_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("EncounterSet", path)
        return self.ReadJsonFile(file)

    async def get_scenario_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Campaign", path)
        return self.ReadJsonFile(file)

    async def get_hero_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Hero", path)
        return self.ReadJsonFile(file)

    async def get_sets_json(self, request: web.Request) -> web.Response:
        file = FileManager.FindJsonPath("SetInfo", "sets_info.json")
        return self.ReadJsonFile(file)

    async def get_statistics_json(self, request: web.Request) -> web.Response:
        # Ajout local : statistiques globales (statistics.json) pour l'ecran de
        # stats du wizard.
        from game.statistics.game_statistics import GAME_STATISTICS_FILE
        import os
        if not os.path.exists(GAME_STATISTICS_FILE.value):
            return web.json_response({})
        return self.ReadJsonFile(GAME_STATISTICS_FILE.value)

    async def get_aspect_decks(self, request: web.Request) -> web.Response:
        # Packages d'aspect prefaits (« Reckless Aggression »...) et deck
        # conseille par heros. Ces 30 cartes ne forment pas un deck a elles
        # seules : l'assistant les assemble avec les cartes signature du heros.
        import os
        chemin = './data/decks_aspect.json'
        if not os.path.exists(chemin):
            return web.json_response({'packages': {}, 'recommandations': {}})
        return self.ReadJsonFile(chemin)

    async def get_achievements(self, request: web.Request) -> web.Response:
        # Etat complet des hauts faits : definitions, progression, dates.
        import json as json_lib
        import os
        from engine import Engine
        from game import achievements
        from engine.config import ConfigVariables

        history_file = ConfigVariables.File('games_history_file', 'games_history.json').value
        try:
            journal = json_lib.load(open(history_file, encoding='utf-8'))
            if not isinstance(journal, list):
                journal = []
        except Exception:
            journal = []

        stats = Engine.statistics.content
        # La galerie montre aussi la progression des hauts faits de campagne :
        # sans ce resume, ils s'afficheraient eternellement a zero.
        from engine.device.web.server.server_campagne import resume_campagnes
        return web.json_response(achievements.etat_complet(stats, journal, resume_campagnes()))

    async def get_partie_en_cours(self, request: web.Request) -> web.Response:
        """La fiche de la partie EN COURS sur ce moteur, pour la page de suivi
        du site (`/suivi`, orchestrateur). AJOUT du 08/09/2026.

        ⚠ Route SANS cookie de siege (l'orchestrateur n'en a pas), donc
        protegee par le jeton que le site a remis au moteur a l'allumage
        (`site_jeton`, server_base.py). Sans jeton configure (jeu local), on
        ne repond qu'a la boucle locale. Rien de nominatif ici : le site
        connait deja le proprietaire de la table.
        """
        from engine.device.web.server.server_base import SITE_JETON
        jeton = request.rel_url.query.get('jeton', '')
        if SITE_JETON.value:
            if jeton != SITE_JETON.value:
                return web.json_response({'error': 'jeton'}, status=403)
        elif (request.remote or '') not in ('127.0.0.1', '::1'):
            return web.json_response({'error': 'local'}, status=403)

        fiche = {'en_cours': False}
        try:
            game = self.controller_manager.game
            world = getattr(game, 'world', None)
            if world is None or not game.state.is_running or getattr(world, 'is_game_over', False):
                return web.json_response(fiche)
            from game.operate.worlds import Worlds
            campaign = getattr(getattr(game, 'scene', None), 'campaign', None)
            fiche = {
                'en_cours': True,
                # La version du MOTEUR qui joue cette partie. Le site la retient
                # avec la sauvegarde : un deploiement change souvent de version,
                # et une sauvegarde plus ancienne que la version minimale
                # supportee fait echouer le chargement (VerifyVersion).
                'version': str(getattr(getattr(game, 'session', None), 'version', '') or ''),
                'round': int(getattr(world, 'round_id', 0) or 0),
                'scenario': str(getattr(campaign, 'name', '') or ''),
                'expert': bool(getattr(campaign, 'expert', False)),
                'joueurs': [],
                'vilains': [],
                'manigances': [],
            }
            for player in world.const_players:
                identite = player.GetIdentity()
                heros = None
                try:
                    heros = player.GetHero()
                except Exception:
                    heros = None
                nom_heros = getattr(getattr(heros or identite, 'paper', None), 'name', '')
                fiche['joueurs'].append({
                    'heros': str(nom_heros or '').lstrip('* '),
                    'card_id': str(getattr(getattr(heros or identite, 'paper', None), 'card_id', '')),
                    'deck': str(getattr(player, 'hero_name', '') or ''),
                    'forme': 'Hero' if player.IsInHeroForm() else 'AlterEgo',
                    'pv': int(getattr(identite, 'health', 0) or 0),
                    'pv_max': int(getattr(identite, 'max_health', 0) or 0),
                    'elimine': bool(getattr(player, 'is_eliminated', False)),
                })
            for vilain in Worlds.GetAllVillains(world):
                fiche['vilains'].append({
                    'nom': str(getattr(vilain.paper, 'name', '')).lstrip('* '),
                    'pv': int(getattr(vilain, 'health', 0) or 0),
                    'pv_max': int(getattr(vilain, 'max_health', 0) or 0),
                    'stage': str(getattr(vilain.paper, 'desc', {}).get('Stage', '') if isinstance(getattr(vilain.paper, 'desc', None), dict) else ''),
                })
            for manigance in list(world.area_schemes_main.Get()):
                fiche['manigances'].append({
                    'nom': str(getattr(manigance.paper, 'name', '')),
                    'menace': int(getattr(manigance, 'threat', 0) or 0),
                })
        except Exception as exc:
            fiche = {'en_cours': False, 'erreur': type(exc).__name__}
        return web.json_response(fiche)

    async def get_games_history(self, request: web.Request) -> web.Response:
        # Ajout local : journal des parties terminees (voir game/rule/statistics.py).
        from engine.config import ConfigVariables
        import os
        history_file = ConfigVariables.File('games_history_file', 'games_history.json').value
        if not os.path.exists(history_file):
            return web.json_response([])
        return self.ReadJsonFile(history_file)

    async def get_sets_custom_scenario(self, request: web.Request) -> web.Response:
        files = FileManager.ListFiles(CUSTOM_SCENARIOS_FOLDER.value, ".json")
        return web.json_response(files)

    async def get_cards_json(self, request: web.Request) -> web.Response:
        # Le frontend a besoin des cartes personnalisees (Stan Lee...) au meme
        # titre que les officielles : sans elles il n'a ni nom, ni PV, ni image
        # pour ces cartes. On fusionne donc les fichiers custom par-dessus la
        # base, comme le fait CardsDB.Initialize.
        from cards.database import CardsDB
        if not CardsDB.cards_custom_files:
            return self.ReadJsonFile(CARDS_JSON_FILE.value)

        fusion: Dict[str, List] = {}

        def ajouter(chemin: str) -> None:
            data, _ = Json.LoadInternal(chemin)
            if not isinstance(data, dict):
                return
            for pack, cartes in data.items():
                if isinstance(cartes, list):
                    fusion.setdefault(pack, []).extend(cartes)

        ajouter(CARDS_JSON_FILE.value)
        for chemin in CardsDB.cards_custom_files:
            ajouter(chemin)
        return web.json_response(fusion)

    async def get_translate_json(self, request: web.Request) -> web.Response:
        from engine.lib import TransText
        return self.ReadJsonFile(TransText.translate_file)

    async def get_card_json(self, request: web.Request) -> web.Response:
        from cards.database import CardsDB
        name = request.rel_url.query_string
        paper = CardsDB.FindCardPaper(name)
        return web.json_response(paper)

    async def get_completion_rate(self, request: web.Request) -> web.Response:
        return web.Response(text=str(self.game.statistics.completion_rate))

    async def get_statistics(self, request: web.Request) -> web.Response:
        return web.json_response(self.game.statistics.content.data)

    async def get_session_statistics(self, request: web.Request) -> web.Response:
        return web.json_response(self.game.session.statistics.dic)

    async def get_play_scene_name(self, request: web.Request) -> web.Response:
        controller = self.get_first_controller(request)
        if controller.world:
            text = controller.world.scene.name
        else:
            text = ""
        return web.Response(text=text)

    async def get_max_timeout(self, request: web.Request) -> web.Response:
        return web.Response(text=str(self.device_manager.timer.max_timeout))

    async def get_puzzle_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Puzzle", path)
        assert file
        return self.ReadPuzzleFile(file)

    async def get_replay_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Replay", path)
        assert file
        return self.ReadReplayFile(file)

    async def marvelcdb_card(self, request: web.Request) -> web.Response:
        # Proxy OPTIONNEL vers fr.marvelcdb.com (textes officiels FR dans
        # l'apercu). Appele seulement si l'option reseau du client est active.
        # Cache memoire, timeout court : le jeu reste 100 % jouable hors ligne.
        import re
        import aiohttp
        code = request.rel_url.query_string.strip()
        if not re.fullmatch(r"\d{5}[a-z]?", code):
            return web.json_response({'error': 'bad code'}, status=400)
        if not hasattr(self, 'marvelcdb_cache'):
            self.marvelcdb_cache = {}
        if code in self.marvelcdb_cache:
            data = self.marvelcdb_cache[code]
            if data is None:
                return web.json_response({'error': 'not found'}, status=404)
            return web.json_response(data)
        try:
            timeout = aiohttp.ClientTimeout(total=6)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"https://fr.marvelcdb.com/api/public/card/{code}.json") as reponse:
                    if reponse.status != 200:
                        self.marvelcdb_cache[code] = None
                        return web.json_response({'error': 'not found'}, status=404)
                    brut = await reponse.json(content_type=None)
        except Exception:
            return web.json_response({'error': 'offline'}, status=502)
        data = {k: brut.get(k) for k in ('name', 'text', 'flavor', 'traits') if brut.get(k)}
        # ⚠ UNE CARTE NON TRADUITE NE DOIT PAS PASSER POUR DU FRANCAIS.
        #
        # Defaut signale en partie le 14/09/2026 : « je suis en FR et le texte
        # dans le tooltip sous la carte est en anglais............... ».
        # fr.marvelcdb.com REND L'ANGLAIS quand la traduction n'existe pas
        # (mesure : Hulk Shape 56033, Silk 52001a, Winter Soldier 54001a), et
        # rien dans la reponse ne le dit... sauf ceci : `text` et `real_text`
        # sont alors IDENTIQUES. Sur une carte traduite ils different
        # (Spider-Man 01001a : « Sens d'Araignee » contre « Spider-Sense »).
        #
        # On retire alors le texte plutot que de l'afficher : le client ne
        # montre son bloc que s'il y a un texte, et le joueur francais ne lit
        # plus d'anglais sous une carte. Le reste (nom, traits) est conserve :
        # un nom propre identique dans les deux langues n'a rien de faux.
        if brut.get('text') and brut.get('text') == brut.get('real_text'):
            data.pop('text', None)
            data['non_traduit'] = True
        self.marvelcdb_cache[code] = data
        return web.json_response(data)

    async def set_cursor(self, request: web.Request) -> web.Response:
        # Curseurs partages en multijoueur : chaque client envoie la position
        # de sa souris normalisee (0..1) par rapport a la scene du plateau.
        # Purement cosmetique, stocke en memoire, perime en 5 s.
        import time
        data = await request.json()
        try:
            p = int(data['p'])
            x = float(data['x'])
            y = float(data['y'])
        except Exception:
            return web.json_response({'error': 'p, x, y required'}, status=400)
        if not hasattr(self, 'cursors'):
            self.cursors = {}
        # `survol` : la carte sous le curseur (17/09/2026). Le spectateur voit
        # ainsi ce que le joueur REGARDE, pas seulement ou il pointe. Borne a
        # 40 caracteres : un card_id en fait moins de dix, et rien de ce qui
        # vient du reseau ne doit pouvoir grossir sans limite.
        # `clic` : identifiant du dernier clic (18/10/2026, pour l'onde du
        # spectateur). Un simple entier qui change a chaque clic ; un envoi de
        # position sans `clic` garde celui d'avant, sinon le mouvement suivant
        # l'effacerait avant que le spectateur l'ait lu.
        try:
            clic = int(data['clic'])
        except Exception:
            clic = self.cursors.get(p, {}).get('clic', 0)
        self.cursors[p] = {
            'x': x, 'y': y, 't': time.time(),
            'survol': str(data.get('survol', ''))[:40],
            'clic': clic,
        }
        from engine.enregistrement import Enregistrement
        Enregistrement.Evenement('c', {'p': p, 'x': round(x, 4), 'y': round(y, 4), 'clic': clic})
        return web.json_response({'result': 'ok'})

    async def get_cursors(self, request: web.Request) -> web.Response:
        import time
        cursors = getattr(self, 'cursors', {})
        now = time.time()
        frais = {
            p: {'x': c['x'], 'y': c['y'], 'survol': c.get('survol', ''), 'clic': c.get('clic', 0)}
            for p, c in cursors.items() if now - c['t'] < 5.0
        }
        return web.json_response(frais)

    # L'etape du cartouche de la phase du mechant que chaque joueur LIT, pour
    # que le spectateur affiche la meme (07/10/2026). Une trame retenue peut
    # porter deux etapes : le monde seul ne dit pas laquelle le joueur regarde.
    # Cosmetique comme les curseurs, mais sans peremption : un joueur peut
    # lire une etape longtemps sans bouger la souris.
    async def set_etape(self, request: web.Request) -> web.Response:
        import time
        data = await request.json()
        try:
            p = int(data['p'])
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)
        if not hasattr(self, 'etapes_lues'):
            self.etapes_lues = {}
        # `mode` : le mode de phase du joueur (08/10/2026), pour que le
        # spectateur voie la phase comme lui. Une valeur inconnue est ignoree.
        mode = data.get('mode')
        self.etapes_lues[p] = {'cle': str(data.get('cle') or '')[:200], 't': time.time(),
                               'mode': mode if mode in ('detaille', 'sur-table', 'instantane') else ''}
        # Refonte de la phase du mechant, lot 6 (multi, 12/10/2026) : les boosts deja
        # retournes sur l'etape lue, et la cle pour laquelle le joueur s'est dit
        # « pret » (choix « tout le monde valide »). Cosmetiques, comme le reste.
        try:
            boosts = int(data.get('boosts') or 0)
        except Exception:
            boosts = 0
        self.etapes_lues[p]['boosts'] = max(0, min(boosts, 50))
        self.etapes_lues[p]['pret'] = str(data.get('pret') or '')[:200]
        # La cle que ce joueur vient de VALIDER : celui qui suit la valide aussi,
        # sinon le moteur attendrait son accuse de reception a jamais.
        self.etapes_lues[p]['valide'] = str(data.get('valide') or '')[:200]
        from engine.enregistrement import Enregistrement
        Enregistrement.Evenement('e', {'p': p, 'cle': self.etapes_lues[p]['cle'], 'mode': self.etapes_lues[p]['mode']})
        return web.json_response({'result': 'ok'})

    async def get_etapes(self, request: web.Request) -> web.Response:
        return web.json_response(getattr(self, 'etapes_lues', {}))

    # QUI FAIT AVANCER LA PHASE DU MECHANT EN MULTI (refonte, lot 6, decisions 32-33) :
    # choisi par l'hote a la premiere phase du mechant, garde pour toute la partie,
    # modifiable ensuite. « concerne » : le joueur concerne (le premier joueur pour
    # les moments communs) ; « tous » : chacun se dit pret ; « quiconque » : le
    # premier qui clique. Vide : pas encore choisi.
    async def set_avance_phase(self, request: web.Request) -> web.Response:
        data = await request.json()
        politique = data.get('politique')
        if politique not in ('concerne', 'tous', 'quiconque'):
            return web.json_response({'error': 'politique inconnue'}, status=400)
        try:
            p = int(data.get('p'))
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)
        if p != 0:
            return web.json_response({'error': "seul l'hote choisit"}, status=403)
        self.avance_phase = politique
        return web.json_response({'result': 'ok', 'politique': politique})

    async def get_avance_phase(self, request: web.Request) -> web.Response:
        return web.json_response({'politique': getattr(self, 'avance_phase', '')})

    # CE QUE LE JOUEUR VOIT, pour le spectateur et la relecture (08/10/2026,
    # « voir 100 % de ce que le joueur a vu ») : sa selection dans une fenetre,
    # la carte qu'il agrandit, la pile qu'il ouvre, ses reglages (volume des
    # sons compris), la taille de son ecran, ses messages, ses menus (dont
    # ceux du mode manuel), son glisser, ses defilements. Un genre par
    # information, une valeur JSON bornee. Cosmetique comme les curseurs :
    # rien ne touche la partie. Enregistre en ligne « v ».
    GENRES_VUS = {'sel', 'loupe', 'pile', 'regl', 'ecran', 'msg', 'menu', 'manu',
                  'glis', 'defil'}
    TAILLE_VU_MAX = 4000
    # Les reglages : une vingtaine de cles, dont quelques-unes longues (art des
    # heros, noms des zones). Le client en ecarte deja toute valeur de plus de
    # 2000 caracteres.
    TAILLE_REGLAGES_MAX = 30000

    async def set_vu(self, request: web.Request) -> web.Response:
        import json
        import time
        data = await request.json()
        try:
            p = int(data['p'])
            g = str(data['g'])
        except Exception:
            return web.json_response({'error': 'p, g required'}, status=400)
        if g not in self.GENRES_VUS:
            return web.json_response({'error': 'genre inconnu'}, status=400)
        v = data.get('v')
        if len(json.dumps(v)) > (self.TAILLE_REGLAGES_MAX if g == 'regl' else self.TAILLE_VU_MAX):
            return web.json_response({'error': 'trop long'}, status=413)
        if not hasattr(self, 'vus'):
            self.vus = {}
        self.vus.setdefault(p, {})[g] = {'v': v, 't': time.time()}
        from engine.enregistrement import Enregistrement
        Enregistrement.Evenement('v', {'p': p, 'g': g, 'v': v})
        return web.json_response({'result': 'ok'})

    async def get_vus(self, request: web.Request) -> web.Response:
        vus = getattr(self, 'vus', {})
        return web.json_response({p: {g: e['v'] for g, e in genres.items()} for p, genres in vus.items()})

    async def get_enregistrement(self, request: web.Request) -> web.Response:
        """Le fichier .marvelreplay de la derniere partie jouee sur cette table."""
        from engine.enregistrement import Enregistrement
        contenu = Enregistrement.Fichier()
        if contenu is None:
            return web.json_response({'error': 'aucune partie enregistree'}, status=404)
        return web.Response(
            body=contenu,
            content_type='application/octet-stream',
            headers={'Content-Disposition': 'attachment; filename="partie.marvelreplay"'},
        )

    # --- Marques du mode manuel (07/10/2026) : cibles, fleches, surlignages ---
    # Comme OCTGN, ou elles sont vues de tous : Maj+clic cible (a la couleur de
    # qui cible), Maj+glisser trace une fleche, le pave numerique surligne. Rien
    # ne touche au moteur : un etat cosmetique, en memoire, remis a zero a chaque
    # nouvelle partie, borne en taille (rien du reseau ne grossit sans limite).
    COULEURS_SURLIGNAGE = {"bleu", "orange", "vert", "violet", "rouge", "noir", "blanc", "actif"}
    MARQUES_MAX = 200

    def _marques(self) -> dict:
        try:
            partie = str(getattr(self.controller_manager.game.session, "game_uid", "") or "")
        except Exception:
            partie = ""
        if getattr(self, "marques_partie", None) != partie or not hasattr(self, "marques"):
            self.marques_partie = partie
            self.marques = {"cibles": {}, "fleches": [], "surlignages": {}}
        return self.marques

    async def set_marque(self, request: web.Request) -> web.Response:
        data = await request.json()
        try:
            p = int(data["p"])
            genre = str(data["genre"])
        except Exception:
            return web.json_response({"error": "p, genre required"}, status=400)
        m = self._marques()
        try:
            if genre == "cibler":
                carte = str(int(data["id"]))
                if m["cibles"].get(carte) == p:
                    del m["cibles"][carte]
                    m["fleches"] = [f for f in m["fleches"] if not (f["a"] == int(carte) and f["p"] == p)]
                elif len(m["cibles"]) < self.MARQUES_MAX:
                    m["cibles"][carte] = p
            elif genre == "fleche":
                de, a = int(data["de"]), int(data["a"])
                existe = [f for f in m["fleches"] if f["de"] == de and f["a"] == a]
                if existe:
                    m["fleches"] = [f for f in m["fleches"] if f not in existe]
                    if m["cibles"].get(str(a)) == p:
                        del m["cibles"][str(a)]
                elif len(m["fleches"]) < self.MARQUES_MAX:
                    m["fleches"].append({"de": de, "a": a, "p": p})
                    m["cibles"][str(a)] = p
            elif genre == "decibler":
                # `clearTargets` d'OCTGN : mes cibles et mes fleches (p = -1 : tout le monde).
                m["cibles"] = {c: q for c, q in m["cibles"].items() if p != -1 and q != p}
                m["fleches"] = [f for f in m["fleches"] if p != -1 and f["p"] != p]
            elif genre == "surligner":
                carte = str(int(data["id"]))
                couleur = data.get("couleur")
                if couleur is None:
                    m["surlignages"].pop(carte, None)
                elif couleur in self.COULEURS_SURLIGNAGE and len(m["surlignages"]) < self.MARQUES_MAX:
                    m["surlignages"][carte] = couleur
                else:
                    return web.json_response({"error": "couleur"}, status=400)
            else:
                return web.json_response({"error": "genre"}, status=400)
        except (KeyError, TypeError, ValueError):
            return web.json_response({"error": "donnees"}, status=400)
        return web.json_response(m)

    async def get_marques(self, request: web.Request) -> web.Response:
        return web.json_response(self._marques())

    # --- Salon multijoueur : un choix de heros/deck par siege ---------------
    # Meme forme que set_cursor/get_cursors ci-dessus, a deux differences pres :
    # aucune peremption (un choix vaut jusqu'au lancement) et une verification
    # du siege en ECRITURE. Sans elle, un spectateur muni du mot de passe
    # d'entree pourrait changer le heros d'un joueur.
    #
    # On ne stocke PAS le deck complet, seulement de quoi le retrouver :
    # l'hote le recharge par /get_hero_json et /list_deck, deja en place. Cela
    # evite de faire transiter 40 cartes et supprime tout risque de decalage
    # entre ce que l'invite a vu et ce que l'hote enverra au moteur.
    async def set_choix_siege(self, request: web.Request) -> web.Response:
        data = await request.json()
        try:
            p = int(data['p'])
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)

        # ⚠ `tient_le_siege` ET NON `allowed_seats` (21/09/2026). `allowed_seats`
        # ouvre tout siege qu'aucun client ne tient (« reprise d'un siege
        # abandonne »), et AVANT le debut d'une partie ils le sont TOUS : un
        # invite du siege 1 pouvait donc ECRIRE le choix du siege 2. La victime
        # partait avec le deck d'un autre — et depuis que le salon compare le
        # heros de son siege a ce qu'il a choisi, elle reste bloquee dans le
        # salon sans jamais se reconnaitre. Meme garde stricte que
        # `get_liens_sieges` et `get_heros_du_siege`.
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords_sieges = SEAT_PASSWORDS.value
        if bool(passwords_sieges) and any(passwords_sieges) \
                and not self.tient_le_siege(request, p):
            return web.json_response({'error': 'not your seat'}, status=403)

        hero_card_id = str(data.get('hero_card_id', ''))
        deck_id = str(data.get('deck_id', ''))
        if not hero_card_id or not deck_id:
            return web.json_response(
                {'error': 'hero_card_id and deck_id required'}, status=400)

        if not hasattr(self, 'choix_sieges'):
            self.choix_sieges = {}
        self.choix_sieges[p] = {
            'hero_card_id': hero_card_id,
            'deck_id': deck_id,
            'deck_source': str(data.get('deck_source', '')),
        }
        return web.json_response({'result': 'ok'})

    async def get_choix_sieges(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        choix = getattr(self, 'choix_sieges', {})
        return web.json_response({
            'multi': bool(passwords) and any(passwords),
            'sieges': {str(p): c for p, c in choix.items()},
        })

    # --- L'equipe en formation, vue de l'invite (09/10/2026) ------------------
    # Le salon montre a l'invite qui est assis ou et contre qui l'equipe va
    # jouer. L'hote publie ce qu'il a choisi (`set_equipe_hote`), les invites
    # publient deja le leur (`set_choix_siege`) ; `get_equipe_salon` ne rend que
    # des IDENTIFIANTS de cartes heros et le scenario. Jamais un deck, jamais une
    # main : meme principe que `get_heros_du_siege`, qui interdit a un invite de
    # lire le siege du voisin. Un siege non choisi rend une chaine vide.
    async def set_equipe_hote(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        try:
            data = await request.json()
        except Exception:
            return web.json_response({'error': 'json required'}, status=400)
        if not isinstance(data, dict):
            return web.json_response({'error': 'json required'}, status=400)
        passwords = SEAT_PASSWORDS.value
        if bool(passwords) and any(passwords) and not self.tient_le_siege(request, 0):
            return web.json_response({'error': 'host only'}, status=403)
        try:
            nombre = int(data.get('nombre', 0))
        except Exception:
            nombre = 0
        if not 1 <= nombre <= 4:
            return web.json_response({'error': 'bad count'}, status=400)

        def ident(valeur) -> str:
            texte = str(valeur or '')
            return texte if len(texte) <= 80 else ''

        heros_bruts = data.get('heros') or {}
        if not isinstance(heros_bruts, dict):
            return web.json_response({'error': 'bad heroes'}, status=400)
        heros = {}
        for p in range(nombre):
            identifiant = ident(heros_bruts.get(str(p)))
            if identifiant:
                heros[str(p)] = identifiant
        self.equipe_hote = {'nombre': nombre, 'heros': heros,
                            'scenario': ident(data.get('scenario'))}
        return web.json_response({'result': 'ok'})

    async def get_equipe_salon(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        try:
            p = int(request.rel_url.query.get('p', ''))
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)
        if p < 0:
            return web.json_response({'error': 'p required'}, status=400)
        passwords = SEAT_PASSWORDS.value
        if bool(passwords) and any(passwords) and not self.tient_le_siege(request, p):
            return web.json_response({'error': 'not your seat'}, status=403)
        hote = getattr(self, 'equipe_hote', None) or {}
        choix = getattr(self, 'choix_sieges', {})
        nombre = int(hote.get('nombre', 0))
        sieges = {}
        for q in range(max(nombre, p + 1)):
            if q in choix:
                sieges[str(q)] = str(choix[q].get('hero_card_id', ''))
            else:
                sieges[str(q)] = (hote.get('heros') or {}).get(str(q), '')
        return web.json_response({
            'nombre': nombre,
            'sieges': sieges,
            'scenario': hote.get('scenario', ''),
        })

    # --- L'equipe reste ensemble entre deux manches (13/10/2026) -------------
    # Demande de l'utilisateur : « en fin de partie, que les joueurs qu'on a
    # invites restent dans le meme lobby, et des qu'on cree une partie, qu'ils
    # aient de nouveau acces a la selection ». L'invite reste sur son ecran de
    # fin ; des que l'HOTE rouvre la preparation, son plateau le ramene au
    # salon (ui-app, `useRetourAuSalon`). Le signal est un simple compteur :
    # seul son CHANGEMENT compte, releve par l'invite a la fin de la partie.
    #
    # Ecriture reservee au siege 0 (meme garde stricte que les cles) : un
    # invite ne doit pas pouvoir expedier les autres au salon en pleine partie.
    async def annoncer_preparation(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        if not passwords or not any(passwords):
            # Table locale : personne a ramener nulle part.
            return web.json_response({'n': 0})
        if not self.tient_le_siege(request, 0):
            return web.json_response({'error': 'host only'}, status=403)
        self.preparations_hote = getattr(self, 'preparations_hote', 0) + 1
        return web.json_response({'n': self.preparations_hote})

    async def get_preparation(self, request: web.Request) -> web.Response:
        # Lisible par tout le monde : un compteur ne dit rien de la partie.
        return web.json_response({'n': getattr(self, 'preparations_hote', 0)})

    # --- La roue de « Partie au hasard » (08/10/2026) ------------------------
    # En ligne, tout le salon voit les bandeaux tourner et s'arreter sur les
    # MEMES resultats. Le tirage est fait UNE fois, chez celui qui lance ou
    # relance, et seul son RESULTAT voyage ici ; chacun anime ce qu'il lit.
    # `n` compte les lancers d'un bandeau : il change meme quand le hasard
    # retombe sur le meme heros, et c'est lui qui dit « fais tourner ».
    #
    # Droits (decision 8 de .planning/todos/2026-10-08-roue-du-hasard.md) :
    # l'hote (siege 0) lance tout et relance le scenario ; chaque joueur ne
    # relance que SON heros. Meme garde stricte que `set_choix_siege`.
    async def set_roue(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        try:
            data = await request.json()
        except Exception:
            return web.json_response({'error': 'json required'}, status=400)
        if not isinstance(data, dict):
            return web.json_response({'error': 'json required'}, status=400)
        passwords = SEAT_PASSWORDS.value
        protegee = bool(passwords) and any(passwords)
        quoi = str(data.get('quoi', ''))

        def ident(valeur) -> str:
            texte = str(valeur or '')
            return texte if 0 < len(texte) <= 80 else ''

        roue = getattr(self, 'roue', None)
        if quoi in ('tout', 'scenario', 'fermer'):
            if protegee and not self.tient_le_siege(request, 0):
                return web.json_response({'error': 'host only'}, status=403)
        if quoi == 'fermer':
            self.roue = None
            return web.json_response({'result': 'ok'})
        if quoi == 'tout':
            try:
                nombre = int(data.get('nombre', 0))
            except Exception:
                nombre = 0
            heros = data.get('heros') or {}
            scenario = ident(data.get('scenario'))
            if not 1 <= nombre <= 4 or not isinstance(heros, dict) or not scenario:
                return web.json_response({'error': 'bad draw'}, status=400)
            avant = (roue or {}).get('heros', {})
            propres = {}
            for p in range(nombre):
                hid = ident(heros.get(str(p)))
                if not hid:
                    return web.json_response({'error': 'bad draw'}, status=400)
                propres[str(p)] = {'id': hid, 'n': avant.get(str(p), {}).get('n', 0) + 1}
            self.roue = {
                'v': (roue or {}).get('v', 0) + 1,
                'nombre': nombre,
                'fanmade': bool(data.get('fanmade')),
                'heros': propres,
                'scenario': {'id': scenario,
                             'n': (roue or {}).get('scenario', {}).get('n', 0) + 1},
            }
            return web.json_response({'result': 'ok', 'roue': self.roue})
        if not roue:
            return web.json_response({'error': 'no wheel'}, status=409)
        if quoi == 'scenario':
            scenario = ident(data.get('id'))
            if not scenario:
                return web.json_response({'error': 'id required'}, status=400)
            roue['scenario'] = {'id': scenario, 'n': roue['scenario']['n'] + 1}
        elif quoi == 'heros':
            try:
                p = int(data.get('p'))
            except Exception:
                return web.json_response({'error': 'p required'}, status=400)
            hid = ident(data.get('id'))
            if not 0 <= p < roue['nombre'] or not hid:
                return web.json_response({'error': 'bad seat'}, status=400)
            if protegee and not self.tient_le_siege(request, p):
                return web.json_response({'error': 'not your seat'}, status=403)
            ancien = roue['heros'].get(str(p), {})
            roue['heros'][str(p)] = {'id': hid, 'n': ancien.get('n', 0) + 1}
        else:
            return web.json_response({'error': 'unknown'}, status=400)
        roue['v'] = roue['v'] + 1
        return web.json_response({'result': 'ok', 'roue': roue})

    async def get_roue(self, request: web.Request) -> web.Response:
        return web.json_response({'roue': getattr(self, 'roue', None)})

    async def get_heros_du_siege(self, request: web.Request) -> web.Response:
        """Le heros que tient UN siege dans la partie EN COURS. Rien d'autre.

        ⚠ A QUOI CA SERT, ET POURQUOI `get_play_scene_name` NE SUFFISAIT PAS.
        Le salon doit distinguer « une partie tourne » de « MA partie a
        commence ». `get_play_scene_name` ne repond qu'a la premiere : il rend
        le nom de scene des qu'un monde existe, donc encore celui de la manche
        precedente, et il en existe un jusqu'au redemarrage. Le 20/09/2026,
        deux fois dans la meme soiree, des invites ont ete expedies dans la
        partie precedente avant d'avoir choisi leur heros, et y sont restes
        bloques. La seule question qui vaut est « le heros de MON siege est-il
        celui que je viens de choisir ? », et c'est cette route qui y repond.

        ⚠⚠ ET LE HEROS SEUL NE SUFFIT PAS, d'ou `debut` (ronde de correction du
        21/09/2026). Rejouer une manche AVEC LE MEME HEROS — ce que fait la
        majorite des joueurs — remettait le defaut en grand : entre deux
        manches, le monde precedent porte encore le heros de l'invite a son
        siege, et l'invite qui re-choisit le meme heros s'y reconnaissait. Il
        faut donc un second signal, de FRAICHEUR, que le salon releve au moment
        du choix et compare ensuite. C'est aussi le SEUL signal utilisable en
        CAMPAGNE, ou l'equipe est fixee par le livret et ou le heros d'un siege
        est donc le meme a toutes les manches.

        ⚠ ON NE PUBLIE QUE CE QU'IL FAUT POUR SE RECONNAITRE. Le siege DEMANDE,
        et de lui le seul identifiant de sa carte heros. Pas son deck, pas sa
        main, pas le nom de son joueur, et pas les autres sieges : le salon n'en
        a aucun besoin pour repondre a sa question, et une route de confort qui
        en dirait plus rouvrirait la fuite d'information entre joueurs corrigee
        le 15/09. Meme esprit que `get_campagne_en_cours` juste a cote, qui ne
        laisse voyager que de quoi se situer.

        ⚠ ET LE SIEGE EST PROUVE PAR `tient_le_siege`, PAS PAR `allowed_seats`.
        La premiere version utilisait `allowed_seats`, par symetrie avec
        `set_choix_siege` — et le temoin d'authentification l'a prise en faute :
        un invite du siege 1 lisait le siege 2. `allowed_seats` ouvre en effet
        tout siege qu'aucun client ne tient (« reprise d'un siege abandonne »),
        et AVANT le debut d'une partie ils sont TOUS orphelins. C'est le piege
        que `get_liens_sieges` documente juste en dessous ; on prend la meme
        garde stricte qu'elle.

        Une table sans protection de siege est une table locale : elle repond,
        comme tout le reste du moteur y repond.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        try:
            p = int(request.rel_url.query.get('p', ''))
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)
        # Un siege negatif n'existe pas : meme refus que pour un `p` illisible,
        # plutot qu'une reponse vide qui aurait l'air d'un fait.
        if p < 0:
            return web.json_response({'error': 'p required'}, status=400)

        passwords = SEAT_PASSWORDS.value
        protegee = bool(passwords) and any(passwords)
        if protegee and not self.tient_le_siege(request, p):
            return web.json_response({'error': 'not your seat'}, status=403)

        # LE REPERE DE LA PARTIE EN COURS : `game_uid`, que `GameSession`
        # tenait deja et que le plateau emploie DEJA pour la meme question
        # (`clePartie`, ui-app/src/board/moteur.ts). On ne reinvente aucune
        # convention, et on n'ajoute aucun compteur.
        #
        # ⚠ `game_uid` SEUL, ET SURTOUT PAS `game_id` AVEC (ronde 2 du
        # 21/09/2026). `game_id` s'incremente a CHAQUE `SetScene`, donc sur une
        # simple annulation de geste — et `/annuler_dernier_geste` est ouverte a
        # tout tenant de siege. Un joueur de la manche precedente aurait ainsi
        # expedie les invites du salon dans sa partie. `game_uid`, lui, ne se
        # retire plus que quand la scene change VRAIMENT (voir
        # `GameSession.SetScene`).
        session = self.game.session
        debut = str(getattr(session, 'game_uid', '') or '')

        controller = self.get_first_controller(request)
        world = controller.world if controller else None
        # ⚠⚠ ET LE MONDE DOIT ETRE CELUI DE LA SCENE COURANTE (21/09/2026,
        # essai de la chaine entiere a l'ecran). `debut` vient de la SESSION,
        # ou `SetScene` l'ecrit des la seconde ou `/new` arrive. Le MONDE, lui,
        # n'est remonte que lorsque le fil du jeu reprend la main et qu'un
        # client s'est connecte (`GameSession.GameSetup` ->
        # `controller_manager.WaitConnect()`). Entre les deux, cette route
        # melangeait le repere de la partie NEUVE au heros de l'ANCIENNE.
        #
        # Mesure sur moteur local : apres un second `/new`, la route a rendu
        # pendant plus de six secondes `debut` neuf et `heros` ancien — et tant
        # qu'aucun VRAI plateau ne se connectait, elle ne s'en est jamais
        # remise. La fenetre n'est donc pas une milliseconde de course : elle
        # dure le temps que met l'hote a ouvrir sa table, et le salon sonde
        # toutes les deux secondes.
        #
        # Ce melange n'est pas qu'un message de travers. Un hote qui relance a
        # DEUX alors que la manche precedente se jouait a TROIS : le siege 2 y
        # lisait SON heros (celui de l'ancien monde) sous un repere neuf, se
        # reconnaissait, et partait vers une table ou son siege n'existe pas —
        # au lieu de lire « l'hote a lance sans ce siege », qu'il ne verrait
        # plus jamais puisqu'il a quitte le salon.
        #
        # On ne rend donc RIEN plutot qu'un melange : la partie que `debut`
        # nomme n'a pas encore commence, et celle qui tient encore la table est
        # finie. C'est mot pour mot la reponse d'une table neuve, et le salon en
        # fait ce qu'il faut — il attend un tour de plus.
        if not world:  # CONSTAT ROUGE TEMPORAIRE, a restaurer
            # Table neuve, eteinte, ou partie annoncee mais pas encore montee :
            # aucune partie ne tourne.
            return web.json_response({'en_jeu': False, 'p': p, 'heros': '', 'debut': ''})

        joueurs = world.scene.players or []
        heros = ''
        if 0 <= p < len(joueurs):
            identites = joueurs[p].hero or []
            # `hero[0]` est l'identite HEROS ("01001a"), parfois suivie de ses
            # variantes separees par une virgule. Meme decoupage que le
            # catalogue du salon (`d.hero[0].split(",")[0]`), sinon la
            # comparaison echouerait sur une carte a variantes.
            heros = str(identites[0]).split(',')[0] if identites else ''
        # `heros` vide alors qu'une partie tourne = ce siege n'a PAS de heros
        # dedans : l'hote a lance a deux alors que trois liens etaient envoyes.
        # Le salon en fait une explication, pas une attente muette.
        return web.json_response({'en_jeu': True, 'p': p, 'heros': heros, 'debut': debut})

    async def get_liens_sieges(self, request: web.Request) -> web.Response:
        """Les cles de siege, pour que l'HOTE fabrique ses liens d'invitation.

        ⚠ RESERVE AU SIEGE 0. Une cle de siege OUVRE ce siege : la rendre a qui
        la demande laisserait n'importe quel visiteur de la partie s'asseoir a
        la place d'un invite. `allowed_seats` prouve la detention du siege 0
        par le cookie que /claim_seat a pose.

        On ne renvoie que les CLES, jamais l'adresse complete : le moteur ignore
        tout du domaine public place devant lui (`p3.exemple.com`), la ou le
        navigateur de l'hote, lui, le connait exactement.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        if not passwords or not any(passwords):
            # Partie sans protection de siege : il n'y a aucun lien a donner.
            return web.json_response({'multi': False, 'cles': []})
        # `tient_le_siege` et NON `allowed_seats` : cette derniere ouvre les
        # sieges orphelins, or avant le debut d'une partie ils le sont TOUS.
        # Elle laisserait donc le premier visiteur venu repartir avec les
        # quatre cles, c'est-a-dire avec la partie.
        if not self.tient_le_siege(request, 0):
            return web.json_response({'error': 'not the host'}, status=403)
        # ⚠ SIGNAL D'INTENTION (07/10/2026). Seul l'assistant de partie
        # ORDINAIRE (public/js/prepare/app.js, `genererLiens`) demande ces
        # liens : l'ecran des campagnes n'en distribue pas. L'hote qui les
        # genere monte donc une table ordinaire, et le monde que tient encore le
        # moteur (un scenario de campagne abandonne, par exemple) n'est PAS ce
        # qu'on va jouer : `get_campagne_en_cours` se tait jusqu'au prochain
        # /new, qui efface ce drapeau. Si un jour l'ecran des campagnes
        # distribue ses propres liens, il ne doit PAS passer par cette route.
        self.table_ordinaire = True
        return web.json_response({'multi': True, 'cles': list(passwords)})

    async def get_site_admin(self, request: web.Request) -> web.Response:
        """L'adresse d'administration du site, s'il y en a une et si c'est l'hote.

        Reserve au siege 0 par la meme garde stricte que les cles : un invite
        n'a rien a faire dans l'administration des comptes.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS, SITE_ADMIN_URL
        url = SITE_ADMIN_URL.value or ''
        if not url:
            return web.json_response({'url': ''})
        passwords = SEAT_PASSWORDS.value
        if passwords and any(passwords) and not self.tient_le_siege(request, 0):
            return web.json_response({'url': ''})
        return web.json_response({'url': url})

    def _hote_de_la_table(self, request: web.Request) -> bool:
        """Meme garde que get_site_admin : le siege 0, quand des sieges sont proteges."""
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        return not (passwords and any(passwords) and not self.tient_le_siege(request, 0))

    async def puzzle_capture(self, request: web.Request) -> web.Response:
        """Le plateau courant sous forme de puzzle v2 (mode « Puzzle » de la preparation, 24/10/2026).

        Reservee a la table du createur : la partie doit porter la regle `mode_createur_puzzle`, et le client doit tenir un siege
        (la capture lit tout le plateau, mains et decks compris). Ne modifie rien. Rend `{"puzzle": ..., "avertissements": [...]}`
        (`game.puzzle.puzzle_capture.CapturePuzzle`) : ce que la capture ne sait pas rendre est dit, jamais tu.
        """
        from game.puzzle.puzzle_capture import CapturePuzzle

        world = self.game.world
        if world is None:
            return web.json_response({'error': 'no game in progress'}, status=409)
        if not world.rule.mode_createur_puzzle:
            return web.json_response({'error': 'not a puzzle creation table'}, status=409)
        # Pendant la mise en place (mulligans, choix de heros) les mains et le deck rencontre ne sont pas encore poses : une capture
        # d'alors est fausse (essai reel du 24/10/2026, deck rencontre vide). `manuel_actif` = le moteur s'est tu, la table est prete.
        if not world.manuel_actif:
            return web.json_response({'error': 'setup not finished'}, status=409)
        if not self.prouve_un_siege(request):
            return web.json_response({'error': 'aucun siege'}, status=403)
        return web.json_response(CapturePuzzle(world))

    async def get_mes_parties(self, request: web.Request) -> web.Response:
        """Les dernieres parties terminees de l'hote (08/10/2026), pour « Revoir une partie »."""
        from engine.enregistrement import Enregistrement
        if not self._hote_de_la_table(request):
            return web.json_response([])
        return web.json_response([{'n': n, 'nom': nom} for n, nom in enumerate(Enregistrement.PartiesDeLHote())])

    async def get_ma_partie(self, request: web.Request) -> web.Response:
        """Une de ces parties, par son RANG (jamais un nom venu de l'adresse)."""
        from engine.enregistrement import Enregistrement
        import os
        if not self._hote_de_la_table(request):
            return web.json_response({'error': 'reserve a l hote'}, status=403)
        try:
            rang = int(request.query.get('n', '-1'))
        except ValueError:
            rang = -1
        parties = Enregistrement.PartiesDeLHote()
        dossier = Enregistrement.DossierDeLHote()
        if not dossier or not 0 <= rang < len(parties):
            return web.json_response({'error': 'aucune partie'}, status=404)
        with open(os.path.join(dossier, parties[rang]), 'rb') as f:
            contenu = f.read()
        return web.Response(body=contenu, content_type='application/octet-stream',
                            headers={'Content-Disposition': 'attachment; filename="%s"' % parties[rang]})

    async def get_site_url(self, request: web.Request) -> web.Response:
        """L'adresse publique du site, pour TOUS les joueurs de la table.

        AJOUT du 19/09/2026. « Mes signalements » vit sur le site, et la page
        de jeu est servie depuis `pN.<domaine>` : un lien relatif y tombe sur
        le moteur, qui rend une image pour tout chemin inconnu. Le bouton a
        donc besoin de l'adresse absolue.

        ⚠ LECTURE OUVERTE, ET C'EST SANS DANGER. Ce n'est pas l'administration
        (`get_site_admin`, reservee au siege 0) : c'est l'adresse d'accueil,
        que tout le monde connait deja puisque c'est par la qu'on est entre.
        Elle ne porte ni jeton ni compte.
        """
        from engine.device.web.server.server_base import SITE_URL
        return web.json_response({'url': SITE_URL.value or ''})

    def _est_administrateur(self, request: web.Request) -> bool:
        """Ce client est-il l'administrateur du site, sur son propre siege ?

        Meme garde que `get_site_admin`, et pour la meme raison : c'est le SITE
        qui decide, jamais le client. `site_admin_url` n'est renseignee par
        l'orchestrateur que pour la table de l'administrateur, et le siege 0 est
        celui du titulaire du compte — un invite arrive par un lien de siege n'y
        a rien a faire.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS, SITE_ADMIN_URL
        if not (SITE_ADMIN_URL.value or ''):
            return False
        passwords = SEAT_PASSWORDS.value
        if passwords and any(passwords) and not self.tient_le_siege(request, 0):
            return False
        return True

    async def get_images_cartes(self, request: web.Request) -> web.Response:
        """Le releve : qui est sur l'illustration de chaque carte.

        AJOUT du 13/09/2026. Quatre cartes du set Muse parlent de « la carte qui
        porte l'image de ton identite », et le moteur ne voit pas les
        illustrations. On les releve donc a la main.

        ⚠ LECTURE OUVERTE, ECRITURE RESERVEE. Le jeu a besoin de ce releve a
        chaque carte jouee, pour tous les joueurs de la table ; seul
        l'administrateur le modifie.

        ⚠ UNE LISTE VIDE ET UNE CLE ABSENTE NE VEULENT PAS DIRE LA MEME CHOSE :
        vide = « aucune identite dessus, c'est releve » ; absente = « pas encore
        regardee », et le jeu retombe sur son approximation.
        """
        from cards.images_cartes import ImagesCartes
        # `_charger` avale deja fichier absent et fichier abime : un releve vide,
        # jamais une erreur. La page de releve doit s'ouvrir meme le premier jour.
        return web.json_response({'cartes': ImagesCartes._charger()})

    async def get_identites(self, request: web.Request) -> web.Response:
        """L'annuaire des personnes, pour la page de releve.

        Lecture ouverte : il ne contient que des noms deja lisibles sur les
        cartes. Le fichier est GENERE par `outils/annuaire-identites.py` et sert
        aussi au moteur (`cards/images_cartes.py`).
        """
        import json as json_lib
        from cards.images_cartes import IDENTITES_FILE
        try:
            with open(IDENTITES_FILE.value, encoding='utf-8') as f:
                donnees = json_lib.load(f)
            liste = donnees.get('identites') if isinstance(donnees, dict) else None
            return web.json_response({'identites': liste if isinstance(liste, list) else []})
        except Exception:
            # ⚠ Annuaire absent : la page doit le DIRE, pas proposer une liste
            # vide ou l'administrateur croirait qu'il n'y a personne a cocher.
            return web.json_response({'identites': [], 'erreur': 'annuaire absent'})

    async def get_palettes_heros(self, request: web.Request) -> web.Response:
        """Les couleurs de chaque heros, tirees du contour de ses cartes.

        GENERE par `outils/palettes-heros.py`, sert a teinter le coin bas droit
        du plateau. Lecture ouverte : ce ne sont que des couleurs, et chaque
        joueur en a besoin pour la table qu'il regarde.

        ⚠ `Toutes()` avale deja fichier absent et fichier abime et rend un
        releve vide : un plateau SANS teinte, jamais une erreur.
        """
        from cards.palettes_heros import PalettesHeros
        return web.json_response({
            'palettes': PalettesHeros.Toutes(),
            # L'editeur a besoin de distinguer ce qui a ete MESURE de ce qui a
            # ete CORRIGE a la main : sans cela, il ne pourrait ni signaler une
            # correction, ni proposer de revenir a la couleur d'origine.
            'corrections': PalettesHeros.Corrections(),
        })

    async def save_palette_heros(self, request: web.Request) -> web.Response:
        """Corrige la palette d'UNE identite. Reserve a l'administrateur.

        AJOUT du 19/09/2026, demande du 18/09 : « un mode disponible que pour
        moi, ou je peux mettre le hex principal, secondaire et tertiaire de
        chaque personnage ». Les couleurs generees sont tirees du CONTOUR des
        cartes ; quelques-unes tombent a cote, et rien ne permettait de les
        reprendre.

        ⚠ LES CORRECTIONS VIVENT DANS UN FICHIER A PART. Ecrire dans
        `palettes-heros.json` serait perdre le travail a la premiere passe du
        generateur, qui reecrit ce fichier en entier.

        ⚠ UNE IDENTITE A LA FOIS, LE FICHIER RELU A CHAQUE FOIS. Meme raison
        que `save_images_cartes` : deux onglets ouverts ne peuvent se marcher
        dessus que sur la meme identite, jamais sur tout le releve.

        ⚠ ECRITURE ATOMIQUE, puis cache vide : la couleur doit arriver au
        plateau sans redemarrer le serveur.
        """
        import json as json_lib
        import os
        if not self._est_administrateur(request):
            return web.json_response({'error': 'reserve a l administrateur'}, status=403)
        data = await request.json()
        cartes = data.get('cartes')
        if not isinstance(cartes, list) or not cartes:
            return web.json_response({'error': 'cartes manquantes'}, status=400)
        cartes = [str(x).strip() for x in cartes if str(x or '').strip()]
        if not cartes:
            return web.json_response({'error': 'cartes manquantes'}, status=400)

        oublier = bool(data.get('oublier'))
        couleurs: List[List[int]] = []
        if not oublier:
            brut = data.get('couleurs')
            if not isinstance(brut, list) or not brut:
                return web.json_response({'error': 'couleurs manquantes'}, status=400)
            for couleur in brut:
                if not isinstance(couleur, list) or len(couleur) != 3:
                    return web.json_response({'error': 'couleur mal formee'}, status=400)
                try:
                    valeurs = [int(c) for c in couleur]
                except (TypeError, ValueError):
                    return web.json_response({'error': 'couleur mal formee'}, status=400)
                if any(v < 0 or v > 255 for v in valeurs):
                    return web.json_response({'error': 'couleur hors bornes'}, status=400)
                couleurs.append(valeurs)

        from cards.palettes_heros import PALETTES_CORRECTIONS_FILE, PalettesHeros
        chemin = PALETTES_CORRECTIONS_FILE.value
        donnees = {
            '_lisez_moi': ("Corrections a la main des palettes de heros, posees PAR-DESSUS "
                           "data/palettes-heros.json. Ecrites par l'editeur du jeu "
                           "(/palettes-heros.html), jamais par outils/palettes-heros.py."),
            'version': 1,
            'palettes': {},
        }
        try:
            with open(chemin, encoding='utf-8') as f:
                lu = json_lib.load(f)
            if isinstance(lu, dict) and isinstance(lu.get('palettes'), dict):
                donnees['palettes'] = lu['palettes']
        except Exception:
            pass
        for carte in cartes:
            if oublier:
                donnees['palettes'].pop(carte, None)
            else:
                donnees['palettes'][carte] = couleurs
        dossier = os.path.dirname(chemin)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        provisoire = chemin + '.tmp'
        with open(provisoire, 'w', encoding='utf-8') as f:
            json_lib.dump(donnees, f, ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(provisoire, chemin)
        PalettesHeros.Recharger()
        return web.json_response({'ok': True, 'corrigees': len(donnees['palettes'])})

    async def save_images_cartes(self, request: web.Request) -> web.Response:
        """Ecrit le releve d'UNE carte. Reserve a l'administrateur.

        ⚠ UNE CARTE A LA FOIS, ET LE FICHIER RELU A CHAQUE FOIS. Envoyer tout le
        releve a chaque clic ferait grossir la requete a mesure du travail, et
        un onglet reste ouvert ecraserait le travail d'un autre avec sa copie
        perimee. Ici deux onglets ne peuvent se marcher dessus que sur la meme
        carte.

        ⚠ ECRITURE ATOMIQUE : ce fichier porte des heures de relevé a la main.
        Une coupure au milieu d'un `write` le laisserait tronque, donc illisible,
        et tout serait a refaire.
        """
        import json as json_lib
        import os
        if not self._est_administrateur(request):
            return web.json_response({'error': 'reserve a l administrateur'}, status=403)
        data = await request.json()
        carte = str(data.get('carte') or '').strip()
        identites = data.get('identites')
        if not carte or not isinstance(identites, list):
            return web.json_response({'error': 'carte ou identites manquantes'}, status=400)
        propres = []
        for x in identites:
            x = str(x or '').strip()
            if x and x not in propres:
                propres.append(x)
        from cards.images_cartes import IMAGES_CARTES_FILE, ImagesCartes
        chemin = IMAGES_CARTES_FILE.value
        donnees = {'version': 1, 'cartes': {}}
        try:
            with open(chemin, encoding='utf-8') as f:
                lu = json_lib.load(f)
            if isinstance(lu, dict) and isinstance(lu.get('cartes'), dict):
                donnees = lu
        except Exception:
            pass
        if data.get('oublier'):
            donnees['cartes'].pop(carte, None)
        else:
            donnees['cartes'][carte] = propres
        dossier = os.path.dirname(chemin)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        provisoire = chemin + '.tmp'
        with open(provisoire, 'w', encoding='utf-8') as f:
            json_lib.dump(donnees, f, ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(provisoire, chemin)
        # ⚠ Le moteur garde le releve en cache. Sans ceci, une carte relevee
        # pendant une partie ne serait prise en compte qu'au prochain
        # redemarrage du serveur, et l'administrateur croirait a un bug.
        ImagesCartes.Recharger()
        return web.json_response({'ok': True, 'relevees': len(donnees['cartes'])})

    async def _appeler_site(self, chemin: str, champs: dict, secondes: int = 5,
                            avec_statut: bool = False):
        """Relaie un appel au site, en 127.0.0.1, avec le jeton de la partie.

        Le navigateur est servi depuis `p<N>.<domaine>` et le site depuis
        `<domaine>` : une requete directe serait croisee, et le cookie de
        session du site ne voyagerait pas. On passe donc par ici, ou l'appel
        part du serveur et n'a aucune frontiere a franchir.

        Avec `avec_statut`, rend le couple (statut HTTP, donnees), le statut
        valant 0 quand le site n'a pas repondu du tout. C'est le seul moyen de
        distinguer « le site a refuse » de « le site est injoignable » : sans
        lui, un rapport de bug trop gros pour le plafond de corps du site
        s'annoncait a son auteur comme une panne de reseau, et il le renvoyait.
        """
        from engine.device.web.server.server_base import SITE_INTERNE, SITE_JETON
        import urllib.parse
        def rendre(statut, donnees):
            return (statut, donnees) if avec_statut else donnees

        base = SITE_INTERNE.value or ''
        jeton = SITE_JETON.value or ''
        if not base or not jeton:
            return rendre(0, None)      # pas de site derriere : rien a relayer
        corps = dict(champs, jeton=jeton)
        try:
            import aiohttp
            temps = aiohttp.ClientTimeout(total=secondes)
            async with aiohttp.ClientSession(timeout=temps) as session:
                async with session.post(base + chemin,
                                        data=urllib.parse.urlencode(corps)) as reponse:
                    if reponse.status != 200:
                        return rendre(reponse.status, None)
                    return rendre(reponse.status, await reponse.json())
        except Exception:
            # Site injoignable ou trop lent : le panneau se taira, la partie
            # continue. Rien ici ne doit pouvoir interrompre une partie.
            return rendre(0, None)

    async def get_salon_joueurs(self, request: web.Request) -> web.Response:
        """Qui est connecte avec un compte, et les derniers messages.

        ⚠ RESERVE AU SIEGE 0. Le tchat est celui des titulaires de compte ; un
        invite arrive par un lien de siege n'en fait pas partie, et n'a pas a
        lire ce qu'ils s'ecrivent.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        if passwords and any(passwords) and not self.tient_le_siege(request, 0):
            return web.json_response({'actif': False})
        depuis = request.rel_url.query.get('depuis', '0')
        # `avec` vide = tchat general ; un pseudo = conversation privee.
        avec = request.rel_url.query.get('avec', '')
        donnees = await self._appeler_site('/api/vue',
                                           {'depuis': depuis, 'avec': avec})
        if donnees is None:
            return web.json_response({'actif': False})
        donnees['actif'] = True
        return web.json_response(donnees)

    async def post_salon_message(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        if passwords and any(passwords) and not self.tient_le_siege(request, 0):
            return web.json_response({'error': 'not the host'}, status=403)
        data = await request.json()
        texte = str(data.get('texte', '') or '')
        if not texte.strip():
            return web.json_response({'error': 'texte vide'}, status=400)
        donnees = await self._appeler_site('/api/dire',
                                           {'texte': texte,
                                            'a': str(data.get('a', '') or '')})
        if donnees is None:
            return web.json_response({'error': 'site injoignable'}, status=503)
        return web.json_response({'ok': True})

    async def get_messages_prives(self, request: web.Request) -> web.Response:
        """Un message prive attend-il ce joueur ?

        AJOUT du 13/09/2026. Le tchat a ete retire du jeu le 12 : personne ne
        s'en servait, et il encombrait deux ecrans pour rien. Mais
        l'administrateur doit pouvoir joindre quelqu'un qui joue. D'ou cette
        route minuscule, qui ne rend qu'un compte et des noms : rien ne
        s'affiche tant que personne n'ecrit, et une pastille apparait quand
        c'est le cas.

        ⚠ RESERVE AU SIEGE 0, comme le tchat l'etait. Les messages sont ceux du
        titulaire du compte ; un invite arrive par un lien de siege n'en fait
        pas partie et n'a pas a savoir qu'il en a recu.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        if passwords and any(passwords) and not self.tient_le_siege(request, 0):
            return web.json_response({'nouveaux': 0, 'de': []})
        donnees = await self._appeler_site('/api/prives', {}, secondes=3)
        return web.json_response(donnees or {'nouveaux': 0, 'de': []})

    async def post_messages_lus(self, request: web.Request) -> web.Response:
        """Eteint la pastille : le joueur a ouvert sa conversation."""
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        if passwords and any(passwords) and not self.tient_le_siege(request, 0):
            return web.json_response({'error': 'not the host'}, status=403)
        await self._appeler_site('/api/prives_lus', {}, secondes=3)
        return web.json_response({'ok': True})

    # --- Inviter un joueur connecte (13/10/2026) -----------------------------
    # Relais vers le site, comme le tchat : le navigateur est sur p<N>.<domaine>
    # et son cookie de site ne voyage pas jusque-la. Le site sait de quel compte
    # il s'agit par le jeton de la TABLE ; c'est pourquoi tout est RESERVE AU
    # SIEGE 0 : un invite assis ici n'est pas le titulaire du compte, il ne doit
    # ni inviter en son nom, ni lire les invitations qu'il a recues.
    # Decisions : .planning/todos/2026-10-13-inviter-un-connecte.md.
    def _hote_du_compte(self, request: web.Request) -> bool:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        return not (passwords and any(passwords)) or self.tient_le_siege(request, 0)

    async def get_connectes(self, request: web.Request) -> web.Response:
        if not self._hote_du_compte(request):
            return web.json_response({'actif': False, 'connectes': []})
        donnees = await self._appeler_site('/api/connectes', {}, secondes=3)
        if donnees is None:
            # Partie locale ou site muet : rien a proposer, l'ecran garde ses liens.
            return web.json_response({'actif': False, 'connectes': []})
        return web.json_response({'actif': True, 'connectes': donnees.get('connectes', [])})

    async def post_inviter(self, request: web.Request) -> web.Response:
        if not self._hote_du_compte(request):
            return web.json_response({'error': 'not the host'}, status=403)
        try:
            data = await request.json()
            siege = int(data.get('siege'))
        except Exception:
            return web.json_response({'error': 'siege required'}, status=400)
        statut, donnees = await self._appeler_site(
            '/api/inviter', {'a': str(data.get('a', '') or ''), 'siege': siege},
            secondes=5, avec_statut=True)
        if statut == 0:
            return web.json_response({'error': 'site injoignable'}, status=503)
        if statut != 200:
            return web.json_response({'error': 'refuse'}, status=statut)
        return web.json_response({'ok': True})

    async def get_invitations(self, request: web.Request) -> web.Response:
        if not self._hote_du_compte(request):
            return web.json_response({'invitations': []})
        donnees = await self._appeler_site('/api/invitations', {}, secondes=3)
        return web.json_response(donnees or {'invitations': []})

    async def post_invitation_reponse(self, request: web.Request) -> web.Response:
        if not self._hote_du_compte(request):
            return web.json_response({'error': 'not the host'}, status=403)
        try:
            data = await request.json()
        except Exception:
            return web.json_response({'error': 'json required'}, status=400)
        statut, donnees = await self._appeler_site(
            '/api/invitation_reponse',
            {'id': str(data.get('id', '') or ''), 'oui': '1' if data.get('oui') else '0'},
            secondes=5, avec_statut=True)
        if statut == 0:
            return web.json_response({'error': 'site injoignable'}, status=503)
        if statut != 200:
            return web.json_response({'error': 'expiree'}, status=statut)
        return web.json_response({'ok': True, 'lien': (donnees or {}).get('lien', '')})

    async def get_invitations_envoyees(self, request: web.Request) -> web.Response:
        if not self._hote_du_compte(request):
            return web.json_response({'sieges': {}})
        donnees = await self._appeler_site('/api/invitations_envoyees', {}, secondes=3)
        return web.json_response(donnees or {'sieges': {}})

    async def get_decks_invite(self, request: web.Request) -> web.Response:
        """Les decks du COMPTE de l'invite assis au siege `p` (decision 3, 13/10/2026).

        ⚠ L'INVERSE DES ROUTES CI-DESSUS : reserve a celui qui tient CE siege,
        pas a l'hote. Ce sont les decks de l'invite ; ni l'hote ni un voisin
        n'ont a les lire. Le site ne les rend que si ce siege a ete pris par
        une invitation acceptee : il sait alors de quel compte il s'agit.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        try:
            p = int(request.rel_url.query.get('p', ''))
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)
        passwords = SEAT_PASSWORDS.value
        if p < 1 or not (passwords and any(passwords)) or not self.tient_le_siege(request, p):
            return web.json_response({'invite': '', 'decks': []})
        donnees = await self._appeler_site('/api/decks_invite', {'siege': p}, secondes=5)
        return web.json_response(donnees or {'invite': '', 'decks': []})

    async def post_quitter_la_table(self, request: web.Request) -> web.Response:
        """L'HOTE a fini : la table doit cesser d'exister.

        AJOUT du 21/09/2026, et ce n'est pas un confort. « Quitter la partie »
        ne faisait que naviguer vers `/prepare.html` : le moteur gardait son
        monde charge et l'emplacement restait pris. Or le salon des invites
        bascule vers le plateau des que la table porte UNE partie, quelle
        qu'elle soit (`public/js/salon/app.js`) : la partie precedente etant
        toujours la, les invites etaient expedies sur l'ANCIENNE avant meme
        d'avoir choisi un heros, et y restaient bloques. Deux soirees perdues
        les 19 et 20/09. La table fermee, l'hypothese du salon redevient vraie.

        ⚠ RESERVE AU SIEGE 0, ET C'EST ICI QUE CA SE JOUE. Cote site,
        `/api/eteindre` s'authentifie par le jeton de la PARTIE : il dit de
        quelle table vient l'appel, jamais qui a clique. Un invite qui
        arriverait jusque-la fermerait la table de son hote. La seule preuve
        d'etre l'hote est le cookie de siege, et il n'existe que de ce cote-ci.
        `tient_le_siege` et non `allowed_seats`, pour la meme raison que
        `get_liens_sieges` : cette derniere ouvre les sieges orphelins.

        ⚠ L'ADRESSE D'ATTERRISSAGE VIENT DU SITE, et on ne la fabrique pas.
        Une seconde apres cette reponse, ce moteur est mort : toute page qu'il
        pourrait proposer (`/prepare.html`, `/`) sera morte avec lui. Le site
        est de toute facon le seul a connaitre le domaine public place devant
        nous.

        ⚠ ET IL Y A TROIS ISSUES, PAS DEUX. Les confondre ferait dire au
        plateau quelque chose de FAUX :

          — `sans-site` : partie locale (JOUER-SOLO.bat), aucune table a rendre
            a personne. On n'a appele personne, rien n'a bouge ;
          — `fermee` : le site a confirme, et a dit ou aller ;
          — `inconnue` : le site a ete SOLLICITE et n'a pas confirme (trop
            lent, 502 d'un deploiement...). Il n'existe aucun chemin d'abandon
            de son cote : `/api/eteindre` revoque le mot de passe et lance
            l'extinction AVANT de repondre. Passe le plafond ci-dessous, la
            table disparait donc quand meme. Annoncer « rien n'a ete detruit »
            serait un mensonge, et proposer de rester sur la partie, une
            impasse. On n'affirme rien, et on rend l'adresse publique du site
            pour que le joueur aille voir.
        """
        from engine.device.web.server.server_base import (
            SEAT_PASSWORDS, SITE_INTERNE, SITE_JETON, SITE_URL)
        passwords = SEAT_PASSWORDS.value
        if passwords and any(passwords) and not self.tient_le_siege(request, 0):
            return web.json_response({'error': 'not the host'}, status=403)
        # ⚠ AVANT D'APPELER, PAS APRES. `_appeler_site` rend le meme statut 0
        # pour « aucun site configure » et pour « site injoignable » : c'est
        # ici, et seulement ici, qu'on peut encore distinguer les deux.
        if not (SITE_INTERNE.value or '') or not (SITE_JETON.value or ''):
            return web.json_response({'issue': 'sans-site', 'url': ''})
        statut, donnees = await self._appeler_site('/api/eteindre', {}, secondes=10,
                                                   avec_statut=True)
        url = str((donnees or {}).get('url') or '')
        if statut == 200 and url:
            return web.json_response({'issue': 'fermee', 'url': url})
        return web.json_response({'issue': 'inconnue', 'url': SITE_URL.value or ''})

    async def get_dossier_sauvegardes(self, request: web.Request) -> web.Response:
        """Le dossier ou CETTE table range ses trois emplacements de sauvegarde.

        ⚠ CORRECTIF DU 13/09/2026, ET LE DEFAUT ETAIT GRAVE. Le plateau ecrivait
        en dur « ../replays/save_1.json » : le dossier COMMUN, le meme pour tout
        le monde. Sur un serveur a vingt places, les trois emplacements etaient
        donc PARTAGES entre tous les comptes — chacun ecrasait la sauvegarde du
        voisin, et chargeait des parties qu'il n'avait jamais jouees. Signale
        par un joueur (« j'ai charge un truc que je n'ai jamais fait »),
        confirme en production : `replays/save_1..3.json` existaient a la racine
        pendant que les dossiers `replays/serveur-N/` de chacun restaient vides.

        La configuration disait pourtant la verite depuis toujours
        (`replay_folders`, separe par place dans `tools/config_serveur.py`) :
        c'est le client qui inventait un chemin au lieu de la lire. Il la
        demande desormais ici, et n'invente plus rien.
        """
        dossier = (REPLAY_FOLDERS.value or ['../replays/'])[0]
        if not dossier.endswith('/'):
            dossier += '/'
        return web.json_response({'dossier': dossier})

    async def get_legacy(self, request: web.Request) -> web.Response:
        """La fiche du mode Legacy de ce compte, ou une fiche vide.

        AJOUT du 13/09/2026. Ce que le mode retient et qui NE SE DEDUIT PAS de
        l'historique des parties : la date de depart (« repartir de zero »),
        les jetons depenses, et un instantane de la progression pour l'afficher
        sans tout recalculer.

        ⚠ L'INSTANTANE N'EST PAS LA VERITE. La verite est
        `games_history-serveur-N.json`, ecrit par le moteur a chaque fin de
        partie : l'instantane n'est qu'une commodite, et l'assistant sait le
        reconstruire. Deux sources de verite finissent toujours par diverger ;
        celle-ci a le droit de se tromper parce qu'elle est jetable.
        """
        import json as json_lib
        import os
        chemin = LEGACY_FILE.value
        if not chemin or not os.path.isfile(chemin):
            return web.json_response({})
        try:
            with open(chemin, encoding='utf-8') as f:
                fiche = json_lib.load(f)
            return web.json_response(fiche if isinstance(fiche, dict) else {})
        except Exception:
            # Fiche illisible : on repond vide plutot que d'echouer. L'assistant
            # la reconstruira depuis l'historique, qui lui n'a pas bouge.
            return web.json_response({})

    async def save_legacy(self, request: web.Request) -> web.Response:
        """Ecrit la fiche du mode Legacy. Remplace tout.

        ⚠ ECRITURE ATOMIQUE. Le fichier porte la progression de quelqu'un : une
        coupure au milieu d'un `write` la laisserait tronquee, donc illisible,
        et le joueur repartirait a zero sans comprendre. On ecrit a cote, puis
        on renomme, ce que le systeme de fichiers garantit indivisible.
        """
        import json as json_lib
        import os
        fiche = await request.json()
        if not isinstance(fiche, dict):
            return web.json_response({'error': 'fiche invalide'}, status=400)
        chemin = LEGACY_FILE.value
        if not chemin:
            return web.json_response({'error': 'pas de fichier legacy'}, status=500)
        dossier = os.path.dirname(chemin)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        provisoire = chemin + '.tmp'
        with open(provisoire, 'w', encoding='utf-8') as f:
            json_lib.dump(fiche, f, ensure_ascii=False, indent=2)
        os.replace(provisoire, chemin)
        return web.json_response({'ok': True})

    def _est_titulaire_du_compte(self, request: web.Request) -> bool:
        """Ce client est-il le TITULAIRE d'un compte du site, sur sa propre table ?

        Deux conditions : le moteur tourne sous le site (`site_url` renseignee
        par l'orchestrateur), et le client tient le siege 0. Un invite arrive
        par un lien de siege n'a pas de compte ici, et un moteur lance a la
        main (`site_url` vide) n'a pas de compte du tout : dans les deux cas le
        choix d'art reste dans le navigateur.
        """
        from engine.device.web.server.server_base import SEAT_PASSWORDS, SITE_URL
        if not (SITE_URL.value or ''):
            return False
        passwords = SEAT_PASSWORDS.value
        return not (passwords and any(passwords)) or self.tient_le_siege(request, 0)

    @staticmethod
    def _arts_heros_valides(brut) -> 'dict[str, str]':
        """Ne garde que les entrees bien formees : cle de heros (avec « b »
        eventuel pour l'alter ego) -> code de serie. Le reste est ignore, un
        fichier ne doit jamais accepter n'importe quoi du navigateur."""
        import re
        propres = {}
        if isinstance(brut, dict):
            for cle, code in brut.items():
                if (isinstance(cle, str) and isinstance(code, str)
                        and re.fullmatch(r'[a-z]{0,4}\d{1,6}b?', cle)
                        and re.fullmatch(r'[a-z0-9]{1,12}', code)):
                    propres[cle] = code
        return propres

    async def get_arts_heros(self, request: web.Request) -> web.Response:
        """Les arts alternatifs de ce compte.

        `compte` dit si le serveur est la reference : faux pour un invite ou un
        moteur local, et le client garde alors son navigateur. `existe` dit si
        le compte a deja un fichier : sinon le client y verse ce que son
        navigateur contient (premier passage), sans rien perdre.
        """
        import json as json_lib
        import os
        if not self._est_titulaire_du_compte(request):
            return web.json_response({'compte': False, 'existe': False, 'arts': {}})
        chemin = ARTS_HEROS_FILE.value
        if not chemin or not os.path.isfile(chemin):
            return web.json_response({'compte': True, 'existe': False, 'arts': {}})
        try:
            with open(chemin, encoding='utf-8') as f:
                lu = json_lib.load(f)
        except Exception:
            # Fichier illisible : comme absent, le client le reecrit depuis son navigateur.
            return web.json_response({'compte': True, 'existe': False, 'arts': {}})
        return web.json_response({'compte': True, 'existe': True,
                                  'arts': self._arts_heros_valides(lu)})

    async def save_arts_heros(self, request: web.Request) -> web.Response:
        """Applique des changements au fichier d'arts du compte.

        Corps : `{"changements": {"38001": "rog", "38001b": null}}` ; `null`
        efface la cle (retour au scan standard).

        ⚠ DES CHANGEMENTS, PAS LE FICHIER ENTIER : deux appareils ouverts en
        meme temps ne s'ecrasent que sur le meme heros. Le fichier est relu a
        chaque appel.
        ⚠ ECRITURE ATOMIQUE, comme `save_legacy`.
        """
        import json as json_lib
        import os
        if not self._est_titulaire_du_compte(request):
            return web.json_response({'error': 'reserve au titulaire du compte'}, status=403)
        data = await request.json()
        changements = data.get('changements') if isinstance(data, dict) else None
        if not isinstance(changements, dict) or len(changements) > 400:
            return web.json_response({'error': 'changements invalides'}, status=400)
        chemin = ARTS_HEROS_FILE.value
        if not chemin:
            return web.json_response({'error': 'pas de fichier d arts'}, status=500)
        arts = {}
        try:
            with open(chemin, encoding='utf-8') as f:
                arts = self._arts_heros_valides(json_lib.load(f))
        except Exception:
            arts = {}
        ajouts = self._arts_heros_valides(
            {c: v for c, v in changements.items() if v is not None})
        for cle, valeur in changements.items():
            if valeur is None:
                arts.pop(cle, None)
        arts.update(ajouts)
        dossier = os.path.dirname(chemin)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        provisoire = chemin + '.tmp'
        with open(provisoire, 'w', encoding='utf-8') as f:
            json_lib.dump(arts, f, ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(provisoire, chemin)
        return web.json_response({'ok': True, 'arts': arts})

    # Les preferences du compte : une liste FERMEE de cles et de valeurs. Rien
    # d'autre n'est jamais ecrit, un fichier ne doit pas accepter n'importe quoi
    # du navigateur.
    PREFERENCES_PERMISES = {'affichage': ('normal', 'sobre', 'epure')}

    # La TEINTE du fond (04/10/2026) : « h,s,l », trois entiers bornes. Les
    # bornes sont celles de la roue (`board/teinte.ts`,
    # `public/js/prepare/teinte-choix.js`) : teinte 0-359, saturation 0-18 (la
    # roue n'offre que des couleurs ternes), luminosite 6-62 (jusqu'au gris
    # clair). Toujours une liste fermee : la forme est verifiee, pas devinee.
    TEINTE_BORNES = ((0, 359), (0, 18), (6, 62))

    @classmethod
    def _teinte_valide(cls, valeur) -> bool:
        if not isinstance(valeur, str):
            return False
        morceaux = valeur.split(',')
        if len(morceaux) != 3 or not all(m.isdigit() for m in morceaux):
            return False
        return all(bas <= int(m) <= haut for m, (bas, haut) in zip(morceaux, cls.TEINTE_BORNES))

    # LA TABLE PERSONNALISABLE (04/10/2026, par briques le 05/10/2026) : une
    # disposition par nombre de joueurs, cles `table-1` a `table-4`.
    # « 12x8|he+so:c,l,w,h,t;... » : la grille (fixe), puis les zones, chacune
    # avec les CODES de ses briques (ui-app/src/board/table-briques.ts) et sa
    # place : colonne et ligne de depart, largeur et hauteur en cases, taille
    # des cartes en pour cent (60-160). Chaque brique apparait une seule fois,
    # les epinglees (pr, pj, an, ma) seules dans leur zone. L'ANCIEN texte (neuf
    # zones sans codes) reste accepte : le plateau le convertit. Entieres dans
    # la grille, sans chevauchement : le plateau n'a jamais a reparer ce qu'il
    # relit.
    TABLE_CLES = ('table-1', 'table-2', 'table-3', 'table-4')
    TABLE_GRILLE = (12, 8)
    TABLE_ZONES_ANCIEN = 9
    TABLE_TAILLE = (60, 160)
    TABLE_BRIQUES = ('pr', 'he', 'so', 'al', 'me', 'sb', 'en', 'mp', 'mx', 'pj', 'an', 'ma')
    TABLE_EPINGLEES = ('pr', 'pj', 'an', 'ma')

    @classmethod
    def _table_valide(cls, valeur) -> bool:
        if not isinstance(valeur, str) or len(valeur) > 400:
            return False
        tete, _, corps = valeur.partition('|')
        if tete != f'{cls.TABLE_GRILLE[0]}x{cls.TABLE_GRILLE[1]}':
            return False
        zones = corps.split(';')
        nouveau = ':' in corps
        if not nouveau and len(zones) != cls.TABLE_ZONES_ANCIEN:
            return False
        rects = []
        vues = []
        for zone in zones:
            codes, deux_points, place = zone.rpartition(':')
            if nouveau != bool(deux_points):
                return False
            if nouveau:
                briques = codes.split('+')
                if any(b not in cls.TABLE_BRIQUES for b in briques):
                    return False
                if len(briques) > 1 and any(b in cls.TABLE_EPINGLEES for b in briques):
                    return False
                vues.extend(briques)
            morceaux = place.split(',')
            if len(morceaux) != 5 or not all(m.isdigit() for m in morceaux):
                return False
            c, l, w, h, t = (int(m) for m in morceaux)
            if c < 1 or l < 1 or w < 1 or h < 1:
                return False
            if c + w - 1 > cls.TABLE_GRILLE[0] or l + h - 1 > cls.TABLE_GRILLE[1]:
                return False
            if not cls.TABLE_TAILLE[0] <= t <= cls.TABLE_TAILLE[1]:
                return False
            rects.append((c, l, w, h))
        if nouveau and sorted(vues) != sorted(cls.TABLE_BRIQUES):
            return False
        for i, (c1, l1, w1, h1) in enumerate(rects):
            for (c2, l2, w2, h2) in rects[i + 1:]:
                if c1 < c2 + w2 and c2 < c1 + w1 and l1 < l2 + h2 and l2 < l1 + h1:
                    return False
        return True

    @staticmethod
    def _chemin_preferences() -> str:
        """Le fichier de preferences du compte, a cote de son fichier d'arts
        (`arts-heros-serveur-3.json` -> `preferences-serveur-3.json`). Derive
        plutot que configure : la configuration des tables n'a pas a bouger."""
        import os
        arts = ARTS_HEROS_FILE.value or ''
        if not arts:
            return ''
        return os.path.join(os.path.dirname(arts),
                            os.path.basename(arts).replace('arts-heros', 'preferences', 1))

    @classmethod
    def _preferences_valides(cls, brut) -> 'dict[str, str]':
        propres = {}
        if isinstance(brut, dict):
            for cle, valeur in brut.items():
                if cle == 'teinte':
                    if cls._teinte_valide(valeur):
                        propres[cle] = valeur
                elif cle in cls.TABLE_CLES:
                    if cls._table_valide(valeur):
                        propres[cle] = valeur
                elif valeur in cls.PREFERENCES_PERMISES.get(cle, ()):
                    propres[cle] = valeur
        return propres

    async def get_preferences(self, request: web.Request) -> web.Response:
        """Les preferences de ce compte, sur le meme contrat que `get_arts_heros` :
        `compte` faux = le navigateur reste la reference ; `existe` faux = le
        client y verse ce que son navigateur contient."""
        import json as json_lib
        import os
        if not self._est_titulaire_du_compte(request):
            return web.json_response({'compte': False, 'existe': False, 'preferences': {}})
        chemin = self._chemin_preferences()
        if not chemin or not os.path.isfile(chemin):
            return web.json_response({'compte': True, 'existe': False, 'preferences': {}})
        try:
            with open(chemin, encoding='utf-8') as f:
                lu = json_lib.load(f)
        except Exception:
            return web.json_response({'compte': True, 'existe': False, 'preferences': {}})
        return web.json_response({'compte': True, 'existe': True,
                                  'preferences': self._preferences_valides(lu)})

    async def save_preferences(self, request: web.Request) -> web.Response:
        """Applique des changements (`{"changements": {"affichage": "sobre"}}`,
        `null` efface). Ecriture atomique, fichier relu a chaque appel."""
        import json as json_lib
        import os
        if not self._est_titulaire_du_compte(request):
            return web.json_response({'error': 'reserve au titulaire du compte'}, status=403)
        data = await request.json()
        changements = data.get('changements') if isinstance(data, dict) else None
        if not isinstance(changements, dict) or len(changements) > 20:
            return web.json_response({'error': 'changements invalides'}, status=400)
        chemin = self._chemin_preferences()
        if not chemin:
            return web.json_response({'error': 'pas de fichier de preferences'}, status=500)
        try:
            with open(chemin, encoding='utf-8') as f:
                preferences = self._preferences_valides(json_lib.load(f))
        except Exception:
            preferences = {}
        for cle, valeur in changements.items():
            if valeur is None:
                preferences.pop(cle, None)
        preferences.update(self._preferences_valides(changements))
        dossier = os.path.dirname(chemin)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        provisoire = chemin + '.tmp'
        with open(provisoire, 'w', encoding='utf-8') as f:
            json_lib.dump(preferences, f, ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(provisoire, chemin)
        return web.json_response({'ok': True, 'preferences': preferences})

    async def sauver_pour_le_site(self, request: web.Request) -> web.Response:
        """Ecrit la partie en cours dans les sauvegardes, a la demande du site.

        AJOUT du 13/09/2026. Le site ferme une table restee inactive
        trois quarts d'heure. Sans cette route, la partie mourait avec le
        moteur : c'est le geste qui la rend a son joueur, qui la retrouvera
        sous « Reprendre ».

        ⚠ MEME LAISSEZ-PASSER QUE `/get_partie_en_cours`, et pour la meme
        raison : l'orchestrateur n'a pas de cookie de siege. Le jeton que le
        site a remis au moteur a l'allumage en tient lieu, et il meurt avec la
        table.

        ⚠ ET ELLE NE SAUVE QUE S'IL Y A QUELQUE CHOSE A SAUVER. Une table
        allumee ou personne n'a quitte l'ecran des heros n'est pas une partie :
        l'ecrire encombrerait la liste des reprises d'entrees vides.
        """
        from engine.device.web.server.server_base import SITE_JETON
        jeton = request.rel_url.query.get('jeton', '')
        if SITE_JETON.value:
            if jeton != SITE_JETON.value:
                return web.json_response({'error': 'jeton'}, status=403)
        elif (request.remote or '') not in ('127.0.0.1', '::1'):
            return web.json_response({'error': 'local'}, status=403)
        try:
            game = self.controller_manager.game
            world = getattr(game, 'world', None)
            if world is None or not game.state.is_running:
                return web.json_response({'sauve': False, 'raison': 'aucune partie'})
            chemin = game.session.SaveScene(delete_old=False)
            return web.json_response({'sauve': bool(chemin), 'fichier': chemin or ''})
        except Exception as souci:
            # Rien ici ne doit empecher la table de s'eteindre : le site
            # enchaine sur l'extinction quoi qu'il arrive.
            return web.json_response({'sauve': False, 'raison': str(souci)})

    async def get_annonce(self, request: web.Request) -> web.Response:
        """L'annonce en cours sur le site, relayee au plateau et a l'assistant.

        AJOUT du 13/09/2026. Un deploiement fait `systemctl restart narwhal` :
        l'orchestrateur emporte tous ses moteurs, et TOUTE PARTIE EN COURS EST
        PERDUE. Le joueur n'a aucun moyen de le savoir, et pas d'autre recours
        que le bouton Save du plateau. Cette route est ce qui lui donne le
        temps de s'en servir.

        ⚠ AUCUNE RESERVE DE SIEGE, a la difference du tchat. Un preavis
        d'extinction concerne toute la table, invite compris : c'est meme lui
        qui n'a aucun autre moyen d'etre prevenu.

        Sans site derriere (partie locale), `_appeler_site` rend None et l'on
        repond un objet vide : le client ne dessine rien. Rien ici ne doit
        pouvoir interrompre une partie.
        """
        donnees = await self._appeler_site('/api/annonce', {}, secondes=3)
        return web.json_response(donnees or {})

    async def get_rapport_actif(self, request: web.Request) -> web.Response:
        """Un site ecoute-t-il derriere ce moteur ?

        Le formulaire s'en sert pour savoir s'il peut ENVOYER, ou s'il doit se
        rabattre sur le presse-papier et le fichier. En partie locale il n'y a
        aucun site : promettre un envoi qui n'arrivera nulle part serait pire
        que de ne rien proposer.
        """
        from engine.device.web.server.server_base import SITE_INTERNE, SITE_JETON
        actif = bool(SITE_INTERNE.value) and bool(SITE_JETON.value)
        return web.json_response({'actif': actif})

    async def post_rapport_bug(self, request: web.Request) -> web.Response:
        """Relaie un rapport de bug vers le site, qui le rangera pour l'admin.

        ⚠ AUCUNE RESERVE DE SIEGE ICI, a la difference du tchat. N'importe qui
        joue a cette table peut signaler un bug, invite compris — ce sont
        justement ceux qui n'ont aucun autre moyen de le dire. Le site tient le
        plafond de debit, et le siege part avec le rapport.
        """
        data = await request.json()
        description = str(data.get('description', '') or '')
        if not description.strip():
            return web.json_response({'error': 'description vide'}, status=400)
        champs = {
            'nom': str(data.get('nom', '') or ''),
            'description': description,
            'journal': str(data.get('journal', '') or ''),
            'ecran': str(data.get('ecran', '') or ''),
            'siege': str(data.get('siege', '') or ''),
            'capture': str(data.get('capture', '') or ''),
            # CORRECTIF (25/09/2026) : le cookie de session du SITE, s'il est
            # present sur CETTE requete du navigateur. Depuis que ce cookie
            # porte `Domain=.<domaine>` (orchestrateur.py), un joueur connecte
            # a son PROPRE compte l'envoie meme depuis une table qui n'est pas
            # la sienne. Relaye tel quel : c'est le site, seul a savoir lire
            # une session, qui decide s'il correspond a un compte reel. Une
            # requete sans ce cookie (invite jamais connecte) passe une chaine
            # vide, comme avant.
            'nc_session': request.cookies.get('nc_session', ''),
        }
        # ⚠ ON TRACE CHAQUE TENTATIVE, ET C'EST LE FRUIT D'UNE ENQUETE RATEE
        # (19/09/2026). Un joueur a signale un bug le 18/09 ; il n'en restait
        # AUCUNE trace nulle part : ni en base, ni cote site, ni ici. Impossible
        # de dire si l'envoi etait parti, avait ete refuse, ou n'avait jamais eu
        # lieu. Une ligne par tentative, et la question se tranche en une minute.
        #
        # ⚠ AUCUN CONTENU PERSONNEL DANS CETTE LIGNE : ni la description, ni le
        # nom, ni la capture. Un journal se lit a plusieurs et se garde
        # longtemps ; il dit ce qui s'est passe, pas ce que le joueur a ecrit.
        from engine.log import Log
        poids = len(champs['capture'])
        Log.Print(f"[rapport-bug] envoi vers le site, siege={champs['siege'] or '?'}"
                  f" capture={poids} octets")

        # Vingt secondes, et non cinq : la capture pese mille fois un message
        # de tchat, et le site l'ecrit sur disque avant de repondre.
        statut, donnees = await self._appeler_site('/api/bug', champs, secondes=20,
                                                   avec_statut=True)
        # ⚠ UN REFUS N'EST PAS UNE PANNE. Le site plafonne le corps d'une
        # requete a huit mega-octets et rend 413 au-dela ; annonce « site
        # injoignable », ce refus poussait a renvoyer le meme rapport, aussi
        # gros, en boucle. On le dit pour ce qu'il est : c'est la capture qui
        # pese trop.
        if statut == 413:
            Log.Print("[rapport-bug] REFUSE : capture trop lourde (413)")
            return web.json_response({'error': 'rapport trop volumineux'}, status=413)
        if donnees is None:
            Log.Print(f"[rapport-bug] PERDU : site injoignable (statut={statut})")
            return web.json_response({'error': 'site injoignable'}, status=503)
        if donnees.get('error'):
            Log.Print(f"[rapport-bug] REFUSE par le site : {donnees['error']}")
            return web.json_response({'error': donnees['error']}, status=429)
        Log.Print(f"[rapport-bug] accepte, numero {donnees.get('numero')}")
        return web.json_response({'ok': True, 'numero': donnees.get('numero')})

    async def set_language(self, request: web.Request) -> web.Response:
        # Bascule FR/EN de la narration a chaud (bouton langue du client) :
        # recharge la table TransText ('fr') ou la vide ('en'). N'affecte que
        # les messages generes apres l'appel.
        from engine.lib import TransText
        lang = request.rel_url.query_string.strip().lower()
        if lang not in ('fr', 'en'):
            return web.json_response({'error': "lang must be 'fr' or 'en'"}, status=400)
        if lang == 'en':
            TransText.translations = {}
        else:
            file = TransText.translate_file or './data/translate_fr.json'
            try:
                TransText.translations = Json.Load(file)
                TransText.translate_file = file
            except Exception:
                return web.json_response({'error': f'cannot load {file}'}, status=500)
        return web.json_response({'result': 'ok', 'language': lang})

    async def get_language(self, request: web.Request) -> web.Response:
        from engine.lib import TransText
        return web.json_response({'language': 'fr' if TransText.translations else 'en'})

    async def get_gamers(self, request: web.Request) -> web.Response:
        if self.controller_manager.game.state.is_running:
            num = str(self.controller_manager.total_players)
        else:
            num = "0"
        return web.Response(text=num)

    async def get_documents(self, request: web.Request) -> web.Response:
        """Les PDF disponibles : nom de fichier et taille, rien de plus.

        Le classement se fait cote navigateur a partir du nom de fichier : le
        numero mcNN d'un livret est celui que porte son extension dans
        sets_info.json (« 56. Civil War » <-> mc56). Le moteur n'a donc aucune
        table a tenir, et un PDF depose dans le dossier apparait tout seul.
        """
        import os
        fichiers = []
        if FileManager.Exists(DOSSIER_DOCUMENTS):
            for nom in sorted(FileManager.ListDir(DOSSIER_DOCUMENTS)):
                chemin = FileManager.JoinPath(DOSSIER_DOCUMENTS, nom)
                if not nom.lower().endswith('.pdf') or not FileManager.IsFile(chemin):
                    continue
                fichiers.append({'fichier': nom, 'octets': os.path.getsize(chemin)})
        return web.json_response({'documents': fichiers})

    async def get_document_pdf(self, request: web.Request) -> web.Response:
        """Sert UN pdf de assets/docs, designe par son seul nom de fichier.

        ⚠ On ne passe PAS par ReadFile(request.path) comme le font les autres
        types de fichiers : cette recherche-la commence par './', donc un '..'
        bien place dans l'adresse sortirait du dossier et servirait n'importe
        quel fichier du serveur. Ici on ne retient que le nom de base, et on ne
        lit que dans DOSSIER_DOCUMENTS.
        """
        import urllib.parse
        nom = FileManager.GetBaseName(urllib.parse.unquote(request.path))
        if not nom.lower().endswith('.pdf'):
            return web.Response(status=404)
        chemin = FileManager.JoinPath(DOSSIER_DOCUMENTS, nom)
        if not FileManager.Exists(chemin) or not FileManager.IsFile(chemin):
            return web.Response(status=404)
        return self.ReadFile(chemin)

    @override
    def __init__(self) -> None:
        super().__init__()
        self.AddAwaitGetSecurity('/list_file', self.list_file)
        self.AddAwaitGetSecurity('/list_scenarios', self.list_scenarios)
        self.AddAwaitGetSecurity('/list_encounter_sets', self.list_encounter_sets)
        self.AddAwaitGetSecurity('/list_deck', self.list_deck)
        self.AddPostSecurity('/save_deck', self.save_deck)
        self.AddPostSecurity('/delete_deck', self.delete_deck)
        self.AddPostSecurity('/sandbox_command', self.sandbox_command)
        self.AddPostSecurity('/puzzle_objectif', self.puzzle_objectif)
        self.AddPostSecurity('/manuel_undo', self.manuel_undo)
        self.AddPostSecurity('/manuel_pause', self.manuel_pause)
        self.AddPostSecurity('/manuel_passer', self.manuel_passer)
        self.AddPostSecurity('/manuel_reprise', self.manuel_reprise)
        self.AddAwaitGetSecurity('/list_starter_deck', self.list_starter_deck)
        self.AddAwaitGetSecurity('/list_replay_files', self.list_replay_files)
        self.AddAwaitGetSecurity('/list_puzzle_files', self.list_puzzle_files)
        self.AddAwaitGetSecurity('/list_puzzle_test_files', self.list_puzzle_test_files)
        
        self.AddAwaitGetSecurity('/read_file', self.read_file)
        self.AddAwaitGetSecurity('/get_encounter_set_json', self.get_encounter_set_json)
        self.AddAwaitGetSecurity('/get_scenario_json', self.get_scenario_json)
        self.AddAwaitGetSecurity('/get_hero_json', self.get_hero_json)
        self.AddAwaitGetSecurity('/get_sets_json', self.get_sets_json)
        self.AddAwaitGetSecurity('/get_sets_custom_scenario', self.get_sets_custom_scenario)
        self.AddAwaitGetSecurity('/get_statistics_json', self.get_statistics_json)
        self.AddAwaitGetSecurity('/get_games_history', self.get_games_history)
        # Page de suivi du site : jeton du site en guise d'authentification, et
        # pas de controle de version (le site n'est pas un client du jeu).
        self.AddAwaitGetSecurity('/get_partie_en_cours', self.get_partie_en_cours,
                                 need_auth=False, need_check_version=False)
        self.AddAwaitGetSecurity('/get_achievements', self.get_achievements)
        self.AddAwaitGetSecurity('/get_aspect_decks', self.get_aspect_decks)
        self.AddAwaitGetSecurity('/get_cards_json', self.get_cards_json)
        self.AddAwaitGetSecurity('/get_translate_json', self.get_translate_json)
        self.AddAwaitGetSecurity('/get_card_json', self.get_card_json)
        self.AddAwaitGetSecurity('/get_completion_rate', self.get_completion_rate)
        self.AddAwaitGetSecurity('/get_statistics', self.get_statistics)
        self.AddAwaitGetSecurity('/get_session_statistics', self.get_session_statistics)
        self.AddAwaitGetSecurity('/get_play_scene_name', self.get_play_scene_name)
        self.AddAwaitGetSecurity('/get_max_timeout', self.get_max_timeout)
        self.AddAwaitGetSecurity('/get_puzzle_json', self.get_puzzle_json)
        self.AddAwaitGetSecurity('/get_replay_json', self.get_replay_json)
        self.AddPostSecurity('/delete_replay', self.delete_replay)

        self.AddAwaitGetSecurity('/marvelcdb_card', self.marvelcdb_card)
        self.AddPostSecurity('/set_cursor', self.set_cursor)
        self.AddAwaitGetSecurity('/get_cursors', self.get_cursors)
        self.AddPostSecurity('/set_etape', self.set_etape)
        self.AddAwaitGetSecurity('/get_etapes', self.get_etapes)
        self.AddPostSecurity('/set_avance_phase', self.set_avance_phase)
        self.AddAwaitGetSecurity('/get_avance_phase', self.get_avance_phase)
        self.AddPostSecurity('/set_vu', self.set_vu)
        self.AddAwaitGetSecurity('/get_vus', self.get_vus)
        self.AddPostSecurity('/set_marque', self.set_marque)
        self.AddAwaitGetSecurity('/get_marques', self.get_marques)
        self.AddAwaitGetSecurity('/get_enregistrement', self.get_enregistrement)
        self.AddAwaitGetSecurity('/get_mes_parties', self.get_mes_parties)
        self.AddAwaitGetSecurity('/puzzle_capture', self.puzzle_capture)
        self.AddAwaitGetSecurity('/get_ma_partie', self.get_ma_partie)
        self.AddPostSecurity('/set_choix_siege', self.set_choix_siege)
        self.AddAwaitGetSecurity('/get_choix_sieges', self.get_choix_sieges)
        self.AddPostSecurity('/set_equipe_hote', self.set_equipe_hote)
        self.AddAwaitGetSecurity('/get_equipe_salon', self.get_equipe_salon)
        self.AddPostSecurity('/annoncer_preparation', self.annoncer_preparation)
        self.AddAwaitGetSecurity('/get_connectes', self.get_connectes)
        self.AddPostSecurity('/post_inviter', self.post_inviter)
        self.AddAwaitGetSecurity('/get_invitations', self.get_invitations)
        self.AddPostSecurity('/post_invitation_reponse', self.post_invitation_reponse)
        self.AddAwaitGetSecurity('/get_invitations_envoyees', self.get_invitations_envoyees)
        self.AddAwaitGetSecurity('/get_decks_invite', self.get_decks_invite)
        self.AddAwaitGetSecurity('/get_preparation', self.get_preparation)
        self.AddPostSecurity('/set_roue', self.set_roue)
        self.AddAwaitGetSecurity('/get_roue', self.get_roue)
        self.AddAwaitGetSecurity('/get_heros_du_siege', self.get_heros_du_siege)
        self.AddAwaitGetSecurity('/get_liens_sieges', self.get_liens_sieges)
        self.AddAwaitGetSecurity('/get_site_admin', self.get_site_admin)
        self.AddAwaitGetSecurity('/get_salon_joueurs', self.get_salon_joueurs)
        self.AddAwaitGetSecurity('/get_documents', self.get_documents)
        self.AddAwaitGetSecurity(r'/{path:.+\.pdf}', self.get_document_pdf)
        self.AddPostSecurity('/post_salon_message', self.post_salon_message)
        self.AddAwaitGetSecurity('/get_rapport_actif', self.get_rapport_actif)
        self.AddAwaitGetSecurity('/get_annonce', self.get_annonce)
        self.AddAwaitGetSecurity('/get_dossier_sauvegardes', self.get_dossier_sauvegardes)
        self.AddAwaitGetSecurity('/get_messages_prives', self.get_messages_prives)
        self.AddPostSecurity('/post_messages_lus', self.post_messages_lus)
        self.AddPostSecurity('/quitter_la_table', self.post_quitter_la_table)
        self.AddAwaitGetSecurity('/get_images_cartes', self.get_images_cartes)
        self.AddAwaitGetSecurity('/get_identites', self.get_identites)
        self.AddAwaitGetSecurity('/get_site_url', self.get_site_url)
        self.AddAwaitGetSecurity('/get_palettes_heros', self.get_palettes_heros)
        self.AddPostSecurity('/save_palette_heros', self.save_palette_heros)
        self.AddPostSecurity('/save_images_cartes', self.save_images_cartes)
        self.AddAwaitGetSecurity('/get_legacy', self.get_legacy)
        self.AddPostSecurity('/save_legacy', self.save_legacy)
        self.AddAwaitGetSecurity('/get_arts_heros', self.get_arts_heros)
        self.AddPostSecurity('/save_arts_heros', self.save_arts_heros)
        self.AddAwaitGetSecurity('/get_preferences', self.get_preferences)
        self.AddPostSecurity('/save_preferences', self.save_preferences)
        # Sauvegarde demandee par le SITE avant de fermer une table inactive :
        # jeton du site en guise d'authentification, et pas de controle de
        # version (le site n'est pas un client du jeu).
        self.AddAwaitGetSecurity('/sauver_pour_le_site', self.sauver_pour_le_site,
                                 need_auth=False, need_check_version=False)
        self.AddPostSecurity('/post_rapport_bug', self.post_rapport_bug)
        self.AddAwaitGetSecurity('/set_language', self.set_language)
        self.AddAwaitGetSecurity('/get_language', self.get_language)
        self.AddAwaitGetSecurity('/get_gamers', self.get_gamers)

