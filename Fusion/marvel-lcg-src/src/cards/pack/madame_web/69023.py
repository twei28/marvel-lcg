from . import *

# * Spider-Woman: Ashley Barton — custom « Kajislav », carte d'aspect AGRESSION
# Spider-Woman gets +1 ATK, if you paid for this card using only [physical]
#   resources.
#
# Toutes les cartes du moteur qui lisent « si vous avez payé uniquement avec »
# sont des EVENEMENTS : elles interrogent `effect.GetPaidResources()` depuis
# leur propre effet de jeu, qui porte le paiement. Une alliée n'a pas d'effet
# de jeu de ce genre — d'où le passage par `AfterPlayerPlayedCard`, dont le
# message expose `paid_resources`.
#
# Le bonus est appliqué ICI, directement. Un `ThisGainKeyword` ne convient pas :
# il est évalué à l'ENTREE EN JEU, donc AVANT que le paiement soit connu, et il
# ne se réévalue pas ensuite. Mesuré : paiement (R R) lu correctement, et
# l'alliée restait quand même à 2 ATK.

def GetAbilities() -> Sequence['Ability']:

    def paye_en_physique(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)

        paye = getattr(message, "paid_resources", None)
        if paye and paye.OnlyHasColor("R"):
            this.Gain(effect, 1, attack=1)

    return [
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.NonKeyword,
            paye_en_physique,
        ),
    ]
