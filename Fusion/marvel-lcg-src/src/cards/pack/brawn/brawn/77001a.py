from . import *

# * Brawn (face heros) — custom « Rainy »
# The Complete Package — While Brawn is exhausted, he gains:
#   "Resource: Generate a [mental] resource. (Limit once per phase.)"
#
# La capacite n'existe QUE tant que Brawn est epuise : c'est une condition
# verifiee au moment ou le moteur recense les sources de paiement, pas un bonus
# pose une fois pour toutes. Meme montage que les identites generatrices
# officielles (Peter Parker 01001b, Star-Lord), a ceci pres que celles-la
# generent en s'epuisant : Brawn, lui, genere PARCE QU'il est deja epuise.

def GetAbilities() -> Sequence['Ability']:

    def brawn_est_epuise(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        this = effect.this.CastTo(Hero)
        return this.card.IsExhaust()

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("B"),
            conditions=[brawn_est_epuise],
        ).SetName("The Complete Package").LimitOncePerPhase(),
    ]
