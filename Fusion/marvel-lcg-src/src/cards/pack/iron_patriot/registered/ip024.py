from . import *

# * Daken — SBIRE du deck REGISTERED (11/20). 4 PV, ATQ 2, MNG 2, boost 3.
# AVENGER. ELITE. MUTANT.
# Surge.
# [star] Daken's attacks gain piercing.
# Forced Response: After the villain phase begins, heal 1 damage from Daken.
# Emotional Pheromones — Special: Choose to either stun or confuse up to 2
#   enemies.
#
# ⚠⚠ SURGE SUR UNE CARTE DU DECK REGISTERED. L'insert tranche : « When you
# reveal a minion from the REGISTERED deck, it enters play as a minion first
# and RESOLVES ANY REVEALED EFFECTS. » Surge en fait partie : reveler Daken
# coute donc une carte de rencontre en plus. C'est le prix imprime de sa
# regeneration, on ne l'ecarte pas.
#
# CARTES DE REFERENCE
#  - `04027` * Crossfire : `UnitAttackGainKeyword("This", piercing=True)`.
#  - `05015` et consorts : `Faces.GiveStatus(..., "Stunned"/"Confused", ...)`.
#
# TEXTE CONTRE CODE
#  ⚠ « After the VILLAIN PHASE BEGINS » : le debut de la phase du mechant, une
#    fois par round, que Daken soit sbire ou allie.
#  ⚠ « heal 1 damage FROM DAKEN » : lui-meme, pas un personnage au choix.
#  ⚠ « CHOOSE TO EITHER stun OR confuse » : un seul des deux statuts, le meme
#    pour les deux ennemis. Pas un statut par cible.
#  ⚠ « UP TO 2 enemies » : de 0 a 2, d'ou une plage `(0, 2)`.
#  ⚠ Surge est une BASE NATIVE lue dans `desc`.
#  ⚠⚠ PAS DE `.SetTarget()` SUR CETTE CARTE. Le moteur l'interdit aux ENNEMIS :
#    `Ability.Initialize` leve `assert self.selectors == []` des que la face
#    est un `Enemy` (ability.py:168), et les cartes du deck REGISTERED sont
#    chargees comme des SBIRES. La cible se demande donc DANS l'operation, par
#    `joueur.AskChooseFaces`. Mesure du 09/09/2026, sur `ip021`.


def GetAbilities() -> Sequence['Ability']:

    def regeneration(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        this = effect.this.CastTo(Unit2)
        Unused(message)
        this.HealHealth(1, effect)

    def pheromones(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        ennemis = Worlds.GetOnFieldEnemies(effect)
        if joueur is None or not ennemis:
            return
        cibles = joueur.AskChooseFaces(ennemis, (0, 2), effect,
                                       prompt="Stun or confuse up to 2 enemies")
        if not cibles:
            return
        statut = joueur.AskChooseOneText(["Stunned", "Confused"])
        Faces.GiveStatus(cibles, statut, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.AfterPhaseBegin(
            AbilityType.ForcedResponse,
            "Villain",
            regeneration,
        ),
        SpecialRegistered("Emotional Pheromones", pheromones),
    ]
