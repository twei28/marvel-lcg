from . import *

# * Rescue

def GetAbilities() -> Sequence['Ability']:

    def rapid_responder(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)

        player = effect.GetInitiator()

        # « make a basic thwart or attack without exhausting Rescue » : la DEF
        # vient d'epuiser le heros ; on le prepare, on lui offre le pouvoir via
        # l'API officielle (qui epuise en l'utilisant), et il finit epuise —
        # exactement l'etat qu'exige la carte.
        Faces.ReadyAll([this], effect)
        player.MakeBasicPowerLikeInTurn(
            [this],
            effect,
            ["THW", "ATK"],
        )

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            rapid_responder,
            # LISTE obligatoire : une chaine serait iteree lettre par lettre
            # dans CheckBasicPower et ne matcherait jamais.
            powers=["DEF"]
        ).SetName("Rapid Responder"),
    ]
