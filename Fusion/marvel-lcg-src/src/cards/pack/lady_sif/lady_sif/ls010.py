from . import *

# * Sif's Spear — amelioration signature, x1 (n/15 = 14).
# ASGARD. WEAPON. Cout 1, ressource [physical].
# Restricted.
# Lady Sif gets +1 DEF while in hero form and gains retaliate 1.
#
# Carte de reference : **`03009` * Captain America's Shield**, jumeau exact au
# nom pres — `GiveKeywordToAttached(CardFinder(name=...), defense=1,
# retaliate=1)`, et rien d'autre.
#
# ⚠ `Restricted` est une BASE AUTOMATIQUE, lue dans `desc.Restricted` :
# **aucun module**. La recoder ferait compter la carte deux fois dans la
# limite des deux cartes Restricted par joueur. Fiche :
# docs/reference/mots-cles/restricted.md.
# ⚠ `retaliate 1` : mot-cle officiel, fiche
# docs/reference/mots-cles/retaliate.md deja ecrite. Il se donne par le
# parametre `retaliate=` de la fabrique, pas par un module.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « LADY SIF gets ... WHILE IN HERO FORM » : les deux faces s'appellent
#    « Lady Sif », le nom seul ne trancherait donc rien. C'est
#    « while in hero form » qui tranche, et on le rend par le TYPE de face
#    (`Hero`) plutot que par le nom — meme lecture que hk012, et sans le
#    risque d'homonyme (`06002` * Lady Sif est un ALLIE officiel de Thor, qui
#    peut se trouver en jeu chez un autre joueur).
#  - `GiveKeywordToAttached(Hero, ...)` et non `("You", ...)` : « you »
#    donnerait le bonus aux DEUX faces, dont l'alter-ego, qui n'a pas de DEF.
#    C'est le piege an002, trouve en partie reelle le 01/09/2026.
#  - La riposte suit la meme portee : elle ne vaut qu'en forme de heros.
#  - Aucune capacite declenchee : ce module n'est QUE le bonus continu.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            defense=1,
            retaliate=1,
        ),
    ]
