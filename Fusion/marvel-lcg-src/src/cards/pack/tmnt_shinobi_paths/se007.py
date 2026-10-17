from . import *

# Yamabushi — PATH hybride (avance), classes Kuji-Kiri + Taijutsu (Inkwire, TMNT Shinobi). KUJI-KIRI. TAIJUTSU.
# Permanent. You get -1 hand size. You gain the TEMPORAL trait.
# Meditate — Hero Action: Exhaust this card and your hero -> draw 3 cards. Choose and discard 1 card from your
#   hand.
#
# Mots-cles (fiches lues AVANT le code) : Permanent (permanent.md) ; Shinobi / Path (shinobi.md).
#
# Cartes de reference :
#  - « -1 hand size » + trait : `sentinel/st005b` / `hunting_season/hs092` ;
#  - « exhaust this card AND your hero -> » : deux couts `CostFunc.Exhaust("This")` +
#    `CostFunc.Exhaust("YourHero")` (jennika/tl... , `ua...` : « exhaust your hero ») ;
#  - « draw N cards. Choose and discard 1 card from your hand » : `joueur.DrawUp(n, effect)` puis
#    `joueur.AskDiscardFaces(main, (1, 1), effect)` (player_phase.py, MayDiscardHandCardsAndDrawUpToMax).
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust this card AND YOUR HERO » : le heros doit etre redresse pour payer (une Action de heros inclinant
#    le heros : le heros n'agit plus ce tour, sauf carte de redressement).
#  ⚠ « draw 3 cards » = EXACTEMENT 3 cartes (`DrawUp(3)`), sans plafond de taille de main ; « Choose and discard
#    1 card from your HAND » : une carte CHOISIE de la main entiere (pas seulement les 3 piochees).
#  ⚠ « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def meditate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Path)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(3, effect)
        main = list(joueur.hand_cards.Get())
        if main:
            joueur.AskDiscardFaces(main, (1, 1), effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1, trait="TEMPORAL"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            meditate,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Exhaust("YourHero")),
    ]
