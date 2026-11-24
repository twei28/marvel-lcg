from . import *

# Countless Numbers — TRAITRISE. Surge. Boost ★ + 1 icone.
# When Revealed : Shuffle each NINJA minion in the encounter discard pile into the encounter deck.
# [star] Boost : Resolve this card's "When Revealed" ability.
#
# Cartes de reference : toafk/anachronauts/11045 (`GetEncounterDiscardPileCards` + `CardFinder2` + `ShuffleAllTo("EncounterDeck")`), shadows_in_the_night/sl010 (boost `ResolveAbility(WhenRevealed)`),
#  fiche mots-cles/surge.md (Surge natif, RR 1.8 : le joueur se distribue une carte face cachee).
# ⚠ Mots-pieges : « each NINJA MINION » (pas les autres cartes NINJA de la defausse : traitrises ou manigances de meme trait) ; la defausse ET le deck sont melanges (le deck de
#  rencontre est remelange avec les sbires). Surge est lu dans `desc`, jamais recode.


def GetAbilities() -> Sequence['Ability']:

    def melanger(effect: 'Effect') -> None:
        faces = CardFinder2("NINJA", Minion).Checks(Worlds.GetEncounterDiscardPileCards(effect))
        Faces.ShuffleAllTo(faces, "EncounterDeck", effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        melanger(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.ResolveAbility([effect.this], message.GetToPlayer(), AbilityType.WhenRevealed, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
