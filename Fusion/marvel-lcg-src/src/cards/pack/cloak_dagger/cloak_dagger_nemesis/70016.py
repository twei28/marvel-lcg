from . import *

# Bigger Fish — custom « DesignHacker » (némésis de Cloak & Dagger)
# Forced Interrupt: When the villain or Mister Negative would attack, they
#   scheme instead.


def GetAbilities() -> Sequence['Ability']:

    def scheme_au_lieu_d_attaquer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        attaquant = message.attacker

        joueur = None
        for unite in message.attacked_targets:
            joueur = unite.GetControlByPlayer()
            if joueur is not None:
                break
        if joueur is None:
            joueur = effect.this.GetControlByPlayer()
        if joueur is None:
            return

        message.SetBeInstead(effect)
        attaquant.DoSchemes(joueur, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            Villain,
            scheme_au_lieu_d_attaquer,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Mister Negative", card_type=Minion),
            scheme_au_lieu_d_attaquer,
        ),
    ]
