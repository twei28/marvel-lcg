from . import *

# * Muse — SBIRE unique. 8 PV, CTR 2, ATQ 2, 3 icones de boost.
# ARTIST. CRIMINAL. ELITE.
# Toughness.
# Forced Interrupt: When a player plays a card that has their identity's
#   picture on it, Muse activates against that player.
#
# CARTES DE REFERENCE
#  - `01102` * Sandman / `04114` Ultimate Bio-Servant : le sbire a `Toughness`
#    dans `desc`. BASE AUTOMATIQUE, aucun script — le moteur pose la carte
#    d'etat Coriace a l'entree en jeu.
#  - `11051` Ancient Grudge : `ennemi.DoActivate(joueur, effect)`, la seule
#    facon de faire agir un ennemi hors de la phase du mechant.
#  - `WhenPlayerPlayCard` (play.py:260) pour la fenetre « quand un joueur joue
#    une carte », avec son `played_card: CardFinder`.
#  - `spider_man_rainy/sr009` J. Jonah Jameson : meme probleme (« a picture of
#    X » est du dessin, le moteur ne le lit pas), meme solution.
#
# ⚠ ARBITRAGE, decision utilisateur du 13/09/2026 puis du 08/11/2026.
# « une carte qui porte l'image de son identite » : l'ancien repli (« carte
# signature ») tournait seul depuis le 13/09, le RELEVE manuel des 5746
# illustrations n'ayant jamais ete rempli — Muse n'a donc jamais applique la
# vraie regle. Remplace le 08/11/2026 : CHAQUE carte jouee, par n'importe qui,
# pose la question au joueur qui vient de jouer (decision utilisateur :
# repetitif mais fidele, « ce que fait un joueur humain face a ce mecanisme
# avec les cartes physiques »).
#
# TEXTE CONTRE CODE
#  ⚠ « A PLAYER », pas « vous » : en multijoueur, Muse se reveille sur la carte
#    de n'importe qui, et s'active CONTRE CE JOUEUR-LA — pas contre celui avec
#    qui il est engage. D'ou `"AnyPlayer"` et `message.to_player`.
#  ⚠ « Forced INTERRUPT » : Muse frappe AVANT que la carte se resolve. Un
#    evenement d'attaque joue sur lui le trouvera donc deja actif.
#  ⚠ AUCUNE limite imprimee : deux cartes qui montrent l'identite dans le meme
#    tour declenchent DEUX activations. C'est ce qui rend le sbire punitif, et
#    c'est voulu — le set entier punit le kit signature.
#  ⚠ « ELITE » : le trait compte, plusieurs cartes du jeu comptent les sbires
#    d'elite (`24069` Combined Effort). Il est dans `traits`, pas dans un script.
#  ⚠ LA QUESTION EST DANS L'OPERATION, PAS DANS UNE CONDITION : une condition
#    de `WhenPlayerPlayCard` peut etre relue plus d'une fois par le moteur
#    (verification, affichage) avant que l'evenement ne resolve vraiment ; y
#    poser une question l'aurait demandee en double, ou hors de propos. Ici
#    la fenetre s'ouvre pour TOUTE carte jouee (aucune condition d'image), et
#    l'operation elle-meme decide, une seule fois, si Muse s'active.


def GetAbilities() -> Sequence['Ability']:

    def muse_se_reveille(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.to_player
        if joueur is None:
            return
        montre = joueur.AskChooseOneText(
            [True, False], ["Yes", "No"],
            f"Muse: does \"{message.played_face.name}\" have a picture of your identity on it?",
        )
        if not montre:
            return
        this.DoActivate(joueur, effect)

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.ForcedInterrupt,
            "AnyPlayer",
            None,
            muse_se_reveille,
        ),
    ]
