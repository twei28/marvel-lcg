from . import *

# Lightforce Daggers — custom « DesignHacker »
# Hero Action (attack): Deal a total of 3 damage divided among enemies as you
#   choose and stun the villain. Then, if Cloak is in play, confuse an enemy.
# (En Hero Action, l'identité est forcément en forme héros : « if Cloak is in
#  play » est toujours vrai ici, le confuse suit donc systématiquement.)


def GetAbilities() -> Sequence['Ability']:

    def lightforce_daggers(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        # 1 dégât par attribution, montage Wasp Sting 13006.
        this.DealDamage(effect.targets, 1, effect)

        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if vilain:
            Faces.GiveStatus([vilain], "Stunned", effect)

        if CloakEstEnJeu(effect):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Confuse an enemy",
                    lambda targets: Faces.GiveStatus(targets, "Confused", effect),
                ).SetTarget(Enemy, canbe_confused=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lightforce_daggers,
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy, range=(1, 3), repeat_rules="Health"),
    ]
