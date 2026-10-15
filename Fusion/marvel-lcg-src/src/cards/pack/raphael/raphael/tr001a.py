from . import *

# * Raphael (face heros) — NINJA. TURTLE. PV 14, ATQ 3, CTR 1, DEF 2, main 4.
# Each rage counter on Raphael can be spent as if it were a [physical] resource.
# Yaban Hito — Response: After Raphael takes any amount of damage from an
#   attack, place 1 rage counter on him (to a maximum of 3).
#
# PHASE A : construit, jamais execute.
#
# CARTES DE REFERENCE
#  - `30001a` * Spider-Ham : MEME montage mot pour mot. Compteur `toon` depense
#    comme ressource wild (`CanGenerateResources(HeroResource, Resources("G"))`
#    + `CostFunc.Counter("This", 1, 'toon')` + `SetToAvailableTimesFn`) et
#    Reponse `AfterUnitTookDamage(Response, "This", ...)`. Ici la couleur est
#    « R » (physique) et le compteur `rage`.
#
# TEXTE CONTRE CODE
#  ⚠ « as if it were a [PHYSICAL] resource » -> `Resources("R")`, pas "G" :
#    contrairement a Spider-Ham, la rage ne vaut PAS une ressource wild.
#    Icone relevee sur le scan : poing, comme la ressource physique des cartes
#    du pack (fiche : RECETTES §8, « poing rouge = R »).
#  ⚠ « from an ATTACK » -> `is_from_attack=True`. Spider-Ham, lui, repond a
#    tout degat. Les degats d'une Sai (`tr011`) ou de Casey Jones (`tr002`) ne
#    sont PAS une attaque : ils ne declenchent pas Yaban Hito, d'ou l'encart de
#    regles qui demande de poser la rage a la main pour les Sai.
#  ⚠ « takes ANY AMOUNT of damage » : le message `AfterUnitTookDamage` ne part
#    qu'apres des degats effectifs ; zero degat (Tough, prevention) ne rend rien.
#  « (to a maximum of 3) » -> `maximum=3` de `PlaceCountersOn`.
#  « on HIM » : la face heros elle-meme (`this`).
#  Le `[star]` n'est PAS imprime sur cette face : capacite ordinaire, pas
#  NonKeywordStar.


def GetAbilities() -> Sequence['Ability']:

    def yaban_hito(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, RAGE, effect, maximum=PLAFOND_RAGE)

    def rage_disponible(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> int:
        this = effect.this.CastTo(Hero)
        Unused(message)
        return this.GetCounters(RAGE)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("R"),
        ).SetCostFunc(CostFunc.Counter("This", 1, RAGE))
        .SetToAvailableTimesFn(rage_disponible),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "This",
            yaban_hito,
            is_from_attack=True,
        ).SetName("Yaban Hito"),
    ]
