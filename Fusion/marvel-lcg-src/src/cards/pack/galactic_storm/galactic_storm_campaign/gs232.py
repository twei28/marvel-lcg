from . import *

# * Her — ALLIE de campagne (Identity-Specific / Campaign, n° 232). Cout 3. THW 2 / ATK 2, 3 PV. AERIAL.
# Honorary.
# [star] Response: After Her enters play, ready an upgrade you control.
#
# Cartes de reference :
#  - **`skrull_menace/skrull_menace_campagne/sk263`** Crusader : `AbilityFactory.AfterCardEnterPlay(
#    Response, "This", ...)` pour « After X enters play ».
#  - **`psylocke/psylocke/41011`** Weapons Training : `.SetTarget(Upgrade, canbe_ready=True, range=...,
#    from_where=["YouControlCards"])` + `Faces.ReadyAll(effect.targets, effect)` pour « ready a[n]
#    <type> you control ».
#
# ⚠ Mots-pieges :
#  - « [star] » devant Response : footnote pure (convention GS-0 Q6, deja actee), aucun effet de jeu ;
#  - « an UPGRADE you control » : type Upgrade uniquement, pas n'importe quelle carte.
# ⚠ Étape 8 bis (ce que la carte DESSINE) : redresser une carte change son etat visible (inclinee ->
#   prete) : cas plateau a prevoir.


def GetAbilities() -> Sequence['Ability']:

    def her(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            her,
        ).SetTarget(Upgrade, canbe_ready=True, from_where=["YouControlCards"]),
    ]
