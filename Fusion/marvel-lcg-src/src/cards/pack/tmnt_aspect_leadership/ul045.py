from . import *

# * Zato-Ino — ALLIE Leadership (TMNT Aspects, Inkwire), cout 3, [energy]. MASSEUSE. PIG. SWORDSMAN.
# THW 1* / ATQ 1[star]* / PV 2.
# [star] Response: After Zato-Ino attacks and damages an enemy, daze that enemy.
#
# MOT-CLE (fiche lue AVANT le code) : Daze — docs/reference/mots-cles/daze.md : poser une carte d'etat
#   Dazed (`Faces.GiveStatus(..., "Dazed", ...)`) ; une seule par personnage (GainStatus refuse la 2e).
#
# CARTES DE REFERENCE
#  - `01118` Sonic Converter : « After X attacks AND DAMAGES a character » =
#    `AfterUnitAttackAndDamageUnit(<type>, X, <cible>, op, target_in_play=True)` ; la cible = `message.attacked`.
#  - `ta002` Nobody : « daze that enemy ».
#
# TEXTE CONTRE CODE
#  ⚠ « attacks AND DAMAGES » : une attaque entierement absorbee (Tenace, Cloaked) ne declenche rien.
#  ⚠ « an ENEMY » : vilain ou sbire ; « THAT enemy » : celui qui a subi les degats, s'il est encore en jeu.
#  ⚠ Response facultative ; le [star] n'est qu'un rappel. Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def zato_ino(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        Faces.GiveStatus([message.attacked], "Dazed", effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.Response,
            "This",
            Enemy,
            zato_ino,
            target_in_play=True,
        ),
    ]
