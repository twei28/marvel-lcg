from . import *

# hs020 Vermin Cloning
# When Revealed: Search the encounter deck and discard pile for a copy of Vermin Clone
# and put it into play engaged with the first player.

def GetAbilities() -> Sequence['Ability']:

    def clone(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndPutIntoPlay(
            effect, Worlds.GetFirstPlayer(effect), finder=CardFinder(name="Vermin Clone", card_type=Minion,
            check_face_fn=lambda f: not f.IsInPlay()),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, clone),
    ]
