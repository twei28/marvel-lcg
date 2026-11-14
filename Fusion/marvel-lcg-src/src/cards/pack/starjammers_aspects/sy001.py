from . import *
# * Ch'od (Basic, allie 4 [physical], 2**/3**, PV 5). STARJAMMER.
# Response: After Ch'od enters play, search your deck and discard pile for a VEHICLE or TECH card and add it to your hand.
#
# Cartes de reference : 08011 Agent Coulson (`AfterCardEnterPlay(Response, "This")` + `Search.PlayerCard(include_player_deck,
# include_discard_pile, trait=...)` + `GainCard`) ; `traits=[...]` d'un CardFinder est un OU (RECETTES §4, cr006).
# « a VEHICLE **or** TECH card » : tout type de carte (allie, soutien, amelioration, evenement) portant l'un des deux traits.
def GetAbilities() -> Sequence['Ability']:
    def chod(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        joueur = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            traits=["VEHICLE", "TECH"],
        )
        if face:
            joueur.GainCard(face, effect)
    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            chod,
        ),
    ]
