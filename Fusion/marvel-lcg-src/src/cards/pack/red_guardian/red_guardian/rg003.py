from . import *

# * White Widow
# Response: After White Widow enters play, confuse the enemy with Red
#   Guardian's Shield attached.
#
# Jumelle de Black Widow (rg002) : meme structure, seul le statut change.
# Voir rg002 pour le detail (cible non choisie, bouclier possiblement plante
# sur une manigance).


def GetAbilities() -> Sequence['Ability']:

    def white_widow(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        cible = CibleDuBouclier(effect)
        if cible is None or not Enemy.IsType(cible):
            return

        Faces.GiveStatus([cible], "Confused", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            white_widow,
        ),
    ]
