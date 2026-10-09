from . import *
from cards.pack.hunting_season.campaign import CampaignSetup

# Rats and More Rats 1A
# Setup: Put Even More Rats into play. Put a Regular Rats minion into play
# engaged with each player. Shuffle the encounter deck. Advance to stage 1B.
# Le passage en 1B est fait par le moteur (face A retournee apres la mise en place).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        Find.FindAndPutIntoPlay(effect, premier, name="Even More Rats", card_type=Environment)

        def rats_reguliers(joueur: 'Player') -> None:
            Find.FindAndPutIntoPlay(
                effect, joueur, finder=CardFinder(name="Regular Rats", card_type=Minion,
                check_face_fn=lambda f: not f.IsInPlay()),
            )
        Players.ForEachPlayer(effect, rats_reguliers)
        Worlds.GetEncounterDeck(effect).Shuffle(effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        *CampaignSetup(1),
    ]
