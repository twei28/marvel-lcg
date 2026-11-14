from . import *
# * Infinite Avengers Mansion — soutien. Alter-Ego Action : incline -> place 1 compteur pym sur une carte que tu
# controles (identite et Mansion compris) ET melange dans ton deck 1 carte « identity-specific » de ta defausse (classe Hero du set de ton identite).
def GetAbilities() -> Sequence['Ability']:
    def mansion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        # CORRECTIF (26/10/2026) : « a card you control » inclut l'IDENTITE et le Mansion lui-meme (RR OWNERSHIP AND CONTROL :
        # « Identity cards are owned and controlled by the player playing as that identity ») ; aucun filtre.
        cartes = list(joueur.GetControlCards())
        if cartes:
            cible = cartes[0] if len(cartes) == 1 else joueur.AskChooseFace(cartes, effect)
            Faces.PlaceCountersOn([cible], 1, 'pym', effect)
        set_identite = joueur.GetIdentity().paper.set_name
        specifiques = [face for face in joueur.discard_pile.GetAll()
                       if face.paper.desc.get("Class") == "Hero" and face.paper.set_name == set_identite]
        if specifiques:
            carte = specifiques[0] if len(specifiques) == 1 else joueur.AskChooseFace(specifiques, effect)
            Faces.ShuffleAllTo([carte], joueur.player_deck, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            mansion,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
