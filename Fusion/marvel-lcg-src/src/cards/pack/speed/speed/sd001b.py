from . import *

# * Thomas Shepherd (face alter-ego) — custom « CptScorp »
# CIVILIAN. PV 9 / REC 3 / main 6.
# Accelerated Perception — Action: Shuffle 1 event from your discard pile into
#   your deck. Then, draw 1 card. (Limit once per round.)
#
# « Action: » NU (et non « Alter-Ego Action: ») sur une FACE alter-ego ->
# `AbilityType.Action` + `.LimitOncePerRound()`, comme Billy Kaplan (wc001b),
# Kaine Parker (ss001b), Bruce Banner (10001b) et Tony Stark (01029b).
# `AlterEgoAction` designe un autre type d'abilite, reserve aux cartes JOUEUR
# qui doivent declarer ce mode puisqu'elles ne sont pas elles-memes la face
# alter-ego.
#
# Le corps de l'action est l'aide partagee `RemonterUnEvenementEtPiocher`
# (speed/speed/__init__.py) : la phrase imprimee est MOT POUR MOT celle de la
# branche « instead » de sd005 « I'm Out ». Modele de la mecanique : 60014
# Karen Page et ok011 Upanga, meme couple `Search.PlayerCard(
# include_discard_pile=True, finder=...)` + `Faces.ShuffleAllTo(...,
# player.player_deck, ...)`.
#
# Le remelange vise UN EVENEMENT (`CardFinder(card_type=Event)`), pas
# n'importe quelle carte : c'est le mot imprime. La pioche est
# INCONDITIONNELLE (« Then, draw 1 card », pas « if you do ») : defausse sans
# le moindre evenement -> on pioche quand meme.
#
# LES DEUX REGLES TRANSVERSES de l'insert (plafond de 1, balayage de fin de
# phase joueur et son effet) sont ajoutees ICI AUSSI, et pas seulement sur
# sd001a : les compteurs explosifs doivent survivre a un changement de forme,
# et etre balayes meme si Speed finit la phase des joueurs en identite civile.
# Une seule des deux faces est en jeu a la fois : la regle n'est jamais
# appliquee en double. Voir le grand commentaire de speed/speed/__init__.py.


def GetAbilities() -> Sequence['Ability']:

    def accelerated_perception(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        RemonterUnEvenementEtPiocher(effect.GetInitiator(), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            accelerated_perception,
        ).SetName("Accelerated Perception")
        .LimitOncePerRound(),
        *ReglesDesCompteursExplosifs(),
    ]
