from . import *

# * Princess Anelle — SOUTIEN de campagne (Basic / Campaign, n° 280). Cout X (coin haut gauche « X »).
# PERSONA. SKRULL. Alliance.
# Alliance.
# X is equal to the total number of players and SKRULL enemies in play.
# Response: After the player phase ends, remove Princess Anelle from the game -> skip the villain phase.
#
# Cartes de reference :
#  - **`sk189a`** (`secret_invasion/__init__.py`, `CapacitesSpiderWoman`) : « The players can pay this ... costs as a
#    group » sur une carte qui n'est PAS un evenement = marque `ability.cout_en_groupe = True` sur la capacite
#    de jeu, lue par `CheckAnyPlayerMayHelpPay` (resources.py) ; le mot-cle `Alliance` natif est reserve aux
#    EVENEMENTS (`HasAlliance`, fiche `mots-cles/alliance.md`). Respecte l'interdiction de sk201.
#  - **`sk270`** Buddy Training Program : un cout « X » calcule = `IncreaseResourceCostToPlay("This", fn,
#    "AnyPlayer")` sur un `desc.Cost` de 0.
#  - **`jj/61020`** Run Them to Ground : « skip the villain phase » : AUCUN precedent propre dans le moteur
#    (il neutralise les etapes une a une) ; ici l'ajout minimal `World.skip_villain_phases` lu par la boucle de
#    round (voir defs/campagne_cartes_moteur.md).
#  - **`CostFunc.RemoveFromGame("This")`** : « remove X from the game -> » en COUT.
#
# ⚠ Mots-pieges :
#  - « X = the total number of PLAYERS AND SKRULL ENEMIES IN PLAY » : joueurs + sbires ET mechant SKRULL en jeu,
#    lu a chaque calcul de cout (Anelle n'est pas un ennemi) ;
#  - « AFTER the PLAYER phase ends » : fenetre de Reponse apres la fin de la phase des joueurs (avant la phase du
#    mechant) ; « remove FROM THE GAME » (pas la defausse) est un COUT : sans elle la Reponse n'est pas offerte ;
#  - « SKIP the villain phase » : la phase entiere (menace du complot, activations, cartes rencontre) est
#    sautee, une seule fois (la phase de CE round) ;
#  - Alliance : tous les joueurs peuvent aider a payer.


def GetAbilities() -> Sequence['Ability']:

    def cout_x(effect: 'Effect') -> int:
        return Worlds.GetPlayerNum(effect) + len(EnnemisSkrull(effect))

    def sauter_la_phase_du_mechant(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        effect.world.skip_villain_phases += 1

    jouer = AbilityFactory.CanPlayThisSupportCard()
    jouer.cout_en_groupe = True  # Alliance (voir sk189a)

    return [
        jouer,
        AbilityFactory.IncreaseResourceCostToPlay("This", cout_x, "AnyPlayer"),
        AbilityFactory.AfterPhaseEnd(
            AbilityType.Response,
            "Player",
            sauter_la_phase_du_mechant,
        ).SetCostFunc(CostFunc.RemoveFromGame("This")),
    ]
