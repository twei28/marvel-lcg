from . import *

# * Endless Greed — pacte BARGAIN. Peril (natif). Capacites communes : `AbilitesDuPacte` (When Revealed attacher/defausser, Response de fin de pacte).
# « Your identity gains +2 hand size. » : `GiveKeywordToAttached(Identity, hand_size=2)` (modele mister_fantastic/mf005).


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesDuPacte(),
        *AbilityFactory.GiveKeywordToAttached(Identity, hand_size=2),
    ]
