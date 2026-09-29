from . import *

# * Redwing

def GetAbilities() -> Sequence['Ability']:

    def redwing(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        faces = effect.cost_func.Get(CostFunc.DiscardDeckTopCards).return_discarded_cards
        value = FacesCounter.CountTotalBoostStarAndBoost(faces)

        this.DealDamage(effect.targets, value, effect)
        this.RemoveThreatFromSchemes(effect.targets, value, effect)

    def dessus_visible_sans_icone(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        # FAQ (MC4DB, 29/09/2026) : si la carte du dessus du deck rencontre
        # est VISIBLE et sans icone, le joueur sait que X vaudra 0 : la
        # capacite ne peut pas etre declenchee (elle n'affecterait pas sa cible).
        dessus = Worlds.GetEncounterDeck(effect).GetTop()
        if dessus is None or not dessus.card.state.is_face_up:
            return True
        return FacesCounter.CountTotalBoostStarAndBoost([dessus]) > 0

    def redwing_condition(effect: 'Effect', face: 'CardFace') -> bool:
        if Scheme2.IsReallyType(face):
            return face.threat > 0
        if Enemy.IsReallyType(face):
            return face.health > 0
        return False

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            redwing,
            conditions=[dessus_visible_sans_icone],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.ReturnToHand("This", to_who="Initiator"))
        .SetCostFunc(CostFunc.DiscardDeckTopCards("EncounterDeck", 1))
        .SetTarget("Enemy|Scheme", check_fn=redwing_condition)
    ]

