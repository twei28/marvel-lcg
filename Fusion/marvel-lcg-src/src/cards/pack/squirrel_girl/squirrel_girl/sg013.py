from . import *

# Call the Squirrels
# Action: Call 1 Squirrel. Then, call 1 Squirrel that enters play ready.
#
# Equilibrage (28/08/2026, doc squirrel_girl_..._starter_deck.md §14) : les
# 2 ecureuils entraient prets a l'origine. Aucune carte officielle ne fait
# entrer un allie invoque directement pret (Get Ready ne fait que readier un
# allie DEJA en jeu), donc un seul des deux entre pret desormais. Reformule
# le 28/08/2026 (relecture) : "1 of them enters play ready" ne precisait pas
# LEQUEL des deux ; le texte et l'ordre du code disent maintenant explicitement
# que c'est le SECOND appel qui entre pret (important pour Network of Trees,
# qui s'interpose sur chaque appel separement).

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is not None:
            AppelerEcureuil(joueur, effect, pret=False)
            AppelerEcureuil(joueur, effect, pret=True)

    return [
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, appeler)
            .SetPlay()),
    ]
