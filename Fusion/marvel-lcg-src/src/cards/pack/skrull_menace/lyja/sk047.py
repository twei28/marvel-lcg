from . import *

# Shapeshifter — AMELIORATION, cout 3 [energie]. SUPERPOWER.
# Lyja gets +1 THW.
# Hero Response: After you play a TREACHERY event, exhaust Shapeshifter → ready Lyja.
#
# Cartes de reference :
#  - **`sk044`** (meme dossier) : bonus nomme sur la face heros.
#  - **`60045`** Echo / **`60046`** : `AfterPlayerPlayedCard(HeroResponse, 'You', <finder>,
#    op).SetCostFunc(CostFunc.Exhaust('This'))`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « LYJA gets +1 THW » : face heros seulement.
#  - « After you PLAY a TREACHERY EVENT » : un evenement portant le trait TREACHERY
#    (les quatre evenements de Lyja), JOUE par le joueur (la carte est ensuite dans
#    le deck rencontre : le filtre porte sur la carte jouee, lue au message).
#  - « HERO Response » : forme heros seulement.
#  - « ready LYJA » : l'identite du joueur (face heros).


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        Faces.ReadyAll([effect.GetInitiator().GetIdentity()], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Lyja"), thwart=1),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(trait="TREACHERY", card_type=Event),
            redresser,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
