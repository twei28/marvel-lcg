from . import *

# * Deathless Persistence — pacte BARGAIN (Corruptive Offers). Boost 3, Peril (natifs). Communs : `AbilitesDePacteCorrompu` (When Revealed + set-aside libre).
# Interrupt : When a character you control would be defeated, place 1 corrupt counter here -> heal 1 damage from that character instead.
#
# Cartes de reference : defeated.py `WhenUnitWouldBeDefeated` (+ `SetBeInstead`), mp016 (compteurs). 
# ⚠ Mots-pieges : « a character YOU CONTROL » : identite, allies du porteur ; « INSTEAD » : le personnage n'est pas vaincu, il perd 1 degat ; le compteur est paye
# a la volee (Interruption facultative).


def GetAbilities() -> Sequence['Ability']:
    def les_miens(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        porteur = effect.this.CastTo(Attachment).GetBindFace()
        joueur = porteur.GetControlByPlayer() if porteur is not None else None
        return joueur is not None and message.trigger.GetControlByPlayer() == joueur

    def persiste(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.PlaceCountersOn([this], 1, 'corrupt', effect)
        message.SetBeInstead(effect)
        message.trigger.HealHealth(1, effect)

    return [
        *AbilitesDePacteCorrompu(),
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.Interrupt, Friend, persiste, conditions=[les_miens]),
    ]
