from . import *

# * Malice — sbire nemesis d'Okoye, DORA MILAJE. ELITE. WAKANDA
# Steady.
# Forced Response: After an ally is defeated, Malice schemes.
#
# "Steady" est un mot-cle purement declaratif (`desc.Steady`, has_steady.py),
# aucune ability necessaire (verifie sur sm/27074 Venom, qui porte "Steady":
# "1" sans aucun crochet dans son code). "Malice schemes" : declenche une
# action de base SCH hors de son activation normale -- modele du couple
# `BasicAttack`/`this.CastTo(Enemy).BasicAttack(...)` (cw/dangerous_recruits/
# 56087.py), transpose a `BasicSchemes` (can_scheme.py:166, symetrique de
# `BasicAttacks`), qui vise le complot principal sans cible explicite a
# fournir (contrairement a une attaque).


def GetAbilities() -> Sequence['Ability']:

    def malice(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)

        this.BasicSchemes(effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Ally,
            malice,
        ),
    ]
