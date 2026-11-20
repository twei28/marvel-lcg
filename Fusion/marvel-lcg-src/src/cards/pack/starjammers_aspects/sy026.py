from . import *
# * Polaris: Lorna Dane (Justice, allie 3 [energy], THW 2*, ATK 2**, PV 3). STARJAMMER. X-MEN.
# [star] Response: After Polaris takes consequential damage from thwarting, if that thwart removed the last threat from a scheme, give a
# her a tough status card.   (coquille imprimee : « give a her » ; lu « give her »)
#
# Cartes de reference : sh014 Minarai / leonardo tl009 (`AfterAllyTakeConsequentialDamage(.., "This", op, conditions=[..])`, filtre
# `from_performing="Thwart"`) ; `AfterUnitThwartAndRemoveLastThreat` (thwart.py:157) pour « removed the last threat » :
# `message.thw_message.remove_the_last_threat` ; `Faces.GiveStatus([this], "Tough", effect)`.
# « takes consequential damage FROM THWARTING » : seulement apres une MENEE (pas une attaque). « removed the LAST threat from A scheme »
# (au moins une manigance a perdu sa derniere menace, `remove_the_last_threat`). Polaris doit rester EN JEU (vaincue par ses propres degats
# consecutifs : rien a donner).
def GetAbilities() -> Sequence['Ability']:
    def polaris(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus([this], "Tough", effect)
    def derniere_menace(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> bool:
        return (message.thw_message is not None and message.thw_message.remove_the_last_threat
                and message.trigger is not None and message.trigger.IsInPlay())
    return [
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            polaris,
            from_performing="Thwart",
            conditions=[derniere_menace],
        ),
    ]
