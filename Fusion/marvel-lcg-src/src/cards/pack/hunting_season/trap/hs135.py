from . import *

# hs135 Tranquilizer Darts
# When Revealed : depensez une ressource mentale ou confusez votre identite. Impossible des deux : 1 degat.

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()

        def confondre(cibles: Sequence['CardFace']) -> None:
            Faces.GiveStatus([identite], "Confused", effect)

        def blesser(cibles: Sequence['CardFace']) -> None:
            identite.TakeDamage(this, 1, effect)

        impossible = identite.IsConfused() and not PeutPayer(joueur, "B")
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(Cost("B")),
            AbilityFactory.ForChoiceAbility("Confuse your identity", confondre, condition=not identite.IsConfused()),
            AbilityFactory.ForChoiceAbility("Take 1 damage", blesser, condition=impossible),
        )

    return [AbilityFactory.WhenThisRevealed(None, revelation)]
