from . import *

# * 3-D Man's Goggles — AMELIORATION de campagne (Leadership / Campaign, n° 283). Cout 2. ITEM. TECH.
# Attach to a non-SKRULL ally.
# Interrupt: When attached ally attacks a SKRULL enemy, that ally does not take consequential damage.
#
# Cartes de reference :
#  - **`magneto/49007`** Wrapped in Metal : une amelioration qui s'accroche a un type precis =
#    `CanPlayThisUpgradeCard(CardFinder(...))`.
#  - **`wonder_man/58020`** Unified Strike : « does not take consequential damage » = `message.
#    DoesNotTakeConsequentialDamage(effect)` sur le message d'attaque (lu par `Ally.GetAbilities`, ally.py:49).
#  - **`WhenUnitWouldAttack(Interrupt, attacker, op, attack_targets=...)`** (do_attack.py:32).
#
# ⚠ Mots-pieges :
#  - « a NON-SKRULL ally » : cible d'attache (un allie sans le trait SKRULL) ;
#  - « attached ally ATTACKS » : une attaque (pas un contre) de L'ALLIE PORTEUR, pas d'un autre allie ;
#  - « a SKRULL ENEMY » : sbire ou mechant SKRULL attaque ; contre un non-SKRULL, l'allie encaisse ;
#  - « Interrupt » : optionnel ; seuls les degats CONSEQUENTS sont evites (l'ATQ est inchangee).


def GetAbilities() -> Sequence['Ability']:

    def allie_porteur_attaque_un_skrull(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        if message.attacker != effect.this.GetBindFace():
            return False
        cibles = [c for c in message.attacked_targets if Enemy.IsType(c)]
        return bool(cibles) and all(c.HasTrait("SKRULL") for c in cibles)

    def sans_degats_consequents(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DoesNotTakeConsequentialDamage(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Ally, non_trait="SKRULL")),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            Ally,
            sans_degats_consequents,
            conditions=[allie_porteur_attaque_un_skrull],
        ),
    ]
