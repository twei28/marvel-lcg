from . import *

# Scale the Wall — EVENEMENT 0 [energy], Ninjutsu (TMNT Shinobi, Inkwire). Aucun trait.
# Play only if your hero is cloaked. Max 1 per round.
# Hero Action: Draw 2 cards.
# « You must be able to overcome any obstacle. » —Splinter
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloaked (cloaked.md).
#
# Cartes de reference :
#  - `vz014` Scared of the Dark : « Max 1 per round » en tete d'un evenement Hero Action =
#    `.SetPlay()...LimitOncePerRound()` ;
#  - `ub033` / `JouableSiVousControlez` : condition de jeu posee en tete des conditions ;
#  - `DrawUp(N, effect)` : pioche.
#
# TEXTE CONTRE CODE
#  ⚠ « Play only if your HERO is cloaked » : forme heros ET carte Cloaked (`HerosCamoufle`). La carte Cloaked n'est PAS
#    depensee (aucun cout).
#  ⚠ « Max 1 PER ROUND » : limite imprimee (`LimitOncePerRound`), donc temoin d'epuisement (PROCESSUS-CARTE 7 bis) :
#    une seconde copie dans le meme round est refusee.
#  ⚠ « Draw 2 cards » : exactement 2.


def GetAbilities() -> Sequence['Ability']:

    def scale_the_wall(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        effect.GetInitiator().DrawUp(2, effect)

    return [
        JouableSiHerosCamoufle(
            AbilityFactory.WhenInYourPlayTurn(
                AbilityType.HeroAction,
                scale_the_wall,
            ).SetPlay().SetLabel()
            .LimitOncePerRound()
        ),
    ]
