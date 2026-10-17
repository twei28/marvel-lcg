from . import *

# Mission Training — AMELIORATION 1 [mental], aspect Justice (TMNT Reskins, Inkwire). TRAINING.
# Attach to a [[NINJA]] or [[MUTANIMAL]] ally. Max 1 [[TRAINING]] upgrade per ally.
# Attached ally gets +1 THW and +2 hit points.
#
# MODIFIEE par rapport a `34016` Mission Training (« Attach to an X-MEN ally ») : la cible change, le
# reste est identique. Pas d'`ability_link` (RECETTES §11 point 7) : script propre, copie de 34016 adaptee.
#
# CARTES DE REFERENCE
#  - `34016` Mission Training (officielle) : `CanPlayThisUpgradeCard(CardFinder2("X-MEN", Ally))` +
#    `GiveKeywordToAttached(Ally, thwart=1, health=2)`.
#  - `wx012` : filtre de cible libre par `CardFinder(card_type=..., check_effect_fn=...)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « a NINJA OR MUTANIMAL ally » : l'un des deux traits suffit ; un ALLIE (pas une identite).
#  ⚠ « Max 1 TRAINING upgrade per ally » : un allie qui porte deja une amelioration TRAINING (celle-ci ou
#    une autre, comme 34016) n'est pas une cible. ⚠ 34016 n'encode PAS cette clause (aucune condition dans
#    son module) : elle est codee ici, et seulement ici.
#  ⚠ « +1 THW and +2 hit points » : l'allie attache.


def CibleMissionTraining(effect: 'Effect', face: 'CardFace') -> bool:
    Unused(effect)
    if not (face.HasTrait("NINJA") or face.HasTrait("MUTANIMAL")):
        return False
    for attache in face.GetAttachedAttachments():
        if Upgrade.IsType(attache) and attache.HasTrait("TRAINING"):
            return False
    return True


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally, check_effect_fn=CibleMissionTraining),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            thwart=1,
            health=2,
        ),
    ]
