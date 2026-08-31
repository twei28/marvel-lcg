from . import *

# Tasty Meal — evenement. ATTACK. SUPERPOWER. THWART. Cout 2. x2
# Hero Action (attack/thwart): Deal 2 damage to an enemy. Remove 1 threat from
#   a scheme. Venompool gets +1 THW, +1 ATK and +1 DEF until the end of the
#   round. If True Form is in play, this attack gains piercing.
#
# Cartes de reference :
#  - 18020 Hit and Run : deux cibles dans UNE capacite, `SetTarget(Enemy)` +
#    `SetTarget2(Scheme2)`, lues dans `effect.targets` / `effect.targets2`.
#  - 12016 Moxie : `hero.GainUntilRoundEnd(effect, attack=1, thwart=1,
#    defense=1)` — les trois bonus d'un coup, exactement le meme libelle.
#  - av005 "I've Got This!" (pack agent_anti_venom) : le montage qui accorde un
#    mot-cle a l'attaque EN COURS, par une capacite temporaire posee juste
#    avant les degats et retiree des sa premiere execution.
#
# Ordre d'execution : le piercing est pose AVANT `DealDamage`, sinon l'attaque
# est deja resolue quand le mot-cle arrive.

def GetAbilities() -> Sequence['Ability']:

    def tasty_meal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        identity = GetVenompool(effect)

        if TrueFormInPlay(effect) and identity is not None:
            identity.effect.RegisterTemp(
                AbilityFactory.UnitAttackGainKeyword(
                    "This",
                    piercing=True,
                ),
                unregister_after_exec=True,
            )

        this.DealDamage(effect.targets, 2, effect)
        this.RemoveThreatFromSchemes(effect.targets2, 1, effect)

        if identity is not None:
            identity.GainUntilRoundEnd(effect, attack=1, thwart=1, defense=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tasty_meal,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]
