from . import *
def GetAbilities() -> Sequence['Ability']:
    def unpreventable(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(Hero)
        # CORRECTIF (12/09/2026) : « takes 1 **unpreventable** damage (ignoring
        # tough) ». La carte nomme les DEUX regles, le code n'en rendait qu'une.
        # `ignore_tough` ne ferme que la carte Coriace ; une prevention chiffree
        # (08032) ou un remplacement (49006) passaient au travers.
        # `DamageProperty.unpreventable`, ajoute pour le pack `sentinel`, ferme
        # les trois portes.
        this.DealDamage(
            [this],
            DamageProperty(damage=1, ignore_tough=True, unpreventable=True),
            effect)
    return [
        AbilityFactory.ThisCanHaveAdditionalTough("Any"),
        AbilityFactory.UnitAttackGainKeyword(None, "This", lost_piercing=True),
        AbilityFactory.AfterStatusDiscardFrom(AbilityType.ForcedResponse, "This", "Tough", unpreventable),
    ]
