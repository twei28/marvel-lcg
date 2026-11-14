from . import *

# Ascending to Godhood (3A). « When Revealed : Find the Immortal Moon Goddess side scheme and reveal it. Find Blackheart and put it into play
# engaged with the first player. (Shuffle.) »
# Cartes de reference : hf105a / hf106a (`ChercherEtReveler`), hf318 Hellfire Hunt (« searches ... puts it into play engaged with them »),
# 04112b (`minion.PutIntoPlay(first_player, effect)` s'engage tout de suite).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        TrouverEtReveler(effect, NOM_MOON_GODDESS, premier)
        sbire = Search.EncounterCard(effect, "FirstPlayer", include_discard_pile=True, include_set_aside=True, name=NOM_BLACKHEART)
        if sbire is not None:
            sbire.PutIntoPlay(premier, effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
