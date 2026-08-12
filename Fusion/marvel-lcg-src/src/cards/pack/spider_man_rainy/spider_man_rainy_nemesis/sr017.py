from . import *

# Smoke and Mirrors — custom « Rainy » (nemesis de Peter Parker)
# Surge.
# When Revealed: Give Mysterio a tough status card and a facedown boost card.
#   If you cannot, give the villain a tough status card and a facedown boost
#   card.
# [star] Boost: You are confused.

def GetAbilities() -> Sequence['Ability']:

    def smoke_and_mirrors(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        mysterios = [
            x for x in Worlds.FindCardsOnField(effect, name="Mysterio", card_type=Minion)
        ]
        cible = mysterios[0] if mysterios else Worlds.FindVillain(effect)
        if not cible:
            return
        Faces.GiveStatus([cible], "Tough", effect)
        cible.GiveFacedownBoostCardsInternal(1, effect, None)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        if player:
            Faces.GiveStatus([player.GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, smoke_and_mirrors),

        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
