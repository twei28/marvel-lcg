from . import *

# * Gladiator

def GetAbilities() -> Sequence['Ability']:

    # « VOS points de vie », pas ceux de Gladiator : c'est l'identite du
    # controleur qu'on lit. Modele 22013 (Venom de Nebula), meme reduction de
    # degats consequents, condition differente.
    def gladiator(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player is None:
            return 0
        identity = player.GetIdentity()
        if identity.health <= 5:
            ui.append(identity)
            return 1
        return 0

    return [
        AbilityFactory.ThisGainKeyword(
            gladiator,
            attack_consequential_damage=-2,
            thwart_consequential_damage=-2,
            change_on_event=OnEvent.Health("YourIdentity")
        ),
    ]
