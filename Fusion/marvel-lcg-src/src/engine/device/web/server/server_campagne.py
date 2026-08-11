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


# --------------------------------------------------- l'enveloppe A.I.M. --
# Les neuf cartes preuve d'Agents of S.H.I.E.L.D., en trois series de trois,
# comme le livret les separe par leur dos (p.5) : le moyen, le mobile, et
# l'occasion. Une de chaque part dans l'enveloppe A.I.M. au debut de la
# campagne, et cette combinaison EST la taupe.
SETS_PREUVES = [
    ('50185', '50186', '50187'),   # moyen   : dossiers, ecoute, scanner
    ('50188', '50189', '50190'),   # mobile  : argent, chantage, ideologie
    ('50191', '50192', '50193'),   # occasion: habilitation, voyages, autorite
]
# Le champ ou dort le secret, et la cle sous laquelle le moteur le lit.
CLE_SECRET = 'secret_aim'
CLE_CARNET_SECRET = 'A.I.M. Envelope'


def _tirer_enveloppe_aim() -> str:
    """Une preuve par serie, au hasard. Appele une seule fois par campagne."""
    import random
    return ';'.join(random.choice(serie) for serie in SETS_PREUVES)


def _sans_secret(campagne: 'Dict[str, Any]') -> 'Dict[str, Any]':
    """La campagne telle que le CLIENT a le droit de la voir.

    Tout ce qui sort par une route passe par ici. Le secret de la taupe ne doit
    jamais atteindre le navigateur : l'ecran affiche le carnet en entier, et le
    montrer reviendrait a ouvrir l'enveloppe devant le joueur.
    """
    return {k: v for k, v in campagne.items() if k != CLE_SECRET}


def secret_pour_le_moteur() -> 'Dict[str, str]':
    """Le secret de la campagne dont une partie vient d'etre lancee.

    Le client n'envoie pas l'identifiant de campagne dans le descripteur de
    `/new` — ce contrat est gele. Mais l'ecran des campagnes ecrit
    `partieEnCours` AVANT de lancer : la campagne concernee est donc celle dont
    la partie en cours est la plus recente. Rien a changer au contrat.
    """
    import json as json_lib
    import os

    dossier = CAMPAGNES_FOLDER.value
    if not os.path.isdir(dossier):
        return {}
    meilleure = None
    for nom in os.listdir(dossier):
        if not nom.endswith('.json'):
            continue
        try:
            with open(os.path.join(dossier, nom), encoding='utf-8') as f:
                campagne = json_lib.load(f)
        except Exception:
            continue
        secret = campagne.get(CLE_SECRET)
        en_cours = campagne.get('partieEnCours') or {}
        if not secret or not en_cours.get('depuis'):
            continue
        if (meilleure is None) or (en_cours['depuis'] > meilleure[0]):
            meilleure = (en_cours['depuis'], secret)
    return {CLE_CARNET_SECRET: meilleure[1]} if meilleure else {}


def _nom_de_fichier(brut: str) -> str:
    """Identifiant de fichier sur, derive d'un nom saisi par le joueur."""
    import re
    propre = re.sub('[^a-zA-Z0-9_-]+', '_', str(brut)).strip('_')[:60]
    return propre or 'campagne'


def resume_campagnes() -> 'List[Dict[str, Any]]':
    """Les campagnes du joueur, telles que les hauts faits les lisent.

    Une campagne est GAGNEE quand tous les scenarios de sa boite sont dans
    `termines` et qu'elle n'a pas ete perdue au dernier (voir la cle `defaite`
    des definitions). Le nombre de scenarios vient de la definition livree,
    jamais d'un nombre en dur : rien ne dit que toutes les boites en auront
    cinq.

    C'est ici et pas dans `game/achievements.py` : savoir ou vivent les
    campagnes est le metier du serveur. Le module des hauts faits, lui, ne lit
    aucun fichier et reste eprouvable sans disque.
    """
    import json as json_lib
    import os

    tailles: Dict[str, int] = {}
    dossier_def = DEFINITIONS_FOLDER.value
    if os.path.isdir(dossier_def):
        for nom in os.listdir(dossier_def):
            if not nom.endswith('.json'):
                continue
            try:
                with open(os.path.join(dossier_def, nom), encoding='utf-8') as f:
                    definition = json_lib.load(f)
            except Exception:
                continue
            tailles[definition.get('code', nom[:-5])] = len(definition.get('scenarios') or [])

    sorties: List[Dict[str, Any]] = []
    dossier = CAMPAGNES_FOLDER.value
    if os.path.isdir(dossier):
        for nom in os.listdir(dossier):
            if not nom.endswith('.json'):
                continue
            try:
                with open(os.path.join(dossier, nom), encoding='utf-8') as f:
                    campagne = json_lib.load(f)
            except Exception:
                continue
            code = campagne.get('code', '')
            total = tailles.get(code, 0)
            faits = len(set(campagne.get('termines') or []))
            sorties.append({
                'code': code,
                'difficulte': campagne.get('difficulte', 'standard'),
                'gagnee': bool(total and (faits >= total) and not campagne.get('perdue')),
            })
    return sorties


