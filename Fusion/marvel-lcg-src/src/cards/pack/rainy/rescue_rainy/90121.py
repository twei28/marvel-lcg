from . import *

# First Responder

def GetAbilities() -> Sequence['Ability']:

    def premiers_secours(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        blesse = message.trigger
        # 2 points si c'est une identite, 1 sinon.
        valeur = 2 if Identity.IsType(blesse) else 1
        this.HealthUnits([blesse], valeur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            None,
            premiers_secours,
            conditions=[
                # « another character » : jamais le porteur de la carte lui-meme.
                # Restreint volontairement aux personnages AMIS (identites et
                # allies) : le texte dit « personnage », donc en toute rigueur
                # le Mechant serait eligible, mais l'intention de la carte
                # (compteurs medicaux) est de soigner l'equipe, et proposer le
                # declenchement a chaque degat inflige au Mechant est penible.
                lambda effect, message:
                    message.trigger != effect.GetInitiator().GetIdentity() and
                    (Identity.IsType(message.trigger) or Ally.IsType(message.trigger))
            ],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'medical')),
    ]
