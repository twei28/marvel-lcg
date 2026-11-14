from . import *

# * Walker's Chopper — soutien unique, cout 3, ressource [physical]. VEHICLE.
# Alter-Ego Response: After you exhaust John Walker to recover or search for U.S. Agent's Shield, exhaust Walker's
# Chopper → change to hero form, then ready U.S. Agent.
#
# Cartes de reference :
#  - `friend.py` `AfterUnitUseBasicPower(type, "You", op, powers=["REC"])` : « After you recover » par le POUVOIR DE BASE
#    (le message `AfterUnitRecovery` part aussi pour une guerison de carte ET ignore `is_basic_recovery` : le piege de
#    `45015`/`AfterUnitMakeRecovery`, qui declencherait la reponse sans qu'on ait incline l'alter ego).
#  - `resolve.py` `AfterCardResolveAbility(type, which_abilities, which_card, op)` : « After you resolve <l'Action d'une
#    carte> » ; ici l'Action de John Walker (`us001b`), seule Action de l'alter ego.
#  - `01025` Split Personality : `identite.ChangeToOtherIdentityForm(effect)` pour « change to hero form ».
#
# ⚠ Mots-pieges :
#  - « After you EXHAUST John Walker TO recover or TO search » : DEUX declencheurs, deux capacites identiques ; le cout
#    d'inclinaison est paye par la recuperation de base ou par l'Action de `us001b`, pas par d'autres effets.
#  - « Alter-Ego Response » : seulement SOUS la forme alter ego (on est donc John Walker).
#  - « exhaust Walker's Chopper → » : cout d'inclinaison du soutien. « change to hero form, THEN ready U.S. Agent » :
#    l'ordre compte (on redresse la face HEROS, que le changement de forme vient de poser).


def GetAbilities() -> Sequence['Ability']:

    def walkers_chopper(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if AlterEgo.IsType(identite):
            identite.ChangeToOtherIdentityForm(effect)
        Faces.ReadyAll([joueur.GetIdentity()], effect)

    def apres_la_recherche(effect: 'Effect', message: 'Message.AfterEffectResolved') -> bool:
        Unused(effect)
        return message.effect.this.IsName(NOM_ALTER_EGO)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.AlterEgoResponse,
            "You",
            walkers_chopper,
            powers=["REC"],
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterCardResolveAbility(
            AbilityType.AlterEgoResponse,
            ["Action"],
            CardFinder(name=NOM_ALTER_EGO),
            walkers_chopper,
            card_control_by="You",
            conditions=[apres_la_recherche],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
