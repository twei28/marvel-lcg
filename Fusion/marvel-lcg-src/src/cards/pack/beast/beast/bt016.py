from . import *

# Ambush — evenement Discovery (3/5). ATTACK. DEFENSE. Cout 0.
# Forced Interrupt (attack/defense): When the villain would attack you,
#   exhaust an support card in play -> cancel that attack.
#
# Carte de reference : 20003 Grasping Tendrils, « Hero Interrupt (defense):
# When the villain initiates an attack against you, cancel that attack », soit
# `WhenUnitInitiatesAttackAgainst(type, Villain, "You", op)` puis
# `message.CancelThisAttack(effect)`. Comparable au declencheur et a l'effet
# pres ; les deux differences sont le TYPE de capacite et le COUT.
#
# ⚠ ARBITRAGE (utilisateur, 31/08/2026) : le texte imprime dit « **Forced**
# Interrupt » sur un evenement joue depuis la main, ce qui est inhabituel (un
# evenement se joue volontairement, et la carte officielle comparable est une
# « Hero Interrupt »). Decision : **on suit le mot imprime**, la capacite est
# bien codee en `AbilityType.ForcedInterrupt`. Consigne au §6 du journal de
# portage, point 7, pour l'auteur.
#
# ⚠ ARBITRAGE, portee du soutien : « an support card in play » n'est pas
# qualifie. Codee comme UN DES TIENS (`from_where=["YouControlCards"]`),
# puisque c'est le joueur attaque qui paie. Point 11 du §6.
#
# ⚠ « exhaust an support card » est ecrit AVANT la fleche : c'est le COUT, pas
# l'effet. Sans soutien pret a incliner, la carte ne peut pas etre jouee — et
# c'est ce qui empeche l'interruption forcee de partir a vide.
#
# ⚠ SEUL le libelle 'defense' est pose, alors que la carte imprime
# « (attack/defense) ». Le moteur REFUSE 'attack' sur une interruption :
# `check_sub_type` n'autorise que `['defense', 'thwart']` pour un
# `Interrupt`/`ForcedInterrupt` (ability.py:198), et le montage du deck tombe
# sinon en « AssertionError: label='attack' ... [bt016] » des la mise en place
# — constate le 01/09/2026. C'est coherent : le libelle sert a savoir si
# Sonne/Desoriente bloque l'action, et une carte jouee en reaction a l'attaque
# du vilain est une DEFENSE, jamais une attaque. Le modele officiel 20003
# Grasping Tendrils, dont le texte dit « (defense) », ne pose que celui-la.
# Choix technique contraint, pas un arbitrage de regles.
#
# ⚠ Les libelles passent en UN SEUL `SetLabel` : l'appeler deux fois leve un
# autre assert (ability.py:380).

def GetAbilities() -> Sequence['Ability']:

    def ambush(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.CancelThisAttack(effect)

    return [
        AbilityFactory.WhenUnitInitiatesAttackAgainst(
            AbilityType.ForcedInterrupt,
            Villain,
            "You",
            ambush
        ).SetPlay().SetLabel('defense')
        .SetCostFunc(CostFunc.Exhaust(card_type=Support, from_where=["YouControlCards"])),
    ]
