from . import *

# * Hank McCoy (alter-ego) : GENIUS. MUTANT. REC 4, main 5, PV 14.
# Setup: Search for Beast's Lab and put it into play under your control.
# Resourceful — Action: Search your deck or discard pile for a resource card and add it to your hand. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `dy001b` (meme famille) : `WhenCardSetup("This", op)` + `Search.PlayerCard(include_player_deck=True, ..)` + `GainCard`.
#  - `face.PutIntoPlay(joueur, effect, under_control=True)` (face_on_event.py:170) pour « put it into play under your control ».
#  - `ma005`/`dz018` : `AbilityType.Action` + `.LimitOncePerPhase()` ; recherche pioche+defausse : `Search.PlayerCard(include_discard_pile=True, card_type=Resource)`.
#
# TEXTE CONTRE CODE
#  « Setup » : capacite d'identite de mise en place. Le Lab porte AUSSI le mot-cle Setup (`desc.Setup`) : il est donc deja en jeu quand cette capacite part, et la recherche ne trouve rien (aucune double entree) ;
#    si le Lab etait encore dans le deck (ordre de mise en place), il entre ici en jeu sous le controle du joueur. « a RESOURCE card » : type Resource, deck OU defausse, ajoutee a la main.
#    « Limit once per PHASE ».
#  Chiffres : PV 14, REC 4, main 5.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None or LabDe(joueur) is not None:
            return
        lab = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            name=NOM_LAB,
            card_type=Support,
        )
        if lab is not None:
            lab.PutIntoPlay(joueur, effect, under_control=True)

    def ressource(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Resource,
        )
        if face is not None:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            ressource,
        ).SetName("Resourceful")
        .LimitOncePerPhase(),
    ]
