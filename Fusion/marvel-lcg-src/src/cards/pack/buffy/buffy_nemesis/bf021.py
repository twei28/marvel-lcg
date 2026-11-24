from . import *

# * Spike — SBIRE nemesis (VAMPIRE). SCH 2, ATQ 2*, PV 5, boost 2.
# [star] Forced Response: After Spike attacks and damages a character, discard the top card of the encounter deck. If that card is a
# treachery, heal all damage from Spike.
#
# CARTES DE REFERENCE
#  - `01050` / `01024` : `AfterUnitAttackEnd(type, "This", op, conditions=[..])` ; `message.damaged_targets` = les unites REELLEMENT blessees
#    (recette « attacks AND damages » : un `AfterUnitAttackEnd` seul part aussi quand l'attaque est prevenue).
#  - `Worlds.DiscardEncounterTopCard(effect)` rend la face defaussee ; `this.HealthUnits([this], "All", effect)` pour « heal all damage ».
#
# TEXTE CONTRE CODE
#  « attacks AND damages a character » -> condition `damaged_targets` non vide (une attaque entierement prevenue ne declenche rien).
#  « that card is a treachery » -> la carte defaussee, de type Treachery. « heal ALL damage from Spike » -> "All".


def GetAbilities() -> Sequence['Ability']:

    def a_blesse(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        Unused(effect)
        return len(message.damaged_targets) > 0

    def spike(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(message)
        carte = Worlds.DiscardEncounterTopCard(effect)
        if carte is not None and Treachery.IsType(carte):
            this.HealthUnits([this], "All", effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            spike,
            conditions=[a_blesse],
        ),
    ]
