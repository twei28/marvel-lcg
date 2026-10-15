from . import *

# * Emperor Dorrek-Vell — amelioration signature (14/16). KREE. SKRULL. TITLE.
# Cout 2 [mental].
# While you have the [[KREE]] trait, each ally you control gets +1 ATK.
# While you have the [[SKRULL]] trait, each ally you control gets +1 THW.
#
# Cartes de reference :
#  - **`as012`** Night Vision (pack armored_spidey, meme auteur) :
#    `GiveKeywordToInPlayWhenApplyThis(finder, control_by="You", thwart=1,
#    condition=..., change_on_event=...)` — un bonus CONTINU et CONDITIONNEL
#    sur des cartes en jeu, recalcule a chaque changement d'etat.
#  - `sk003` Wiccan (meme set) : la meme paire KREE->ATK / SKRULL->THW sur un
#    seul allie, et `RECALCUL_TRAITS`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « While **you** have » : le trait de l'IDENTITE (forme heros : l'origine
#    le donne ; forme civile : rien).
#  - « **each ally you control** » : `card_type=Ally` + `control_by="You"`,
#    pas les allies des autres joueurs.
#  - KREE -> ATK, SKRULL -> THW, ne pas croiser ; les deux avec Ancestors.
#  - TITLE : trait purement declaratif ici.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Ally),
            control_by="You",
            attack=1,
            condition=lambda effect: IdentiteATrait(effect, "KREE"),
            change_on_event=RECALCUL_TRAITS,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Ally),
            control_by="You",
            thwart=1,
            condition=lambda effect: IdentiteATrait(effect, "SKRULL"),
            change_on_event=RECALCUL_TRAITS,
        ),
    ]
