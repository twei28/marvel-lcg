from core import *
from game.scene import *
from game.scene.replay import *
from engine.lib import Json, Ver
from engine.file import FileManager

CATEGORY_NAME = "SCENE"

class LoaderHelper:

    @staticmethod
    def CreateScene(seed: int, campaign: CampaignDescriptor, players: Sequence[HeroDescriptor], rules: List[str]) -> 'Scene':
        scene = Scene(
            version=str(Ver.version),
            metadata={
                "seed": seed,
            },
            rules=rules,
            campaign=campaign,
            players=players,
            inputs=[]
        )
        scene.UpdateVersion()
        for player in scene.players:
            assert player.name != ""
        return scene

    @staticmethod
    def Loads(file_path: str) -> 'Scene':
        # Log.Debug(f"File: {file_path}")

        scene = Json.LoadAs(file_path, Scene, check_sum="Warn")
        scene.UpdateVersion()

        scene.SetMetadataStr("path", file_path)

        return scene

class SceneLoader:

    @staticmethod
    def LoadCampaign(campaign_json: str, encounter_set_names: List[str]|None) -> 'CampaignDescriptor':
        """Un scenario, avec ses sets de rencontre.

        `None` veut dire « ceux du fichier, plus ses modulaires recommandes » ;
        une liste veut dire « exactement ceux-la », ce qu'envoie l'ecran de
        preparation quand le joueur a choisi ses modulaires.
        """
        campaign = Json.LoadsAs(campaign_json, CampaignDescriptor)
        campaign.UpdateVersion()

        if encounter_set_names != None:
            campaign.encounter_sets = encounter_set_names[:]
        else:
            campaign.encounter_sets += campaign.modular_sets
        return campaign

    @staticmethod
    def NewFromJson(campaign_json: str, encounter_set_names: List[str]|None, hero_jsons: List[str], seed: int, rules: List[str], campaign_log: Dict[str, str],
                    campaign_json_2: str="", encounter_set_names_2: List[str]|None=None, teams: List[int]|None=None) -> 'Scene':
        players: List[HeroDescriptor] = []
        for index, hero_text in enumerate(hero_jsons):
            player = Json.LoadsAs(hero_text, HeroDescriptor)
            player.UpdateVersion()
            # Le camp du joueur, dans l'ordre des decks recus. Absent en partie
            # ordinaire : tout le monde reste dans le camp 0, seule zone de jeu.
            if teams and index < len(teams):
                player.team = teams[index]
            players.append(player)
            # L'identite liee est developpee APRES : elle herite du camp de son
            # porteur (voir ExpandLinkedIdentity).
            players += SceneLoader.ExpandLinkedIdentity(player)

        campaign = SceneLoader.LoadCampaign(campaign_json, encounter_set_names)

        if campaign_log:
            campaign.campaign_log |= campaign_log

        scene = LoaderHelper.CreateScene(seed, campaign, players, rules)

        # Mode competitif : le scenario pose devant la seconde equipe.
        if campaign_json_2:
            scene.campaign_2 = SceneLoader.LoadCampaign(campaign_json_2, encounter_set_names_2)

        return scene

    @staticmethod
    def ExpandLinkedIdentity(player: 'HeroDescriptor') -> List['HeroDescriptor']:
        """Developpe une identite LIEE en un joueur supplementaire.

        Un pack a deux heros pour un seul joueur (Cloak & Dagger) se declare
        avec une cle `linked_identity` portant sa propre identite et son propre
        mini-deck. On en fait un second `HeroDescriptor` : le moteur cree alors
        un vrai second joueur, avec identite, deck, main et defausse distincts,
        sans qu'aucune des ~770 lectures de `GetIdentity()` ait a changer.
        """
        lie = player.linked_identity
        if not lie:
            return []
        return [HeroDescriptor(
            version=player.version,
            name=str(lie.get("name") or f"{player.name} (2)"),
            hero=list(lie.get("hero") or []),
            hero_deck=list(lie.get("hero_deck") or []),
            obligations=list(lie.get("obligations") or []),
            nemesis_set=list(lie.get("nemesis_set") or []),
            player_deck=list(lie.get("player_deck") or []),
            team=player.team,
        )]

    @staticmethod
    def NewScene(campaign_name: str, encounter_set_names: List[str]|None, hero_names: List[str], seed: int) -> 'Scene':
        heroes_text: List[str] = []
        campaign_text: str = ""

        assert type(campaign_name) is str, f"{campaign_name=}"
        for hero_json in hero_names:
            file_path = FileManager.FindJsonPath('Hero', hero_json)
            assert file_path, f"{file_path=}"
            with FileManager.OpenFile(file_path, read=True) as file:
                heroes_text.append(file.Read())

        file_path = FileManager.FindJsonPath('Campaign', campaign_name)
        assert file_path, f"{file_path=}"
        with FileManager.OpenFile(file_path, read=True) as file:
            campaign_text = file.Read()

        scene = SceneLoader.NewFromJson(campaign_text, encounter_set_names, heroes_text, seed, [], {})
        return scene

    @staticmethod
    def Load(replay: str, nullable: bool=False) -> 'Scene|None':
        file_path = FileManager.FindJsonPath('Replay', replay, nullable=nullable)
        if file_path:
            scene = LoaderHelper.Loads(file_path)
            return scene
        else:
            return None

