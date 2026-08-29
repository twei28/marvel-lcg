from . import *
def GetAbilities() -> Sequence['Ability']:
    def lay_down_the_law(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Event)
        # « 4 threat instead if you paid for this card using a [mental]
        # resource » : meme test que « For Justice! » (01060).
        amount = 4 if effect.GetPaidResources().HasColor("B") else 3
        this.RemoveThreatFromSchemes(effect.targets, amount, effect)
    return [
        # CORRECTIF (29/08/2026) : `.SetPlay()` manquait. Lay Down the Law est
        # un EVENEMENT, joue de la main en reaction. Sans capacite de jeu,
        # `CardFactory.CreateFace` (factory.py:120) exige exactement UNE
        # capacite `Play` sur un evenement et levait
        # `AssertionError: face.paper.card_id='61018'` : le deck jessica_jones
        # ne montait pas. Et la carte n'aurait jamais ete jouable.
        AbilityFactory.AfterUnitChangeForm(AbilityType.HeroResponse, "You", lay_down_the_law)
        .SetPlay().SetLabel('thwart').SetTarget(Scheme2, range=(1, 1)),
    ]
