from ..commun import *
from ..campaign import *

# ⚠ Le dossier porte le nom du set nettoye (`FileManager.CleanName("Campaign - The City Never Sleeps")`) : sinon le chargeur ne trouve aucun
# script (cartes sans capacite, sans erreur : trouve le 22/10/2026).
# Cartes de campagne de « La ville ne dort jamais » (MC×DC 2026) : pu140 Big Apple Gang War! (combat 1) et pu141 Seized Tech Crates
# (recompense du combat 1). La mise en place et le releve du carnet sont dans `punisher_mcdc_2026/campaign.py`.


def JetonsDeDepart(effect: 'Effect') -> int:
    """pu141, Setup : « Place 1 counter here, plus 1 more for each player who did not play the last game together. »
    Un joueur « nouveau » = un heros absent du carnet de la partie precedente (`Player N Identity`, ecrit par `WriteCampaignLogAtGameOver`)."""
    precedents = {CampaignLog.GetStrInternal(f'Player {i} Identity', effect) for i in range(1, 5)} - {''}
    if not precedents:
        return 1
    nouveaux = 0
    for joueur in effect.world.const_players:
        identite = joueur.GetIdentity()
        if identite is None:
            continue
        try:
            nom = identite.GetHeroFace().paper.name.lstrip('* ')
        except AssertionError:      # une identite sans face heros lisible (voir mts/campaign.py) : comptee comme nouvelle
            nom = ''
        if nom not in precedents:
            nouveaux += 1
    return 1 + nouveaux
