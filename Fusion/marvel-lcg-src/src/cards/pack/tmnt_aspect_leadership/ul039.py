from . import *

# * Venus « Bonnie » — ALLIE Leadership (TMNT Aspects, Inkwire), cout 3, [mental]. NINJA. TEMPORAL. TURTLE.
# THW 2** / ATQ 2** / PV 3.
# You may play the card attached to Venus as if it were in your hand.
# Response: After Venus enters play, choose a card in your discard pile that shares a [[TRAIT]] with Venus
#   and attach it to her facedown.
#
# MODIFIEE (calquee sur `26013` Jocasta) : « the EVENT attached » -> « the CARD attached » ; « a
# [[Defense]] event » -> « a card ... that shares a TRAIT with Venus ». Script propre copie de 26013.
#
# CARTES DE REFERENCE
#  - `26013` Jocasta : `AttachedCardCanPlayLikeInHand(finder)` + `AfterCardEnterPlay(Response, "This")`,
#    cible dans la defausse (`from_where=["YourDiscardPile"]`), pose face cachee `PlaceCardHere(cibles,
#    False, effect)`.
#  - `vz001` Agent Anti-Venom : « shares a TRAIT with HIM » = `face.ShareTrait(this)` (traits de la carte
#    elle-meme, pas de l'identite).
#
# TEXTE CONTRE CODE
#  ⚠ « the CARD attached » : quel que soit son type (allie, amelioration, soutien, evenement) : aucun filtre.
#  ⚠ « shares a TRAIT with VENUS » : NINJA, TEMPORAL ou TURTLE (traits courants de Venus).
#  ⚠ « YOUR discard pile » ; « attach it to her FACEDOWN ».
#  ⚠ Unicite : l'identite `tv001` « * Venus » porte le meme titre. Question ouverte Q-UL-3.


def GetAbilities() -> Sequence['Ability']:

    def partage_un_trait(effect: 'Effect', face: 'CardFace') -> bool:
        return face.ShareTrait(effect.this)

    def venus(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.PlaceCardHere(effect.targets, False, effect)

    return [
        *AbilityFactory.AttachedCardCanPlayLikeInHand(
            CardFinder(),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            venus,
        ).SetTarget(CardFinder(check_effect_fn=partage_un_trait), from_where=["YourDiscardPile"]),
    ]
