from . import *

# * Inhibitor Mask — AMELIORATION de campagne (Basic / Campaign, n° 284). Cout 1. ITEM. Temporary.
# Attach to a SKRULL enemy.
# Temporary.
# Treat attached enemy's printed text box as if it were blank.
#
# Cartes de reference :
#  - **`magneto/49007`** Wrapped in Metal : meme montage ligne a ligne, `CanPlayThisUpgradeCard(...)` +
#    `GiveKeywordToAttached("Character", treat_as_blank=True)` (le texte imprime est ignore, les TRAITS restent).
#  - **fiche `temporary.md`** : « Temporary » est lu dans `desc` (`HasTemporary`) ; la defausse de fin de round
#    est faite par `ProcessTemporary` (world_action.py), y compris sur une amelioration attachee a un ennemi
#    (`33005` Exploit Weakness) : aucun script pour le mot-cle.
#
# ⚠ Mots-pieges :
#  - « a SKRULL ENEMY » : sbire OU mechant SKRULL (un mechant SKRULL de la campagne : Paibok, Super-Skrull...) ;
#  - « printed text box as if it were blank » : les capacites imprimees de l'ennemi sont eteintes, ses traits,
#    ses PV, son ATQ/MNG et ses icones restent ;
#  - « TEMPORARY » : la carte est defaussee a la FIN DU ROUND (et le texte redevient actif).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy, trait="SKRULL")),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            treat_as_blank=True,
        ),
    ]
