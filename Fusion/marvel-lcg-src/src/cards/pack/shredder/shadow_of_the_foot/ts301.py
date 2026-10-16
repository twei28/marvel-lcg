from . import *

# Foot Assassin (x2) — SBIRE (Shadow of the Foot). FOOT CLAN. NINJA.
# MNG 1 / ATQ 1 / PV 1, 2 icones de boost. Quickstrike.
# When Revealed: Cloak Foot Assassin.
# Forced Response: After Foot Assassin attacks, cloak them.
#
# Cartes de reference : `ts010` (« Cloak <lui-meme> » au When Revealed) ;
# `AfterUnitAttackEnd` (RECETTES §1 : « After you attack an enemy », ici avec
# « This » comme attaquant) pour « after Foot Assassin attacks » ; Quickstrike
# dans `desc`.
#
# Mots-pieges : « AFTER Foot Assassin attacks » (Reponse forcee, apres CHAQUE
# attaque, meme sans degats) ; « cloak THEM » = elle-meme ; un seul Cloaked a la
# fois (plafond).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Cloak(effect, effect.this)

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Cloak(effect, effect.this)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", apres_attaque),
    ]
