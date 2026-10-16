from . import *

# Annihilation (TMNT Expert 1/3) — TRAITRISE. Etoile + 2 icones de boost.
# When Revealed: The villain attacks you. That attack gains overkill.
# [star] Boost: If the villain is attacking, this attack gains overkill.
#
# Cartes de reference : `hood 24054` Total Annihilation (MEME mecanique :
# `villain.DoAttackYou(player, effect, property=AttackProperty(overkill=True))`
# et `WhenCardBecomeBoost(..., during_attack=True, attacker=Villain)` +
# `GainOverKill`). ⚠ 24054 n'a que le When Revealed (Hero) ; ici SANS distinction
# de forme (« The villain attacks you » sans parenthese).
#
# Mots-pieges : « the VILLAIN » (pas un sbire : `attacker=Villain`) ; « THAT
# attack » : l'attaque de cette carte.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        villain = Worlds.FindVillain(effect)
        if villain:
            villain.DoAttackYou(message.GetToPlayer(), effect, property=AttackProperty(overkill=True))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True, attacker=Villain),
    ]
