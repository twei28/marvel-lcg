from . import *

# * The Watchtower : SOUTIEN, cout 3, [energy]. LOCATION.
# You get +2 THW.
# Interrupt: When a balance counter would be placed on Duality Aspect, exhaust this card → place that counter here instead (to a maximum of 1).
#
# CARTES DE REFERENCE
#  - « You get +2 THW » : `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", thwart=2)` (modele `ca003` pour +1 REC, `ra013`).
#  - « When a counter would be placed » : `AbilityFactory.WhenCardWouldBePlacedCounter(Interrupt, CardFinder(name=..), 'balance', op)` (`game/ability/factory/counter.py`) ;
#    remplacer l'evenement : `message.SetBeInstead(effect)` (RECETTES §27).
#  - « place a counter here » : `Faces.PlaceCountersOn([this], 1, 'balance', effect, maximum=1)`.
#
# TEXTE CONTRE CODE
#  « You get +2 THW » : l'identite du joueur (face HEROS : seule face avec un THW). « that counter » : UN compteur ; si l'effet en place plusieurs a la fois (obligation : 3), UN est
#  detourne ici et les autres restent sur Duality Aspect. « to a maximum of 1 » (decision utilisateur du 03/11 : la carte prime sur l'insert qui dit 2) : l'Interruption n'est pas
#  proposee quand la carte porte deja un compteur ou qu'elle est epuisee.
#  Chiffres : cout 3, +2 THW, plafond 1.


# ⚠ LIMITE DE COMPTEURS DE LA TOUR : UNE SEULE constante. QUESTION EN ATTENTE DE LA REPONSE DE L'AUTEUR (Neptune) : la carte imprimee dit « to a maximum of 1 », l'insert et la page de regles A4 disent
# « able to hold up to 2 ». Provisoirement 1 (decision utilisateur du 03/11 : la carte prime). Si l'auteur repond 2 : changer CETTE ligne (le cas de test `tools/cas/sentry.py` la lit) et le texte de `cards.json` (rr005).
WATCHTOWER_MAX_COMPTEURS = 1


def GetAbilities() -> Sequence['Ability']:

    def detourner(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> None:
        this = effect.this
        if message.counters <= 1:
            message.SetBeInstead(effect)
        else:
            message.counters -= 1
        Faces.PlaceCountersOn([this], 1, NOM_EQUILIBRE, effect, maximum=WATCHTOWER_MAX_COMPTEURS)

    def possible(effect: 'Effect', message: 'Message.WhenCardWouldBePlacedCounter') -> bool:
        this = effect.this
        return (message.counters >= 1 and CanPlaceCounter.IsType(this)
                and this.CastTo(CanPlaceCounter).GetCounters(NOM_EQUILIBRE) < WATCHTOWER_MAX_COMPTEURS)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            thwart=2,
        ),
        AbilityFactory.WhenCardWouldBePlacedCounter(
            AbilityType.Interrupt,
            CardFinder(name=NOM_DUALITE),
            NOM_EQUILIBRE,
            detourner,
            conditions=[possible],
        ).SetName("Watchtower").SetCostFunc(CostFunc.Exhaust("This")),
    ]
