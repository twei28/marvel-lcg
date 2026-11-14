from . import *

# * The Vault — ENVIRONNEMENT. LOCATION.
# Forced Response: After a unique minion (✦) is defeated, place it beneath The Vault facedown.
# If no villain is beneath The Vault, the players lose the game.
# If all the villains are either beneath The Vault or defeated, the players win the game.
#
# Cartes de reference :
#  - « After a unique minion is defeated, place it beneath X facedown » : `AfterUnitBeDefeated(ForcedResponse, Minion, ...,
#    conditions=[unique])` + `CardFace.TuckCardUnderHere` (fiche tuck.md ; helper `PoserSousLeVault`).
#  - Les deux conditions de fin de partie (texte en gras, pas une capacite a declencheur) : `VerifierFinDePartie` (helper du
#    set), appele a chaque changement d'etat qui les touche (mise en place, vilain sous le Vault, vilain vaincu, vilain
#    melange dans le deck, revelation). Victoire : `Worlds.SetGameOver(True, effect)` (modele gs162a) ; defaite : `False`.
#
# ⚠ Mots-pieges : « unique minion (✦) » = `IsUnique()` (nom precede de « * ») ; « beneath » = la zone des cartes glissees du
# Vault, FACE CACHEE ; victoire ET defaite vraies ensemble = VICTOIRE (arbitrage de l'utilisateur, 25/10/2026) ; « defeated »
# = retire de la partie (livret p.1), donc plus en jeu et plus dans le deck de vilains.


def GetAbilities() -> Sequence['Ability']:

    def sbire_unique_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        sbire = message.trigger.CastTo(Minion)
        PoserSousLeVault([sbire], effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse, Minion, sbire_unique_vaincu,
            conditions=[lambda effect, message: message.trigger.IsUnique()]),
    ]
