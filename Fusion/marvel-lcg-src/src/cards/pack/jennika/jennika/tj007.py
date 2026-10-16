from . import *

# * Jenny's Crib — SOUTIEN signature, x1. LOCATION. NYC. SKYLINE. Cout 1, [energy].
# Alter-Ego Action: Exhaust Jenny's Crib and discard 1 card from your hand ->
#   draw 1 card and ready your identity.
#
# Cartes de reference :
#  - `bkw/black_widow/08005` Safe House #29 : soutien a `AlterEgoAction` +
#    `CostFunc.Exhaust("This")` ;
#  - cout a deux parties (incliner ET defausser 1 carte) : `sunfire/sf010` /
#    `michelangelo/tm001b` : deux `SetCostFunc` chaines, `CostFunc.Discard(
#    "YourHandCards", range=(1, 1))` ;
#  - piocher : `joueur.DrawUp(1, effect)` ; redresser : `Faces.ReadyAll`.
#
# ⚠ Mots-pieges :
#  - « Alter-Ego Action » : forme alter-ego obligatoire ;
#  - le « -> » regroupe DEUX couts : incliner la Crib ET defausser 1 carte de la
#    main ; sans carte en main l'action n'est pas jouable ;
#  - « ready YOUR IDENTITY » : l'identite (alter-ego ici), pas le heros nomme ;
#  - « draw 1 card AND ready » : les deux effets, dans cet ordre.


def GetAbilities() -> Sequence['Ability']:

    def jennys_crib(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)
        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            jennys_crib,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
