from . import *

# hs133 Quicksand
# ATK/THW/DEF -1 (donnees de la carte). When Revealed : epuiser son identite ou attacher.
# Interrupt : quand vous jouez un evenement, annulez ses effets et defaussez-le → defaussez Quicksand.

def GetAbilities() -> Sequence['Ability']:

    def engloutir(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> None:
        message.CancelEffects(effect, discard_it=True)
        Faces.DiscardAll([effect.this], effect)

    def joueur_porteur(effect: 'Effect', message: 'Message.WhenPlayerWouldPlayCard') -> bool:
        return JoueurDuPorteur(effect) is message.to_player

    return [
        PiegeAttachement(),
        AbilityFactory.WhenPlayerWouldPlayCard(AbilityType.HeroInterrupt, "AnyPlayer", Event, engloutir, conditions=[joueur_porteur]),
    ]
