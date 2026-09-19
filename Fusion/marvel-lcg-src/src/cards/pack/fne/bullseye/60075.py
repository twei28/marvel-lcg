from . import *

# Unerring Desire
# When Revealed: Choose to either give this card to the villain as a facedown
#   boost card, or remove a PERSONA support you control from the game.
# [star] Boost: If this activation is an attack, it gains overkill.
# Modeles : 56091 (GiveBoostCard), an013 Hel-Wolf (GainOverKill en boost).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillain(effect)

        def au_vilain(targets: Sequence['CardFace']) -> None:
            if vilain:
                vilain.GiveBoostCard(this, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Give this card to the villain as a facedown boost card", au_vilain),
            AbilityFactory.ForChoiceAbility(
                "Remove a Persona support you control from the game",
                lambda targets: Faces.RemoveAllFromGame(targets, effect),
            ).SetTarget(CardFinder(card_type=Support, trait="PERSONA"), from_where=["YouControlCards"]),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
