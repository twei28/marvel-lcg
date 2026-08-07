# Mesures de câblage, sonde `FIN_DE_PARTIE=1`

| Boîte | Niv. | Scénario | Carnet entrant appliqué | Carnet sortant écrit | Effet propre au niveau prouvé |
|---|---|---|---|---|---|
| mts | 2 | the_tower_defense | oui (21181) | oui | non mesuré (exigence ajoutée après ces lignes) |
| mts | 4 | hela | oui (21188, 21185) | oui | non mesuré (exigence ajoutée après ces lignes) |
| mts | 5 | loki | oui (21139) | oui | non mesuré (exigence ajoutée après ces lignes) |
| mut_gen | 1 | sabretooth | minimal (Player 1 Role, pas d'erreur) | oui | non mesuré (exigence ajoutée après ces lignes) |
| mut_gen | 2 | project_wideawake | minimal (Player 1 Role, pas d'erreur) | oui | non mesuré (exigence ajoutée après ces lignes) |
| mut_gen | 3 | master_mold | oui (32089) | oui | non mesuré (exigence ajoutée après ces lignes) |
| mut_gen | 4 | mansion_attack | minimal (Player 1 Role, pas d'erreur) | oui | non mesuré (exigence ajoutée après ces lignes) |
| mut_gen | 5 | magneto | minimal (Player 1 Role, pas d'erreur) | oui | non mesuré (exigence ajoutée après ces lignes) |
| next_evol | 1 | morlock_siege | minimal (pas d'erreur) | oui | aucun : `CampaignSetup(1)` n'ajoute rien sous `if (level == 1)`, seule la partie commune (PutEarnedEnvironmentsIntoPlay, ChooseCampaignPlayerSideScheme, écriture du carnet) tourne, et elle tourne à tous les niveaux |
| next_evol | 2 | on_the_run | oui (Campaign Pool: Team Assembled) | oui | statut Tough sur le vilain : absent sans carnet, présent (`monde.area_villain`, `card_id=tough`) avec 1 environnement en carnet (`GiveEnemiesToughIfEnvEarned`, `if (level == 2)` seulement) |
| next_evol | 3 | juggernaut | oui (Campaign Pool: Team Assembled, Geared Up) | oui | 2 environnements en jeu (40190b, 40192b) et `c_momentum` sur Juggernaut passant de 1 (base carte, hors campagne) à 3, delta +2 = nombre d'environnements (`JuggernautMomentumCounters`, `if (level == 3)` seulement) |
| next_evol | 4 | mister_sinister | oui (Campaign Pool: Team Assembled) | oui | `k_threat` sur « Teleported Away » (40146) passant de 4 (sans carnet) à 5 (avec 1 environnement), delta +1 = environnements × joueurs (`TeleportedAwaySetup`, `if (level == 4)` seulement) |
| next_evol | 5 | stryfe | oui (Campaign Pool: Team Assembled) | oui | `k_threat` sur « Stryfe's Grasp » (40168a) passant de 10 (sans carnet) à 11 (avec 1 environnement), delta +1 = environnements × joueurs (`StryfesGraspThreat`, `if (level == 5)` seulement) |
| aoa | 1 | unus | minimal (pas d'erreur) | oui | aucun : `CampaignSetup(1)` d'`aoa` n'a pas de branche `if (level == n)`, `SetupMissionAndOverseer(level)` suit le même chemin qu'aux niveaux 2 à 4, chemin de code identique |
| aoa | 2 | four_horsemen | oui (Campaign Pool: Panicked Refugees, mesure entrante séparée) | oui | aucun : chemin de code identique aux niveaux 1, 3 et 4 ; seule preuve indirecte : `EachPlayerShufflesCopyIfPool('45178', 'Panicked Refugees')` distribue bien 45178 à un joueur (`monde.players.hand_cards`) quand le carnet entrant le porte |
| aoa | 3 | apocalypse | minimal (pas d'erreur) | oui | aucun : chemin de code identique aux niveaux 1, 2 et 4 |
| aoa | 4 | dark_beast | minimal (pas d'erreur) | oui | aucun : chemin de code identique aux niveaux 1, 2 et 3 |
| aoa | 5 | en_sabah_nur | minimal (pas d'erreur) | oui | mission forcée sur « Protect the Professor » (`SetupMissionAndOverseer`, `if (level == 5)` seulement, seule branche qui distingue un niveau dans `aoa`) : carte 45170a en jeu (`monde.area_schemes_side`) et `Mission Done: Protect the Professor` dans le carnet sortant (`Current Mission` est remis à `None` par `CollectAoA` à la fin de partie, non observable en carnet sortant) |
