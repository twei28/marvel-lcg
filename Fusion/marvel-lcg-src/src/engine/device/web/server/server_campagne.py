"""Campagnes : definitions livrees et parties en cours sauvegardees.

Deux notions distinctes, d'ou deux dossiers :

* les DEFINITIONS (`./data/campagnes/*.json`) decrivent une boite-campagne :
  ordre des scenarios, resume francais, pages du livret, recompenses de
  victoire. Elles sont livrees avec le jeu et ne changent jamais en cours de
  partie.
* les CAMPAGNES EN COURS (`../campagnes/*.json`, a cote de `replays/`) sont
  les parties du joueur : equipe figee, difficulte, scenarios termines,
  carnet de campagne. Elles vivent hors de `.game`, qui est reconstruit a
  chaque lancement.

Le carnet stocke ici est exactement le dict `campaign_log` que le moteur
consomme (voir `game/operate/campaign_logs.py`) : aucune traduction entre les
deux, ce qui evite qu'ils divergent.
"""
from core import *
from aiohttp import web
from engine.config import ConfigVariables
from engine.device.web.server.server_base import GameServerBase

CATEGORY_NAME = "CAMPAGNE"

DEFINITIONS_FOLDER = ConfigVariables.Folder('campagne_definitions_folder', "./data/campagnes/")
CAMPAGNES_FOLDER = ConfigVariables.Folder('campagne_folder', "../campagnes/")
# Carnet SORTANT, ecrit par WriteCampaignLogAtGameOver a la fin de chaque
# partie de campagne (voir src/cards/pack/mts/campaign.py). Chemin relatif au
# repertoire courant du serveur, soit .game, comme les deux dossiers ci-dessus.
CARNET_SUGGERE_FILE = ConfigVariables.File('campaign_log_last_file', "./campaign_log_last.json")


def _nom_de_fichier(brut: str) -> str:
    """Identifiant de fichier sur, derive d'un nom saisi par le joueur."""
    import re
    propre = re.sub('[^a-zA-Z0-9_-]+', '_', str(brut)).strip('_')[:60]
    return propre or 'campagne'


