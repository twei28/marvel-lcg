from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout, RetournerLAttachement

# Helpers du set Bullseye (Fear No Evil, 60065-60075).


def TrouverBullseye(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, name="Bullseye", card_type=Villain)


def DeadlySaiAttache(effect: 'Effect') -> bool:
    """Deadly Sai (60070) : « Bullseye's attacks lose ranged ». Le ranged est
    accorde par la capacite etoilee de Bullseye lui-meme : c'est elle qui lit
    l'attachement, faute d'un `lost_ranged` dans AttackProperty."""
    bullseye = TrouverBullseye(effect)
    if bullseye is None:
        return False
    return any(a.IsName("Deadly Sai") for a in bullseye.GetAttachedAttachments())


def CapacitesDeBullseye() -> Sequence['Ability']:
    """[star] Forced Interrupt : When Bullseye activates, each of his boost
    cards gains [boost]. If this activation is an attack, it gains ranged.

    - icones : `IncreaseBoostIconsOnEncounterCard` (modele 15024), restreint
      aux cartes qui sont DANS la pile de boost de Bullseye ;
    - ranged : `WhenUnitWouldAttack(ForcedInterrupt, "This")` + GainRanged,
      sauf si Deadly Sai est attache (« lose ranged »).
    """
    # « each of HIS boost cards » : au moment du comptage la carte a quitte sa
    # pile (« deplacee vers la zone de boost », world.area_boosting), on ne peut
    # plus la rattacher a Bullseye par sa zone. On note donc l'ACTIVATION de
    # Bullseye elle-meme (drapeau pose a WhenUnitWouldAttack/Scheme, leve a
    # AfterEnemyActivationEnd) et on n'augmente que pendant celle-ci.
    etat = {"activation": False}

    def carte_boost_de_bullseye(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> bool:
        this = effect.this
        zone = message.trigger.card.area
        return etat["activation"] and (zone is this.components.boostable.GetDeck() or zone is effect.world.area_boosting)

    def debut(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> None:
        etat["activation"] = True

        def fin() -> None:
            etat["activation"] = False

        RunAt.AfterEnemyActivationEnd(effect, message, fin)

    def ranged(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        debut(effect, message)
        if not DeadlySaiAttache(effect):
            message.GainRanged(effect)

    return [
        AbilityFactory.IncreaseBoostIconsOnEncounterCard(conditions=[carte_boost_de_bullseye]),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", ranged),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", debut),
    ]

def RetournerLaColonne(this: 'Attachment', effect: 'Effect') -> None:
    """Adamantium-Laced Spine <-> Damaged Spine : voir RetournerLAttachement
    (cards/pack/fne/__init__.py), commun a tous les attachements recto-verso du
    pack. Sans revelation : aucune des deux faces n'a de When Revealed."""
    RetournerLAttachement(this, effect, call_reveal=False)

