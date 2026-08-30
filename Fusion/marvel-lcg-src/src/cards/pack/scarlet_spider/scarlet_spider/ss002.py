from . import *

# Grim Resolve (1/2) — CONDITION
# Action: Choose a basic power, you get +1 to that power until the end of
#   the round for each different resource spent on this card. Then, ready
#   your identity.
#
# "for each different resource spent on this card" : modele 47009 Grande
# Finale, `effect.GetPaidResources().GetResourceIconTypes()` (nombre de
# TYPES de ressource distincts utilises pour payer le cout de CETTE carte,
# pas leur total). "Choose a basic power" : `initiator.AskChooseOneText`
# (modele determination/dt070.py Munitions Cache) sur les 4 libelles
# ATK/THW/DEF/REC, mappes sur les kwargs de `TemporaryGain`
# (attack/thwart/defense/recover, meme signature que ok001a.py). "until the
# end of the round" : `end_event=Message.WhenRoundEnd` (modele brawn/bw015.py
# Hulk Out, meme TemporaryGain). "Ready your identity" : `Faces.ReadyAll`
# (modele il015.py Iron Lad's Suit, `ReadyAll([initiator.GetIdentity()],
# effect)`).


def GetAbilities() -> Sequence['Ability']:

    def grim_resolve(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        identity = initiator.GetIdentity()
        power = initiator.AskChooseOneText(["ATK", "THW", "DEF", "REC"])
        value = effect.GetPaidResources().GetResourceIconTypes()

        kwargs: Dict[str, int] = {}
        if power == "ATK":
            kwargs["attack"] = value
        elif power == "THW":
            kwargs["thwart"] = value
        elif power == "DEF":
            kwargs["defense"] = value
        elif power == "REC":
            kwargs["recover"] = value

        identity.TemporaryGain(effect, None, Message.WhenRoundEnd, **kwargs)
        Faces.ReadyAll([identity], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            grim_resolve,
        ).SetPlay()
        .SetName("Grim Resolve"),
    ]
