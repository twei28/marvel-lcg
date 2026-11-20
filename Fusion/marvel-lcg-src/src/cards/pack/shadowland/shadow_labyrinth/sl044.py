from . import *

# No Time to Think! — TRAITRISE x2. Peril. Boost 1 + ★.
# When Revealed : The villain activates against you.
# ★ Boost : If this activation is an attack, this card gains [boost][boost] and this attack gains overkill.
#
# Cartes de reference : bp/extreme_risk/51041 (`WhenEnemyWouldActivate`), game/card/face/base/enemy.py `DoActivate(joueur, effect)` (attaque ou manigance selon la forme),
# gmw/badoon_lieutenant/16119 (`message.GainBoostIcon(n, effect)` en boost, `during_scheme=True`), an013 Hel-Wolf (`attaque.GainOverKill(effect)`), peril.md (Peril natif).
# ⚠ Mots-pieges : « the villain activates against YOU » : le joueur a qui la carte est revelee ; Shifting Corridors, s'il est le vilain, REMPLACE cette activation (sl037) ;
#  « if this activation IS AN ATTACK » (`during_attack`) : en forme alter-ego l'activation est une manigance et le boost ne fait rien ; « gains [boost][boost] » : +2
#  icones pour CETTE activation ; « this attack gains overkill » ; Peril natif (desc).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            vilain.DoActivate(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GainBoostIcon(2, effect)
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
