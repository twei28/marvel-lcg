from . import *

# Captain Atlas — SBIRE (ensemble Doctor Minerva), unique. KREE. SOLDIER. SCH 2, ATK 1, PV 6.
# [star] Forces Response: After Captain Atlas attacks you, deal yourself a facedown encounter card.
#
# Cartes de reference :
#  - « After Captain Atlas attacks you, deal yourself a facedown encounter card » :
#    `AbilityFactory.AfterEnemyActivatesAgainstYou` (comme Annihilus/Doctor Minerva, mais limite a
#    l'ATTAQUE precisement ici : « attacks », pas « activates » ni « schemes ») : condition sur
#    `message.atk_message is not None`.
#
# ⚠ Mots-pieges : « attacks YOU » = l'attaque seulement (pas une manigance de Captain Atlas, s'il peut en
# faire) ; texte imprime « Forces Response » (faute d'impression), code en Forced Response.


def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        if message.atk_message is None:
            return
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            joueur.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterEnemyActivatesAgainstYou(AbilityType.ForcedResponse, "This", apres_attaque),
    ]
