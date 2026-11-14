from . import *

# Punisher's Hit List (1A) — ENVIRONNEMENT. Setup. Permanent.
# Forced Response : After Punisher defeats a character, add 1 counter here. Then, if there are at least 2+1[per hero]
#   counters here, remove all counters and flip this card.
# Forced Response : After the player phase ends, resolve Punisher's "Punishment" ability, if able.
#
# Cartes de reference : `AbilityFactory.AfterUnitDefeatedUnit(ForcedResponse, ...)` (ar005, sk029),
# `AbilityFactory.AfterPhaseEnd(ForcedResponse, "Player", ...)` (sk280), `Faces.PlaceCountersOn` / `RemoveCountersOn`,
# `this.card.Flip(effect)` (fne/kingpin/60163a : la face qui apparait resout son When Revealed).
# Setup et Permanent : natifs.
#
# ⚠ « at least 2+1[per hero] » : 2 + le nombre de joueurs (3 en solo) ; « a CHARACTER » : heros, allie, sbire ou vilain ;
# « ALL counters removed » puis retournee ; la face 1B (Satchel Charge) resout son When Revealed au retournement et se
# retourne elle-meme (retour a 1A).

def GetAbilities() -> Sequence['Ability']:

    def apres_victoire(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this
        Faces.PlaceCountersOn([this], 1, 'counter', effect)
        seuil = 2 + len(list(Worlds.GetPlayers(effect)))
        if this.GetCounters('counter') >= seuil:
            Faces.RemoveCountersOn([this], this.GetCounters('counter'), 'counter', effect)
            this.card.Flip(effect)

    def fin_phase_joueur(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Punishment(effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.ForcedResponse, CardFinder(name="Punisher"), Unit2, apres_victoire),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Player", fin_phase_joueur),
    ]
