from . import *

# Eternal Manipulation (module Darkhold). Attachement SPELL, SPELL OF DARKHOLD, +1 ATK (desc). « Treat attached ally as a minion with a blank text
# box (except for TRAITS). Attach minion's SCH is equal to its printed THW and it does not take consequential damage. When Revealed : If Darkhold is
# attached to the villain, attached this to your ally with highest hit-point, Remove 1 darkspell counter from Darkhold. Otherwise, find Darkhold
# attachment and reveal it. »
# Cartes de reference : hf324 Mind Manipulation (MEME texte : `TreatAttachedCardAsMinion(Ally, "Minion")`), hp017 Take Over Signal ;
# `ResolutionDeSort` (__init__.py) pour la forme commune des quatre sorts. « highest hit-point » = le plus de PV RESTANTS (comme Hyponotic
# Trance). Aucun allie : la carte ne s'attache pas et est defaussee ; le compteur Darkspell est retire quand meme (QUESTIONS.md n°6).


def GetAbilities() -> Sequence['Ability']:
    def sort(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this
        allies = [f for f in joueur.GetControlCards(CardFinder(card_type=Ally)) if f.IsInPlay()]
        cible = Filter.One(allies, effect, most_remaining_hp=True) if allies else None
        if cible is None:
            Faces.DiscardAll([this], effect)
            return
        this.AttachTo2(cible, effect)

    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Minion"),
        ResolutionDeSort(sort),
    ]
