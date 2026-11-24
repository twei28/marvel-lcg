from . import *
from cards.pack.hellfire_hunt.campaign import CampaignSetup

# Jailbreak at the Hellfire Club (1A). « Setup : Remove each minion named Sebastian Shaw from the game. Set each CAPTIVE ally aside. Reveal the
# Captured by Hellfire! side scheme. Attach Black King to Sebastian Shaw. » (`MiseEnPlaceDuScenario`, __init__.py) + mise en place de CAMPAGNE
# commune (`CampaignSetup(2)` : deck Recruited Mutants, Potential Ally, Xavier's Institute, Emma Frost's Redemption).
# Cartes de reference : hf104a (White Queen : `WhenCardSetup("This", ...)` + `Faces.RemoveAllFromGame`), tk001a (Black King = attachement mis
# de cote par le scenario puis mis en jeu), cards.pack.skrull_menace.campaign (`CampaignSetup`).
# ⚠ Mot-piege : « minion named Sebastian Shaw » : le VILAIN porte le meme nom ; le filtre est `Minion.IsType`.


def GetAbilities() -> Sequence['Ability']:
    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        MiseEnPlaceDuScenario(effect)

    return [AbilityFactory.WhenCardSetup("This", mise_en_place), *CampaignSetup(2)]
