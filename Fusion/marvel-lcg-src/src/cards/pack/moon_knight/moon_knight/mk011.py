from . import *

# Versatility — custom « DesignHacker »
# Treat this card as any aspect you choose. (règle de deck-building, sans effet
# moteur : la carte est signature et rentre dans le deck de toute façon)
# Hero Action: If the aspect of the top card on your discard pile is:
# - Aggression: deal 4 damage to an enemy. - Justice: remove 3 threat from a
#   scheme. - Leadership: confuse an enemy. - Protection: stun an enemy.


def GetAbilities() -> Sequence['Ability']:

    def versatility(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        dessus = None
        for face in initiator.discard_pile.Get():
            dessus = face
            break
        if dessus is None:
            return
        classe = dessus.paper.desc.get("Class", "") \
            if hasattr(dessus.paper, "desc") else ""

        if classe == "Aggression":
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 4 damage to an enemy",
                    lambda targets: this.DealDamage(list(targets), 4, effect),
                ).SetTarget(Enemy),
            )
        elif classe == "Justice":
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 3 threat from a scheme",
                    lambda targets: this.RemoveThreatFromSchemes(list(targets), 3, effect),
                ).SetTarget(Scheme2),
            )
        elif classe == "Leadership":
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Confuse an enemy",
                    lambda targets: Faces.GiveStatus(targets, "Confused", effect),
                ).SetTarget(Enemy, canbe_confused=True),
            )
        elif classe == "Protection":
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy",
                    lambda targets: Faces.GiveStatus(targets, "Stunned", effect),
                ).SetTarget(Enemy, canbe_stunned=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            versatility,
        ).SetPlay(),
    ]
