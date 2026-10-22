"""Campagne « La ville ne dort jamais » (MC×DC 2026) : mise en place et releve du carnet, combat 1 « The Big Apple ».

Livret FR (`docs/packs/mcdc-2026-punisher/regles-fr.md`) et cartes p263 (pu140) / p264 (pu141) :
  * MISE EN PLACE : l'environnement « Guerre des Gangs a Big Apple ! » (pu140) est mis en jeu ; les sets Cops et Tracksuit Mafia et
    l'absence d'Uptown viennent du scenario (`data/scenarios/the_big_apple*.json`) ; « chaque joueur a besoin d'un pion joueur » =
    The City (pu005), rien a faire ici.
  * stade 2A (pu002a) : en campagne, NOTER le lieu de la derniere piste ajoutee a la pile de victoire (`NoterLeLieuDeLaDerniere
    Piste`, appelee par pu002a).
  * RELEVE (a la VICTOIRE seulement : « defaite : on reinitialise le scenario, sans penalite ») : le CAPO qui etait le Trafiquant
    d'armes (Gunrunner), pu140 retournee (« Victory: flip this card ») et pu141 gagnee pour les combats 2 et 3 ; les PV restants
    sont ecrits par `WriteCampaignLogAtGameOver` pour tous les packs (campagne experte).

Cles du carnet (toutes declarees dans `data/campagnes/punisher_mcdc_2026.json`, car le panneau ne reporte QUE les cles declarees) :
  - "Final LEAD Location" : nom du lieu de la derniere piste (le tableau de p265, combat 2, choisit la manigance principale) ;
  - "Gunrunner" : nom du CAPO porteur de Gunrunner (combat 2 : Hobgoblin si Count Nefaria, Ringmaster, Mister Negative ou Nightshade,
    Jigsaw sinon) ;
  - "Big Apple Gang War!" : "Flipped" une fois le combat 1 gagne ;
  - "Seized Tech Crates" : "1" une fois gagnee (a mettre en jeu aux combats 2 et 3) ;
  - "Punisher Ally" : "1" une fois gagne au combat 3 (a mettre en jeu au combat 4 ; Kingsfall le demande) ;
  - "Tracking the Buyer" : "Flipped" une fois le combat 2 gagne ; "Punisher's Ordnance Cache" : "1" (a mettre en jeu au combat 3) ;
    "Underling" : le sous-fifre affronte au combat 2 (Hobgoblin ou Jigsaw : au combat 3, l'AUTRE) ;
  - "Player N Remaining hit points", "Player N Identity" (communes a toutes les boites).
"""
from cards.pack import *
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver

SCENARIO = 'the_big_apple'
ENVIRONNEMENT_COMBAT_1 = 'pu140'
CAISSES = 'pu141'

CLE_LIEU = 'Final LEAD Location'
CLE_TRAFIQUANT = 'Gunrunner'
CLE_COMBAT_1 = 'Big Apple Gang War!'
CLE_CAISSES = 'Seized Tech Crates'
CLE_COMBAT_2 = 'Tracking the Buyer'
CLE_CACHE = "Punisher's Ordnance Cache"
CLE_SOUS_FIFRE = 'Underling'
ENVIRONNEMENT_COMBAT_2 = 'pu142'
CACHE = 'pu143'
ENVIRONNEMENT_COMBAT_3 = 'pu144'
SOUTIEN_SHIELD = 'pu145'
ALLIE_PUNISHER = 'pu146'
POUVOIR_AU_PEUPLE = 'pu148'
CLE_ALLIE_PUNISHER = 'Punisher Ally'

# Les 9 lieux, dans l'ordre de la grille (un LEAD pu039..pu047 porte le meme numero que son lieu pu030..pu038).
NOMS_DES_LIEUX = {'pu030': "Hell's Kitchen", 'pu031': 'Theater District', 'pu032': 'Upper East Side',
                  'pu033': 'West Village', 'pu034': 'Midtown', 'pu035': 'Lower East Side',
                  'pu036': 'Soho', 'pu037': 'Financial District', 'pu038': 'Chinatown'}


