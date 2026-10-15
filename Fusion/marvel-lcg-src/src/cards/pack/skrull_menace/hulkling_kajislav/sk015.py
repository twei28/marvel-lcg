from . import *

# * Lauri-Ell — allie d'aspect PROTECTION (n° 15). KREE. SOLDIER.
# Cout 4 [physical]. THW 0* / ATK 3* (1 degat consecutif chacun), 3 PV.
# Response: After Lauri-Ell takes any amount of damage from an attack, give her
#   a tough status card.
#
# Cartes de reference :
#  - **`27080`** Lashing Out (via `AfterVenomTakesAttackDamageRemoveEqualThreat`,
#    sm/venom/__init__.py) : « After Venom takes any amount of damage from an
#    attack » = `AfterUnitTookDamage(Response, <qui>, op, is_from_attack=True)`.
#  - `13033` Perseverance pour `Faces.GiveStatus([...], "Tough", effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **from an attack** » : `is_from_attack=True`. Les degats CONSECUTIFS
#    de sa propre attaque ne sont pas « from an attack » contre elle.
#  - « any amount » : 1 degat suffit ; 0 (tout prevenu) ne declenche rien.
#  - « give **her** » : Lauri-Ell, pas l'identite. Si elle meurt de cette
#    attaque, la reponse n'a plus de cible : rien.
#  - Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def soldat(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        if this.IsInPlay():
            Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "This",
            soldat,
            is_from_attack=True,
        ),
    ]
