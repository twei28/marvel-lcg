from . import *
# * D'Ken. Sbire ELITE KING SHI'AR, nemesis de Corsair. Villainous (cle `desc`).
#
# As an additional cost to attack D'Ken, you must discard a card from your hand.
#
# Carte de reference : 58027 Brother vs. Brother (« As an additional cost to attack Grim Reaper, you must discard 1 card
# from your hand ») : `WhenUnitWouldAttack(ForcedInterrupt)` ; l'attaquant choisit la carte de SA main, et si elle est
# vide l'attaque est empechee (`SetBeInstead`). Ecrite ici sur D'Ken lui-meme.
def GetAbilities() -> Sequence['Ability']:
    def cout(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        attaquant = message.trigger
        joueur = attaquant.GetControlByPlayer()
        if not joueur:
            return
        main = list(joueur.hand_cards.Get())
        if not main:
            message.SetBeInstead(effect)
            return
        def action(chosen: Sequence['CardFace']):
            Faces.DiscardAll(list(chosen), effect)
        joueur.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility(
            'Discard 1 card from your hand', action).SetTarget(main, range=(1, 1), not_move=True))
    def attaque_dken(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        attaquant = message.trigger
        if not (Hero.IsType(attaquant) or Ally.IsType(attaquant)):
            return False
        return message.HasTarget(effect.this)
    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, None, cout, conditions=[attaque_dken]),
    ]
