from cards.pack import *

# ===========================================================================
# Pack WOLVERINE X-23 — contenu custom de BlueHG.
#
# Ce set est un RE-SKIN strict de X-23 (pack officiel `x23`, cartes 43001a a
# 43012) : memes couts, memes valeurs, memes textes, memes ressources. Deux
# choses seulement changent sur les cartes imprimees :
#   - le heros s'appelle « Wolverine » au lieu de « X-23 » ;
#   - son trait passe de X-FORCE a X-MEN.
# L'alter-ego reste « Laura Kinney » (trait MUTANT), et l'obligation comme le
# set nemesis ne sont pas fournis par l'auteur : le deck de depart reutilise
# ceux de X-23 (43028 a 43033), qui parlent deja de Laura Kinney et de Honey
# Badger.
#
# ---------------------------------------------------------------------------
# POURQUOI CE FICHIER EXISTE : LE PIEGE DU NOM « WOLVERINE »
# ---------------------------------------------------------------------------
# Le jeu contient DEJA un heros nomme « Wolverine » : le Logan officiel,
# 35001a du pack `wolv`. Les modules de X-23 se ciblent par nom en dur
# (`SetTarget(name="X-23")`, `CardFinder(name="X-23")`), ce qui est sans
# danger tant que le nom est unique. Ici il ne l'est plus.
#
# Le ciblage par nom n'est PAS borne au joueur : le `from_where` par defaut
# d'un selecteur vaut « Default », qui se resout en `get_InPlay`
# (src/game/selector/selector_where.py:197), c'est-a-dire tout ce qui est en
# jeu, chez tout le monde. Une table ou quelqu'un joue le Wolverine officiel
# et quelqu'un d'autre ce Wolverine-ci verrait donc « Wolverine's Claws »
# donner +2 ATK au mauvais heros.
#
# On borne donc chaque reference au CONTROLEUR, via `EstTonHeros` /
# `TonHoneyBadger` ci-dessous, ou en ciblant directement « YourIdentity ».
#
# ECART CONNU, non corrigeable ici : la reciproque reste vraie. Adamantium
# Skeleton (35004) et Berserker Frenzy (35005), du pack officiel, cherchent
# `CardFinder(name="Wolverine")` sans borne et verraient ce heros-ci. Corriger
# cela demanderait de toucher des cartes OFFICIELLES pour le confort d'un
# custom, ce que ce projet ne fait pas. Le cas ne se produit que si les deux
# Wolverine sont a la meme table.
# ===========================================================================

NOM_HEROS = "Wolverine"
NOM_SOEUR = "Honey Badger"


def EstTonHeros(effect: 'Effect', face: 'CardFace') -> bool:
    """Le `name="Wolverine"` des cartes designe TON Wolverine, pas un autre.

    A combiner avec `name=NOM_HEROS` dans un CardFinder : le nom filtre, et
    cette fonction tranche entre deux porteurs du meme nom.
    """
    return face.GetControlByPlayer() == effect.GetInitiator()


def TonHoneyBadger(effect: 'Effect') -> 'CardFace|None':
    """Ta Honey Badger en jeu, et pas celle du joueur X-23 d'a cote."""
    return Worlds.FindCardOnField(
        effect,
        name=NOM_SOEUR,
        check_effect_fn=EstTonHeros,
    )
