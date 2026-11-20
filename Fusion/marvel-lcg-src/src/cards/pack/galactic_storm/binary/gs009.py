from . import *

# Body in Flames — AMELIORATION, cout 2, [physical]. CONDITION. SUPERPOWER. Binary 12/15.
# While the number of [energy] resources in your hand is equal to:
#  • 1 or 2 - Binary gains retaliate 1.
#  • 3 or 4 - Binary gains retaliate 2.
#  • 5 or more - Binary gains retaliate 3.
#
# Cartes de reference :
#  - **`iron_fist/64009`** Embody the Dragon : « <NOM> gains retaliate X, X
#    dynamique » = `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You",
#    retaliate=1, get_new_value=fn, change_on_event=...)` (fiche
#    `mots-cles/retaliate.md`, « Retaliate X a valeur dynamique »).
#  - rafraichi quand la main change : `OnEvent.HandCards` (`27154`), et quand
#    Energy Conversion entre ou sort (`RecalculEnergie`, binary/__init__.py).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « BINARY gains » : le NOM de la face heros, donc `Hero` et jamais
#    `"You"` : Carol Danvers ne riposte pas (contre-cas alter ego, RECETTES §3).
#  - paliers « equal to 1 OR 2 / 3 OR 4 / 5 OR MORE » : 0 -> rien ; 1, 2 -> 1 ;
#    3, 4 -> 2 ; 5 et plus -> 3. Pas de cumul entre paliers.
#  - « [energy] resources in your hand » : icones, apres Energy Conversion,
#    wild exclu (Q3). Helper `EnergieEnMain`.
#  - Amelioration sans « Attach to » : elle entre en jeu chez son proprietaire
#    (`CanPlayThisUpgradeCard()` sans cible, comme 64009).


def Palier(n: int) -> int:
    if n >= 5:
        return 3
    if n >= 3:
        return 2
    if n >= 1:
        return 1
    return 0


def GetAbilities() -> Sequence['Ability']:

    def riposte(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        return Palier(EnergieDuJoueur(effect))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            retaliate=1,
            get_new_value=riposte,
            change_on_event=RecalculEnergie(),
        ),
    ]