class GameServerCampagne(GameServerBase):

    # ------------------------------------------------------------- definitions --
    async def list_campagnes_definies(self, request: web.Request) -> web.Response:
        """Toutes les boites-campagnes jouables, dans l'ordre de leur code."""
        import json as json_lib
        import os

        dossier = DEFINITIONS_FOLDER.value
        sorties: List[Dict[str, Any]] = []
        if os.path.isdir(dossier):
            for nom in sorted(os.listdir(dossier)):
                if not nom.endswith('.json'):
                    continue
                try:
                    with open(os.path.join(dossier, nom), encoding='utf-8') as f:
                        definition = json_lib.load(f)
                except Exception:
                    continue
                # On ne renvoie que l'entete : la definition complete (pages,
                # recompenses) ne sert qu'une fois la boite choisie.
                sorties.append({
                    'code': definition.get('code', nom[:-5]),
                    'nom': definition.get('nom', ''),
                    'nom_en': definition.get('nom_en', ''),
                    'cle_extension': definition.get('cle_extension', ''),
                    'resume': definition.get('resume', ''),
                    'resume_en': definition.get('resume_en', ''),
                    'nb_scenarios': len(definition.get('scenarios', [])),
                })
        return web.json_response(sorties)

    async def get_campagne_definition(self, request: web.Request) -> web.Response:
        """Definition complete d'une boite-campagne, par son code (`?trors`)."""
        import json as json_lib
        import os

        code = _nom_de_fichier(request.rel_url.query_string)
        chemin = os.path.join(DEFINITIONS_FOLDER.value, f'{code}.json')
        if not os.path.isfile(chemin):
            return web.json_response({'error': f'campagne inconnue : {code}'}, status=404)
        with open(chemin, encoding='utf-8') as f:
            return web.json_response(json_lib.load(f))

    async def get_carnet_suggere(self, request: web.Request) -> web.Response:
        """Le carnet que le MOTEUR a calcule a la derniere fin de partie.

        Les quatre boites cablees en 2026 (mts, mut_gen, next_evol, aoa)
        relevent elles-memes leur carnet a `WhenGameOver` : le plateau n'a
        aucune raison de le redeviner depuis le descripteur. Il pre-remplit
        d'abord avec ces valeurs, et ne retombe sur ses detecteurs que pour les
        cles absentes — ce qui est le cas de toutes celles de trors et sm, qui
        n'ont pas de collecteur cote moteur.

        Fichier absent : reponse vide et 200, pas 404. Une partie hors campagne
        ou une boite sans collecteur n'est pas une erreur.
        """
        import json as json_lib
        import os

        chemin = CARNET_SUGGERE_FILE.value
        if not os.path.isfile(chemin):
            return web.json_response({'players_won': False, 'suggestions': {}})
        try:
            with open(chemin, encoding='utf-8') as f:
                brut = json_lib.load(f)
        except Exception:
            return web.json_response({'players_won': False, 'suggestions': {}})
        suggestions = brut.get('suggestions') or {}
        return web.json_response({
            'players_won': bool(brut.get('players_won')),
            'suggestions': {str(k): str(v) for k, v in suggestions.items() if v is not None},
        })

    # -------------------------------------------------------- campagnes en cours --
    async def list_campagnes(self, request: web.Request) -> web.Response:
        """Campagnes du joueur, la plus recemment jouee en tete."""
        import json as json_lib
        import os

        dossier = CAMPAGNES_FOLDER.value
        sorties: List[Dict[str, Any]] = []
        if os.path.isdir(dossier):
            for nom in os.listdir(dossier):
                if not nom.endswith('.json'):
                    continue
                try:
                    with open(os.path.join(dossier, nom), encoding='utf-8') as f:
                        campagne = json_lib.load(f)
                except Exception:
                    continue
                campagne['id'] = nom[:-5]
                sorties.append(campagne)
        sorties.sort(key=lambda c: str(c.get('derniere_activite', '')), reverse=True)
        return web.json_response(sorties)

    async def get_campagne(self, request: web.Request) -> web.Response:
        """Une campagne en cours, par son identifiant (`?ma_campagne`)."""
        import json as json_lib
        import os

        identifiant = _nom_de_fichier(request.rel_url.query_string)
        chemin = os.path.join(CAMPAGNES_FOLDER.value, f'{identifiant}.json')
        if not os.path.isfile(chemin):
            return web.json_response({'error': f'campagne introuvable : {identifiant}'}, status=404)
        with open(chemin, encoding='utf-8') as f:
            campagne = json_lib.load(f)
        campagne['id'] = identifiant
        return web.json_response(campagne)

    async def save_campagne(self, request: web.Request) -> web.Response:
        """Ecrit (ou remplace) une campagne en cours.

        L'identifiant est fourni par le client s'il met a jour une campagne
        existante ; sinon il est derive du nom, avec un suffixe numerique pour
        ne jamais ecraser silencieusement une autre campagne.
        """
        import json as json_lib
        import os
        import datetime

        donnees = await request.json()
        campagne = donnees.get('campagne')
        if not isinstance(campagne, dict) or not campagne.get('code'):
            return web.json_response({'error': 'campagne invalide'}, status=400)

        dossier = CAMPAGNES_FOLDER.value
        os.makedirs(dossier, exist_ok=True)

        identifiant = campagne.get('id') or ''
        if identifiant:
            identifiant = _nom_de_fichier(identifiant)
        else:
            base = _nom_de_fichier(campagne.get('nom') or campagne.get('code'))
            identifiant = base
            suffixe = 2
            while os.path.exists(os.path.join(dossier, f'{identifiant}.json')):
                identifiant = f'{base}_{suffixe}'
                suffixe += 1

        campagne['id'] = identifiant
        campagne['derniere_activite'] = datetime.datetime.now().isoformat(timespec='seconds')

        chemin = os.path.join(dossier, f'{identifiant}.json')
        with open(chemin, 'w', encoding='utf-8') as f:
            json_lib.dump(campagne, f, ensure_ascii=False, indent=1)
        return web.json_response({'result': 'saved', 'id': identifiant,
                                  'campagne': campagne})

    async def delete_campagne(self, request: web.Request) -> web.Response:
        """Supprime une campagne en cours."""
        import os

        donnees = await request.json()
        identifiant = _nom_de_fichier(donnees.get('id') or '')
        chemin = os.path.join(CAMPAGNES_FOLDER.value, f'{identifiant}.json')
        if not os.path.isfile(chemin):
            return web.json_response({'error': f'campagne introuvable : {identifiant}'}, status=404)
        os.remove(chemin)
        return web.json_response({'result': 'deleted', 'id': identifiant})

    @override
    def __init__(self) -> None:
        super().__init__()
        self.AddAwaitGetSecurity('/list_campagnes_definies', self.list_campagnes_definies)
        self.AddAwaitGetSecurity('/get_campagne_definition', self.get_campagne_definition)
        self.AddAwaitGetSecurity('/get_carnet_suggere', self.get_carnet_suggere)
        self.AddAwaitGetSecurity('/list_campagnes', self.list_campagnes)
        self.AddAwaitGetSecurity('/get_campagne', self.get_campagne)
        self.AddPostSecurity('/save_campagne', self.save_campagne)
        self.AddPostSecurity('/delete_campagne', self.delete_campagne)
