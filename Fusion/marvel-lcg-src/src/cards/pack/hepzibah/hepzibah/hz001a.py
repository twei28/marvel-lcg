from . import *
# * Hepzibah, face heros. Prefixe `hz`.
#
# Response: After you play an event, resolve the "Special" ability on a card in your hand.
#
# Carte de reference : zeus/ze002 Hera (choisir une carte EN MAIN qui IMPRIME un Special, puis le resoudre : `APrintedSpecial` /
# `ResoudreLeSpecialDe`) ; declencheur 56033 Hulk Shape (`AfterPlayerPlayedCard(.., Event, ..)`).
# ⚠ Le filtre « au moins une carte avec un Special en main » va dans `conditions` : une Response est PROPOSEE avant que le corps
# ne tourne (RECETTES-MOTEUR §1).
def GetAbilities() -> Sequence['Ability']:
    def hepzibah(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        ResoudreUnSpecialEnMain(effect.GetInitiator(), effect)
    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            Event,
            hepzibah,
            conditions=[UnSpecialEnMain],
        ),
    ]
