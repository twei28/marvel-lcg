from . import *

# * Herman — ALLIE 2 [physical], aspect Protection (TMNT Aspects, Inkwire). CRAB. MUTANIMAL. SOLDIER.
# THW 1 (2 degats consecutifs), ATK 2 (2), PV 1.
# Toughness. Herman can have up to 3 tough status cards.
# Interrupt: When Herman enters play, place an additional tough status card on him (to a max of 2) for
#   each resource you overpaid for Herman's cost.
#
# NOUVELLE. MOT-CLE (fiche lue AVANT le code) : Toughness (toughness.md) — lu dans `desc`, aucun code ;
# le plafond de cartes Tough est `tough_max` (« GainStatus refuse d'en ajouter au-dela »).
#
# CARTES DE REFERENCE
#  - `12011` Ant-Man : « When X enters play, place ... for each resource you overpaid for X's cost (to a
#    maximum of 4) » = `WhenCardEnterPlay(Interrupt, "This", ...)` + `min(N, message.overpaid)`.
#  - `62001a` Luke Cage / `32001a` Colossus : « can have up to N tough status cards » =
#    `AbilityFactory.ThisCanHaveAdditionalTough(N - 1)`.
#  - `56041` Patriot : `Faces.GiveStatus([this], "Tough", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « up to 3 tough » : 1 de base + 2 supplementaires -> `ThisCanHaveAdditionalTough(2)`.
#  ⚠ « an ADDITIONAL tough ... (to a max of 2) for EACH resource you overpaid » : min(2, surpaiement)
#    cartes EN PLUS de celle de Toughness.
#  ⚠ Interrupt « When Herman enters play » (pas After) : meme fenetre que 12011.


def GetAbilities() -> Sequence['Ability']:

    def herman(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        valeur = min(2, message.overpaid)
        for _ in range(valeur):
            Faces.GiveStatus([this], "Tough", effect)

    return [
        AbilityFactory.ThisCanHaveAdditionalTough(2),
        AbilityFactory.WhenCardEnterPlay(
            AbilityType.Interrupt,
            "This",
            herman,
        ),
    ]
