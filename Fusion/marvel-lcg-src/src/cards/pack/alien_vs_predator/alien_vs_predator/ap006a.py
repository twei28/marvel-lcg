from . import *

# Battleground Earth (2A) — COMPLOT PRINCIPAL, stade 2.
# When Revealed: Each player searches the encounter deck and discard pile for a [[YAUTJA]] minion and a [[XENOMORPH]] minion and puts them
#   into play engaged with them. Shuffle the encounter deck.
#
# Cartes de reference :
#  - « search the encounter deck and discard pile for X » : `Search.EncounterCard(.., include_discard_pile=True, trait=, card_type=Minion)`
#    (07001a / tk) ; « puts them into play engaged with them » : `PutIntoPlay(joueur)` + `EngagePlayer` (pd008) ;
#  - « Shuffle the encounter deck » : `Worlds.GetEncounterDeck(effect).Shuffle(effect)` (07001a).
#
# ⚠ Mots-pieges :
#  - « EACH player » : un sbire YAUTJA ET un sbire XENOMORPH par joueur ; rien trouve -> rien (pas de defausse) ;
#  - « puts into play » (pas « reveals ») : aucun « When Revealed » des sbires (Blooded Predator, Predator Elite) ne part.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        for joueur in Worlds.GetPlayers(effect):
            for trait in ("YAUTJA", "XENOMORPH"):
                sbire = Search.EncounterCard(effect, joueur, include_discard_pile=True, trait=trait, card_type=Minion)
                if sbire is not None and sbire.PutIntoPlay(joueur, effect):
                    sbire.CastTo(Minion).EngagePlayer(joueur, effect)
        Worlds.GetEncounterDeck(effect).Shuffle(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
