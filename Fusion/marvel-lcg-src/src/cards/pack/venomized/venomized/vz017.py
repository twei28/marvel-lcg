from . import *

# Symbiotic For Justice! — EVENEMENT, cout 2, RES [energy]. SYMBIOTE. THWART.
# Hero Action (thwart): Remove 3 threat from a scheme (4 threat instead, if you
#   paid for this card using a [mental] resource).
#
# CARTE DE REFERENCE
#  - `01060` For Justice! (Justice, pack core) : MEME TEXTE, meme cout, meme
#    ressource. Corps repris tel quel (voir l'en-tete du set).
#
# TEXTE CONTRE CODE
#  ⚠ « using A [mental] resource » -> `HasColor("B")`, et non `OnlyHasColor` :
#    un seul jeton mental suffit, le reste du paiement est libre. C'est
#    l'inverse exact de vz016.
def GetAbilities() -> Sequence['Ability']:

    def symbiotic_for_justice(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        valeur = 4 if effect.GetPaidResources().HasColor("B") else 3
        this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            symbiotic_for_justice
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2)
    ]
