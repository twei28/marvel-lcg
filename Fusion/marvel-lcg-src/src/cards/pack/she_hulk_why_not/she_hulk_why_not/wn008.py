from . import *

# Superhuman Strength (variante Why Not) : traits GAMMA ajoute. Note de
# l'auteur : « If you have no one to stun, you cannot discard it. »
# Decision de l'utilisateur du 25/10/2026 : si l'attaque a VAINCU l'ennemi
# attaque (plus personne a sonner), la carte reste en jeu avec son +2 ATK ;
# sinon elle se defausse et sonne l'ennemi, comme 01028.


def ennemi_attaque_en_jeu(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
    return any(Enemy.IsType(cible) and cible.IsInPlay() for cible in message.attacked_targets)


def GetAbilities() -> Sequence['Ability']:

    def superhuman_strength(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="She-Hulk"),
            attack=2,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="She-Hulk"),
            superhuman_strength,
            conditions=[ennemi_attaque_en_jeu],
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("Targets", canbe_stunned=True),
    ]
