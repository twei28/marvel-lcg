from . import *

# Aided Defense (2/2) — exemplaire physique 2/2, contenu identique a pt003
# (voir ce fichier pour le detail des modeles et des arbitrages, notamment
# la lecture de la fleche comme un COUT et le releve des PV COURANTS).


def GetAbilities() -> Sequence['Ability']:

    def aided_defense(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        epuises = list(effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards)
        if not epuises:
            return

        bonus = 0
        for allie in epuises:
            bonus += max(0, allie.CastTo(Unit2).health)
        if bonus > 0:
            message.GainDEFForThisAttack(bonus, effect)

        def redresser():
            vivants = [x for x in epuises if x.IsInPlay()]
            if vivants:
                Faces.ReadyAll(vivants, effect)

        message.IfYouTakeNoDamage(redresser)

    return [
        AbilityFactory.WhenUnitDefendAgainstAttack(
            AbilityType.HeroInterrupt,
            "YourHero",
            aided_defense,
        ).SetPlay()
        .SetLabel('defense')
        .SetCostFunc(CostFunc.Exhaust("YourAlly")),
    ]
