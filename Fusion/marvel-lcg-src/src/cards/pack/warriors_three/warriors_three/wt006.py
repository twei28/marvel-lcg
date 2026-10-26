from . import *


def GetAbilities() -> Sequence['Ability']:
    def hildegarde(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        joueur = effect.this.GetControlByPlayer()
        if joueur is None:
            return
        # « all WARRIORS THREE get +1 ATK and +1 THW until the end of the phase » : l'identite (le gain suit les changements
        # de heros : `ignore_flip=True`) et chaque allie WARRIORS THREE (Hildegarde elle-meme comprise).
        identite = joueur.GetIdentity()
        if identite is not None and Hero.IsType(identite):
            identite.GainUntilPhaseEnd(effect, attack=1, thwart=1)
        for allie in joueur.allies.Get():
            if allie.HasTrait("WARRIORS THREE"):
                allie.GainUntilPhaseEnd(effect, attack=1, thwart=1)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", hildegarde),
    ]
