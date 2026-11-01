from . import *

# Matter Manipulation (x3 : hf346, hf347, hf348). Traitrise PSIONIC SKILL, Boost 2. « When Revealed : Discard a card you control, then search your deck and discard
# pile for a card of the same type but with a resource cost less than the resource cost of the discarded card, and put that card into play. Otherwise, this card
# gains surge. »
# Cartes de reference : 40160 (`ThisCardGainSurge`), `Search.PlayerCard(... include_player_deck / include_discard_pile, finder)` + `face.PutIntoPlay(joueur, effect)`
# (jubilee 47003), `CardFinder(cost_less_than=...)` (checker.py : borne INCLUSIVE, d'ou `cout - 1`), `joueur.AskChooseFace`.
# ⚠ « same type » : Ally / Support / Upgrade (les seules cartes joueur en jeu qui ont un cout) ; « resource cost » = cout IMPRIME ; « less than » STRICT ;
# « Otherwise » : si rien n'est mis en jeu (aucune carte controlee, cout 0, aucune carte plus petite), la carte gagne surge (la defausse, elle, a eu lieu).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        controlees = [f for f in joueur.GetControlCards() if Ally.IsType(f) or Support.IsType(f) or Upgrade.IsType(f)]
        mise_en_jeu = None
        if controlees:
            choisie = controlees[0] if len(controlees) == 1 else joueur.AskChooseFace(controlees, effect, not_move=True)
            if choisie is not None:
                type_ = Ally if Ally.IsType(choisie) else (Support if Support.IsType(choisie) else Upgrade)
                cout = choisie.printed_cost.val
                Faces.DiscardAll([choisie], effect)
                if cout >= 1:
                    mise_en_jeu = Search.PlayerCard(effect, joueur, include_player_deck=True, include_discard_pile=True,
                                                    card_type=type_, cost_less_than=cout - 1)
                    if mise_en_jeu is not None:
                        mise_en_jeu.PutIntoPlay(joueur, effect)
        if mise_en_jeu is None:
            ThisCardGainSurge(effect, message)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
