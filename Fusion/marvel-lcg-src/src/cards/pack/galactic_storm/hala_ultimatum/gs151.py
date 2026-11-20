from . import *

# Mobilizing the Empire — MANIGANCE ANNEXE (Hala Ultimatum). Menace 4. 2 icones de boost. 2 exemplaires.
# Hinder 1[per_hero].
# When Defeated: Remove 1 hideout counter from Hala. If you cannot, the defeating player may draw 1 card.
#
# Cartes de reference : meme structure que gs150 (voir ce fichier pour le detail) ; branche alternative
# ici plus simple, sans cible : `joueur.DrawUp(1, effect)` dans un `ForChoiceAbility` sans `.SetTarget`
# (modele gmw 16154, deuxieme branche de `calculate_the_odds`).


def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        if RetirerRepli(effect, 1):
            return
        joueur = message.GetDefeatingPlayer() or effect.GetInitiator()
        if joueur is None:
            return
        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Draw 1 card",
                lambda cibles: joueur.DrawUp(1, effect),
            ),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue, has_defeating_player=True),
    ]
