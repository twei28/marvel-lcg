from . import *

# Psychic Bulwark (manigance annexe PSIONIC, Victory 1, Boost 2 + [star]). « Each minion gains guard and patrol. [star] Boost : Give each minion a tough status card. »
# Victory 1 : natif. Cartes de reference : 27142 Guerrilla Tactics / hf313 (`GiveKeywordToInPlayWhenApplyThis(Minion, guard=1, patrol=1)`), 01121 (`GiveStatus`),
# fiches guard.md / patrol.md. ⚠ « each minion » : TOUS les sbires en jeu (pas seulement HELLFIRE) ; le Boost : chaque sbire EN JEU recoit un statut Tough.


def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        Faces.GiveStatus(Worlds.GetOnFieldMinions(effect), "Tough", effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Minion, guard=1, patrol=1),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
