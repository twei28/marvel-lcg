from . import *

# * Mikey's Couch — soutien signature, x1 (11/15). LOCATION. NYC. SEWERS.
# Cout 1, ressource [mental].
# Mikey gets +1 REC.
# Alter-Ego Action: Exhaust Mikey's Couch -> choose up to 2 cards in your
#   discard pile and shuffle them into your deck.
#
# Cartes de reference :
#  - « X gets +1 REC » nominatif : `ncrawler/48003` Kurt's Chapel —
#    `*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...),
#    recover=1)` ;
#  - Action d'alter-ego payee par l'epuisement du soutien :
#    `lady_sif/ls007` Sif's Chambers (`CostFunc.Exhaust("This")`) ;
#  - remelange depuis la defausse : `ls007` —
#    `Faces.ShuffleAllTo(cartes, joueur.player_deck, effect)`, choix de
#    plusieurs cartes : `joueur.AskChooseFaces(pile, (0, 2), effect, prompt=)`
#    (modele `sunfire/sf010`).
#
# ⚠ Mots-pieges :
#  - « Mikey gets +1 REC » : le nom de l'ALTER-EGO (« Mikey », sans l'etoile).
#    Le heros s'appelle « Michelangelo » : le bonus n'a donc d'effet qu'en
#    forme civile, et l'Action est une Action d'alter-ego.
#  - « up to 2 » : de 0 a 2 cartes, choisies dans LA defausse du joueur.
#  - « choose ... and shuffle » : cartes choisies, pas aleatoires ; le deck est
#    melange par ShuffleAllTo.
#  - Le « → » ne couvre que l'epuisement (cout).

def GetAbilities() -> Sequence['Ability']:

    def canape(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        pile = list(joueur.discard_pile.Get(True))
        if not pile:
            return
        choisies = joueur.AskChooseFaces(
            pile, (0, 2), effect, not_move=True,
            prompt="Choose up to 2 cards to shuffle into your deck")
        if choisies:
            Faces.ShuffleAllTo(list(choisies), joueur.player_deck, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Mikey"),
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            canape,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
