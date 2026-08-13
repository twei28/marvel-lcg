from . import *

# * Dagger

def GetAbilities() -> Sequence['Ability']:

    # « attachee a l'allie Cloak » : Cloak pose ses cartes SOUS lui (TuckCardUnderHere),
    # elles sont donc dans sa zone de placement. C'est la seule facon pour une
    # carte encore injouee d'etre « attachee » a un allie.
    def check_attached_to_cloak(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        this = effect.this
        for cloak in Worlds.FindCardsOnField(effect, finder=CardFinder(name="* Cloak")):
            if this in cloak.GetPlacedCardArea().Get():
                return True
        return False

    return [
        Fragile(),
        AbilityFactory.ReduceCostToPlayThis(
            2,
            conditions=[check_attached_to_cloak]
        ),
    ]
