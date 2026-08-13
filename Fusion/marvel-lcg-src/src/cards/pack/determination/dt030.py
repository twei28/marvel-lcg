from . import *

# Adrenaline Shot

def GetAbilities() -> Sequence['Ability']:

    def adrenaline_shot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        for allie in effect.targets:
            allie = allie.CastTo(Ally)

            # « sa PROCHAINE attaque » : une capacite temporaire posee sur
            # l'allie et retiree des qu'elle a servi (mk023, The Hell Charger).
            def prochaine_attaque(effect2: 'Effect', message2: 'Message.WhenUnitWouldAttack',
                                  allie: 'Ally'=allie) -> None:
                # « inflige 2 degats supplementaires » : ce sont les DEGATS qu'on
                # augmente, pas l'ATK — sinon un effet qui lit l'ATK entre-temps
                # verrait un chiffre que la carte ne donne pas. Le moteur publie
                # `IncreaseDamage` sur la fenetre des degats, posee ici le temps
                # de cette attaque.
                allie.effect.RegisterTemp(
                    AbilityFactory.WhenFaceWouldDealDamage(
                        AbilityType.ForcedInterrupt,
                        "This",
                        lambda effect3, message3: message3.IncreaseDamage(2, effect3),
                    ),
                    unregister_after_exec=True,
                )
                allie.GainForThisActive(effect2, message2, attack_consequential_damage=1)

            allie.effect.RegisterTemp(
                AbilityFactory.WhenUnitMakeAttack(
                    AbilityType.ForcedInterrupt,
                    "This",
                    prochaine_attaque,
                ),
                unregister_after_exec=True,
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            adrenaline_shot
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'adrenaline'))
        .SetTarget(Ally),
    ]
