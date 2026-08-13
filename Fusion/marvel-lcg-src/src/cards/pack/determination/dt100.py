from . import *

# * Archangel

def GetAbilities() -> Sequence['Ability']:

    # « Alias » est le dernier des cinq mots-cles sans crochet, et sa
    # definition est sur la carte : « si vous controlez une carte au meme
    # sous-titre, defaussez-la et jouez celle-ci gratuitement ». Le moteur sait
    # reduire un cout sous condition ; c'est la defausse simultanee qu'il ne
    # sait pas exiger. APPROXIMATION ECRITE : le cout tombe a zero quand la
    # carte homonyme est en jeu, et le joueur la defausse lui-meme.
    def controle_un_homonyme(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        this = effect.this
        initiator = effect.GetInitiator()
        if initiator is None:
            return False
        sous_titre = this.paper.subtitle
        if not sous_titre:
            return False
        for face in initiator.GetControlCards():
            if face is not this and face.paper.subtitle == sous_titre:
                return True
        return False

    def archangel(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Faces.ReadyAll([message.trigger], effect)

    return [
        Reckless(),
        AbilityFactory.ReduceCostToPlayThis(
            lambda effect: effect.this.printed_cost,
            conditions=[controle_un_homonyme]
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "This",
            retaliate=2,
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            CardFinder(trait="AERIAL"),
            archangel
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
