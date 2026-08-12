from . import *

# Recon Team
# Hero Action (thwart): Remove 3 threat from a scheme. If you spent a Squirrel
#   to play this card, remove 1 threat from a different scheme.

def GetAbilities() -> Sequence['Ability']:

    def deblayer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        vises = list(effect.targets)
        this.RemoveThreatFromSchemes(vises, 3, effect)

        if not ADepenseUnEcureuil(effect):
            return

        autres = [face for face in Worlds.FindCardsOnField(effect, card_type=Scheme2)
                  if face not in vises]
        if not autres:
            return

        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a different scheme",
                lambda targets: this.RemoveThreatFromSchemes(list(targets), 1, effect),
            ).SetTarget(Select.From(faces=autres), range=(1, 1)),
        )

    return [
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, deblayer)
            .SetPlay()
            .SetLabel("thwart")
            .SetTarget(Scheme2)),
    ]
