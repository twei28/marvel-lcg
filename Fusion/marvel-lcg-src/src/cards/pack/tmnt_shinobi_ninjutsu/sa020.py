from . import *

# From the Shadows — RESSOURCE, Ninjutsu (TMNT Shinobi, Inkwire). Sans cout, [wild], aucun trait.
# Max 1 per deck.
# Hero Response: After you spend this card to play a Ninjutsu card, cloak your hero.
#
# NOUVELLE. Mots-cles (fiches lues AVANT le code) : Cloak / Cloaked (cloak.md, cloaked.md), Shinobi (shinobi.md).
# Icone de ressource (etoile verte) verifiee contre `ub017` Gofu Talisman / `ub031` Mutagen (`RES = G`) : wild.
#
# Cartes de reference :
#  - `21046` Audacity : « Hero Response: After you spend this card, ... » = `AfterYouSpendThisCard(HeroResponse, fn)` ;
#    le filtre « to play a <carte> » = parametre `to_pay_card=<CardFinder>` de la fabrique ;
#  - `CarteShinobi("Ninjutsu")` : « a Ninjutsu card » (une Dual Ninjutsu compte).
#
# TEXTE CONTRE CODE
#  ⚠ « After you spend THIS card » : cette ressource precisement, depensee (defaussee) pour payer ; « TO PLAY a Ninjutsu
#    card » : un paiement de JEU d'une carte Ninjutsu (pas une capacite, pas une carte Bushido/Taijutsu/Basic) ; « cloak
#    YOUR HERO » : sur le heros (forme heros : Hero Response).
#  ⚠ « Max 1 per deck » : `desc.MaxPerDeck = 1`, regle de construction (aucun module).


def GetAbilities() -> Sequence['Ability']:

    def from_the_shadows(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None or not joueur.IsHero():
            return
        ShinobiCloak(effect, joueur.GetHero())

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            from_the_shadows,
            to_pay_card=CarteShinobi("Ninjutsu"),
        ),
    ]
