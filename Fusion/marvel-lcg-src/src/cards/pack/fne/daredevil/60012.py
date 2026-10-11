from . import *
SENSE_ATTACH_TARGETS = {
    '60002': (Enemy, Scheme2), '60003': (Enemy, Scheme2),
    '60004': (Enemy,), '60005': (Enemy,), '60006': (Scheme2,)}
def MoveSenseUpgrades(player: 'Player', effect: 'Effect') -> None:
    mine = [u for u in Worlds.FindCardsOnField(effect, card_type=Upgrade)
            if u.paper.card_id in SENSE_ATTACH_TARGETS and u.GetControlByPlayer() == player]
    if not mine:
        return
    def choose_upgrades(chosen: Sequence['CardFace']):
        for face in list(chosen):
            upgrade = face.CastTo(Upgrade)
            dests = [t for kind in SENSE_ATTACH_TARGETS[upgrade.paper.card_id]
                     for t in Worlds.FindCardsOnField(effect, card_type=kind)
                     if t != upgrade.bind_face and t != effect.this]
            if not dests:
                continue
            def move(to: Sequence['CardFace'], upgrade=upgrade):
                if to:
                    upgrade.AttachTo2(to[0], effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Move ' + upgrade.paper.name + ' to another card', move).SetTarget(dests, range=(0, 1), not_move=True, not_shuffle=True))
    player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Move any number of Sense upgrades in play to other cards they can attach to', choose_upgrades).SetTarget(mine, range=(0, len(mine)), not_move=True, not_shuffle=True))
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer()
        if not player:
            player = effect.GetInitiator()
        MoveSenseUpgrades(player, effect)
        PlaySenseUpgradeFree(player, effect, any_number=True)
    def check_remover(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        remover = message.by_effect.GetInitiator() if message.by_effect else None
        if remover and Player.IsType(remover):
            for face in remover.GetAllIdentityFace():
                if (face.paper.name in ('Daredevil', 'Matt Murdock')):
                    return False
        return True
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    return [AbilityFactory.CanPlayThisSchemeCard(),
            AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove, conditions=[check_remover]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
