from . import *

# Predator's Prey — TRAITRISE. Boost 1.
# When Revealed: Discard cards from the top of your deck until you discard an ally, then put that ally into play under your control. The
#   active villain attacks that ally. This attack gains overkill.
#
# Cartes de reference : 21055 Summoning Spell (`DiscardDeckUntil(card_type=Ally)` puis `PutIntoPlay`) ; « attacks that ally » :
#   `AttackCharacter(allie, overkill=True)` (brique 16.1).
#
# ⚠ Mots-pieges :
#  - « until you discard an ally » : un Alien Scout rencontre en route est distribue face cachee au lieu d'etre defausse (sa propre
#    Interruption) ; aucun allie dans le deck -> rien ;
#  - « the ACTIVE villain » ; « overkill » : l'exces va a l'identite du controleur (regle de l'allie).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        allie = joueur.DiscardDeckUntil(effect, card_type=Ally)
        if allie is None or not allie.PutIntoPlay(joueur, effect):
            return
        actif = MechantActif(effect)
        if actif is not None and allie.IsInPlay():
            actif.AttackCharacter(allie, effect, overkill=True)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
