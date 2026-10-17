from . import *

# Kirby's Pencil (sj013), Kuji-Kiri, amelioration ARTIFACT, unique (Inkwire, TMNT Shinobi).
# Hero Action: Play a card from your hand, ignoring its resource cost. Discard cards from the top of the
# encounter deck equal to that card's printed resource cost. Then, remove this card from the game.
#
# Carte de reference (texte quasi identique) : `scw/15003` Chaos Magic (« Play a card from your hand, ignoring
# its resource cost. Discard cards from the top of the encounter deck equal to that card's printed resource
# cost » : `PlayCardsLikeInTurn(..., ignore_resources_cost=True, after_play=...)` +
# `Worlds.DiscardEncounterCards(FacesCounter.GetPrintedResourceCost([face]), effect)`) ;
# `mut_gen/32179` (« Remove this card from the game » apres l'effet : `Faces.RemoveAllFromGame`).
#
# TEXTE CONTRE CODE
#  ⚠ « Play a card FROM YOUR HAND » : cible choisie dans la main, jouable (`canbe_play`) ; « ignoring its
#    resource cost » : aucune ressource depensee.
#  ⚠ « equal to that card's PRINTED resource cost » : le cout IMPRIME (pas le cout modifie), compte apres que
#    la carte a ete jouee.
#  ⚠ « THEN remove THIS card from the game » : l'amelioration quitte le jeu (pas la defausse) apres tout le
#    reste ; une seule utilisation.
#  ⚠ Amelioration sans « Attach to » : posee sur sa propre identite (`CanPlayThisUpgradeCard()`).


def GetAbilities() -> Sequence['Ability']:

    def kirbys_pencil(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.PlayCardsLikeInTurn(
            effect.targets, effect, ignore_resources_cost=True,
            after_play=lambda face:
                Worlds.DiscardEncounterCards(FacesCounter.GetPrintedResourceCost([face]), effect)
        )
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kirbys_pencil,
        ).SetLabel()
        .SetTarget(canbe_play=True, from_where=["YourHandCards"]),
    ]
