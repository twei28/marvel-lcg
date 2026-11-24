from . import *
from .jigsaw_commun import TrouverJigsaw

# A Made Man — TRAITRISE. Boost 1★.
# When Revealed (Alter-Ego) : Discard an ally from play. Otherwise, place 1[per hero] threat on each scheme.
# When Revealed (Hero) : Give Jigsaw a facedown boost card. If a MAGGIA minion is in play, give him an additional
#   boost card.
# ★ Boost : After this activation, give Jigsaw a facedown boost card.
#
# Cartes de reference : `PlaceThreatOnSchemes("EachScheme", "1*", effect)` (sm/campaign.py, 27094),
# `Faces.GiveFacedownBoostCards` (new_revengers/sk167), `RunAt.AfterEnemyActivationEnd` (secret_invasion/sk196),
# `WhenThisRevealed("Alter-Ego"|"Hero", ...)`.
#
# ⚠ « Discard an ally FROM PLAY » (sans « you control ») : l'allie est choisi parmi TOUS ceux en jeu, par le joueur
# qui revele ; aucun allie = « Otherwise » (menace 1 par joueur sur CHAQUE complot, principal et annexes).
# « an ADDITIONAL boost card » : 1 + 1 = 2 en tout si un sbire MAGGIA est en jeu (le vilain Jigsaw ne compte pas).

def GetAbilities() -> Sequence['Ability']:

    def alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        allies = [a for j in Worlds.GetPlayers(effect) for a in j.GetControlAllies()]
        if allies:
            choisi = allies[0] if len(allies) == 1 else joueur.AskChooseFace(allies, effect)
            if choisi is not None:
                Faces.DiscardAll([choisi], effect)
                return
        this.PlaceThreatOnSchemes("EachScheme", "1*", effect)

    def heros(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        jigsaw = TrouverJigsaw(effect)
        if jigsaw is None:
            return
        nombre = 1
        if any(m.HasTrait("MAGGIA") for m in Worlds.GetOnFieldEnemies(effect) if Minion.IsType(m)):
            nombre += 1
        Faces.GiveFacedownBoostCards([jigsaw], nombre, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        def ensuite() -> None:
            jigsaw = TrouverJigsaw(effect)
            if jigsaw is not None:
                Faces.GiveFacedownBoostCards([jigsaw], 1, effect)
        RunAt.AfterEnemyActivationEnd(effect, message.would_message, ensuite)

    return [
        AbilityFactory.WhenThisRevealed("Alter-Ego", alter_ego),
        AbilityFactory.WhenThisRevealed("Hero", heros),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
