from . import *

# Human Demon (mp128, deux exemplaires identiques) — SBIRE MYSTIC. PV 2, ATK 1, SCH 2, Boost 1, Patrol 1, Teamwork (MYSTIC) (natifs).
# When Revealed : Place 1 threat on the main scheme. [star] Boost : Put Human Demon into play against you.
# ⚠ Mots-pieges : « the MAIN scheme » (menace sur le complot principal) ; Boost : « against you » = engage avec le joueur vise, tout de suite (pas apres l'activation).


def GetAbilities() -> Sequence['Ability']:
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            effect.this.CastTo(Minion).EngagePlayer(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
