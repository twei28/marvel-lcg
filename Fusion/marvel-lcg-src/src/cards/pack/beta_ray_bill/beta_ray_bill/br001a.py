from . import *

# * Beta Ray Bill (face heros) — ASGARD. CYBORG. GUARDIAN.
#   PV 14, CTR 1, ATQ 2, DEF 2, main 4.
# Worthy — Action: Find Stormbreaker and add it to your hand. If it leaves
#   play this way, deal 3 damage to an enemy. (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `04001b` Clint Barton : « search your deck and discard pile for
#    Hawkeye's Bow and add it to your hand », le meme rappel d'arme nommee.
#  - `bk008` Blink's Quiver : ⚠ `Search.PlayerCard` rend UNE FACE OU None
#    (`-> TC|None`, search.py:146), PAS une liste. L'indexer levait
#    « 'Upgrade' object is not subscriptable », que le moteur AVALE.
#
# TEXTE CONTRE CODE
#  « FIND » n'est pas « search your deck » : le mot couvre le deck, la
#    defausse ET LE TERRAIN. C'est toute la carte — rappeler le marteau DEPUIS
#    LE JEU est le cas interessant, puisque c'est le seul qui frappe.
#  « If it LEAVES PLAY this way » -> les 3 degats ne tombent QUE si le marteau
#    etait en jeu. Le rappeler du deck ou de la defausse ne frappe personne.
#    Mot-piege : « this way » restreint au rappel qu'on vient de faire.
#  ⚠ « While it is tucked here, Stormbreaker CANNOT BE FOUND » (br012
#    Unworthy) : une carte glissee sous l'obligation n'est ni en jeu, ni dans
#    le deck, ni en defausse. Les deux chemins ci-dessous la manquent donc
#    NATIVEMENT, sans garde supplementaire. C'est verifie par un cas.
#  « (Limit once per round.) » -> `.LimitOncePerRound()`, et br008 Calm Before
#    the Storm existe precisement pour la contourner.


def GetAbilities() -> Sequence['Ability']:

    def digne(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        # Le corps vit dans le `__init__.py` du set : br008 Calm Before the
        # Storm le rejoue « en ignorant sa limite », et deux copies auraient
        # diverge des la premiere correction.
        ResoudreWorthy(effect, JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            digne,
        ).LimitOncePerRound()
        .SetName("Worthy"),
    ]
