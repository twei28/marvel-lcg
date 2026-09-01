from . import *

# Unbreakable Grip — amelioration signature. SUPERPOWER. Cout 2, [physical].
# While in hero form, Alligator Loki gets +1 ATK.
# Hero Interrupt: When you would detach Alligator Loki from an enemy in play,
#   exhaust Unbreakable Grip instead.
#
# Carte de reference : ma006 Star Flight, « <heros> gets +1 THW » ->
# `GiveKeywordToAttached(Hero, ...)`, l'amelioration etant posee sur
# l'identite par `Upgrade.GetAbilities` (aucun « Attach to » imprime).
# `Hero` et non `Identity` : « while in HERO form ».
#
# ⚠ LA SECONDE CAPACITE N'EST PAS ICI, ET C'EST VOULU. Le moteur n'a aucune
# fenetre « would detach » (`DetachFrom2` n'emet que `AfterCardDetachFrom`,
# apres coup), et l'accrochage du heros est une extension du pack. La fenetre
# est donc ouverte A LA MAIN dans `DetacherLeHeros` (alligator_loki/__init__.py),
# seul point de passage de tous les detachements du pack : c'est la que la
# Grip est cherchee (`CardFinder(name="Unbreakable Grip")`, prete et en jeu)
# et proposee au joueur (Interrupt nu, donc facultatif). Un module qui
# declarerait ici un `WhenCardWouldDetach` n'existerait pour aucun message.
#
# ⚠ Quels detachements passent par cette fenetre : la Reponse Obligatoire
# d'al001a (« after attached enemy activates, detach ») OUI, c'est le cas
# d'usage de la carte (une Forced Response n'empeche pas un effet de
# remplacement). Nap Time (al001b) NON : c'est un « HERO Interrupt » et Nap
# Time se resout APRES le passage en alter-ego, la Grip ne peut plus parler ;
# al001b detache donc avec `force=True`. Un ennemi qui quitte le jeu ne
# « detache » rien non plus (« from an enemy IN PLAY »).

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            attack=1,
        ),
    ]
