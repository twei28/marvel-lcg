from itertools import chain
from core import *
from game.card import *
from game.card.face import *
from game.render.descriptor.world import WorldDescriptor
from game.render.descriptor.card import CardDescriptor
from game.deck import *
from game.world import *
from game.player import *

def stats_de_partie(world: 'World') -> Dict[str, Any]:
    """Les statistiques de la partie pour l'ecran de fin (onglet Stats).

    Tout vient de compteurs MESURES pendant la partie (SessionStatistics,
    remplis par game/rule/statistics.py et CanAttack._CompterDefense) : rien
    n'est estime ici. Le temps est fige au premier appel apres la fin, sinon
    il continuerait de tourner pendant que l'ecran de fin reste affiche.
    """
    from engine import Engine
    from core.lib import Time
    session = Engine.game.session
    stats = session.statistics
    if getattr(stats, 'temps_fin', None) is None:
        scene = session.scene
        stats.temps_fin = int(Time.GetTime() - session.start_time + (scene.playtime if scene else 0))
    joueurs: List[Dict[str, Any]] = []
    for index, player in enumerate(world.const_players):
        face = player.GetIdentity()
        try:
            hero = player.GetHero()
            if hero is not None:
                face = hero
        except Exception:
            pass
        aspects: List[str] = []
        try:
            zones = [player.player_deck, player.discard_pile, player.hand_cards]
            faces = [f for z in zones for f in list(z.GetAll())] + list(player.GetControlCards())
            for f in faces:
                lire = getattr(f, 'GetAspect', None)
                aspect = lire() if lire else None
                if aspect and aspect not in aspects:
                    aspects.append(aspect)
        except Exception:
            aspects = []
        identite = player.GetIdentity()
        cartes = stats.cartes.get(index, {})
        def ligne(card_id: str, entree: Dict[str, Any], cle: str) -> Dict[str, Any]:
            return {'card_id': card_id, 'nom': entree['nom'], 'n': entree[cle],
                    'piochee': entree['piochee'], 'jouee': entree['jouee']}
        jouees = sorted(((k, v) for k, v in cartes.items() if v['jouee'] > 0),
                        key=lambda kv: (-kv[1]['jouee'], kv[1]['nom']))
        # « Moins jouees » au sens de l'utilisateur : PIOCHEES mais jamais ou peu
        # jouees. Une carte jamais piochee ne dit rien du deck.
        delaissees = sorted(((k, v) for k, v in cartes.items() if v['piochee'] > 0),
                            key=lambda kv: (kv[1]['jouee'], -kv[1]['piochee'], kv[1]['nom']))
        joueurs.append({
            'siege': index,
            'heros': face.paper.name,
            'heros_id': face.paper.card_id,
            'aspects': aspects,
            'pv': getattr(identite, 'health', None),
            'pv_max': getattr(identite, 'max_health', None),
            'compteurs': dict(stats.sieges.get(index, {})),
            'plus_jouees': [ligne(k, v, 'jouee') for k, v in jouees[:3]],
            'moins_jouees': [ligne(k, v, 'jouee') for k, v in delaissees[:3]],
        })
    return {
        'temps': stats.temps_fin,
        'rounds': world.round_id,
        'joueurs': joueurs,
    }

def deck_to_descriptors(deck: 'Deck') -> List['CardDescriptor']:
    return list(chain.from_iterable(
        ToDescriptor.Card(face.card) for face in deck.GetAll()
    ))

import json


