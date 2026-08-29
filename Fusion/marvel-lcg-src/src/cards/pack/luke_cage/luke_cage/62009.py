from . import *

# Cruisin' for a Bruisin'
# Attach to a minion. Max 1 per minion.
# Attacks against attached minion deal 2 additional damage and gain overkill.
# Response: After you play this card, engage attached minion.

def GetAbilities() -> Sequence['Ability']:

    def engager(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        cible = this.bind_face
        player = effect.GetInitiator()
        if cible is None or player is None:
            return
        if Minion.IsType(cible):
            cible.CastTo(Minion).EngagePlayer(player, effect)

    return [
        *AbilityFactory.UnitGetATKWhileAttacking(AbilityType.NonKeyword, None, "AttachedCharacter", 2),
        AbilityFactory.UnitAttackGainKeyword(None, "AttachedCharacter", overkill=True),
        # Clause qui manquait : le sbire attache s'engage avec vous.
        AbilityFactory.AfterYouPlayThisFromHand(AbilityType.Response, engager),
    ]
