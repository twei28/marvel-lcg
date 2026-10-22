from . import *

# Tracking the Buyer — ENVIRONNEMENT de campagne (combat 2, p265). Setup. Permanent.
# Battle Setup : Villain Hobgoblin (si Gunrunner etait Count Nefaria, Ringmaster, Mr. Negative ou Nightshade) ou Jigsaw (les 4 autres CAPO) ;
#   sets Punisher's Hit List, The Syndicate, Capo of the Past ; manigance principale selon la derniere piste (tableau).
# Victory : Flip this card and put Punisher's Ordnance Cache into play for battle 3.
#
# Cartes de reference : pu140 (meme famille : mots-cles dans `desc`, Battle Setup porte par le scenario), `campaign.py` (`EnregistrerLeReleve`,
# `MettreLesRecompenses`, `ReleveCombat2`), fne/campaign.py `MettreLesEnvironnements` (un environnement de campagne mis en jeu a la mise en place).
# ⚠ Le Battle Setup est dans les SCENARIOS generes `data/scenarios/tracking_the_buyer_<manigance>_<sous-fifre>(_expert).json` (choisis par
# `ScenarioDuCombat2` d'apres le carnet) : ce script ne fait que (1) mettre en jeu Seized Tech Crates si le carnet l'a gagnee (« for battles 2
# and 3 ») et (2) declarer le releve de victoire. L'environnement entre en jeu par le mot-cle Setup, via la liste `encounters` du scenario.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        Unused(message)
        sous_fifre = NomDuSousFifre(effect)
        EnregistrerLeReleve(effect, lambda e, m: ReleveCombat2(sous_fifre, e, m), 'tracking_the_buyer')
        MettreLesRecompenses(effect, (CLE_CAISSES, CAISSES))

    return [AbilityFactoryCampaign.WhenCampaignSetup(mise_en_place)]
