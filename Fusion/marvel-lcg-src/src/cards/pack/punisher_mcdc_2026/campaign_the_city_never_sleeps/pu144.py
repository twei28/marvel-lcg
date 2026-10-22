from . import *

# Punishment — ENVIRONNEMENT de campagne (combat 3, p267). Setup. Permanent.
# Battle Setup : Scenario Punishment ; UNDERLING = celui (Hobgoblin ou Jigsaw) PAS affronte au combat 2 ; set Punisher's Armory.
# Forced Response : After Punisher's first stage is defeated or the main scheme advances to stage 2A, flip this card.
#
# Cartes de reference : fne/campaign.py (`WriteCampaignLogAtGameOver` + `ExpertCampaignSetPlayersHPToTheirRemainingHP`), pu142 (meme famille, mise en jeu par `encounters`), pu140, `campaign.py` (`EnregistrerLeReleve`, `MettreLesRecompenses`),
# pu001b (`AfterCardsMoved`/`MainScheme.Advance` : un complot qui avance), `Faces.RemoveFromGame` / `PutIntoPlay` pour l'echange de faces.
# ⚠ Mots-pieges :
#  - « flip this card » : cette carte est RECTO-VERSO (6134A / 6134B S.H.I.E.L.D. Support Team, la recompense du combat 3). Le moteur n'a pas de carte
#    a deux faces de types differents (environnement / amelioration) : on retire pu144 et on met pu145 en jeu, sous le controle du premier joueur ;
#  - « Punisher's FIRST stage is defeated » (stade I du Punisher, villain pu0xx) OU « the main scheme advances to 2A » : le PREMIER des deux, une seule fois ;
#  - Victoire (instructions de campagne) : « Vous avez gagne l'allie Punisher (6138) » : releve du carnet (`Punisher Ally` = 1), PAS de retournement.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCampaignSetup') -> None:
        Unused(message)
        MettreLesRecompenses(effect, (CLE_CAISSES, CAISSES), (CLE_CACHE, CACHE))

    return [
        AbilityFactoryCampaign.WhenCampaignSetup(mise_en_place),
        # Le scenario Punishment (One Last Kill) n'ecrit AUCUN releve de campagne : pu144 le fait elle-meme (pas de collecteur partage ici).
        AbilityFactoryCampaign.ExpertCampaignSetPlayersHPToTheirRemainingHP(),
        WriteCampaignLogAtGameOver(ReleveCombat3, scenario_id='punishment'),
        *RetournerPunishment(),
    ]
