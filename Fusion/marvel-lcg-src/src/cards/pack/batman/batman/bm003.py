from . import *
# Violent Means — EVENEMENT cout 2 [physical]. ATTACK. SKILL. Hero Action (attack) : deal 2 damage to an enemy. Deal 2 damage to an enemy.
# Reference : 01021 Gamma Slam (`SetLabel('attack')`) ; une cible CHOISIE A CHAQUE coup (sm004 Rapid Strikes) : le joueur peut repartir.
def GetAbilities() -> Sequence['Ability']:
    def violent_means(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        for _ in range(2):
            cible = ChoisirUnEnnemi(joueur, effect)
            if cible is not None:
                this.DealDamage([cible], 2, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, violent_means).SetPlay().SetLabel('attack'),
    ]
