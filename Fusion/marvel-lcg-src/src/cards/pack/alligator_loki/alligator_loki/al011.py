from . import *

# * Butterfly Swamp — support signature. LOCATION. Cout 1, [mental].
# While in alter-ego form, Alligator Loki gets +1 REC.
# Alter-Ego Action: Exhaust Butterfly Swamp → shuffle 1 [[PREPARATION]] card
#   from your discard pile into your deck. Draw 1 card.
#
# Cartes de reference :
#  - 10008 * Banner's Laboratory : « Bruce Banner gets +2 REC » ->
#    `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...), recover=)` ;
#  - 01092 Helicarrier : action de support payee par l'inclinaison,
#    `WhenInYourPlayTurn(type, op).SetCostFunc(CostFunc.Exhaust("This"))` ;
#  - 01067 : « draw a card » -> `DrawUp(1, effect)`.
#
# ⚠ « while in ALTER-EGO form » -> `card_type=AlterEgo` : la face civile
# seulement, celle qui recupere.
# ⚠ ORDRE : le melange D'ABORD, la pioche ENSUITE, c'est ce que la carte
# imprime. Le joueur peut donc repiocher la carte qu'il vient de remelanger.
# ⚠ Aucune carte PREPARATION dans la defausse : la fleche a ete payee, on
# pioche quand meme. « shuffle 1 card » n'est pas une condition de l'action.
# ⚠ « 1 PREPARATION card » : au joueur de choisir laquelle s'il en a
# plusieurs (`AskChooseFace`), les trois Lurking ayant des icones distinctes.

def GetAbilities() -> Sequence['Ability']:

    def butterfly_swamp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        preparations = CardFinder(trait="PREPARATION").Checks(joueur.discard_pile.Get(True))
        if preparations:
            choisie = joueur.AskChooseFace(preparations, effect, prompt="Shuffle into your deck")
            Faces.ShuffleAllTo([choisie or preparations[0]], joueur.player_deck, effect)

        joueur.DrawUp(1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=NOM_HEROS, card_type=AlterEgo),
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            butterfly_swamp,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
