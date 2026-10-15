from . import *

# * Xavin — ALLIEE de campagne (Protection / Campaign, n° 269). Cout 3. THW 2** / ATK 3**, 5 PV.
# RUNAWAYS. SKRULL.
# Interrupt: When Xavin enters play, discard cards from your deck until you discard an event with a
#   "Hero Action" ability. You may resolve that event's "Hero Action" ability.
#
# Cartes de reference :
#  - **`AbilityFactory.WhenCardEnterPlay`** (card_move.py:92) : « WHEN X enters play » = Interruption, avant l'entree.
#  - **`player.DiscardDeckUntil`** (player_action.py:1628) : « discard cards from your deck until you discard
#    a X » ; le filtre `with_texts=["Hero Action"]` du CardFinder reconnait une carte qui porte une
#    capacite « Hero Action ».
#  - **`dz035`** Karaoke Night : « resolve the Hero Action of that card » = `Faces.ResolveAbility([carte],
#    joueur, AbilityType.HeroAction, effect, ref)` avec `ref = Message.WhenPlayerInTurn(joueur, effect)`
#    (sans message de reference : AssertionError, effect_invoke.py:197).
#
# ⚠ Mots-pieges : « an EVENT with a Hero Action ability » (l'evenement DOIT porter une « Hero Action » ; les
# autres cartes defaussees restent defaussees) ; « YOUR deck » ; « You MAY resolve » : choix optionnel, la
# carte reste en defausse ; deck epuise sans evenement : rien a resoudre.


def GetAbilities() -> Sequence['Ability']:

    def xavin(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()

        evenement = joueur.DiscardDeckUntil(effect, card_type=Event, with_texts=["Hero Action"])
        if evenement is None:
            return

        def resoudre(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            ref = Message.WhenPlayerInTurn(joueur, effect)
            Faces.ResolveAbility([evenement], joueur, AbilityType.HeroAction, effect, ref)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Resolve that event's \"Hero Action\" ability",
                resoudre,
            ),
        )

    return [
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Interrupt,
            "This",
            xavin,
        ),
    ]
