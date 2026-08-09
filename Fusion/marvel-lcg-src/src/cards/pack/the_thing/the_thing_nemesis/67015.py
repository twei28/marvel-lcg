from . import *

# Friendly Fire — custom « DesignHacker » (traîtrise némésis de The Thing)
# When Revealed: You take X damage, where X is the ATK of the friendly
# character with the highest ATK. If your identity is the only friendly
# character in play, this card gains surge.

def GetAbilities() -> Sequence['Ability']:

    def friendly_fire(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()
        personnages = list(player.GetControlCharacters())
        if not personnages:
            return

        # CORRECTIF 4/8/2026 : les deux phrases de la carte ne s'excluent PAS.
        # Le script sortait avant d'infliger les degats des que l'identite etait
        # seule en jeu, c'est-a-dire dans le cas solo le plus courant : la carte
        # se contentait alors de prendre Renfort. On encaisse toujours le
        # meilleur ATK ami (le sien quand on est seul), et le Renfort s'ajoute.
        valeur = max(x.attack for x in personnages)
        if valeur > 0:
            this.DealDamage([player.GetIdentity()], valeur, effect)

        if len(personnages) <= 1:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            friendly_fire
        ),
    ]
