from . import *

# * U.S. Agent (face HEROS) — AVENGER. SOLDIER. PV 11, THW 2, ATK 2, DEF 2, main 6.
# Bolster — Response: After you defend, ready an upgrade you control.
#
# Cartes de reference :
#  - `mf006` Unstable Uniform (`AfterUnitDefendEnd(HeroResponse, "You", op)`) : le declencheur « After you defend ».
#  - `31022` Spider-Man (Otto) / `gs232` Her : « ready an upgrade you control » =
#    `.SetTarget(Upgrade, canbe_ready=True, from_where=["YouControlCards"])` + `Faces.ReadyAll(effect.targets, effect)`.
#  - `01019a` * She-Hulk : une Response imprimee sur la face HEROS s'ecrit `AbilityType.Response` (pas HeroResponse).
#
# ⚠ Mots-pieges : « Response » nu (optionnelle, imprimee sur la face HEROS) ; « After you DEFEND » (le heros a defendu,
# peu importe les degats) ; « AN upgrade you control » = une cible obligatoire, INCLINEE (`canbe_ready=True`) : sans
# amelioration inclinee la capacite n'est pas proposee.


def GetAbilities() -> Sequence['Ability']:

    def bolster(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.Response,
            "You",
            bolster,
        ).SetName("Bolster")
        .SetTarget(Upgrade, canbe_ready=True, from_where=["YouControlCards"]),
    ]
