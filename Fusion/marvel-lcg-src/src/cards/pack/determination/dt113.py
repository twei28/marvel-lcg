from . import *

# * Tabula Rasa

def GetAbilities() -> Sequence['Ability']:

    def boite_vide(effect: 'Effect', face: 'CardFace') -> bool:
        return bool(face.GetKeyword('TreatAsBlank'))

    def tabula_rasa(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this.CastTo(Upgrade)
        porteur = this.GetBindFace()
        if porteur is None:
            return None
        return porteur.printed_resource

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Unit2, check_effect_fn=boite_vide)
        ),
        AbilityFactory.CheckThisCanDropPay(
            tabula_rasa,
            for_card=CardFinder(card_type=Event),
        ).SetCostFunc(CostFunc.Exhaust("Attached")),
    ]