def _evaluer_hauts_faits() -> None:
    """Debloque ce qu'une campagne qui vient de s'achever peut debloquer.

    Ici, et pas a la fin de la partie : le scenario final est gagne AVANT que
    le panneau de recompenses n'ecrive `termines`. Evalue a la fin de partie,
    la campagne ne serait jamais terminee au bon moment, et le haut fait
    tomberait une partie trop tard.
    """
    import json as json_lib
    import os
    try:
        from game import achievements
        from engine import Engine

        chemin = ConfigVariables.File('games_history_file', 'games_history.json').value
        journal = []
        if os.path.exists(chemin):
            try:
                with open(chemin, encoding='utf-8') as f:
                    charge = json_lib.load(f)
                if isinstance(charge, list):
                    journal = charge
            except Exception:
                journal = []
        achievements.evaluer(Engine.statistics.content, journal, None, resume_campagnes())
    except Exception as exc:
        # Un haut fait manque n'a jamais justifie de perdre une campagne : la
        # sauvegarde a deja abouti quand on arrive ici.
        try:
            from engine.log import Log
            Log.Debug(CATEGORY_NAME, f'hauts faits non evalues : {exc}')
        except Exception:
            pass


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

        Rien n'efface jamais ce fichier : il reste au disque, inchange, entre
        la fin d'une partie et la consultation suivante, meme si une AUTRE
        boite (sans collecteur, comme trors ou sm) a ete jouee entre-temps.
        `scenario` porte donc l'estampille du scenario qui a ECRIT ces
        suggestions ; c'est au plateau de la comparer a son scenario en cours
        avant de s'en servir (voir preremplissage.ts).

        Fichier absent : reponse vide et 200, pas 404. Une partie hors campagne
        ou une boite sans collecteur n'est pas une erreur.
        """
        import json as json_lib
        import os

        chemin = CARNET_SUGGERE_FILE.value
        if not os.path.isfile(chemin):
            return web.json_response({'players_won': False, 'scenario': None, 'suggestions': {}})
        try:
            with open(chemin, encoding='utf-8') as f:
                brut = json_lib.load(f)
        except Exception:
            return web.json_response({'players_won': False, 'scenario': None, 'suggestions': {}})
        suggestions = brut.get('suggestions') or {}
        scenario = brut.get('scenario')
        return web.json_response({
            'players_won': bool(brut.get('players_won')),
            'scenario': (str(scenario) if scenario else None),
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
                sorties.append(_sans_secret(campagne))
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
        return web.json_response(_sans_secret(campagne))

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

        # Le secret ne vient JAMAIS du client : il est tire ici a la premiere
        # ecriture, et repris du fichier ensuite. Un client qui en enverrait un
        # se le ferait remplacer, ce qui est le but.
        ancien = {}
        if os.path.isfile(chemin_existant := os.path.join(dossier, f'{identifiant}.json')):
            try:
                with open(chemin_existant, encoding='utf-8') as f:
                    ancien = json_lib.load(f)
            except Exception:
                ancien = {}
        if any(campagne.get('code') == c for c in ('aos',)):
            campagne[CLE_SECRET] = ancien.get(CLE_SECRET) or _tirer_enveloppe_aim()
        elif ancien.get(CLE_SECRET):
            campagne[CLE_SECRET] = ancien[CLE_SECRET]
        else:
            campagne.pop(CLE_SECRET, None)

        # Ecriture tout-ou-rien : une coupure ici laissait un fichier vide,
        # que list_campagnes saute en silence. La campagne disparaissait de
        # l'ecran sans un mot (constate le 10/8/2026).
        from engine.ecriture_atomique import ecrire_json
        chemin = os.path.join(dossier, f'{identifiant}.json')
        ecrire_json(chemin, campagne)
        # Une campagne ne s'acheve qu'ici : c'est le seul endroit qui voie
        # passer le dernier scenario reporte au carnet.
        _evaluer_hauts_faits()
        return web.json_response({'result': 'saved', 'id': identifiant,
                                  'campagne': _sans_secret(campagne)})

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
