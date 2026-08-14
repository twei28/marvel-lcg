from . import *

# * The Great Web

def GetAbilities() -> Sequence['Ability']:

    def concerne(effect: 'Effect', message: 'Message.CheckIfFaceApplyUniqueRule') -> bool:
        # « The unique rule does not apply to each WEB-WARRIOR character and
        # each card with "Spider" in its title. »
        face = message.which_face
        return face.HasTrait("WEB-WARRIOR") or "spider" in face.name.lower()

    return [
        # `UniqueRuleNotApplyTo` ne sait viser qu'UNE carte, par nom ou par
        # « This » : ici la regle vise une famille, d'ou l'abilite ecrite a la
        # main sur le meme message que la fabrique.
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfFaceApplyUniqueRule,
            [concerne],
            lambda effect, message: message.IgnoreUniqueRule(effect),
        ),
    ]
