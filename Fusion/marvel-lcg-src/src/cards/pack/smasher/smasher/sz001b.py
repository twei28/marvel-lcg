from . import *
# * Izzy Kane, face alter ego. Prefixe `sz`.
#
# You cannot have more than 1 EXOSPEX upgrade in play.
# Battle Ready — Action: Search your deck and discard pile for an EXOSPEX upgrade and add it to your hand. (Limit once per turn.)
#
# Carte de reference : 56029b Teddy Altman (« You cannot have more than 1 [[Shapeshift]] upgrade in play » +
# « Shape-Changer — Action: Search your deck and discard pile for a Shapeshift upgrade and add it to your hand (limit once per round) »).
# ⚠ « once per TURN » (corrige le 26/10/2026, verdict RR « Action ») : la limite se compte par TOUR, pas par round. Un joueur peut jouer un
# tour de plus dans le meme round (rm007) : `LimitOncePerRound` le bloquait a tort. Les compteurs « ce tour » du joueur
# (`PlayerStat.this_turn_limited_abilities`, videe a chaque tour) tiennent la limite ; on y inscrit la carte a l'usage de l'Action.
def GetAbilities() -> Sequence['Ability']:
    def battle_ready(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        initiator = effect.GetInitiator()
        initiator.stat.RecordLimitedAbility(this)
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            trait=TRAIT_EXOSPEX,
            card_type=Upgrade,
        )
        if face:
            Faces.AddToHand([face], initiator, effect)
    def pas_encore_utilisee_ce_tour(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return not message.to_player.stat.HasUsedLimitedAbilityThisTurn(effect.this)

    return [
        AbilityFactory.PlayersCannotPlayCardWhile(
            "You",
            CardFinder2(TRAIT_EXOSPEX, Upgrade),
            conditions=[
                lambda effect, message:
                    effect.GetInitiator().GetControlCards2(CardFinder2(TRAIT_EXOSPEX, Upgrade)) != []
            ]
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            battle_ready,
            conditions=[pas_encore_utilisee_ce_tour],
        ).SetName("Battle Ready"),
    ]
