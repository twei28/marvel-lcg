from . import *

# Psionic Active (x2). Traitrise SKILL. « When Revealed : If White Queen is in DIAMOND form, she attacks you. If you are in alter-ego form, you may
# choose to exhaust your identity and take 1 damage to cancel this attack. If White Queen is in PSIONIC form, she schemes. »
# Cartes de reference : 02030 I See You (`villain.DoAttackYou(player, effect, operation=...)`), `message.CancelThisAttack`,
# nt014 (`MayChooseOneAbility`), `DoScheme`.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        villain = VilainWQ(effect)
        if villain is None:
            return
        if EstDiamant(villain):
            def a_l_attaque(attaque: 'Message.WhenUnitWouldAttack') -> None:
                identite = joueur.GetIdentity()
                if joueur.IsAlterEgo() and identite.IsReady():
                    choix = joueur.MayChooseOneAbility(
                        effect,
                        AbilityFactory.ForChoiceAbility(
                            "Exhaust your identity and take 1 damage to cancel this attack",
                            lambda cibles: None,
                        ),
                    )
                    if choix is not None:
                        Faces.ExhaustAll([identite], effect)
                        identite.TakeDamage(effect.this, 1, effect)
                        attaque.CancelThisAttack(effect)

            villain.DoAttackYou(joueur, effect, operation=a_l_attaque)
        elif EstPsionique(villain):
            villain.DoSchemes(joueur, effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
