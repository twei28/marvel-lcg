from . import *
# Batarangs — AMELIORATION cout 2 [physical]. ITEM. TECH. Hero Response : after resolving the « When Revealed » effect or boost ability of a
# deterrence card, deal 1 damage to an enemy.
# Reference : resolve.py (`AfterCardResolveAbility`). ⚠ Son filtre `which_abilities` ne connait pas « Boost » : on le laisse vide et la condition
# lit le type de la capacite resolue (WhenRevealed ou Boost).
def GetAbilities() -> Sequence['Ability']:
    def batarangs(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = JoueurDeCetteCarte(effect)
        cible = ChoisirUnEnnemi(joueur, effect) if joueur is not None else None
        if cible is not None:
            this.DealDamage([cible], 1, effect)
    return [
        AbilityFactory.AfterCardResolveAbility(
            AbilityType.HeroResponse, None, CardFinder(trait=TRAIT_DISSUASION), batarangs,
            conditions=[EstUneResolutionDeDissuasion],
        ),
    ]
