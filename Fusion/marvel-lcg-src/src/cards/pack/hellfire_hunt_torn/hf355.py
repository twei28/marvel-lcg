from . import *

# Jumpstart (x2 : hf355, hf356). Attachement CONDITION, +2 SCH, ATQ [star], [star] Boost 0 icone. « Attach to the highest hit-point minion. Otherwise, this gains surge.
# [star] Forced Interrupt : When the attached character attacks you, give them 1 additional boost card for this activation. [star] Boost : Deal yourself 1 facedown
# encounter card. » +2 SCH (`desc.SCH+`) : natif.
# Cartes de reference : 01133 / 04119 (`AttachToFaceWhenPutIntoPlay(Minion, highest_printed_hp=True, if_cannot_gain_surge=True)`), 02020 Hysteria (`message.
# GiveAdditionalBoostCardForThisActivation(1, effect)` sur `WhenUnitWouldAttack`), `WhenUnitAttackYou`.
# ⚠ « highest hit-point » lu comme les PV IMPRIMES les plus hauts (`highest_printed_hp`) ; « attacks YOU » : une attaque contre un autre joueur ne donne pas la carte de boost.


def GetAbilities() -> Sequence['Ability']:
    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Minion, highest_printed_hp=True, if_cannot_gain_surge=True),
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "AttachedCharacter", attaque),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
