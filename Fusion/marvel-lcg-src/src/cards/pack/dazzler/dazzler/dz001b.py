from . import *

# * Alison Blaire
# Setup: Find Live Concert and put it into play under your control.
# Songwriter — Action: Search the top 5 cards of your deck for a SONG event and
#   place it into your hand. (Limit once per round.)
#
# Le Setup reprend `SetupPutIntoPlay`, comme Laura Kinney (43001b) pose les
# griffes de X-23.
#
# « Search the TOP 5 CARDS of your deck » n'est pas une recherche dans tout le
# deck : la fouille est bornee, et ce qui n'est pas pris reste en place.
#
# C'est `Search.SearchForCard` qui fouille, et NON `AskChooseOneText`.
# Signale en jeu : ce dernier ne transporte que des NOMS, et le joueur devait
# choisir entre deux titres qu'il n'avait jamais lus (« je ne sais pas ce que
# les cartes font »). `Search` ouvre la meme fenetre de cartes que Johnny Storm
# (ht001b) ou Baxter Building (mf004) : on VOIT les cinq cartes du sommet, et
# seules les chansons y sont prenables.
#
# `not_move=True` : sans lui le moteur deplace la carte prise, puis MELANGE le
# deck (SelectorEnd.Process). La carte ne demande pas de melanger, et les
# quatre autres doivent rester ou elles sont, dans leur ordre.

PROFONDEUR = 5


def GetAbilities() -> Sequence['Ability']:

    def songwriter(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        # Rien a trouver : on s'arrete AVANT la fouille. Une recherche qui
        # echoue melange le deck (SelectorEnd.OnSelectTargetFailure), ce que
        # cette carte-ci ne doit jamais faire.
        sommet = list(joueur.player_deck.Get(True))[:PROFONDEUR]
        if not any(f is not None and EstUnSong(f) for f in sommet):
            return

        choisie = Search.SearchForCard(
            effect,
            joueur,
            include_player_deck=True,
            most_top=PROFONDEUR,
            trait=TRAIT_SONG,
            card_type=Event,
            not_move=True,
        )
        if choisie is not None:
            Faces.AddToHand([choisie], joueur, effect)

    return [
        # « dz017a,dz017b » et non « dz017a » : c'est UNE carte a DEUX FACES.
        # Posee sur son seul recto, `card.back_faces` reste vide et la Hero
        # Action de Live Concert ne retourne rien : `Card.Flip` (game/card/
        # card.py:770) se rabat alors sur `is_face_up = not is_face_up` et la
        # carte quitte le jeu face cachee. Modele : Betsy Braddock (41001b),
        # qui pose « 41002a,41002b » avec le meme `flip_to_name`.
        AbilityFactory.SetupPutIntoPlay(
            ["dz017a,dz017b"],
            flip_to_name=NOM_CONCERT,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            songwriter,
            conditions=[
                # « You cannot use your Songwriter ability » tant que
                # Performance Anxiety (dz019) est posee chez toi.
                lambda effect, message: not AngoisseEnJeu(effect),
            ],
        ).SetName("Songwriter")
        .LimitOncePerRound(),
    ]
