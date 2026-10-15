from . import *

# * R'kin — SBIRE (Super-Skrull). GENIUS. SKRULL. SCH 2, ATK 1, 2 PV, 2 icones Y.
# When Defeated: Discard cards from the top of the encounter deck until an
#   attachment is discarded. Reveal that card.
#
# Cartes de reference :
#  - **`sk102`** A New Skrull Is Born (scenario 1) : `Worlds.DiscardEncounterCardsUntil(
#    card_type=...)` puis `Reveal` ; filtre `Attachment` au lieu de SKRULL minion.
#  - **`01182`** Hydra Soldier : `WhenUnitBeDefeated(WhenDefeated, "This", op)` ;
#    le joueur qui resout vient du message (`defeating_player`).
#
# ⚠ Mots-pieges : « WHEN DEFEATED » (Une fois vaincu, pas Interruption forcee) ; on
# defausse JUSQU'A un attachement (il est lui aussi defausse, puis revele) ; « that
# card » = l'attachement defausse (il quitte la defausse pour entrer en jeu) ;
# deck epuise : la regle native remelange la defausse et pose un jeton d'acceleration.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.defeating_player or this.GetEngagedPlayer() or Worlds.GetFirstPlayer(effect)
        face = Worlds.DiscardEncounterCardsUntil(effect, card_type=Attachment)
        if face is not None:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
