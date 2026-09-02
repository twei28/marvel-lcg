from . import *

# Welcome to Darkness 3B — COMPLOT PRINCIPAL, face jouable. Seuil 8 par
# joueur, acceleration +1 par joueur, menace de depart 2 par joueur.
#
# Forced Response: After a player's deck runs out of cards, place 4 necro
#   counters on the All-Black Necroverse environment.
# Hero Action: Discard 1 card from your hand at random → remove 1 necro
#   counter from All-Black Necroverse.
# If this stage is completed, the players lose the game.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « After a player's deck runs out of cards » : meme montage a la main que
#   gb001 (modele wc019b), la fabrique `AfterDeckRunOut` ne sachant pas dire
#   « n'importe quel joueur ».
# - Action de heros avec defausse aleatoire en cout : 50090b (Alert Level)
#   pour la forme `WhenInYourPlayTurn(HeroAction, ...)`, et 07020 (Ball and
#   Chain) pour le cout exact : `CostFunc.Discard("RandomHandCard")`, pose par
#   `SetCostFunc` et non par `SetCost` (qui, lui, attend des ressources).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « 4 necro counters » -> 4 fixe, aucune icone joueur.
# « Hero Action » -> action de tour, forme HEROS seulement.
# « Discard 1 card FROM YOUR HAND AT RANDOM » -> c'est un COUT (la fleche →),
#   pas un effet : si la main est vide, l'action n'est pas jouable.
# « remove 1 necro counter FROM ALL-BLACK NECROVERSE » -> sur l'environnement,
#   pas sur ce complot : l'horloge vit ailleurs.


def GetAbilities() -> Sequence['Ability']:

    def est_un_deck_de_joueur(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> bool:
        Unused(effect)
        return message.deck.flags.is_player_deck

    def quatre_necro(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this, message)

        PoserNecro(effect, 4)

    def retirer_un_necro(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this, message)

        env = TrouverNecroverse(effect)
        if env is not None:
            Faces.RemoveCountersOn([env], 1, 'necro', effect)

    return [
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterDeckRunOut,
            [est_un_deck_de_joueur],
            quatre_necro,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            retirer_un_necro,
        ).SetCostFunc(CostFunc.Discard("RandomHandCard")),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
