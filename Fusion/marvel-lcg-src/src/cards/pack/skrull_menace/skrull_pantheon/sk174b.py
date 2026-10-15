from . import *

# Slaying the False Gods 2B (174B) — complot principal, face B. Menace 12[per_hero], depart 0, escalade +1[per_hero].
# When Revealed: Flip the villain.
# If this stage is completed, the players lose the game. (gras)
#
# Cartes de reference :
#  - Retournement du mechant : `fne/typhoid_mary/60112` (`card.Flip`, modele 45101a) via le helper
#    `RetournerLeMechant` (defausse les elements associes, puis Flip avec revelation de la face d'arrivee).
#  - « If this stage is completed, the players lose the game » : base AUTOMATIQUE du moteur
#    (`MainScheme.GetAbilities` lit le texte gras exact « <b>If this stage is completed, the players lose the
#    game ») : aucun module pour cette phrase (modele wd055b `IfThisSchemeStageIsCompletedPlayersLoseTheGame`).
#
# ⚠ Mots-pieges : « Flip the VILLAIN » (la carte double face, pas ce complot) ; la phrase en gras est
# imprimee dans le texte de la carte, pas deduite ; la face retournee resout son « When Revealed » (insert
# p.14, Alternation of Gods) : un jeton de foi de plus a chaque retournement.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        RetournerLeMechant(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
