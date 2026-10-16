from . import *

# * Power Play (manigance joueur Linked)

def GetAbilities() -> Sequence['Ability']:

    def hors_limite(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        for face in effect.this.card.printed_faces:
            face.not_count_player_side_scheme_limit = True

    def apres_retrait(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this
        this.RemoveThreatFromSchemes([this], 2, effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        def action(joueur: 'Player') -> None:
            joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun and confuse an enemy",
                    lambda targets: (Faces.GiveStatus(list(targets), "Stunned", effect),
                                     Faces.GiveStatus(list(targets), "Confused", effect))
                ).SetTarget(Enemy),
            )
        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.Temp0, "This", hors_limite),
        # « Hero Response: After you remove threat from this scheme, discard 1 card from
        # your hand -> remove 2 threat from this scheme. »
        AbilityFactory.AfterSchemeRemoveThreat(
            AbilityType.HeroResponse, "This", apres_retrait, by_who="You",
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
