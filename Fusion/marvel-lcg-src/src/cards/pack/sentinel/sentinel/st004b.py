from . import *

# * Torso (Destroyed) — COMPONENT. DESTROYED. TECH.
# Permanent.
# Your upgrades cost 1 additional resource.
#
# Carte de reference : `39062` Growing Pains, meme montage a la valeur pres,
# mais posee sur le helper du pack (voir ci-dessous).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « your **upgrades** » : le filtre est un TYPE de carte, pas un trait. La
#    fabrique du moteur saurait donc le rendre telle quelle... mais elle ne
#    verifie PAS quelle face est visible, et son malus s'appliquait avec Torso
#    encore INTACTE (voir le commentaire de `VosCartesCoutentUnDePlus`). On
#    passe donc par le helper du pack, comme st002b et st003b.
#  - Le surcout frappe AUSSI les autres Component qu'on rejouerait... mais
#    aucun ne se joue depuis la main : ils arrivent au setup. Aucun effet de
#    bord, verifie.


def GetAbilities() -> Sequence['Ability']:
    return [
        VosCartesCoutentUnDePlus(card_type=Upgrade),
    ]
