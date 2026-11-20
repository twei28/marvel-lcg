from . import *

# Cosmic Surfboard — UPGRADE. ITEM. SURFBOARD. Permanent. Setup. Sans cout
# imprime (entre en jeu au Setup, modele dm001b/`04159a` Basic Thwart Upgrade :
# `desc` = {"Permanent": "1", "Setup": "1"}, aucune cle Cost).
#
# Texte imprime :
#  « Forced Interrupt: At the end of the round, all enemies at a PLANET
#    depart. »
#  « Action: Exhaust this card and choose a PLANET → Silver Surfer arrives
#    at that PLANET. »
#
# CARTES DE REFERENCE
#  - `fne/bullseye/60075.py` : `.SetTarget(card_type=Support, trait="...")`
#    pour cibler une carte EN JEU par type+trait (modele de la cible
#    « choose a PLANET »). Les cartes PLANET de ce pack sont typees `Support`
#    (voir pc003 Zenn-La a venir) : aucun nouveau type de carte invente,
#    lecon du 05/11/2026 (docs/reference/mots-cles/environnement-joueur.md).
#  - `AbilityFactory.WhenRoundEnd(ForcedInterrupt, None, ...)` (turn_phase.py)
#    pour « at the end of the round ».
#  - `Worlds.GetOnFieldEnemies(effect)` : tous les ennemis EN JEU (le marqueur
#    ne les deplace jamais, decision du 04/11/2026), filtres par
#    `EstÀUnePlanète(...) is not None`.
#  - helpers `ArriverA`/`EstÀUnePlanète` (__init__.py du pack).
#
# TEXTE CONTRE CODE
#  « all enemies at a PLANET depart » : TOUS, pas un seul — boucle sur
#    `Worlds.GetOnFieldEnemies`, pas de limite.
#  « Silver Surfer arrives » : toujours l'identite de Silver Surfer (pas
#    « a character »), quelle que soit sa face courante.
#  « choose a PLANET » : n'importe quelle carte PLANET en jeu, pas
#    necessairement celle du joueur qui active l'action.


def GetAbilities() -> Sequence['Ability']:

    def tous_les_ennemis_partent(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        Unused(message)
        for ennemi in Worlds.GetOnFieldEnemies(effect):
            if EstÀUnePlanète(ennemi) is not None:
                Departir(effect, ennemi)

    def arriver(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        if not effect.targets:
            return
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        silver_surfer = joueur.GetIdentity()
        ArriverA(effect, silver_surfer, effect.targets[0])

    return [
        AbilityFactory.WhenRoundEnd(
            AbilityType.ForcedInterrupt,
            None,
            tous_les_ennemis_partent,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            arriver,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(card_type=Support, trait="PLANET"),
    ]
