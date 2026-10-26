from . import *
# * Cannonball (Sam Guthrie), allie. Cout 3, PV 3, ATQ 2**, CTR 2**, [wild]. AERIAL. X-MEN.
#
# Cannonball has toughness if your identity has the AERIAL trait.
# Response: After you play an AERIAL card, give Cannonball a tough status card.
#
# Cartes de reference : 49035 Bling! (« gains toughness » conditionnel : `ThisGainKeyword(.., toughness=1, change_on_event=OnEvent.Trait("YourIdentity"))`) ;
# 01017 Cosmic Flight (donne le trait AERIAL a l'identite) ; `AfterPlayerPlayedCard(Response, "You", CardFinder(trait=..), op)`.
# ⚠ « an AERIAL card » = tout type (evenement Power Couple, amelioration Exo-Flight, allie) : filtre par TRAIT seul.
def GetAbilities() -> Sequence['Ability']:
    def cannonball(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus([this], "Tough", effect)
    return [
        AbilityFactory.ThisGainKeyword(
            IdentiteAerienneUI,
            toughness=1,
            change_on_event=OnEvent.Trait("YourIdentity"),
        ),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait=TRAIT_AERIAL),
            cannonball,
        ),
    ]
