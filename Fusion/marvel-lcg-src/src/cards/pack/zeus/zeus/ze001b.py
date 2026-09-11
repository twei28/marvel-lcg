from . import *

# * Zeus Panhellenios (alter ego)
# God of Lightning — Action: Search your deck and discard pile for the
# Thunderbolt upgrade and add it to your hand. (Limit once per round.)
#
# Modele : 03001b Steve Rogers (Search.PlayerCard deck + defausse, puis
# GainCard). ⚠ `card_type=Upgrade` et le NOM exact : `50131b` Thunderbolt
# Backup et `57021` The Thunderbolts existent, une recherche par sous-chaine
# les attraperait.

def GetAbilities() -> Sequence['Ability']:

    def god_of_lightning(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            name=THUNDERBOLT,
            card_type=Upgrade,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            god_of_lightning,
        ).LimitOncePerRound()
        .SetName(GOD_OF_LIGHTNING),
    ]
