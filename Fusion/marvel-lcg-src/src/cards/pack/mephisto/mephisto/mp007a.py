from . import *

# Gateway to Corruption — ENVIRONNEMENT (face A de la carte 7/28). SETTING. Permanent. Setup.
# Forced Interrupt: When a card is set aside from a player's deck, put it facedown into Damnation instead.
# If there are 10[per_hero] cards in Damnation, the players lose the game.
#
# Cartes de reference :
#  - « Permanent » et « Setup » : BASES AUTOMATIQUES `desc.Permanent` / `desc.Setup` (fiches permanent.md, setup.md).
#  - « When a card is set aside from a player's deck, ... instead » : `WhenCardWouldMoveToArea` + `message.ChangeToArea(zone, effect)`
#    (card_move.py, sender_card.py) ; modele de la redirection : recette gs082 « la destination n'est pas deja la reserve ».
#    Helper `RedirectionVersLaDamnation` (set), fiche damnation.md.
#  - « If there are 10[per_hero] cards in Damnation, the players lose the game » : texte en gras, pas un declencheur ; `VerifierDamnation`
#    est appele a chaque entree d'une carte en Damnation (redirection ci-dessus, `MettreEnDamnation`).
#
# ⚠ Mots-pieges : « SET ASIDE FROM A PLAYER'S DECK » (pas les cartes de rencontre mises de cote) ; « 10[per_hero] » = 10 par joueur de
# la partie, toutes piles confondues.


def GetAbilities() -> Sequence['Ability']:
    return [
        RedirectionVersLaDamnation(),
    ]
