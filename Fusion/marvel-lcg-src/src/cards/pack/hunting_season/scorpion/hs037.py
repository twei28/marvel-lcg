from . import *

# hs037 Tail Armor
# Le Forced Interrupt (dégâts placés sur la Queue vont ici, 8 ou plus : défausse)
# est dans PlacerDegatsSurLaQueue (__init__), appelé par l'absorption de hs036.

def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        AttacherALaQueue(effect.this.CastTo(Attachment), effect)
    return [AbilityFactory.WhenThisRevealed(None, revelee)]
