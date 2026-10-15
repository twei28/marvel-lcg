from . import *

# * Donatello (face heros) — NINJA. TURTLE. PV 11, ATQ 1, CTR 2, DEF 2, main 5.
# Kashikoi — Action: Spend [mental][mental] resources -> draw 2 cards.
#   (Limit once per round.)
#
# CARTES DE REFERENCE
#  - `wd056b` The Cure : `SetCost(Cost("BB"))` pour « spend [mental][mental]
#    resources » (cout en ressources generees/depensees, pas de carte ciblee).
#  - `03001a` Captain America / `sf001b` : un `AbilityType.Action` sur la FACE
#    d'identite, `.LimitOncePerRound()`.
#  - `mf011` Slippery : `initiator.DrawUp(2, effect)` pour « draw 2 cards ».
#
# TEXTE CONTRE CODE
#  « Action » imprime NU (pas « Hero Action ») : on ecrit ce qui est imprime.
#  La capacite est portee par la face HEROS, donc injouable en alter-ego.
#  « spend [mental][mental] resources » -> Cost("BB") (insert : « 2 cards is
#  almost always a better option then [mental][mental] » ne change rien).
#  « (Limit once per round.) » -> `.LimitOncePerRound()` (carte unique d'un
#  seul joueur : la limite globale vaut la limite par joueur).
#  Insert « Hero Power » : les cartes de defense propres a l'identite portent
#  une ressource [mental] imprimee (td003, td004, td007...) : donnees, pas code.


def GetAbilities() -> Sequence['Ability']:

    def kashikoi(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            kashikoi,
        ).SetName("Kashikoi")
        .SetCost(Cost("BB"))
        .LimitOncePerRound(),
    ]
