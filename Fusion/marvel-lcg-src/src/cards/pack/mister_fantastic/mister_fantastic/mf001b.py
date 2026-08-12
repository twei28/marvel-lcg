from . import *

# * Reed Richards — custom « DesignHacker »
# Great Minds — Resource: Exhaust Reed Richards -> generate a [mental]
# resource ([mental][mental] instead if Sue Storm is in play). If you paid for
# a TECH card using resources from this ability, ready Reed Richards.
# (Limit once per round.)

def GetAbilities() -> Sequence['Ability']:

    def great_minds(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        if Worlds.FindCardOnField(effect, name="Invisible Woman", card_type=Ally):
            return Resources("BB")
        return Resources("B")

    def redresser_si_tech(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(AlterEgo)

        # CORRECTIF (4/8/2026) : `for_targets` liste les CIBLES de l'effet paye,
        # pas la carte payee. En jouant une amelioration TECH la liste est vide,
        # donc Reed ne se redressait jamais. La carte payee est
        # `message.for_effect.this` (meme montage que Sue Storm iw001b).
        payee = message.for_effect.this
        if payee is not None and payee.HasTrait("TECH"):
            Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=great_minds,
            ex_operation=redresser_si_tech,
        ).SetName("Great Minds")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .LimitOncePerRound(),
    ]
