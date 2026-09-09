from . import *

# First Contact — AMELIORATION, cout 2, RES [wild]. SYMBIOTE.
# Play under any players control. Max 1 per player.
# Your hero gets +1 ATK, +1 THW, and +1 DEF.
#
# CARTES DE REFERENCE
#  - `01057` Combat Training (+1 ATQ), `01065` Heroic Intuition (+1 CTR) et
#    `01081` Armored Vest (+1 DEF), les trois ameliorations basiques du Set de
#    base. Elles ont EXACTEMENT ce texte, une caracteristique chacune : cette
#    carte est les trois a la fois. `GiveKeywordToAttached` prend les trois
#    dans le meme appel (`asset.py`), donc une seule capacite.
#
# TEXTE CONTRE CODE
#  ⚠ « Play under ANY players control » -> `CanPlayThisUpgradeCard("Players")`,
#    exactement comme les trois basiques : sans ce parametre la carte ne se
#    poserait que sur soi.
#  ⚠ « Max 1 per player » est dans `cards.json` (`MaxPerUnit: "1"`) : rien a
#    coder.
#
# ⚠ ICONE NON IDENTIFIEE, SANS EFFET SUR LE CODE. Le scan porte sous le texte
# une silhouette de CARTE frappee d'un PLUS. Elle n'est definie NI par
# l'insert du pack (relu le 09/09/2026), NI par la police du moteur
# (`icon.css` ne connait que acceleration, amplify, boost, consequential,
# cost, crisis, energy, hazard, mental, per, physical, unique, wild). Le texte
# imprime se suffit a lui-meme — « Play under any players control. Max 1 per
# player. Your hero gets +1 ATK, +1 THW, and +1 DEF. » — et aucune de ses
# phrases ne depend de l'icone. On porte donc le texte tel qu'il est imprime.
# QUESTION OUVERTE POUR L'AUTEUR, pas un blocage.
def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            attack=1,
            thwart=1,
            defense=1,
        )
    ]
