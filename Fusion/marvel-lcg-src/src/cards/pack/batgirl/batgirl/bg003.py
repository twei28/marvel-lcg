from . import *

# * Nightwing — allie (Multiverse de bg002). « [star] Hero Response: After Nightwing uses a basic power, the next resource you
# generate is considered a [wild] resource rather than its printed type. »
# Carte de reference : `ah001a` Hypermind (`Message.CheckEffectGeneratedResources` + `message.SetResources(Resources("G") * n)`) ;
# ici POSE EN TEMP (un seul declenchement : « the next resource »), sur la carte elle-meme.


def GetAbilities() -> Sequence['Ability']:

    def nightwing(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        ConvertirEnWild(joueur, until_round=False, once=True, porteur=effect.this, origine=effect.this)

    return [
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.HeroResponse, "This", nightwing),
    ]
