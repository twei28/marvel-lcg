from . import *

# * John Walker (face ALTER EGO) — SOLDIER. PV 11, REC 3, main 6.
# Master of None — You may include cards in your deck from any aspect. You cannot include allies or basic cards.
# Action: Exhaust John Walker → search your deck and discard pile for the U.S. Agent's Shield upgrade and add it to
# your hand.
#
# Cartes de reference :
#  - `06001b` * Odinson (Thor) : « Search your deck and discard pile for the Mjolnir upgrade and add it to your hand » =
#    `Search.PlayerCard(effect, joueur, include_player_deck=True, include_discard_pile=True, card_type=Upgrade, name=...)`
#    puis `joueur.GainCard(face, effect)` (le melange est le comportement par defaut).
#  - `04001b` * Clint Barton : meme recherche avec un cout, sur une capacite NON limitee ici.
#
# ⚠ Mots-pieges :
#  - « Master of None » : regle de CONSTRUCTION de deck, pas de partie. Elle vit dans `deck/starter/us_agent.json`
#    (`metadata.deckbuilding` : tous les aspects, ni allies ni cartes Basic), lue par le deckbuilder, jamais par le moteur.
#  - « Action » nue (pas « Alter-Ego Action ») : imprimee sur la face ALTER EGO, donc jouable seulement sous cette forme.
#  - « Exhaust John Walker → » : le cout est l'inclinaison de l'identite (`CostFunc.Exhaust("This")`), payee AVANT la
#    recherche ; sans U.S. Agent's Shield dans le deck ni la defausse, la recherche ne trouve rien et le cout est quand
#    meme paye.
#  - AUCUNE limite imprimee : pas de `LimitOncePer...` (l'identite s'incline, une seule fois par tour de toute facon).


def GetAbilities() -> Sequence['Ability']:

    def john_walker(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Upgrade,
            name=NOM_BOUCLIER,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            john_walker,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
