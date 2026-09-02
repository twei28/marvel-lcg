from . import *

# Godbomb — ENVIRONNEMENT, face A d'une carte recto-verso (verso : gb007b
# All-Black Necroverse). Mis de cote au setup, pose en jeu par le complot 2A.
#
# If there are 12[per_hero] or more timer counters here, the players lose the
#   game.
# Hero Action: Discard an ally you control → remove 1 timer counter from here.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Seuil de compteurs qui fait perdre : 39003b (The Champion, pack mojo),
#   `IfThereAreAtLeastCounterHere("10*", 'ratings', ... SetGameOver(False))`.
#   Meme fabrique ici, avec `'timer'` et `"12*"`.
# - Action de heros dont le cout est de defausser un allie : 07020 (Ball and
#   Chain) pour la forme `SetCostFunc`, et `CostFunc.Discard(card_type=Ally,
#   target=...)` pour le cout.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « 12[per_hero] OR MORE » -> "12*", comparaison >=, la fabrique s'en charge.
# « the players LOSE the game » -> `Worlds.SetGameOver(False, effect)`.
# « Discard AN ALLY YOU CONTROL » -> un allie du joueur qui declenche
#   l'action, jamais un allie adverse ni un sbire : c'est un COUT (fleche →),
#   donc l'action n'est pas jouable sans allie.
# « remove 1 timer counter FROM HERE » -> sur cette carte, la seule qui porte
#   des compteurs `timer`.
#
# ⚠ Cette face ne compte que les `timer`. Les `necro` vivent sur le verso, et
#   les deux ne sont jamais en jeu ensemble.


def GetAbilities() -> Sequence['Ability']:

    def retirer_un_timer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(message)

        Faces.RemoveCountersOn([this], 1, 'timer', effect)

    return [
        AbilityFactory.IfThereAreAtLeastCounterHere(
            "12*",
            'timer',
            lambda effect, message: Worlds.SetGameOver(False, effect),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            retirer_un_timer,
        ).SetCostFunc(CostFunc.Discard("YourAlly")),
    ]
