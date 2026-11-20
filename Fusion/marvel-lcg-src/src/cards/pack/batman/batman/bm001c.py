from . import *
# * Batman (version « Lantern ») — HEROS. « FEAR ME!!! » — Hero Response : after Batman attacks or thwarts, choose a deterrence
# card and shuffle it into the encounter deck. Regle imprimee : 3 melanges par round au plus (MelangerUneDissuasion).
# Carte de reference : 01028 Superhuman Strength (reponse a une attaque de l'identite), bm001b (le deck de dissuasion).
def GetAbilities() -> Sequence['Ability']:
    def dark_knight(effect: 'Effect', message: 'Message2') -> None:
        MelangerUneDissuasion(effect)
    return [
        AbilityFactory.AfterUnitAttackEnd(AbilityType.HeroResponse, "You", dark_knight).SetName("FEAR ME!!!"),
        AbilityFactory.AfterUnitThwartEnd(AbilityType.HeroResponse, "You", dark_knight).SetName("FEAR ME!!!"),
    ]
