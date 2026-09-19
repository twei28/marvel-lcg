from . import *

# * Bullseye (II) — SCH 1 / ATK 2 / 16[per_hero]
# When Revealed: Find Adamantium-Laced Spine and attach it to Bullseye.
# « Find » fouille toutes les zones (mise de cote, deck, defausse) :
# Find.FindAndAttachTo (find.py:74).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Find.FindAndAttachTo(effect, this, who_perform=message.GetToPlayer(), name="Adamantium-Laced Spine", card_type=Attachment)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeBullseye(),
    ]
