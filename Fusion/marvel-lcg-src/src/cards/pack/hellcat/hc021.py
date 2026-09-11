from . import *
# Hell-Iron — EVENEMENT BASIQUE custom (jakxin), cout 1, [energy].
# Team-Up (Hellcat and Iron Man). Max 1 per deck.   (desc.TeamUp, base auto)
# Hero Action: Ready Hellcat and Iron Man. Search your deck and discard pile
#   for an upgrade and add it to your hand.
#
# ⚠ `.SetTarget("TeamUp")` obligatoire, voir hc020.
# Modeles : hc020 Green Hell, ze001b (`Search.PlayerCard(include_player_deck,
# include_discard_pile, card_type=Upgrade)`), `Faces.AddToHand`.

def GetAbilities() -> Sequence['Ability']:

    def hell_iron(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        Faces.ReadyAll(list(effect.targets), effect)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(effect, joueur, include_player_deck=True, include_discard_pile=True, card_type=Upgrade)
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hell_iron,
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp"),
    ]
