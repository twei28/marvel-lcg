from . import *

# hs202 * Lizard (allie, recompense du scenario 3)
# +3 THW tant que tu es en alter-ego, +3 ATK tant que tu es en heros.

def _forme(heros: bool):
    def compter(effect: 'Effect', ui: 'List[CardFace]') -> int:
        joueur = effect.this.GetControlBy()
        if not Player.IsType(joueur):
            return 0
        identite = joueur.GetIdentity()
        if identite is None:
            return 0
        return 1 if Hero.IsType(identite) == heros else 0
    return compter


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.ThisGainKeyword(_forme(False), thwart=3, change_on_event=OnEvent.Form(Identity)),
        AbilityFactory.ThisGainKeyword(_forme(True), attack=3, change_on_event=OnEvent.Form(Identity)),
    ]
