from . import *

# hs097 Knocked Out of the Sky
# Surge (donnees). When Revealed : si vous avez AERIAL, vous le perdez jusqu'a la fin de la ronde, puis 2 degats.

def GetAbilities() -> Sequence['Ability']:

    def abattre(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        identite = message.GetToPlayer().GetIdentity()
        if not identite.HasTrait("AERIAL"):
            return
        PerdreAerialJusquaLaRonde(identite, effect)
        if not identite.HasTrait("AERIAL"):
            effect.this.DealDamage([identite], 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, abattre),
    ]
