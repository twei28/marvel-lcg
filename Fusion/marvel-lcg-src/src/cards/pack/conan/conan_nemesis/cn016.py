from cards.pack.conan.conan import *

# * Hymdul — sbire nemesis de Conan. GIANT. SCH 1 / ATK 3 / 5 PV. Toughness.
# Response: After you make a basic attack against Hymdul, deal 1 damage to Hrothgar.
# (Conan's nemesis minion.)
# [star] Boost: You are confused.
#
# CARTES DE REFERENCE
#  - Response de JOUEUR imprimee sur une carte de rencontre : 32147 Magneto's
#    Helmet, `AfterUnitMakeBasicAttack(type, Hero, op, against_who=...)`.
#  - Boost « You are confused » : 11030 Ancient Warrior, `WhenCardBecomeBoost` +
#    `Faces.GiveStatus([joueur.GetIdentity()], ...)`.
#  - Toughness et Nemesis : lus dans `desc`. Les deux sbires entrent par
#    01190 Shadow of the Past, qui revele TOUS les sbires nemesis du set.
#
# TEXTE CONTRE CODE
#  « you make a basic attack » : une attaque de BASE d'un heros (pas un allie,
#    pas un evenement).
#  « deal 1 damage to Hrothgar » : seulement s'il est en jeu ; sa Toughness
#    absorbe ce degat s'il la porte encore.


def GetAbilities() -> Sequence['Ability']:

    def frere(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        Unused(message)
        this = effect.this.CastTo(Minion)
        autre = Worlds.FindCardOnField(effect, name="Hrothgar", card_type=Minion)
        if autre is not None:
            this.DealDamage([autre], 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if isinstance(joueur, Player):
            Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.AfterUnitMakeBasicAttack(
            AbilityType.Response,
            Hero,
            frere,
            against_who="This",
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
