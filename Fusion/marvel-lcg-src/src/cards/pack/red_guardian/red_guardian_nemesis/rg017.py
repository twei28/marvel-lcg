from . import *

# Symbol of Failure — traitrise nemesis de Red Guardian
# When Revealed: Choose to either discard a card you control or discard 1
#   random card from your hand.
#
# Meme forme que rg015 et rg016 : un `ChooseAbilities` a deux options.
#
# « A card you control » : `from_where=["YouControlCards"]`, la zone du
# selecteur qui applique la definition officielle — cartes EN JEU sous le
# controle du joueur uniquement (selector_where.py:169). Elle inclut la carte
# identite, d'ou `canbe_discard=True` qui ecarte les identites et les cartes
# permanentes (checker.py:169). Gabarit de la paire zone + filtre : Ben Urich
# (bkw/black_widow/08025) et Doctor Faustus (agent_13/agent_13_nemesis/ag012)
# pour le fait de poser le `.SetTarget()` sur le `ForChoiceAbility` et non sur
# la capacite de la carte de rencontre.
#
# Si le joueur ne controle rien de defaussable, l'option n'a pas de cible
# legale et `ChooseEffects` la retire : il ne reste que la defausse au hasard.
# C'est la regle du choix (« an option that you can fulfill »), pas un ecart.


def GetAbilities() -> Sequence['Ability']:

    def symbol_of_failure(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a card you control",
                lambda targets:
                    Faces.DiscardAll(targets, effect),
            ).SetTarget(from_where=["YouControlCards"], canbe_discard=True),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 random card from your hand",
                lambda targets:
                    joueur.DiscardRandomHandCards(1, effect),
            ),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            symbol_of_failure,
        ),
    ]
