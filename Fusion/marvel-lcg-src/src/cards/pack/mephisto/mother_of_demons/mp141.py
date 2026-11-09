from . import *

# * Lilith — SBIRE ELITE (MYSTIC). PV 7, ATK 1, SCH 1, Boost 2, Steady 1, Villainous 1 (natifs, `desc`).
# [star] Forced Response : After Lilith activates against you, if Call of the Demoness is in play, put the top card of your discard pile facedown engaged with you as a MYSTIC minion.
#
# Cartes de reference : activate.py `AfterEnemyActivationEnd(.., "This", .., is_against_you=True)`, `MettreEnSbireFaceCachee`.
# ⚠ Mots-pieges : « activates AGAINST YOU » (le joueur vise, pas le premier joueur) ; « IF Call of the Demoness is IN PLAY » ; « YOUR discard pile » ; defausse vide : rien.


def GetAbilities() -> Sequence['Ability']:
    def appel_en_jeu(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> bool:
        return AppelDeLaDemoniaque(effect) is not None

    def engendre(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        joueur = message.GetAgainstPlayer()
        dessus = DessusDeLaDefausse(joueur, 1) if joueur is not None else []
        if dessus:
            MettreEnSbireFaceCachee(effect, joueur, dessus[0])

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, "This", engendre, conditions=[appel_en_jeu], is_against_you=True),
    ]
