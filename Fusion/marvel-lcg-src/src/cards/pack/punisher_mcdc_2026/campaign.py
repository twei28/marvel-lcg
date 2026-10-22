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
