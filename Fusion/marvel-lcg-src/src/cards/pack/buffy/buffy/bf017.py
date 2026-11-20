from . import *

# * Angel — ALLIE (CHAMPION. VAMPIRE), cout 4, [wild]. THW 2*, ATQ 2*, PV 3. Unique. Linked (Angelus).
# [star] Angel's attacks gain piercing.
# Response: After you change to alter-ego form, heal 1 damage from Angel.
#
# CARTES DE REFERENCE
#  - `04012` Black Knight : `UnitAttackGainKeyword("This", piercing=True)` (sans `is_basic_attack` : le texte dit « attacks », pas « basic attacks »).
#  - `01019a`, `12001a`, `bt001b` : `AfterUnitChangeForm(type, "You", op, to_form=..)` pour « after you change to X form ».
#  - `desc.Linked = "Angelus"` : nom distinct de toute carte livree (fiche `mots-cles/linked.md`) ; Angelus n'est pas fourni.
#
# TEXTE CONTRE CODE
#  « After YOU change to alter-ego form » -> le JOUEUR d'Angel (`"You"`), vers l'alter-ego (`to_form=AlterEgo`), pas vers le heros. « heal 1 damage from Angel » -> Angel.


def GetAbilities() -> Sequence['Ability']:

    def angel(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.HealthUnits([this], 1, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            angel,
            to_form=AlterEgo,
        ),
    ]
