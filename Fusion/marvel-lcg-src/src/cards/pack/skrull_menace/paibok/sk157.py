from . import *

# Settling Scores — COMPLOT ANNEXE x2 (Paibok). Menace 2 (fixe), Hinder 2[per_hero], 2 boosts.
# Hinder 2[per_hero].
# Resolve the "Boost" ability on each boost card 1 additional time.
# When Revealed: Shuffle each POWER SKRULL card from the encounter discard pile into the encounter deck.
#
# Cartes de reference :
#  - Hinder : natif (`desc.Hinder`, fiche mots-cles/hinder.md), comme `sk111` Plotting Revenge.
#  - « resolve each ... 1 additional time » : **`gob 02049`** Media Coverage
#    (`ResolveEachWhenRevealedAbilityAdditionalTime` : `AfterPlayerResolveAbility` puis
#    `face.ResolveAbility(...)`) ; ici le Boost n'a pas de fabrique : `AfterCardBecomeBoost` (boost.py:81)
#    puis `ResolveAbility(joueur, AbilityType.Boost, effect, ref_message=message.boost_message)` : le Boost
#    est rejoue AVEC le message d'origine (il voit donc l'attaque ou la manigance en cours).
#  - « Shuffle ... into the encounter deck » : `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)` (modele
#    `sk087`, Overthrow).
#
# ⚠ Mots-pieges : « ON EACH BOOST CARD » = toute carte de boost de toute activation (pas seulement celles
# du set Paibok) ; « 1 ADDITIONAL time » = une seule fois de plus (pas une boucle) ; un Boost ANNULE
# (`is_cancel_boost_ability`) n'est pas rejoue ; une carte sans « Boost » n'a rien a rejouer ; defausse
# rencontre : SEULEMENT les cartes POWER SKRULL.


def GetAbilities() -> Sequence['Ability']:

    def rejouer(effect: 'Effect', message: 'Message.AfterCardBecomeBoost') -> None:
        boost = message.boost_message
        if boost.is_cancel_boost_ability:
            return
        # ⚠ `ResolveAbility` direct SAUTE les conditions de la capacite (« during an attack »,
        # « if this attack is undefended »...) que le moteur evalue avant la 1re resolution : on
        # les rejoue ici avec le message d'origine, sinon un Boost reserve aux attaques partirait
        # aussi sur une manigance (constate en autoplay : Vermin, AttributeError `would_atk_message`).
        boosts = message.trigger.effect.Find(type=AbilityType.Boost)
        if not boosts or not all(condition(boosts[0], boost) for condition in boosts[0].ability.conditions):
            return
        message.trigger.ResolveAbility(boost.GetToPlayer(), AbilityType.Boost, effect, boost)

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        faces = [f for f in Worlds.GetEncounterDiscardPileCards(effect) if f.HasTrait(TRAIT_POUVOIR)]
        if faces:
            Faces.ShuffleAllTo(faces, "EncounterDeck", effect)

    return [
        AbilityFactory.AfterCardBecomeBoost(
            AbilityType.NonKeyword, None, rejouer,
            conditions=[lambda effect, message: message.trigger.effect.Find(type=AbilityType.Boost) != []],
        ),
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
