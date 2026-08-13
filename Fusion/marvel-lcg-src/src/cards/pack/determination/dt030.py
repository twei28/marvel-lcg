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
                # « deals 2 additional damage » : le moteur n'a qu'un levier
                # pour le degat d'une attaque, l'ATK de cette attaque. L'ecart
                # ne se voit que pour un effet qui LIRAIT l'ATK entre-temps.
                message2.GainATKForThisAttack(2, effect2)
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
