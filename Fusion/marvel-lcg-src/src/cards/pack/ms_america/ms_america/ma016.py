from . import *

# Break Through (2/2) - exemplaire physique 2/2, contenu identique a
# ma015 (voir ce fichier pour le detail des modeles et du drapeau qui
# garantit un seul Etourdi/Desoriente).

DEGATS = 4
MENACE = 3


def GetAbilities() -> Sequence['Ability']:

    def break_through(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        une_defaite = [False]

        def noter(*args):
            Unused(args)
            une_defaite[0] = True

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Break Through: deal 4 damage to an enemy",
                lambda targets:
                    this.DealDamage(list(targets), DEGATS, effect,
                                    if_this_attack_defeats=noter),
            ).SetTarget(Enemy),
        )

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Break Through: remove 3 threat from a scheme",
                lambda targets:
                    this.RemoveThreatFromSchemes(list(targets), MENACE, effect,
                                                 if_this_remove_last_threat=noter),
            ).SetTarget(Scheme2),
        )

        if not une_defaite[0]:
            return

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Break Through: stun an enemy",
                lambda targets:
                    Faces.GiveStatus(list(targets), "Stunned", effect),
            ).SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility(
                "Break Through: confuse an enemy",
                lambda targets:
                    Faces.GiveStatus(list(targets), "Confused", effect),
            ).SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            break_through,
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
