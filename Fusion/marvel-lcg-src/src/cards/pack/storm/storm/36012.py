from . import *

# Flash Freeze

def GetAbilities() -> Sequence['Ability']:

    def flash_freeze(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        def get_attack(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
            message.trigger.CastTo(Unit2).GainForThisActive(effect, message, attack=-3)

        get_attack(effect, message)

        initiator = effect.GetInitiator()

        # CORRECTIF (10/10/2026, audit Storm) : « the villain and each minion
        # engaged with you ... this phase ». La liste etait figee au jeu de la
        # carte : un sbire engage PLUS TARD dans la phase attaquait sans le -3.
        # Rules Reference, Lasting Effects : l'effet se met a jour, une carte
        # arrivee apres sa creation est quand meme affectee. On juge donc
        # l'attaquant au moment de CHAQUE attaque.
        def mechant_ou_sbire_engage(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
            attaquant = message.trigger
            if Villain.IsType(attaquant):
                return True
            return Minion.IsType(attaquant) and attaquant in initiator.GetEngagedMinions()

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitAttackYou(
                AbilityType.Temp0,
                None,
                get_attack,
                conditions=[mechant_ou_sbire_engage],
            ),
            unregister_after_exec=False,
            until_phase_end=True
        )

        blizzard = Worlds.FindCardOnField(
            effect,
            name="Blizzard",
            card_type=Support
        )
        if blizzard:
            blizzard.ResolveSpecialAbility(initiator, effect)


    return [
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.HeroInterrupt,
            Villain,
            flash_freeze,
        ).SetPlay().SetLabel('defense')
        .SetTarget("Attacker"),
    ]

