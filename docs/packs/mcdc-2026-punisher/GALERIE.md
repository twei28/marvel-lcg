# Galerie MC/DC 2026 : inventaire des images téléchargées

Source : https://www.mcdc.fun/2026-card-gallery (site Squarespace). Relevé du 20/10/2026 : **215 images uniques** (la regexp de la consigne en compte 216 : l'URL du bandeau « Copy of mcdc 2026-3.png » y figure deux fois, avec et sans `https:`). Dont 1 bandeau et 214 cartes. Les images sont dans `sources/galerie/<section>/` (dossier ignoré par git : fichiers de l'équipe MC/DC). Pour les retrouver : `python3 telecharger-galerie.py` (relançable, ne retélécharge pas un fichier présent). Les noms de fichier sont décodés (`+` devient espace ; le `_` du site tient lieu d'apostrophe : « It_s a Trap! »).

Sections : les ancres `#basic` à `#other` ne délimitent que les cinq aspects, la section « campaign-challenge » et « other » ; les images qui précèdent `#basic` dans la page (scénarios, lieux, méchants, sous-fifres, sets modulaires) sont rangées sous `campagne-punisher`. Types lus dans le nom de fichier : DS = deux faces (A/B), AE et RE = cartes de campagne, RP = REPRINT (art alternatif d'une carte du jeu). Préfixe d'un reprint : B Basic, A Aggression, J Justice, L Leadership, P Protection.

Les reprints (41) sont traités par `importer-full-art.py` : la colonne « Branché » donne la carte du jeu remplacée (`card_id`) ; les cas non branchés sont tranchés dans `.planning/todos/2026-10-20-mcdc-full-art-questions.md`. Les autres sections sont à télécharger seulement (future campagne Punisher), non intégrées.


## Campagne Punisher (scénarios, lieux, méchants, sous-fifres, sets modulaires) (154 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6001A | Main Scheme 1A (n° 01A) | deux faces |  | oui | 2150×1500 | 388 Ko |  |
| 6001B | Main Scheme 1B (n° 01B) | deux faces |  | oui | 2150×1500 | 578 Ko |  |
| 6002A | Main Scheme 2A (n° 02A) | deux faces |  | oui | 2150×1500 | 463 Ko |  |
| 6002B | Main Scheme 2B (n° 02B) | deux faces |  | oui | 2150×1500 | 608 Ko |  |
| 6003A | Main Scheme 3A (n° 03A) | deux faces |  | oui | 2150×1500 | 463 Ko |  |
| 6003B | Main Scheme 3B (n° 03B) | deux faces |  | oui | 2150×1500 | 533 Ko |  |
| 6004 | Gunrunner (n° 04) | carte de campagne (AE) |  | oui | 1500×2150 | 435 Ko |  |
| 6005 | The City (n° 05) | carte de campagne (AE) |  | oui | 1500×2150 | 383 Ko |  |
| 6006 | Never Sleeps (n° 06) | carte de campagne (AE) |  | oui | 1500×2150 | 336 Ko |  |
| 6007 | Burning Building (n° 07) | carte de campagne (RE) |  | oui | 1500×2150 | 451 Ko |  |
| 6008 | Citizens in Danger (n° 08) | carte de campagne (RE) |  | oui | 1500×2150 | 467 Ko |  |
| 6009 | Hunted by the Past (n° 09) | carte de campagne (RE) |  | oui | 1500×2150 | 381 Ko |  |
| 6010 | It_s a Trap! (n° 10) | carte de campagne (RE) |  | oui | 1500×2150 | 425 Ko |  |
| 6011 | Bellona (n° 11) | carte de campagne (RE) |  | oui | 1500×2150 | 466 Ko |  |
| 6012 | Black Tarantula (n° 12) | carte de campagne (RE) |  | oui | 1500×2150 | 369 Ko |  |
| 6013 | Overdrive (n° 13) | carte de campagne (RE) |  | oui | 1500×2150 | 475 Ko |  |
| 6014 | Muse (n° 14) | carte de campagne (RE) |  | oui | 1500×2150 | 529 Ko |  |
| 6015 | Screwball (n° 15) | carte de campagne (RE) |  | oui | 1500×2150 | 500 Ko |  |
| 6016 | Busted (n° 16) | carte de campagne (RE) |  | oui | 1500×2150 | 378 Ko |  |
| 6017 | Conflicting Evidence (n° 17) | carte de campagne (RE) |  | oui | 1500×2150 | 462 Ko |  |
| 6018 | Red Herring (n° 18) | carte de campagne (RE) |  | oui | 1500×2150 | 429 Ko |  |
| 6019 | Red Herring (n° 19) | carte de campagne (RE) |  | oui | 1500×2150 | 429 Ko |  |
| 6020 | Shootout (n° 20) | carte de campagne (RE) |  | oui | 1500×2150 | 428 Ko |  |
| 6021 | Bank Robbery (n° 21) | carte de campagne (RE) |  | oui | 2150×1500 | 445 Ko |  |
| 6022 | Like and Subscribe (n° 22) | carte de campagne (RE) |  | oui | 2150×1500 | 403 Ko |  |
| 6023 | U1 upper west side (n° 01) | carte de campagne (AE) |  | oui | 1500×2150 | 440 Ko |  |
| 6024 | U2 harlem (n° 02) | carte de campagne (AE) |  | oui | 1500×2150 | 374 Ko |  |
| 6025 | U3 the bronx (n° 03) | carte de campagne (AE) |  | oui | 1500×2150 | 315 Ko |  |
| 6026 | U1 west side warrior (n° 04) | carte de campagne (AE) |  | oui | 1500×2150 | 426 Ko |  |
| 6027 | U2 the harlem hustle (n° 05) | carte de campagne (AE) |  | oui | 1500×2150 | 391 Ko |  |
| 6028 | U3 bronx bombered (n° 06) | carte de campagne (AE) |  | oui | 1500×2150 | 406 Ko |  |
| 6029 | uptown expansion instructions (n° 07) | carte de campagne (AE) |  | oui | 1500×2150 | 335 Ko |  |
| 6030 | hells kitchen (n° 01) | carte de campagne (AE) |  | oui | 1500×2150 | 506 Ko |  |
| 6031 | theater district (n° 02) | carte de campagne (AE) |  | oui | 1500×2150 | 412 Ko |  |
| 6032 | upper east side (n° 03) | carte de campagne (AE) |  | oui | 1500×2150 | 429 Ko |  |
| 6033 | west village (n° 04) | carte de campagne (AE) |  | oui | 1500×2150 | 465 Ko |  |
| 6034 | midtown (n° 05) | carte de campagne (AE) |  | oui | 1500×2150 | 297 Ko |  |
| 6035 | lower east side (n° 06) | carte de campagne (AE) |  | oui | 1500×2150 | 491 Ko |  |
| 6036 | soho (n° 07) | carte de campagne (AE) |  | oui | 1500×2150 | 365 Ko |  |
| 6037 | financial district (n° 08) | carte de campagne (AE) |  | oui | 1500×2150 | 459 Ko |  |
| 6038 | chinatown (n° 09) | carte de campagne (AE) |  | oui | 1500×2150 | 488 Ko |  |
| 6039 | bar fight at josies (n° 01) | carte de campagne (AE) |  | oui | 1500×2150 | 439 Ko |  |
| 6040 | art heals the soul (n° 02) | carte de campagne (AE) |  | oui | 1500×2150 | 450 Ko |  |
| 6041 | a walk in the park (n° 03) | carte de campagne (AE) |  | oui | 1500×2150 | 420 Ko |  |
| 6042 | village of the dammed (n° 04) | carte de campagne (AE) |  | oui | 1500×2150 | 457 Ko |  |
| 6043 | midtown memories (n° 05) | carte de campagne (AE) |  | oui | 1500×2150 | 338 Ko |  |
| 6044 | kings of yancy street (n° 06) | carte de campagne (AE) |  | oui | 1500×2150 | 457 Ko |  |
| 6045 | wheres my rent (n° 07) | carte de campagne (AE) |  | oui | 1500×2150 | 392 Ko |  |
| 6046 | play the market (n° 08) | carte de campagne (AE) |  | oui | 1500×2150 | 445 Ko |  |
| 6047 | forget it its chinatown (n° 09) | carte de campagne (AE) |  | oui | 1500×2150 | 472 Ko |  |
| 6048A | Count Nefaria (n° 01A) | deux faces |  | oui | 1500×2150 | 414 Ko |  |
| 6048B | Count Nefaria (n° 01B) | deux faces |  | oui | 1500×2150 | 415 Ko |  |
| 6049A | Crime Master (n° 02A) | deux faces |  | oui | 1500×2150 | 383 Ko |  |
| 6049B | Crime Master (n° 02B) | deux faces |  | oui | 1500×2150 | 383 Ko |  |
| 6050A | Ringmaster (n° 03A) | deux faces |  | oui | 1500×2150 | 465 Ko |  |
| 6050B | Ringmaster (n° 03B) | deux faces |  | oui | 1500×2150 | 465 Ko |  |
| 6051A | Lady Yulan (n° 04A) | deux faces |  | oui | 1500×2150 | 388 Ko |  |
| 6051B | Lady Yulan (n° 04B) | deux faces |  | oui | 1500×2150 | 388 Ko |  |
| 6052A | Mr Negative (n° 05A) | deux faces |  | oui | 1500×2150 | 414 Ko |  |
| 6052B | Mr Negative (n° 05B) | deux faces |  | oui | 1500×2150 | 408 Ko |  |
| 6053A | The Rose (n° 06A) | deux faces |  | oui | 1500×2150 | 443 Ko |  |
| 6053B | The Rose (n° 06B) | deux faces |  | oui | 1500×2150 | 442 Ko |  |
| 6054A | Nightshade (n° 07A) | deux faces |  | oui | 1500×2150 | 431 Ko |  |
| 6054B | Nightshade (n° 07B) | deux faces |  | oui | 1500×2150 | 431 Ko |  |
| 6055A | Diamondback (n° 08A) | deux faces |  | oui | 1500×2150 | 453 Ko |  |
| 6055B | Diamondback (n° 08B) | deux faces |  | oui | 1500×2150 | 453 Ko |  |
| 6056A | Jigsaw I (n° 01A) | deux faces |  | oui | 1500×2150 | 469 Ko |  |
| 6056B | Jigsaw II (n° 01B) | deux faces |  | oui | 1500×2150 | 473 Ko |  |
| 6057A | Jigsaw II (n° 02A) | deux faces |  | oui | 1500×2150 | 474 Ko |  |
| 6057B | Jigsaw III (n° 02B) | deux faces |  | oui | 1500×2150 | 475 Ko |  |
| 6058 | Jigsaw_s Knife (n° 03) | carte de campagne (RE) |  | oui | 1500×2150 | 394 Ko |  |
| 6059 | Bushwacker (n° 04) | carte de campagne (RE) |  | oui | 1500×2150 | 429 Ko |  |
| 6060 | Maggia Thug (n° 05) | carte de campagne (RE) |  | oui | 1500×2150 | 434 Ko |  |
| 6061 | Maggia Thug (n° 06) | carte de campagne (RE) |  | oui | 1500×2150 | 434 Ko |  |
| 6062 | Maggia Thug (n° 07) | carte de campagne (RE) |  | oui | 1500×2150 | 434 Ko |  |
| 6063 | Man Mountain Marko (n° 08) | carte de campagne (RE) |  | oui | 1500×2150 | 363 Ko |  |
| 6064 | The Eel (n° 09) | carte de campagne (RE) |  | oui | 1500×2150 | 409 Ko |  |
| 6065 | Putting the Pieces Together (n° 10) | carte de campagne (RE) |  | oui | 2150×1500 | 522 Ko |  |
| 6066 | Cut to Pieces (n° 11) | carte de campagne (RE) |  | oui | 1500×2150 | 362 Ko |  |
| 6067 | Cut to Pieces (n° 12) | carte de campagne (RE) |  | oui | 1500×2150 | 362 Ko |  |
| 6068 | Friends of Ours (n° 13) | carte de campagne (RE) |  | oui | 1500×2150 | 451 Ko |  |
| 6069 | Friends of Ours (n° 14) | carte de campagne (RE) |  | oui | 1500×2150 | 450 Ko |  |
| 6070 | A Made Man (n° 15) | carte de campagne (RE) |  | oui | 1500×2150 | 485 Ko |  |
| 6071A | Hobgoblin I (n° 01A) | deux faces |  | oui | 1500×2150 | 481 Ko |  |
| 6071B | Hobgoblin II (n° 01B) | deux faces |  | oui | 1500×2150 | 490 Ko |  |
| 6072A | Hobgoblin II (n° 02A) | deux faces |  | oui | 1500×2150 | 490 Ko |  |
| 6072B | Hobgoblin III (n° 02B) | deux faces |  | oui | 1500×2150 | 504 Ko |  |
| 6073 | Goblin Glider (n° 03) | carte de campagne (AE) |  | oui | 1500×2150 | 476 Ko |  |
| 6074 | Flaming Sword (n° 04) | carte de campagne (RE) |  | oui | 1500×2150 | 533 Ko |  |
| 6075 | Prowler (n° 05) | carte de campagne (RE) |  | oui | 1500×2150 | 543 Ko |  |
| 6076 | Rabble (n° 06) | carte de campagne (RE) |  | oui | 1500×2150 | 452 Ko |  |
| 6077 | The Enforcers (n° 07) | carte de campagne (RE) |  | oui | 1500×2150 | 389 Ko |  |
| 6078 | Torn to Pieces (n° 08) | carte de campagne (RE) |  | oui | 1500×2150 | 506 Ko |  |
| 6079 | Designs on Crimes (n° 09) | carte de campagne (RE) |  | oui | 2150×1500 | 407 Ko |  |
| 6080 | Guise to Terrorize (n° 10) | carte de campagne (RE) |  | oui | 1500×2150 | 460 Ko |  |
| 6081 | Guise to Terrorize (n° 11) | carte de campagne (RE) |  | oui | 1500×2150 | 460 Ko |  |
| 6082 | Smashing Pumpkins (n° 12) | carte de campagne (RE) |  | oui | 1500×2150 | 523 Ko |  |
| 6083 | Smashing Pumpkins (n° 13) | carte de campagne (RE) |  | oui | 1500×2150 | 534 Ko |  |
| 6084 | Wrath of the Hobgoblin (n° 14) | carte de campagne (RE) |  | oui | 1500×2150 | 428 Ko |  |
| 6085 | Wrath of the Hobgoblin (n° 15) | carte de campagne (RE) |  | oui | 1500×2150 | 430 Ko |  |
| 6086A | Punisher I (n° 01A) | deux faces |  | oui | 1500×2150 | 507 Ko |  |
| 6086B | Punisher II (n° 01B) | deux faces |  | oui | 1500×2150 | 521 Ko |  |
| 6087A | Punisher II (n° 02A) | deux faces |  | oui | 1500×2150 | 512 Ko |  |
| 6087B | Punisher III (n° 02B) | deux faces |  | oui | 1500×2150 | 504 Ko |  |
| 6088A | Punisher Main 1A (n° 03A) | deux faces |  | oui | 2150×1500 | 442 Ko |  |
| 6088B | Punisher Main 1B (n° 03B) | deux faces |  | oui | 2150×1500 | 549 Ko |  |
| 6089A | Punisher Main 2A (n° 04A) | deux faces |  | oui | 2150×1500 | 336 Ko |  |
| 6089B | Punisher Main 2B (n° 04B) | deux faces |  | oui | 2150×1500 | 493 Ko |  |
| 6090A | Justice or Punishment (n° 05A) | deux faces |  | oui | 1500×2150 | 383 Ko |  |
| 6090B | Justice or Punishment (n° 05B) | deux faces |  | oui | 1500×2150 | 459 Ko |  |
| 6091A | Target Lock Focused (n° 06A) | deux faces |  | oui | 1500×2150 | 501 Ko |  |
| 6091B | Target Lock Distracted (n° 06B) | deux faces |  | oui | 1500×2150 | 443 Ko |  |
| 6092 | In the Crosshairs (n° 07) | carte de campagne (AE) |  | oui | 1500×2150 | 476 Ko |  |
| 6093 | Punisher_s Assault Rifle (n° 08) | carte de campagne (RE) |  | oui | 1500×2150 | 496 Ko |  |
| 6094 | Punisher_s RPG (n° 09) | carte de campagne (RE) |  | oui | 1500×2150 | 498 Ko |  |
| 6095 | Punishers M1911s (n° 10) | carte de campagne (RE) |  | oui | 1500×2150 | 391 Ko |  |
| 6096 | Mexican Standoff (n° 11) | carte de campagne (RE) |  | oui | 1500×2150 | 538 Ko |  |
| 6097 | Microchip (n° 12) | carte de campagne (RE) |  | oui | 1500×2150 | 382 Ko |  |
| 6098 | Rachel Cole Alves (n° 13) | carte de campagne (RE) |  | oui | 1500×2150 | 406 Ko |  |
| 6099 | Judge, Jury Side Scheme (n° 14) | carte de campagne (RE) |  | oui | 2150×1500 | 484 Ko |  |
| 6100 | Back Against the Wall (n° 15) | carte de campagne (RE) |  | oui | 1500×2150 | 568 Ko |  |
| 6101 | Back Against the Wall (n° 16) | carte de campagne (RE) |  | oui | 1500×2150 | 568 Ko |  |
| 6102 | Bullet Spray (n° 17) | carte de campagne (RE) |  | oui | 1500×2150 | 499 Ko |  |
| 6103 | Bullet Spray (n° 18) | carte de campagne (RE) |  | oui | 1500×2150 | 499 Ko |  |
| 6104 | Flash Bang (n° 19) | carte de campagne (RE) |  | oui | 1500×2150 | 309 Ko |  |
| 6105 | Say Goodnight (n° 20) | carte de campagne (RE) |  | oui | 1500×2150 | 545 Ko |  |
| 6106A | punisher_s hit list (n° 01A) | deux faces |  | oui | 1500×2150 | 472 Ko |  |
| 6106B | satchel charge (n° 01B) | deux faces |  | oui | 1500×2150 | 511 Ko |  |
| 6107 | punisher (n° 02) | carte de campagne (RE) |  | oui | 1500×2150 | 403 Ko |  |
| 6108 | rachel cole alves (n° 03) | carte de campagne (RE) |  | oui | 1500×2150 | 406 Ko |  |
| 6109 | punishers katana (n° 04) | carte de campagne (RE) |  | oui | 1500×2150 | 392 Ko |  |
| 6110 | punishers M1911 (n° 05) | carte de campagne (RE) |  | oui | 1500×2150 | 394 Ko |  |
| 6111 | dramatic entrance (n° 06) | carte de campagne (RE) |  | oui | 1500×2150 | 457 Ko |  |
| 6112 | dramatic entrance (n° 07) | carte de campagne (RE) |  | oui | 1500×2150 | 457 Ko |  |
| 6113 | punishers arsenal (n° 08) | carte de campagne (RE) |  | oui | 2150×1500 | 417 Ko |  |
| 6114 | Punishers Armory (n° 01) | carte de campagne (RE) |  | oui | 2150×1500 | 473 Ko |  |
| 6115 | Punishers Shotgun (n° 02) | carte de campagne (RE) |  | oui | 1500×2150 | 474 Ko |  |
| 6116 | Punishers Sniper Rifle (n° 03) | carte de campagne (RE) |  | oui | 1500×2150 | 373 Ko |  |
| 6117 | Punishers SMG (n° 04) | carte de campagne (RE) |  | oui | 1500×2150 | 449 Ko |  |
| 6118 | Frag Grenade (n° 05) | carte de campagne (RE) |  | oui | 1500×2150 | 359 Ko |  |
| 6119 | SWAT (n° 01) | carte de campagne (AE) |  | oui | 2150×1500 | 473 Ko |  |
| 6120 | Cole North (n° 02) | carte de campagne (RE) |  | oui | 1500×2150 | 431 Ko |  |
| 6121 | Riot Police (n° 03) | carte de campagne (RE) |  | oui | 1500×2150 | 488 Ko |  |
| 6122 | Riot Police (n° 04) | carte de campagne (RE) |  | oui | 1500×2150 | 488 Ko |  |
| 6123 | Tactical Sniper (n° 05) | carte de campagne (RE) |  | oui | 1500×2150 | 459 Ko |  |
| 6124 | Tactical Sniper (n° 06) | carte de campagne (RE) |  | oui | 1500×2150 | 459 Ko |  |
| 6125 | beetle (n° 01) | carte de campagne (RE) |  | oui | 1500×2150 | 425 Ko |  |
| 6126 | white rabbit (n° 02) | carte de campagne (RE) |  | oui | 1500×2150 | 467 Ko |  |
| 6127 | electro (n° 03) | carte de campagne (RE) |  | oui | 1500×2150 | 423 Ko |  |
| 6128 | lady octopus (n° 04) | carte de campagne (RE) |  | oui | 1500×2150 | 472 Ko |  |
| 6129 | scorpia (n° 05) | carte de campagne (RE) |  | oui | 1500×2150 | 393 Ko |  |
| 6130 | trapstr (n° 06) | carte de campagne (RE) |  | oui | 1500×2150 | 427 Ko |  |
| 6131 | the syndicate (n° 07) | carte de campagne (RE) |  | oui | 2150×1500 | 661 Ko |  |
|  | bandeau de la page |  |  | oui | 2000×1125 | 478 Ko |  |

## #basic (8 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6144 | face the past | reprint (art alternatif) | Basic | oui | 1500×2150 | 424 Ko | `49022` |
| 6142 | heli_quincarrier | reprint (art alternatif) | Basic | oui | 1500×2150 | 434 Ko | non branchée, décision utilisateur |
| 6149 | ingenuity | reprint (art alternatif) | Basic | oui | 1500×2150 | 463 Ko | `29027` |
| 6145 | ironheart | reprint (art alternatif) | Basic | oui | 1500×2150 | 439 Ko | `13018` |
| 6146 | professor x | reprint (art alternatif) | Basic | oui | 1500×2150 | 361 Ko | `32019` |
| 6148 | spdr | reprint (art alternatif) | Basic | oui | 1500×2150 | 365 Ko | `30021` |
| 6147 | spider man otto | reprint (art alternatif) | Basic | oui | 1500×2150 | 537 Ko | `31022` |
| 6143 | spider man peter | reprint (art alternatif) | Basic | oui | 1500×2150 | 403 Ko | `27049` |

## #aggression (8 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6153 | angela | reprint (art alternatif) | Aggression | oui | 1500×2150 | 598 Ko | `18011` |
| 6157 | boot camp | reprint (art alternatif) | Aggression | oui | 1500×2150 | 392 Ko | `13016` |
| 6155 | dive bomb | reprint (art alternatif) | Aggression | oui | 1500×2150 | 397 Ko | `17028` |
| 6152 | honed technique | reprint (art alternatif) | Aggression | oui | 1500×2150 | 771 Ko | `28017` |
| 6156 | martial prowess | reprint (art alternatif) | Aggression | oui | 1500×2150 | 480 Ko | `10018` |
| 6151 | sunfire | reprint (art alternatif) | Aggression | oui | 1500×2150 | 381 Ko | `35014` |
| 6150 | throg | reprint (art alternatif) | Aggression | oui | 1500×2150 | 525 Ko | `25014` |
| 6154 | wolverine | reprint (art alternatif) | Aggression | oui | 1500×2150 | 471 Ko | `32041` |

## #justice (8 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6163 | captain britain | reprint (art alternatif) | Justice | oui | 1500×2150 | 497 Ko | `41012` |
| 6161 | crisis averted | reprint (art alternatif) | Justice | oui | 1500×2150 | 548 Ko | `15012` |
| 6160 | CTA | reprint (art alternatif) | Justice | oui | 1500×2150 | 486 Ko | `04049` |
| 6164 | eros | reprint (art alternatif) | Justice | oui | 1500×2150 | 356 Ko | `22011` |
| 6165 | field agent | reprint (art alternatif) | Justice | oui | 1500×2150 | 407 Ko | `27044` |
| 6159 | overwatch | reprint (art alternatif) | Justice | oui | 1500×2150 | 492 Ko | `30019` |
| 6162 | spider man pavitr | reprint (art alternatif) | Justice | oui | 1500×2150 | 503 Ko | `30013` |
| 6158 | wiccan | reprint (art alternatif) | Justice | oui | 1500×2150 | 425 Ko | non branchée, décision utilisateur |

## #leadership (8 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6172 | black panther | reprint (art alternatif) | Leadership | oui | 1500×2150 | 439 Ko | `23012` |
| 6168 | clarity of purpose | reprint (art alternatif) | Leadership | oui | 1500×2150 | 563 Ko | `31029` |
| 6167 | cyclops | reprint (art alternatif) | Leadership | oui | 1500×2150 | 411 Ko | `49015` |
| 6171 | kaluu | reprint (art alternatif) | Leadership | oui | 1500×2150 | 412 Ko | `21014` |
| 6170 | rapid response | reprint (art alternatif) | Leadership | oui | 1500×2150 | 532 Ko | `08031` |
| 6173 | side by side | reprint (art alternatif) | Leadership | oui | 1500×2150 | 553 Ko | `45016` |
| 6166 | strength in numbers | reprint (art alternatif) | Leadership | oui | 1500×2150 | 451 Ko | `03017` |
| 6169 | white tiger | reprint (art alternatif) | Leadership | oui | 1500×2150 | 551 Ko | `21013` |

## #protection (8 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6179 | armor | reprint (art alternatif) | Protection | oui | 1500×2150 | 395 Ko | `38012` |
| 6176 | dr sinclair | reprint (art alternatif) | Protection | oui | 1500×2150 | 457 Ko | `52017` |
| 6181 | electrostatic armor | reprint (art alternatif) | Protection | oui | 1500×2150 | 581 Ko | `10031` |
| 6175 | ready for a fight | reprint (art alternatif) | Protection | oui | 1500×2150 | 637 Ko | `52019` |
| 6178 | rogue | reprint (art alternatif) | Protection | oui | 1500×2150 | 419 Ko | `48012` |
| 6180 | silk | reprint (art alternatif) | Protection | oui | 1500×2150 | 409 Ko | `27010` |
| 6177 | spider UK | reprint (art alternatif) | Protection | oui | 1500×2150 | 530 Ko | `27012` |
| 6174 | what doesnt kill me | reprint (art alternatif) | Protection | oui | 1500×2150 | 577 Ko | `27016` |

## #campaign-challenge (15 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6132A | campaign 1 instructions (n° 01A) | deux faces |  | oui | 1500×2150 | 401 Ko |  |
| 6132B | campaign 1 reward (n° 01B) | deux faces |  | oui | 1500×2150 | 455 Ko |  |
| 6133A | campaign 2 instructions (n° 02A) | deux faces |  | oui | 1500×2150 | 419 Ko |  |
| 6133B | campaign 2 reward (n° 02B) | deux faces |  | oui | 1500×2150 | 481 Ko |  |
| 6134A | campaign 3 instructions (n° 03A) | deux faces |  | oui | 1500×2150 | 398 Ko |  |
| 6134B | campaign 3 reward (n° 03B) | deux faces |  | oui | 1500×2150 | 452 Ko |  |
| 6135A | kingsfall instructions (n° 01A) | deux faces |  | oui | 1500×2150 | 404 Ko |  |
| 6135B | power to the people (n° 01B) | deux faces |  | oui | 1500×2150 | 457 Ko |  |
| 6136A | Long Live (n° 02A) | deux faces |  | oui | 1500×2150 | 456 Ko |  |
| 6136B | Down With (n° 02B) | deux faces |  | oui | 1500×2150 | 437 Ko |  |
| 6137 | The King (n° 03) | carte de campagne (AE) |  | oui | 1500×2150 | 453 Ko |  |
| 6140A | rise of the machines (n° 01) | deux faces |  | oui | 1500×2150 | 349 Ko |  |
| 6140B | secret agent (n° 02) | deux faces |  | oui | 1500×2150 | 337 Ko |  |
| 6141A | its a trap (n° 03) | deux faces |  | oui | 1500×2150 | 271 Ko |  |
| 6141B | angry birds (n° 04) | deux faces |  | oui | 1500×2150 | 361 Ko |  |

## #other (6 images)

| N° | Nom | Type | Aspect | Fichier | Dimensions | Poids | Branché |
|---|---|---|---|---|---|---|---|
| 6138 | punisher | reprint (art alternatif) | Aggression | oui | 1500×2150 | 454 Ko | à créer avec la campagne Punisher |
| 6139 | Capo of the Past | carte de campagne (RE) |  | oui | 1500×2150 | 392 Ko |  |
| 6182A | Clint Barton | deux faces |  | oui | 1500×2150 | 404 Ko |  |
| 6182B | Hawkeye | deux faces |  | oui | 1500×2150 | 418 Ko |  |
| 6183A | punisher hand A |  |  | oui | 1500×2150 | 467 Ko |  |
| 6183B | punisher hand B |  |  | oui | 1500×2150 | 475 Ko |  |

Total : 215 fichiers présents sur 215.
