from . import *

# Distributed Presence

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()

        # « Place a total of 5 threat among Spot cards in play with the Threat
        # Level keyword as evenly as possible, starting from the lowest Threat
        # Level number. If you placed 5 threat on The Spot this way, you may
        # ready a card you control. »
        #
        # `GetThreatLevelFaces` rend deja les cartes du plus BAS niveau au plus
        # haut : la repartition « aussi egale que possible » se fait donc en
        # tournant sur cette liste.
        cibles = Worlds.GetThreatLevelFaces(effect)
        if not cibles:
            return
        total = Worlds.ConvertPerPlayerIconToInt("5*", effect)
        pose_sur_le_spot = 0
        for i in range(total):
            cible = cibles[i % len(cibles)]
            Faces.PlaceTokensOn([cible], 1, 'threat', effect)
            if cible.IsName("The Spot"):
                pose_sur_le_spot += 1

        if pose_sur_le_spot >= 5:
            player.ReadyControlCards(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee
        ),
    ]
