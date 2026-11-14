from . import *

# Superhuman Mutants Murdering — MANIGANCE ANNEXE de l'ennemi juré. Menace de depart 6 (fixe, pas par heros), boost 3, [hazard].
# Forced Response: After Donald Pierce activates against you, it activates against you again.
#
# CARTES DE REFERENCE
#  - `11051` Ancient Grudge : `minion.DoActivate(player, effect)` pour faire s'activer un sbire contre un joueur.
#  - `AbilityFactory.AfterEnemyActivatesAgainstYou(type, finder, op)` (`04078` Absorbing Man, `15025` Luminous) : « after X activates
#    against you ».
#
# ⚠ ARBITRAGE PROVISOIRE (voir le gabarit) : le texte est recursif tel qu'imprime (la seconde activation declenche a nouveau la
# Response). Lecture retenue : UNE activation supplementaire par activation d'origine, sans rebond (garde `REACTIVATIONS_EN_COURS`).
# ⚠ « it » = Donald Pierce (le sbire), pas la manigance.


# Garde anti-rebond : une activation DECLENCHEE PAR CETTE MEME carte (`activate_message.by_effect`, l'effet de la Response) ne
# redeclenche pas la Response. Une garde « en cours » (liste, attribut) ne tient pas : les messages d'une activation imbriquee
# sont traites APRES le retour de `DoActivate` (premiere ecriture : 3 attaques au lieu de 2, 9 degats au lieu de 6).


# Journal de MESURE du banc de test (`tools/cas/sunspot_hellfire.py`) : « extra » = une activation supplementaire lancee,
# « ignore » = la Response d'une activation causee par cette carte, volontairement sans effet. Invariant : extra == ignore.
JOURNAL_ACTIVATIONS: List[str] = []


def GetAbilities() -> Sequence['Ability']:

    def superhuman_mutants_murdering(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        pierce = message.trigger
        joueur = message.GetToPlayer()
        if pierce is None or joueur is None or not pierce.IsInPlay():
            return
        par = message.activate_message.by_effect
        if par is not None and par.this is not None and par.this.paper.card_id == effect.this.paper.card_id:
            JOURNAL_ACTIVATIONS.append("ignore")
            return
        JOURNAL_ACTIVATIONS.append("extra")
        pierce.DoActivate(joueur, effect)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(
            AbilityType.ForcedResponse,
            CardFinder(name="Donald Pierce"),
            superhuman_mutants_murdering,
        ),
    ]
