from . import *

# Kingpin's Influence (side scheme) — 2[per_hero], boost 3, Hazard : base desc.
# When Defeated: The player who defeated this scheme places 3 threat on their
#   nemesis side scheme. If it is not in play, they find it and reveal it.
# Modeles : 60113a (WhenSchemeBeDefeated WhenDefeated), message.GetDefeatingPlayer,
# CardFinder(card_type=EncounterSideScheme, is_nemesis=joueur) (checker.py:304),
# Find.FindAndReveal (fouille la reserve nemesis). Lecture litterale : en jeu ->
# 3 menaces ; sinon -> trouvee et revelee (sa menace de depart), sans les 3.

def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        joueur = message.GetDefeatingPlayer()
        finder = CardFinder(card_type=EncounterSideScheme, is_nemesis=joueur)
        complot = Worlds.FindCardOnField(effect, finder=finder)
        if complot is not None:
            this.PlaceThreatOnSchemes([complot], 3, effect)
        else:
            Find.FindAndReveal(effect, joueur, finder=finder)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
