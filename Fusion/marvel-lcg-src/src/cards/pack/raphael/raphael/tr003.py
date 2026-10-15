from . import *

# Disarm — EVENEMENT, cout 2, [physical]. THWART. x2.
# Requirement ([physical]).
# Hero Action (thwart): Remove 4 threat from a scheme. You may discard a [[SAI]]
#   upgrade you control to discard an attachment with the text "Hero Action" or
#   "Hero Response" from an enemy.
#
# PHASE A : construit, jamais execute.
#
# MOT-CLE : REQUIREMENT — fiche `docs/reference/mots-cles/requirement.md`.
# BASE AUTOMATIQUE : `desc.Requirement = "R"`. AUCUN SCRIPT. « 2 dont au moins
# 1 physique », pas « 2 + 1 ».
#
# CARTES DE REFERENCE
#  - `sf003` Burning Hands (sunfire) : meme texte, « Remove N threat ... choose
#    an attachment with the text Hero Action / Hero Response and discard it ».
#    Difference de fond : ici c'est OPTIONNEL et il faut PAYER avec une Sai,
#    et l'attachement doit etre « from an ENEMY » (attache a un ennemi), la ou
#    Burning Hands regarde tout le terrain.
#  - `42006` Natural Flight : `SetPlay().SetLabel('thwart').SetTarget(Scheme2)`.
#  - `57062` : « may » + choix de carte via `ForChoiceAbility(...).SetTarget(
#    liste, range=(1, 1), not_move=True)` ; `MayChooseOneAbility` ajoute le
#    « Cancel » (player_action.py:393).
#
# TEXTE CONTRE CODE
#  ⚠ « You MAY discard a SAI upgrade you control TO discard an attachment » :
#    le « to » fait de la Sai le COUT du retrait, et le tout est facultatif.
#    On n'offre le choix que si les DEUX existent (une Sai ET un attachement
#    eligible), et la Sai n'est defaussee que si le joueur accepte.
#  ⚠ « an attachment with the text ... FROM AN ENEMY » -> on balaie les ENNEMIS
#    et leurs `GetAttachedAttachments()` (jamais `GetControlUpgrade`, voir
#    sunfire `EnnemisEnFeu`). Une amelioration attachee a un ennemi (type
#    Upgrade, ex. Burning) n'est PAS un « attachment » au sens des cartes.
#  ⚠ « you control » : Sai sous le controle du joueur (`GetControlUpgrade`).
#  « Remove 4 threat » : inconditionnel, avant le reste.


def GetAbilities() -> Sequence['Ability']:

    def desarmer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 4, effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        sai = SaisSousControle(joueur)
        attachements = [a for e in Worlds.GetOnFieldEnemies(effect)
                        for a in e.GetAttachedAttachments()
                        if AttachementAvecActionDeHeros(a)]
        if not sai or not attachements:
            return

        def defausser_sai_puis_attachement(cibles: Sequence['CardFace']) -> None:
            Faces.DiscardAll(list(cibles), effect)
            choisi = joueur.AskChooseFace(attachements, effect)
            if choisi is not None:
                Faces.DiscardAll([choisi], effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard a SAI upgrade to discard an attachment from an enemy",
                defausser_sai_puis_attachement,
            ).SetTarget(sai, range=(1, 1), not_move=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            desarmer,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
