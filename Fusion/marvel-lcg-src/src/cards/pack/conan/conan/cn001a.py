from . import *

# * Conan the Thief — face heros. ADVENTURER. THIEF. THW 2 / ATK 1 / DEF 2, 11 PV, main 5.
# Rogue's Intuition — Response: After you remove 4 or more threat from a
#   scheme in a phase, place 1 Crom counter on The Cimmerian.
#
# CARTES DE REFERENCE
#  - `AbilityFactory.AfterSchemeRemoveThreat` (factory/scheme.py) : message
#    AfterSchemeRemoveThreat, `value` = menace reellement retiree.
#  - seuil cumule par phase : `FranchitLeSeuil` (conan/__init__.py), voir le
#    commentaire de tete du pack.
#
# TEXTE CONTRE CODE
#  « you remove » : Conan, ses evenements, ameliorations, ressources ; PAS un
#    allie (Bealit). La source est le contre (`would_thw_message.trigger`)
#    quand il y en a un, sinon la carte de l'effet.
#  « 4 or more threat from a scheme in a phase » : cumul PAR manigance, une
#    fois par manigance et par phase (insert : « it is 1 enemy or 1 scheme »).

SEUIL = 4


def GetAbilities() -> Sequence['Ability']:

    def franchit(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> bool:
        joueur = JoueurDe(effect)
        if joueur is None:
            return False
        if message.would_thw_message is not None:
            source = message.would_thw_message.trigger
        else:
            source = message.by_effect.this
        if not SourceDuJoueur(source, joueur):
            return False
        return FranchitLeSeuil(joueur, effect, message, message.trigger,
                               message.value, SEUIL, 'menace')

    def rogues_intuition(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        Unused(message)
        PoserCrom(JoueurDe(effect), 1, effect)

    return [
        AbilityFactory.AfterSchemeRemoveThreat(
            AbilityType.Response,
            Scheme2,
            rogues_intuition,
            conditions=[franchit],
        ).SetName("Rogue's Intuition"),
        *CapacitesCitadelle(thw=True, atk=False),
    ]
