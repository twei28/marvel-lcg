from . import *

# He Never Made — manigance annexe JOUEUR, cout 1, menace 3*, Victory 0
# Victory 0.
# While He Never Made is in the victory display, Howard the Duck gets +1 THW.
# When Defeated: Each player may shuffle up to 3 cards from their discard pile
#   into their deck. The player who defeated this scheme, may add 1 of those
#   cards, to their hand instead.
#
# Meme montage que hd010/hd011 pour le bonus de zone de victoire et le
# declencheur When Defeated.
#
# « shuffle up to 3 cards from their discard pile into their deck » :
# `player.AskChooseFaces(defausse, (0, 3), effect, ...)` puis
# `Faces.ShuffleAllTo(choisies, player.player_deck, effect)` — modele
# ok001b/kb002 pour le remelange, `range=(0, 3)` pour le « up to 3 » (modele
# ok006, `range=("Zero", 3)`, ici en bornes numeriques puisque
# `AskChooseFaces` prend un couple).
#
# « THE PLAYER WHO DEFEATED this scheme, may add 1 OF THOSE CARDS to their
# hand INSTEAD » : piege `instead` du tableau — la carte ne part PAS dans le
# deck puis en main, elle va en main AU LIEU d'aller dans le deck. Elle est
# donc retiree de la liste a remelanger AVANT le `ShuffleAllTo`, et
# « those cards » designe bien les cartes que CE joueur vient de choisir
# (piege `that <nom>`), pas la defausse entiere.


def GetAbilities() -> Sequence['Ability']:

    def he_never_made_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        vainqueur = message.GetDefeatingPlayer()

        def remelanger(player: 'Player') -> None:
            defausse = list(player.discard_pile.GetAll())
            if not defausse:
                return

            choisies = player.AskChooseFaces(
                defausse, (0, 3), effect,
                forced=False,
                prompt="Shuffle up to 3 cards from your discard pile into your deck",
            )
            if not choisies:
                return

            if player == vainqueur:
                def en_main(targets: Sequence['CardFace']) -> None:
                    Unused(targets)
                    gardee = player.AskChooseFace(choisies, effect)
                    if gardee is not None:
                        choisies.remove(gardee)
                        player.GainCard(gardee, effect)

                player.MayChooseOneAbility(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Add 1 of those cards to your hand instead",
                        en_main,
                    ),
                )

            if choisies:
                Faces.ShuffleAllTo(choisies, player.player_deck, effect)

        Players.ForEachPlayer(effect, remelanger)

    return [
        *BonusDepuisLaZoneDeVictoire(thwart=1),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            he_never_made_defeated,
            has_defeating_player=True,
        ),
    ]
