from . import *

# * Dwayne Taylor — face ALTER-EGO. PV 9, REC 3, main 6. GENIUS.
# Tech Deck — During deck-building you may include up to 4 [[SKILL]] cards in
#   your deck from aspects other than your own.
# Manual — Action: Shuffle X [[SKILL]] cards from your hand into your deck ->
#   draw X cards. (Limit once per round.)
#
# Cartes de reference :
#  - **`mw001b`** * Cassandra Webb (pack madame_web) : « You may include
#    allies with ... from any aspect in your deck » — regle de CONSTRUCTION DE
#    DECK, appliquee par le deck-builder et PAS par le moteur, qui ne valide
#    pas les decks. Rien a scripter pour « Tech Deck ». Voir aussi `40001b`
#    * Nathan Summers, meme famille.
#  - `Faces.ShuffleAllTo(faces, joueur.player_deck, effect)` (faces.py:48),
#    modele `bt001b` / `bt006` pour le remelange dans le deck du joueur.
#  - `bt023` / `an001b` pour `initiator.DrawUp(n, effect)`.
#  - `32030b` * Kitty Pride pour `.LimitOncePerRound()`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Shuffle **X** SKILL cards » : X est le nombre de cartes CHOISIES par le
#    joueur, pas un cout paye en ressources. La portee est donc `(1, "All")`
#    sur la main, et c'est le NOMBRE REELLEMENT retenu qui fixe la pioche.
#  - « draw **X** cards » : autant que de cartes remises, jamais un nombre
#    fixe. Lire `len(effect.targets)`, jamais une constante.
#  - « into your **deck** » : remelange dans le DECK, pas dans la defausse.
#    `ShuffleAllTo`, et le melange est fait par la methode elle-meme.
#  - « **SKILL** cards » : le trait, pas le type. Le filtre porte sur la main.
#  - « **Action** » nue : imprimee sur la face civile, elle n'existe donc
#    qu'en forme alter-ego. Rien a conditionner en plus.
#  - « (Limit once per **round**.) » : au round, pas a la phase — l'inverse
#    exact de `nt001a` Varial Heelflip, sur la face d'en dessous.
#  - ⚠ La capacite est un ECHANGE NEUTRE en nombre de cartes : elle ne pioche
#    pas, elle RECYCLE. Son interet est de rendre au deck des SKILL inutiles
#    sur le moment, et de nourrir `nt005` Kickflip et `nt010` Multi-Skilled.


def GetAbilities() -> Sequence['Ability']:

    def manual(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        cartes = list(effect.targets)
        if not cartes:
            return

        Faces.ShuffleAllTo(cartes, initiator.player_deck, effect)
        initiator.DrawUp(len(cartes), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            manual,
        ).SetName("Manual")
        .LimitOncePerRound()
        .SetTarget(CardFinder(trait="SKILL"), from_where=["YourHandCards"], range=(1, "All")),
    ]