class ToDescriptor:

    @staticmethod
    def Player(player: 'Player') -> 'WorldDescriptor.PlayerDescriptor':
        player_descriptor = WorldDescriptor.PlayerDescriptor()

        player_descriptor.area_hero                 = deck_to_descriptors(player.area_hero)
        player_descriptor.allies                    = deck_to_descriptors(player.allies)
        player_descriptor.supports                  = deck_to_descriptors(player.supports)
        player_descriptor.player_deck               = deck_to_descriptors(player.player_deck)
        player_descriptor.player_discard_pile       = deck_to_descriptors(player.discard_pile)
        player_descriptor.dealt_encounter_cards     = deck_to_descriptors(player.dealt_encounter_cards)
        player_descriptor.area_processing           = deck_to_descriptors(player.area_processing)
        player_descriptor.hand_cards                = deck_to_descriptors(player.hand_cards)
        player_descriptor.reserve                   = deck_to_descriptors(player.reserve) # CORRECTIF (pack brawn)
        player_descriptor.rising_tide                = deck_to_descriptors(player.rising_tide) # AJOUT (pack wave)
        player_descriptor.engaged_enemies           = deck_to_descriptors(player.engaged_minions)
        player_descriptor.set_aside_nemesis_sets    = deck_to_descriptors(player.set_aside_nemesis_sets)
        player_descriptor.additional_deck           = deck_to_descriptors(player.additional_deck)
        player_descriptor.additional_discard_pile   = deck_to_descriptors(player.additional_discard_pile)
        player_descriptor.obligations_area          = deck_to_descriptors(player.obligations_area)
        player_descriptor.environment_area          = deck_to_descriptors(player.area_environment)
            
        player_descriptor.resources = player.res_pool.Get().text_legacy
        player_descriptor.is_eliminated = player.is_eliminated
        # Pendant la mise en place, `GetIdentity()` rend None ou un `Insert`
        # (carte provisoire, sans taille de main) : on publie alors 0, que le
        # plateau sait ne pas afficher. Constate au premier passage du harnais.
        player_descriptor.hand_size = getattr(player.GetIdentity(), 'hand_size', 0) or 0
        player_descriptor.has_finished_turn_this_round = player.has_finished_turn_this_round
        return player_descriptor

    @staticmethod
    def Assemblee(world: 'World') -> Dict[str, Any]:
        """L'etat de l'assemblee (Kingsfall multi-tables) vu depuis CETTE table, ou {} hors assemblee. Lu dans le stockage commun a chaque rendu :
        c'est ce qui fait voir aux joueurs les jetons, les degats et la menace des AUTRES tables sans attendre une action."""
        from game.operate.assemblee import Assemblee
        pod = getattr(world.rule, 'assemblee', None)
        if pod is None:
            return {}
        try:
            etat = Assemblee.Etat(pod[0])
        except Exception:
            return {}
        if etat is None:
            return {}
        etat['table'] = pod[1]
        return etat

    @staticmethod
    def Ville(world: 'World') -> Dict[str, Any]:
        """L'etat de la ville pour l'onglet « Ville » (vide hors campagne MC×DC 2026).

        {"lignes": [{"ligne": 0, "capo": <object_id|None>, "capo_card_id": "pu048a"}...],
         "cases":  [{"ligne": 0, "colonne": 0, "objet": <object_id du lieu>, "card_id": "pu030", "joueurs": [player_id...],
                     "sbires_attaches": [object_id...], "limite_utilisee": bool, "piste": {"objet": id, "card_id": "pu039", "porteur": player_id,
                     "compteurs": {"bouncer": 2}} | None}...],
         "joueurs": [{"player_id": 0, "ligne": 1, "colonne": 1}...]}
        Les lignes sont numerotees comme dans le moteur (la rangee Uptown est -1)."""
        from game.operate.ville import Ville
        etat = Ville.Etat(world)
        if etat is None:
            return {}
        scenario = world.GetScenario()

        def limite_utilisee(face: 'CardFace') -> bool:
            from game.ability.condition import Condition
            from game.ability.condition.once_per import GetForDelayAbility
            try:
                for effet in face.effect.Find():
                    if Condition.LimitOncePerRound in effet.ability.conditions:
                        if not world.stat.IsOncePerRound(GetForDelayAbility(effet)):
                            return True
            except Exception:
                return False
            return False

        # les pistes (LEAD) sont dans l'aire des joueurs ; piste n (pu039..pu047) <-> lieu n (pu030..pu038)
        pistes: Dict[str, Dict[str, Any]] = {}
        for joueur in world.const_seat_order_players:
            for face in joueur.obligations_area.Get():
                cid = str(face.paper.card_id)
                if cid.startswith('pu') and cid[2:].isdigit() and 39 <= int(cid[2:]) <= 47:
                    pistes['pu%03d' % (int(cid[2:]) - 9)] = {
                        'objet': face.card.object_id, 'card_id': cid, 'porteur': joueur.player_id,
                        'compteurs': {k: v for k, v in face.components.counter.counters.items() if v}}

        cases: List[Dict[str, Any]] = []
        for (ligne, colonne), lieu in sorted(etat.cases.items()):
            cid = str(lieu.paper.card_id)
            cases.append({
                'ligne': ligne, 'colonne': colonne, 'objet': lieu.card.object_id, 'card_id': cid,
                'joueurs': [pid for pid, case in etat.positions.items() if case == (ligne, colonne)],
                'sbires_attaches': [s.card.object_id for s in Ville.SbiresAttaches(lieu)],
                'limite_utilisee': limite_utilisee(lieu),
                'piste': pistes.get(cid),
            })
        lignes: List[Dict[str, Any]] = []
        for ligne in sorted({l for (l, _c) in etat.cases}):
            zone = etat.zones.get(ligne)
            capos = [v for v in scenario.area_villain.Get() if zone is not None and v.card.game_area is zone]
            lignes.append({'ligne': ligne, 'capo': capos[0].card.object_id if capos else None,
                           'capo_card_id': str(capos[0].paper.card_id) if capos else ''})
        joueurs = [{'player_id': p.player_id, 'ligne': etat.positions[p.player_id][0], 'colonne': etat.positions[p.player_id][1]}
                   for p in world.const_seat_order_players if p.player_id in etat.positions]
        return {'lignes': lignes, 'cases': cases, 'joueurs': joueurs}

    @staticmethod
    def World(world: 'World', event_name: str, sound_name: str) -> 'WorldDescriptor':
        world_descriptor = WorldDescriptor()

        world_descriptor.render_id = world.render.last_render_id
        world_descriptor.round_id = world.round_id

        world_descriptor.phase = world.GetPhaseText()
        world_descriptor.event_name = event_name

        world_descriptor.prompt_last_text = world.render.last_prompt
        world_descriptor.prompt = world.render.prompt
        world_descriptor.max_card_object_id = len(world.object_manager.card_dict)
        world_descriptor.sound_name = sound_name
        world_descriptor.mode_sandbox = bool(world.rule.mode_sandbox)
        world_descriptor.mode_createur_puzzle = bool(world.rule.mode_createur_puzzle)
        world_descriptor.mode_campaign = bool(world.rule.mode_campaign)
        # Une partie repartie en automatique (`scene.reprise_auto`) n'est plus
        # DECLAREE manuelle : le plateau la traite comme une partie ordinaire.
        world_descriptor.mode_manuel = bool(
            world.rule.mode_manuel and not world.scene.reprise_auto)
        # Tache 8 bis : `manuel_actif` (l'ETAT, le moteur s'est tu) est lu sur
        # `world.manuel_actif`, PAS sur `world.rule.mode_manuel` -- voir le
        # commentaire de WorldDescriptor.manuel_actif pour la distinction.
        world_descriptor.manuel_actif = bool(world.manuel_actif)
        world_descriptor.confirm_main_scheme = bool(world.rule.confirm_main_scheme)
        world_descriptor.confirm_side_scheme = bool(world.rule.confirm_side_scheme)
        world_descriptor.confirm_scheme_setup_order = bool(world.rule.confirm_scheme_setup_order)
        # Tache 4 ter : la trace d'un geste manuel refuse (DrainSandboxCommands
        # la pose, personne ne la lisait). Projetee telle quelle, sans mode a
        # verifier : le champ est vide hors refus, peu importe le mode.
        world_descriptor.manuel_refus = world.controller_manager.device_manager.sandbox_last_error
        # Tache 2 : la marque « corrigee a la main » est lue sur la SCENE
        # (`world.scene.corrigee_a_la_main`), pas sur le monde -- c'est elle,
        # et non `world`, qui survit a la sauvegarde.
        world_descriptor.corrigee_a_la_main = bool(world.scene.corrigee_a_la_main)
        # Tache 3 : la pause EN COURS (qui, depuis quand), lue sur la SCENE
        # comme la marque juste au-dessus -- effacee a la reprise, elle,
        # contrairement a `corrigee_a_la_main`. Meme acces direct que la
        # ligne juste au-dessus : les champs absents d'une vieille sauvegarde
        # retombent deja sur leur defaut (`engine/lib/json.py`).
        world_descriptor.pause_par = str(world.scene.pause_par)
        world_descriptor.pause_a = str(world.scene.pause_a)
        world_descriptor.pause_epoch = float(getattr(world.scene, 'pause_epoch', 0.0) or 0.0)

        world_descriptor.active_card_ids = world.render.last_active_card_ids
        # Journal des activations ennemies du round (voir WorldStat). Copie, et
        # pas la liste vivante : le descripteur est serialise plus tard, et le
        # moteur peut avoir repris sa course d'ici la.
        world_descriptor.faits_mechant = list(world.stat.faits_mechant)
        world_descriptor.choix_uniques = list(world.stat.choix_uniques)

        world_descriptor.players = []
        for player in world.const_seat_order_players:
            world_descriptor.players.append(ToDescriptor.Player(player))
        world_descriptor.ville = ToDescriptor.Ville(world)
        world_descriptor.assemblee = ToDescriptor.Assemblee(world)

        scenario = world.GetScenario()

        world_descriptor.area_villain           = deck_to_descriptors(scenario.area_villain)
        world_descriptor.villain_deck           = deck_to_descriptors(scenario.villain_deck)
        world_descriptor.encounter_deck         = deck_to_descriptors(scenario.encounter_deck)
        world_descriptor.encounter_discard_pile = deck_to_descriptors(scenario.encounter_discard_pile)
        world_descriptor.area_schemes_main      = deck_to_descriptors(world.area_schemes_main)
        world_descriptor.main_schemes_deck      = deck_to_descriptors(world.main_schemes_deck)
        world_descriptor.area_schemes_side      = deck_to_descriptors(world.area_schemes_side)

        world_descriptor.area_boost             = deck_to_descriptors(world.area_boosting)
        world_descriptor.area_environment       = deck_to_descriptors(world.area_environment)
        world_descriptor.area_evidence          = deck_to_descriptors(world.area_evidence)
        world_descriptor.area_rule              = deck_to_descriptors(world.area_rule)

        world_descriptor.area_processing = []
        for player in world.const_seat_order_players:
            world_descriptor.area_processing.extend(deck_to_descriptors(player.area_processing))
        world_descriptor.area_processing.extend(deck_to_descriptors(world.area_processing))
        world_descriptor.area_revealing         = deck_to_descriptors(world.area_revealing)

        world_descriptor.area_removed           = deck_to_descriptors(world.area_removed)
        world_descriptor.area_insert            = deck_to_descriptors(world.area_insert)
        world_descriptor.area_set_aside         = deck_to_descriptors(world.aside_deck)
        world_descriptor.area_set_aside         += deck_to_descriptors(world.aside_modular)
        # Mode competitif : les cartes joueur du leader de chaque camp, mises
        # de cote a l'etape 3 (mc56 p.14). Elles se voient, c'est le livret qui
        # le veut : les joueurs savent ce qu'ils peuvent gagner.
        for deck in world.team_set_aside.values():
            world_descriptor.area_set_aside     += deck_to_descriptors(deck)
        world_descriptor.victory_display        = deck_to_descriptors(world.victory_display)
        world_descriptor.area_status_cards      = deck_to_descriptors(world.area_status_cards)
        # Fin de partie exposee au client : players_won n'est defini que sur une
        # vraie fin gagnee/perdue (pas Exit/Undo), d'ou le getattr None -> pas de
        # game over. reason = texte affichable ("The Final Stage of the Villain
        # was Defeated"...).
        _victoire = getattr(world.game_over, 'players_won', None)
        world_descriptor.game_over = _victoire is not None
        world_descriptor.puzzle_objectives = world.puzzle_objectives.Status()
        try:
            world_descriptor.puzzle_info = json.loads(world.scene.puzzle_info) if world.scene.puzzle_info else {}
        except ValueError:
            world_descriptor.puzzle_info = {}
        world_descriptor.players_won = bool(_victoire) if _victoire is not None else False
        world_descriptor.game_over_reason = (world.game_over.reason or '') if _victoire is not None else ''
        if world_descriptor.game_over:
            try:
                world_descriptor.stats_partie = stats_de_partie(world)
            except Exception:
                world_descriptor.stats_partie = {}
        # Mode competitif : le camp gagnant, et le camp de chaque siege. Sans
        # eux, l'ecran de fin annoncerait la meme chose aux deux tables.
        if world.rule.mode_competitive:
            world_descriptor.winning_team = world.competitive.camp_gagnant
            world_descriptor.teams = [world.GetTeamOfPlayer(x)
                                      for x in world.const_seat_order_players]

        for deck in world.additional_decks:
            faces = deck_to_descriptors(deck)
            world_descriptor.additional_decks.append(faces)
        for deck in world.additional_discard_piles:
            faces = deck_to_descriptors(deck)
            world_descriptor.additional_discard_piles.append(faces)

        world_descriptor.area_resources = []
        for player in world.const_seat_order_players:
            world_descriptor.area_resources.extend(deck_to_descriptors(player.area_resources))

        return world_descriptor

    @staticmethod
    def Card(card: 'Card') -> List['CardDescriptor']:

        card_descriptor = [card.Render()]

        for face in card.components.status.GetDeck().GetAll():
            card_descriptor += ToDescriptor.Card(face.card)
        for face in card.components.inventory.GetDeck().GetAll():
            card_descriptor += ToDescriptor.Card(face.card)
        for face in card.components.placed_card.GetDeck().GetAll():
            card_descriptor += ToDescriptor.Card(face.card)
        for face in card.components.boostable.GetDeck().GetAll():
            card_descriptor += ToDescriptor.Card(face.card)
        return card_descriptor

