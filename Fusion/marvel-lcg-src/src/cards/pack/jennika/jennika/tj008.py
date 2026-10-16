from . import *

# * Jennika's Bow — AMELIORATION signature, x1. BOW. NINJA. WEAPON. Cout 3, [physical].
# Restricted.
# Hero Action: Exhaust Jennika's Bow -> deal 1 damage to an enemy or remove 1 threat
#   from a scheme.
# Hero Response: After you play an ATTACK or THWART event, ready Jennika's Bow.
#
# Mot-cle : Restricted (mots-cles/restricted.md) : BASE AUTOMATIQUE (`desc`).
#
# Cartes de reference :
#  - le « choose to either deal 1 damage ... or remove 1 threat » :
#    `venomized/vz032` Klyntar Tendrils (`ChooseAbilities` + deux `ForChoiceAbility`,
#    libelles `attack` / `thwart`, cibles Enemy / Scheme2) ;
#  - `ho010` Powered Gauntlets : `CanPlayThisUpgradeCard()` + Hero Action ;
#  - la Reponse : `michelangelo/tm011` — `AfterPlayerPlayedCard(HeroResponse, "You",
#    CardFinder(card_type=Event, ...), op)` ; `traits=[...]` du CardFinder est un
#    OU.
#
# ⚠ Mots-pieges :
#  - « deal 1 damage to an enemy OR remove 1 threat from a scheme » : UN SEUL des deux,
#    au choix (aucun « and ») ;
#  - « play an ATTACK OR THWART event » : un evenement portant l'un des deux
#    traits (OU), type Event seulement ;
#  - « ready JENNIKA'S BOW » : cette carte-ci (`this`), pas une autre arme ;
#  - la Reponse n'est proposee que si l'arc est incline (sinon rien a redresser, et
#    le moteur demanderait pour rien) : filtre dans `conditions`.


def GetAbilities() -> Sequence['Ability']:

    def jennikas_bow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy",
                lambda cibles: this.DealDamage(cibles, 1, effect)
            ).SetLabel('attack').SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 1, effect)
            ).SetLabel('thwart').SetTarget(Scheme2),
        )

    def rearmer_l_arc(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            jennikas_bow,
        ).SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(card_type=Event, traits=["ATTACK", "THWART"]),
            rearmer_l_arc,
            conditions=[lambda effect, message: not effect.this.IsReady()],
        ),
    ]
