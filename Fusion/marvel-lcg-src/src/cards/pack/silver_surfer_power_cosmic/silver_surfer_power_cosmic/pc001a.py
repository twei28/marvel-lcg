from . import *

# * Silver Surfer (face HEROS) — POWER COSMIC. COSMIC. AERIAL. HP 12, THW 1,
# ATK 1, DEF 2, main 5.
#
# Texte imprime :
#  « Characters at a PLANET cannot attack or scheme and lose guard and
#    patrol. »
#  « Surf — Action: I depart a PLANET. »
#
# Meme texte passif imprime a l'IDENTIQUE sur la face Alter-Ego (pc001b) :
# les deux faces l'implementent chacune separement via le helper partage
# `AbilitésBlocagePlanet` (silver_surfer_power_cosmic/__init__.py), une
# capacite imprimee sur une face n'etant active que quand cette face est
# visible. Decision utilisateur du 05/11/2026 (A creer/import-silver-surfer-
# power-cosmic/QUESTIONS-AUTEUR.md, Q1) : SEUL le texte imprime compte —
# attaque et manigance bloquees, PAS la defense.
#
# CARTES DE REFERENCE
#  - `sk185`/`sk283` (skrull_menace) : `WhenUnitWouldAttack(ForcedInterrupt,
#    ...)` + `SetBeInstead` pour empecher une attaque de se produire du tout ;
#    `sk283` avec un CardType large (`Ally`) pour une portee GENERALE,
#    modele repris ici avec `CardFinder()` (n'importe quel personnage, ami ou
#    ennemi — Black Hole, pc003 a venir, peut y envoyer le mechant/des sbires).
#  - `01056` Tac Team (core) : gabarit d'une `AbilityType.Action` imprimee,
#    sans cout, sur `AbilityFactory.WhenInYourPlayTurn`.
#  - helpers `EstÀUnePlanète`/`Departir`/`AbilitésBlocagePlanet` (voir
#    __init__.py du pack) : fiche docs/reference/mots-cles/environnement-joueur.md.
#
# TEXTE CONTRE CODE
#  « lose guard and patrol » : Garde/Patrouille sont des capacites de SBIRE
#    dans ce moteur (aucun allie/heros du joueur n'en a) ; decision
#    utilisateur du 04/11/2026 : phrase sans effet de code supplementaire —
#    un ennemi a une planete est deja exclu de l'activation normale par le
#    blocage attaque/manigance.
#  « Surf — Action: I depart a PLANET » : seulement si Silver Surfer est
#    actuellement a une planete (condition posee sur l'Action, pas verifiee
#    dans l'operation, pour que l'action ne soit meme pas proposee sinon).


def GetAbilities() -> Sequence['Ability']:

    def peut_partir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return EstÀUnePlanète(effect.this) is not None

    def surf(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        Departir(effect, effect.this)

    return AbilitésBlocagePlanet() + [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            surf,
            conditions=[peut_partir],
        ).SetName("Surf"),
    ]
