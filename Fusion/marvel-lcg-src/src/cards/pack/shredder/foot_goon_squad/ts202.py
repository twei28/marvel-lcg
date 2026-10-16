from . import *

# * Bludgeon — SBIRE UNIQUE (Foot Goon Squad). BRUTE. FOOT CLAN. SHARK.
# MNG 2 / ATQ 2 / PV 3, 1 icone de boost + etoile. Quickstrike.
# Forced Response: After Bludgeon attacks and damages a character, exhaust that character.
# [star] Boost: Exhaust your hero.
#
# Cartes de reference : `gob 02038` Scorpion / `mts 21086` Supergiant
# (`AfterUnitAttackAndDamageUnit(ForcedResponse, "This", "Character", op,
# target_in_play=True)`) ; `core klaw 01123` Sonic Boom (boost « exhaust your
# hero » : `player.IsHero()` puis `Faces.ExhaustAll`).
#
# Mots-pieges : « attacks AND DAMAGES » (pas une attaque absorbee par Toughness) ;
# « that character » = le blesse (identite ou allie) ; « your HERO » (rien en
# alter-ego).


def GetAbilities() -> Sequence['Ability']:

    def blesse(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.ExhaustAll([message.attacked], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None and joueur.IsHero():
            Faces.ExhaustAll([joueur.GetHero()], effect)

    return [
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse, "This", "Character", blesse, target_in_play=True,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
