from . import *

# * C.L.O.C. (Centrally Located Organic Computer) : ALLIE, cout 2, [energy]. ANDROID. AVENGER. THW 2☆ / ATQ 1☆, PV 3.
# Response: When C.L.O.C. enters play, you may remove 1 balance counter from play.
#
# CARTES DE REFERENCE
#  - « When X enters play » en Reponse : `AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", op)` (forme de `counter.py::ThisEnterPlayWithCounters`).
#  - « remove a balance counter from play » : helper `RetirerEquilibre` (Duality Aspect d'abord, puis The Watchtower).
#  - ☆ sous THW/ATQ (dégâts consécutifs) : lu dans `desc` (`"2*"`, `"1*"`), aucun code (fiche `consequential.md`).
#
# TEXTE CONTRE CODE
#  « you MAY » : Reponse facultative. « 1 balance counter FROM PLAY » : n'importe quelle carte en jeu (pas seulement Duality Aspect) ; sans compteur la Reponse est sans effet.
#  Chiffres : cout 2, THW 2, ATQ 1, PV 3.


def GetAbilities() -> Sequence['Ability']:

    def retirer_un(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        RetirerEquilibre(effect, 1)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            retirer_un,
        ),
    ]
