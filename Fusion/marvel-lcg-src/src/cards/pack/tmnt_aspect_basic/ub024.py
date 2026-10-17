from . import *

# * The Kennel Klub — SOUTIEN 2 [mental], aspect Basic (TMNT Reskins). LOCATION. NYC. STREETS.
# If each of your allies has the [[MUTANIMAL]] or [[NINJA]] trait, increase your ally limit by 1.
# Response: After a [[MUTANIMAL]] or [[NINJA]] ally enters play, exhaust The Kennel Klub → ready a
#   [[MUTANIMAL]] or [[NINJA]] character.
#
# MODIFIEE de 33020 Utopia : X-MEN -> MUTANIMAL ou NINJA (trois fois) ; ressource [mental] au lieu de
# [physical] (desc). Script copie de 33020. `if_each_of_your_allies_has_trait` n'accepte qu'UN trait :
# la condition « MUTANIMAL ou NINJA » passe par `condition=` avec les MEMES evenements de recalcul que
# la fabrique pose pour le trait unique (environment.py : trait des allies + zone des allies).

TRAITS = ["MUTANIMAL", "NINJA"]


def _chaque_allie(effect: 'Effect') -> bool:
    return all(any(a.HasTrait(t) for t in TRAITS) for a in effect.GetInitiator().GetControlAllies())


def GetAbilities() -> Sequence['Ability']:

    def kennel_klub(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            condition=_chaque_allie,
            ally_limit=1,
            change_on_event=Condition.AddEvent(OnEvent.Trait("YourAlly"), OnEvent.PlayAreaCard("YourAlly")),
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            CardFinder(card_type=Ally, traits=TRAITS),
            kennel_klub,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Unit2, traits=TRAITS, canbe_ready=True),
    ]
