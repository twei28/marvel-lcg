from . import *

# * Wiccan (William Kaplan) — allie signature (2/16). AVENGER. Cout 3 [mental].
# THW 2* / ATK 1* (1 degat consecutif chacun), 3 PV.
# While you have the [[KREE]] trait, Wiccan gets +1 ATK.
# While you have the [[SKRULL]] trait, Wiccan gets +1 THW.
#
# Cartes de reference :
#  - **`cn002`** * Belit (pack conan, MEME auteur Kajislav) : « While you have
#    the THIEF or KING trait, Belit gets +1 THW » — meme phrase, meme montage :
#    `ThisGainKeyword(fn, thwart=1, change_on_event=...)`.
#  - `26003` * Vivian : le meme couple de bonus, l'un sur THW l'autre sur ATK,
#    selon la FORME additionnelle de l'identite.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « While **you** have » : l'IDENTITE du controleur de Wiccan, pas Wiccan.
#  - KREE -> **ATK**, SKRULL -> **THW** : ne pas croiser. Avec les deux traits
#    (sk010 Ancestors), les DEUX bonus s'appliquent.
#  - Bonus CONTINU, relu a chaque changement de forme/trait : RECALCUL_TRAITS.
#  - En forme civile, Teddy Altman n'a ni KREE ni SKRULL : aucun bonus.
#  - « 2* / 1* » : degats consecutifs (convention desc, pas un script).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if IdentiteATrait(effect, "KREE") else 0,
            attack=1,
            change_on_event=RECALCUL_TRAITS,
        ),
        AbilityFactory.ThisGainKeyword(
            lambda effect, ui: 1 if IdentiteATrait(effect, "SKRULL") else 0,
            thwart=1,
            change_on_event=RECALCUL_TRAITS,
        ),
    ]
