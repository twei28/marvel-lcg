from . import *

# Rage of Retribution — Amelioration, cout 2, ressource [physical]. CONDITION.
# Silver Surfer gains retaliate 1.
# Interrupt: When Silver Surfer would change form, discard Rage of Retribution -> ready Silver Surfer instead.
#
# Cartes de reference :
#  - `ar001b` / `45030b` : `WhenUnitWouldChangeForm(Interrupt, "You", op)` (fenetre « would change form »).
#  - `aa010`, `ag012` : `message.SetBeInstead(effect)` pour « ... instead ».
#  - `14001a` / `tg001a` : `.SetTarget("YourHero")` + `Faces.ReadyAll(effect.targets)`.
#  - `RECETTES-MOTEUR` §3 : `*GiveKeywordToInPlayWhenApplyThis("YourHero", retaliate=1)` (« Your hero gains »,
#    forme heros seulement, PAS `"You"`).
#
# ⚠ Mots-pieges :
#  - « Silver Surfer gains retaliate 1 » : un NOM PROPRE, donc la face HEROS seulement (pas Norrin Radd).
#  - « would change form » : on part de la face HEROS (from_form=Hero).
#  - « discard Rage of Retribution -> » : la defausse est un COUT ; sans elle, rien n'est remplace.
#  - « ready Silver Surfer INSTEAD » : le changement de forme n'a PAS lieu, il est remplace par le redressement.


def GetAbilities() -> Sequence['Ability']:

    def remplacer(effect: 'Effect', message: 'Message.WhenUnitWouldChangeForm') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.SetBeInstead(effect)
        Faces.ReadyAll(effect.targets, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "YourHero",
            retaliate=1,
        ),
        AbilityFactory.WhenUnitWouldChangeForm(
            AbilityType.Interrupt,
            "You",
            remplacer,
            from_form=Hero,
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("YourHero"),
    ]