def LieuDeLaPisteGagnee(card_id_piste: str) -> str:
    """Le nom du lieu d'une piste : pu039 -> Hell's Kitchen ... pu047 -> Chinatown ('' si ce n'est pas une piste du combat 1)."""
    try:
        return NOMS_DES_LIEUX.get('pu%03d' % (int(card_id_piste[2:5]) - 9), '')
    except ValueError:
        return ''


def NoterLeLieuDeLaDernierePiste(effect: 'Effect', piste: 'CardFace|None') -> None:
    """pu002a : « (In campaign mode, record the location where the final LEAD card was added to the victory display.) »"""
    if piste is None or not Worlds.IsCampaign(effect):
        return
    lieu = LieuDeLaPisteGagnee(piste.paper.card_id)
    if lieu:
        CampaignLog.SetStr(CLE_LIEU, lieu, effect.world)


def _trafiquant(effect: 'Effect') -> str:
    """Le nom (sans l'etoile des uniques) du CAPO auquel Gunrunner (pu004) est attache, '' si Gunrunner n'est pas en jeu."""
    # ⚠ Au `WhenGameOver` de la victoire par Gunrunner, le CAPO vaincu a deja quitte le terrain : `FindCardsOnField` ne voit plus pu004 (cas
    # rouge). On parcourt donc TOUTES les cartes du monde ; le lien `bind_face` survit a la defaite.
    for objet in effect.world.object_manager.card_dict.values():
        face = getattr(objet, 'face', None) or objet
        if getattr(getattr(face, 'paper', None), 'card_id', None) == 'pu004' and getattr(face, 'bind_face', None) is not None:
            return face.bind_face.paper.name.lstrip('* ')
    return ''


def MiseEnPlace() -> 'Ability':
    """Battle Setup de pu140 : l'environnement entre en jeu (les sets, Uptown et les pions viennent du scenario)."""
    return AbilityFactoryCampaign.PutCardIntoPlay(ENVIRONNEMENT_COMBAT_1)


def _par_joueur(effect: 'Effect') -> Dict[str, Any]:
    """`Player N Remaining hit points` et `Player N Identity`. ⚠ `WriteCampaignLogAtGameOver` les ecrit avec `Worlds.GetPlayers(effect)`, qui
    filtre par la ZONE de la carte porteuse : dans la ville (une zone par rangee) il ne voit AUCUN joueur depuis le complot (zone commune) et
    les deux cles manquaient (campagne experte sans PV, pu141 sans carnet de la partie precedente). On les ecrit ici pour TOUS les joueurs."""
    updates: Dict[str, Any] = {}
    for joueur in effect.world.const_players:
        identite = joueur.GetIdentity()
        if identite is None:
            continue
        updates[f'Player {joueur.player_id + 1} Remaining hit points'] = str(max(0, identite.health))
        try:
            updates[f'Player {joueur.player_id + 1} Identity'] = identite.GetHeroFace().paper.name.lstrip('* ')
        except AssertionError:
            pass
    return updates


def Releve(effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """Ce que le livret fait noter a la VICTOIRE du combat 1 (rien a la defaite, hors PV restants et identites)."""
    updates: Dict[str, Any] = _par_joueur(effect)
    if not message.players_won:
        return updates
    updates.update({CLE_COMBAT_1: 'Flipped', CLE_CAISSES: '1'})
    trafiquant = _trafiquant(effect)
    if trafiquant:
        updates[CLE_TRAFIQUANT] = trafiquant
    return updates


def CampaignSetup() -> 'List[Ability]':
    """Ce que le complot principal 1A (pu001a) doit appeler."""
    return [
        MiseEnPlace(),
        WriteCampaignLogAtGameOver(Releve, scenario_id=SCENARIO),
    ]


# ------------------------------------------------------------------------------------------------------------- combat 2 et suivants
def EnregistrerLeReleve(effect: 'Effect', collecteur: 'Callable[[Effect, Message.WhenGameOver], dict]', estampille: str) -> None:
    """Un combat 2 ou 3 joue sur un scenario Fear No Evil, dont le 1A ecrit DEJA son releve (`CollectFNE`). L'environnement du combat ne peut
    donc pas poser un second `WriteCampaignLogAtGameOver` (le dernier a ecrire gagnerait) : il declare un collecteur et l'estampille sur le
    monde, que chaque ecriture rejoue (voir `mts/campaign.py`)."""
    world = effect.world
    if not hasattr(world, 'campagne_collecteurs'):
        world.campagne_collecteurs = []
    world.campagne_collecteurs.append(collecteur)
    world.campagne_estampille = estampille


def MettreLesRecompenses(effect: 'Effect', *recompenses: 'tuple[str, str]') -> None:
    """Met en jeu, sous le controle du premier joueur, chaque recompense (cle du carnet, card_id) que le carnet dit gagnee."""
    from game.card.factory import CardFactory
    for cle, card_id in recompenses:
        if CampaignLog.GetStrInternal(cle, effect) == '1':
            carte = CardFactory.GenerateCard(card_id, None, effect.world)
            carte.face.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect, under_control=True)


