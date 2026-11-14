from . import *

# Complot principal Battle for the Soul (1B), face B. Hidden Clause : 1[per_hero] carte(s) du dessus du deck en Damnation.
# Forced Response: At the end of your turn, resolve the "Hidden Clause" ability for each BARGAIN attachment you control.
# Hidden Clause - Special: Put 1[per_hero] card(s) from the top of your deck facedown into Damnation.
#
# Cartes de reference : sk192b/sk193b (`AfterPlayerTurnEnd(ForcedResponse, "AnyPlayer", ..)`, le joueur dont le tour finit = `message.GetToPlayer()`),
# gs091 (`WhenResolveSpecialAbility("This", ..)`, resolu par `ResolveSpecialAbility(joueur, effect)`). Fiche hidden-clause.md.
#
# ⚠ Mots-pieges : « FOR EACH BARGAIN attachment YOU control » (une resolution par pacte du joueur dont le tour finit, pas de ceux des autres) ;
# « YOUR deck » = celui du joueur qui resout ; N[per_hero] = N x nombre de joueurs de la partie.


def GetAbilities() -> Sequence['Ability']:
    return [
        *ClauseCachee(1),
    ]
