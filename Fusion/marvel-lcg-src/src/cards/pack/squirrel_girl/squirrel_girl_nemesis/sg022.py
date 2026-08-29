from . import *

# Ratatoskr's Whispers
# Attach to your identity card. You cannot spend SQUIRREL allies.
# Alter-Ego Action: Exhaust Doreen Green and discard a card with a printed
#   [mental] resource from your hand → discard Ratatoskr's Whispers.
# [star] Boost: Discard 1 SQUIRREL ally you control. If you cannot, the villain
#   gets +1 ATK and +1 SCH for this activation.
#
# Texte corrige le 28/08/2026 : il disait « this activation gets +1 ATK » —
# une activation ne porte pas de valeurs. Convention officielle verifiee
# (04116 Zola, 08026 Taskmaster) : c'est le VILAIN qui recoit le bonus pour
# cette activation. Le code faisait deja exactement cela
# (GainATKForThisAttack / GainSCHForThisScheme), seul le texte etait faux.
#
# L'interdiction de depense n'est pas une capacite de cette carte : la
# capacite Resource de chaque ecureuil teste sa presence (PeutDepenser dans le
# module du pack), le moteur n'ayant pas de notion de « depenser un allie ».

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        joueur = message.GetToPlayer()

        ecureuils = EcureuilsControles(effect, joueur)
        if ecureuils:
            choisi = joueur.AskChooseFace(ecureuils, effect)
            Faces.DiscardAll([choisi] if choisi else ecureuils[:1], effect)
            return

        being = message.being_message
        if being.IsAttack():
            being.GainATKForThisAttack(1, effect)
        if being.IsScheme():
            being.GainSCHForThisScheme(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        (AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.AlterEgoAction,
        )
            .SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Discard(
                Select.From(
                    CardFinder(has_printed_res="B"),
                    from_where=["YourHandCards"]
                )))),
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Boost,
            None,
            boost,
        ),
    ]
