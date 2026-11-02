from . import *

# Psionic Projection. Attachement ILLUSION PSIONIC. « Attach to your identity. Uses (1 illusion counter). As an additional cost for your hero to use a
# basic power, spend a [mental] resource. When Revealed : ... Forced Response : After your hero makes a basic attack or a basic thwart, remove 1
# illusion counter from here. » L'icone du cout est lue contre rm004 (noeuds relies = [mental], `RES=B`).
# Cartes de reference : 13027 (`AdditionalCostToAttack(Hero, CostFunc.Spend(Cost(...)))`), gb011 et 50173 (attaque, contre ET defense : meme libelle
# « additional cost to use a basic power »).
# « basic power » : le Rules Reference 1.8 (p.10) en compte CINQ (ATK, THW, DEF, REC, SCH). Le HEROS n'en a que trois (la forme heros n'a ni
# recuperation ni manigance : `REC` n'existe que sur l'alter-ego, factory.py, et « your hero » exclut l'alter-ego) : attaque, contre ET DEFENSE.
# Le cout est donc pose sur les trois. La Reponse forcee, elle, ne vise que l'attaque et le contre, comme imprime (« basic attack or a basic thwart »).


def GetAbilities() -> Sequence['Ability']:
    def apres_pouvoir(effect: 'Effect', message: 'Message2') -> None:
        RetirerUnCompteurIllusion(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        PoserUnCompteurSiPsionique(),
        AbilityFactory.AdditionalCostToAttack(Hero, CostFunc.Spend(Cost("B")), is_basic_attack=True),
        AbilityFactory.AdditionalCostToThwart(Hero, CostFunc.Spend(Cost("B"))),
        AbilityFactory.AdditionalCostToDefense(Hero, CostFunc.Spend(Cost("B"))),
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.ForcedResponse, "AttachedHero", apres_pouvoir, powers=["ATK", "THW"]),
    ]
