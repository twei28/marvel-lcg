from . import *

# Bobby's Belt : AMELIORATION (ITEM. TECH.), cout 3, [energy].
# Reduce the cost of this card by 1 if you control an upgrade with the TECH trait. Reduce the damage Beast takes by 1.
#
# CARTES DE REFERENCE
#  - `28027` Height Advantage : `WhenUnitWouldTakeDamage(NonKeyword, "You", fn)` + `message.ReduceDamage(1, effect)` (« reduce » : la Robustesse reste, contrairement a `PreventDamage`).
#  - `nt005` : `ReduceCostToPlayThis(1, conditions=[..])`.
#
# TEXTE CONTRE CODE
#  « Reduce the damage Beast takes by 1 » : TOUS les degats subis (attaque ou non, aucune restriction imprimee : `is_from_attack` laisse a `None`), par instance. « BEAST takes » : forme heros seulement
#    (condition `IsHero`). Un degat de 0 ne descend pas sous 0.
#  Chiffres : cout 3, reduction 1, degats -1.


def GetAbilities() -> Sequence['Ability']:

    def controle_une_amelioration_tech(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and bool(AmeliorationsTech(joueur))

    def en_forme_heros(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        Unused(message)
        joueur = effect.this.CastTo(Upgrade).GetControlByPlayer()
        return joueur is not None and joueur.IsHero()

    return [
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[controle_une_amelioration_tech]),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.NonKeyword,
            "You",
            lambda effect, message:
                message.ReduceDamage(1, effect),
            conditions=[en_forme_heros],
        ),
    ]
