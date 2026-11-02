from . import *

# Illusory Duty (traitrise ILLUSION PSIONIC, Boost 2). « When Revealed : Discard 3 cards from the top of the encounter deck. Reveal each obligation discarded in this way.
# If no obligation was not revealed this way, search the encounter deck, discard pile, set-aside area, and removed-from-game area for a copy of your obligation, then
# reveal it and remove this card from the game. »
# Cartes de reference : hf321 / hf325 (`Search...` + `face.Reveal`), `Worlds.DiscardEncounterCards(3, effect)`, `Faces.RemoveAllFromGame`, `CardFinder(obligation_give_to=joueur)`.
# ⚠⚠ LECTURE (QUESTIONS.md n°2) : « If no obligation was NOT revealed this way » est un DOUBLE NEGATIF. Lu a la lettre il est toujours vrai (chaque obligation defaussee est
# revelee) ; lu comme « If no obligation was revealed this way » (coquille probable), il ne l'est que si AUCUNE obligation n'a ete defaussee. CHOIX PROVISOIRE : la lecture
# voulue (aucune obligation revelee -> on cherche la VOTRE, on la revele, la carte quitte la partie) ; sinon la carte reste simplement defaussee avec le reste.
# ⚠ « your obligation » : l'obligation DONNEE a ce joueur (`obligation_give_to`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        defaussees = Worlds.DiscardEncounterCards(3, effect)
        obligations = [f for f in defaussees if Obligation.IsType(f)]
        for face in obligations:
            face.Reveal(joueur, effect)
        if not obligations:
            la_votre = Search.SearchForCard(effect, joueur, include_encounter_deck=True, include_encounter_discard_pile=True, include_set_aside=True,
                                            include_removed_area=True, card_type=Obligation, obligation_give_to=joueur)
            if la_votre is not None:
                la_votre.Reveal(joueur, effect)
                Faces.RemoveAllFromGame([this], effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
