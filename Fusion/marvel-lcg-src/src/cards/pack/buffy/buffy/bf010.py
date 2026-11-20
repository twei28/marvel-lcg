from . import *

# Sunnydale Library — SOUTIEN (LOCATION), cout 1, [mental].
# Buffy Summers gets +2 REC.
# Alter-Ego Action: Exhaust Sunnydale Library → choose a player. That player shuffles 1 identity-specific card from their discard pile
# into their deck.
#
# CARTES DE REFERENCE
#  - `mv001b` (Tactical Foresight) : `SetTarget("Players")` pour « choose a player » et `Faces.MoveAllToDeck` / `joueur.AskChooseFace` pour la carte choisie.
#  - `Faces.ShuffleAllTo(faces, joueur.player_deck, effect)` (nt001b) pour « shuffle into their deck » ; `face.IsClass("IdentitySpecific")`
#    (card_player.py:191) pour « identity-specific ».
#  - `GiveKeywordToInPlayWhenApplyThis(<cible>, recover=N)` pour « gets +N REC » (modele ra001b / an002).
#
# TEXTE CONTRE CODE
#  « Buffy Summers gets » -> NOM PROPRE : l'alter-ego seulement (le heros s'appelle Buffy). « +2 REC » -> `recover=2`.
#  « that player shuffles ... from THEIR discard pile » -> la defausse du joueur CHOISI, et c'est LUI qui choisit la carte. « 1 » -> une carte.
#    « identity-specific » = carte de classe Hero (signature). Defausse vide de telles cartes : rien.


def GetAbilities() -> Sequence['Ability']:

    def library(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            if joueur is None:
                continue
            candidates = [f for f in joueur.discard_pile.Get() if ClassCard.IsType(f) and f.IsClass("IdentitySpecific")]
            carte = ChoisirUne(joueur, candidates, effect, "Sunnydale Library : shuffle 1 identity-specific card into your deck")
            if carte is not None:
                Faces.ShuffleAllTo([carte], joueur.player_deck, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=NOM_BUFFY_AE),
            recover=2,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            library,
        ).SetTarget("Players")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
