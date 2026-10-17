from . import *

# * Sally Pride — ALLIE 3 [physical], aspect Justice (TMNT Aspects, Inkwire). LION. MUTANIMAL.
# PV 2, THW 2 (1 degat consecutif), ATK 2 (1 degat consecutif).
# [star] Response: After Sally Pride attacks or thwarts, remove 2 threat from a scheme.
#
# Le [star] (et les etoiles a cote des valeurs) : icone de rappel des Rules Reference, aucune ligne de code.
#
# CARTES DE REFERENCE
#  - `27046` Agent 13 : « After <allie> attacks or thwarts » = `AfterUnitAttackOrThwart(Response, "This", op)`.
#  - `04049` Clear the Area : « remove 2 threat from a scheme » = `SetTarget(Scheme2)` +
#    `RemoveThreatFromSchemes(effect.targets, 2, effect)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « After SALLY PRIDE attacks OR thwarts » : ses deux pouvoirs (ATK et THW), elle seule.
#  ⚠ « a scheme » : principale ou annexe, au choix (pas forcement celle qu'elle vient de contrer).
#  ⚠ Aucune limite imprimee : une fois par attaque ou contre.


def GetAbilities() -> Sequence['Ability']:

    def sally(effect: 'Effect', message: 'Message.AfterUnitAttackEnd|Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterUnitAttackOrThwart(
            AbilityType.Response,
            "This",
            sally,
        ).SetTarget(Scheme2),
    ]
