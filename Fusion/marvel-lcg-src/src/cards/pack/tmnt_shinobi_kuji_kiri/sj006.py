from . import *

# Enthrall (sj006), Kuji-Kiri, amelioration CONDITION SPELL (Inkwire, TMNT Shinobi).
# Attach to a non-ELITE minion.
# Take control of attached minion and treat it as a CONTROLLED ally with a blank textbox. Its THW is equal to
# its printed SCH and it takes 3 consequential damage ([consequential]) after it thwarts or attacks.
#
# Carte de reference (texte identique a une consequence pres) : `phoenix/34009` Mind Control (1 degat
# consequentiel) ; meme mecanique `rogue/38011` Karma (2) et `bp/51036` Redemption (1).
# `AbilityFactory.TakeControlOfAttachedMinion("<gabarit d'allie>")` : le sbire devient un allie sous le controle
# du joueur (texte vide, THW = SCH imprime, ATQ = ATQ imprimee, PV = ceux du sbire) et le redevient quand
# l'amelioration quitte le jeu.
#
# EXTENSION DE DONNEES (pas de code moteur) : le nombre de degats consequentiels est porte par le GABARIT d'allie
# (une etoile par degat dans ATK / THW : `phoenix_controlled_ally` « 0* », `karma_controlled_ally` « 0** »).
# Enthrall : 3 -> nouveau gabarit `enthrall_controlled_ally` (`ATK "0***"`, `THW "0***"`, trait CONTROLLED),
# dans `data/cards.json`, pack `tmnt_shinobi_kuji_kiri`.
#
# TEXTE CONTRE CODE
#  ⚠ « non-ELITE minion » : `NonEliteMinion` (un sbire ELITE n'est pas une cible legale).
#  ⚠ « THW equal to its printed SCH » (pas son SCH courant) ; ATQ : celle du sbire (pas citee : la face
#    d'allie reprend l'ATQ imprimee du sbire, comme 34009).
#  ⚠ « 3 consequential damage ... after it thwarts OR attacks » : apres chacune de ses actions de base.
#  ⚠ « blank textbox » : les capacites du sbire disparaissent (traits conserves).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            NonEliteMinion,
        ),
        AbilityFactory.TakeControlOfAttachedMinion("enthrall_controlled_ally"),
    ]
