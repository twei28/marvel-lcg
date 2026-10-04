from . import *

# * Conan the Barbarian — face heros. ADVENTURER. BARBARIAN. THW 1 / ATK 2 / DEF 2, 11 PV, main 5.
# Born of Battle — Response: After you deal 5 or more damage to an enemy in a
#   phase, place 1 Crom counter on The Cimmerian.
#
# CARTES DE REFERENCE
#  - `AbilityFactory.AfterUnitTookDamage(type, Enemy, op)` (factory/damage.py) :
#    `took_damage` = degats REELLEMENT encaisses (la Toughness les annule,
#    ils ne sont donc pas « dealt »), `source` = la carte qui frappe.
#  - seuil cumule par phase : `FranchitLeSeuil` (conan/__init__.py).
#
# TEXTE CONTRE CODE
#  « you deal » : Conan, ses evenements, ameliorations, ressources ; PAS un
#    allie (Bealit) -- arbitrage utilisateur du 25/09/2026.
#  « 5 or more damage to an enemy in a phase » : cumul PAR ennemi, un seul
#    compteur par ennemi et par phase (insert).

SEUIL = 5


def GetAbilities() -> Sequence['Ability']:

    def franchit(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        joueur = JoueurDe(effect)
        if joueur is None or not SourceDuJoueur(message.source, joueur):
            return False
        return FranchitLeSeuil(joueur, effect, message, message.who_took_damage,
                               message.took_damage, SEUIL, 'degats')

    def born_of_battle(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        Unused(message)
        PoserCrom(JoueurDe(effect), 1, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            Enemy,
            born_of_battle,
            conditions=[franchit],
        ).SetName("Born of Battle"),
        *CapacitesCitadelle(thw=False, atk=True),
    ]
