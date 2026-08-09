from . import *

# The Bruiser
# Interrupt: When another SQUIRREL ally you control would take consequential
#   damage, exhaust The Bruiser → deal 1 of that damage to The Bruiser instead.
#
# Les ecureuils ne peuvent pas defendre : leurs degats viennent donc de leurs
# propres attaques et manigances, pas des cartes rencontre. C'est la seule
# blessure que The Bruiser peut utilement absorber.

def GetAbilities() -> Sequence['Ability']:

    def autre_ecureuil(effect: 'Effect', face: 'CardFace') -> bool:
        this = effect.this
        if face is this:
            return False
        joueur = this.GetControlByPlayer()
        return joueur is not None and face.GetControlByPlayer() == joueur

    def encaisser(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)
        message.PreventDamage(1, effect)
        this.TakeDamage(this, 1, effect)

    return [
        *Ecureuil(),
        (AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            CardFinder(card_type=Ally, traits=['SQUIRREL'], check_effect_fn=autre_ecureuil),
            encaisser,
            is_consequential_damage=True,
            conditions=[PasDeDiscorde],
        )
            .SetCostFunc(CostFunc.Exhaust("This"))),
    ]
