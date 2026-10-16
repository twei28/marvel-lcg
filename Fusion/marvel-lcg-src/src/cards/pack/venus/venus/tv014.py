from . import *

# * Turtle Shell — AMELIORATION, cout 2, [wild]. ELEMENT. TURTLE. x1.
# Hero Action: Exhaust this card and discard the top 2 cards of your deck -> ready Venus.
#
# CARTES DE REFERENCE
#  - `td011` Donatello's Bo : `Hero Action: Exhaust this card -> ready Donatello`
#    (`Faces.ReadyAll([heros], effect)`) ; `tv009` (meme pack) pour le cout
#    `DiscardDeckTopCards("YourDeck", 2)`.
#
# TEXTE CONTRE CODE
#  ⚠ « ready VENUS » -> le heros (Hero Action = forme heros). Heros deja pret : rien a faire,
#    mais les couts sont payes.
#  ⚠ Deux couts (inclinaison + defausse des 2 cartes du dessus).


def GetAbilities() -> Sequence['Ability']:

    def carapace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        heros = HerosDuJoueur(effect, joueur)
        if heros is not None:
            Faces.ReadyAll([heros], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            carapace,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 2)),
    ]
