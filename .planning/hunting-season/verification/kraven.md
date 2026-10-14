# Vérification groupe « kraven » (hs104-hs124, hs157-hs163), 28 scans

Bilan : 19 CONFORME, 9 ÉCART, 0 DOUTE.

Remarques globales (cosmétiques, non comptées en écart) :
- Les stats portant une étoile sur le scan (ATK 0★ hs110, ATK ★ hs111/hs113, SCH +1★ hs114, ATK 2★ hs158, ATK 3★ hs159, SCH 2★/ATK 3★ hs160, SCH 1★/ATK 2★ hs161, SCH 0★ hs163) sont saisies sans étoile dans desc. Valeurs numériques correctes. Pour hs111 et hs113 le scan montre « ★ » à la place d'une valeur d'ATK (pas de chiffre), absent du JSON.
- hs110 : le scan met une étoile devant « Forced Interrupt : When Chameleon would attack », absente du JSON.
- Numérotation des scans : Kraven The Hunter (n/21) pour hs104-124 (hs107 = 4/21, hs108 = 5/21, hs109 = 6/21 ... hs124 = 21/21), Savage Six (n/7) pour hs157-163 (1/7 à 7/7). Les cartes à 2 exemplaires (hs117/118, 119/120, 121/122, 123/124) sont numérotées séparément (14 à 21).
- hs107, hs108 sont des cartes recto (A) et verso (B) séparées, scans a/b.

## Tableau

