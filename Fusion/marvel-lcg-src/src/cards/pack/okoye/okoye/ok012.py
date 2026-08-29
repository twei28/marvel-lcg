from . import *

# Midnight Angel Armor (1/2)
# Attach to a friendly DORA MILAJE character. Max 1 per character.
# Attached character gets +2 hit points, gains the AERIAL trait, and loses
#   the fragile keyword.
#
# Exemplaire physique 1 de 2 (ok012, ok013). Modele exact du couple play-cible
# + gain permanent : cap/03025.py (Honorary Avenger),
# `AbilityFactory.CanPlayThisUpgradeCard(cible)` +
# `*AbilityFactory.GiveKeywordToAttached(cible, health=2, trait="AERIAL")`.
# "Max 1 per character" est deja applique par le moteur pour toute carte
# attachee du meme NOM (verifie sur Clarity of Purpose, spdr/31029.py, qui ne
# code aucune verification supplementaire).
#
# "loses the fragile keyword" : ce moteur n'a pas de mecanisme generique pour
# desactiver une ability imprimee sur une AUTRE carte. La condition est donc
# integree directement dans `Fragile()` (okoye/__init__.py) : elle verifie
# elle-meme si "Midnight Angel Armor" est attachee et, si oui, n'accorde pas
# l'overkill -- resultat observable identique a "perdre Fragile".


CIBLE = CardFinder(card_type=Friend, trait="DORA MILAJE")


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CIBLE),
        *AbilityFactory.GiveKeywordToAttached(
            CIBLE,
            health=2,
            trait="AERIAL",
        ),
    ]
