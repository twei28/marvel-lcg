from . import *

# * Pearl Pangan
#
# Setup: You begin the game with a Rising Tide area (see insert). -- TEXTE
# PUREMENT EXPLICATIF, aucun code : la zone existe deja pour TOUT joueur
# (`player.rising_tide`, meme choix que la Reserve du pack `brawn`, voir
# `game/player/player.py`), qu'il joue Wave ou non. Rien a creer ici.
#
# Champion Swimmer — Action: texte imprime NU (« Action: », pas « Alter-Ego
# Action: ») sur la face alter-ego elle-meme : meme convention que Sharon
# Carter (ag001b), Bruce Banner (10001b), Tony Stark (01029b) -- AbilityType.
# Action + .LimitOncePerPhase(), jamais AlterEgoAction (reserve aux cartes
# JOUEUR qui declarent ce mode explicitement, n'etant pas elles-memes la face
# alter-ego).

def GetAbilities() -> Sequence['Ability']:

    def champion_swimmer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        joueur = effect.GetInitiator()
        dessus = joueur.player_deck.GetTop()
        if dessus is None:
            return
        PlacerFaceVisibleDansRisingTide(dessus, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            champion_swimmer,
        ).SetName("Champion Swimmer")
        .LimitOncePerPhase(),
    ]
