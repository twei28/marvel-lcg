from . import *

# Alongside — Permanent (base).
# When Revealed: Each player takes 1 indirect damage. The villain takes
#   2[per_hero] damage.
# La face apparait par retournement (RetournerLAttachement, call_reveal) : le
# When Revealed se resout alors (FAQ du livret sur Bloody Mary (B)).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        def un_indirect(player: 'Player') -> None:
            player.GetIdentity().TakeIndirectDamage(this, 1, effect)

        Players.ForEachPlayer(effect, un_indirect)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            this.DealDamage([vilain], 2 * Worlds.GetPlayerNumIcon(effect), effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
