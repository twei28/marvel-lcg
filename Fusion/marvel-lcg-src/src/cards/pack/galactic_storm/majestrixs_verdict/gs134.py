from . import *

# Tortured Prisoners — MANIGANCE ANNEXE (Majestrix's Verdict), menace de depart 1[per_hero]. Crisis. 2 icones de boost.
# When Revealed: Place 1 additional threat here for each STARJAMMER ally tucked under Imprisoned on Chandilar.
#
# Cartes de reference :
#  - Crisis : BASE AUTOMATIQUE (`desc.Crisis`) ; icone comparee par decoupe a sk115 Hijacked (« ! » explose).
#  - « Place 1 additional threat here for each ... » : `WhenThisRevealed(None)` + `PlaceThreatOnSchemes([this], n)`
#    (modele sk156 Galactic Ambassador / sk168, meme auteur).
#
# ⚠ Mots-pieges : « for each STARJAMMER ally TUCKED under Imprisoned » (pas ceux en jeu) ; « additional » =
# en plus de la menace de depart.


def GetAbilities() -> Sequence['Ability']:

    def torturer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        n = len(GlissesSousLaPrison(effect))
        if n:
            effect.this.PlaceThreatOnSchemes([effect.this], n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, torturer),
    ]
