from . import *

# * Freedom Ring — ATTACHEMENT (Skrull Elite - Crusader). ITEM. 3 icones de boost.
# Attach to Crusader. If Crusader is not in play, discard cards from the top of the encounter deck
#   until a minion is discarded. Put that minion into play engaged with you and attach this card to
#   it. If you cannot, give the villain 1 facedown boost card.
# Attached minion gains villainous.
#
# Cartes de reference :
#  - « Attach to X. If you cannot ... » : `AttachToFaceWhenPutIntoPlay(finder, if_cannot_operation=...)`
#    (attachment.py) ; le repli reçoit `(effect, joueur)`, joueur = celui qui revele.
#  - « Discard cards until a minion is discarded » : **`sk137`/`sk142`** (`Worlds.DiscardEncounterCardsUntil`,
#    helper `SbireSkrullDuDeckRencontre` de skrull_empire) ; « put into play engaged with you » : **`sk136`**.
#  - « Attached minion gains villainous » : **`sk161`** O.M.N.I.T.R.O.N.I.C.U.S. / **`30037`**
#    (`villainous=1`) via `GiveKeywordToAttached(Minion, villainous=1)`.
#
# ⚠ Mots-pieges : « If CRUSADER is not in play » (un Crusader en jeu : il y est attache, rien d'autre ne
# se passe) ; « until a MINION is discarded » (n'importe quel sbire, pas seulement un Skrull) ; « put THAT
# minion into play ENGAGED WITH YOU » (mis en jeu, pas revele : ses « When Revealed » ne partent pas) ;
# « attach THIS card to it » ; « IF YOU CANNOT » (aucun sbire dans le deck : une carte de boost face
# cachee au mechant) ; la carte reste en jeu apres s'etre attachee au sbire trouve.


def GetAbilities() -> Sequence['Ability']:

    def sans_crusader(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Attachment)
        sbire = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if sbire is not None and MettreEnJeuEngage(effect, sbire, joueur):
            this.AttachTo2(sbire, effect)
        else:
            DonnerBoostAuMechant(effect, 1)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_CRUSADER, card_type=Minion),
            if_cannot_operation=sans_crusader,
        ),
        *AbilityFactory.GiveKeywordToAttached(Minion, villainous=1),
    ]
