from . import *

# Rage of Black King (side scheme 2, Hinder 1[per_hero] natif, boost 2). « Forced Response : After Sebastian Shaw activates, he gains a tough status
# card. When Defeated : Each player chooses to either place 2 energy counters on Sebastian Shaw or deal themselves 1 facedown encounter card. »
# Cartes de reference : activate.py (`AfterEnemyActivationEnd(ForcedResponse, ...)`), 60075 / ap024 (`player.ChooseAbilities(ForChoiceAbility, ForChoiceAbility)`),
# 29011-like `Faces.GiveStatus(..., "Tough")`.


def GetAbilities() -> Sequence['Ability']:
    def robuste(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        shaw = ShawVilain(effect)
        if shaw is not None:
            Faces.GiveStatus([shaw], "Tough", effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        for joueur in Worlds.GetPlayers(effect):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Place 2 energy counters on Sebastian Shaw", lambda cibles: PlacerEnergie(effect, 2)),
                AbilityFactory.ForChoiceAbility("Deal yourself 1 facedown encounter card", lambda cibles, joueur=joueur: joueur.DealEncounterCards(1, effect)),
            )

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, SurShaw(), robuste),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
