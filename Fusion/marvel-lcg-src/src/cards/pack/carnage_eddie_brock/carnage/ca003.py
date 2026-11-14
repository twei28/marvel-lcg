from . import *

# * Symbiote Hive-Mind : SOUTIEN (LIEU. SYMBIOTE.), cout 1, [mental]. Classe Hero.
# Eddie Brock gets +1 REC.
# Alter-Ego Action: Exhaust this card -> shuffle 1 Carnage card from your discard pile into your deck.
#
# CARTES DE REFERENCE
#  - +1 REC en continu : `ho005` (Gwen Stacy Osborn, « Harry Osborn gets +1 REC ») : `GiveKeywordToInPlayWhenApplyThis(.., control_by="You", recover=1)` (un SOUTIEN, pas un attachement) ;
#    mais le TYPE vise ICI `AlterEgo` et non `Identity` : « Eddie Brock » est un NOM PROPRE, il ne designe que la face alter-ego (RECETTES §3, lecon an002 Sera ; contre-cas en forme heros).
#  - Action alter-ego qui remelange une carte du set depuis la defausse : `bw012` (Cho's Lab, « shuffle a Brawn card from your discard pile into your deck ») :
#    `CardFinder(set_name=..).Checks(joueur.discard_pile.Get())` + `AskChooseFace(.., not_move=True)` + `Faces.ShuffleAllTo`.
#
# TEXTE CONTRE CODE
#  « EDDIE BROCK gets +1 REC » : nom propre = la face alter-ego du joueur qui controle la carte, jamais la face heros (Carnage). « Alter-Ego Action » : `AlterEgoAction` (jouable en forme alter-ego seulement).
#  « Exhaust this card → » : l'epuisement est le COUT (`CostFunc.Exhaust("This")`). « 1 Carnage card » : une carte du SET « Carnage » (ca002-ca013), PAS du set nemesis ;
#    UNE carte, choisie par le joueur. « from YOUR discard pile into YOUR deck » : defausse et deck du joueur, deck remelange (`ShuffleAllTo`).
#  Chiffres : cout 1, +1 REC, 1 carte.


def GetAbilities() -> Sequence['Ability']:

    def remelanger_une_carte_carnage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        candidates = CardFinder(set_name=NOM_CARNAGE).Checks(joueur.discard_pile.Get())
        if not candidates:
            return

        choisie = joueur.AskChooseFace(candidates, effect, not_move=True)
        if choisie is None:
            return
        Faces.ShuffleAllTo([choisie], joueur.player_deck, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            AlterEgo,
            control_by="You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            remelanger_une_carte_carnage,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
