from . import *

# Yi (sj017), Kuji-Kiri, allie MYSTIC NINJA TURTLE, unique (Inkwire, TMNT Shinobi).
# [star] Response: After Yi uses a basic power, choose a SPELL or TECH card in your discard pile and put it on
# the top of your deck.
#
# Cartes de reference : `aos/50023` Melinda May (« [star] Response: After X uses a basic power » :
# `AfterUnitUseBasicPower(AbilityType.Response, "This", ...)`) ; `leonardo/tl002` Splinter et `gmw/16033`
# Salvage (« choose a ... card in your discard pile and put it on top of your deck » :
# `SetTarget(..., from_where=["YourDiscardPile"])` + `Faces.MoveAllToDeck(cartes, player_deck, "Top")`).
# Stats : THW « 1* » / ATK « 1* » = 1 degat consequentiel apres chacune (une etoile, comme tous les allies TMNT
# de l'auteur : `ub022`, `uj039`...) ; le [star] devant Response est l'icone etoile des regles (aucun code).
#
# TEXTE CONTRE CODE
#  ⚠ « After Yi uses A BASIC POWER » : ATQ, CTR, DEF ou REC (`AfterUnitUseBasicPower`, comme Melinda May) ;
#    seulement Yi.
#  ⚠ « a SPELL OR TECH card » : une carte portant SPELL ou TECH (OU : `traits=[...]`), dans VOTRE defausse ;
#    « put it on the TOP of your deck » : dessus du deck, sans melanger.
#  ⚠ Ressource imprimee : etoile verte = [wild] (`RES: G`).


def GetAbilities() -> Sequence['Ability']:

    def yi(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        Faces.MoveAllToDeck(list(effect.targets), joueur.player_deck, "Top", effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            yi,
        ).SetTarget(traits=["SPELL", "TECH"], from_where=["YourDiscardPile"]),
    ]
