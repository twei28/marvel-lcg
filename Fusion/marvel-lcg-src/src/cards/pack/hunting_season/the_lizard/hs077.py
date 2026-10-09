from . import *

# The Chameleon

def GetAbilities() -> Sequence['Ability']:

    def valeur_du_vilain(champ: str):
        def calcul(effect: 'Effect', faces) -> int:
            v = Vilain(effect)
            return getattr(v, champ) if v is not None else 0
        return calcul

    return [
        AbilityFactory.ThisGainKeyword(valeur_du_vilain("attack"), attack=1),
        AbilityFactory.ThisGainKeyword(valeur_du_vilain("scheme"), scheme=1),
    ]
