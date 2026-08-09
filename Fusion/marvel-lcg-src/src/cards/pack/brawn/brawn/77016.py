from . import *

# Hulk Out (2e exemplaire) — custom « Rainy »
# Uses (2 rage counters).
# For each rage counter here, Brawn gets +1 ATK and +1 DEF and gains retaliate 1.
# Forced Interrupt: When the round ends, remove 1 rage counter from here.
#
# ARBITRAGE (utilisateur, 7/8/2026) : le « for each » porte sur l'ATK et la DEF,
# PAS sur riposte. Deux compteurs donnent donc +2 ATK, +2 DEF et riposte 1 —
# riposte est un etat qu'on a ou qu'on n'a pas, pas une valeur qui monte.
#
# Le bonus n'est pas pose une fois pour toutes : il vaut le nombre de compteurs
# a l'instant ou on le lit, et ce nombre diminue chaque fin de round. D'ou le
# montage de Jessica's Camera 73009 — `get_new_value` sert de multiplicateur et
# `ex_change_on_event` fait relire la valeur a chaque mouvement de compteur.
#
# Le bonus vise "You" et non le type Hero : leçon du pack totally_awesome_hulk,
# ou Motivation et Gamma Barrier ne s'appliquaient jamais parce qu'elles
# visaient un type de carte au lieu du porteur.
#
# Quand le dernier compteur part, le moteur defausse l'amelioration tout seul
# (regle des `Uses`) : rien a ecrire pour cela.

def GetAbilities() -> Sequence['Ability']:

    def compteurs_de_rage(effect: 'Effect', attach: Any, ui: List['CardFace']) -> int:
        return effect.this.CastTo(Upgrade).GetCounters("rage")

    def au_moins_un_compteur(effect: 'Effect', attach: Any, ui: List['CardFace']) -> int:
        return 1 if effect.this.CastTo(Upgrade).GetCounters("rage") > 0 else 0

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.RemoveCountersOn([this], 1, "rage", effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            get_new_value=compteurs_de_rage,
            attack=1,
            defense=1,
            ex_change_on_event=OnEvent.Counter("This", "rage"),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            get_new_value=au_moins_un_compteur,
            retaliate=1,
            ex_change_on_event=OnEvent.Counter("This", "rage"),
        ),

        AbilityFactory.WhenRoundEnd(
            AbilityType.ForcedInterrupt,
            None,
            fin_de_round,
        ),
    ]
