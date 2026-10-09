from . import *

# Ancient Reptilian Brain

def GetAbilities() -> Sequence['Ability']:

    def rebondir(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        attaque = [t for t in message.damaged_targets if t in Worlds.GetOnFieldFriendlyCharacters(effect)]
        if not attaque:
            return
        touche = attaque[0]
        valeur = touche.attack
        autres = [c for c in Worlds.GetOnFieldFriendlyCharacters(effect) if c is not touche]
        joueur = message.GetAgainstPlayer() or Worlds.GetFirstPlayer(effect)
        if not autres:
            return
        joueur.ChooseAbilities(
            effect,
            *[AbilityFactory.ForChoiceAbility(
                f"{c.name}", lambda cibles, c=c: effect.this.DealDamage([c], valeur, effect))
              for c in autres],
        )

    def confondre(cibles, effect) -> bool:
        heros = effect.GetInitiator().GetIdentity()
        if heros is None or heros.IsConfused():
            return False
        Faces.GiveStatus([heros], "Confused", effect)
        return True

    return [
        AttacherAuLizard(),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedInterrupt, "AttachedVillain", rebondir),
        ActionHeros(None, CostFunc.Custom(None, confondre)),
    ]
