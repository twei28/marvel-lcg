from . import *

# Replaced Archenemy — ATTACHEMENT (Expert Skrull). CONDITION. +1 MNG, 2 icones de boost.
# Attached minion gains the SKRULL trait.
# When Revealed: If your nemesis minion is in play, attach this card to it. Then, it activates against you.
#   Otherwise, find your nemesis minion, attach this card to it and reveal it.
#
# Cartes de reference :
#  - « Attach to X » depuis un When Revealed : **`sk098`** Impostor (`this.AttachTo2(cible, effect)`, sans
#    `AttachToFaceWhenPutIntoPlay`).
#  - « nemesis minion in play -> it activates against you, otherwise find it and reveal it » : **`fne 60176`**
#    Unrelenting Hate (`DoActivate` + `Find.Find` / `Reveal`).
#  - « Attached minion gains the SKRULL trait » : `GiveKeywordToAttached(Minion, trait="SKRULL")` (asset.py, param
#    `trait`) ; +1 MNG natif (`SCH+`).
#
# ⚠ Mots-pieges : « YOUR nemesis minion » (celui du joueur qui revele) ; « Then, it activates » : APRES
# l'attache, donc avec le trait SKRULL et le +1 MNG ; le sbire trouve (hors jeu) est REVELE d'abord, puis la carte s'y
# attache (le moteur refuse d'attacher a une carte hors jeu : ecart avec l'ordre imprime « attach ... and reveal it »,
# voir defs/modulaires_questions.md n°8) ; aucun sbire nemesis trouvable : l'attachement n'a pas de cible et est
# defausse ; l'attachement n'agit que sur un SBIRE.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        joueur = message.GetToPlayer()
        sbire = SbireNemesisEnJeu(joueur, effect)
        if sbire is not None:
            this.AttachTo2(sbire, effect)
            sbire.CastTo(Minion).DoActivate(joueur, effect)
            return
        trouve = Find.Find(effect, finder=CardFinder(card_type=Minion, is_nemesis=joueur))
        if trouve is None:
            Faces.DiscardAll([this], effect)
            return
        # Un attachement ne peut pas s'accrocher a une carte encore HORS JEU (AttachTo2 echoue en silence) : le
        # sbire est donc revele d'abord, puis la carte s'y attache (lecture a confirmer, defs/modulaires_questions.md).
        trouve.Reveal(joueur, effect)
        if trouve.IsInPlay():
            this.AttachTo2(trouve, effect)
        else:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *AbilityFactory.GiveKeywordToAttached(Minion, trait="SKRULL"),
    ]
