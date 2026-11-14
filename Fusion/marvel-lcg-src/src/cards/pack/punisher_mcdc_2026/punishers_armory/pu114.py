from . import *

# Punisher's Armory — COMPLOT ANNEXE. Menace de depart 4 par joueur, Boost ★.
# Forced Response : After the villain phase begins, if there is no WEAPON attachment on the villain, discard from the
#   encounter deck until a WEAPON is discarded. Reveal that card.
# When Defeated : Shuffle each WEAPON in the encounter discard pile into the encounter deck.
# ★ Boost : Reveal this card.
#
# Cartes de reference : `AbilityFactory.AfterPhaseBegin(ForcedResponse, "Villain", ...)` (falcon/53011),
# `Worlds.DiscardEncounterCardsUntil(effect, trait=...)`, `Faces.ShuffleAllTo`, gmw 16140 (`RevealThisCard` en Boost),
# jigsaw/pu065.py (`WhenSchemeBeDefeated(WhenDefeated)`).
# ⚠ « no WEAPON ATTACHMENT on the villain » : une arme du paquet (WEAPON, ARMAMENT ou non) attachee au vilain actif ;
# « discard UNTIL a WEAPON is discarded » : toutes les cartes avant sont defaussees aussi, la ARME est revelee (elle
# quitte la defausse) ; pas de WEAPON dans le deck = tout le deck est defausse sans rien reveler.

def GetAbilities() -> Sequence['Ability']:

    def debut_phase(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        vilains = Worlds.GetVillains(effect)
        if not vilains:
            return
        if any(a.HasTrait("WEAPON") for v in vilains for a in v.GetAttachedAttachments()):
            return
        arme = Worlds.DiscardEncounterCardsUntil(effect, trait="WEAPON")
        if arme is not None:
            arme.Reveal(Worlds.GetFirstPlayer(effect), effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        armes = [c for c in Worlds.GetEncounterDiscardPileCards(effect) if c.HasTrait("WEAPON")]
        if armes:
            Faces.ShuffleAllTo(armes, Worlds.GetEncounterDeck(effect), effect)

    return [
        AbilityFactory.AfterPhaseBegin(AbilityType.ForcedResponse, "Villain", debut_phase),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
