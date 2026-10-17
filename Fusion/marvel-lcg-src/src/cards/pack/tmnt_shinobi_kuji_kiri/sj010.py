from . import *

# Flash Ward (sj010), Kuji-Kiri, evenement DEFENSE SPELL (Inkwire, TMNT Shinobi).
# Hero Interrupt (defense): When a friendly character would take damage, discard the top 2 cards of the
# encounter deck → prevent 1 damage for each icon ([star] and [boost]) in each of the discarded card's boost
# areas.
#
# Cartes de reference : `falcon/53010` Battlefield Awareness (cout « discard the top card of the encounter
# deck » : `CostFunc.DiscardDeckTopCards("EncounterDeck", N)` ; « for each icon ([star] and [boost]) in the
# discarded card's boost area » : `FacesCounter.CountTotalBoostStarAndBoost(cartes defaussees du cout)`) ;
# `nova/28003` Forcefield Projection et `determination/dt046` (« When a friendly character would take damage »,
# `WhenUnitWouldTakeDamage` sur `Friend`, evenement defense : `.SetPlay().SetLabel('defense')`, `PreventDamage`).
# Mot-cle : Boost (`boost.md`).
#
# TEXTE CONTRE CODE
#  ⚠ « would take damage » (tout degat, pas seulement d'attaque) ; « a FRIENDLY character » : heros ou allie.
#  ⚠ « discard the top 2 cards ... → » : la defausse des 2 cartes du deck RENCONTRE est le COUT, payee avant
#    de savoir combien d'icones ; « prevent 1 damage FOR EACH icon ... IN EACH of the discarded card's boost
#    areas » : le total des deux cartes (icones [boost] + etoiles de boost).
#  ⚠ La prevention est plafonnee par les degats (`PreventDamage` ne depasse pas les degats a subir).


def GetAbilities() -> Sequence['Ability']:

    def flash_ward(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        defaussees = effect.cost_func.Get(CostFunc.DiscardDeckTopCards).return_discarded_cards
        valeur = FacesCounter.CountTotalBoostStarAndBoost(defaussees)
        if valeur > 0:
            message.PreventDamage(valeur, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Friend,
            flash_ward,
        ).SetPlay().SetLabel('defense')
        .SetCostFunc(CostFunc.DiscardDeckTopCards("EncounterDeck", 2)),
    ]
