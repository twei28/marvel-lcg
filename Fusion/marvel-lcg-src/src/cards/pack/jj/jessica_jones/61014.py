from . import *
def GetAbilities() -> Sequence['Ability']:
    def attach_stakeout(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        for target in effect.targets:
            this.AttachTo2(target, effect)
    def check_in_play_area(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # « If this card is in your play area » : Stakeout attend d'etre en jeu
        # SANS etre encore accrochee a une manigance.
        return effect.this.IsInPlay() and effect.this.CastTo(Upgrade).bind_face is None
    def bonus_thwart(effect: 'Effect', message: 'Message.WhenSchemeBeingThwart') -> None:
        message.GainThwartForThisThwart(2, effect)
    def check_bonus_thwart(effect: 'Effect', message: 'Message.WhenSchemeBeingThwart') -> bool:
        return message.scheme == effect.this.CastTo(Upgrade).bind_face
    def evidence_on_defeat(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        alias = Worlds.FindCardOnField(effect, name='Alias Investigations')
        if alias:
            alias.PlaceCountersInternal(2, 'evidence', effect)
    def check_defeated(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> bool:
        target = effect.this.CastTo(Upgrade).bind_face
        return target is not None and target.CastTo(Scheme2).IsDefeated()
    return [
        # Stakeout entre en jeu dans la zone du joueur SANS etre accrochee ;
        # c'est l'action ci-dessous qui l'accroche ensuite a une manigance
        # annexe. Sans cette option, la carte restait injouable.
        AbilityFactory.CanPlayThisUpgradeCard("Players"),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, attach_stakeout, conditions=[check_in_play_area])
        .SetTarget(CardFinder(card_type=EncounterSideScheme, is_permanent=False), range=(1, 1)),
        AbilityFactory.WhenUnitThwartScheme(AbilityType.Interrupt, None, bonus_thwart, conditions=[check_bonus_thwart]),
        AbilityFactory.AfterUnitThwartScheme(AbilityType.Response, None, None, evidence_on_defeat, conditions=[check_defeated]),
    ]
