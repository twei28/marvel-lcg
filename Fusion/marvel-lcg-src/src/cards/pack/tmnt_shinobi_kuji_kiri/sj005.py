from . import *

# Tai Chi (sj005), Kuji-Kiri, RESSOURCE (genere : [wild]) (Inkwire, TMNT Shinobi).
# Max 2 per deck.
# Response: After you spend this card on a SPELL card, draw 1 card.
#
# Cartes de reference : `aos/maria_hill/50007` Special Funding et `angel/42008` Avian Anatomy (« Response: After
# you spend this card to pay for a <filtre> » : `AfterYouSpendThisCard(..., to_pay_card=CardFinder(...))`).
# « Max 2 per deck » = `desc.MaxPerDeck "2"` (base automatique, `mut_gen/32018` Defensive Energy).
# Icone de ressource : etoile verte = [wild] (`RES: G`), meme glyphe que `tj009` / Light of Foot.
#
# TEXTE CONTRE CODE
#  ⚠ « spend this card ON A SPELL CARD » : toute carte au trait SPELL payee avec CETTE ressource (evenement,
#    amelioration, soutien, allie), pas seulement un evenement. Une carte non SPELL payee : rien.
#  ⚠ « draw 1 card » : pour le joueur qui a depense (l'initiateur de la Reponse).


def GetAbilities() -> Sequence['Ability']:

    def tai_chi(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            tai_chi,
            to_pay_card=CardFinder(trait="SPELL"),
        ),
    ]
