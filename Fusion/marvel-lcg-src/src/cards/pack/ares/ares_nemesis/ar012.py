from . import *

# * Athena — SBIRE nemesis. SCH 3 / ATK 2 / 6 PV. ELITE. OLYMPUS. 1 boost.
# Retaliate 1. Toughness.
# Athena cannot have TACTIC upgrades attached to her.
# (Ares' nemesis minion.)
# [star] Boost: After this activation, deal yourself 1 facedown encounter card.
#
# CARTES DE REFERENCE
#  - `ability_factory.py:178` `ThisCannotHaveCardsAttached` : la regle
#    « cannot have cards attached » ecoute `Message.CheckIfFaceCanAttachTo` et
#    repond `SetCannotAttachTo`. Ici on n'interdit que les ameliorations
#    TACTIC, d'ou une `Ability` ecrite a la main sur le meme message.
#  - `16118` Badoon Grunt : `player.DealEncounterCards(1, effect)`.
#  - `sender_card.py:746` `message.AfterThisActivation(effect, action)` : le
#    « After this activation » d'un texte de boost, execute a la fin de
#    l'activation et non a la revelation.
#
# TEXTE CONTRE CODE
#  ⚠ « Retaliate 1. Toughness. » -> desc, lus par le moteur, aucun module.
#  ⚠ « cannot have TACTIC UPGRADES attached » -> le refus ne porte que sur une
#    amelioration (type Upgrade) portant TACTIC : Ares' Axe n'est pas concerne
#    (il ne s'attache pas a un ennemi de toute facon), une amelioration sans le
#    trait passerait. Aegis Breastplate (ar013, ATTACHEMENT) s'attache a elle
#    sans probleme. C'est la question que pose `PeutSAttacherA` (God of War) :
#    Athena y repond non.
#  ⚠ « deal YOURSELF » -> le joueur contre qui l'activation a lieu,
#    `message.GetAgainstPlayer()`.
#  ⚠ « AFTER this activation » -> `AfterThisActivation`, pas tout de suite : la
#    carte face cachee arrive apres les degats ou la menace de l'activation.


def GetAbilities() -> Sequence['Ability']:

    def refuse_une_tactique(effect: 'Effect', question: 'Message.CheckIfFaceCanAttachTo') -> bool:
        amelioration = getattr(question, "upgrade", None)
        return (getattr(question, "to_face", None) is effect.this
                and amelioration is not None
                and Upgrade.IsType(amelioration)
                and amelioration.HasTrait(TRAIT_TACTIC))

    def une_carte_de_plus(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetAgainstPlayer()
        if not EstJoueur(joueur):
            return

        def distribuer() -> None:
            joueur.DealEncounterCards(1, effect)

        message.AfterThisActivation(effect, distribuer)

    return [
        Ability(
            AbilityType.NonKeyword,
            Message.CheckIfFaceCanAttachTo,
            [refuse_une_tactique],
            lambda effect, question: question.SetCannotAttachTo(effect),
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            une_carte_de_plus,
        ),
    ]
