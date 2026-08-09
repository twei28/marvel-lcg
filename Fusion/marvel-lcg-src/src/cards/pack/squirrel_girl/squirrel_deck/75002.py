from . import *

# Tippy-Toe
# Response: After Tippy-Toe enters play, look at the top 2 cards of the
#   Squirrel deck. Return them in any order.

def GetAbilities() -> Sequence['Ability']:

    def reordonner(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        if joueur is None:
            return

        deux = list(joueur.additional_deck.Get())[-2:]
        if len(deux) < 2:
            return

        joueur.LookAtDeck(joueur.additional_deck, 2, effect)

        # A deux cartes, « remettre dans l'ordre voulu » se resume a choisir
        # celle qui reste sur le dessus.
        #
        # CORRECTIF : passer par une capacite de choix avec
        # `SetTarget(Select.From(faces=...))` ne restreignait RIEN sur des
        # cartes hors jeu — le pilote a choisi Rhino et l'a deplace. Les faces
        # d'un deck se designent avec MayChooseFace, qui prend la liste telle
        # quelle.
        choisi = joueur.MayChooseFace(deux, effect, not_move=True)
        if choisi is not None:
            Faces.MoveAllToDeck([choisi], joueur.additional_deck, "Top", effect)

    return [
        *Ecureuil(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            reordonner,
            conditions=[PasDeDiscorde],
        ),
    ]
