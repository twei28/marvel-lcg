from . import *

# Stealth Mastery — AMELIORATION, cout 1, [energy]. SKILL. x1 (Elektra 15/15).
# Forced Interrupt: When you attack or are attacked, choose to either increase or reduce the damage that attack deals by 3. Put Stealth Mastery
# on top of your deck.
#
# CARTES DE REFERENCE
#  - « the damage that attack deals » modifie a l'etape « would be DEALT » : `62010` Metal Bracer (`WhenDamageWouldBeDealtTo` + `message.ReduceDamage`) et
#    `Message.WhenFaceWouldDealDamage.IncreaseDamage` (sender_damage.py:638-660), qui passent AVANT le Tenace (Rules Reference, Damage).
#  - « When you attack » : `AbilityFactory.WhenFaceWouldDealDamage(.., "You", op, from_attack=True)` (damage.py:534) ; « are attacked » :
#    `WhenDamageWouldBeDealtTo(.., "You", op)` avec la condition « venu d'une attaque ».
#  - « choose to either A or B » : `joueur.AskChooseOneText([...])` ; « put ... on top of your deck » : `Faces.MoveAllToDeck([this], joueur.player_deck, "Top", effect)`.
#
# TEXTE CONTRE CODE
#  ⚠ « When you ATTACK or are ATTACKED » : les degats d'une attaque dont l'attaquant OU la cible est l'IDENTITE du joueur (attaque de base ou par carte ;
#    attaque d'un ennemi contre l'identite). Une attaque contre un allie ou entre deux autres cartes ne declenche rien.
#  ⚠ « choose to EITHER increase OR reduce » : un choix OBLIGATOIRE (Forced), +3 ou -3, jamais les deux ; la reduction ne descend pas sous 0.
#  ⚠ « that attack » : les degats de CETTE attaque. L'etape « would be dealt » precede le Tenace.
#  ⚠ « Put Stealth Mastery on top of your deck » : apres le choix, la carte QUITTE le jeu pour le dessus du paquet (elle ne reste pas attachee).
#  Chiffres : cout 1, +3 ou -3, dessus du paquet.

INCREASE = "Increase_the_damage_by_3"
REDUCE = "Reduce_the_damage_by_3"


def GetAbilities() -> Sequence['Ability']:

    def stealth_mastery(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        choix = joueur.AskChooseOneText([INCREASE, REDUCE])
        if choix == INCREASE:
            message.IncreaseDamage(3, effect)
        else:
            message.ReduceDamage(3, effect)
        Faces.MoveAllToDeck([this], joueur.player_deck, "Top", effect)

    def vient_d_une_attaque(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> bool:
        Unused(effect)
        return message.being_atk_message is not None or message.would_atk_message is not None

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenFaceWouldDealDamage(
            AbilityType.ForcedInterrupt,
            "You",
            stealth_mastery,
            from_attack=True,
        ),
        AbilityFactory.WhenDamageWouldBeDealtTo(
            AbilityType.ForcedInterrupt,
            "You",
            stealth_mastery,
            conditions=[vient_d_une_attaque],
        ),
    ]
