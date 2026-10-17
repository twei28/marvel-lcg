from . import *

# * Hatamoto (Donnie) — ALLIE 3 [physical], aspect Justice (TMNT Aspects, Inkwire). NINJA. SAMURAI. TURTLE.
# PV 3, THW 1 (1 degat consecutif), ATK 2 (1 degat consecutif).
# Toughness.
# Interrupt: When Hatamoto defends against an attack, remove 1 threat from a scheme.
#
# MOT-CLE (fiche lue AVANT le code) : TOUGHNESS — docs/reference/mots-cles/toughness.md : base native lue
# dans `desc.Toughness` (« 1 »), AUCUN code ici.
#
# CARTES DE REFERENCE
#  - `62012` Iron Fist : « Interrupt: When <allie> defends against an attack » =
#    `WhenUnitDefendAgainstAttack(AbilityType.Interrupt, "This", op)`.
#  - `04049` Clear the Area : « remove N threat from a scheme » = `SetTarget(Scheme2)` +
#    `RemoveThreatFromSchemes(effect.targets, N, effect)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « When HATAMOTO defends » : lui seul, contre n'importe quelle attaque (vilain ou sbire).
#  ⚠ « Interrupt » : AVANT la resolution des degats, optionnel.
#  ⚠ « a scheme » : principale ou annexe.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def hatamoto(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.Interrupt,
            "This",
            hatamoto,
        ).SetTarget(Scheme2),
    ]
