from . import *
# Making Amends. Obligation alternative (donnee au joueur Christopher Summers), boost 2.
#
# You may flip to alter-ego form. Choose:
# • Exhaust Christopher Summers and tell someone you love them → remove Making Amends from the game.
# • Discard a card you control. This card gains surge. Discard this obligation.
#
# Carte de reference : 01160 Legal Work (meme squelette : `YouMayFlipToYourAlterEgoForm` + deux branches, la premiere
# reservee a l'alter ego et payee par `Exhaust("YourIdentity")`). « Tell someone you love them » est un geste a faire a la
# table : le moteur ne l'exige pas.
def GetAbilities() -> Sequence['Ability']:
    def amends(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer()
        YouMayFlipToYourAlterEgoForm(joueur, effect)
        def deuxieme(targets: Sequence['CardFace']):
            identite = joueur.GetIdentity()
            candidates = [f for f in joueur.GetControlCards() if f.IsInPlay() and f is not identite and f is not this]
            if candidates:
                choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(
                    candidates, effect, prompt="Discard a card you control", forced=True)
                if choisie is not None:
                    Faces.DiscardAll([choisie], effect)
            this.GainSurge(1, effect)
            Faces.DiscardAll([this], effect)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Christopher Summers and tell someone you love them → remove Making Amends from the game",
                lambda targets:
                    Faces.RemoveAllFromGame([this], effect),
                condition=joueur.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
            AbilityFactory.ForChoiceAbility(
                "Discard a card you control. This card gains surge. Discard this obligation",
                deuxieme,
            ),
        )
    return [
        AbilityFactory.WhenThisObligationGiveToYou(amends),
    ]
