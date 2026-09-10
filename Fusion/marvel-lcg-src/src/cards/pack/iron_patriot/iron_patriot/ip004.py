from . import *

# * Corrupt Absolutely — MANIGANCE-JOUEUR, cout 1, RES [mental], 3 menaces.
# Victory 0.
# Threat cannot be removed from this scheme by heroes or allies.
# While in the victory display, each REGISTERED character gets +1 THW.
# Alter-Ego Action: Exhaust a REGISTERED character you control -> remove 1
#   threat from here. Any player may trigger this ability.
#
# ⚠ LA JUMELLE EXACTE DE `ip003` Absolute Power, a trois mots pres :
#     ip003  [physical]  Action de HEROS      +1 ATQ
#     ip004  [mental]    Action d'ALTER EGO   +1 CTR
# Le reste est identique, verrou compris. Voir l'en-tete de `ip003` pour la
# lecture qui rend les deux compatibles (le personnage incline est le COUT, pas
# l'auteur du retrait).


def GetAbilities() -> Sequence['Ability']:

    def un_heros_ou_un_allie(face: 'CardFace') -> bool:
        return Hero.IsType(face) or AlterEgo.IsType(face) or Ally.IsType(face)

    def retirer_une_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(message)
        this.RemoveThreatFromSchemes([this], 1, effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            by_character=CardFinder(check_face_fn=un_heros_ou_un_allie),
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Unit2, trait=TRAIT_REGISTERED),
            works_in_the_victory_display=True,
            thwart=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            retirer_une_menace,
        ).SetCostFunc(CostFunc.Exhaust(CardFinder(trait=TRAIT_REGISTERED))),
    ]
