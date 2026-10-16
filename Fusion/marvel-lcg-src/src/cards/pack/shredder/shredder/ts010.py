from . import *

# Foot Ninja (x2) — SBIRE. FOOT CLAN. NINJA. MNG 1 / ATQ 1 / PV 1, 1 icone de boost + etoile.
# When Revealed: Cloak Foot Ninja.
# Forced Interrupt: When Foot Ninja is defeated, shuffle them into the encounter deck.
# [star] Boost: After this activation resolves, cloak the villain.
#
# Cartes de reference :
#  - `hood 24015` Griffin : « when defeated, shuffle into the encounter deck »
#    = `WhenUnitBeDefeated` + `Faces.ShuffleAllTo([this], deck, effect)` (la
#    defaite A LIEU : elle compte, contrairement a un « would be defeated ...
#    instead » comme `an014`) ;
#  - `hs042` / `aoa four_horsemen` : `message.AfterThisActivation(effect, op)`
#    pour « after this activation resolves ».
#
# Mots-pieges : « When Foot Ninja IS defeated » (pas « would ... instead ») :
# le sbire est vaincu PUIS melange ; « cloak THE VILLAIN » (le vilain, pas
# Shredder par nom) ; « THEM » = le sbire lui-meme.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Cloak(effect, effect.this)

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Faces.ShuffleAllTo([this], Worlds.GetEncounterDeck(effect), effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        def apres() -> None:
            Cloak(effect, Worlds.FindVillain(effect))

        message.AfterThisActivation(effect, apres)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedInterrupt, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
