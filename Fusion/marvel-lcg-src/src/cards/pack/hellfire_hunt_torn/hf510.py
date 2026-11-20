from . import *

# Hellfire Assault (manigance annexe, menace 1 par joueur, [star] Boost). « Threat cannot be removed from here except by thwarting. Forced Response : After a HELLFIRE
# minion is defeated by a player, if it is White Queen, Emma Frost attacks the player. Otherwise, Emma Frost schemes. [star] Boost : Reveal this card. »
# Cartes de reference : `ThreatCannotBeRemovedFromWhile("This", by_thwarting=False)` (scheme.py), hf110 (`WhenCardBecomeBoost("This", RevealThisCard)`), hf120
# (`villain.DoAttackYou(joueur, effect)` / `villain.DoSchemes(joueur, effect)`), `WhenUnitBeDefeated(..., has_defeating_player=True)`.
# ⚠ « defeated BY A PLAYER » : `has_defeating_player=True`. « the player » = le joueur qui a vaincu le sbire (Emma l'attaque, ou manigance contre lui).
# « if it is White Queen » : le sbire vaincu s'appelle White Queen (Perfection hf301 / hf302), pas le vilain Emma Frost.


def GetAbilities() -> Sequence['Ability']:
    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        joueur = message.defeating_player
        emma = EmmaFrost(effect)
        if joueur is None or emma is None:
            return
        if message.trigger.IsName(NOM_WHITE_QUEEN):
            emma.DoAttackYou(joueur, effect)
        else:
            emma.DoSchemes(joueur, effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile("This", by_thwarting=False),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.ForcedResponse, CardFinder2(HELLFIRE, Minion), vaincu, has_defeating_player=True),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
