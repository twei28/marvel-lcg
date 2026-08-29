from . import *
def GetAbilities() -> Sequence['Ability']:
    def attack_twice_more(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        player = message.attacked_you
        if player:
            for _ in range(2):
                this.DoAttackYou(player, effect)
    def boost_ability(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        # « Deal THIS card to the Luke Cage player as a facedown encounter
        # card » : c'est bien cette carte-ci qu'on distribue, pas une copie
        # cherchee par nom. A defaut de joueur Luke Cage a la table, la carte
        # revient au joueur vise par l'activation en cours.
        this = effect.this.CastTo(Minion)
        cible = None
        for player in Worlds.GetPlayers(effect):
            identity = player.GetIdentity()
            if identity and (identity.IsName('Luke Cage') or identity.IsSubName('Luke Cage')):
                cible = player
                break
        if cible is None:
            cible = message.GetToPlayer()
        if cible:
            cible.DealEncounterCard(this, effect)
    return [
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", None, attack_twice_more)
        .LimitOncePerPhase(),
        AbilityFactory.WhenBoostCardTurnedFaceUp(AbilityType.Boost, None, boost_ability),
    ]
