from . import *

# hs141 Feral Instincts
# Attach to the villain. [star] Forced Interrupt: When the villain would scheme against you,
# it attacks you instead (overkill, no boost card). Then, discard Feral Instincts.
# Modele : fne 60182 (SetBeInstead puis attaque).

def GetAbilities() -> Sequence['Ability']:

    def attaque_a_la_place(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        joueur = message.GetAgainstPlayer()
        vilain = message.trigger.CastTo(Villain)
        message.SetBeInstead(effect)
        vilain.DoAttackYou(joueur, effect, property=AttackProperty(
            against_player=joueur, overkill=True, do_not_give_boost=True))
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Villain)),
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            attaque_a_la_place,
            against_player="You",
        ),
    ]
