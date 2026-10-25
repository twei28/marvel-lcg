from . import *

# * Apex Predator — SBIRE unique. ELITE. YAUTJA. SCH 1, ATK 3, PV 7. Boost 2.
# Toughness.
# [star] Apex Predator's attacks gain piercing.
# Forced Response: After a character attacks Apex Predator, discard the top card of the encounter deck. If that card is a treachery, stun the
#   attacker.
#
# Cartes de reference : Toughness natif (`desc`) ; `UnitAttackGainKeyword("This", piercing=True)` (27059) ; la Reponse est mot pour mot
#   55044 God of Lies (`AfterUnitAttackUnit(ForcedResponse, Hero|Ally, "This")`, `DiscardEncounterCards(1)`, `Filter.ByType(.., Treachery)`).
#
# ⚠ Mots-pieges : « a CHARACTER » : heros ou allie ; « stun the ATTACKER » (pas l'identite).


def GetAbilities() -> Sequence['Ability']:

    def attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        cartes = Worlds.DiscardEncounterCards(1, effect)
        if Filter.ByType(cartes, Treachery):
            Faces.GiveStatus([message.attacker], "Stunned", effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, (CardFinder(card_type=Hero) | CardFinder(card_type=Ally)), "This", attaque),
    ]
