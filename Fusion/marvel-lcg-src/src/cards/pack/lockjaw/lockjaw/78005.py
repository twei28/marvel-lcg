from . import *

# * Kamala's Room — custom « Nugget »
# Your alter-ego gets +1 REC.
# Alter-Ego Action: Exhaust Kamala's Room → look at the top 3 cards of your
#   deck. Add 1 to your hand and discard the others.
#
# CORRECTIF. L'action ne se resolvait jamais : elle appelait
#     initiator.LookAtDeck("PlayerDeck", 3, effect, gain=1, discard_other=True)
# avec DEUX erreurs sur la meme ligne. `LookAtDeck` n'accepte ni `gain` ni
# `discard_other` — sa signature s'arrete a (deck, num, by_effect, *, from_top) —
# et "PlayerDeck" n'est pas une valeur reconnue : seul "EncounterDeck" est
# converti, tout autre texte finit en appel de methode sur une chaine.
#
# La reecriture suit le texte imprime etape par etape. Le dessus du deck est
# releve AVANT la recherche : celle-ci peut remanier le deck, et il faut savoir
# quelles cartes defausser ensuite.


def GetAbilities() -> Sequence['Ability']:

    def fouiller(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()

        dessus = list(initiator.player_deck.Get(True))[:3]
        if not dessus:
            return

        Faces.LookAt(dessus, initiator, effect)

        gardee = Search.PlayerDeckTop(effect, initiator, 3)
        if gardee is None:
            return
        initiator.GainCard(gardee, effect)

        autres = [face for face in dessus if face is not gardee]
        if autres:
            Faces.DiscardAll(autres, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            fouiller,
        ).SetName("Kamala's Room")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
