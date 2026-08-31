from . import *

# * Gwen Stacy Osborn — soutien signature. PERSONA. Cout 2.
# Harry Osborn gets +1 REC.
# Alter-Ego Action: Exhaust Harry Osborn and Gwen Stacy Osborn ->
#   confuse an enemy.
#
# Cartes de reference :
#  - +1 REC en continu : an002 * Sera (« Angela gets +1 hand size »), meme
#    `GiveKeywordToInPlayWhenApplyThis(Identity, control_by="You", ...)` —
#    Gwen est un SOUTIEN, pas un attachement, donc pas GiveKeywordToAttached ;
#  - double cout d'epuisement : 31009 SP//dr Command, chainage de deux
#    `SetCostFunc(CostFunc.Exhaust(...))` ;
#  - la confusion : 01083 * Mockingbird (GiveStatus + canbe_confused).
#
# PERSONA est un TRAIT du moteur (card_face.py, enum TRAITS), pas un mot-cle :
# aucune regle a scripter, il ne sert que de reference a d'autres cartes
# (ex. 60036 Eye on the Target vise les soutiens [[Persona]]).

def GetAbilities() -> Sequence['Ability']:

    def gwen(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        Faces.GiveStatus(effect.targets, "Confused", effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            gwen
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy, canbe_confused=True),
    ]
