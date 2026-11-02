from . import *

# * White Phoenix (Hope Summers) : allie Basic, cout 4, PV 3, THW 1*, ATK 3*. PSIONIC. X-FORCE.
# White Phoenix gains each TRAIT on your identity.
# Interrupt: When White Phoenix leaves play, search your discard pile for an event card and add it to your hand.
#
# Cartes de reference : `AbilityFactory.ThisGainEachTraitOnYourIdentity` (ability_factory.py), `WhenCardLeavePlay` (card_move.py:208),
# `Search.PlayerCard(include_discard_pile=True, card_type=Event)` (Ch'od sy001).
def GetAbilities() -> Sequence['Ability']:
    def phoenix(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        joueur = JoueurDe(effect)
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=False,
            include_discard_pile=True,
            card_type=Event,
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        *AbilityFactory.ThisGainEachTraitOnYourIdentity(),
        AbilityFactory.WhenCardLeavePlay(
            AbilityType.Interrupt,
            "This",
            phoenix,
        ),
    ]
