from . import *
# * Hank Pym (alter ego) — « Scientist Supreme » : Action, depense 1 [mental] -> 1 compteur pym sur un
# Size Manipulation ; sinon (aucun en jeu) cherche un Size Manipulation dans le deck et le met en jeu.
def GetAbilities() -> Sequence['Ability']:
    def scientist_supreme(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        joueur = effect.GetInitiator()
        cartes = size_manipulations(joueur)
        if cartes:
            cible = cartes[0] if len(cartes) == 1 else joueur.AskChooseFace(cartes, effect)
            Faces.PlaceCountersOn([cible], 1, 'pym', effect)
            return
        face = Search.PlayerCard(effect, joueur, include_player_deck=True, name="Size Manipulation", card_type=Upgrade)
        if face:
            face.PutIntoPlay(joueur, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            scientist_supreme,
        ).SetCost(Cost("B")).SetName("Scientist Supreme"),
        # Seized Control (hp016) est MIS DE COTE au Setup et non melange au set nemesis.
        AbilityFactory.BeginGameWithSetAside(["hp016"]),
    ]
