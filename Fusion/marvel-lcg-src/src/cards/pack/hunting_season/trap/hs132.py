from . import *

# hs132 Capture Net
# When Revealed : epuiser son identite ou attacher. Forced Interrupt : fin de phase heros, depensez une ressource
# physique ou epuisez votre identite. Interrupt : quand vous allez attaquer, depensez une ressource physique →
# defaussez Capture Net a la place.

def GetAbilities() -> Sequence['Ability']:

    def serrer(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(Attachment)
        cible = this.bind_face
        joueur = None if cible is None else cible.GetControlByPlayer()
        if cible is None or joueur is None:
            return

        def epuiser(cibles: Sequence['CardFace']) -> None:
            Faces.ExhaustAll([cible], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(Cost("R")),
            AbilityFactory.ForChoiceAbility("Exhaust your identity", epuiser, condition=cible.IsReady()),
        )

    def echapper(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.SetBeInstead(effect)
        Faces.DiscardAll([effect.this], effect)

    def porteur_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return PorteurEstAttaquant(effect, message)

    return [
        PiegeAttachement(),
        AbilityFactory.WhenPlayerPhaseEnd(AbilityType.ForcedInterrupt, serrer),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, "Character", echapper, conditions=[porteur_attaque])
            .SetCost(Cost("R")),
    ]
