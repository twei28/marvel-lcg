from . import *

# * Model V Helmet

def GetAbilities() -> Sequence['Ability']:

    def crise_en_jeu(effect: 'Effect') -> bool:
        for face in Worlds.GetOnFieldCards(effect.this.card.game_area):
            if Scheme2.IsType(face) and face.IsInPlay() and getattr(face, 'crisis', 0):
                return True
        return False

    def casque(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)

        valeur = 2 if crise_en_jeu(effect) else 1
        # « ce complot-la » : la cible est le plan qui vient d'entrer en jeu.
        this.RemoveThreatFromSchemes([message.trigger], valeur, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Rescue"),
            thwart=1,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            SchemeSide2,
            casque,
        ).SetLabel('thwart')
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
