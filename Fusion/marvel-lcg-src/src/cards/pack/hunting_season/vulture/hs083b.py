from . import *

# hs083b Aerial Mayhem
# Forced Response : apres qu'un de vos personnages sans AERIAL a pare et retire de la menace ici,
# 1 degat a ce personnage ou 1 menace ici. Complot complete = defaite (regle native).

def GetAbilities() -> Sequence['Ability']:

    def retire_ici(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> bool:
        return effect.this in message.schemes and message.total_remove_threat > 0 \
            and not message.trigger.HasTrait("AERIAL")

    def choisir(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        perso = message.trigger
        joueur = perso.GetControlByPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "1 degat au personnage",
                lambda cibles: effect.this.DealDamage([perso], 1, effect)),
            AbilityFactory.ForChoiceAbility(
                "1 menace sur le complot",
                lambda cibles: effect.this.PlaceThreatOnSchemes([effect.this], 1, effect)),
        )

    return [
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.ForcedResponse, "YouControlCharacter", choisir, conditions=[retire_ici]),
    ]
