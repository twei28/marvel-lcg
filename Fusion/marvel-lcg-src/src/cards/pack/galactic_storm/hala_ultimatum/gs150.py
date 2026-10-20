from . import *

# House of Fiyero — MANIGANCE ANNEXE (Hala Ultimatum). Menace 4. 3 icones de boost.
# Hinder 1[per_hero].
# When Defeated: Remove 1 hideout counter from Hala. If you cannot, the defeating player may discard an
#   attachment with the text "Hero Action" from an enemy.
#
# Cartes de reference :
#  - Hinder : natif (desc.Hinder, fiche mots-cles/hinder.md).
#  - « When Defeated » d'une manigance annexe : `AbilityFactory.WhenSchemeBeDefeated(WhenDefeated, "This",
#    ..., has_defeating_player=True)` + `message.GetDefeatingPlayer()`, modele 01166 Highway Robbery (type)
#    / jj061021 (`has_defeating_player`).
#  - « Remove 1 hideout counter from Hala. If you cannot, ... » : `RetirerRepli` (hala_ultimatum/__init__.py)
#    rend False si Hala n'a plus de jeton -> branche alternative.
#  - « the defeating player may discard an attachment with the text "Hero Action" from an enemy » :
#    `player.MayChooseOneAbility` + `AbilityFactory.ForChoiceAbility(...).SetTarget(Attachment,
#    with_texts=["Hero Action"], ...)`, modele gmw 16154 Calculate the Odds pour le "may", `CardFinder.KWArgs
#    with_texts` pour filtrer le texte imprime.
#
# ⚠ Mots-pieges : « If you cannot » = seulement si Hala n'a PLUS aucun jeton de repli ; « an attachment ...
# FROM AN ENEMY » (pas de l'identite d'un joueur) ; « may » = le joueur peut refuser meme avec une cible
# valide.


def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        if RetirerRepli(effect, 1):
            return
        joueur = message.GetDefeatingPlayer() or effect.GetInitiator()
        if joueur is None:
            return

        def choisir_attachement(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(cibles, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard an attachment with the text \"Hero Action\" from an enemy",
                choisir_attachement,
            ).SetTarget(Attachment, with_texts=["Hero Action"],
                        check_face_fn=lambda f: Enemy.IsType(getattr(f, 'bind_face', None))),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue, has_defeating_player=True),
    ]
