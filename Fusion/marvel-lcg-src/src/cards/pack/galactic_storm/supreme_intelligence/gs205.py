from . import *

# Loyalty to Supremor — COMPLOT ANNEXE (Supreme Intelligence). Menace 3[per_hero], icone d'ACCELERATION,
# 1 icone de boost.
# Each minion gains guard.
#
# Cartes de reference : **`cw/56111`** S.H.I.E.L.D. Patrol (meme phrase) :
# `*GiveKeywordToInPlayWhenApplyThis(Minion, guard=1)`. Acceleration : base AUTOMATIQUE (`desc.Acceleration`).
#
# ⚠ Mots-pieges : « EACH minion » (tous les sbires en jeu, pas seulement KREE, et ceux qui entrent ensuite) ;
# l'effet tombe quand le complot est dejoue.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Minion, guard=1),
    ]
