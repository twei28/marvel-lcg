from . import *

# Reboot — Evenement 1 [physical], BASIC. Carte EXTRA, hors set du heros.
# Action: Ready a friendly [[ANDROID]] character and heal 1 damage from it.
#
# Cartes de reference :
#  - `09009` Cloak of Levitation : `Faces.ReadyAll(effect.targets, effect)`.
#  - `03007` Steve's Apartment : `this.HealthUnits(effect.targets, 1, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **Action** » nue, pas « Hero Action » : jouable AUSSI en forme
#    alter-ego. Ne pas mettre `SetLabel`.
#  - PAS de filtre `canbe_ready` : la carte fait DEUX choses, et soigner un
#    personnage deja redresse reste legal. Exiger l'inclinaison interdirait ce
#    cas, que le texte autorise.
#  - « **friendly** ANDROID character » : identites ET allies, de n'importe
#    quel joueur — d'ou `Friend` et non `"YouControlUnit"`.
#  - Sentinel est ANDROID sur ses deux faces : la carte le soigne en civil
#    comme en heros.


def GetAbilities() -> Sequence['Ability']:

    def reboot(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        Faces.ReadyAll(effect.targets, effect)
        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            reboot,
        ).SetPlay()
        .SetTarget(Friend, trait="ANDROID"),
    ]
