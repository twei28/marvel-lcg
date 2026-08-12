from . import *

# Burst Fire — custom « Rainy »
# Hero Action: Make the following two attacks:
# (attack): Deal 2 damage to an enemy. This attack gains ranged.
# (attack): Deal 2 damage to an enemy. This attack gains ranged.
#
# Modele : It's Clobberin' Time! (th010, The Thing), pour la boucle de deux
# attaques choisies via ForChoiceAbility (`SetLabel` doit preceder
# `SetTarget`, sans quoi la carte plante silencieusement, comme note dans ce
# fichier). Le ranged de chaque attaque reprend Psi-Bow Attack (41030,
# Psylocke) : `property=AttackProperty(ranged=True)` passe a `DealDamage`.

def GetAbilities() -> Sequence['Ability']:

    def burst_fire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()

        def une_attaque(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 2, effect, property=AttackProperty(ranged=True))

        for _ in range(2):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 2 damage to an enemy. This attack gains ranged.",
                    une_attaque
                ).SetLabel('attack').SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            burst_fire
        ).SetPlay().SetLabel('attack'),
    ]
