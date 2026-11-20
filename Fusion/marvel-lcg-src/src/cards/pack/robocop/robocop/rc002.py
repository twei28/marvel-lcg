from . import *

# Authorized Force (x3) : EVENEMENT (ATTACK. THWART.), cout 2, [mental].
# Hero Action (attack/thwart): Remove 4 threat from a scheme. If that scheme has an [acceleration], [amplify], [crisis] or [hazard] icon, deal 2 damage to an enemy.
#
# CARTES DE REFERENCE
#  - `01012` Crisis Interdiction : evenement de CONTRE (`SetLabel('thwart')` + `SetTarget(Scheme2)` + `RemoveThreatFromSchemes`) puis une seconde cible choisie
#    apres coup par `ChooseAbilities` + `ForChoiceAbility("", fn).SetTarget(..)`. `jj/61040` : les quatre champs d'icones de manigance (`acceleration_icon`,
#    `amplify`, `crisis`, `hazard`).
#
# TEXTE CONTRE CODE
#  « a scheme » -> principal OU annexe (`Scheme2`). « If THAT scheme has an icon » -> la manigance visee, l'une des QUATRE icones imprimees (jamais « un
#    complot quelconque »). « deal 2 damage to AN enemy » -> un ennemi au choix, pas forcement lie a la manigance ; rien si la manigance n'a pas d'icone.
#  Label (attack/thwart) : les deux. Chiffres : cout 2, 4 menaces, 2 degats.


def GetAbilities() -> Sequence['Ability']:

    def authorized_force(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        cible = effect.targets[0] if effect.targets else None
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)
        if cible is None or not PorteUneIcone(cible):
            return
        effect.GetInitiator().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 2 damage to an enemy",
                lambda cibles:
                    this.DealDamage(cibles, 2, effect),
            ).SetTarget(Enemy),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            authorized_force,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Scheme2),
    ]
