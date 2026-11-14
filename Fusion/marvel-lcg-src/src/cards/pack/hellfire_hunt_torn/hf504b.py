from . import *

# Nova's Psychic Puppetry, face B (FRAGMENT). « Permanent. Hinder 12[per_hero]. Each HELLFIRE minion gains the ILLUSION trait. Forced Interrupt : When the last
# threat is removed from this scheme, Emma Frost escapes from the control of Cassandra Nova, the players win the game. Forced Response : After an ELITE,
# HELLFIRE minion is defeated, remove 5 threat from another side scheme. Otherwise, remove 5 threat from here. »
# Cartes de reference : 27102b Light at the End (face B : `Worlds.SetGameOver(True, effect)` a la derniere menace), cw/56097b (`GiveKeywordToInPlayWhenApplyThis(...,
# trait=...)`), hf504a (reponse forcee).


def GetAbilities() -> Sequence['Ability']:
    def derniere_menace(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        Worlds.SetGameOver(True, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2(HELLFIRE, Minion), trait=ILLUSION, change_on_event=OnEvent.CardInPlay(Minion)),
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(AbilityType.ForcedInterrupt, derniere_menace),
        ReponseSbireEliteVaincu(),
    ]
