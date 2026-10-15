from . import *

# * Teddy Altman — face ALTER-EGO. PV 13, REC 4, main 6. HYBRID.
# Kree/Skrull Hybrid — Setup: Put your origin form upgrade into play, Skrull
#   Origin side faceup.
# Response: After you change origin form, heal 1 damage from Teddy Altman.
#
# Cartes de reference :
#  - **`as001b`** * Peter Parker (Earth-31198) : « Setup: Put your Spider
#    Armor upgrade into play, [[OPERATIONAL]] side faceup. » Meme phrase :
#    `SetupPutIntoPlay(["as002a,as002b"], flip_to_trait=...)`. Ici la face
#    se designe par son NOM (les deux faces d'origine n'ont aucun trait
#    propre), donc `flip_to_name=`, comme `26001b` * Vision.
#  - **`26007`** Density Control : `AfterUnitChangeForm(..., "You", op,
#    is_change_additional_form=True)`, « after you change [additional] form ».
#  - `47012` / `ab012` pour `this.HealthUnits([this], 1, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « After you change **origin** form » : SEULEMENT le retournement de
#    l'upgrade d'origine (sk002a/b), pas le passage heros <-> civil. C'est ce
#    que filtre `is_change_additional_form=True` (message.to_additional_form
#    non vide), et sk002a/b passent bien par `ChangeAdditionalFrom`.
#  - La Response est imprimee sur la face CIVILE : elle n'existe qu'en forme
#    alter-ego. En forme heros, retourner l'origine ne soigne rien.
#  - « heal 1 damage from **Teddy Altman** » : l'identite elle-meme.
#  - « Skrull Origin side **faceup** » : `flip_to_name="Skrull Origin"`,
#    redondant aujourd'hui (sk002a EST la face Skrull) mais ecrit quand meme,
#    comme as001b : c'est le texte imprime.
#  - Pas de limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def hybride(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(message)

        this.HealthUnits([this], 1, effect)

    return [
        AbilityFactory.SetupPutIntoPlay(
            ["sk002a,sk002b"],
            flip_to_name="Skrull Origin",
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            hybride,
            is_change_additional_form=True,
        ),
    ]
