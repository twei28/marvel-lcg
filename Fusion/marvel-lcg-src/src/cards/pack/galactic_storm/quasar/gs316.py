from . import *

# Quantum Weapon — amelioration signature (QUASAR 16/16). SUPERPOWER.
# Cout 2, [wild].
# Hero Interrupt: When you pay for an ATTACK event with Quantum Bands, that
#   attack deals 1 additional damage and gains piercing and overkill.
#
# Cartes de reference :
#  - **`32047`** Aggressive Energy / `54002` Cybernetic Arm : au paiement d'un
#    evenement ATTACK, `RegisterTemp(WhenUnitWouldAttack(Temp0, "You",
#    DealAdditionalDamage(1), by_effect=message.for_effect),
#    until_resolve_effect=message.for_effect)` (RECETTES §2 « +1 degat a un
#    evenement ») ; ici la fenetre est le paiement PAR LES BANDES (helper
#    `QuandLesBandesPaient`, voir gs313).
#  - `WhenUnitWouldAttack.GainPiercing / GainOverKill` (sender_damage.py) pour
#    « gains piercing and overkill » sur l'attaque en cours.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « THAT attack » : l'attaque de l'evenement paye, une seule fois
#    (`unregister_after_exec=True`), pas toutes les attaques du round.
#  - « 1 ADDITIONAL damage » : +1 en plus des degats imprimes ; avec No Holding
#    Back (3 par [physical]) l'attaque fait 3n + 1.
#  - « gains piercing AND overkill » : les deux.
#  - « [[ATTACK]] event » : trait ATTACK + type evenement.


def GetAbilities() -> Sequence['Ability']:

    def arme(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        this = effect.this.CastTo(Upgrade)

        def renforcer(effect2: 'Effect', atk_message: 'Message.WhenUnitWouldAttack') -> None:
            atk_message.DealAdditionalDamage(1, effect2)
            atk_message.GainPiercing(effect2)
            atk_message.GainOverKill(effect2)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                "You",
                renforcer,
                by_effect=message.for_effect,
            ),
            unregister_after_exec=True,
            until_resolve_effect=message.for_effect,
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        QuandLesBandesPaient(
            AbilityType.HeroInterrupt,
            CardFinder2("ATTACK", Event),
            arme,
        ),
    ]
