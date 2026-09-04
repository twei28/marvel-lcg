from . import *

# Proper Funeral (x2) — EVENEMENT BASIC, cout 0, [mental].
# Alliance. Max 1 per phase.
# Response: After an ally is defeated, remove that ally from the game -> draw
#   3 cards.
#
# ⚠ `Alliance` est un mot-cle OFFICIEL, employe par 17 cartes du jeu
# (fiche docs/reference/mots-cles/alliance.md) : « les joueurs peuvent payer
# le cout de cette carte en groupe ». Rien a coder, le moteur le lit.
#
# TEXTE CONTRE CODE
#  « REMOVE that ally FROM THE GAME » est le COUT (fleche), pas l'effet : sans
#    allie a sacrifier, la carte ne se joue pas.
#  « Max 1 per phase » -> `.MaxOnePerPhase()` (modele 19030 « Bring It! »).
#  « an ally » -> N'IMPORTE quel allie vaincu, y compris celui d'un voisin.


def GetAbilities() -> Sequence['Ability']:

    def funerailles(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        vaincu = getattr(message, "trigger", None)
        if vaincu is not None:
            Faces.RemoveAllFromGame([vaincu], effect)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(3, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            Ally,
            funerailles,
        ).SetPlay()
        .MaxOnePerPhase(),
    ]
