from . import *

# Tough Nut — EVENEMENT 1 [physical], Taijutsu (TMNT Shinobi, Inkwire). SKILL.
# Hero Response: After your hero uses a basic power, give it a tough status card. If you paid for this card with a
#   DEFENSE or THWART event, heal 2 damage from your hero.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md).
#
# Cartes de reference :
#  - « After your hero uses a basic power » : `27037` Power Within (`AfterUnitUseBasicPower(HeroResponse, "YourHero", op)`)
#    en version evenement (`.SetPlay().SetLabel()`, `41015` Upside the Head) ;
#  - « give X a tough status card » : `19001a` / `tmnt_aspect_dual/ud006` (`Faces.GiveStatus([heros], "Tough", effect)`) ;
#  - « if you paid for this card with a DEFENSE or THWART event » : `jennika/tj004` (`PayeAvecUnEvenement(effect, "DEFENSE",
#    "THWART")` : l'un OU l'autre) ; « heal N damage from your hero » : `tmnt_aspect_protection` (`this.HealthUnits([unite], 2, effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « After your HERO uses a basic power » : ATK, THW ou DEF du heros (pas un allie, pas un evenement) ; « give IT a
#    tough » : le heros.
#  ⚠ Le soin est une phrase SEPAREE : il a lieu meme si le heros avait deja une carte Tough ; seulement si le paiement
#    contient un evenement DEFENSE ou THWART (un evenement ATTACK ne compte pas).
#  ⚠ « heal 2 damage from YOUR hero » : le heros, au plus 2.


def GetAbilities() -> Sequence['Ability']:

    def tough_nut(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        heros = joueur.GetHero()
        Faces.GiveStatus([heros], "Tough", effect)
        if PayeAvecUnEvenement(effect, "DEFENSE", "THWART"):
            this.HealthUnits([heros], 2, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "YourHero",
            tough_nut,
        ).SetPlay().SetLabel(),
    ]
