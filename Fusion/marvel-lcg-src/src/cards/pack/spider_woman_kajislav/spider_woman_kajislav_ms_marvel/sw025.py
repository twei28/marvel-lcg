from . import *

# * Ms. Marvel — SBIRE de nemesis (1/5). 4 PV, ATQ 3, MNG 0*, boost 2. ELITE.
# Retaliate 1. Toughness.
# Forced Response: After Ms. Marvel schemes, place 2 threat on Superhuman
#   Registration Act.
# (Spider-Woman's nemesis minion.)
#
# ⚠ RETALIATE, TOUGHNESS et ELITE sont des BASES AUTOMATIQUES, lues dans
# `desc` / `traits` : rien a coder ici. Fiches lues avant d'ecrire :
# `mots-cles/retaliate.md`, `mots-cles/toughness.md`.
#
# ⚠ « SCH 0* » : l'etoile est le degat consecutif, base native elle aussi. Une
# MNG de ZERO avec un Forced Response qui pose 2 menaces ailleurs : la carte ne
# menace jamais le complot principal, elle nourrit l'Acte d'Enregistrement.
#
# CARTE DE REFERENCE
#  - `50029` Press Conference : le couple `AbilityType.ForcedResponse` + une
#    fabrique de fenetre, sans rien d'autre.
#  - `AbilityFactory.AfterUnitSchemeEnd(..., "This", ...)` : « APRES que Ms.
#    Marvel manigance », donc a la fin de l'activation, pas pendant.
#
# TEXTE CONTRE CODE
#  ⚠ « After MS. MARVEL schemes » : elle, pas n'importe quel ennemi. D'ou
#    `"This"`.
#  ⚠ Acte d'Enregistrement absent du jeu : rien ne se passe. Le texte ne
#    prevoit aucun repli.


def GetAbilities() -> Sequence['Ability']:

    def nourrir_l_acte(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        Unused(message)
        PoserSurLActe(effect.this, 2, effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            "This",
            nourrir_l_acte,
        ),
    ]
