from . import *
# * K-Zzat (Protection, allie 3 [energy], THW 1*, ATK 2*, PV 3). STARJAMMER.
# Response: After K-Zzat attacks an enemy, deal 1 damage to a friendly character → stun the attacked enemy.
#
# Cartes de reference : 01083 Mockingbird (`Faces.GiveStatus(.., "Stunned", ..)`) ; dt066 Misty Knight (`CostFunc.DealDamage(1, "This")` ; la
# cible du cout se designe par un selecteur) ; `AfterUnitAttackEnd(type, "This", op)` (RECETTES §1 : `message.attacked_targets`).
# « deal 1 damage to a FRIENDLY character » est DEVANT la fleche : un COUT, au choix du joueur parmi les personnages amis (K-Zzat peut se
# viser). « stun THE ATTACKED enemy » : la cible de l'attaque, si elle est encore en jeu (un ennemi vaincu ne se sonne pas).
def GetAbilities() -> Sequence['Ability']:
    def kzzat(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        cibles = [f for f in message.attacked_targets if f.IsInPlay()]
        Faces.GiveStatus(cibles, "Stunned", effect)
    def une_cible_vivante(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return any(f.IsInPlay() for f in message.attacked_targets)
    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response,
            "This",
            kzzat,
            against_who=Enemy,
            conditions=[une_cible_vivante],
        ).SetCostFunc(CostFunc.DealDamage(1, "Friend")),
    ]
