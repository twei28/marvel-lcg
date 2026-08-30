from . import *

# Magic Bolt (1/3) — custom « CptScorp »
# Cout 2, [energy], classe Hero, traits ATTACK / SPELL / SUPERPOWER.
# Hero Action (attack): Deal 3 damage to an enemy. Then, if the top card of
#   the encounter deck has:
#   • 0 or 1 boost icons -> draw 1 card.
#   • 2 or more boost icons -> deal 3 damage to an enemy. This attack gains
#     ranged.
#
# Exemplaire physique 1 de 3 (wc005, wc006, wc007). Commentaire complet ici,
# pointeur bref sur wc006 et wc007.
#
# Structure a paliers -> modele EXACT : Hex Bolt (`scw/scarlet_witch/
# 15004.py`), le seul evenement officiel du depot qui branche sur le NOMBRE
# d'icones de bonus (0 / 1 / 2 / 3+) et resout une consequence differente par
# palier. Ici deux paliers seulement : « 0 ou 1 » et « 2 ou plus ».
#
# Premier bloc de degats -> `.SetTarget(Enemy)` + `.SetLabel('attack')`,
# forme standard d'un evenement d'attaque (modele ag003 Burst Fire, 45004).
#
# Second bloc de degats -> `initiator.ChooseAbilities(...)` imbrique avec son
# propre `.SetTarget(Enemy)`, et NON `.SetTarget2`. C'est la lecon hd009
# (Quack and Burn) : `effect.targets2` n'est pas alimente par le pilote
# generique du harnais, la seconde moitie de la carte n'etait jamais exercee
# et rien ne le signalait. Le choix imbrique pose une question distincte, et
# reste testable.
#
# « This attack gains ranged » -> `property=AttackProperty(ranged=True)` passe
# a `DealDamage` (modele ag003/ag005/45004 ; `ranged` = « ignore retaliate »,
# game/card/face/attribute/can_attack.py:9).
#
# ARBITRAGE (tranche faute d'interlocuteur, session en arriere-plan) : « this
# attack » designe le SECOND bloc de degats, pas les 3 premiers. Raison : le
# texte imprime sequence explicitement (« Deal 3 damage... THEN, if the top
# card... »). Les 3 premiers degats sont deja resolus — et une eventuelle
# riposte deja subie — quand on lit les icones ; les rendre retroactivement
# ranged serait un rendu que le texte ne permet pas. La phrase « This attack
# gains ranged » suit immediatement le second « deal 3 damage to an enemy »
# dans la meme puce : c'est son antecedent le plus proche.
#
# Deck de rencontre vide, ou obligation wc018 active -> 0 icone, donc branche
# « 0 ou 1 » : on pioche. Lecture fidele du texte imprime.

def GetAbilities() -> Sequence['Ability']:

    def magic_bolt(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 3, effect)

        icones = IconesBoostDuDessus(effect, initiator)
        if initiator is None:
            return

        if icones <= 1:
            initiator.DrawUp(1, effect)
        else:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 3 damage to an enemy (this attack gains ranged)",
                    lambda targets:
                        this.DealDamage(targets, 3, effect,
                                        property=AttackProperty(ranged=True)),
                ).SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            magic_bolt,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
