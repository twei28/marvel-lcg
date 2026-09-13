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
#
# ⚠ ARBITRAGE, decision utilisateur du 13/09/2026 : « une carte qui porte
# l'image de son identite » = une CARTE SIGNATURE. Voir le `__init__.py` du
# set, l'arbitrage vaut pour les quatre cartes qui l'emploient.
#
# TEXTE CONTRE CODE
#  ⚠ « A PLAYER », pas « vous » : en multijoueur, Muse se reveille sur la carte
#    de n'importe qui, et s'active CONTRE CE JOUEUR-LA — pas contre celui avec
#    qui il est engage. D'ou `"AnyPlayer"` et `message.to_player`.
#  ⚠ « Forced INTERRUPT » : Muse frappe AVANT que la carte se resolve. Un
#    evenement d'attaque joue sur lui le trouvera donc deja actif.
#  ⚠ AUCUNE limite imprimee : deux cartes signature dans le meme tour
#    declenchent DEUX activations. C'est ce qui rend le sbire punitif, et c'est
#    voulu — le set entier punit le kit signature.
#  ⚠ « ELITE » : le trait compte, plusieurs cartes du jeu comptent les sbires
#    d'elite (`24069` Combined Effort). Il est dans `traits`, pas dans un script.


def GetAbilities() -> Sequence['Ability']:

    def muse_se_reveille(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Minion)

        joueur = message.to_player
        if joueur is None:
            return
        this.DoActivate(joueur, effect)

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.ForcedInterrupt,
            "AnyPlayer",
            None,
            muse_se_reveille,
            conditions=[
                lambda effect, message:
                    EstUneCarteSignature(message.played_face)
            ],
        ),
    ]
