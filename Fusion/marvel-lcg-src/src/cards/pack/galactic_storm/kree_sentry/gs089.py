from . import *

# Caught in Its Sights — TRAITRISE (Kree Sentry), 2 exemplaires. 1 icone de boost.
# When Revealed: You may spend 2 resources of any type. If you do not, Kree Sentry attacks Rick Jones.
#
# Cartes de reference :
#  - « You may spend N resources. If you do not, ... » : `joueur.AskSpendResources(Cost("2"), effect)`, modele OFFICIEL
#    28024 War Delivery ; `Cost("2")` = deux ressources de n'importe quel type (modele blade bl015, `Cost("1")`).
#  - « Kree Sentry attacks Rick Jones » : `Enemy.AttackCharacter(cible, effect, ally_attack_is_against_player=False)`
#    (brique commune, RECETTES-MOTEUR §16.1 ; decision du 20/10/2026 : le livret p.4 s'applique dans Galactic Storm).
#
# ⚠ La depense n'est offerte que si deux ressources sont couvrables (`PeutDepenserDeuxRessources`) : sinon le moteur propose un
# paiement PARTIEL (« Do as much as you can »), compte comme depense. Ecart assume : les generateurs en jeu ne sont pas comptes.
#
# ⚠ Mots-pieges : « YOU may spend » (le joueur qui revele, pas le premier) ; « 2 resources OF ANY TYPE » ; « If you do NOT »
# (refus ou impossibilite) ; l'attaque vise RICK JONES directement : l'Interruption forcee de Rick (qui detourne une
# attaque contre « vous ») ne joue pas, les joueurs peuvent defendre comme d'habitude, le « vous » des Boost est le
# controleur de Rick Jones.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if PeutDepenserDeuxRessources(joueur) and joueur.AskSpendResources(Cost("2"), effect):
            return
        sentry = KreeSentry(effect)
        rick = RickJones(effect)
        if sentry is not None and rick is not None:
            sentry.AttackCharacter(rick, effect, ally_attack_is_against_player=False)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
