from . import *

# Kuji-Kaijū (sj014), Kuji-Kiri, amelioration SPELL TITLE, unique (Inkwire, TMNT Shinobi).
# Attach to an ally you control. That ally gains the FERAL and GIANT traits.
# Attached ally gets +2 hit points and +2 ATK.
# Attached ally takes +1 consequential damage ([consequential]) after it attacks.
#
# Cartes de reference : `cap/03031` Enraged (« Attached ally gets +2 ATK and takes +1 consequential damage after
# it attacks » : `GiveKeywordToAttached(Ally, attack=2, attack_consequential_damage=1)`) ; `cyclops/33035` Honorary
# X-Men (« gains the X-MEN trait » : `GiveKeywordToAttached(..., trait=...)`, un appel par trait) ;
# `ant/12018` Reinforced Suit (« +2 hit points » : `health=2`) ; « an ally YOU control » : selecteur `"YourAlly"`
# (les allies du joueur, pas ceux d'un autre).
#
# TEXTE CONTRE CODE
#  ⚠ « Attach to an ally YOU CONTROL » : seuls vos allies sont des cibles legales (contrairement a « an ally »).
#  ⚠ « gains the FERAL AND GIANT traits » : les DEUX traits (deux appels : l'API n'en prend qu'un).
#  ⚠ « +2 hit points AND +2 ATK » : les deux ; PAS de bonus de THW.
#  ⚠ « takes +1 consequential damage after it ATTACKS » : apres une attaque seulement (pas apres une action
#    de menace), en plus des degats consequentiels imprimes (+1 : un allie sans icone en subit 1).
#  ⚠ Pas de « Max 1 per ally » imprime : aucune limite par allie.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard("YourAlly"),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            trait="FERAL",
            health=2,
            attack=2,
            attack_consequential_damage=1,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            trait="GIANT",
        ),
    ]
