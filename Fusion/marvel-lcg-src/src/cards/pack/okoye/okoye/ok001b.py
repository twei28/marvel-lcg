from . import *

# * Okoye (face alter-ego)
# Vanguard Leader — Setup: Search your deck and discard pile for a
#   REINFORCEMENTS card and add it to your hand. (Shuffle.)
# Marshalling Forces — Action: Shuffle a REINFORCEMENTS card from your
#   discard pile into your deck. (Limit once per round.)
#
# Modele du Setup : T'Challa (core/black_panther/01040b.py), meme structure
# `AbilityFactory.WhenCardSetup("This", ...)` + `Search.PlayerCard(...)` +
# `initiator.GainCard(face, effect)` (T'Challa cherche par trait dans le
# deck seul ; ici deck ET defausse, comme imprime). "Shuffle a REINFORCEMENTS
# card from your discard pile into your deck" : modele kb002/kb001a
# (`Faces.ShuffleAllTo`).


def GetAbilities() -> Sequence['Ability']:

    def vanguard_leader(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            trait="REINFORCEMENTS",
        )
        if face:
            initiator.GainCard(face, effect)

    def marshalling_forces(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=False,
            include_discard_pile=True,
            trait="REINFORCEMENTS",
        )
        if face:
            Faces.ShuffleAllTo([face], initiator.player_deck, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            vanguard_leader,
        ).SetName("Vanguard Leader"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            marshalling_forces,
        ).SetName("Marshalling Forces")
        .LimitOncePerRound(),
    ]
