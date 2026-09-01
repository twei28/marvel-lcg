from . import *

# * Doom's Armor — amelioration signature. TECH. Cout 3.
# Doctor Doom gets +3 hit points and gains the AERIAL trait.
# Hero Interrupt: If Doctor Doom has villainous, when using a basic power,
#   exhaust Doom's Armor -> deal yourself 1 additional boost card.
#
# Cartes de reference :
#  - bonus continu + trait : an008 * Siri's Dress et ho011 * Goblin Glider,
#    `GiveKeywordToAttached("You", health=3, trait="AERIAL")` — le trait et le
#    bonus visent la meme cible, un seul appel (recette moteur §3) ;
#  - « when using a basic power » : le moteur n'a pas de declencheur unique
#    pour les trois pouvoirs. On accroche l'ATTAQUE de base
#    (`WhenUnitMakeAttack(..., is_basic_attack=True)`, modele 19005 Knife
#    Leap), qui est le seul des trois a distribuer des cartes de boost
#    (can_attack.py:220).
#  - la carte de boost supplementaire : `AttackProperty.additional_boost_card`
#    (can_attack.py:5), champ prevu exactement pour ca et commente « Only for
#    basic attack ».
#
# ⚠ Cette carte ne fonctionne QUE grace a l'extension moteur du 01/09/2026
# (voir le __init__.py du pack) : sans `HasVillainous` sur `Hero`,
# `IsVillainous()` n'existerait pas sur l'identite et la condition ne pourrait
# jamais etre lue. C'est la seconde carte, avec dd001a, qui la justifie.
#
# ⚠ « If Doctor Doom HAS villainous » est une CONDITION, pas un cout : elle est
# verifiee avant de proposer l'inclinaison, sinon le joueur paierait pour rien.

def GetAbilities() -> Sequence['Ability']:

    def a_villainous(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        Unused(message)
        initiator = effect.GetInitiator()
        if initiator is None:
            return False
        hero = initiator.GetHero()
        if hero is None:
            return False
        return hero.CastTo(HasVillainous).IsVillainous()

    def dooms_armor(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.property.additional_boost_card += 1

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
            trait="AERIAL",
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            dooms_armor,
            is_basic_attack=True,
            conditions=[a_villainous],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
