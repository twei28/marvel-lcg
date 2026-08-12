from . import *

# The Made Men — custom « DesignHacker » (manigance secondaire nemesis)
# Forced Interrupt: After Maniac schemes or attacks, the ally under each
#   player's control with the highest printed ATK gains traitor.

def GetAbilities() -> Sequence['Ability']:

    def the_made_men(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        for player in Worlds.GetPlayers(effect):
            allies = [x for x in player.GetControlAllies() if Ally.IsType(x)]
            if not allies:
                continue
            # `Filter.One` ne connait pas « plus haut ATK IMPRIME » (seulement
            # highest_atk, qui inclut les bonus) : on trie a la main.
            unit = max(allies, key=lambda x: x.printed_attack)
            GainTraitor(unit, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(
            AbilityType.ForcedResponse,
            CardFinder(name="Maniac"),
            the_made_men,
        ),
    ]
