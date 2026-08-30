from . import *

# Grim Resolve (2/2) — exemplaire physique 2 de 2, contenu identique a
# ss002 (voir ce fichier pour le detail du modele repris).


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
