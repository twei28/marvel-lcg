from . import *

# War of the Realms — custom "Rainy" (némésis de Thor Jane Foster)
# When Revealed: Each player takes 1 indirect damage for each character
# they control.

def GetAbilities() -> Sequence['Ability']:

    def war_of_the_realms(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        for player in list(effect.world.players):
            if player.is_eliminated:
                continue
            characters = [x for x in Worlds.FindCardsOnField(effect, card_type=Friend)
                          if x.GetControlBy() == player]
            num = len(characters)
            if num > 0:
                # LENIENT : les dégâts indirects sont affectés à l'identité
                # (la répartition libre n'est pas demandée ici).
                player.GetIdentity().TakeIndirectDamage(this, num, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            war_of_the_realms
        )
    ]
