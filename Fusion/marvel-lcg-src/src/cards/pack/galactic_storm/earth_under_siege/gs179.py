from . import *

# Programmed to Obliterate — MANIGANCE ANNEXE (ensemble Destroyer). Hinder 1.
# [star] Boost: If this attack deals excess damage, place it as threat on the main scheme.
#
# Cartes de reference :
#  - « If this attack deals excess damage, place it as threat on the main scheme » : meme effet que le
#    texte imprime de Destroyer lui-meme (gs176/gs177), mais depuis une carte de BOOST plutot que
#    l'attaquant : `WhenCardBecomeBoost` + `message.would_atk_message` + report apres resolution
#    (`RunAt.AfterEnemyActivationEnd`, modele gs083/gs144) + `ExcesVersMenaceSurManigancePrincipale`
#    (earth_under_siege/__init__.py, partagee avec gs176/gs177/gs180).
#
# ⚠ Mots-pieges : « THIS attack » = l'attaque EN COURS qui a revele cette carte comme boost, pas une
# attaque future ; l'exces ne se connait qu'APRES resolution complete de l'attaque (degats calcules), d'ou
# le report. Si la carte n'est pas revelee pendant une ATTAQUE (manigance par exemple), rien ne se passe
# (`would_atk_message` absent).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        atk_message = getattr(message, 'would_atk_message', None)
        if atk_message is None:
            return

        def apres() -> None:
            exces = getattr(atk_message, 'excess_damage', None)
            if exces is None:
                being = getattr(message, 'being_message', None)
                exces = getattr(being, 'excess_damage', 0) or 0
            if exces > 0:
                ExcesVersMenaceSurManigancePrincipale(effect, exces)

        RunAt.AfterEnemyActivationEnd(effect, message.would_message, apres)

    return [
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
