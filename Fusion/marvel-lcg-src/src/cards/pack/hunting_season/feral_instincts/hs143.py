from . import *

# hs143 Unleashed Beast
# When Revealed: The villain attacks you. If you are in alter-ego form, no boost card.
# [star] Boost: +1 boost icon if this activation is an attack.
# Modele boost : fne 60072 (WhenBoostCardWouldTurnedFaceUp + GainBoostIcon).

def GetAbilities() -> Sequence['Ability']:

    def bete(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if joueur is None or vilain is None:
            return
        vilain.DoAttackYou(joueur, effect, property=AttackProperty(
            against_player=joueur, do_not_give_boost=joueur.IsAlterEgo()))

    def icone(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> None:
        message.GainBoostIcon(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, bete),
        AbilityFactory.WhenBoostCardWouldTurnedFaceUp(
            AbilityType.ForcedInterrupt,
            icone,
            while_attack=True,
            conditions=[lambda effect, message: message.trigger == effect.this],
        ),
    ]
