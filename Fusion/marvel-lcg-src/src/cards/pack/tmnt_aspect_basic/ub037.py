from . import *

# * Pepperoni — SOUTIEN 2 [physical], aspect Basic (TMNT Aspects, Inkwire). DINOSAUR. PERSONA.
# Uses (3 pep counters).
# Response: After you defeat an enemy or remove the last threat from a scheme, exhaust Pepperoni and remove 1 pep
#   counter from her → you get +1 hand size until the end of the phase.
#
# NOUVELLE. Cartes de reference :
#  - Uses (3 pep) : `desc.Uses = "3,pep"`, lu par le moteur (fiche uses.md : pose des pions ET sortie au dernier
#    pion retire, ne PAS la recoder). Compteur `pep` AJOUTE a `CardFace.COUNTER` (card_face.py).
#  - cout « exhaust X and remove 1 <counter> counter from her » : 47019 Cell Phone,
#    `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 1, '<nom>')`.
#  - « After you remove the last threat from a scheme » : hd014 Ducktective Agency,
#    `AfterUnitDefeatedScheme(<type>, "You", None, ...)`.
#  - « After you defeat an enemy » : `AfterUnitDefeatedUnit(<type>, "You", Enemy, ...)` (meme famille).
#  - « you get +1 hand size until the end of the phase » : 12033 Assess the Situation,
#    `identite.GainUntilPhaseEnd(effect, hand_size=1)`.
# TEXTE CONTRE CODE : « YOU defeat » / « YOU remove » (le joueur, ses personnages) ; « an ENEMY » (vilain ou
#   sbire) ; « a scheme » (principale ou annexe) ; deux declencheurs, UNE capacite au meme cout.


def GetAbilities() -> Sequence['Ability']:

    def pepperoni(effect: 'Effect', message: 'Message2') -> None:
        effect.GetInitiator().GetIdentity().GainUntilPhaseEnd(effect, hand_size=1)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Enemy,
            pepperoni,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'pep')),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.Response,
            "You",
            None,
            pepperoni,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'pep')),
    ]
