from . import *

# * Magneto: Erik Lehnsherr
#
# ⚠ TICKET #107 (02/11/2026) : « Magneto ne s'est pas soigne apres avoir vaincu une sentinelle ». Le degat consequent de son attaque
# est pris APRES l'attaque (`ally.py`, capacite Consequential) : une Reponse « apres qu'il vainc » partait donc quand Magneto etait
# encore intact, `canbe_heal` ne trouvait aucune cible, puis le degat tombait sans que rien le soigne.
# Deux Reponses, une seule des deux se declenche par attaque :
#  - degat consequent a venir -> le soin attend `AfterAllyTakeConsequentialDamage` (modele ud004), sur une attaque qui a vaincu une
#    SENTINEL ;
#  - pas de degat consequent (neutralise) -> le soin part tout de suite, comme avant.

def GetAbilities() -> Sequence['Ability']:

    def magneto(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        this.HealthUnits([this], 1, effect)

    def pas_de_degat_consequent(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        this = effect.this.CastTo(Ally)
        attaque = getattr(message, "would_atk_message", None)
        evite = attaque is not None and attaque.does_not_take_consequential_damage
        return this.attack_consequential_damage <= 0 or evite


    return [
        AbilityFactory.FirstPlayerControlThis(),
        *AbilityFactory.ThisNotCountAllyLimit(),
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.Response,
            "This",
            CardFinder2("SENTINEL", Minion),
            magneto,
            conditions=[pas_de_degat_consequent],
        ).SetTarget("This", canbe_heal=True),
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.Response,
            "This",
            magneto,
            from_performing="Attack",
            defeated_face=CardFinder2("SENTINEL", Minion),
            conditions=[lambda effect, message: effect.this.IsInPlay()],
        ).SetTarget("This", canbe_heal=True),
    ]
