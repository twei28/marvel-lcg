from . import *

# * Spiders-Man

def GetAbilities() -> Sequence['Ability']:

    def spiders_man(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        disponibles = this.GetCounters('spider')
        if disponibles <= 0:
            return
        combien = initiator.DeclareNumber(1, disponibles)
        Faces.RemoveCountersOn([this], combien, 'spider', effect)
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal %d damage to an enemy" % combien,
                lambda targets: this.DealDamage(targets, combien, effect)
            ).SetTarget(Enemy)
        )

    return [
        Fragile(),
        # « Uses (5 spider counters) » : le champ `desc.Uses` n'existe QUE pour
        # Upgrade, Support, Attachment, Obligation et Environment. Spiders-Man
        # est un allie : ses compteurs sont poses ici.
        AbilityFactory.ThisEnterPlayWithCounters(5, 'spider'),
        # « il ne peut pas quitter le jeu tant qu'il a des compteurs spider » :
        # le moteur sait empecher une defaite, c'est le sens jouable de la
        # phrase pour un allie a 0 PV.
        *AbilityFactory.UnitCannotBeDefeatedWhile(
            AbilityType.NonKeyword,
            "This",
            condition=lambda effect:
                effect.this.CastTo(CanPlaceCounter).GetCounters('spider') > 0,
            change_on_event=OnEvent.Counter("This", 'spider'),
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.ForcedInterrupt,
            "This",
            spiders_man
        ).SetTarget('Trigger'),
    ]
