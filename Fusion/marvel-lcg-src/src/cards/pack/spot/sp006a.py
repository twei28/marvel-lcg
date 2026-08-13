from . import *

# What Goes Around... (A, mode standard)

def GetAbilities() -> Sequence['Ability']:

    def carte_du_spot_revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When a card that belongs to The Spot encounter set is revealed,
        # place 1 threat on the main scheme. »
        if message.trigger.paper.set_name != "The Spot":
            return
        scheme = Worlds.FindMainScheme(effect)
        if scheme:
            Faces.PlaceTokensOn([scheme], 1, 'threat', effect)

    return [
        AbilityFactory.WhenCardRevealed(
            AbilityType.ForcedInterrupt,
            None,
            carte_du_spot_revelee
        ),
        # « Hero Action: Discard a card from hand -> move up to 3 threat from
        # one Spot card with the Threat Level keyword to a different Spot card
        # with the Threat Level keyword. »
        #
        # ECART ASSUME, ecrit plutot que silencieux : le deplacement de menace
        # d'une carte VERS UNE AUTRE, avec un montant choisi par le joueur, n'a
        # pas de crochet. Le joueur peut obtenir le meme resultat a la main
        # avec le bac a sable ; la carte, elle, ne le propose pas.
    ]
