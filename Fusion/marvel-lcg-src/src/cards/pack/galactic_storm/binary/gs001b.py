from . import *

# * Carol Danvers — face ALTER-EGO (1B). PV 12, REC 4, main 5. ASTRONAUT.
# You must include an equal number of cards with a printed [energy], [mental],
#   and [physical] resource in your deck.
# Exploring Space — Action: Draw 1 card. (Limit once per round.)
#
# Cartes de reference :
#  - **`sk001b`** Teddy Altman / **`64001b`** Danny Rand : Action d'alter-ego
#    limitee une fois, `WhenInYourPlayTurn(Action, op).LimitOncePerRound()`.
#  - `01091` Avengers Mansion pour `joueur.DrawUp(1, effect)`.
#  - La contrainte de construction (« equal number of cards ») n'est PAS une
#    capacite de jeu : le moteur ne valide pas les decks. Elle est declaree dans
#    `deck/starter/binary.json` (`metadata.deckbuilding.ressources_egales`) et
#    jugee par le deck-builder (`public/js/deckbuilder/regles.js`), comme les
#    regles de Fatalis ou d'Ares (GUIDE §5.4).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Action » nue, imprimee sur la face ALTER-EGO : n'existe qu'en forme
#    Carol Danvers (contre-cas en heros).
#  - « (Limit once per ROUND.) » : `LimitOncePerRound()`, temoin d'epuisement.
#  - « cards with a printed ... resource » : des CARTES (pas des icones), le
#    wild ne compte pour aucune couleur ; FAQ du livret p.22 : les cartes de
#    campagne ne comptent pas.


def GetAbilities() -> Sequence['Ability']:

    def explorer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            explorer,
        ).SetName("Exploring Space")
        .LimitOncePerRound(),
    ]
