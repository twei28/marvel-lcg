from . import *

# Look Who Finally Showed (2B)

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        valeur = Worlds.ConvertPerPlayerIconToInt("1*", effect)
        Faces.RemoveTokensOn([this], valeur, 'threat', effect)

    return [
        # « After Shocker or Rhino is defeated, remove 1[per_hero] threat from
        # this scheme. » Shocker n'est jamais vaincu pour de bon (il se
        # retourne), mais l'interruption de sa defaite passe quand meme par
        # ici : c'est voulu, le texte parle de la defaite, pas de la mort.
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Unit2,
            vaincu,
            conditions=[
                lambda effect, message:
                    message.trigger.IsName("Shocker") or message.trigger.IsName("Rhino")
            ],
        ),
    ]
