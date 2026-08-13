from . import *

# * The Hypernova

def GetAbilities() -> Sequence['Ability']:

    def apres_activation(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Attachment)

        # « After attached enemy activates, discard X cards from the top of the
        # encounter deck, where X is the amount of threat here. If an
        # acceleration token was placed this way, discard this card. »
        nombre = this.GetTokens('threat')
        if nombre <= 0:
            return
        defaussees = Worlds.DiscardEncounterCards(nombre, effect)
        if any(x.acceleration_icon > 0 for x in defaussees):
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            "AttachedTo",
            apres_activation
        ),
    ]
