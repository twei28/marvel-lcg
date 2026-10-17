from . import *

# Ring of Protection (sj007), Kuji-Kiri, amelioration SPELL, unique (Inkwire, TMNT Shinobi).
# Hero Interrupt: When a treachery is revealed, discard this card → cancel all of the effects of that treachery
# and discard it. Discard cards from the top of your deck for each icon ([star] and [boost]) in the discarded
# card's boost area.
#
# Cartes de reference : `drs/doctor_strange/09007` Protective Ward (« When a treachery is revealed from the
# encounter deck, cancel all of its effects and discard it » : `WhenPlayerRevealCard` +
# `message.CancelAllEffectsAndDiscardIt`) ; `falcon/53010` Battlefield Awareness (« for each icon ([star] and
# [boost]) in the discarded card's boost area » : `FacesCounter.CountTotalBoostStarAndBoost`) ; `gmw/16033`
# / `scw/15008` Magic Shield (cout « discard this card » : `CostFunc.Discard("This")`).
# Mot-cle : Boost (`boost.md`) : `desc.Boost` = icones [boost], l'etoile de boost = capacite `[star] Boost`.
#
# TEXTE CONTRE CODE
#  ⚠ « When a treachery is revealed » : SANS « from the encounter deck » (contrairement a 09007) : toute
#    revelation d'une traitrise, par n'importe quel joueur (`from_encounter` laisse a None).
#  ⚠ « discard THIS card → » : la defausse de l'amelioration est le COUT (avant la fleche), pas un effet.
#  ⚠ « cancel ALL of the effects ... and discard it » : `CancelAllEffectsAndDiscardIt` (pas seulement le When
#    Revealed).
#  ⚠ « for each icon ([star] and [boost]) in the DISCARDED card's boost area » : la traitrise annulee, icones
#    [boost] imprimees + l'etoile de boost (1 si elle a un effet [star] Boost) ; defausse de VOTRE deck.
#  ⚠ Icone « Y » du scan = l'icone de boost (comparee au coin de `01099` Charge), pas une ressource.


def GetAbilities() -> Sequence['Ability']:

    def ring_of_protection(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        joueur = effect.GetInitiator()
        traitrise = message.trigger
        # Les icones se lisent AVANT la defausse (la carte est encore celle qu'on a revelee).
        icones = FacesCounter.CountTotalBoostStarAndBoost([traitrise])
        message.CancelAllEffectsAndDiscardIt(effect)
        if joueur is not None and icones > 0:
            joueur.DiscardDeckTopCards(icones, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "AnyPlayer",
            Treachery,
            "All",
            ring_of_protection,
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
