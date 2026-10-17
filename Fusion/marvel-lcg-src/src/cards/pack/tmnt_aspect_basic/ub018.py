from . import *

# * Herold Lilja's Lab (bandeau « ✦ Cerebro ») — SOUTIEN 1 [mental], aspect Basic. LOCATION. NYC. STREETS.
# Play only if your identity has the [[MUTANT]] trait.
# Alter-Ego Action: Exhaust this card → search the top 5 cards of your deck for a [[DIMENSION X]], [[NINJA]],
#   or [[MUTANIMAL]] ally (search the whole deck instead if you control a [[TEMPORAL]] character) and add
#   that ally to your hand. (Shuffle.)
#
# MODIFIEE de 34022 Cerebro : X-MEN -> DIMENSION X / NINJA / MUTANIMAL (OU, `traits=[...]`) ; PSIONIC ->
# TEMPORAL. Script copie de 34022.


ALLIE = ["DIMENSION X", "NINJA", "MUTANIMAL"]


def GetAbilities() -> Sequence['Ability']:

    def lab(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()

        if initiator.IsControl(CardFinder2("TEMPORAL", Unit2)):
            face = Search.PlayerCard(
                effect,
                initiator,
                include_player_deck=True,
                card_type=Ally,
                traits=ALLIE,
            )
        else:
            face = Search.PlayerDeckTop(
                effect,
                initiator,
                5,
                card_type=Ally,
                traits=ALLIE,
            )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(
        ).SetPlay(only_if_your_identity_has_trait="MUTANT"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            lab
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
