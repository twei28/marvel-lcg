from . import *

# * Anthony Druid (face alter-ego) — MYSTIC. REC 2, main 6, PV 9.
# Psychiatric Care - Interrupt: When a friendly character makes a basic
#   recovery, they get +X REC, where X is equal to Anthony Druid's REC.
#
# CARTES DE REFERENCE
#  - `aa003` (Agatha Harkness) et `al011` (Alligator Loki), tous deux sur
#    `GiveKeywordToInPlayWhenApplyThis(..., recover=)`.
#
# TEXTE CONTRE CODE
#  « a friendly CHARACTER » -> `Friend` + `control_by="You"` : les ALLIES sont
#    inclus, pas seulement l'identite. Sans REC imprimee ils n'en profitent
#    pas, mais le filtre suit le texte.
#
# ⚠ ECART ASSUME, ET SA RAISON. Le texte dit « Interrupt: when ... makes a
# basic recovery ». On code un BONUS PERMANENT tant qu'Anthony Druid est en
# jeu. L'effet observable est le meme — la REC ne sert QUE lors d'une
# recuperation — et le montage evite une fenetre d'interruption fragile.
#
# ⚠ ET SURTOUT : X est lu sur la REC **IMPRIMEE** (`printed_recovery`), pas
# sur la REC courante. Lire la REC courante ferait boucler la carte sur
# elle-meme : Anthony a REC 2, le bonus la porte a 4, qui redonnerait +4,
# donc 8... Le texte suppose un X fige au moment ou il se lit ; l'imprime est
# la seule valeur qui ne se mord pas la queue.


def GetAbilities() -> Sequence['Ability']:

    def rec_d_anthony(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        this = effect.this
        return int(getattr(this, "printed_recovery", 0) or 0)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Friend,
            control_by="You",
            get_new_value=rec_d_anthony,
            recover=1,
        ),
    ]
