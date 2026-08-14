from cards.pack.web_of_deceit import *


def DefausserJusquAUneTraitrise(effect: 'Effect', *, avec_boost: bool=False) -> 'CardFace|None':
    """« Discard cards from the top of the encounter deck until a treachery is
    discarded. »

    Le meme Forced Response porte les trois stades d'Electro, au detail pres du
    stade III qui exige une traitrise PORTANT au moins une icone de boost. Le
    filtre par icone n'existe pas dans `CardFinder` : il passe par
    `check_face_fn`, la porte de sortie prevue pour ce genre de critere.
    """
    verification = None
    if avec_boost:
        def verification(face: 'CardFace') -> bool:
            return HasBoostIcon.IsType(face) and face.printed_boost > 0

    return Worlds.DiscardEncounterCardsUntil(
        effect,
        card_type=Treachery,
        check_face_fn=verification,
    )


def JetonsEtIconesDAcceleration(effect: 'Effect') -> int:
    """« for each acceleration token and icon in play »

    Le scenario compte les DEUX : les icones imprimees (`GetAccelerationIcons`)
    et les jetons poses sur les cartes. C'est la mesure qui gouverne le soin du
    vilain (Power Outage 1B), la menace des deux manigances et la difficulte de
    la partie tout entiere.
    """
    total = Worlds.GetAccelerationIcons(effect)
    for face in Worlds.FindCardsOnField(effect):
        if CanAccelerationToken.IsType(face):
            total += face.acceleration_token
    return total


def JetonDAccelerationIci(effect: 'Effect') -> None:
    """« place an acceleration token here » — sur l'attachement lui-meme.

    `CanAccelerationToken` est porte par `EncounterCard`, donc par les
    attachements aussi bien que par les manigances : le jeton peut vivre sur
    Greased Lightning, et le complot principal le comptera quand meme dans son
    escalade.
    """
    effect.this.CastTo(CanAccelerationToken).PlaceAccelerationToken(1, effect)
