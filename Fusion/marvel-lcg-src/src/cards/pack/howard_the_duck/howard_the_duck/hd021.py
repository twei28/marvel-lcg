from . import *

# Waddle it Be? — OBLIGATION, give to the Howard Duckson player. Boost 2.
# You may flip to alter-ego form. Choose:
# • Exhaust Howard Duckson → remove Waddle it Be? from the game.
# • Remove and shuffle all Howard the Duck side schemes from the victory
#   display into your deck. If no schemes were removed this way, this card
#   gains surge. Discard this obligation.
#
# Modele exact : ok019 (Funeral Rites) et ss017 (Murderer's Guilt), meme
# structure `AbilityFactory.WhenThisObligationGiveToYou` +
# `YouMayFlipToYourAlterEgoForm(player, effect)` + `player.ChooseAbilities`
# a 2 branches (choix FORCE : le texte dit « Choose », pas « you may choose »).
#
# Branche 1 : « Exhaust HOWARD DUCKSON » = la face ALTER-EGO nommement (le
# joueur vient d'etre invite a s'y retourner), donc
# `player.GetIdentity().GetAlterEgoFace()` comme ok019, pas `GetIdentity()`
# tout court. Retrait de la partie : `Faces.RemoveAllFromGame`.
#
# Branche 2 : « all HOWARD THE DUCK side schemes from the victory display »
# — portee restreinte au set « Howard the Duck » (ses trois manigances
# joueur), JAMAIS a toutes les manigances annexes de la zone de victoire :
# la phrase les remelange DANS VOTRE DECK, ce qu'une carte rencontre ne peut
# pas faire. C'est la meme distinction de portee que hd002, documentee dans le
# __init__.py du set. `Faces.ShuffleAllTo(<cartes>, player.player_deck,
# effect)` (modele ok001b/kb002) ; « If NO schemes were removed this way » ->
# `ThisCardGainSurge` (modele ok019, meme branche « si rien n'a bouge »).
# Le « Discard this obligation » final appartient a la SEULE branche 2 (la
# branche 1 la retire du jeu) : `Faces.DiscardAll([this], effect)`.


def GetAbilities() -> Sequence['Ability']:

    def waddle_it_be(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def retirer_du_jeu(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            alter_ego = player.GetIdentity().GetAlterEgoFace()
            Faces.ExhaustAll([alter_ego], effect)
            Faces.RemoveAllFromGame([this], effect)

        def remelanger_les_manigances(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            manigances = ManigancesHowardEnVictoire(effect)
            if manigances:
                Faces.ShuffleAllTo(manigances, player.player_deck, effect)
            else:
                ThisCardGainSurge(effect, None)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Howard Duckson → remove Waddle it Be? from the game",
                retirer_du_jeu,
            ),
            AbilityFactory.ForChoiceAbility(
                "Remove and shuffle all Howard the Duck side schemes from the victory display into your deck",
                remelanger_les_manigances,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            waddle_it_be,
        ),
    ]
