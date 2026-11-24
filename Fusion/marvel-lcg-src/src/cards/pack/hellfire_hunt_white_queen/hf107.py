from . import *

# Crystalline Adaptation (x3). Attachement SKILL. « Max 1 per enemy. Attach to White Queen. Otherwise, this card gains surge. »
# « Forced Interrupt : When White Queen is attacked, if she is in PSIONIC form, flip her and discard this card. »
# « [star] Boost : After this activation, if White Queen is in DIAMOND form, flip her and place 2 threat on the main scheme. »
# +1 SCH / +1 ATK : `desc.SCH+` / `desc.ATK+`, appliques par le moteur a la carte portee (`has_modify.py`).
# Cartes de reference : 04119 Neurological Implants (`AttachToFaceWhenPutIntoPlay(... without_another_copy=True, if_cannot_gain_surge=True)`),
# 16095 / 01121 (boost `message.AfterThisActivation`), valk 25011 (`WhenUnitBeingAttack`).


def GetAbilities() -> Sequence['Ability']:
    def attaquee(effect: 'Effect', message: 'Message.WhenUnitBeingAttack') -> None:
        this = effect.this
        villain = VilainWQ(effect)
        if EstPsionique(villain):
            RetournerWQ(effect, villain)
            Faces.DiscardAll([this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        def apres_l_activation() -> None:
            villain = VilainWQ(effect)
            if EstDiamant(villain):
                RetournerWQ(effect, villain)
                MenaceSurLeComplotPrincipal(effect, 2)

        message.AfterThisActivation(effect, apres_l_activation)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(ChercheurWQ(), without_another_copy=True, if_cannot_gain_surge=True),
        AbilityFactory.WhenUnitBeingAttack(AbilityType.ForcedInterrupt, ChercheurWQ(), None, attaquee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
