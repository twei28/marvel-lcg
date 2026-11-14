from . import *

# Avatar of Oblivion — ATTACHEMENT NEMESIS de Quasar (QUASAR NEMESIS 3/5, numero
# imprime 237, en collision avec Touched de Binary : suffixe q). TITLE.
# +1 ATK (encadre imprime : desc « ATK+ », base automatique, has_modify.py).
# Aucune icone de boost imprimee.
# Attach to the minion with the highest ATK. If you cannot, this card gains surge.
# Attached minion gains the ELITE trait.
# Forced Interrupt: When attached minion would be defeated, heal all damage from
#   it instead, then discard this card.
#
# Cartes de reference :
#  - **`16131`** Kree Combat Armor / `19028` : `AttachToFaceWhenPutIntoPlay(
#    <type>, highest_atk=True)` ; `if_cannot_gain_surge=True` pour « If you
#    cannot, this card gains surge » (attachment.py).
#  - **`01185`** Biomechanical Upgrades : MEME Interruption forcee, mot pour mot
#    (« When attached minion would be defeated, heal all damage from it instead,
#    then discard this card ») : `WhenUnitWouldBeDefeated(ForcedInterrupt,
#    "AttachedMinion", op)` + `SetBeInstead` + `HealthUnits("All")` + defausse.
#  - **`sk064`** / `sk287` : « gains the X trait » =
#    `*GiveKeywordToAttached("Character", trait=...)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « the MINION with the highest ATK » : un SBIRE (pas le vilain) ; aucun
#    sbire en jeu -> Renfort.
#  - « +1 ATK » : desc « ATK+ » (01100 Enhanced Ivory Horn), lu par le moteur.
#  - « INSTEAD » : la defaite n'a pas lieu ; le sbire reste en jeu, soigne de
#    TOUT, et c'est l'attachement qui part (une seule fois).
#  - « gains the [[ELITE]] trait » : tant que l'attachement est en place.


def GetAbilities() -> Sequence['Ability']:

    def avatar(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Attachment)

        message.SetBeInstead(effect)
        this.HealthUnits([message.trigger], "All", effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Minion,
            highest_atk=True,
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            trait="ELITE",
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "AttachedMinion",
            avatar,
        ),
    ]
