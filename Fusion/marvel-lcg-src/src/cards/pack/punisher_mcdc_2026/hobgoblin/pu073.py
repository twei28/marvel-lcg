from . import *

# Hobgoblin's Glider — ATTACHEMENT. Setup. Permanent. Attach to Hobgoblin.
# "Pumpkin Bomb" — Special : voir __init__.py (`PumpkinBomb`, l'aptitude commune de tout le set).
#
# Cartes de reference : sm/sinister_six/27100b.py (`WhenResolveSpecialAbility("This", ...).SetName(...)`),
# skrull_menace/paibok/__init__.py (`AttachToFaceWhenPutIntoPlay(CardFinder(name=..., card_type=Villain))`).
# Setup et Permanent : natifs, lus dans `desc` (fiches mots-cles/permanent.md).
#
# ⚠ Le reste du set appelle `ResoudrePumpkinBomb` (fonction), pas cette aptitude : meme effet, sans dependre de la
# presence du Glider en jeu.

def GetAbilities() -> Sequence['Ability']:

    def pumpkin_bomb(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        joueur = message.GetToPlayer() or Worlds.GetFirstPlayer(effect)
        PumpkinBomb(effect, joueur)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Hobgoblin", card_type=Villain)),
        AbilityFactory.WhenResolveSpecialAbility("This", pumpkin_bomb).SetName("Pumpkin Bomb"),
    ]
