from . import *

# hs083a Aerial Mayhem
# Setup : S.H.I.E.L.D. Wingsuits est cherche (paquet et defausse de rencontre), mis en jeu, puis 1B.
from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        if not Worlds.FindCardsOnField(effect, name="S.H.I.E.L.D. Wingsuits"):
            Find.FindAndPutIntoPlay(
                effect, Worlds.GetFirstPlayer(effect),
                finder=CardFinder(name="S.H.I.E.L.D. Wingsuits", card_type=Environment,
                                  check_face_fn=lambda f: not f.IsInPlay()),
            )

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        *CampaignSetup(4),
    ]
