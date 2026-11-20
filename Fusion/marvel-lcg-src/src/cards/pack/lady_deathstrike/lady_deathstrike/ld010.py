from . import *

# Deep Wound — OBLIGATION de rencontre (sans « Give to » : va au joueur qui la revele). Boost 2.
# Your hero gets -1 ATK, -1 THW and -1 DEF.
# Response: After you resolve the "Alter-Ego Action" on the copy of Bleeding Out attached to your identity, discard a card from your
#   hand → discard this card.
#
# Cartes de reference :
#  - obligation de set sans « Give to » : `11018` Weakened (Kang), `60184` Wanted (`desc.GiveTo = ""`) ;
#  - malus de heros : `GiveKeywordToInPlayWhenApplyThis(Hero, control_by="You", attack=-1, thwart=-1, defense=-1)` (`64009` pour le
#    `control_by="You"`) ;
#  - « After you resolve the Alter-Ego Action » : `AfterPlayerResolveAbility(..., which_abilities="AlterEgoAction", control_by_you=True)`
#    (`27009`) ; cout `CostFunc.Discard("YourHandCards", range=(1, 1))`.
#
# ⚠ Mots-pieges :
#  - « YOUR hero » : le heros du porteur de l'obligation, forme heros seulement (en alter-ego aucune stat ne bouge) ;
#  - la Response porte sur l'Alter-Ego Action de VOTRE Bleeding Out (ld005), pas sur n'importe quelle action ;
#  - « discard a card → discard this card » : le cout est la defausse d'une carte de la main, l'effet defausse l'obligation.


def GetAbilities() -> Sequence['Ability']:

    def guerir(effect: 'Effect', message: 'Message.AfterEffectResolved') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)

        Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            attack=-1,
            thwart=-1,
            defense=-1,
        ),
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.Response,
            "You",
            CardFinder(card_ids=[ID_SAIGNEMENT]),
            guerir,
            which_abilities="AlterEgoAction",
            control_by_you=True,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
