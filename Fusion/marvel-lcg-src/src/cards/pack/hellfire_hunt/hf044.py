from . import *

# Psychic Minefield (manigance annexe de campagne, scenario 4 Torn). Victory 1. Icone Acceleration (desc).
# Threat cannot be removed from here while there is only 1 threat here.
# When Defeated: Deal 5[per_hero] damage to Emma Frost. Each player draws 1 card.
#
# Cartes de reference : 27104 (`ThreatCannotBeRemovedFromWhile`), `Worlds.FindCardOnField(effect, name=..., card_type=Villain)` (04070), `DrawUp`.
# ⚠ « 5 PER HERO » : 5 x le nombre de joueurs ; « Emma Frost » : le vilain du scenario 4.
def GetAbilities() -> Sequence['Ability']:
    def mines(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueurs = Worlds.GetPlayers(effect)
        emma = Worlds.FindCardOnField(effect, name="Emma Frost", card_type=Villain)
        if emma is not None:
            this.DealDamage([emma], 5 * len(joueurs), effect)
        for joueur in joueurs:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            conditions=[lambda effect, message: effect.this.threat <= 1],
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            mines,
            has_defeating_player=True,
        ),
    ]
