from . import *

# * Aka — SBIRE. HAND. NINJA. ATQ 3* / MNG 1 / PV 6, Boost ★ + 1. Quickstrike. Villainous.
# [star] Interrupt : When Aka would attack you, you may place 1 corruption counter on your Creeping Corruption. If you do, cancel that attack.
# [star] Boost : Choose: Either place 1 corruption counter on your Creeping Corruption, or discard 1 random card from your hand.
#
# Cartes de reference : hunting_season/feral_instincts/hs142 (Interruption FACULTATIVE sur `WhenUnitWouldAttack(..., against_player="You")` + `MayChooseOneAbility`), beast/beast/bt015
#  (`message.CancelThisAttack(effect)`), aoa/clan_akkaba/45162 (boost « Choose: either ... or ... » par `ChooseAbilities`), toafk/anachronauts/11044 (`DiscardRandomHandCards`).
# ⚠ Mots-pieges : « would attack YOU » = le joueur attaque ; « you MAY » : facultatif (fenetre d'Interruption), et sans Creeping Corruption la pose est impossible, donc pas d'annulation ; « if you do » : on
#  n'annule QUE si le compteur a ete pose ; l'activation de Aka n'est pas annulee, seulement le coup (Quickstrike et boost deja donnes) ; boost : la branche « discard random » est
#  masquee quand la main est vide (elle n'aurait aucun effet : echappatoire a la corruption, voir DECISIONS-d.md n°8). Quickstrike et Villainous sont lus dans `desc`.


def GetAbilities() -> Sequence['Ability']:

    def peut_payer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return PeutPoserCorruption(message.GetAgainstPlayer())

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « you may ... If you do, cancel » : l'optionnel est la FENETRE d'Interruption elle-meme (le joueur l'accepte ou la passe), on ne repose donc pas la question ;
        # sans Creeping Corruption la capacite n'est pas offerte (condition), donc jamais d'annulation sans compteur pose.
        if PoserCorruption(effect, message.GetAgainstPlayer(), 1):
            message.CancelThisAttack(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            BrancheCorruption(effect, joueur, 1),
            AbilityFactory.ForChoiceAbility("Discard 1 random card from your hand", lambda cibles: joueur.DiscardRandomHandCards(1, effect),
                                            condition=not MainVide(joueur)),
        )

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, "This", attaque, against_player="You", conditions=[peut_payer]),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
