from . import *

# Pure Destruction — TRAITRISE (ensemble Destroyer), x2 exemplaires.
# When Revealed: Deal 3 damage to a character you control. If that character took excess damage that way,
#   place it as threat on the main scheme.
# [star] Boost: If this attack deals excess damage, place it as threat on the main scheme.
#
# Cartes de reference :
#  - « Deal 3 damage to a character you control. If ... took excess damage, place it as threat » :
#    `CardFace.DealDamage(.., if_this_attack_deal_excess_damage=...)` (card_face.py), callback direct vers
#    `ExcesVersMenaceSurManigancePrincipale` (earth_under_siege/__init__.py).
#  - « [star] Boost: If this attack deals excess damage, place it as threat on the main scheme » : meme
#    helper que gs179 Programmed to Obliterate (`WhenCardBecomeBoost` + report + `excess_damage`).
#
# ⚠ Mots-pieges : « a character YOU control » (le joueur qui revele, identite ou allie a lui) ; l'exces de
# la Reponse et celui du Boost sont deux declencheurs INDEPENDANTS (une seule capacite active a la fois
# selon le contexte de revelation).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        cibles = [f for f in joueur.GetControlCards() if Friend.IsType(f)]
        if not cibles:
            return
        cible = joueur.AskChooseFace(cibles, effect) or cibles[0]
        effect.this.DealDamage(
            [cible], 3, effect,
            if_this_attack_deal_excess_damage=lambda exces: ExcesVersMenaceSurManigancePrincipale(effect, exces),
        )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        atk_message = getattr(message, 'would_atk_message', None)
        if atk_message is None:
            return

        def apres() -> None:
            exces = getattr(atk_message, 'excess_damage', 0) or 0
            if exces > 0:
                ExcesVersMenaceSurManigancePrincipale(effect, exces)

        RunAt.AfterEnemyActivationEnd(effect, message.would_message, apres)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
