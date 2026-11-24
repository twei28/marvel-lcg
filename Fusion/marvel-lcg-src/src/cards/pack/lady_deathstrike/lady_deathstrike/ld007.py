from . import *

# Reaver Commander — ATTACHEMENT, TITLE. Boost : etoile seule (« [star] Boost: Reveal this card »).
# Attach to Lady Deathstrike. Lady Deathstrike gains steady.
# Forced Response: After an ally is defeated by a REAVER, place 1 threat on the main scheme.
# Hero Action: Spend [mental][mental] resources → discard this card.
# [star] Boost: Reveal this card.
#
# Cartes de reference :
#  - « Boost: Reveal this card » : `WhenCardBecomeBoost("This", RevealThisCard)` (`04084` Ball and Chain) ;
#  - `steady` : `*GiveKeywordToAttached(Enemy, steady=1)` (fiche mots-cles/steady.md) ;
#  - « Spend ... → discard this card » : `PlayerActionToDiscardThis(HeroAction).SetCost(Cost("BB"))` (`40090`, `02019`) ;
#  - « after an ally is defeated by X » : `AfterUnitDefeatedUnit(type, <tueur>, Ally, op)` (`defeated.py`).
#
# ⚠ Mots-pieges :
#  - « defeated BY a REAVER » : le tueur est un ennemi REAVER (pas n'importe quelle cause de defaite) ;
#  - « place 1 threat on THE MAIN scheme » : le complot principal (`ld004b`), pas une manigance annexe ;
#  - [mental][mental] = DEUX icones noeuds bleus (verifie contre les icones mentales du pack Shang-Chi) : `Cost("BB")` ;
#  - le Boost est une ETOILE seule : aucune icone numerique (`desc.Boost` absent).


def GetAbilities() -> Sequence['Ability']:

    def menace(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)

        this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=IDS_VILAIN)),
        *AbilityFactory.GiveKeywordToAttached(Enemy, steady=1),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.ForcedResponse,
            CardFinder(trait="REAVER", card_type=Enemy),
            Ally,
            menace,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("BB")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
