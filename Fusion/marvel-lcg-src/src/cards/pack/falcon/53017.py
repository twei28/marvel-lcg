from . import *

# * Hugin & Munin

def GetAbilities() -> Sequence['Ability']:

    # « Response: After Hugin & Munin enter play, search the top 10 cards of the
    # encounter deck for a minion and put it into play engaged with you → ready
    # 1 character you control for each icon in that minion's boost area. »
    #
    # La fouille est le COUT, le redressement l'effet. Le redressement exigeait
    # une cible inclinee AU DECLENCHEMENT (`SetTarget(..., canbe_ready=True,
    # range=(1, "All"))`) : avec tous les personnages redresses, la reponse
    # n'etait jamais proposee (signalement Yarro n°47, 03/10/2026). Chaque icone
    # propose desormais un redressement APRES la fouille, comme 53012 Talon Line.
    def hugin_munin(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        faces = effect.cost_func.Get(CostFunc.SearchForCard).searched_faces
        value = FacesCounter.CountTotalBoostStarAndBoost(faces)

        for _ in range(value):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready a character you control",
                    lambda targets:
                        Faces.ReadyAll(targets, effect)
                ).SetTarget("YouControlUnit", canbe_ready=True),
            )


    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            hugin_munin
        ).SetCostFunc(CostFunc.SearchForCard(Minion, "PutIntoPlayEngagedYou", encounter_deck_top=10)),
    ]
