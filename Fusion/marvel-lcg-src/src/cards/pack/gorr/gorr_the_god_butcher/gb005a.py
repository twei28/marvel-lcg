from . import *

# Make Ready the Bomb 2A — COMPLOT PRINCIPAL, face de transition.
#
# When Revealed: Put the set-aside Godbomb environment into play. Shuffle 1
#   copy of the Heroes' Labor treachery into each player's deck. Advance to
#   stage 2B.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Put the set-aside <environnement> into play » : 50087a (Batroc),
#   `SetupCards.PutIntoPlay(effect, name=..., card_type=Environment,
#   flip_to_name=...)`. Le `flip_to_name` garantit qu'on entre par la BONNE
#   face d'une carte recto-verso.
# - « Shuffle 1 copy of <carte> into each player's deck » : campaign_setup.py
#   du pack aoa (Panicked Refugees 45178), qui cree la copie DANS le deck du
#   joueur puis la melange :
#     copy = CardFactory.GenerateCard('45178', player.player_deck, world)
#     Faces.ShuffleAllTo([copy.face], player.player_deck, effect)
#   ⚠ C'est cette creation dans `player.player_deck` qui donne a la carte son
#   DOS DE CARTE JOUEUR (card.py:815-838 : le dos se deduit du proprietaire).
#   Le PDF de l'auteur l'exige noir sur blanc pour Heroes' Labor.
# - « Advance to stage 2B » : rien a coder, cf. gb004a (une face A sans
#   `TargetThreat` avance seule).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « the SET-ASIDE Godbomb environment » -> la carte du `set_aside` du
#   scenario, pas une copie neuve : on la cherche, on ne la fabrique pas.
# « 1 COPY ... into EACH player's deck » -> une copie NEUVE par joueur (les
#   quatre exemplaires physiques), pas une carte deplacee.
# Ordre : environnement d'abord, copies ensuite, avancement en dernier (rendu
#   par le moteur).


def GetAbilities() -> Sequence['Ability']:

    def preparer_la_bombe(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this, message)

        SetupCards.PutIntoPlay(
            effect,
            name=NOM_GODBOMB,
            card_type=Environment,
            flip_to_name=NOM_GODBOMB,
        )

        monde = effect.world
        for joueur in Worlds.GetPlayers(effect):
            copie = CardFactory.GenerateCard("gb021", joueur.player_deck, monde)
            Faces.ShuffleAllTo([copie.face], joueur.player_deck, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            preparer_la_bombe,
        ),
    ]