| card_id | verdict | résumé |
|---|---|---|
| hs104 | CONFORME | Kraven I, PV 15 par joueur, SCH 2 ATK 2, texte identique |
| hs105 | CONFORME | Kraven II, PV 17 par joueur, SCH 2 ATK 2, texte identique |
| hs106 | CONFORME | Kraven III, PV 19 par joueur, SCH 3 ATK 3, « twice per round per player » ok |
| hs107a | ÉCART | Contents sans « Trap deck », Setup différent |
| hs107b | ÉCART | « flip » au lieu de « change », « this scheme » au lieu de « here », étoile en trop |
| hs108a | CONFORME | « the Calypso Serum » (JSON « The ») : différence d'article sans effet |
| hs108b | ÉCART | Clause de défaite : « stage » / « have been hunted and therefore lose » |
| hs109 | ÉCART | Limite « once per round » sur le scan, le JSON ajoute « per player » |
| hs110 | CONFORME | Chameleon HP 1 SCH 1 ATK 0★ coût 1 ; étoile de texte absente (cosmétique) |
| hs111 | CONFORME | Poisoned Dagger boost 2, ATK ★, texte identique |
| hs112 | CONFORME | Kraven's Spear ATK +1, boost 2, retaliate 1, texte identique |
| hs113 | ÉCART | Condition de dégâts reformulée (« doesn't damage you » vs « you take no damage from that attack ») |
| hs114 | CONFORME | Tooth Necklace SCH +1★, boost 1, texte identique |
| hs115 | CONFORME | Calypso Serum menace 3, icône danger (carte +), boost 3 (3 icônes), texte identique |
| hs116 | CONFORME | Toxic Gas menace 3, boost 2, icône de forme maison+croix (accélération, forme à confirmer), texte identique |
| hs117 | ÉCART | « Kraven The Hunter attacks you » au lieu de « The villain attacks you » |
| hs118 | ÉCART | Idem hs117 |
| hs119 | CONFORME | Boost 1, texte identique à des reformulations de rédaction près (« attachments were revealed ») |
| hs120 | CONFORME | Idem hs119 |
| hs121 | ÉCART | « Other characters cannot defend against this attack » vs « Other players cannot defend this attack » |
| hs122 | ÉCART | Idem hs121 |
| hs123 | CONFORME | Boost 0 (étoile seule), texte identique |
| hs124 | CONFORME | Idem hs123 |
| hs157 | CONFORME | The Savage Six menace 3 par joueur, danger, boost 3, texte identique |
| hs158 | CONFORME | Vulture PV 4 SCH 2 ATK 2★, boost 1, texte identique |
| hs159 | CONFORME | Rhino PV 6 SCH 1 ATK 3★, boost 1, texte identique |
| hs160 | CONFORME | Scorpion PV 5 SCH 2★ ATK 3★, boost 1, texte identique |
| hs161 | CONFORME | Tarantula PV 4 SCH 1★ ATK 2★, boost 1, texte identique |
| hs162 | CONFORME | King Cobra PV 5 SCH 2 ATK 1, boost 1, texte identique |
| hs163 | CONFORME | Stegron PV 6 SCH 0★ ATK 2, boost 1, texte identique |

Note : sur les minions le grand chiffre dans le cercle orange/rouge (bas droite de l'illustration) est le nombre de PV du scan (hs109 : 6, hs110 : 1, hs158 : 4, hs159 : 6, hs160 : 5, hs161 : 4, hs162 : 5, hs163 : 6), tous égaux au JSON.

## Détail des écarts

### hs107a (Acquiring Targets 1A)
- Scan : « Contents: Kraven The Hunter (I) and Kraven The Hunter (II). (Kraven The Hunter (II) and Kraven The Hunter (III) instead for expert mode.) Kraven The Hunter and Standard encounter sets. Trap deck. One modular encounter set (recommended: Savage Six). / Setup: Kraven The Hunter starts the game with a separate TRAP deck. (See insert.) Advance to stage 1B. »
- JSON : « ... Kraven The Hunter and Standard encounter sets. One modular encounter set (recommended: Savage Six). / Setup: Shuffle all of the TRAP cards into a separate TRAP deck. Advance to stage 1B. »
- Diffère : « Trap deck. » absent des Contents ; Setup reformulé (« starts the game with a separate TRAP deck (See insert) » remplacé par « Shuffle all of the TRAP cards into a separate TRAP deck »).
- Effet : le contenu de mise en place ne mentionne pas le paquet Trap comme élément du scénario ; le mélange explicite est une interprétation de l'insert, pas du scan.

### hs107b (Acquiring Targets 1B, menace cible 7 par joueur, départ 0, escalade +1 par joueur : conformes)
- Scan : « Forced Interrupt: When you flip to hero form, place 2 threat here. / Forced Response: After you flip to alter-ego form, remove 1 threat from this scheme. » (aucune étoile devant)
- JSON : « [star] Forced Interrupt: When you change to hero form, place 2 threat here. / Forced Response: After you change to alter-ego form, remove 1 threat from here. »
- Diffère : « flip » au lieu de « change » (deux fois), « this scheme » au lieu de « here », étoile ajoutée devant le premier effet.
- Effet : « flip » est le terme officiel ; « change » est équivalent en pratique mais le moteur peut cibler un mot-clé différent. Étoile en trop sans effet de règle.

### hs108b (The Great Hunt 2B, menace 9 par joueur, départ 0, escalade +1 par joueur : conformes)
- Scan : « If this stage is completed, the players have been hunted and therefore lose the game. » (en gras)  Réponse forcée : « After a TRAP card is revealed, place 1 threat here. (Limit once per player per round.) »
- JSON : « If this scheme is completed, the players lose the game. »
- Diffère : « stage » / « scheme », et la partie « have been hunted and therefore » manque.
- Effet : sens de règle identique ; le mot « stage » est le terme du scan.

### hs109 (Last Son of Kraven)
- Scan : « ... deal yourself a TRAP card from the TRAP deck. (Limit once per round.) »
- JSON : « ... (Limit once per round per player.) »
- Diffère : « per player » ajouté.
- Effet : sur le scan la limite est globale (une fois par round pour toute la table) ; le JSON la rend par joueur, donc plus de déclenchements en multijoueur.

### hs113 (Hunting Rifle)
- Scan : « Forced Response: After Kraven The Hunter attacks you and doesn't damage you, take 1 damage. »
- JSON : « After Kraven The Hunter attacks you and you take no damage from that attack, take 1 damage. »
- Diffère : formulation. « doesn't damage you » (l'attaque ne vous inflige pas de dégâts) vs « you take no damage ».
- Effet : quasi identique ; un doute possible si les dégâts sont absorbés par un bouclier/prévention (ce que Kraven « inflige » vs ce que vous « prenez »).

### hs117 et hs118 (Predatory Ambush)
- Scan : « When Revealed: Kraven The Hunter attacks you. If you are in alter-ego form, do not give the villain a boost card for this activation. If you have a TRAP attachment attached to you, deal yourself a TRAP card from the TRAP deck. »
- JSON : « The villain attacks you. ... If you have a TRAP attachment on you, ... »
- Diffère : « Kraven The Hunter » remplacé par « The villain » ; « attached to you » devient « on you ».
- Effet : si un autre vilain est en jeu (stade ou scénario modulaire), « The villain » désigne le vilain en cours et non spécifiquement Kraven.

### hs121 et hs122 (Big Game Hunter)
- Scan : « Kraven The Hunter attacks the hero with the highest printed hit points. Other characters cannot defend against this attack. If no attacks were made this way, deal yourself a TRAP card from the TRAP deck. »
- JSON : « ... Other players cannot defend this attack. ... »
- Diffère : « Other characters » devient « Other players ».
- Effet : le scan interdit à tout autre personnage (alliés compris) de défendre ; le JSON ne vise que les autres joueurs, un allié du joueur ciblé ne serait pas exclu.
