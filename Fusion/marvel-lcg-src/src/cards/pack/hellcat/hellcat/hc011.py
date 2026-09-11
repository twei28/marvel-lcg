from . import *
# * Hedy Wolfe — SOUTIEN, cout 1, [mental]. BEST FRENEMY.
# Alter-Ego Action: Exhaust Hedy Wolfe → search your discard pile for a card
#   with a printed [mental] resource and attach it to your identity.
#
# Modeles : ze010 Hephaestus (Alter-Ego Action a cout Exhaust), ze014
# (`Search.PlayerCard(include_discard_pile=True, has_printed_res=...)`, qui
# rend la face sans la deplacer, puis `PlaceCardHere`).
# ⚠ Le trait BEST FRENEMY n'est pas dans l'enum TRAITS : il reste dans
#   cards.json, le module n'en a pas besoin.

def GetAbilities() -> Sequence['Ability']:

    def hedy_wolfe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = effect.GetInitiator()
        identite = IdentiteDe(effect)
        if joueur is None or identite is None:
            return
        face = Search.PlayerCard(effect, joueur, include_player_deck=False, include_discard_pile=True, has_printed_res="B")
        if face is not None:
            AccrocherA(identite, [face], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            hedy_wolfe,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
