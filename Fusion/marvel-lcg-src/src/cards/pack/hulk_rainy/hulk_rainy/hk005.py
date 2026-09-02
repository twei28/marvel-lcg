from . import *

# Interception — evenement signature, x2 (n/15 = 6 et 7).
# TACTIC. Cout 0, ressource [physical].
# Hero Interrupt: When a treachery is revealed, take 2 damage -> cancel all of
#   its effects and discard it. If you overpaid for this card with a [energy]
#   or [physical] resource, remove 2 threat from a scheme.
#
# Cartes de reference :
#  - `dz013` Velvet Sky / `09007` Protective Ward pour l'annulation :
#    `WhenPlayerRevealCard(HeroInterrupt, "AnyPlayer", Treachery, "All", op)`
#    puis `message.CancelAllEffectsAndDiscardIt(effect)` ;
#  - `dt015` Preparation #2 pour le cout en degats subis
#    (`CostFunc.DealDamage(2, "YourHero")`) ;
#  - `58005` Starstruck pour le surpaiement, transpose en
#    `SurpaiementEnergieOuPhysique` (helper du set, voir __init__.py).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « cancel ALL of its effects » : niveau d'annulation « All », PAS le
#    `CancelWhenRevealedEffect` d'an005, qui ne couvre que le « When
#    Revealed » et laisse passer les mots-cles (Surge compris). Lecon dz013,
#    payee en partie reelle.
#  - « When a treachery is revealed » sans « you » : n'importe quel joueur de
#    la table, d'ou `"AnyPlayer"`. Et sans « from the encounter deck » : pas
#    de `from_encounter=True`, une traitrise revelee autrement compte aussi.
#  - « take 2 damage -> » : la fleche en fait un COUT, paye AVANT l'effet, et
#    ces 2 degats declenchent Anger (hk001a), qui n'a aucun filtre
#    `is_from_attack`. Se proteger avec Interception rend donc 1 degat.
#  - « If you OVERPAID » : la carte coute 0, donc tout paiement est un
#    surpaiement — mais il doit contenir de l'energie ou du physique. Un
#    mental seul ne retire aucune menace.
#  - « remove 2 threat from A SCHEME » : au choix, principale ou annexe, d'ou
#    le `ChooseAbilities` conditionnel plutot qu'un `SetTarget` sur
#    l'abilite, qui exigerait une cible meme sans surpaiement.


def GetAbilities() -> Sequence['Ability']:

    def interception(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)

        message.CancelAllEffectsAndDiscardIt(effect)

        # Cout imprime 0 : tout paiement depasse le cout, mais la couleur
        # depensee doit etre energie ou physique.
        if not SurpaiementEnergieOuPhysique(effect, 0):
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from a scheme",
                lambda cibles: this.RemoveThreatFromSchemes(cibles, 2, effect),
            ).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "All",
            interception,
        ).SetPlay().SetCostFunc(CostFunc.DealDamage(2, "YourHero")),
    ]
