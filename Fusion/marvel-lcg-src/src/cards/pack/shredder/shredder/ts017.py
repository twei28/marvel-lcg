from . import *

# Shred (x3) — TRAITRISE. 2 icones de boost + etoile.
# When Revealed (Alter-Ego): Place a cloaked status card on Shredder.
# When Revealed (Hero): Shredder attacks you. Do not give Shredder any boost
#   cards for this activation.
# [star] Boost: After this activation resolves, cloak Shredder.
#
# Cartes de reference : `01187` Assault (le couple `WhenThisRevealed("Hero")` /
# `("Alter-Ego")`), `ts015` (attaque sans boost), `ts013` (boost « after this
# activation resolves, cloak Shredder »).
#
# Mots-pieges : deux When Revealed DISTINCTS selon la forme (sans « surge » en
# alter-ego : il pose seulement la carte) ; « place a cloaked status card ON
# Shredder » = `Cloak`.


def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Cloak(effect, TrouverShredder(effect))

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        ShredderAttaqueSansBoost(effect, message.GetToPlayer())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.AfterThisActivation(effect, lambda: Cloak(effect, TrouverShredder(effect)))

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
