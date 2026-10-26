from . import *
def GetAbilities() -> Sequence['Ability']:
    # « Exhaust Implanted Tools AND ANOTHER TECH upgrade you control » : la seconde carte est UNE AUTRE que celle-ci.
    # ⚠ `CostFunc.Exhaust(trait="TECH", card_type=Upgrade, ...)` seul laisse Implanted Tools dans les candidates : quand elle est la
    # SEULE amelioration TECH en jeu, le moteur propose la ressource (la verification des couts compte la carte elle-meme), puis
    # le paiement echoue (`GameSignal_UndoRequest`) et le pilote reboucle sur la meme question (autoplay `rl`, graines 7 et 8).
    autre_tech = Select.From(
        None,
        finder=CardFinder(trait="TECH", card_type=Upgrade),
        from_where=["YouControlCards"],
        range=(1, 1),
    )
    autre_tech.selector_filter.AddParameter(check_effect_fn=lambda effect, face: face is not effect.this)
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Exhaust(autre_tech)),
    ]
