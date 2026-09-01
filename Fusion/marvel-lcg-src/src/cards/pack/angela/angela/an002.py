from . import *

# * Sera — allie signature. HEVEN. Cout 3 / PV 2 / THW 1 / ATK 2*
# Angela gets +1 hand size.
#
# Carte de reference : 06007 * Asgard (pack rainy), meme montage
# `GiveKeywordToInPlayWhenApplyThis(..., control_by="You", hand_size=1)`.
#
# ⚠ CORRECTIF 01/09/2026 — LA CIBLE N'EST PAS LA MEME QUE LE MODELE. Asgard
# dit « **You** get +1 hand size » : « you », c'est l'identite, donc les DEUX
# faces, d'ou son `Identity`. Sera dit « **Angela** gets +1 hand size », et
# « Angela » est le nom de la seule face HEROS (an001a) — l'alter-ego
# s'appelle « Aldrif Odinsdottir » (an001b). Le bonus ne vaut donc qu'en forme
# de heros, et la cible est `Hero`, pas `Identity`.
# Signale par l'utilisateur en partie reelle : il gagnait la carte
# supplementaire en alter-ego, ou la main est deja de 6.
# C'est le mot-piege « that <nom> » de PROCESSUS-CARTE etape 5 : verifier que
# le nom cite designe bien la carte qu'on croit.
#
# 05023 Endurance (`GiveKeywordToAttached`) ne conviendrait PAS : Sera est un
# ALLIE, elle ne s'attache a rien. Et `GiveKeywordToUnits` n'existe pas dans
# le moteur, malgre ce que son nom laisserait esperer.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            hand_size=1,
        ),
    ]
