from . import *
import re
def InPool(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(f'Campaign Pool: {name}', effect) != '')
    return check
def LogSet(name: str):
    def check(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> bool:
        return (CampaignLog.GetStrInternal(name, effect) != '')
    return check
def PutSideSchemeIntoPlay(card_id: str) -> 'Ability':
    # ⚠ La manigance de campagne est RECTO-VERSO (21184a/21184b...) : sans la face b, « Flip this card over » ne fait que la
    # coucher face cachee (rapport #105 : Hack Sanctuary's Computer ne se retournait pas). Meme convention que Puzzle.PutIntoPlay('a,b').
    paire = f'{card_id},{card_id[:-1]}b'
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(paire, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action)
def PutIntoPlayIfPool(card_id: str, pool_name: str, *, under_control: bool = False) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        card.face.PutIntoPlay('FirstPlayer', effect, under_control=under_control)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def ShuffleIntoEncounterIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        card = CardFactory.GenerateCard(card_id, None, effect.world)
        Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerShufflesCopyIfPool(card_id: str, pool_name: str) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard(card_id, player.player_deck, effect.world)
            Faces.ShuffleAllTo([card.face], player.player_deck, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool(pool_name)])
def EachPlayerNornStoneIfPool() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            card = CardFactory.GenerateCard('21187a,21187b', None, effect.world)
            card.SetOwner(player)
            card.face.CastTo(Upgrade).AttachTo2(player.GetIdentity(), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[InPool('Norn Stone')])
def AvengersTowerDamagedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            identity.CastTo(Unit2).TakeDamage(effect.this, 3, effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('Avengers Tower Damaged')])
def InfinityStonesCompletedPenalty() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        for player in Worlds.GetPlayers(effect):
            half = (player.player_deck.GetSize() // 2)
            if (half > 0):
                Faces.DiscardAll(player.player_deck.GetTops(half), effect)
    return AbilityFactoryCampaign.WhenCampaignSetup(action, conditions=[LogSet('The Infinity Stones 1B completed')])
def ExpertMayPlaceAccelerationToHeal() -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
        this = effect.this.CastTo(MainScheme)
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            def heal(targets: Sequence['CardFace']):
                this.PlaceTokensInternal(1, 'acceleration_token', effect)
                identity.CastTo(CanHealth).HealHealth('All', effect)
            player.MayChooseOneAbility(effect, AbilityFactory.ForChoiceAbility('Place 1 acceleration token on the main scheme to heal to full', heal))
    return AbilityFactoryCampaign.WhenCampaignSetupExpertOnly(action)
def FaceExists(effect: 'Effect', card_id: str, *, in_play: 'bool|None' = None, in_victory: 'bool|None' = None) -> bool:
    world = effect.world
    victory = world.victory_display.Get()
    for card in world.object_manager.card_dict.values():
        face = card.face
        if (face == None) or (face.paper.card_id != card_id):
            continue
        if (in_victory != None):
            if ((face in victory) != in_victory):
                continue
        if (in_play != None):
            if (face.IsInPlay() != in_play):
                continue
        return True
    return False
def ActiveMainSchemeStartswith(effect: 'Effect', prefix: str) -> bool:
    return any(s.paper.card_id.startswith(prefix) for s in Worlds.GetAllMainSchemes(effect.world))
# Cles du carnet que le SERVEUR injecte et que le joueur ne doit jamais lire.
# `server_new_game.py` remet la combinaison de la taupe d'Agents of S.H.I.E.L.D.
# dans le carnet juste avant `NewGame` : elle se retrouve donc dans le store du
# monde comme n'importe quelle autre cle. Sans ce filtre elle ressortait deux
# fois — au fichier sortant, que l'ecran relit et propose au joueur, et au
# journal de partie rendu plus bas — ce qui revenait a ouvrir l'enveloppe
# A.I.M. devant lui.
# Les deux cles d'aos qui ne doivent JAMAIS sortir au carnet : la combinaison de la
# taupe, et le compte des preuves gagnees hors campagne (une cle de travail, voir
# `cards/pack/aos/campaign.py`). Ecrites en litteral ici pour ne pas importer aos
# depuis mts, qui n'en sait rien par ailleurs.
CLES_SECRETES = ('A.I.M. Envelope', 'A.I.M. Envelope Gained')


def WriteCampaignLogAtGameOver(collect_fn, scenario_id: 'str|None'=None) -> 'Ability':
    def action(effect: 'Effect', message: 'Message.WhenGameOver'):
        import json
        world = effect.world
        out = {k: v for k, v in world.store.dic.items()
               if isinstance(v, str) and k not in CLES_SECRETES}
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            hp = (identity.health if identity else 0)
            out[f'Player {(player.player_id + 1)} Remaining hit points'] = str(max(0, hp))
            # player.GetHero() leve une AssertionError (pas None) des que le
            # joueur est cote Alter Ego, ce qui est l'etat normal en fin de
            # partie. On lit donc la face heros via GetHeroFace(), qui la
            # retrouve quelle que soit la forme active du joueur ; elle aussi
            # leve si la carte n'a vraiment aucune face heros, d'ou le garde.
            # Une identite illisible ne doit couter que sa propre cle, pas
            # faire perdre le reste du carnet.
            if identity:
                try:
                    hero_face = identity.GetHeroFace()
                except AssertionError:
                    hero_face = None
                if hero_face:
                    out[f'Player {(player.player_id + 1)} Identity'] = hero_face.paper.name.lstrip('* ')
        # ⚠ LE RESULTAT DE LA PARTIE N'EST PAS ENCORE POSE SUR LE MONDE.
        # `GameOver.SetGameOver` envoie ce message PUIS affecte
        # `self.players_won` (game_over.py:85-90) : un collecteur qui lisait
        # `world.game_over` pendant le message voyait donc TOUJOURS « perdue ».
        # Fear No Evil, qui ne coche l'affaire qu'a la victoire, n'inscrivait
        # jamais rien — trouve le 19/09/2026 par `tools/test_campagnes.py`, la
        # premiere gate a jouer la FIN d'une partie. Le collecteur recoit donc
        # le message, seul porteur de la verite a cet instant.
        updates = collect_fn(effect, message)
        # AJOUT (22/10/2026, Punisher MC×DC) : une carte de CAMPAGNE d'un AUTRE pack (l'environnement « Tracking the Buyer » joue sur les
        # scenarios Fear No Evil, dont le 1A ecrit deja son propre releve) ne peut pas poser un second `WriteCampaignLogAtGameOver` : le
        # dernier a ecrire gagnerait. Elle declare donc un COLLECTEUR sur le monde (`world.campagne_collecteurs`) que CHAQUE ecriture rejoue,
        # et au besoin une estampille (`world.campagne_estampille`). Sans ces attributs, rien ne change.
        for extra in getattr(world, 'campagne_collecteurs', []):
            updates = {**updates, **extra(effect, message)}
        for key, value in updates.items():
            if (value == None):
                out.pop(key, None)
            else:
                out[key] = value
        # Estampille du scenario : sans elle, ce carnet reste au fichier apres
        # la fin de partie et une AUTRE boite, jouee plus tard sur la meme
        # place, le lirait comme sien (voir preremplissage.ts, qui compare
        # cette valeur au scenario du contexte de campagne avant d'utiliser
        # quoi que ce soit d'ici). Derivee du set_name de la manigance
        # principale active, deja la facon etablie d'identifier « quel
        # scenario » dans ce fichier (voir ActiveMainSchemeStartswith
        # ci-dessus) : 'Ebony Maw' -> 'ebony_maw', ce qui correspond
        # exactement a l'id de scenario dans data/campagnes/mts.json.
        # ⚠ `scenario_id` PASSE PAR LA BOITE QUAND LE set_name NE SUFFIT PAS
        # (signalement n°50, 04/10/2026). Le set_name de la manigance principale
        # n'est l'id du scenario que pour les boites ou ils coincident ;
        # `gmw` ecrit « collector_1 » et « collector_2 » pour les scenarios
        # `infiltrate_the_museum` et `escape_the_museum`. Le panneau de
        # recompenses ignore alors tout le releve du moteur (estampille
        # differente) et les unites gagnees ne parviennent jamais au Marche.
        stamp = getattr(world, 'campagne_estampille', None) or scenario_id
        schemes = Worlds.GetAllMainSchemes(effect.world)
        if stamp is None and schemes:
            set_name = schemes[0].paper.set_name
            if set_name:
                # CORRECTIF (18/09/2026, Fear No Evil) : « Stop the Presses! »
                # donnait « stop_the_presses! », qui ne correspond a aucun id
                # de scenario. On ne garde que [a-z0-9_].
                stamp = re.sub(r'[^a-z0-9_]', '', set_name.lower().replace(' ', '_'))
        try:
            from engine.config import ConfigVariables
            chemin = ConfigVariables.File('campaign_log_last_file', './campaign_log_last.json').value
            # Tout-ou-rien : une lecture concurrente de /get_carnet_suggere
            # tombait sur du JSON tronque, la route avalait l'erreur et rendait
            # un carnet VIDE. Pour mts, dont aucune cle n'a de detecteur de
            # secours, la recompense etait perdue sans un mot.
            from engine.ecriture_atomique import ecrire_json
            ecrire_json(chemin, {'players_won': message.players_won,
                                 'scenario': stamp, 'suggestions': out})
        except OSError:
            pass
        Message.TextRender('\n--- Campaign Log (suggestions) ---', world)
        for key in sorted(out):
            Message.TextRender(f'{key} = {out[key]}', world)
    return Ability(AbilityType.Campaign, Message.WhenGameOver, [lambda e, m: Worlds.IsCampaign(e)], action)
def CollectMTS(level: int, effect: 'Effect') -> dict:
    updates = {}
    if (level == 1):
        if FaceExists(effect, '21180b', in_play=True):
            updates['Campaign Pool: Cosmo'] = '1'
        if ActiveMainSchemeStartswith(effect, '21075'):
            updates['Campaign Pool: Security Breach'] = '1'
    if (level == 2):
        if FaceExists(effect, '21182b'):
            updates['Campaign Pool: Shawarma'] = '1'
            if not FaceExists(effect, '21182b', in_victory=True):
                updates['Campaign Pool: Black Swan'] = '1'
        if FaceExists(effect, '21100b', in_play=True):
            updates['Avengers Tower Damaged'] = '1'
    if (level == 3):
        if not FaceExists(effect, '21184b', in_victory=True):
            updates['Campaign Pool: System Shock'] = '1'
        if ActiveMainSchemeStartswith(effect, '21115'):
            updates['The Infinity Stones 1B completed'] = '1'
    if (level == 4):
        if FaceExists(effect, '21186b'):
            updates['Campaign Pool: Norn Stone'] = '1'
        if FaceExists(effect, '21186b', in_victory=True):
            updates['Campaign Pool: Odin'] = '1'
    return updates
def CampaignSetup(level: int) -> List['Ability']:
    abilities = []
    if (level == 1):
        abilities.append(PutSideSchemeIntoPlay('21180a'))
        def shuffle_breach(effect: 'Effect', message: 'Message.WhenCampaignSetup'):
            card = CardFactory.GenerateCard('21181', None, effect.world)
            Faces.ShuffleAllTo([card.face], 'EncounterDeck', effect)
        abilities.append(AbilityFactoryCampaign.WhenCampaignSetup(shuffle_breach))
    if (level == 2):
        abilities.append(PutSideSchemeIntoPlay('21182a'))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
    if (level == 3):
        abilities.append(PutSideSchemeIntoPlay('21184a'))
        abilities.append(PutIntoPlayIfPool('21180b', 'Cosmo', under_control=True))
        abilities.append(ShuffleIntoEncounterIfPool('21181', 'Security Breach'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(PutIntoPlayIfPool('21182b', 'Black Swan'))
        abilities.append(AvengersTowerDamagedPenalty())
    if (level == 4):
        abilities.append(PutSideSchemeIntoPlay('21186a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
    if (level == 5):
        abilities.append(PutSideSchemeIntoPlay('21189a'))
        abilities.append(AbilityFactoryCampaign.ShuffleCardIntoDeck('21188', 'EncounterDeck'))
        abilities.append(EachPlayerShufflesCopyIfPool('21183', 'Shawarma'))
        abilities.append(EachPlayerShufflesCopyIfPool('21185', 'System Shock'))
        abilities.append(InfinityStonesCompletedPenalty())
        abilities.append(EachPlayerNornStoneIfPool())
        abilities.append(PutIntoPlayIfPool('21139b,21139a', 'Odin', under_control=True))
    if (level >= 2):
        abilities.append(AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP())
        abilities.append(ExpertMayPlaceAccelerationToHeal())
    abilities.append(WriteCampaignLogAtGameOver(lambda effect, message: CollectMTS(level, effect)))
    return abilities
