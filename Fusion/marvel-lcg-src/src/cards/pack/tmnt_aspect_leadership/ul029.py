from . import *

# * Splinter — ALLIE Leadership (MC Custom Content, Inkwire), cout 2, [mental]. NINJA. RAT.
# THW 1* / ATQ 1* / PV 2.
# Response: After Splinter enters play, look at the top 5 cards of your deck. Add 1 of those cards to your
#   hand, and place the rest on the bottom of your deck in any order.
#
# CARTES DE REFERENCE
#  - `15007` Agatha Harkness : « look at the top 3 cards of your deck. Add 1 of those to your hand and place
#    the rest on the bottom of your deck in any order » = `LookAtDeck(player_deck, N)` +
#    `AskChooseFace` + `GainCard` + `PlaceOnBottomInAnyOrder`. Meme phrase, N = 5.
#  - `03013` Squirrel Girl : `AfterCardEnterPlay(Response, "This", op)`.
#
# TEXTE CONTRE CODE
#  ⚠ « YOUR deck » : le joueur qui controle Splinter.
#  ⚠ « Add 1 » : exactement une carte (s'il en reste au moins une a regarder).
#  ⚠ « the rest on the BOTTOM ... in any order » : sous le deck, pas dessus.
#  ⚠ Unicite : l'allie `tl002` « * Splinter » (kit de Leonardo) porte le meme titre : les deux ne
#    peuvent pas etre en jeu ensemble (regle d'unicite, `CanCoexistWith`). Question ouverte Q-UL-2.


def GetAbilities() -> Sequence['Ability']:

    def splinter(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        joueur = effect.GetInitiator()
        faces = list(joueur.LookAtDeck(joueur.player_deck, 5, effect))
        if not faces:
            return
        face = joueur.AskChooseFace(faces, effect)
        if face:
            faces.remove(face)
            joueur.GainCard(face, effect)

        joueur.PlaceOnBottomInAnyOrder(faces, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            splinter,
        ),
    ]
