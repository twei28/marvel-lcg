from . import *

# What Goes Around... (B, mode expert)

def GetAbilities() -> Sequence['Ability']:

    def carte_du_spot_revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When a card that belongs to The Spot encounter set is revealed,
        # place 1 threat on the main scheme. »
        if message.trigger.paper.set_name != "The Spot":
            return
        scheme = Worlds.FindMainScheme(effect)
        if scheme:
            Faces.PlaceTokensOn([scheme], 1, 'threat', effect)

    def deplacer_la_menace(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()

        cartes = Worlds.GetThreatLevelFaces(effect)
        sources = [x for x in cartes if x.CastTo(CanPlaceToken).GetTokens('threat') > 0]
        if not sources:
            return
        source = joueur.AskChooseFace(sources, effect, prompt="Move threat from")
        if not source:
            return

        destinations = [x for x in cartes if x != source]
        if not destinations:
            return
        destination = joueur.AskChooseFace(destinations, effect, prompt="Move threat to")
        if not destination:
            return

        # « up to 3 » : jamais plus que ce que la source porte. Le moteur ne
        # sait pas demander un NOMBRE (`AskChooseOneText` demande un choix parmi
        # des libelles) : on propose donc les quantites possibles une par une.
        maximum = min(3, source.CastTo(CanPlaceToken).GetTokens('threat'))
        quantites = list(range(1, maximum + 1))
        nombre = quantites[0] if len(quantites) == 1 else \
            joueur.AskChooseOneText(quantites, [f"Move {n} threat" for n in quantites])
        if not nombre:
            return
        retire = Faces.RemoveTokensOn([source], nombre, 'threat', effect)
        if retire:
            Faces.PlaceTokensOn([destination], retire, 'threat', effect)

    return [
        AbilityFactory.WhenCardRevealed(
            AbilityType.ForcedInterrupt,
            None,
            carte_du_spot_revelee
        ),
        # « Hero Action: Discard a card from hand -> move up to 3 threat from
        # one Spot card with the Threat Level keyword to a different Spot card
        # with the Threat Level keyword. »
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deplacer_la_menace,
            conditions=[
                # Il faut au moins deux cartes a niveau, et de la menace a
                # prendre quelque part : sans quoi l'action ne mene a rien.
                lambda effect, message:
                    len([x for x in Worlds.GetThreatLevelFaces(effect)
                         if x.CastTo(CanPlaceToken).GetTokens('threat') > 0]) > 0
                    and len(Worlds.GetThreatLevelFaces(effect)) >= 2
            ],
        ).SetCostFunc(CostFunc.Discard("YourHandCards")),
    ]
