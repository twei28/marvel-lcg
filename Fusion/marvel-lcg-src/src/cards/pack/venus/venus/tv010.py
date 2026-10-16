from . import *

# * Cosmic Requiem — AMELIORATION, cout 2, [wild]. ELEMENT. SONG. x1.
# Hero Action: Exhaust this card and remove 2 dredge counters from Venus -> discard cards
#   from the top of your deck until you discard an event. Add that card to your hand.
#
# CARTES DE REFERENCE
#  - `br009` Oathbrother : `joueur.DiscardDeckUntil(effect, card_type=Event)` puis
#    `Faces.AddToHand([face], joueur, effect)` (mot-cle `seek`, fiche `mots-cles/seek.md`).
#  - `tr013` : cout `CostFunc.Counter("YourIdentity", n, ...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust this card AND remove 2 dredge counters from Venus -> » : deux couts.
#  ⚠ « until you discard AN EVENT » -> `DefausserJusquA(card_type=Event)` : l'evenement
#    trouve est DEFAUSSE puis ajoute a la MAIN (les cartes traversees restent en defausse) ;
#    aucun evenement : tout le deck est defausse. Helper : derniere carte du deck incluse.
#  ⚠ Action de HEROS : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def requiem(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = DefausserJusquA(effect, joueur, card_type=Event)
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            requiem,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("YourIdentity", 2, DREDGE)),
    ]
