from . import *

# Iaidō — EVENEMENT SKILL, classe Bushido (Inkwire, TMNT Shinobi). Cout 1, [mental].
# Hero Interrupt: When you use a basic power, you get +2 to that power for this use. You may place 1 samurai counter on an OATH
#   upgrade you control.
# « Pay close attention, I won't show you twice... » —Ronin
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md).
#
# Cartes de reference :
#  - « When you use a basic power, ... get +N to that power for this use » : `wsp/13005` Rapid Growth
#    (`WhenUnitUseBasicPower(HeroInterrupt, "You", op, powers=["ATK", "THW", "DEF"]).SetPlay().SetLabel()` + `message.GainValue(+N,
#    effect)`, qui route seul vers ATQ / CTR / DEF) ;
#  - « you may place 1 samurai counter on an OATH upgrade you control » : `PlacerUnCompteurSamurai(..., optionnel=True)` (helper du pack).
#
# TEXTE CONTRE CODE
#  ⚠ « Hero Interrupt » : forme heros seule, AVANT le calcul du pouvoir (le +2 compte dans le pouvoir lui-meme).
#  ⚠ « When YOU use a basic power » : un pouvoir de base du HEROS (ATQ, CTR ou DEF), pas celui d'un allie ; « +2 to THAT power » : le
#    pouvoir utilise, pas les autres ; « FOR THIS USE » : un seul usage (`GainValue` sur le message, aucune valeur durable).
#  ⚠ « You MAY place 1 samurai counter » : facultatif (refuser laisse le +2) ; 1 compteur sur une OATH SOUS SON CONTROLE choisie.


def GetAbilities() -> Sequence['Ability']:

    def iaido(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.GainValue(+2, effect)
        PlacerUnCompteurSamurai(effect, effect.GetInitiator(), optionnel=True)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "You",
            iaido,
            powers=["ATK", "THW", "DEF"],
        ).SetPlay().SetLabel(),
    ]
