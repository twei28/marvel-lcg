from . import *

# * The Cimmerian — amelioration (16/16), recto TITLE, sans cout. Permanent.
# Response: After there are at least 8 Crom counters here, ready your identity
#   and swap him with King Conan. Remove your other identities from the game.
#   Flip this card.
#
# Mise en jeu au Setup par l'alter-ego (cn001b, `SetupPutIntoPlay`, modele
# 26001b Vision). Permanent : lu dans `desc`.
#
# CARTES DE REFERENCE
#  - « After there are at least N counters here » : `AfterCounterPlacedOn(type,
#    "This", 'crom', op, at_least=8)` (factory/counter.py).
#  - l'echange : `Couronner` (conan/__init__.py), arbitrage du 25/09/2026
#    (garde le cote, n'est pas un changement de forme).
#
# TEXTE CONTRE CODE
#  « Response » : optionnelle. Refusee a 8, elle repart au compteur suivant.
#  « Flip this card » : les compteurs restent sur la carte (insert).


def GetAbilities() -> Sequence['Ability']:

    def couronnement(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        Unused(message)
        joueur = JoueurDe(effect)
        if joueur is None:
            joueur = effect.this.GetControlBy()
        if isinstance(joueur, Player):
            Couronner(joueur, effect)

    return [
        AbilityFactory.AfterCounterPlacedOn(
            AbilityType.Response,
            "This",
            'crom',
            couronnement,
            at_least=8,
        ),
    ]
