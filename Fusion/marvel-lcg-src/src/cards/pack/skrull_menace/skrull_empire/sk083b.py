from . import *

# Andromeda Galaxy Colonization 2B — complot principal, face B : « When Revealed: Reveal the top card of the
# PLANET deck. » (1B, 2B, 3B, 4B ; 4B ajoute « If this stage is completed,
# the players lose the game », regle native : c'est le dernier stade.)
#
# Cartes de reference : **`21129`** Infinity Gauntlet (`GetTopCard` d'un paquet
# de scenario puis mise en jeu d'un environnement) et `21165a` Loki
# (`face.Reveal(...)` depuis un paquet nomme). Helper `RevelerPlanete`.
#
# ⚠ Mots-pieges : « Reveal » (pas « put into play ») : la planete est REVELEE,
# un environnement revele entre en jeu (Environment.OnWhenCardRevealed).
# Paquet PLANET vide : rien. Valeurs de menace dans desc (objectif, escalade,
# depart, regle verifiee par l'utilisateur le 15/10/2026).


def GetAbilities() -> Sequence['Ability']:

    def planete(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        RevelerPlanete(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, planete),
    ]
