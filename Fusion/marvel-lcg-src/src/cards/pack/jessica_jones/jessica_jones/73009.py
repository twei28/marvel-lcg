from . import *

# * Jessica's Camera — custom « ekAugust »
# Response: After you defeat a side scheme, exhaust Jessica's Camera -> place
#   1 evidence counter here. While Jessica's Camera has at least:
#   (1) Jessica Jones gets +1 DEF.
#   (2) Jessica Jones gets +1 THW.
#   (3) Jessica Jones gets +1 ATK.

def GetAbilities() -> Sequence['Ability']:

    def place_evidence(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        this = effect.this.CastTo(Upgrade)
        Faces.PlaceCountersOn([this], 1, 'evidence', effect)

    def au_moins(seuil: int) -> Any:
        return lambda effect, attach, ui: \
            1 if effect.this.CastTo(Upgrade).GetCounters('evidence') >= seuil else 0

    return [
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            get_new_value=au_moins(1),
            defense=1,
            ex_change_on_event=OnEvent.Counter("This", 'evidence'),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            get_new_value=au_moins(2),
            thwart=1,
            ex_change_on_event=OnEvent.Counter("This", 'evidence'),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            get_new_value=au_moins(3),
            attack=1,
            ex_change_on_event=OnEvent.Counter("This", 'evidence'),
        ),

        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.Response,
            "You",
            SchemeSide2,
            place_evidence,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
