from . import *

# Secrets of Detention Core — MANIGANCE ANNEXE (Hala Ultimatum). Menace 4. 1 icone de boost.
# Hinder 1[per_hero].
# When Defeated: Remove 1 hideout counter from Hala. If you cannot, the defeating player may ready a
#   character they control.
#
# Cartes de reference : meme structure que gs150/gs151 (voir gs150 pour le detail) ; branche alternative
# ici : `AbilityFactory.ForChoiceAbility(...).SetTarget(Unit2, canbe_ready=True,
# finder=CardFinder(check_face_fn=...))` + `Faces.ReadyAll`, modele 53012 Talon Line (« Ready a character
# you control », `canbe_ready=True`) — `check_face_fn` (sur un `CardFinder`, PAS directement sur
# `Ability.SetTarget`, qui ne le prend pas en parametre -- erreur constatee a l'execution le 20/10/2026,
# corrigee ici) remplace « YouControlUnit » pour viser precisement le joueur qui a vaincu la manigance, qui
# peut differer de l'initiateur de l'effet.
#
# ⚠ Note de transcription : le nom imprime lu sur le scan est « Secrets of Detention Core » ; une fiche
# recapitulative anterieure (INVENTAIRE.md, section 1) l'avait note « Secrets of Detention Cells ». Le nom
# retenu est celui lu directement sur l'image (transcriptions/hala-ultimatum.md), consigne en question
# (voir .planning/todos/2026-10-20-gs6-hala-ultimatum-questions.md).


def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        if RetirerRepli(effect, 1):
            return
        joueur = message.GetDefeatingPlayer() or effect.GetInitiator()
        if joueur is None:
            return

        def rafraichir(cibles: Sequence['CardFace']) -> None:
            Faces.ReadyAll(cibles, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Ready a character you control",
                rafraichir,
            ).SetTarget(Unit2, canbe_ready=True,
                        finder=CardFinder(check_face_fn=lambda f: f.GetControlByPlayer() == joueur)),
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue, has_defeating_player=True),
    ]
