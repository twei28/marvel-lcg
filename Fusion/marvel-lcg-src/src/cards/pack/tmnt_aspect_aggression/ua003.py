from . import *

# * Assassin (Leo) — ALLIE 3 [mental], ATK 3 (2 degats consecutifs), THW 1 (1), PV 3. NINJA. TURTLE.
# [star] Assassin takes -1 consequential damage ([consequential]) after he attacks the villain or an ELITE minion.
#
# CARTE DE REFERENCE : `36016` * Gentle (« takes +1 consequential damage after he attacks the villain ») :
#   `AfterUnitAttackEnd(NonKeywordStar, "This", ..., against_who=Villain)` + `GainForThisActive(...,
#   attack_consequential_damage=+1)`. Ici -1, et la cible est « the villain OR an ELITE minion ».
# TEXTE CONTRE CODE
#  ⚠ « the villain or an ELITE minion » : condition sur les cibles de l'attaque ; un sbire non ELITE garde
#    les 2 degats consecutifs (contre-cas).
#  ⚠ [star] = capacite permanente marquee de l'etoile (Star Icon) : pas de declencheur a choisir.
#  Aucune limite imprimee.


def ContreLeVilainOuUnElite(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
    Unused(effect)
    for cible in message.attacked_targets:
        if Villain.IsType(cible):
            return True
        if Minion.IsType(cible) and cible.HasTrait("ELITE"):
            return True
    return False


def GetAbilities() -> Sequence['Ability']:

    def assassin(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        this.GainForThisActive(effect, message, attack_consequential_damage=-1)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.NonKeywordStar,
            "This",
            assassin,
            conditions=[ContreLeVilainOuUnElite],
        ),
    ]
