from . import *

# Mutant Suppression (x2, hf220-hf221). Traitrise TACTIC. « When Revealed : Exhaust your identity and each ally you control. [star] Boost : After this
# activation, exhaust your identity and place 1 energy counter on Sebastian Shaw. »
# Cartes de reference : hf321 (WQ : boost `Faces.ExhaustAll([message.GetToPlayer().GetIdentity()], effect)`), hf118 (allies du joueur :
# `joueur.GetControlCards(CardFinder(card_type=Ally))`), 49042 / hf107 (`message.AfterThisActivation`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        allies = [f for f in joueur.GetControlCards(CardFinder(card_type=Ally)) if f.IsInPlay()]
        Faces.ExhaustAll([joueur.GetIdentity()] + allies, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()

        def apres_l_activation() -> None:
            Faces.ExhaustAll([joueur.GetIdentity()], effect)
            PlacerEnergie(effect, 1)

        message.AfterThisActivation(effect, apres_l_activation)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
