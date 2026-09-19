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

    async def sandbox_command(self, request: web.Request) -> web.Response:
        # Mode bac a sable : execute une commande Puzzle.* sur la partie EN COURS.
        # Le moteur sait deja poser une carte en jeu, regler des PV, une menace,
        # un statut... via l'API Puzzle ; on l'expose ici plutot que de reecrire
        # ces mecaniques. Puzzle.Exec n'autorise QUE les appels `Puzzle.<methode>`
        # (il rejette tout le reste a l'analyse syntaxique), donc pas d'execution
        # de code arbitraire.
        from game.puzzle.puzzle import PuzzleHelper

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

    async def manuel_undo(self, request: web.Request) -> web.Response:
        """Ctrl+Z du mode manuel : retire le dernier geste et rejoue sans lui.

        Aucun corps de requete : il n'y a qu'un seul geste annulable, le
        dernier. Le plateau n'a donc rien a envoyer, et rien a tenir a jour de
        son cote.
        """
        world = self.game.world
        if world is None or not world.rule.mode_manuel:
            return web.json_response({'error': 'pas une partie manuelle'}, status=409)
        if not self.game.session.AnnulerDernierGeste():
            return web.json_response({'error': 'rien a annuler'}, status=409)
        return web.json_response({
            'result': 'annule',
            'restants': len(self.game.scene.manuel_commands),
        })

    async def list_starter_deck(self, request: web.Request) -> web.Response:
        return self.ListFile(STARTER_DECK_FOLDER.value)

    async def list_replay_files(self, request: web.Request) -> web.Response:
        if READ_ONLY_FIRST_REPLAY_FOLDER.value:
            return self.ListFile(REPLAY_FOLDERS.value[0])
        else:
            return self.ListFile(*REPLAY_FOLDERS.value)

    async def list_puzzle_files(self, request: web.Request) -> web.Response:
        return self.ListFile(PUZZLE_FOLDER.value)

    async def list_puzzle_test_files(self, request: web.Request) -> web.Response:
        return self.ListFile(PUZZLE_TEST_FOLDER.value)

    def ReadReplayFile(self, file_path: str) -> web.Response:
        from game.scene.scene import Scene
        replay, checksum = Json.LoadAsInternal(file_path, Scene)
        return web.json_response({
            "version": replay.version,
            "is_puzzle": replay.is_puzzle,
            "time": replay.time,
            "cover": replay.cover,
            "path": replay.path,
            "comment": replay.comment,
            "villain": replay.campaign.villain[0] if replay.campaign.villain else replay.campaign.schemes[0],
            "players": [x.hero[0] for x in replay.players],
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
        self.cursors[p] = {
            'x': x, 'y': y, 't': time.time(),
            'survol': str(data.get('survol', ''))[:40],
        }
        return web.json_response({'result': 'ok'})

    async def get_cursors(self, request: web.Request) -> web.Response:
        import time
        cursors = getattr(self, 'cursors', {})
        now = time.time()
        frais = {
            p: {'x': c['x'], 'y': c['y'], 'survol': c.get('survol', '')}
            for p, c in cursors.items() if now - c['t'] < 5.0
        }
        return web.json_response(frais)

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

        autorises = self.allowed_seats(request)
        if autorises is not None and p not in autorises:
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
        return web.json_response({'palettes': PalettesHeros.Toutes()})

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
        self.AddPostSecurity('/sandbox_command', self.sandbox_command)
        self.AddPostSecurity('/manuel_undo', self.manuel_undo)
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

        self.AddAwaitGetSecurity('/marvelcdb_card', self.marvelcdb_card)
        self.AddPostSecurity('/set_cursor', self.set_cursor)
        self.AddAwaitGetSecurity('/get_cursors', self.get_cursors)
        self.AddPostSecurity('/set_choix_siege', self.set_choix_siege)
        self.AddAwaitGetSecurity('/get_choix_sieges', self.get_choix_sieges)
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
        self.AddAwaitGetSecurity('/get_images_cartes', self.get_images_cartes)
        self.AddAwaitGetSecurity('/get_identites', self.get_identites)
        self.AddAwaitGetSecurity('/get_palettes_heros', self.get_palettes_heros)
        self.AddPostSecurity('/save_images_cartes', self.save_images_cartes)
        self.AddAwaitGetSecurity('/get_legacy', self.get_legacy)
        self.AddPostSecurity('/save_legacy', self.save_legacy)
        # Sauvegarde demandee par le SITE avant de fermer une table inactive :
        # jeton du site en guise d'authentification, et pas de controle de
        # version (le site n'est pas un client du jeu).
        self.AddAwaitGetSecurity('/sauver_pour_le_site', self.sauver_pour_le_site,
                                 need_auth=False, need_check_version=False)
        self.AddPostSecurity('/post_rapport_bug', self.post_rapport_bug)
        self.AddAwaitGetSecurity('/set_language', self.set_language)
        self.AddAwaitGetSecurity('/get_language', self.get_language)
        self.AddAwaitGetSecurity('/get_gamers', self.get_gamers)

