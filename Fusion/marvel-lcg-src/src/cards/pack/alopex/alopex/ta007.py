from . import *

# * Mutant Shelter — SOUTIEN signature, x1. LOCATION. NYC. STREETS.
# Cout 1, [mental].
# Your alter-ego gets +2 REC.
# Alter-Ego Action: Exhaust Mutant Shelter -> shuffle the topmost ally in your
#   discard pile into your deck.
#
# Cartes de reference :
#  - « Your alter-ego gets +N REC » : `lj005` * Kamala's Room,
#    `*AbilityFactory.GiveKeywordToAttached("You", recover=N)` (le meme texte,
#    +1 REC) ;
#  - « the topmost ally in your discard pile » : `harry_osborn/ho013`
#    (`joueur.discard_pile.FindTopmost(CardFinder2(...))`) ;
#  - `Faces.ShuffleAllTo([face], joueur.player_deck, effect)` (melange le deck).
#
# Mots-pieges :
#  - « Your ALTER-EGO gets +2 REC » : seulement la forme alter-ego (la bonne
#    forme est lue par `GiveKeywordToAttached("You", ...)` sur l'identite, qui
#    ne s'applique qu'a la face qui a REC) ; a verifier en forme heros ;
#  - « Alter-Ego Action » : AlterEgoAction, forme civile seulement ;
#  - « Exhaust Mutant Shelter -> » : dans le COUT ;
#  - « the TOPMOST ally » : le plus haut de la defausse, sans choix ; sans
#    allie dans la defausse, rien ne se passe (le cout est paye quand meme).


def GetAbilities() -> Sequence['Ability']:

    def remelanger_un_allie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = joueur.discard_pile.FindTopmost(CardFinder(card_type=Ally))
        if face:
            Faces.ShuffleAllTo([face], joueur.player_deck, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            recover=2,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            remelanger_un_allie,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
