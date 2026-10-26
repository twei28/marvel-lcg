from . import *

# Deranged Burst — evenement signature, x2. ATTACK. Cout 2, [physical].
# Hero Action (attack): Discard 1 card from your hand at random -> deal 6 damage to an enemy, this attack deals X additional
# damage, where X is equal to the numeral in the printed resource cost of that card. If you exhausted Wolverine's Claws to
# play this card, this attack gains piercing.
#
# Cartes de reference :
#  - `35010` Lunging Strike (Wolverine officiel) : « If you exhausted Wolverine's Claws to play this card, this attack gains
#    overkill » = `AttackProperty(overkill=...)` ; ici `piercing`, et les Griffes sont une RESSOURCE (uw002) : on lit les
#    effets qui ont paye (`effect.context.paid_this_res_effects`, modele `tj004`), helper `PayeeAvecLesGriffes` ;
#  - le COUT « discard 1 card at random » : `CoutDefausseAuHasard()` (helpers du set), qui garde la carte tiree.
#
# Mots-pieges : « at random » (pas de choix) ; « THAT card » (la carte defaussee, pas la carte jouee) ; « numeral in the
# PRINTED resource cost » (0 sans cout imprime) ; « this attack deals X ADDITIONAL » (6 + X en un seul coup).


def GetAbilities() -> Sequence['Ability']:

    def deranged_burst(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        perforant = PayeeAvecLesGriffes(effect)
        this.DealDamage(
            effect.targets,
            6 + XDeLaCarteDefaussee(effect),
            effect,
            property=AttackProperty(piercing=True) if perforant else None,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deranged_burst,
            conditions=[UneCarteADefausser],
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CoutDefausseAuHasard())
        .SetTarget(Enemy),
    ]
