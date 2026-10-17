from . import *

# * Screwloose — ALLIE 3 [energy], aspect Justice (TMNT Reskins, Inkwire). AERIAL. DIMENSION X. MOSQUITO.
# Bandeau « ✦ Dagger » (unique_also, decision Q-R1).
# PV 3, THW 1 (2 degats consecutifs), ATK 2 (2 degats consecutifs).
# Wingnut loses each [acceleration] icon.
# [star] If Wingnut is in play, Screwloose takes -1 consequential damage after he uses a basic power.
#
# MODIFIEE par rapport a `60021` Dagger (Tandy Bowen) : « Cloak » -> « Wingnut », « she » -> « he ». Le
# module de 60021 compare le NOM « Cloak » en dur (`CardFinder(name='Cloak', card_type=Ally)`) : pas
# d'`ability_link` possible (RECETTES §11 point 3), script propre, copie de 60021 au nom pres.
#
# CARTES DE REFERENCE
#  - `60021` Dagger : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=..., card_type=Ally),
#    acceleration_icon=-1)` + `WhenAllyWouldTakeConsequentialDamage('This', update_damage=...)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « WINGNUT loses EACH [acceleration] icon » : l'allie Wingnut (uj038, 1 icone imprimee) ; tant que
#    Screwloose est en jeu.
#  ⚠ « If Wingnut is IN PLAY » : n'importe ou en jeu (pas seulement sous ton controle), lu a chaque usage.
#  ⚠ « -1 consequential damage » : sur SES degats consecutifs, apres un pouvoir de base (ATK 2* -> 1).


def GetAbilities() -> Sequence['Ability']:

    def wingnut_en_jeu(effect: 'Effect') -> int:
        face = Worlds.FindCardOnField(effect, CardFinder(name='Wingnut', card_type=Ally))
        return (-1 if face else 0)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name='Wingnut', card_type=Ally),
                                                         acceleration_icon=-1),
        AbilityFactory.WhenAllyWouldTakeConsequentialDamage('This', update_damage=wingnut_en_jeu),
    ]
