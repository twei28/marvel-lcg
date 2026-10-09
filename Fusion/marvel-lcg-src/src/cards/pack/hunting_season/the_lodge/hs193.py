from . import *

# hs193 Hunterbot (Experience Cost 3)
# Max 1 per player (donnees). Ton heros gagne +1 ATK.
# Forced Interrupt : quand tu subirais des degats, place-les ici a la place ;
# puis, s'il y a 3 degats ou plus ici, defausse Hunterbot.

def GetAbilities() -> Sequence['Ability']:

    def encaisser(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this
        degats = message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], degats, 'damage', effect)
        if this.GetCounters('damage') >= 3:
            Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", attack=1),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "You", encaisser),
    ]
