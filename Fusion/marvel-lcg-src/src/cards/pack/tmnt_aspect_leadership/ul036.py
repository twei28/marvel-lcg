from . import *

# * Turtle Titan « Mikey » — ALLIE Leadership (TMNT Aspects, Inkwire), cout 4, [physical]. HERO. NINJA.
# TURTLE. THW 1[star]* / ATQ 2* / PV 3.
# [star] Response: After Turtle Titan thwarts a scheme, heal 2 damage from him.
#
# Le [star] a cote du THW et devant la Reponse est l'icone de rappel (fiche special.md) : aucune ligne de
# code, seule la Reponse compte.
#
# CARTES DE REFERENCE
#  - `ta002` Nobody : « After X thwarts » = `AfterUnitThwartEnd(Response, "This", op)`.
#  - `45015` Sidekick : « heal 2 damage from <allie> » = `this.HealthUnits([cible], 2, effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « heal 2 damage from HIM » : Turtle Titan lui-meme (y compris le degat consecutif du contre).
#  ⚠ Response facultative ; aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def turtle_titan(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.HealthUnits([this], 2, effect)

    return [
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.Response,
            "This",
            turtle_titan,
        ),
    ]
