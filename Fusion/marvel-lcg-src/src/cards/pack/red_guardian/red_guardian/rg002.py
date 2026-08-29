from . import *

# * Black Widow
# Response: After Black Widow enters play, stun the enemy with Red Guardian's
#   Shield attached.
#
# Aucune cible n'est CHOISIE : le texte designe l'ennemi porteur du bouclier.
# On le retrouve donc par `CibleDuBouclier` plutot que par `SetTarget`.
# Modele du declencheur : Spider-Woman (01011).
#
# Le bouclier peut etre plante sur une MANIGANCE : dans ce cas il n'y a pas
# d'ennemi a etourdir et la reaction ne fait rien. D'ou le test `Enemy.IsType`.


def GetAbilities() -> Sequence['Ability']:

    def black_widow(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        cible = CibleDuBouclier(effect)
        if cible is None or not Enemy.IsType(cible):
            return

        Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            black_widow,
        ),
    ]
