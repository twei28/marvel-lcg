from . import *

# Nova's Psychic Puppetry, face A (CONTROLLED). « Permanent. Hinder 5[per_hero]. Forced Interrupt : When the last threat is removed from this scheme, discard
# each HELLFIRE minion in play and deal each player a facedown encounter card. Then, flip this card. Forced Response : After an ELITE, HELLFIRE minion is
# defeated, remove 5 threat from another side scheme. Otherwise, remove 5 threat from here. »
# Permanent, Hinder 5* et menace de depart 8 : natifs (`desc`). Cartes de reference : 27102a Light at the End (`WhenLastThreatRemoveFromThisScheme` +
# `card.Flip`, Permanent + Hinder), hf501a (`RemoveThreatFromSchemes`).
# ⚠ « each HELLFIRE minion » (pas seulement ELITE) : tous les sbires HELLFIRE en jeu (Hellfire Pawn compris) ; un sbire ELITE HELLFIRE defausse va dans la
# defausse Hellfire (`bind_discard_pile`), les autres dans celle du deck de rencontre.


def GetAbilities() -> Sequence['Ability']:
    def derniere_menace(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        this = effect.this.CastTo(SchemeSide2)
        sbires = [m for m in Worlds.GetOnFieldMinions(effect) if EstSbireHellfire(m)]
        if sbires:
            Faces.DiscardAll(sbires, effect)
        DonnerUneCarteFaceCachee(effect)
        this.card.Flip(effect)

    return [
        AbilityFactory.WhenLastThreatRemoveFromThisScheme(AbilityType.ForcedInterrupt, derniere_menace),
        ReponseSbireEliteVaincu(),
    ]
