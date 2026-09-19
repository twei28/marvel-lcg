from . import *

# Bystanders in Peril — Peril : base desc.
# When Revealed: Place 1 civilian counter on a DISASTER environment. If no
#   counter was placed this way, search the encounter deck and discard pile
#   for a DISASTER environment and reveal it.
# [star] Boost: Place 1 civilian counter on a DISASTER environment.
# Modeles : 60109 (Search.SearchForCard deck + defausse), choix du joueur par
# AskChooseFace quand plusieurs catastrophes sont en jeu.

def PoserUnCivil(effect: 'Effect', joueur: 'Player') -> bool:
    envs = Worlds.FindCardsOnField(effect, trait="DISASTER", card_type=Environment)
    if not envs:
        return False
    cible = envs[0] if len(envs) == 1 else joueur.AskChooseFace(list(envs), effect)
    if cible is None:
        return False
    Faces.PlaceCountersOn([cible], 1, 'civilian', effect)
    return True


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if PoserUnCivil(effect, joueur):
            return
        face = Search.SearchForCard(
            effect, joueur,
            include_encounter_deck=True, include_encounter_discard_pile=True,
            trait="DISASTER", card_type=Environment,
        )
        if face:
            face.Reveal(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        PoserUnCivil(effect, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
