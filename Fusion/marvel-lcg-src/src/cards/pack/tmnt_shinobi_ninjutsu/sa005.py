from . import *

# Run the Rooftops — EVENEMENT 0 [energy], Ninjutsu (TMNT Shinobi, Inkwire). NYC. THWART.
# Play only if your hero is cloaked.
# Hero Action (thwart): Remove 2 threat from a scheme.
# « We are the unseen guardians of the city. » —Donatello
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloaked (cloaked.md).
#
# Cartes de reference :
#  - `10019` To the Rescue! : MEME effet (« Hero Action (thwart): Remove 2 threat from a scheme ») =
#    `this.RemoveThreatFromSchemes(effect.targets, 2, effect)` + `.SetPlay().SetLabel('thwart').SetTarget(Scheme2)` ;
#  - `ub033` / `JouableSiVousControlez` : condition de jeu posee en tete des conditions.
#
# TEXTE CONTRE CODE
#  ⚠ « Play only if your HERO is cloaked » : forme heros ET Cloaked (`HerosCamoufle`) ; la carte Cloaked reste.
#  ⚠ « 2 threat from A scheme » : un seul complot, n'importe lequel (principal, annexe, d'un autre joueur) ; 2 exactement
#    (moins s'il en reste moins).


def GetAbilities() -> Sequence['Ability']:

    def run_the_rooftops(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

    return [
        JouableSiHerosCamoufle(
            AbilityFactory.WhenInYourPlayTurn(
                AbilityType.HeroAction,
                run_the_rooftops,
            ).SetPlay().SetLabel('thwart')
            .SetTarget(Scheme2)
        ),
    ]
