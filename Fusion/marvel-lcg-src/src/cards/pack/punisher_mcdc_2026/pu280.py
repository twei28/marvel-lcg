from .commun import *

# Secret Agent (defi 2, p280, ID 6140) : Captain America (Civil War), complots Gathering Support / « Guerilla Warfare » (Civil War), sets Hydra Assault,
# Hydra Patrol, Legions of Hydra, Captain America Nemesis. Difficulte 4.
# Regles speciales : (1) « Captain America gains the HYDRA trait » ; (2) « All HYDRA minions gain quickstrike » ; (3) complot avance a 2A.
#
# Cartes de reference : challenges/2421_battle_of_the_bots (`GiveKeywordToInPlayWhenApplyThis(..., trait=...)` sur un type et un trait), 2412 (complot en 2A).
# DECISION SANS TEXTE DE RR : la carte imprime « Guerilla Warfare (Civil War) » pour le complot 2, nom ABSENT du moteur (aucune carte de ce nom) : on prend
# Resistance Tactics (56142a) puis Guerilla Warfare (pu284b), confirme par la carte fournie par l utilisateur.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Captain America", card_type=Villain), trait="HYDRA"),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("HYDRA", Minion), quickstrike=1),
        ComplotEn2A(),
    ]
