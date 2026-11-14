from . import *

# Moloid — SBIRE (ensemble Mole Man), x3 exemplaires. SUBTERRANEAN. SCH 1, ATK 1, PV 3.
# Guard.
# Forced Response: After Moloid enters play, search the encounter deck for a SUBTERRANEAN minion and put
#   it into play engaged with you.
#
# Cartes de reference :
#  - Guard : BASE AUTOMATIQUE (`desc` ne porte pas Guard ici car imprime en texte, pas en badge — mot-cle
#    standard, aucun module necessaire au-dela du texte).
#  - « After Moloid enters play, search the encounter deck for a SUBTERRANEAN minion and put it into play
#    engaged with you » : `AbilityFactory.AfterCardEnterPlay` + `Search.EncounterCard(trait="SUBTERRANEAN",
#    card_type=Minion)` + `face.PutIntoPlay(joueur, effect)` (modele conan cn017, sans reveler : simple
#    recherche + mise en jeu directe engagee).
#
# ⚠ Mots-pieges : la recherche porte sur le DECK de rencontre seulement (pas la defausse, contrairement a
# gs186/gs187) ; « put it into play engaged with YOU » = le joueur qui controle CE Moloid, pas forcement le
# premier joueur ; un Moloid trouve par cette recherche N'EST PAS revele (pas de « reveal it » imprime).


def GetAbilities() -> Sequence['Ability']:

    def entree_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        joueur = message.trigger.GetControlByPlayer() or Worlds.GetFirstPlayer(effect)
        trouve = Search.EncounterCard(effect, joueur, trait="SUBTERRANEAN", card_type=Minion)
        if trouve is not None:
            trouve.PutIntoPlay(joueur, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, "This", entree_en_jeu),
    ]
