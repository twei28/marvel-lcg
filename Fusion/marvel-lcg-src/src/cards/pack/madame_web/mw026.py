from . import *

# * Spider-Woman: Veranke — custom « Kajislav », carte d'aspect LEADERSHIP
# Forced Interrupt: When Spider-Woman would be defeated, heal all damage from
#   her instead and engage her as a minion. Treat Spider-Woman as a minion with
#   a blank text box (except for TRAITS). Her SCH is equal to her printed THW
#   and she does not take consequential damage.
#
# `TreatAsMinion` (game/ability/factory/treat.py) fait exactement cela : il
# echange la face contre un gabarit Sbire, recopie ATK imprimee et prend le THW
# imprime comme SCH. Le gabarit `mweb_veranke_minion` est declare dans
# cards.json, sur le modele de `karma_controlled_ally`.

def GetAbilities() -> Sequence['Ability']:

    def veranke(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        from game.ability.factory.treat import TreatAsMinion

        this = effect.this.CastTo(Ally)

        message.SetBeInstead(effect)

        player = this.GetControlByPlayer()
        this.HealthUnits([this], "All", effect)

        TreatAsMinion(
            this,
            "mweb_veranke_minion",
            player,
            effect,
            process=lambda minion, ally, by_effect:
                minion.CopyTrait(ally, by_effect),
        )

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            veranke
        ),
    ]
