from . import *

# Yang (sj003), Kuji-Kiri, evenement ATTACK SPELL (Inkwire, TMNT Shinobi).
# Hero Action (attack): Deal 2 damage to an enemy. Choose:
#  • Stun an enemy.
#  • Give a friendly character a tough status card.
#
# Cartes de reference : `jennika/tj004` Decisive Strike (« Hero Action (attack): Deal 3 damage to an enemy »,
# `DealDamage(effect.targets, ...)`, label 'attack') ; `donatello/td005` Improvised Tactics (« choose »
# modal : `ChooseAbilities` + `ForChoiceAbility`, cibles propres a chaque option).
#
# TEXTE CONTRE CODE
#  ⚠ « Deal 2 damage to an enemy » : degats DIRECTS (pas une attaque de base : ATK du heros ignoree).
#  ⚠ « Choose: » : UNE seule des deux options, apres les degats ; « Stun AN enemy » : n'importe quel ennemi
#    (pas forcement celui qui a pris les 2 degats) ; « a FRIENDLY character » : heros ou allie de n'importe
#    quel joueur (`Friend`).
#  ⚠ Label 'attack' (parenthese imprimee) : Sonne / Desoriente peuvent annuler l'evenement.


def GetAbilities() -> Sequence['Ability']:

    def yang(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        this.DealDamage(effect.targets, 2, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy",
                lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect),
            ).SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility(
                "Give a friendly character a tough status card",
                lambda cibles: Faces.GiveStatus(cibles, "Tough", effect),
            ).SetTarget(Friend, canbe_tough=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            yang,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
