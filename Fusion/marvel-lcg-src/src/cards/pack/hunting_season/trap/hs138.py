from . import *

# hs138 Swinging Boulder
# When Revealed : epuisez votre identite, defaussez un allie, defaussez une amelioration, ou subissez 3 degats.

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()

        def epuiser(cibles: Sequence['CardFace']) -> None:
            Faces.ExhaustAll([identite], effect)

        def defausser(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(list(cibles), effect)

        def blesser(cibles: Sequence['CardFace']) -> None:
            identite.TakeDamage(this, 3, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust your identity", epuiser, condition=identite.IsReady()),
            AbilityFactory.ForChoiceAbility("Discard an ally you control", defausser).SetTarget("YouControlUnit", card_type=Ally),
            AbilityFactory.ForChoiceAbility("Discard an upgrade you control", defausser).SetTarget("YouControlUnit", card_type=Upgrade),
            AbilityFactory.ForChoiceAbility("Take 3 damage", blesser),
        )

    return [AbilityFactory.WhenThisRevealed(None, revelation)]
