from . import *

# « And What Is Theirs... Is Mine. » (Black King, face B), apres le retournement de 2A.
# « Sebastian Shaw gains stalwart while there is more than 5 energy counters on him. » + King's Tactic limitee a 1[par joueur] par round.
# Cartes de reference : tk007a (`GiveKeywordToAttached(Villain, get_new_value=..., ex_change_on_event=OnEvent.Counter(...))`).


def GetAbilities() -> Sequence['Ability']:
    def stalwart(effect: 'Effect', face: 'CardFace', ui: List['CardFace']) -> int:
        return 1 if Energie(face) > 5 else 0

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(SurShaw()),
        *AbilityFactory.GiveKeywordToAttached(
            Villain, get_new_value=stalwart, stalwart=1,
            ex_change_on_event=OnEvent.Counter(SurShaw(), ENERGIE)),
        TactiqueDuRoi(True),
    ]
