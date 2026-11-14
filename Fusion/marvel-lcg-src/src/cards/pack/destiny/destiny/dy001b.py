from . import *

# * Irene Adler (alter-ego) : MUTANT. PSIONIC. REC 3, main 6, PV 9.
# Setup: Search your deck for a [[PSIONIC]] upgrade and add it to your hand. (Shuffle.)
# Response: After you change to this form, shuffle a [[PSIONIC]] card from your discard pile into your deck.
#
# CARTES DE REFERENCE
#  - `01040b` * T'Challa : `WhenCardSetup("This", op)` + `Search.PlayerCard(include_player_deck=True, trait=, card_type=Upgrade)` + `GainCard` (la recherche melange le deck a la sortie d'une carte).
#  - `27030b` * Miles Morales : `AfterUnitChangeForm(Response, "You", op, to_this_form=True).SetTarget(.., from_where=["YourDiscardPile"])` + `Faces.ShuffleAllTo(effect.targets, joueur.player_deck, effect)`.
#
# TEXTE CONTRE CODE
#  « Setup » : capacite d'identite jouee a la mise en place (pas le mot-cle Setup de carte). « a PSIONIC UPGRADE » : une amelioration seulement (FR 1.2 : amelioration PSIONIQUE). « After you change TO THIS FORM » : le
#    retour en alter-ego, pas le passage en heros. « a PSIONIC card FROM YOUR DISCARD PILE » : n'importe quel type de carte portant le trait.
#  Chiffres : REC 3, main 6, PV 9.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        joueur = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            trait="PSIONIC",
            card_type=Upgrade,
        )
        if face:
            joueur.GainCard(face, effect)

    def retour_en_alter_ego(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        joueur = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, joueur.player_deck, effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            retour_en_alter_ego,
            to_this_form=True,
        ).SetTarget(trait="PSIONIC", from_where=["YourDiscardPile"]),
    ]
