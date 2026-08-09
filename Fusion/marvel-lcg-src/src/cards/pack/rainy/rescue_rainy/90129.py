from . import *

# Wounded Civilians

# La carte parle de « civilian counters », mais le moteur ne connait pas ce nom
# de compteur ; « bystander » existe et designe exactement la meme chose (des
# passants a secourir). Comportement identique, seul le libelle du texte differe.
COMPTEUR = 'bystander'


def GetAbilities() -> Sequence['Ability']:

    def reste_des_civils(effect: 'Effect', message: 'Message2') -> bool:
        return effect.this.GetCounters(COMPTEUR) > 0

    def a_la_place_du_soin(effect: 'Effect', message: 'Message.WhenUnitHealHealth') -> None:
        this = effect.this

        # Le soin est remplace par le retrait d'un compteur.
        message.SetBeInstead(effect)
        Faces.RemoveCountersOn([this], 1, COMPTEUR, effect)

    return [
        Ability(
            AbilityType.Interrupt,
            Message.WhenUnitHealHealth,
            [reste_des_civils],
            a_la_place_du_soin,
        ).SetName("Wounded Civilians"),
    ]
