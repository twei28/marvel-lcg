from . import *

# * Mutant Fight Club — SOUTIEN unique 1 [energy], Taijutsu (TMNT Shinobi, Inkwire). LOCATION. NYC. STREETS.
# You may play events attached to this card as if they were in your hand.
# Alter-Ego Action: Exhaust this card and take 1 damage → attach an ATTACK or DEFENSE event in your discard pile to
#   this card facedown.
#
# Mots-cles (fiche lue AVANT le code) : tuck.md (« attach facedown here » = `PlaceCardHere(..., False, effect)`).
#
# Cartes de reference :
#  - « Events attached to X may be played as if they were in your hand » : `ms_america/ma004` Santana Family et
#    `27007` George Stacy (`*AbilityFactory.AttachedCardCanPlayLikeInHand(CardFinder(card_type=Event))`) ;
#  - « Alter-Ego Action: Exhaust X and take 1 damage → ... » : `35022` Weapon X (`CostFunc.TakeDamage(1, "YourIdentity")`
#    + `CostFunc.Exhaust("This")`) ;
#  - « attach an event in your discard pile to this card facedown » : `26013` Jocasta / `tmnt_aspect_leadership/ul039`
#    Venus (`SetTarget(finder, from_where=["YourDiscardPile"])` + `PlaceCardHere(cibles, False, effect)`).
#
# TEXTE CONTRE CODE
#  ⚠ « Alter-Ego Action » : sous-type dedie ; la carte se REMPLIT en identite civile.
#  ⚠ « take 1 damage » est un COUT (avant la fleche) ; l'inclinaison aussi : les deux payes ou aucun.
#  ⚠ « an ATTACK OR DEFENSE event in YOUR DISCARD PILE » : un evenement ATTACK ou DEFENSE de VOTRE defausse (pas THWART
#    seul, pas une autre carte) ; « FACEDOWN » : `peek=False`, face cachee.
#  ⚠ AUCUN plafond imprime (contrairement a Santana Family / George Stacy) : pas de condition sur la taille de la zone.
#  ⚠ « You MAY play events attached ... as if in your hand » : permission de JOUER seulement (pas de depense ni de
#    defausse comme en main : `AttachedCardCanPlayLikeInHand()` sans `also_spend` / `also_discard`).


def GetAbilities() -> Sequence['Ability']:

    def mutant_fight_club(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        this.PlaceCardHere(effect.targets, False, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        *AbilityFactory.AttachedCardCanPlayLikeInHand(
            CardFinder(card_type=Event),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            mutant_fight_club,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TakeDamage(1, "YourIdentity"))
        .SetTarget(CardFinder(card_type=Event, traits=["ATTACK", "DEFENSE"]),  # type: ignore
                   from_where=["YourDiscardPile"]),
    ]
