from . import *

# Vampire — SBIRE nemesis (N 3/8 et 4/8). VAMPIRE. 6 PV, SCH 2, ATQ 2, 2 boost.
# Attacks with piercing deal double damage to Vampire.
# [star] Forced Response: After Vampire attacks and damages a character, heal
#   all damage from Vampire. If no damage was healed this way, give Vampire a
#   tough status card.
#
# CARTES DE REFERENCE
#  - `39051` Vampire (Mojo, set Horror) : COPIE EXACTE, meme nom, memes
#    chiffres, meme texte. `CapacitesDeVampire()`.
#
# TEXTE CONTRE CODE
#  ⚠ Homonyme : « Vampire » est aussi 39051. Aucune carte du pack ne cherche par
#    ce nom ; On the Hunt lit le TRAIT.
#  ⚠ Une attaque percante de 4 (Go for the Heart) le tue net (4 x 2 = 8 > 6) ;
#    une attaque de 2 sans percant laisse 4 PV, qu'il soigne a sa prochaine
#    attaque reussie.


def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDeVampire(),
    ]
