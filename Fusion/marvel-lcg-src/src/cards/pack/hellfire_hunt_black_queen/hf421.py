from . import *

# Eternal Night. Manigance annexe, menace 3. « Time counter on Under the Moonlight environment could not be removed. When Revealed : Flip
# Beneath the Sun. » Cartes de reference : 16093 / `Message.WhenCardWouldRemovedCounter` + `SetBeInstead` (can_place_counter.py : le retrait est
# remplace par rien, aucune suite `AfterCardRemovedCounter`, donc pas de retournement), 39026a (`card.Flip`).
# « Flip Beneath the Sun » : si le JOUR est la face visible, l'environnement se retourne (la nuit entre en jeu avec ses 3 compteurs par joueur :
# QUESTIONS.md n°1) ; si c'est deja la nuit, rien. La capacite « could not be removed » vit SUR CETTE CARTE (preuve par substitution).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        env = Temps(effect)
        if env is not None and env.IsName(NOM_JOUR):
            env.card.Flip(effect)

    def sur_la_nuit(effect: 'Effect', message: 'Message.WhenCardWouldRemovedCounter') -> bool:
        return message.counter_name == COMPTEUR_TEMPS and Environment.IsType(message.trigger) and message.trigger.IsName(NOM_NUIT)

    def pas_de_retrait(effect: 'Effect', message: 'Message.WhenCardWouldRemovedCounter') -> None:
        message.SetBeInstead(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        Ability(AbilityType.NonKeyword, Message.WhenCardWouldRemovedCounter, [sur_la_nuit], pas_de_retrait),
    ]
