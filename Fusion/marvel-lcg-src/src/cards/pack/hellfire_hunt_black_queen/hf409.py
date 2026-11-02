from . import *

# Little Demon (x4). Sbire DEMON HELL, Patrol et Teamwork (DEMON) : desc, natifs (fiche mots-cles/teamwork.md : ne JAMAIS les recoder).
# « Forced Response : After Little Demon attacks and damages you, you are confused. »
# Cartes de reference : hf124 Mutant Supremacy (`AfterUnitAttackAndDamageUnit`), 41029 (`GiveStatus(..., "Confused")`).
# ⚠ « damages YOU » : la cible est l'identite du joueur (un allie qui defend et encaisse ne la desoriente pas).


def GetAbilities() -> Sequence['Ability']:
    def desorienter(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Confused", effect)

    return [AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "This", "You", desorienter)]
