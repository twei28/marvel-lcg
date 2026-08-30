from . import *

# Unrestrained (2/2) — exemplaire physique 2 de 2, contenu identique a
# ss009 (voir ce fichier pour le detail du modele repris).


def GetAbilities() -> Sequence['Ability']:

    def unrestrained(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        def on_excess(value: int) -> None:
            Unused(value)
            target = effect.targets[0]
            if Villain.IsType(target):
                Faces.GiveStatus([target], "Stunned", effect)
                Faces.GiveStatus([target], "Confused", effect)

        this.DealDamage(
            effect.targets, 7, effect,
            if_this_attack_deal_excess_damage=on_excess,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            unrestrained,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetName("Unrestrained"),
    ]
