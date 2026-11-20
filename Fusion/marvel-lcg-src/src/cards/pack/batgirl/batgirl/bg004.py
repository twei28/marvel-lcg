from . import *

# Applying Pressure — evenement, cout 2, [energy]. « Hero Action (attack/thwart): Remove 4 threat from a scheme. If you paid for this
# event using only [physical] resources, deal 2 damage to an enemy. If this attack defeats an enemy, draw 1 card. »
# Cartes de reference : `18020` Hit and Run (`SetLabel('attack', 'thwart')`), `10004` Sub-Orbital Leap (`GetPaidResources().OnlyHasColor("R")`).
# ⚠ « If this attack defeats an enemy » : la branche du paiement SEULE inflige les 2 degats (c'est elle « l'attaque »).


def GetAbilities() -> Sequence['Ability']:

    def applying_pressure(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)
        if joueur is None or not SeulementPaye(effect.GetPaidResources(), Icone(effect, "R"), effect):
            return
        cible = ChoisirUnEnnemi(joueur, effect)
        if cible is None:
            return
        this.DealDamage([cible], 2, effect)
        if FaceEstVaincue(cible):
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            applying_pressure,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Scheme2),
    ]
