from . import *

# * Ana Kraven — custom « Kajislav », minion nemesis
# [star] Forced Response: After Ana Kraven attacks you, place 1 threat on The
#   Grim Hunt side scheme. If The Grim Hunt is not in play, place 1 threat on
#   the main scheme.

def GetAbilities() -> Sequence['Ability']:

    def ana_kraven(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)

        chasse = Worlds.FindCardOnField(
            effect,
            name="The Grim Hunt",
            card_type=EncounterSideScheme
        )
        if chasse:
            this.PlaceThreatOnSchemes([chasse], 1, effect)
        else:
            this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        # (attaquant, attaque) : « After Ana Kraven attacks YOU » vise le joueur
        # engage, pas n'importe quelle identite de la table.
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            "You",
            ana_kraven
        ),
    ]
