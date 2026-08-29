from . import *

# Daniel Hall
#
# "Usage (3 jetons Flouze)" = mot-cle officiel Uses (desc.Uses="3,cash"),
# modele Support Staff (aos/maria_hill/50008.py) : Resource + CostFunc.Exhaust
# + CostFunc.Counter. Uses auto-defausse la carte quand le dernier compteur
# part (has_uses.py) : coherent avec le theme (le contact s'epuise). La
# clause annexe imprimee ("quand vous seriez cense retirer le DERNIER jeton,
# defaussez une carte de votre main") est ajoutee via `ex_operation`, execute
# APRES le paiement du cout (donc APRES le retrait du compteur) : verifier
# `GetCounters('cash') == 0` a ce moment detecte bien "c'etait le dernier".

def GetAbilities() -> Sequence['Ability']:

    def apres_generation(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Support)
        if this.GetCounters('cash') == 0:
            initiator = effect.GetInitiator()
            face = initiator.AskChooseFace(list(initiator.hand_cards.Get()), effect)
            if face:
                Faces.DiscardAll([face], effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            ex_operation=apres_generation,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'cash')),
    ]
