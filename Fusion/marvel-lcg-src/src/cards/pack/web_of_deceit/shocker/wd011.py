from . import *

# Grand Larceny

def GetAbilities() -> Sequence['Ability']:

    def sbire_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Faces.RemoveTokensOn([this], 5, 'threat', effect)

    return [
        # « Threat cannot be removed from The Long Night. »
        #
        # `from_where` prend un CardType, pas un nom : le filtre par nom passe
        # donc par une condition, comme le fait le moteur lui-meme quand il
        # veut viser UNE carte (`from_card_name` est commente dans la fabrique).
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            SchemeSide2,
            conditions=[
                lambda effect, message:
                    message.trigger.IsName("The Long Night")
            ],
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            Minion,
            sbire_vaincu,
            conditions=[
                lambda effect, message:
                    message.trigger.HasTrait("CRIMINAL")
            ],
        ).SetLabel('thwart'),
    ]