def NomDuSousFifre(effect: 'Effect') -> str:
    """Le nom (sans etoile) du vilain en jeu : Hobgoblin ou Jigsaw au combat 2."""
    vilain = Worlds.FindVillain(effect)
    return vilain.paper.name.lstrip('* ') if vilain is not None else ''


def ReleveCombat2(sous_fifre: str, effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """pu142, Victory : « Flip this card and put Punisher's Ordnance Cache into play for battle 3. » + le sous-fifre affronte (combat 3 :
    l'autre). Rien a la defaite."""
    if not message.players_won:
        return {}
    updates: Dict[str, Any] = {CLE_COMBAT_2: 'Flipped', CLE_CACHE: '1'}
    if sous_fifre:
        updates[CLE_SOUS_FIFRE] = sous_fifre
    return updates


# Le tableau de p265 : le lieu de la derniere piste (combat 1) -> la manigance principale du combat 2.
MANIGANCE_DU_LIEU = {
    'Theater District': 'art_museum_heist', 'Financial District': 'art_museum_heist',
    "Hell's Kitchen": 'the_getaway', 'Lower East Side': 'the_getaway',
    'Upper East Side': 'the_raft_breakout', 'Midtown': 'the_raft_breakout',
    'Chinatown': 'protection_racket',
    'West Village': 'stop_the_presses', 'Soho': 'stop_the_presses',
}
# « Hobgoblin if Gunrunner was Count Nefaria, Ringmaster, Mr. Negative or Nightshade, or Jigsaw (other 4 CAPOS) ».
SOUS_FIFRE_DU_TRAFIQUANT = {'Count Nefaria': 'hobgoblin', 'Ringmaster': 'hobgoblin', 'Mister Negative': 'hobgoblin', 'Nightshade': 'hobgoblin',
                            'Crime-Master': 'jigsaw', 'Lady Yulan': 'jigsaw', 'The Rose': 'jigsaw', 'Diamondback': 'jigsaw'}


def ScenarioDuCombat2(lieu: str, trafiquant: str, expert: bool=False) -> str:
    """Le fichier de scenario du combat 2, d'apres le carnet du combat 1 ('' si le carnet est incomplet)."""
    manigance = MANIGANCE_DU_LIEU.get(lieu)
    sous_fifre = SOUS_FIFRE_DU_TRAFIQUANT.get(trafiquant)
    if manigance is None or sous_fifre is None:
        return ''
    return f"tracking_the_buyer_{manigance}_{sous_fifre}" + ('_expert' if expert else '')


# ------------------------------------------------------------------------------------------------------------------------------ combat 3
def ReleveCombat3(effect: 'Effect', message: 'Message.WhenGameOver') -> dict:
    """Instructions de campagne du combat 3 : « VICTOIRE : Vous avez gagne l'allie Punisher (6138). » Rien a la defaite."""
    if not message.players_won:
        return {}
    return {CLE_ALLIE_PUNISHER: '1'}


def RetournerPunishment() -> 'List[Ability]':
    """pu144 : « Forced Response : After Punisher's first stage is defeated or the main scheme advances to stage 2A, flip this card. »
    L'environnement (6134A) a pour verso la recompense S.H.I.E.L.D. Support Team (6134B) : on retire pu144 et on met pu145 en jeu (une seule fois,
    la carte disparaissant avec son retournement)."""
    from game.card.factory import CardFactory

    def retourner(effect: 'Effect', message: 'Message2') -> None:
        Unused(message)
        premier = Worlds.GetFirstPlayer(effect)
        Faces.RemoveAllFromGame([effect.this], effect)
        carte = CardFactory.GenerateCard(SOUTIEN_SHIELD, None, effect.world)
        carte.face.PutIntoPlay(premier, effect, under_control=True)

    def vers_2a(effect: 'Effect', message: 'Message.AfterMainSchemeAdvanced') -> bool:
        return message.scheme.paper.card_id.startswith('pu089a')

    def premier_stade_du_punisher(effect: 'Effect', message: 'Message.AfterVillainAdvanced') -> bool:
        return message.trigger.paper.name.lstrip('* ').startswith('Punisher')

    return [
        Ability(AbilityType.ForcedResponse, Message.AfterMainSchemeAdvanced, [vers_2a], retourner),
        Ability(AbilityType.ForcedResponse, Message.AfterVillainAdvanced, [premier_stade_du_punisher], retourner),
    ]


# Combat 3 : le sous-fifre que l'on n'a PAS affronte au combat 2 (« Hobgoblin or Jigsaw that you did not use in campaign battle 2 »).
def ScenarioDuCombat3(sous_fifre_du_combat_2: str, expert: bool=False) -> str:
    """Le fichier de scenario du combat 3 d'apres le carnet ('' si le sous-fifre du combat 2 n'est pas note)."""
    autre = {'jigsaw': 'hobgoblin', 'hobgoblin': 'jigsaw'}.get(sous_fifre_du_combat_2.strip().lower())
    return f"punishment_{autre}" + ('_expert' if expert else '') if autre else ''


# ------------------------------------------------------------------------------------------------------ campagne experte, combats 2 a 4
def SoignerParRec(effect: 'Effect') -> None:
    """Le corps de `SoinExpertParRec`, appelable depuis le Setup d'une carte qui sort du jeu elle-meme (pu147 : sa 2e capacite ne partirait pas)."""
    if not Worlds.IsExpert(effect) or not Worlds.IsCampaign(effect):
        return
    this = effect.this
    for joueur in Worlds.GetPlayers(effect):
        identite = joueur.GetIdentity()
        if identite is None:
            continue

        def soigner(cibles: 'Sequence[CardFace]', joueur: 'Player'=joueur, identite: 'CardFace'=identite) -> None:
            joueur.DealEncounterCards(1, effect)
            this.HealthUnits([identite], getattr(identite, 'recover', 0), effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal yourself 1 facedown encounter card to heal damage from your identity equal to your REC",
                soigner,
            ).SetTarget([identite], canbe_heal=True),
        )




