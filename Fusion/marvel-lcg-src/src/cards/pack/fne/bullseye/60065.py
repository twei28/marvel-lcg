from . import *

# * Bullseye (I) — SCH 0 / ATK 1 / 14[per_hero]
# When Revealed: Set aside Adamantium-Laced Spine (68A).
# [star] Forced Interrupt : voir CapacitesDeBullseye.
# La colonne est dans le deck de rencontre (set Bullseye) ; on la met de cote
# pour que le stade II la « Find » (la recherche couvre la mise de cote).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        SetupCards.SetAsideCards(effect, name="Adamantium-Laced Spine", card_type=Attachment)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeBullseye(),
    ]
