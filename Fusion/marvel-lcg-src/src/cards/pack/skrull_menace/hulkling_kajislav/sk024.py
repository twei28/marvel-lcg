from . import *

# Drunk in Love — evenement d'aspect BASIC (n° 24). Cout 1 [mental].
# Action: Confuse your identity → heal 4 damage from it.
#
# Cartes de reference :
#  - **`32008`** Steel Fist pour `Faces.GiveStatus(cibles, "Confused", effect)`,
#    et `SetTarget(..., canbe_status=[...])` qui ne retient que les cibles
#    capables de recevoir le statut.
#  - `47012` / `ab012` pour `HealthUnits(...)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Confuse your identity **→** » : un COUT. Une identite deja desorientee
#    (ou incapable de l'etre, Stalwart) ne peut pas payer : la carte n'est pas
#    jouable. D'ou la cible `"YourIdentity"` filtree par
#    `canbe_status=["Confused"]` ; le statut puis le soin tombent ensuite dans
#    l'ordre imprime.
#  - « heal 4 damage from **it** » : de l'identite, celle qu'on vient de
#    desorienter.
#  - « Action » nue : jouable dans les deux formes (une identite civile peut
#    etre desorientee : elle ne pourra plus contrer... en civil, sans effet).


def GetAbilities() -> Sequence['Ability']:

    def ivre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        cibles = list(effect.targets)
        Faces.GiveStatus(cibles, "Confused", effect)
        this.HealthUnits(cibles, 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            ivre,
        ).SetPlay().SetLabel()
        .SetTarget("YourIdentity", canbe_status=["Confused"]),
    ]
