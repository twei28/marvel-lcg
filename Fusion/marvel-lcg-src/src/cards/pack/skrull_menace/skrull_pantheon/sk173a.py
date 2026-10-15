from . import *
from cards.pack.skrull_menace.campaign import CampaignSetup

# Protect the Pantheon 1A (173A) — complot principal, face A (mise en place).
# Contents: Kly'bn I and Kly'bn II (Kly'bn II and Kly'bn III for expert mode). Skrull Pantheon, Dard'van Sect,
#   Skrull Society and Standard sets.
# La face A n'a aucune capacite imprimee : ce module n'existait pas (« Contents » et « Setup » sont portes par
# le scenario). Il n'existe que pour appeler `CampaignSetup(4)` : en mode campagne, la mise en place,
# la regle de cooperation et le releve du carnet sont attaches a la manigance principale 1A du scenario
# (modele `gmw/brotherhood_of_badoon/16061a`). Hors campagne, `CampaignSetup` ne fait rien (chaque capacite
# est gardee par `Worlds.IsCampaign`), donc aucune partie ordinaire ne change.


def GetAbilities() -> Sequence['Ability']:
    return [
        *CampaignSetup(4),
    ]
