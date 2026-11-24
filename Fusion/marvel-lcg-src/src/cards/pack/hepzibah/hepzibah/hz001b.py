from . import *
# * Hepzibah, face alter ego. Prefixe `hz`.
#
# Weapons Officer — You may include up to 3 WEAPONS in your deck from aspects other than your chosen aspect.
#   -> regle de DECKBUILDER : `metadata.deckbuilding.hors_aspect` du deck `hepzibah` (quota de 3 cartes [[WEAPON]]), rien a coder ici.
# Response: After you flip to alter-ego, place 2 events in your discard pile on the bottom of your deck.
#
# Cartes de reference : 01019a (`AfterUnitChangeForm(.., to_this_form=True)`), 40044 (`Faces.MoveAllTo`), `Faces.MoveAllToDeck(..,
# "Bottom", ..)`. Le joueur CHOISIT les deux evenements ; s'il n'y en a qu'un, il place celui-la.
def GetAbilities() -> Sequence['Ability']:
    def evenements_defausses(joueur: 'Player') -> List['CardFace']:
        return [f for f in joueur.discard_pile.Get() if Event.IsType(f)]
    def un_evenement(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> bool:
        joueur = effect.GetInitiator()
        return joueur is not None and evenements_defausses(joueur) != []
    def hepzibah(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        for _ in range(2):
            cartes = evenements_defausses(joueur)
            if not cartes:
                return
            choisie = cartes[0] if len(cartes) == 1 else joueur.AskChooseFace(
                cartes, effect, prompt="Place on the bottom of your deck", forced=True)
            if choisie is None:
                return
            Faces.MoveAllToDeck([choisie], joueur.player_deck, "Bottom", effect)
    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            hepzibah,
            to_this_form=True,
            conditions=[un_evenement],
        ),
    ]
