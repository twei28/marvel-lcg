from . import *
# Targeting Goggles. Amelioration ITEM TECH, cout 1.
#
# Hero Action: Exhaust Targeting Goggles -> search your deck for an event and add it to your hand. Then place 1 card from your
# hand on the top of your deck.
#
# Cartes de reference : ok001b (`Search.PlayerCard` + `GainCard`), 40044 (`Faces.MoveAllTo(.., joueur.player_deck)` = « on top
# of your deck »), 14022 (Hero Action d'amelioration).
def GetAbilities() -> Sequence['Ability']:
    def goggles(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        joueur = effect.GetInitiator()
        face = Search.PlayerCard(effect, joueur, include_player_deck=True, card_type=Event)
        if not face:
            # RR « Then » : le texte avant « then » ne se resout pas (aucun evenement trouve) -> « place 1 card ... on top » n'est pas tente
            # (corrige le 26/10/2026 : on remettait une carte sur le deck meme sans evenement). Le joueur est PREVENU (comme Safe House #30).
            joueur.NotifyNoResult(effect.this, "No event in your deck: no card is placed on top of your deck.")
            return
        joueur.GainCard(face, effect)
        main = list(joueur.hand_cards.Get())
        if not main:
            return
        choisie = joueur.AskChooseFace(main, effect, prompt="Place on the top of your deck", forced=True)
        if choisie:
            Faces.MoveAllTo([choisie], joueur.player_deck, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            goggles,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
