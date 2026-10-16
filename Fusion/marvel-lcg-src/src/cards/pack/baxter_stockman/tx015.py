from . import *

# Roadkill Rodneys — SBIRE (High Speed 1/5, x3). ROBOT. SWARM. SCH 1, ATK 1, PV 3, 2 boosts.
# Enters play with 1 cable counter on them.
# Quickstrike.
# [star] This minion gets +1 ATK for each cable counter here.
# [star] Forced Response: After this minion attacks and damages a character, daze that character and
#   remove each cable counter from here.
#
# Cartes de reference : `ThisGainKeyword(fn, attack=1, change_on_event=OnEvent.Counter(...))` (tx013,
# td016) pour « +1 ATK par compteur » ; `wd005` / `dz020` Klaw (`AfterUnitAttackAndDamageUnit(
# ForcedResponse, "This", "Character", op, target_in_play=True)`) ; `Faces.RemoveCountersOn(..., "All", ...)`.
# Quickstrike : natif (`desc.Quickstrike`). Compteur maison `cable`.
#
# Mots-pieges : « +1 ATK FOR EACH cable counter » s'AJOUTE a l'ATQ imprimee 1 ; « attacks AND damages » (un
# coup entierement prevenu ne declenche rien) ; « daze THAT character » (le personnage touche) ; « EACH cable
# counter » : tous, pas un seul.


def GetAbilities() -> Sequence['Ability']:

    def jauge(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
        return effect.this.CastTo(Minion).GetCounters("cable")

    def hebeter_et_defausser_les_cables(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Faces.GiveStatus([message.attacked], "Dazed", effect)
        Faces.RemoveCountersOn([this], "All", "cable", effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(1, "cable"),
        AbilityFactory.ThisGainKeyword(
            jauge,
            attack=1,
            change_on_event=OnEvent.Counter("This", "cable"),
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            hebeter_et_defausser_les_cables,
            target_in_play=True,
        ),
    ]
