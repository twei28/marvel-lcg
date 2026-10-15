from . import *

# DNA Masking — COMPLOT ANNEXE nemesis de Hulkling (n° 33, 2/5).
# Menace de depart 3 par joueur, 1 icone boost.
# Minions cannot take damage.
# Threat cannot be removed from DNA Masking while there are no minions in play.
#
# Cartes de reference :
#  - **`60131`** (fne, The Getaway) : « The villain cannot be dealt damage » =
#    `*AbilityFactory.UnitCannotTakeDamage(Villain)` (liste, deballage `*`).
#  - **`31030`** Grand Larceny : « Threat cannot be removed from this scheme
#    while a CRIMINAL minion is in play » = `ThreatCannotBeRemovedFromWhile(
#    "This", ...)`. Ici la condition INVERSE (« while there are NO minions »),
#    d'ou `conditions=` plutot que `while_face_is_in_play=`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Minions** cannot take damage » : TOUS les sbires, de tous les joueurs,
#    tant que le complot est en jeu. Le vilain, lui, se blesse normalement.
#  - « while there are **no** minions in play » : le piege est la combinaison.
#    Sans sbire, la menace ne bouge pas ; avec un sbire, elle bouge mais le
#    sbire est invulnerable. Le complot se vide donc AVEC un sbire en jeu.
#  - Menace de depart « 3★ par joueur » : desc.StartingThreat « 3* » (verifie
#    sur le scan le 15/10/2026, aucune autre icone).
#  - Le texte d'ambiance imprime AU-DESSUS des regles n'est pas une capacite.


def GetAbilities() -> Sequence['Ability']:

    def aucun_sbire(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        Unused(message)
        return not any(Minion.IsType(f) for f in Worlds.GetOnFieldCards(effect))

    return [
        *AbilityFactory.UnitCannotTakeDamage(Minion),
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            conditions=[aucun_sbire],
        ),
    ]
