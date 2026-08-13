from . import *

# Penchant for Pilfery

def GetAbilities() -> Sequence['Ability']:

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        # « if there is 4 threat or greater here, each player chooses to either
        # discard a card they control or take 2 damage. »
        seuil = Worlds.ConvertPerPlayerIconToInt("4*", effect)
        if this.threat < seuil:
            return

        def pour_chaque_joueur(player: 'Player'):
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard a card you control",
                    lambda targets: player.DiscardControlCards(effect)
                ),
                AbilityFactory.ForChoiceAbility(
                    "Take 2 damage",
                    lambda targets: Utility.DealDamageToCharacterYouControl(player, 2, effect)
                ),
            )

        Players.ForEachPlayer(effect, pour_chaque_joueur)

    return [
        AbilityFactory.WhenVillainPhaseEnd(
            AbilityType.ForcedResponse,
            fin_de_phase
        ),
    ]
