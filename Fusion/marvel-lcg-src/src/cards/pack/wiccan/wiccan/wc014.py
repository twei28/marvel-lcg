from . import *

# Warping Reality — custom « CptScorp »
# Cout 0, [wild], classe Hero, traits SPELL / SUPERPOWER.
# Action: Reduce the cost of the next card played this round by 1+X, where X
#   is the number of boost icons on the top card of the encounter deck.
#
# Mecanisme -> `Worlds.UpdateNextCardPlayCost(player, -valeur, effect,
# in_this=...)` (game/operate/worlds.py:808), la brique unique du depot pour
# « reduce the cost of the next card played ». Modeles : Helicarrier
# (`core/01092.py`, « the next card that player plays this phase ») et Pore
# Over the Evidence (`jessica_jones/on_the_job/jj015.py`, meme brique sur un
# joueur nomme).
#
# « this ROUND » : `in_this="Round"` (portee ajoutee au moteur le 06/10/2026
# pour dz003). Jusqu'au 20/10/2026 ce module prenait `"Phase"` et l'ecart
# etait avoue ici : une carte jouee en reaction pendant la phase du VILAIN
# perdait la reduction. Elle la garde desormais jusqu'a la fin du round (cas
# test_capacites « wc014 Warping Reality — ... TOUT LE ROUND »).
#
# `1+X` -> `1 + IconesBoostDuDessus(...)`. La reduction vaut donc AU MOINS 1,
# meme a 0 icone, meme sur un deck de rencontre vide, meme quand l'obligation
# wc018 a eteint le comptage : le « 1 » est imprime en dur, seul X depend des
# icones. `UpdateNextCardPlayCost` attend une valeur NEGATIVE pour une
# reduction (Helicarrier passe -1), d'ou le `-valeur`.
#
# « Action: » nu -> `AbilityType.Action`, jouable dans les deux formes.

def GetAbilities() -> Sequence['Ability']:

    def warping_reality(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        valeur = 1 + IconesBoostDuDessus(effect, initiator)
        Worlds.UpdateNextCardPlayCost(
            initiator,
            -valeur,
            effect,
            in_this="Round",
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            warping_reality,
        ).SetPlay(),
    ]
