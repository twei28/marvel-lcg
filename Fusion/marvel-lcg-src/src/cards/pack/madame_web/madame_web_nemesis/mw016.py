from . import *

# Hypnosis — custom « Kajislav », traitrise nemesis
# Surge. (mot-cle porte par cards.json)
# When Revealed: Stun and confuse a character you control.

def GetAbilities() -> Sequence['Ability']:

    def hypnose(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        cible = player.AskChooseFace(player.GetControlCharacters(), effect)
        if cible:
            Faces.GiveStatus([cible], "Stunned", effect)
            Faces.GiveStatus([cible], "Confused", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hypnose
        ),
    ]
