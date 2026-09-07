from . import *

# Sundered — AMELIORATION, cout 0, [physical]. CONDITION. TACTIC. x2.
# Attach to a minion. Max 1 per enemy.
# Increase the amount of damage attached enemy takes from each attack by 1.
#
# BRIQUE 6 : une amelioration JOUEUR attachee a un SBIRE.
#
# CARTES DE REFERENCE
#  - `sf006` Atomic Samurai (pack sunfire) et `dt094` Diversion Skill :
#    `WhenUnitWouldTakeDamage` + `message.IncreaseDamage(n, effect)`, la
#    fenetre et la primitive qui alourdissent des degats deja en route.
#    ⚠ `UpdateDamage` existe aussi mais sur un AUTRE message (l'exces,
#    sender_damage.py:932) : l'employer ici ne ferait rien (lecon sf006).
#  - `damage.py` : le drapeau `is_from_attack=True` de la meme fabrique.
#
# TEXTE CONTRE CODE
#  ⚠ « Attach to a MINION » -> `CanPlayThisUpgradeCard(Minion)`.
#  ⚠ « Max 1 per enemy » -> `desc.MaxPerUnit = "1"`, aucun code.
#  ⚠ « from EACH ATTACK » -> `is_from_attack=True` : les degats directs
#    (Feint, un evenement « deal 3 damage » qui n'est pas une attaque) ne sont
#    pas alourdis. Spray and Pray (ar002) est CINQ attaques : +5 sur un sbire
#    sondere.
#  ⚠ « ATTACHED enemy takes » -> `conditions=[est_mon_hote]` sur
#    `message.trigger`, l'unite qui va prendre les degats.
#  ⚠ Capacite CONSTANTE (aucun mot en gras) -> `ForcedInterrupt`, jamais un
#    Interrupt optionnel : personne ne choisit d'alourdir ou non.


def GetAbilities() -> Sequence['Ability']:

    def est_mon_hote(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        hote = Hote(effect.this)
        return hote is not None and getattr(message, "trigger", None) is hote

    def alourdir(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.IncreaseDamage(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Minion),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            Enemy,
            alourdir,
            is_from_attack=True,
            conditions=[est_mon_hote],
        ),
    ]
