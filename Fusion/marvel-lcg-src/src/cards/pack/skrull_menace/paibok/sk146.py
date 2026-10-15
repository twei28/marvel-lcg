from . import *

# Captain Paibok — ATTACHEMENT (Paibok). TITLE. 2 icones de boost + etoile, icone HAZARD (desc).
# Attach to Paibok.
# Hero Action: Resolve the "Boost" ability on each attachment in play that belongs to the
#   Paibok encounter set → discard this card.
# [star] Boost: Heal 2 damage from Paibok.
#
# Cartes de reference :
#  - Attache : **`01100`** Enhanced Ivory Horn (`AttachToFaceWhenPutIntoPlay(CardFinder(name=...))`,
#    helper `AttacherAPaibok`).
#  - Action de heros dont le COUT est un effet : `CostFunc.Custom(None, fn)`, modele `sk086`
#    (Incite Rebellion, meme coffret) ; defausse : `PlayerActionToDiscardThis` (modele 01100).
#  - Boost : **`04136`** Bitter Rival (`WhenCardBecomeBoost("This", ...)`) ; soin :
#    `villain.HealHealth(2, effect)` (modele `sk107`).
#
# ⚠ Mots-pieges : le « → » separe COUT et EFFET : resoudre les Boost est le COUT, « discard this
# card » l'effet ; « each attachment IN PLAY that belongs to the Paibok SET » (Captain Paibok
# compris, sur Paibok OU sur une identite) ; l'icone du milieu de la boite est HAZARD (desc.Hazard 1),
# pas une « icone de heros » (lecture du 15/10/2026, voir defs/paibok_questions.md).


def GetAbilities() -> Sequence['Ability']:

    def cout(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        ResoudreLesBoosts(effect, effect.GetInitiator())
        return True

    def soin(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        paibok = PaibokEnJeu(effect)
        if paibok is not None:
            paibok.HealHealth(2, effect)

    return [
        AttacherAPaibok(),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCostFunc(CostFunc.Custom(None, cout)),
        AbilityFactory.WhenCardBecomeBoost("This", soin),
    ]
