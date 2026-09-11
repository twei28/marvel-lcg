from . import *

# * Thunderbolt (amelioration, cout 0, OLYMPUS WEAPON, energie)
# Hero Resource: Exhaust Thunderbolt → generate a [energy] resource.
# Hero Response: After you resolve your "Skyfather's Tempest" ability, ready
# Thunderbolt.
#
# Modele : ab007 Donald Pierce, presque mot pour mot (ressource sur
# inclinaison + redressement apres une capacite nommee). ⚠ Elle genere une
# ENERGIE officielle, pas un eclair : c'est Mount Olympus (`ze011`) qui fait
# l'eclair. UNE SEULE CanGenerateResources par carte (assert du moteur).

def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("Y"),
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.HeroResponse,
            "You",
            CardFinder(name="Zeus", card_type=Hero),
            redresser,
            ability_name=TEMPEST,
        ),
    ]
