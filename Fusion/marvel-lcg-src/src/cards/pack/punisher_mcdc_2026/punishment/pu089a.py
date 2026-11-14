from . import *

# Escaping Punishment (2A) — MANIGANCE PRINCIPALE.
# When Revealed : Find and reveal Punisher's Assault Rifle. Flip Target Lock to its DISTRACTED side.
#
# Cartes de reference : pu088b (`Find.FindAndReveal`), `RetournerTargetLockVersDistracted` (__init__.py).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(effect, message.GetToPlayer() or Worlds.GetFirstPlayer(effect), name="Punisher's Assault Rifle", card_type=Attachment)
        RetournerTargetLockVersDistracted(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
