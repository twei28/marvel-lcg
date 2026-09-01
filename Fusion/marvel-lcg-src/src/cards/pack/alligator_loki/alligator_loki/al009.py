from . import *

# "Alligator Antics" — evenement signature. Cout 0, [wild].
# Action: Ready your identity. Search any deck and discard pile for the Throg
#   minion and put him into play. Search the set-aside area, encounter deck and
#   discard pile area for an attachment that can be attached to a minion and
#   attach it to Throg.
#
# Cartes de reference :
#  - bw021 Imperius Rex! : « find X, put him into play » -> `Search.EncounterCard`
#    puis `PutIntoPlay(joueur, effect)` (qui engage le sbire tout seul,
#    face_on_event.py:169) ;
#  - 45134 Magistrate : un attachement attache depuis hors jeu par
#    `AttachTo2` ;
#  - `Search.SearchForCard` avec `include_player_deck="All"` pour « ANY deck ».
#
# ---------------------------------------------------------------------------
# ARBITRAGE : QUEL THROG ?
#
# Deux cartes « Throg » existent dans le pack : al002, le SBIRE DE JOUEUR
# (4 PV, 0/0, Patrol 1, dans TON deck) et al019, le sbire NEMESIS (dans le
# deck de rencontre). « Search ANY deck and discard pile » couvre les deux.
# Le sens de la carte est un DETOURNEMENT : mettre en jeu un Throg inoffensif
# et lui coller un attachement de rencontre qui, sinon, tomberait sur le vilain
# ou un vrai sbire. Les deux Throgs se pretent a ce jeu, le joueur choisit donc
# parmi ceux qu'il trouve : recherche par `card_ids=["al002", "al019"]`,
# jamais par nom. Si les deux sont trouves, le moteur ouvre le choix.
#
# ⚠ al019 « Forced Interrupt: When this minion would enter play, discard any
# other Throg from play » : mettre al019 en jeu alors qu'al002 est la defausse
# al002. C'est le texte d'al019, pas un effet de cette carte.
#
# ---------------------------------------------------------------------------
# « AN ATTACHMENT THAT CAN BE ATTACHED TO A MINION »
#
# Le moteur ne sait pas lire, sur un attachement encore dans le deck, a quoi
# il s'attachera (sa cible vit dans un `AttachToFaceWhenPutIntoPlay` qui ne
# resout qu'a l'entree en jeu). On propose donc tout `Attachment` de
# rencontre que `CanAttachTo(throg)` accepte (asset.py:69, la limite par
# unite), et le joueur tranche. Un attachement « attach to the villain »
# peut donc etre choisi a tort : c'est au joueur de lire la carte, comme sur
# table. Arbitrage note au journal.
#
# « READY your identity » : `Faces.ReadyAll([identite], effect)`, et non le
# heros seulement : la carte dit « identity », en alter-ego ca marche aussi
# (c'est une « Action », pas une « Hero Action »).

def GetAbilities() -> Sequence['Ability']:

    def alligator_antics(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.ReadyAll([identite], effect)

        throg = Search.SearchForCard(
            effect,
            joueur,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            include_player_deck="All",
            include_player_discard_pile="All",
            card_ids=["al002", "al019"],
        )
        if throg is None:
            return
        throg.PutIntoPlay(joueur, effect)
        if not throg.card.IsOnField():
            return

        attachement = Search.SearchForCard(
            effect,
            joueur,
            include_set_aside=True,
            include_encounter_deck=True,
            include_encounter_discard_pile=True,
            card_type=Attachment,
            finder=CardFinder(
                check_face_fn=lambda face: face.CastTo(Asset2).CanAttachTo(throg),
            ),
        )
        if attachement is not None:
            attachement.CastTo(Attachment).AttachTo2(throg, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            alligator_antics,
        ).SetPlay(),
    ]
