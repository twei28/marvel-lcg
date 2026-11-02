from . import *

# Psychic Combo (TREACHERY PSIONIC TACTIC, x2 : hf616, hf617). Boost 1 + etoile. « When Revealed : Cassandra Nova activates against you. You are
# stunned. [star] Boost : If this activation is an attack, this attack gains overkill and piercing. Otherwise, place threat on the main scheme
# equals to the number of Cassandra Controls counter on your identity. »
# Cartes de reference : 27082 / 27136 (`villain.DoActivate(joueur, effect)`), ts201 (`would_atk_message.GainPiercing`), hf112 (boost conditionnel a
# une attaque), `GainOverKill` (sender_damage.py).
# ⚠ Ordre imprime : l'activation PUIS l'etourdissement ; « this activation » : celle pour laquelle la carte est boost (le « you » du boost = le
# joueur vise) ; « threat equals to the number of counters on YOUR identity » : le compte se lit au moment du boost.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        villain = VilainCN(effect)
        if villain is not None:
            villain.DoActivate(joueur, effect)
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if message.being_message.IsAttack():
            message.would_atk_message.GainOverKill(effect)
            message.would_atk_message.GainPiercing(effect)
        else:
            joueur = message.GetToPlayer()
            n = Controles(joueur) if joueur is not None else 0
            if n > 0:
                effect.this.PlaceThreatOnSchemes("MainScheme", n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
