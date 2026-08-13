from . import *

# Heightened Threat (1B)

def GetAbilities() -> Sequence['Ability']:

    def derouter_la_menace(effect: 'Effect', message: 'Message.WhenCardWouldRemovedToken') -> None:
        this = effect.this.CastTo(MainScheme)

        # « When you would remove any amount of threat from here or a Spot side
        # scheme, move that threat to the card with the highest Threat Level
        # instead. (If the side scheme you removed threat from has the highest
        # Threat Level number in play, remove that threat.) »
        plus_haute = Worlds.GetHighestThreatLevelFace(effect)
        if not plus_haute:
            return
        if plus_haute == message.trigger:
            return          # la carte visee EST la plus haute : le retrait a lieu

        nombre = message.would_remove
        if not nombre:
            return          # « All » : on laisse le moteur retirer, faute de nombre

        # « MOVE that threat » : la menace PART bien d'ici -- on laisse donc le
        # retrait se faire -- et elle ARRIVE sur la carte au plus haut niveau.
        # Empecher le retrait la dupliquerait : mesure en partie, le complot
        # principal se completait alors en 2,3 rounds au lieu de 6,5.
        Faces.PlaceTokensOn([plus_haute], nombre, 'threat', effect)
        Unused(this)

    def est_une_carte_du_spot(effect: 'Effect', message: 'Message.WhenCardWouldRemovedToken') -> bool:
        """« ici ou une manigance annexe du Spot »."""
        face = message.trigger
        if face == effect.this:
            return True
        return EncounterSideScheme.IsType(face) and face.paper.set_name == "The Spot"

    return [
        AbilityFactory.WhenCardWouldRemovedToken(
            AbilityType.ForcedInterrupt,
            Scheme2,
            'threat',
            derouter_la_menace,
            conditions=[est_une_carte_du_spot]
        ),
        # « If this stage is completed, the players lose the game » ne demande
        # AUCUN module : c'est la regle de base du complot principal, et le
        # dernier stade des autres boites ne l'ecrit pas non plus (56124b).
    ]
