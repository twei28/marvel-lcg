from . import *

# The Thirst — OBLIGATION (bandeau BLADE, set du heros), 2 icones de boost.
# Give to the Eric Brooks player.
# Uses (3 thirst counters).
# Forced Interrupt: When your turn begins, remove 1 blood counter from your
#   identity to remove 1 thirst counter from here. If you cannot, take 2 damage.
#
# CARTES DE REFERENCE
#  - `WhenPlayerTurnBegin(ForcedInterrupt, "You", op)` (turn_phase.py:23).
#  - fiche uses.md : `desc.Uses = "3,thirst"`, la sortie de jeu au dernier pion
#    est NATIVE (`RemoveCountersInternal`), ne pas la coder.
#  - `ar010` Ire of Athena : une obligation qui RESTE en jeu.
#  - `ar006` Feint : `this.DealDamage([identite], 2, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « When YOUR turn begins » -> le tour du joueur qui la controle, chaque
#    round tant qu'elle est en jeu : trois tours avec un pion de sang chacun
#    la font partir ; sans pion, 2 degats a l'identite et elle RESTE.
#  ⚠ « remove 1 blood counter from your identity TO remove 1 thirst counter »
#    -> le pion de sang est la condition ; sans lui, rien n'est retire ici.
#  ⚠ « take 2 damage » -> l'identite, quelle que soit la forme.


def GetAbilities() -> Sequence['Ability']:

    def la_soif(effect: 'Effect', message: 'Message.WhenPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        # ⚠ Le joueur est lu sur le MESSAGE (`to_player`), pas sur le controleur
        # de l'obligation : en jeu, une carte de rencontre n'est controlee par
        # aucun joueur, et `JoueurDeCetteCarte` rendait None (la capacite
        # « activait » sans rien faire, cas bl011 du 07/09/2026).
        joueur = getattr(message, "to_player", None)
        if not EstJoueur(joueur):
            joueur = JoueurDeCetteCarte(effect)
        identite = IdentiteDuJoueur(effect, joueur)
        if identite is None:
            return
        if PionsDeSang(identite) >= 1:
            Faces.RemoveCountersOn([identite], 1, COMPTEUR_SANG, effect)
            Faces.RemoveCountersOn([this], 1, COMPTEUR_SOIF, effect)
            return
        this.DealDamage([identite], 2, effect)

    return [
        AbilityFactory.WhenPlayerTurnBegin(
            AbilityType.ForcedInterrupt,
            "You",
            la_soif,
        ),
    ]
