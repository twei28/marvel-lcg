from . import *

# True Form — amelioration. SUPERPOWER. SYMBIOTE. Cout 1.
# Discard this card from play if you do not control Klyntar Suit.
# Hero Interrupt: When Venompool makes a basic attack against an enemy,
#   exhaust True Form -> that attack gains overkill. Drain 1 from that enemy.
#
# Cartes de reference :
#  - 27017 * Spider-Man : `AfterCardLeavePlay` pour reagir a la disparition
#    d'une AUTRE carte. Aucune carte du depot ne portait « Discard this card
#    from play if... » avant celle-ci (mesure faite sur data/cards.json) : la
#    dependance est donc rendue par l'evenement « Klyntar Suit quitte le jeu »,
#    et non par une verification continue.
#  - av005 "I've Got This!" / av009 Bear Arms : la capacite temporaire
#    `UnitAttackGainKeyword` posee sur l'identite juste avant l'attaque et
#    retiree des sa premiere execution, seule facon d'accorder un mot-cle a
#    UNE attaque precise.
#
# ⚠ « makes a BASIC attack » : `is_basic_attack=True`, contrairement a vp007
# Eat Them All! qui dit « attacks » tout court. Le contraste est imprime dans
# le meme pack, il est donc voulu.

def GetAbilities() -> Sequence['Ability']:

    def klyntar_perdue(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        if not ControlsUpgrade(effect, KLYNTAR_SUIT_NAME):
            this.Discard(effect)

    def true_form(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)

        identity = GetVenompool(effect)
        if identity is not None:
            identity.effect.RegisterTemp(
                AbilityFactory.UnitAttackGainKeyword(
                    "This",
                    overkill=True,
                    is_basic_attack=True,
                ),
                unregister_after_exec=True,
            )

        cibles = [f for f in message.GetAttackTargets() if f is not None]
        Drain(this, cibles, 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.ForcedResponse,
            Upgrade,
            klyntar_perdue,
        ),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            true_form,
            is_basic_attack=True,
            attack_targets=Enemy,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
