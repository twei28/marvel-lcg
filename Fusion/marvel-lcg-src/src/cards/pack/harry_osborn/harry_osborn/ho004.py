from . import *

# Pumpkin Bomb — evenement. ATTACK. SUPERPOWER. Cout X. x2
# Hero Action (attack): Choose a player. Deal X damage to the villain and
#   each minion engaged with that player. For each enemy defeated this way,
#   confuse an enemy.
#
# Cartes de reference :
#  - l'arrosage : 04006 Explosive Arrow (pack trors), meme phrase « deal 3
#    damage to the villain and each minion engaged with that player », rendue
#    par `SetTarget("VillainAndEngagedSamePlayerMinion")` (le choix du joueur
#    est porte par le selecteur) ;
#  - le X : 14006 Speed Cyclone, `effect.GetCostX()` ;
#  - « defeated this way » : ag006 Takedown / th009 Sock 'Em, parametre
#    `if_this_attack_defeats` de `DealDamage`, appele une fois PAR unite
#    vaincue par CES degats-la ;
#  - la confusion au choix : 01083 Mockingbird transpose (GiveStatus
#    "Confused" + cible via ChooseAbilities, modele 08013 Stealth Strike).
#
# ⚠ « confuse AN enemy » : la confusion va a n'importe quel ennemi, pas
# forcement un de ceux touches par la bombe (contraste avec « THAT enemy »
# de ho003, mots-pieges etape 5).

def GetAbilities() -> Sequence['Ability']:

    def pumpkin_bomb(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        x = effect.GetCostX()

        vaincus: List['Unit2'] = []

        def vaincu(unit: 'Unit2') -> None:
            vaincus.append(unit)

        this.DealDamage(effect.targets, x, effect,
                        if_this_attack_defeats=vaincu)

        def confuse(cibles: Sequence['CardFace']) -> None:
            Faces.GiveStatus(cibles, "Confused", effect)

        for _ in vaincus:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Confuse an enemy", confuse,
                ).SetTarget(Enemy, canbe_confused=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pumpkin_bomb
        ).SetPlay().SetLabel('attack')
        .SetTarget("VillainAndEngagedSamePlayerMinion"),
    ]
