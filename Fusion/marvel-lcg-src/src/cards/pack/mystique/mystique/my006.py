from . import *

# * Destiny / Irene Adler (ALLIE) : PSIONIC. X-MEN. Cout 3, PV 2, CTR 1, ATQ 1*, [wild].
# Interrupt: When a boost card is turned faceup during a scheme activation, discard the top card of the encounter deck. You may count the number of boost icons on that card instead. (Limit once per phase.)
#
# CARTES DE REFERENCE
#  - `dy001a` Destiny (hero) : `WhenBoostCardTurnedFaceUp(Interrupt, None, op, ..)` + `LimitOncePerPhase` ; `sender_card.py` (`WhenBoostCardTurnedFaceUp.boost_icons`, `CancelBoostIcons`) pour remplacer le compte d'icones de la carte retournee.
#  - `53004` Bird's Eye View : `Worlds.GetEncounterDeck(effect).GetTop()` + `Faces.DiscardAll` pour « discard the top card of the encounter deck ».
#
# TEXTE CONTRE CODE
#  « during a SCHEME activation » : `while_scheme=True` (jamais une attaque). « discard the top card of the encounter deck » : TOUJOURS, meme si le joueur ne compte pas ses icones (il n'y a pas de « may » sur la defausse).
#    « You MAY count the number of boost ICONS on THAT card INSTEAD » : option ; le compte d'icones de la carte retournee est REMPLACE par celui de la carte defaussee (icones numeriques seulement, pas l'effet [star]),
#    qui reste applique. « Limit once per phase » : `LimitOncePerPhase`. Deck Rencontre vide : rien n'est defausse, la capacite n'a pas d'effet.
#  Chiffres : cout 3, PV 2, CTR 1, ATQ 1.


def GetAbilities() -> Sequence['Ability']:

    def pressentiment(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        joueur = effect.GetInitiator()
        pile = Worlds.GetEncounterDeck(effect)
        if joueur is None or pile.GetSize() == 0:
            return
        dessus = pile.GetTop()
        if dessus is None:
            return
        icones = int(dessus.CountBoostIconsInternal()) if hasattr(dessus, "CountBoostIconsInternal") else 0
        Faces.DiscardAll([dessus], effect)

        def compter_ses_icones(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            message.boost_icons = icones
            if hasattr(message.trigger, "SetBoostIcon"):
                message.trigger.SetBoostIcon(icones, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Count the {icones} boost icon(s) of the discarded card instead",
                compter_ses_icones,
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Interrupt,
            None,
            pressentiment,
            while_scheme=True,
        ).LimitOncePerPhase(),
    ]
