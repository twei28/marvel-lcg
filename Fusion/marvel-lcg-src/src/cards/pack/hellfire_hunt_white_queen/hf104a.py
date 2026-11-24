from . import *
from cards.pack.hellfire_hunt.campaign import CampaignSetup

# Infiltrating the Mansion (1A). « Setup : Remove each minion named White Queen from the game. » (les deux sbires « White Queen » du module
# Perfection ne doivent jamais entrer en jeu : ils servent aux AUTRES scenarios, livret p. 8 ; eux-memes portent un Forced Interrupt qui les
# defausse s'ils tentent d'entrer en jeu).
# Cartes de reference : vt017a (`WhenCardSetup("This", ...)`), nt012 / 22027 (`Faces.RemoveAllFromGame`), 06027 (recherche par nom).
# Campagne (livret p.8) : `*CampaignSetup(1)` (cards.pack.hellfire_hunt.campaign) : allies Recruited mis de cote, Potential Ally, Cerebro Insights, Xavier's Institute
# + releve du carnet a la victoire. AJOUTE le 01/11/2026 en bouclant la chaine de campagne 1 -> 5 : le scenario 1 etait le seul a ne pas l'appeler (rien ne s'ecrivait au carnet).
# ⚠ Mot-piege : « minion named White Queen » : le VILAIN porte le meme nom ; le filtre est `Minion.IsType`.


def GetAbilities() -> Sequence['Ability']:
    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        sbires = [f for f in Worlds.GetEncounterDeckCards(effect) if Minion.IsType(f) and f.IsName(NOM_WQ)]
        if sbires:
            Faces.RemoveAllFromGame(sbires, effect)

    return [AbilityFactory.WhenCardSetup("This", mise_en_place), *CampaignSetup(1)]
