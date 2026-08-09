from . import *

# Living Light — custom « DesignHacker »
# This card cannot be exhausted until you have dealt 5 or more damage to the
#   villain this phase.
# Hero Action: Exhaust Living Light → ready Dagger.
#
# « Cannot be exhausted » est rendu par une CONDITION sur l'action (seule
# capacité qui incline la carte). Le compteur de dégâts vit sur `world`
# (helpers du __init__ du set) : il est alimenté ici par AfterUnitTookDamage
# sur le méchant et remis à zéro à chaque début de phase. Les dégâts infligés
# AVANT l'entrée en jeu de l'upgrade ne sont pas comptés : écart minime,
# documenté au §9.


def GetAbilities() -> Sequence['Ability']:

    def compter_degats(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        par_joueur = message.GetByPlayer()
        if par_joueur is None:
            return
        AjouterDegatsVilainCettePhase(effect.world, par_joueur, message.took_damage)

    def remettre_a_zero(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        RemettreDegatsVilainPhase(effect.world)

    def seuil_atteint(effect: 'Effect', message: 'Message2') -> bool:
        controleur = effect.this.GetControlByPlayer()
        if controleur is None:
            return False
        return DegatsVilainCettePhase(effect.world, controleur) >= 5

    def living_light(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        dagger = TrouverDagger(effect)
        if dagger:
            Faces.ReadyAll([dagger], effect)

    return [
        Ability(
            AbilityType.Temp0,
            Message.AfterUnitTookDamage,
            [
                lambda effect, message: Villain.IsType(message.trigger),
            ],
            compter_degats,
        ),
        Ability(
            AbilityType.Temp0,
            Message.AfterPhaseBegin,
            [],
            remettre_a_zero,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            living_light,
            conditions=[seuil_atteint],
        ).SetName("Living Light")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
