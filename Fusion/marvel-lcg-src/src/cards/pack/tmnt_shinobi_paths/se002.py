from . import *

# Onmyōdō — PATH (la Voie de l'Onmyōdō), classe Kuji-Kiri (Inkwire, TMNT Shinobi). KUJI-KIRI.
# Permanent. You get -1 hand size.
# You gain the MYSTIC trait.
# Insight — Hero Action: Exhaust this card -> look at the top 2 cards of any deck and put them back in the
#   same order.
#
# Mots-cles (fiches lues AVANT le code) : Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « -1 hand size » : `sentinel/st005b` (`GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1)`) ;
#  - « gain the X trait » : `hunting_season/hs092` (`GiveKeywordToInPlayWhenApplyThis("You", trait=...)`) ;
#  - « look at the top N cards of any deck » : `gwenpool/gp008` Comicbook Panels (`_bulle_look_top` :
#    `joueur.LookAtDeck(deck, n, effect)` pour chaque deck propose, `ChooseAbilities`) ;
#  - ici 2 cartes et on propose AUSSI les decks des autres joueurs (« ANY deck »).
#
# TEXTE CONTRE CODE
#  ⚠ « YOU gain the MYSTIC trait » : l'identite, les deux formes ("You") ; difference de formulation avec
#    Kagemusha (« Your hero gains ») conservee.
#  ⚠ « the top 2 cards of ANY deck » : le deck du joueur, celui de chaque autre joueur, le deck rencontre ;
#    UN seul deck choisi.
#  ⚠ « put them back in the SAME ORDER » : regarder ne deplace rien (`LookAtDeck` ne retire pas les
#    cartes) : l'ordre est donc conserve par construction, aucune re-pose, contrairement a « in any order ».
#  ⚠ « Hero Action » : forme heros ; cout « Exhaust this card ».


def GetAbilities() -> Sequence['Ability']:

    def insight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def regarder(deck: Any):
            def action(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                joueur.LookAtDeck(deck, 2, effect)
            return action

        options = [AbilityFactory.ForChoiceAbility("Look at the top 2 cards of your deck", regarder(joueur.player_deck))]
        for autre in effect.world.const_players:
            if autre is not joueur and not autre.is_eliminated:
                options.append(AbilityFactory.ForChoiceAbility(
                    f"Look at the top 2 cards of {autre.name}'s deck", regarder(autre.player_deck)))
        options.append(AbilityFactory.ForChoiceAbility(
            "Look at the top 2 cards of the encounter deck", regarder("EncounterDeck")))
        joueur.ChooseAbilities(effect, *options)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1, trait="MYSTIC"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            insight,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
