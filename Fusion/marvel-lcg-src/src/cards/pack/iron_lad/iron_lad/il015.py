from . import *

# * Iron Lad's Suit
# You get +3 hit points.
# Hero Action: Exhaust Iron Lad's Suit → ready Iron Lad.
#
# Bonus de PV sans cible attachee : modele ag009 (agent_13/agent_13/
# ag009.py), `*AbilityFactory.GiveKeywordToAttached("You", health=3)`.
# Redresser l'identite : `Faces.ReadyAll([initiator.GetIdentity()], effect)`
# (modele : iceman/46015.py, fne/60054.py, determination/dt034.py).
#
# CORRECTIF (trouve par test_capacites.py) : `.SetPlay()` marque une
# ability comme LA resolution de mise en jeu de la carte -- juste pour un
# Event, pas pour un Upgrade dont la mise en jeu (attache/pose) est deja
# geree par la classe de base. Le poser ICI faisait echouer
# `Puzzle.PutIntoPlay` (la carte finissait sur le dessus du deck au lieu
# d'etre en jeu). Modele correct d'une Action reguliere sur un Upgrade deja
# en jeu, SANS `.SetPlay()` : Munitions Cache (determination/dt070.py).

def GetAbilities() -> Sequence['Ability']:

    def suit(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ReadyAll([initiator.GetIdentity()], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            suit
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
