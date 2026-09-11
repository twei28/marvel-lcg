from . import *
# Green Hell — EVENEMENT BASIQUE custom (jakxin), cout 1, [physical].
# Team-Up (Hellcat and She-Hulk). Max 1 per deck.   (desc.TeamUp, base auto)
# Hero Action: Ready Hellcat and She-Hulk. They get +2 ATK until the end of
#   the phase.
#
# ⚠ TEAM-UP : le chargeur EXIGE `.SetTarget("TeamUp")` sur chaque capacite
#   d'un evenement a `desc.TeamUp` (cards/database.py:223, assert en debug) :
#   les deux personnages nommes deviennent les cibles. Modele 14018 Order and
#   Chaos. Vu au setup le 11/09/2026 (« AssertionError: origin_card_id='hc020' »).
# Modeles : 45016
# (`GainUntilPhaseEnd(effect, attack=2)`). ⚠ PAS de `canbe_ready=True` dans le
# finder : une She-Hulk deja prete doit quand meme recevoir les +2 ATQ.

def GetAbilities() -> Sequence['Ability']:

    def green_hell(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        cibles = list(effect.targets)
        Faces.ReadyAll(cibles, effect)
        for face in cibles:
            face.GainUntilPhaseEnd(effect, attack=2)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            green_hell,
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp"),
    ]
