from . import *

# Sensory Overload — TRAITRISE du set « Venomized Weakness » (2/2).
# Weakness. (Begins the game in your deck and is discarded into your discard
#   pile.)
# Forced Response: After this card enters your hand, place 1 threat on each
#   scheme. (You may discard this card from your hand at the end of the player
#   phase like any other card.)
#
# MOT-CLE
#  - `weakness` : voir `docs/reference/mots-cles/weakness.md` et l'en-tete de
#    `vz036`, sa jumelle. Rien du mot-cle ne se code : c'est une regle de
#    construction de deck plus le comportement natif d'une carte en main.
#
# CARTES DE REFERENCE
#  - `vz036` Flash Fire, sa jumelle : meme declencheur, meme montage.
#  - `determination/__init__.py`, helper `Reckless` :
#    `this.PlaceThreatOnSchemes("EachScheme", 1, effect)` — la meme phrase
#    (« place 1 threat on each scheme »), deja portee au depot.
#
# TEXTE CONTRE CODE
#  ⚠ « EACH scheme » : le complot principal ET toutes les manigances annexes,
#    y compris les manigances-joueur. `"EachScheme"` est exactement cela.
#  ⚠ Voir vz036 pour `which_card="This"`, qui pose `CanWorkOnlyInHand()` seul,
#    et pour la parenthese finale, qui ne se code pas.
def GetAbilities() -> Sequence['Ability']:

    def sensory_overload(effect: 'Effect', message: 'Message.AfterCardEnterHand') -> None:
        this = effect.this
        Unused(message)

        this.PlaceThreatOnSchemes("EachScheme", 1, effect)

    return [
        AbilityFactory.AfterCardEnterHand(
            AbilityType.ForcedResponse,
            "This",
            sensory_overload,
        ),
    ]