def SoinExpertParRec() -> 'Ability':
    """Instructions de campagne des combats 2, 3 et 4, « Campagne experte uniquement » : « chaque joueur a le droit de s'attribuer une carte Rencontre face
    cachee pour soigner son identite d'un nombre de degats egal a sa REC ».

    Cartes de reference : `game/ability/factory/campaign.py` `ExpertCampaignEachPlayerMayDealFacedownEncounterCardYpHealHP` (sm, next_evol : la meme carte face
    cachee, mais soin COMPLET), `aos/campaign.py` `SoinExpertDuConseil` (soin de la REC : `identite.recover`, lue sur la face alter-ego active au debut).
    ⚠ Pieges : (1) « a player MAY » : `MayChooseOneAbility`, le joueur peut refuser ; (2) soigne de la REC, pas jusqu'aux PV imprimes ; (3) APRES la remise des
    PV reportes (`ExpertCampaignSetPlayersHPToTheirRemainingHP`, dans le scenario ou dans la carte de campagne) : donc `AfterGameSetup` (apres toute la mise en
    place de campagne) ; (4) campagne experte seulement (`Worlds.IsExpert`) ; (5) la carte vient du deck rencontre (`DealEncounterCards`)."""
    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Unused(message)
        SoignerParRec(effect)

    return AbilityFactory.AfterGameSetup(mise_en_place)
