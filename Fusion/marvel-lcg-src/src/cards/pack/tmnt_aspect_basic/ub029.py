from . import *

# * Michelangelo « Mikey » — ALLIE 3 [energy], 1*/1*, 3 PV, aspect Basic (TMNT Aspects). NINJA. TURTLE.
# Response: After Michelangelo enters play, heal 2 damage from a friendly character.
#
# NOUVELLE. Carte de reference : 45048 Triage (« After Triage enters play, heal 2 damage from an X-Men
# character » : `AfterCardEnterPlay(Response, "This")` + `HealthUnits(targets, 2)` + `canbe_heal=True`).
# Difference : n'importe quel personnage AMI (`Friend`), sans trait.
# TEXTE CONTRE CODE : « a FRIENDLY character » (identite ou allie, d'un joueur ; pas un ennemi) ; « 2 ».


def GetAbilities() -> Sequence['Ability']:

    def michelangelo(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.HealthUnits(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            michelangelo
        ).SetTarget(Friend, canbe_heal=True),
    ]
