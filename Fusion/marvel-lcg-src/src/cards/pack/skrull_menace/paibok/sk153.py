from . import *

# Trapped in Ice — ATTACHEMENT x2 (Paibok). CONDITION. Etoile de boost.
# Attach to your identity.
# Forced Interrupt: When you attack, reduce the amount of damage that attacks deals by 1.
# Hero Action: Spend [physical][physical] resources → discard this card.
# [star] Boost: Take 1 damage.
#
# Cartes de reference :
#  - Attache : **`27166`** Webbed Up ; fenetre « when you attack » : `AbilityFactory.WhenUnitWouldAttack(
#    ForcedInterrupt, "AttachedIdentity", ...)` (do_attack.py:32).
#  - Malus de degats : **`19018`** Subdue / `drax` : `message.GainATKForThisAttack(-1, effect)` ; hors
#    attaque de base : `message.DealAdditionalDamage(-1, effect)` (modele `55053`).
#  - Boost « take 1 damage » : `identity.TakeDamage(this, 1, effect)` (modele `27166`).
#  - Cout 2 physiques : `Cost("RR")` (modele 01100, `RRR`).
#
# ⚠ Mots-pieges : « When YOU attack » = l'identite attachee, pas un allie ; « by 1 » sur les degats de
# CETTE attaque ; texte imprime « attacks deals » (coquille de l'auteur, laisse tel quel) ; cout
# `[physical][physical]` = `RR` (poings).


def GetAbilities() -> Sequence['Ability']:

    def gele(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        if message.IsBasicAttack():
            message.GainATKForThisAttack(-1, effect)
        else:
            message.DealAdditionalDamage(-1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)
        message.GetToPlayer().GetIdentity().TakeDamage(this, 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "AttachedIdentity", gele),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("RR")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
