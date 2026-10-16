from . import *

# Personality Adjustment — OBLIGATION. Boost 2. Give to the Jenny player.
# You may flip to alter-ego form. Choose:
#  - Exhaust Jenny -> remove Personality Adjustment from the game.
#  - Place 3 threat on the main scheme. Discard this obligation.
#
# Carte de reference : `qsv/14024` Need for Speed — MEME squelette (« You may flip to
# alter-ego form. Choose: - Exhaust <alter-ego> -> remove from the game / - ... Discard this
# obligation ») : `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm` +
# `ChooseAbilities` avec `condition=player.IsAlterEgo()` sur l'option a cout.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau imprime dit « JENNIKA » : set du HEROS, module ici.
#
# ⚠ Mots-pieges :
#  - « You MAY flip » : facultatif (helper `YouMayFlip...`, pas `Flip...`) ;
#  - « Exhaust JENNY » : l'alter-ego, donc l'option n'existe qu'en forme alter-ego
#    (`condition=player.IsAlterEgo()`) ET si l'identite est redressee (le cout
#    d'inclinaison) ;
#  - « REMOVE ... FROM THE GAME » (pas defausse) : `Faces.RemoveAllFromGame` ;
#  - seconde option : 3 menaces sur le complot PRINCIPAL, PUIS defausse de l'obligation :
#    les deux phrases appartiennent a la meme branche.
#  - desc.GiveTo = « Jenny » (nom de l'alter-ego), pas « Jennika ».


def GetAbilities() -> Sequence['Ability']:

    def personality_adjustment(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def menace_et_defausse(targets: Sequence['CardFace']):
            this.PlaceThreatOnSchemes("MainScheme", 3, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Jenny → remove Personality Adjustment from the game",
                lambda targets:
                    Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Place 3 threat on the main scheme. Discard this obligation",
                menace_et_defausse,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            personality_adjustment
        )
    ]
