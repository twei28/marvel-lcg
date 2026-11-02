# Hellfire Hunt, scenario 2 « Black King » (Dipsome), prefixe `hf` : gabarits PROCESSUS-CARTE (01/11/2026)

Worktree `Marvel-LCG-campagnes`, branche `campagnes-fanmade`. Pack `hellfire_hunt_black_king` (set 242) : hf201-hf227 (scenario, numero du scan + 200) + module « Sebastian Shaw » hf331-hf338 (porte ICI seul, reutilise par Torn via `hf_sebastian_shaw`).
Scenarios : `hellfire_black_king` (Shaw I puis II) et `hellfire_black_king_expert` (II puis III). Cas : `tools/cas/hellfire_black_king.py` (noms `[hf] hfNNN ...`, verificateur `hfk_etat`). Generation des donnees (idempotente) : `docs/packs/hellfire-hunt-black-king/generer_donnees.py`. Doutes de regle : `QUESTIONS.md`.

## Etat net
- Cartes : 38 entrees `cards.json` (30 scans du scenario, 4 doubles faces comptees par face, + 8 du module hf331-hf338). Cas : 124.
- Preuve par substitution (`tools/substituer_pack.py`, prefixes hf20, hf21, hf22, hf33) : voir par carte ci-dessous (« rouges N/M » avec M>N = les temoins/contre-cas d'ABSENCE d'effet et les mots-cles natifs de `desc` restent verts sans module, comme prevu par PROCESSUS-CARTE) ; sortie brute : `/tmp/hfk/subst.txt` (recopiee en fin de fichier).
- Autoplay : `tools/autoplay.py` (game_dir `.game-src-hfk-auto`, ports 9950-9979) : Sunspot (`sunspot_hellfire`) 4 parties normal + 4 expert = 8 parties : 0 victoire / 8 defaites (4 « The Main Scheme was Completed », 4 « All players were eliminated », 2,2 a 3,0 rounds) ; TEMOIN Spider-Man (`spider_man`) 4 parties normal : 0 / 4 (3 complots complets, 1 elimine, 5,0 rounds). grep `NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback` sur les 12 journaux `/tmp/autoplay_*hellfire_black_king*.log` : 0 partout. Journal lu (spider_man normal 1) : Setup, Captured by Hellfire!, Black King qui convertit 2 compteurs en 2 menaces (« Black King (Forced Interrupt) AfterUnitTookDamage »), escalade +1 par round, « La menace ne peut pas etre retiree » sur 1B face a Surveillance Team, complot complet au round 4. Le pilote ne sait pas defaire Captured by Hellfire! (le seul moyen d'avancer a 2A) : 0 % de victoire est donc attendu et identique au temoin ; ce n'est PAS une mesure d'equilibre.
- **« Carte terminee : NON (partie humaine a faire) » pour TOUTES les cartes** : aucune partie reelle n'a ete jouee dans le navigateur par un humain ; le controle du voile FR dans Chromium n'a pas pu etre fait (aucun navigateur connecte a cette session).
- Extensions moteur : AUCUNE dans `src/game/**`. Fondations touchees (additif, `src/cards/pack/hellfire_hunt/campaign.py`) : `CAPTIFS`, captifs acceptes par `_allies_recrutes`, releve des captifs liberes (`_captif_libere`), revelation d'Emma Frost's Redemption au scenario 2 (livret p. 10 : etape manquante).

## Pieges de harnais (recopies dans RECETTES-MOTEUR §40)
- `Puzzle.CreateEncounterDeck(a, b, c)` pose `a` en DERNIER ; `deck()` inverse la liste.
- `main_exclusive` met 01090 (RR !) en main par defaut ; deux attaques du meme heros : `Puzzle.Ready('01001a')` entre les deux ; nouveau round : `Puzzle.ResetRoundStats()`.
- `Rand.RandomChoice` n'est pas deterministe : mesurer des comptes.
- Un sbire unique (« * Sebastian Shaw ») ne peut pas entrer en jeu a cote du vilain homonyme : tester hf331 dans le scenario White Queen.
- Charge machine : 6 cas paralleles + autres agents = « processus mort » ; relancer a 3.

### hf201 : Sebastian Shaw

- [x] Etape 2 : cartes de reference : Sebastian Shaw (stade I), vilain. « Absorb » + Forced Interrupt a l'attaque : voir `AbilitesDeShaw` (__init__.py). Cartes de reference : the_hunger_core / shadowland Elektra (`WhenUnitWouldAttack(ForcedInterrupt, "This")` + `GainATKForThisAttack`), sk151 (`AfterUnitTookDamage` « After X takes damage », `message.took_damage`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf201.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "13*", "ATK": "0*", "SCH": "2", "Stage": "1"} ; traits ['HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (6) : hf201 Absorb : le heros inflige 2 degats -> 2 compteurs d'energie sur Shaw | hf201 Absorb : TEMOIN, des degats qui ne viennent PAS d'une attaque (Puzzle.Damage) n | hf201 Interruption forcee : Shaw (2 compteurs) attaque le heros -> +2 ATK pour cette  | hf201 Interruption forcee : au plus 3 compteurs retires -> 5 compteurs : 3 retires (+ | hf201 Interruption forcee : TEMOIN, Shaw sans compteur attaque avec son ATK imprimee  | hf201 stade vaincu : Black King (Permanent) reste attache a Shaw (II)
      preuve par substitution : rouges 3/6 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteurs energie). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf202 : Sebastian Shaw

- [x] Etape 2 : cartes de reference : Sebastian Shaw (stade II), vilain. « Absorb » + Forced Interrupt a l'attaque : voir `AbilitesDeShaw` (__init__.py). Cartes de reference : the_hunger_core / shadowland Elektra (`WhenUnitWouldAttack(ForcedInterrupt, "This")` + `GainATKForThisAttack`), sk151 (`AfterUnitTookDamage` « After X takes damage », `message.took_damage`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf202.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "15*", "ATK": "1*", "SCH": "3", "Stage": "2"} ; traits ['HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf202 stade II : PV 15, ATK 1, SCH 3 ; Absorb et interruption identiques (le heros in | hf202 Absorb : stade II, le heros inflige 2 degats -> 2 compteurs | hf202 Interruption forcee : stade II, 2 compteurs -> ATK 1 + 2 = 3 degats
      preuve par substitution : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteurs). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf203 : Sebastian Shaw

- [x] Etape 2 : cartes de reference : Sebastian Shaw (stade III, mode expert), vilain. Meme texte que (I)/(II) + « Place 1 additional energy counter here. » a la fin de l'Absorb. Cartes de reference : voir hf201.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf203.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "17*", "ATK": "1*", "SCH": "3", "Stage": "3"} ; traits ['HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf203 mode expert : la partie commence au stade II (PV 15), le stade I est retire | hf203 Absorb : stade III, 2 degats d'attaque -> 3 compteurs (2 + 1 supplementaire) | hf203 Absorb : TEMOIN, au stade II (expert aussi) la meme attaque ne donne que 2 comp
      preuve par substitution : rouges 1/3 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (compteurs). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf204a : Jailbreak at the Hellfire Club

- [x] Etape 2 : cartes de reference : Jailbreak at the Hellfire Club (1A). « Setup : Remove each minion named Sebastian Shaw from the game. Set each CAPTIVE ally aside. Reveal the Captured by Hellfire! side scheme. Attach Black King to Sebastian Shaw. » (`MiseEnPlaceDuScenario`, __init__.py) + mise en place de CAMPAGNE commune (`CampaignSetup(2)` : deck Recruited Mutants, Potential Ally, Xavier's Institute, Emma Frost's Redemption). Cartes de reference : hf104a (White Queen : `WhenCardSetup("This", ...)` + `Faces.RemoveAllFromGame`), tk001a (Black King = attachement mis de cote par le scenario puis mis en jeu), cards.pack.skrull_menace.campaign (`CampaignSetup`). ⚠ Mot-piege : « minion named Sebastian Shaw » : le VILAIN porte le meme nom ; le filtre est `Minion.IsType`.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf204a.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Stage": "1"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (4) : hf204a mise en place : Sebastian Shaw I en jeu (PV 13, ATK 0, SCH 2), complot 1B a 0  | hf204a Setup : Captured by Hellfire! revelee (menace 5), un captif cache dessous (1 p | hf204a Setup : le sbire Sebastian Shaw (hf331) du module n'est PAS dans le deck de re | hf204a Setup a DEUX joueurs : deux captifs caches sous Captured by Hellfire! (1 par j
      preuve par substitution : rouges 3/4 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf204b : Jailbreak at the Hellfire Club

- [x] Etape 2 : cartes de reference : Jailbreak at the Hellfire Club (1B). « Threat cannot be removed from this scheme. Forced Interrupt : When Sebastian Shaw would scheme against you, deal you 1 facedown encounter card instead. If this stage is completed, the players lose the game. » (le dernier est lu dans le texte imprime). Cartes de reference : 01139b Countdown to Oblivion (`ThreatCannotBeRemovedFromWhile("This")`), sk099 (`WhenUnitWouldScheme` + `SetBeInstead`), 40146 / the_hunger_core (« instead » d'une activation).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf204b.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"StartingThreat": "0", "TargetThreat": "5*", "EscalationThreat": "1*", "Stage": "1"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (4) : hf204b Threat cannot be removed : une attaque de menace du heros (THW 1) laisse les 3 | hf204b Threat cannot be removed : TEMOIN, la meme action contre une side scheme (hf22 | hf204b Interruption forcee : contre un ALTER-EGO, Shaw (I) ne manigance pas : le joue | hf204b stade 1 complete : « the players lose the game »
      preuve par substitution : rouges 2/4 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf205a : Operation Hellfire Ascendant

- [x] Etape 2 : cartes de reference : Operation Hellfire Ascendant (2A). « When Revealed : Deal each player a facedown encounter card. Flip Black King attachment. » Cartes de reference : tk007a (`card.Flip(effect)` d'un attachement a deux faces), 01121 / hf124 (`DealEncounterCards`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf205a.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Stage": "2"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (2) : hf205a When Revealed : chaque joueur recoit 1 carte face cachee et Black King se RETO | hf205a When Revealed : a DEUX joueurs chacun recoit sa carte (le joueur 1 en recoit 1
      preuve par substitution : rouges 2/2
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf205b : Operation Hellfire Ascendant

- [x] Etape 2 : cartes de reference : Operation Hellfire Ascendant (2B). « Hero Action : Exhaust a CAPTIVE ally you control -> remove 2 energy counters from Sebastian Shaw. (Limit once per round per player.) If this stage is completed, the players lose the game. » Cartes de reference : dz026 / pt004 (`CostFunc.Exhaust("YourAlly")`), 31009-like `LimitOncePerRoundPerPlayer` (FAQ du livret p. 22 : une fois par round et PAR JOUEUR, meme si l'on a plusieurs captifs).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf205b.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"StartingThreat": "4*", "TargetThreat": "13*", "EscalationThreat": "1*", "Stage": "2"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (6) : hf205b nombres : menace de depart 4 pour 1 joueur, cible 13 ; complete -> les joueurs | hf205b menace de depart : 4 | hf205b Hero Action : exhaust a CAPTIVE ally -> 2 compteurs d'energie retires de Shaw  | hf205b Hero Action : TEMOIN D'EPUISEMENT, DEUX captifs prets mais une seule Action pa | hf205b Hero Action : la limite se renouvelle au round suivant -> 5 -> 3 -> 1 | hf205b stade 2 : Shaw manigane normalement (plus de remplacement par une carte face c
      preuve par substitution : rouges 3/6 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? OUI : « once per round per player » : cas `hf205b Hero Action : TEMOIN D'EPUISEMENT` (5 -> 3, pas 1) + renouvellement au round suivant (5 -> 3 -> 1)
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf206 : Captured by Hellfire!

- [x] Etape 2 : cartes de reference : Captured by Hellfire! (side scheme 5, Permanent, Victory 1). « When Revealed : Place 1[per player] random set-aside CAPTIVE allies facedown beneath this scheme. When Defeated : The player who defeated this scheme takes a random card from beneath here, and add it to their hand. After that, if there still has card under this scheme, place 5 threat here. Otherwise, advance to main scheme 2A and add this card to the victory display. » Cartes de reference : sk265 / sk267 (cartes glissees sous une carte : `PlaceCardHere(face, False, effect)`, `GetPlacedCardArea()`), 60113a (side scheme PERMANENT : le moteur envoie « When Defeated » sans la defausser : `EncounterSideScheme.OnBeDefeated`), 04141 (`WhenSchemeBeDefeated`, `message.defeating_player`), `Faces.AddToVictoryDisplay`. ⚠ Mots-pieges : « beneath » = face cachee SOUS la carte ; « random » = `Rand.RandomChoice` (deterministe en test) ; « th
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf206.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"StartingThreat": "5", "Victory": "1", "Permanent": "1"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (5) : hf206 When Defeated (1 joueur, 1 captif dessous) : le joueur qui la defait prend le c | hf206 When Defeated : le captif libere est bien un des quatre allies CAPTIVE (jamais  | hf206 When Defeated (2 joueurs, 2 captifs dessous) : 1er captif pris, il en reste 1 - | hf206 When Defeated (2 joueurs) : la 2e defaite prend le dernier captif -> victoire + | hf206 Permanent : tant qu'il reste un captif la manigance ne quitte pas le jeu apres 
      preuve par substitution : rouges 4/5 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (captifs glisses dessous). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf207a : Black King

- [x] Etape 2 : cartes de reference : Black King (face A), attachement TITLE Permanent. Mis en jeu par le Setup de 1A (hf204a), il s'attache a Sebastian Shaw. « King's Tactic » : voir `TactiqueDuRoi` (__init__.py). Cartes de reference : tk007a (Hog Wild, attachement a deux faces : `AttachToFaceWhenPutIntoPlay(SurLeVilain(...))`, `card.Flip`), sk151 (`AfterUnitTookDamage(..., "AttachedEnemy", ...)`). Permanent : desc, natif (has_permanent.py).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf207a.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Permanent": "1"} ; traits ['TITLE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf207a King's Tactic : Shaw a 3 compteurs et absorbe 2 degats -> les 3 sont retires A | hf207a King's Tactic : TEMOIN, Shaw sans compteur -> aucune conversion (2 compteurs p | hf207a King's Tactic : face A sans limite -> DEUX Absorb dans le round convertissent 
      preuve par substitution : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attachement sur Shaw). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf207b : "And What Is Theirs... Is Mine."

- [x] Etape 2 : cartes de reference : « And What Is Theirs... Is Mine. » (Black King, face B), apres le retournement de 2A. « Sebastian Shaw gains stalwart while there is more than 5 energy counters on him. » + King's Tactic limitee a 1[par joueur] par round. Cartes de reference : tk007a (`GiveKeywordToAttached(Villain, get_new_value=..., ex_change_on_event=OnEvent.Counter(...))`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf207b.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Permanent": "1"} ; traits ['TITLE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (8) : hf207b King's Tactic : face B, premiere instance du round -> conversion (3 compteurs  | hf207b King's Tactic : TEMOIN D'EPUISEMENT, 2e Absorb du MEME round (1 joueur) -> pas | hf207b King's Tactic : la limite se renouvelle au round suivant -> 2e conversion (2 c | hf207b King's Tactic : a DEUX joueurs la limite est de 2 par round -> 2 conversions p | hf207b Stalwart : Shaw a 6 compteurs (plus de 5) -> stalwart ; avec 5 -> pas stalwart | hf207b Stalwart : TEMOIN, 5 compteurs exactement -> pas de stalwart | hf207b Stalwart : TEMOIN, face A avec 6 compteurs -> pas de stalwart (propre a la fac | hf207b Stalwart : les compteurs retires (Hero Action de 2B, 6 -> 4) font perdre le st
      preuve par substitution : rouges 5/8 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? OUI : « Max 1[per player] times per round » : cas `hf207b ... TEMOIN D'EPUISEMENT` (2e Absorb du round : 2 -> 4 compteurs, menace inchangee 7), renouvellement, 2 joueurs
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attachement, compteurs). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf208 : Dust

- [x] Etape 2 : cartes de reference : Dust (Sooraya Qadir), allie CAPTIVE MUTANT. « [star] Interrupt : When Dust attacks, resolve this attack against the villain and each minion engaged with you. » Cartes de reference : 33012 Dust (officiel, meme nom, ATTAQUE tous les sbires : `WhenUnitWouldAttack(Interrupt, "This", op)` + `message.AlsoResolveThisAttackTo(units)`), 01130 Whirlwind (`AlsoResolveThisAttackTo`). ⚠ Mots-pieges : « the villain AND each minion engaged WITH YOU » : le vilain + les sbires engages avec le CONTROLEUR de Dust (pas tous les sbires) ; `AlsoResolveThisAttackTo` ignore la cible deja visee (jamais de doublon). Allie : consequences = icones imprimees (`desc.ATK "2**"`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf208.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Cost": "2", "HP": "3", "ATK": "2**", "THW": "2*", "RES": "R", "Class": "Campaign;Basic"} ; traits ['CAPTIVE', 'MUTANT']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (5) : hf208 Dust : l'attaque vise un sbire engage (Tiger Shark) ET le vilain : 2 degats a c | hf208 Dust : TEMOIN, un sbire engage avec un AUTRE joueur n'est pas touche (2 joueurs | hf208 Dust : l'attaque vise le VILAIN : le sbire engage est touche aussi (pas de doub | hf208 RECRUITED : un captif note « Recruited » au carnet porte le trait RECRUITED (sc | hf208 RECRUITED : TEMOIN, dans le scenario 2 lui-meme (carnet sans lui) il n'est PAS 
      preuve par substitution : rouges 4/5 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf209 : Mercury

- [x] Etape 2 : cartes de reference : Mercury (Cessily Kincaid), allie CAPTIVE MUTANT. « Toughness. » (desc, natif). Seule capacite : le trait RECRUITED une fois la campagne notee. Carte de reference : hf208 (`CaptifRecrute`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf209.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Cost": "2", "HP": "5", "ATK": "2***", "THW": "2***", "RES": "B", "Toughness": "1", "Class": "Campaign;Basic"} ; traits ['CAPTIVE', 'MUTANT']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (2) : hf209 Mercury : valeurs imprimees (PV 5, Toughness : arrive avec un statut Robuste) | hf209 RECRUITED : Mercury note « Recruited » au carnet porte le trait RECRUITED (scen
      preuve par substitution : rouges 1/2 (RECRUITED rouge ; Toughness natif reste vert)
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf210 : Surge

- [x] Etape 2 : cartes de reference : Surge (Noriko Ashida), allie CAPTIVE MUTANT. « [star] Interrupt : When Surge attacks an enemy, that enemy get stunned. » Cartes de reference : hf208 (`WhenUnitWouldAttack(Interrupt, "This", op)`), 01083 / 05015 (`Faces.GiveStatus(cibles, "Stunned", effect)`). ⚠ « attacks an ENEMY » : les cibles de l'attaque qui sont des ennemis ; l'Interruption est au CHOIX du joueur (Interrupt, pas Forced).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf210.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Cost": "2", "HP": "2", "ATK": "1*", "THW": "2*", "RES": "Y", "Class": "Campaign;Basic"} ; traits ['CAPTIVE', 'MUTANT']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf210 Surge : elle attaque le vilain -> Shaw est ETOURDI (Interruption) | hf210 Surge : TEMOIN, Mercury (sans texte) attaque le vilain -> pas d'etourdissement | hf210 RECRUITED : Surge note « Recruited » au carnet porte le trait RECRUITED (scenar
      preuve par substitution : rouges 2/3 (temoin Mercury reste vert)
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf211 : Prodigy

- [x] Etape 2 : cartes de reference : Prodigy (David Alleyne), allie CAPTIVE MUTANT. « Response : After you play Prodigy from hand, draw 1 card. » Carte de reference : sj012 (`AfterPlayerPlayedCard(Response, "You", "This", op, from_hand=True)`, recette « After you play X from your hand » sur la carte elle-meme), `player.DrawUp`.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf211.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Cost": "1", "HP": "1", "ATK": "1*", "THW": "1*", "RES": "G", "Class": "Campaign;Basic"} ; traits ['CAPTIVE', 'MUTANT']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf211 Prodigy : jouee DEPUIS LA MAIN -> pioche 1 carte (main 1 : la carte piochee) | hf211 Prodigy : TEMOIN, mise en jeu autrement que depuis la main -> pas de pioche (la | hf211 RECRUITED : Prodigy note « Recruited » au carnet porte le trait RECRUITED (scen
      preuve par substitution : rouges 2/3 (temoin sans pioche reste vert)
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf212 : Ebon Knight

- [x] Etape 2 : cartes de reference : Ebon Knight (x4, hf212-hf215). Sbire HELLFIRE, Guard + Patrol + Quickstrike (desc, natif). « [star] Boost : After this activation, deal Ebon Knight to you as a facedown encounter card. » Cartes de reference : 01121 Weapons Runner (boost qui agit sur LA carte), 49042 (`message.AfterThisActivation`), `player.DealEncounterCard(face, effect)` (Puzzle.Deal). ⚠ « deal to YOU » : le joueur qui subit l'activation (`message.GetToPlayer()`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf212.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "2", "ATK": "2", "SCH": "2", "Boost": "1", "Guard": "1", "Patrol": "1", "Quickstrike": "1"} ; traits ['HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf212 Ebon Knight : valeurs imprimees (PV 2, ATK 2, SCH 2), Guard + Patrol + Quickstr | hf212 Boost : Shaw attaque avec Ebon Knight en boost (1 icone : 0 + 1 = 1 degat) -> A | hf212 Boost : TEMOIN, une carte de boost sans effet (Bomb Scare) -> rien n'est distri
      preuve par substitution : rouges 1/3 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf213 : Ebon Knight

- [x] Etape 2 : cartes de reference : Ebon Knight (x4, hf212-hf215). Sbire HELLFIRE, Guard + Patrol + Quickstrike (desc, natif). « [star] Boost : After this activation, deal Ebon Knight to you as a facedown encounter card. » Cartes de reference : 01121 Weapons Runner (boost qui agit sur LA carte), 49042 (`message.AfterThisActivation`), `player.DealEncounterCard(face, effect)` (Puzzle.Deal). ⚠ « deal to YOU » : le joueur qui subit l'activation (`message.GetToPlayer()`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf213.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "2", "ATK": "2", "SCH": "2", "Boost": "1", "Guard": "1", "Patrol": "1", "Quickstrike": "1"} ; traits ['HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf213 Ebon Knight (2e exemplaire) : meme carte, meme boost
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf214 : Ebon Knight

- [x] Etape 2 : cartes de reference : Ebon Knight (x4, hf212-hf215). Sbire HELLFIRE, Guard + Patrol + Quickstrike (desc, natif). « [star] Boost : After this activation, deal Ebon Knight to you as a facedown encounter card. » Cartes de reference : 01121 Weapons Runner (boost qui agit sur LA carte), 49042 (`message.AfterThisActivation`), `player.DealEncounterCard(face, effect)` (Puzzle.Deal). ⚠ « deal to YOU » : le joueur qui subit l'activation (`message.GetToPlayer()`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf214.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "2", "ATK": "2", "SCH": "2", "Boost": "1", "Guard": "1", "Patrol": "1", "Quickstrike": "1"} ; traits ['HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf214 Ebon Knight (3e exemplaire) : meme boost
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf215 : Ebon Knight

- [x] Etape 2 : cartes de reference : Ebon Knight (x4, hf212-hf215). Sbire HELLFIRE, Guard + Patrol + Quickstrike (desc, natif). « [star] Boost : After this activation, deal Ebon Knight to you as a facedown encounter card. » Cartes de reference : 01121 Weapons Runner (boost qui agit sur LA carte), 49042 (`message.AfterThisActivation`), `player.DealEncounterCard(face, effect)` (Puzzle.Deal). ⚠ « deal to YOU » : le joueur qui subit l'activation (`message.GetToPlayer()`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf215.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "2", "ATK": "2", "SCH": "2", "Boost": "1", "Guard": "1", "Patrol": "1", "Quickstrike": "1"} ; traits ['HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf215 Ebon Knight (4e exemplaire) : meme boost
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf216 : Inhibitor Collar

- [x] Etape 2 : cartes de reference : Inhibitor Collar (x2, hf216-hf217). Attachement TECH ARTIFACT. « Attach to your identity. Treat your identity's printed text box as blank (except for TRAITS). Alter-Ego Action : Spend [physical][physical] resources -> discard this card. Any player may trigger this ability. [star] Boost : If this activation is an attack, this attack gains overkill. » Cartes de reference EXACTES : ld017 / 40092 Inhibitor Collar (meme attache + texte blanc + `PlayerActionToDiscardThis(...).AnyPlayerCanDoThis()`), hf110 (`PlayerActionToDiscardThis(...).SetCost(Cost(...))`), 16134 (`message.would_atk_message.GainOverKill`). ⚠ Icone de ressource : le poing = [physical] = `R` (so002 / hf110 du meme auteur), `Cost("RR")` ; l'action est « Alter-Ego Action » (pas Hero).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf216.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "2"} ; traits ['TECH', 'ARTIFACT']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (7) : hf216 Inhibitor Collar : revele, s'attache a l'IDENTITE du joueur et son texte imprim | hf216 Inhibitor Collar : TEMOIN, sans collier le texte de l'identite n'est pas blanc | hf216 Alter-Ego Action : depenser [physical][physical] (2 Strength) defausse le colli | hf216 Alter-Ego Action : TEMOIN, une seule ressource ne suffit pas -> le collier rest | hf216 Alter-Ego Action : ANY PLAYER, le 2e joueur defausse le collier du 1er avec SES | hf216 Boost : Shaw (1 compteur : ATK 1 + 2 icones = 3) attaque, Black Cat (PV 2) defe | hf216 Boost : TEMOIN, sans le collier (Bomb Scare en boost : 0 icone, ATK 1) Black Ca
      preuve par substitution : rouges 5/7 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attachement a l identite). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf217 : Inhibitor Collar

- [x] Etape 2 : cartes de reference : Inhibitor Collar (x2, hf216-hf217). Attachement TECH ARTIFACT. « Attach to your identity. Treat your identity's printed text box as blank (except for TRAITS). Alter-Ego Action : Spend [physical][physical] resources -> discard this card. Any player may trigger this ability. [star] Boost : If this activation is an attack, this attack gains overkill. » Cartes de reference EXACTES : ld017 / 40092 Inhibitor Collar (meme attache + texte blanc + `PlayerActionToDiscardThis(...).AnyPlayerCanDoThis()`), hf110 (`PlayerActionToDiscardThis(...).SetCost(Cost(...))`), 16134 (`message.would_atk_message.GainOverKill`). ⚠ Icone de ressource : le poing = [physical] = `R` (so002 / hf110 du meme auteur), `Cost("RR")` ; l'action est « Alter-Ego Action » (pas Hero).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf217.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "2"} ; traits ['TECH', 'ARTIFACT']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf217 Inhibitor Collar (2e exemplaire) : s'attache a l'identite, texte blanc
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf218 : Targeted by Hellfire

- [x] Etape 2 : cartes de reference : Targeted by Hellfire (x2, hf218-hf219). Attachement CONDITION. « Attach to your identity if a copy of Targeted by Hellfire is not attached to you. Otherwise, this card gains surge. Forced Response : After you change to hero form, Sebastian Shaw and each HELLFIRE minion engaged with you attacks you. Discard this card. » Cartes de reference : 04119 Neurological Implants (`AttachToFaceWhenPutIntoPlay("YourIdentity", without_another_copy=True, if_cannot_gain_surge=True)`), 90110 (`AfterUnitChangeForm(..., "You", ...)`), hf-fondations `DoAttackYou` (02030 I See You). ⚠ Mots-pieges : « Sebastian Shaw AND each HELLFIRE minion ENGAGED WITH YOU » : Shaw (vilain, meme non engage) + les sbires HELLFIRE engages avec CE joueur ; « to HERO form » : `to_form=Hero` ; la carte se defausse APRES les attaques.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf218.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "3"} ; traits ['CONDITION']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (4) : hf218 Targeted by Hellfire : revelee, s'attache a l'identite (alter-ego) | hf218 Targeted by Hellfire : Reponse forcee, le joueur passe en forme HEROS -> Shaw ( | hf218 Targeted by Hellfire : TEMOIN, un changement de forme vers l'ALTER-EGO ne decle | hf218 Targeted by Hellfire : un 2e exemplaire (hf219) ne s'attache pas a un joueur qu
      preuve par substitution : rouges 4/4
- [x] Etape 7 bis : limite imprimee ? « a copy ... is not attached to you » (une par joueur) : cas `hf218 ... un 2e exemplaire (hf219) ne s'attache pas`
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf219 : Targeted by Hellfire

- [x] Etape 2 : cartes de reference : Targeted by Hellfire (x2, hf218-hf219). Attachement CONDITION. « Attach to your identity if a copy of Targeted by Hellfire is not attached to you. Otherwise, this card gains surge. Forced Response : After you change to hero form, Sebastian Shaw and each HELLFIRE minion engaged with you attacks you. Discard this card. » Cartes de reference : 04119 Neurological Implants (`AttachToFaceWhenPutIntoPlay("YourIdentity", without_another_copy=True, if_cannot_gain_surge=True)`), 90110 (`AfterUnitChangeForm(..., "You", ...)`), hf-fondations `DoAttackYou` (02030 I See You). ⚠ Mots-pieges : « Sebastian Shaw AND each HELLFIRE minion ENGAGED WITH YOU » : Shaw (vilain, meme non engage) + les sbires HELLFIRE engages avec CE joueur ; « to HERO form » : `to_form=Hero` ; la carte se defausse APRES les attaques.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf219.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "3"} ; traits ['CONDITION']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf219 Targeted by Hellfire (2e exemplaire) : s'attache et fonctionne comme hf218
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? voir hf218
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf220 : Mutant Suppression

- [x] Etape 2 : cartes de reference : Mutant Suppression (x2, hf220-hf221). Traitrise TACTIC. « When Revealed : Exhaust your identity and each ally you control. [star] Boost : After this activation, exhaust your identity and place 1 energy counter on Sebastian Shaw. » Cartes de reference : hf321 (WQ : boost `Faces.ExhaustAll([message.GetToPlayer().GetIdentity()], effect)`), hf118 (allies du joueur : `joueur.GetControlCards(CardFinder(card_type=Ally))`), 49042 / hf107 (`message.AfterThisActivation`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf220.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['TACTIC']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf220 Mutant Suppression : When Revealed, l'identite ET chaque allie du joueur sont i | hf220 Mutant Suppression : Boost, apres l'activation de Shaw (stade 2, contre l'alter | hf220 Mutant Suppression : TEMOIN, boost sans effet -> identite prete, aucun compteur
      preuve par substitution : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf221 : Mutant Suppression

- [x] Etape 2 : cartes de reference : Mutant Suppression (x2, hf220-hf221). Traitrise TACTIC. « When Revealed : Exhaust your identity and each ally you control. [star] Boost : After this activation, exhaust your identity and place 1 energy counter on Sebastian Shaw. » Cartes de reference : hf321 (WQ : boost `Faces.ExhaustAll([message.GetToPlayer().GetIdentity()], effect)`), hf118 (allies du joueur : `joueur.GetControlCards(CardFinder(card_type=Ally))`), 49042 / hf107 (`message.AfterThisActivation`).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf221.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['TACTIC']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf221 Mutant Suppression (2e exemplaire) : identite et allie incline
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf222 : Hellfire Indoctrination

- [x] Etape 2 : cartes de reference : Hellfire Indoctrination (x2, hf222-hf223). Traitrise HELLFIRE TACTIC. « When Revealed : Confuse each ally you control. If there is no CAPTIVE ally is confused in this way, this gains surge. [star] Boost : After this activation, place 2 energy counters on Sebastian Shaw. » Cartes de reference : hf118 (WQ : `ThisCardGainSurge`, allies du joueur), 41029 (`Faces.GiveStatus(..., "Confused")`, le RETOUR compte les unites reellement servies, faces.py:180), 49042 (`AfterThisActivation`). ⚠ « confused IN THIS WAY » : un captif DEJA desoriente n'est pas desoriente « de cette facon » ; on compte donc les captifs desorientes par CETTE carte.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf222.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['HELLFIRE', 'TACTIC']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (5) : hf222 Hellfire Indoctrination : un captif ET un allie ordinaire sont desorientes, la  | hf222 Hellfire Indoctrination : AUCUN captif (allie ordinaire seul) -> desoriente, et | hf222 Hellfire Indoctrination : sans aucun allie -> surge | hf222 Hellfire Indoctrination : le captif etait DEJA desoriente -> pas desoriente « d | hf222 Hellfire Indoctrination : Boost, apres l'activation de Shaw -> 2 compteurs d'en
      preuve par substitution : rouges 5/5
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf223 : Hellfire Indoctrination

- [x] Etape 2 : cartes de reference : Hellfire Indoctrination (x2, hf222-hf223). Traitrise HELLFIRE TACTIC. « When Revealed : Confuse each ally you control. If there is no CAPTIVE ally is confused in this way, this gains surge. [star] Boost : After this activation, place 2 energy counters on Sebastian Shaw. » Cartes de reference : hf118 (WQ : `ThisCardGainSurge`, allies du joueur), 41029 (`Faces.GiveStatus(..., "Confused")`, le RETOUR compte les unites reellement servies, faces.py:180), 49042 (`AfterThisActivation`). ⚠ « confused IN THIS WAY » : un captif DEJA desoriente n'est pas desoriente « de cette facon » ; on compte donc les captifs desorientes par CETTE carte.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf223.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['HELLFIRE', 'TACTIC']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf223 Hellfire Indoctrination (2e exemplaire) : captif desoriente, pas de surge
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf224 : Energic Backlash

- [x] Etape 2 : cartes de reference : Energic Backlash (x2, hf224-hf225). Traitrise SKILL. « When Revealed (Alter-Ego) : Place 4 energy counters on Sebastian Shaw. When Revealed (Hero) : Place 2 energy counters on Sebastian Shaw. Sebastian Shaw attacks you. [star] Boost : After this activation, place 3 energy counters on Sebastian Shaw. » Cartes de reference : hf120 (WQ : forme du joueur `IsAlterEgo()` / `DoAttackYou`), 49042 (`AfterThisActivation`). ⚠ L'attaque de Shaw passe par son Forced Interrupt (retire jusqu'a 3 compteurs pour +1 ATK chacun) : les 2 compteurs poses AVANT l'attaque servent donc.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf224.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['SKILL']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf224 Energic Backlash : When Revealed (ALTER-EGO) -> 4 compteurs d'energie sur Shaw | hf224 Energic Backlash : When Revealed (HERO) -> 2 compteurs, puis Shaw attaque : ses | hf224 Energic Backlash : Boost, apres l'activation de Shaw -> 3 compteurs d'energie
      preuve par substitution : rouges 3/3
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf225 : Energic Backlash

- [x] Etape 2 : cartes de reference : Energic Backlash (x2, hf224-hf225). Traitrise SKILL. « When Revealed (Alter-Ego) : Place 4 energy counters on Sebastian Shaw. When Revealed (Hero) : Place 2 energy counters on Sebastian Shaw. Sebastian Shaw attacks you. [star] Boost : After this activation, place 3 energy counters on Sebastian Shaw. » Cartes de reference : hf120 (WQ : forme du joueur `IsAlterEgo()` / `DoAttackYou`), 49042 (`AfterThisActivation`). ⚠ L'attaque de Shaw passe par son Forced Interrupt (retire jusqu'a 3 compteurs pour +1 ATK chacun) : les 2 compteurs poses AVANT l'attaque servent donc.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf225.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['SKILL']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf225 Energic Backlash (2e exemplaire) : alter-ego -> 4 compteurs
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf226 : Mutant Experimentation

- [x] Etape 2 : cartes de reference : Mutant Experimentation (side scheme 3[per_hero], icone Hazard, boost 2). « When Defeated : Each player must choose and discard 1 card from their hand. » Cartes de reference : 04141 Prison Camps (`WhenSchemeBeDefeated`), `player.AskChooseFace` + `Faces.DiscardAll`. ⚠ « Each player » : tous les joueurs, pas seulement le vainqueur ; « must » : pas de refus ; main vide : rien.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf226.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"StartingThreat": "3*", "Boost": "2", "Hazard": "1"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf226 Mutant Experimentation : menace de depart 3 (1 joueur), icone HAZARD 1, boost 2 | hf226 When Defeated : le joueur doit choisir et defausser 1 carte de sa main (main 2  | hf226 When Defeated : A DEUX joueurs chacun defausse 1 carte (la main du joueur 1 : 2
      preuve par substitution : rouges 2/4 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf227 : Rage of Black King

- [x] Etape 2 : cartes de reference : Rage of Black King (side scheme 2, Hinder 1[per_hero] natif, boost 2). « Forced Response : After Sebastian Shaw activates, he gains a tough status card. When Defeated : Each player chooses to either place 2 energy counters on Sebastian Shaw or deal themselves 1 facedown encounter card. » Cartes de reference : activate.py (`AfterEnemyActivationEnd(ForcedResponse, ...)`), 60075 / ap024 (`player.ChooseAbilities(ForChoiceAbility, ForChoiceAbility)`), 29011-like `Faces.GiveStatus(..., "Tough")`.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf227.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"StartingThreat": "2", "Boost": "2", "Hinder": "1*"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (5) : hf227 Rage of Black King : menace 2 + Hinder 1[par joueur] a l'entree en jeu = 3 (1 j | hf227 Forced Response : apres l'activation de Shaw -> Shaw gagne un statut Robuste | hf227 Forced Response : TEMOIN, sans la manigance Shaw n'a pas de statut Robuste | hf227 When Defeated : le joueur choisit de placer 2 compteurs d'energie sur Shaw | hf227 When Defeated : l'autre branche, le joueur se distribue 1 carte face cachee (Sh
      preuve par substitution : rouges 3/5 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf331 : Sebastian Shaw

- [x] Etape 2 : cartes de reference : Sebastian Shaw (sbire ELITE HELLFIRE, module « Sebastian Shaw », Villainous natif). « Forced Response : After Sebastian Shaw takes any amount of damage, place that amount of threat on the main scheme. [star] Boost : Give the villain a facedown boost card. » Cartes de reference : sk151 (`AfterUnitTookDamage(ForcedResponse, ..., "This")`, `message.took_damage`), hf110 (WQ : `Faces.GiveFacedownBoostCards`). ⚠ « any amount of damage » : tout degat (attaque OU non, contrairement a l'Absorb du vilain) ; ce sbire n'entre jamais en jeu dans « Black King » (retire au Setup de 1A) : il sert aux autres scenarios (Torn).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf331.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"HP": "6", "ATK": "2", "SCH": "1", "Boost": "1", "Villainous": "1"} ; traits ['ELITE', 'HELLFIRE']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf331 Sebastian Shaw (sbire) : valeurs imprimees (PV 6, ATK 2, SCH 1), ELITE HELLFIRE | hf331 Boost : Shaw (sbire) en boost de l'attaque de Shaw (vilain) -> le VILAIN recoit | hf331 Boost : TEMOIN, une carte de boost sans effet -> aucune carte de boost donnee a
      preuve par substitution : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf332 : Energy Absorption

- [x] Etape 2 : cartes de reference : Energy Absorption (x2, hf332-hf333). Attachement SUPERPOWER. « Max 1 per character. Attach to Sebastian Shaw. Otherwise, attach to the villain. Forced Interrupt : When the attached character would take any amount of damage, heal that character for that amount instead of dealing damage. If no damage was healed this way, give that character a tough status card. Set aside this card. » Cartes de reference : 90129 Wounded Civilians (`SetBeInstead` sur `WhenUnitWouldTakeDamage`), hf101b (WQ : meme message, `PreventDamage`), 60113a, `Faces.SetAside` (27100a Sinister Six), `HealthUnits` (rend la quantite REELLEMENT soignee). ⚠ « instead of dealing damage » : les degats sont REMPLACES par le soin (la carte reste donc sans effet sur Absorb) ; « If no damage was healed » (personnage deja intact) : statut Robuste ; la carte part ensuite de cote DANS TOUS LES CAS.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf332.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "2", "MaxPerUnit": "1"} ; traits ['SUPERPOWER']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (6) : hf332 Energy Absorption : revelee, s'attache a Sebastian Shaw ; il est blesse (3) : l | hf332 Energy Absorption : Shaw intact -> rien a soigner : statut Robuste, aucun degat | hf332 Energy Absorption : revelee, elle est attachee a Shaw (mode scenario) | hf332 Energy Absorption : dans un AUTRE scenario (vilain White Queen), elle s'attache | hf332 Energy Absorption : dans un AUTRE scenario sans Shaw (White Queen seule) -> ell | hf332 Energy Absorption : Max 1 par personnage, un 2e exemplaire (hf333) ne s'ajoute 
      preuve par substitution : rouges 6/6
- [x] Etape 7 bis : limite imprimee ? « Max 1 par personnage » : cas `hf332 ... Max 1` (2e exemplaire non attache)
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attachement). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf333 : Energy Absorption

- [x] Etape 2 : cartes de reference : Energy Absorption (x2, hf332-hf333). Attachement SUPERPOWER. « Max 1 per character. Attach to Sebastian Shaw. Otherwise, attach to the villain. Forced Interrupt : When the attached character would take any amount of damage, heal that character for that amount instead of dealing damage. If no damage was healed this way, give that character a tough status card. Set aside this card. » Cartes de reference : 90129 Wounded Civilians (`SetBeInstead` sur `WhenUnitWouldTakeDamage`), hf101b (WQ : meme message, `PreventDamage`), 60113a, `Faces.SetAside` (27100a Sinister Six), `HealthUnits` (rend la quantite REELLEMENT soignee). ⚠ « instead of dealing damage » : les degats sont REMPLACES par le soin (la carte reste donc sans effet sur Absorb) ; « If no damage was healed » (personnage deja intact) : statut Robuste ; la carte part ensuite de cote DANS TOUS LES CAS.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf333.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "2", "MaxPerUnit": "1"} ; traits ['SUPERPOWER']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf333 Energy Absorption (2e exemplaire) : meme effet (soin 2 sur 3 degats)
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? voir hf332
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf334 : Energy Counterattack

- [x] Etape 2 : cartes de reference : Energy Counterattack (x2, hf334-hf335). Attachement SUPERPOWER. « Max 1 per character. Attach to Sebastian Shaw. Otherwise, attach to the villain. Forced Interrupt : When a character attacks the attached character, the attached character attacks that character. (Resolve the attached character's attack first). Set aside this card. » Cartes de reference : hf107 (WQ : `WhenUnitBeingAttack(ForcedInterrupt, ..., None, op)`), `CanAttack.BasicAttack(units, effect)` (can_attack.py:1146). ⚠ « When a character attacks » : un PERSONNAGE (heros / allie), pas un sbire ; l'attaque du porteur est resolue AVANT celle qui la declenche (Interruption) ; la carte part de cote ensuite.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf334.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "2", "MaxPerUnit": "1"} ; traits ['SUPERPOWER']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf334 Energy Counterattack : revelee, attachee a Shaw ; le heros l'attaque -> Shaw (2 | hf334 Energy Counterattack : attachee a Shaw -> attache (hf201) | hf334 Energy Counterattack : TEMOIN, un SBIRE (pas un personnage) n'attaque pas Shaw 
      preuve par substitution : rouges 3/3
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf335 : Energy Counterattack

- [x] Etape 2 : cartes de reference : Energy Counterattack (x2, hf334-hf335). Attachement SUPERPOWER. « Max 1 per character. Attach to Sebastian Shaw. Otherwise, attach to the villain. Forced Interrupt : When a character attacks the attached character, the attached character attacks that character. (Resolve the attached character's attack first). Set aside this card. » Cartes de reference : hf107 (WQ : `WhenUnitBeingAttack(ForcedInterrupt, ..., None, op)`), `CanAttack.BasicAttack(units, effect)` (can_attack.py:1146). ⚠ « When a character attacks » : un PERSONNAGE (heros / allie), pas un sbire ; l'attaque du porteur est resolue AVANT celle qui la declenche (Interruption) ; la carte part de cote ensuite.
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf335.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "2", "MaxPerUnit": "1"} ; traits ['SUPERPOWER']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf335 Energy Counterattack (2e exemplaire) : meme effet
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf336 : Ambient Energy Absorption

- [x] Etape 2 : cartes de reference : Ambient Energy Absorption (x2, hf336-hf337). Traitrise SKILL. « When Revealed : Choose a set-aside Sebastian Shaw attachment and reveal it. Give this card to the enemy who attached that attachment as a facedown boost card. Otherwise, this card gains surge. [star] Boost : Give this enemy 1 additional boost card for this activation. » Cartes de reference : 49042 Power and Decadence (`villain.GiveBoostCard(this, effect)`), ap024 (`ChooseAbilities`), 60075 ; hf118 (`ThisCardGainSurge`) ; boost : 02035 Intimidation / 01164 (`message.GiveBoostCardForThisActivation(face, 1, effect)` ; on passe l'ennemi qui active : sans cela le moteur ne sert que le VILAIN). ⚠ « Give this card to the enemy WHO ATTACHED that attachment » = l'ennemi porteur (Shaw, ou le vilain si Shaw n'est pas la) ; sans attachement de cote, la carte gagne surge ; « 1 additional boost card FOR THIS ACTIVATION » : une carte de bo
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf336.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['SKILL']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf336 Ambient Energy Absorption : un attachement Shaw de COTE (Energy Absorption) est | hf336 Ambient Energy Absorption : aucun attachement Shaw de cote -> la carte gagne su | hf336 Ambient Energy Absorption : Boost, Shaw recoit 1 carte de boost de PLUS pour ce
      preuve par substitution : rouges 3/3
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (carte de boost donnee). Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf337 : Ambient Energy Absorption

- [x] Etape 2 : cartes de reference : Ambient Energy Absorption (x2, hf336-hf337). Traitrise SKILL. « When Revealed : Choose a set-aside Sebastian Shaw attachment and reveal it. Give this card to the enemy who attached that attachment as a facedown boost card. Otherwise, this card gains surge. [star] Boost : Give this enemy 1 additional boost card for this activation. » Cartes de reference : 49042 Power and Decadence (`villain.GiveBoostCard(this, effect)`), ap024 (`ChooseAbilities`), 60075 ; hf118 (`ThisCardGainSurge`) ; boost : 02035 Intimidation / 01164 (`message.GiveBoostCardForThisActivation(face, 1, effect)` ; on passe l'ennemi qui active : sans cela le moteur ne sert que le VILAIN). ⚠ « Give this card to the enemy WHO ATTACHED that attachment » = l'ennemi porteur (Shaw, ou le vilain si Shaw n'est pas la) ; sans attachement de cote, la carte gagne surge ; « 1 additional boost card FOR THIS ACTIVATION » : une carte de bo
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf337.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"Boost": "1"} ; traits ['SKILL']. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (1) : hf337 Ambient Energy Absorption (2e exemplaire) : meme effet
      preuve par substitution : rouges 1/1
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

### hf338 : Hellfire Domination

- [x] Etape 2 : cartes de reference : Hellfire Domination (side scheme 3[per_hero], icone AMPLIFY (corrige le 01/11 : avion + croix, pas Acceleration), boost 3). « When Defeated : Shuffle each set-aside Sebastian Shaw encounter card into the encounter deck. » Cartes de reference : 04141 (`WhenSchemeBeDefeated`), `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)` (hf-fondations campaign.py), `Worlds.GetSetAsideAreaCards(effect, CardFinder(...))`. ⚠ « each set-aside Sebastian Shaw encounter CARD » : toute carte du set « Sebastian Shaw » de la zone mise de cote (pas seulement les attachements).
- [x] Etape 5 : texte-contre-code, mots-pieges verifies phrase par phrase (voir le commentaire de tete du script `src/cards/pack/hellfire_hunt_black_king/hf338.py`). Resultat : conforme au scan.
- [x] Etape 6 : nombres texte <-> code : `desc` = {"StartingThreat": "3*", "Boost": "3", "Amplify": "1"} ; traits []. Resultat : identiques au scan (lus a l'ecran).
- [x] Etape 7 : cas test_capacites (3) : hf338 Hellfire Domination : menace de depart 3 (1 joueur), icone AMPLIFY 1, boos | hf338 When Defeated : tous les attachements Shaw mis de cote retournent dans le deck  | hf338 When Defeated : TEMOIN, une carte de COTE d'un autre set (Black King hf207) n'e
      preuve par substitution : rouges 2/3 ⚠ un cas reste vert sans module
- [x] Etape 7 bis : limite imprimee ? NON
- [ ] Etape 8 : autoplay ciblé : voir « Etat net » ; cartes de rencontre tirees au hasard, journal lu en partie.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Cas plateau : `ui-app/src/board/black-king-plateau.test.ts` (5 cas verts, calibre : retirer `bind_object_id` du Black King le fait tomber).

Carte terminee : NON : partie humaine a faire (test dans le navigateur) ; le reste est prouve ci-dessus.

## Sortie brute de la preuve par substitution

```
SUBST hf201 : rouges 3/6 ⚠ un cas reste vert sans module
SUBST hf202 : rouges 2/3 ⚠ un cas reste vert sans module
SUBST hf203 : rouges 1/3 ⚠ un cas reste vert sans module
SUBST hf204a : rouges 3/4 ⚠ un cas reste vert sans module
SUBST hf204b : rouges 2/4 ⚠ un cas reste vert sans module
SUBST hf205a : rouges 2/2
SUBST hf205b : rouges 3/6 ⚠ un cas reste vert sans module
SUBST hf206 : rouges 4/5 ⚠ un cas reste vert sans module
SUBST hf207a : rouges 2/3 ⚠ un cas reste vert sans module
SUBST hf207b : rouges 5/8 ⚠ un cas reste vert sans module
SUBST hf208 : rouges 4/5 ⚠ un cas reste vert sans module
SUBST hf209 : rouges 0/1 ⚠ un cas reste vert sans module

BILAN : 11/12 cartes avec au moins un cas tombe au rouge sans leur module
SUBST hf210 : rouges 1/2 ⚠ un cas reste vert sans module
SUBST hf211 : rouges 1/2 ⚠ un cas reste vert sans module
SUBST hf212 : rouges 1/3 ⚠ un cas reste vert sans module
SUBST hf213 : rouges 1/1
SUBST hf214 : rouges 1/1
SUBST hf215 : rouges 1/1
SUBST hf216 : rouges 5/7 ⚠ un cas reste vert sans module
SUBST hf217 : rouges 1/1
SUBST hf218 : rouges 4/4
SUBST hf219 : rouges 1/1

BILAN : 10/10 cartes avec au moins un cas tombe au rouge sans leur module
SUBST hf220 : rouges 2/3 ⚠ un cas reste vert sans module
SUBST hf221 : rouges 1/1
SUBST hf222 : rouges 5/5
SUBST hf223 : rouges 1/1
SUBST hf224 : rouges 3/3
SUBST hf225 : rouges 1/1
SUBST hf226 : rouges 2/4 ⚠ un cas reste vert sans module
SUBST hf227 : rouges 3/5 ⚠ un cas reste vert sans module

BILAN : 8/8 cartes avec au moins un cas tombe au rouge sans leur module
SUBST hf331 : rouges 2/3 ⚠ un cas reste vert sans module
SUBST hf332 : rouges 6/6
SUBST hf333 : rouges 1/1
SUBST hf334 : rouges 3/3
SUBST hf335 : rouges 1/1
SUBST hf336 : rouges 3/3
SUBST hf337 : rouges 1/1
SUBST hf338 : rouges 2/3 ⚠ un cas reste vert sans module

BILAN : 8/8 cartes avec au moins un cas tombe au rouge sans leur module
SUBST hf209 : rouges 1/2 (RECRUITED rouge ; Toughness natif reste vert)
SUBST hf210 : rouges 2/3 (temoin Mercury reste vert)
SUBST hf211 : rouges 2/3 (temoin sans pioche reste vert)

```

## Finitions du 01/11/2026 (session « finitions Hellfire Hunt »)

- Outil de preuve sur COPIE PRIVEE (jamais sur les sources partagees) : `docs/packs/hellfire-hunt/substituer_prive.py <pack> <port> <sortie.json>` (generalisation de celui de Torn ; `HFF_TAG='[hfc]'` pour les fondations). Mutations ponctuelles : un seul fragment du module retire, le cas doit tomber au rouge.
- **Icones (revue du 01/11/2026)** : `hf338` Hellfire Domination porte l'icone AMPLIFY (avion + croix), pas Acceleration : `desc` et cas corriges. Les 18 cartes a icone du pack hf ont ete comparees planche par planche a une carte du MEME pack de glyphe connu.
- **2B (FAQ p.22, usage pendant le tour d'un autre joueur)** : NON code, blocage documente avec precision dans `QUESTIONS.md` (boucle du tour par joueur dans `EventManager.ProcessOptionalEffect`, barriere `WhenInYourPlayTurn` + `check_initiator` des manigances, UI non verifiable sans deux navigateurs).
- Verts sans module : numeriques natifs (`desc`), `Permanent`/`Stalwart` natifs (hf201, hf206, hf207b), « If this stage is completed, the players lose the game » natif (hf204b, hf205b), temoins. Voir la liste au rejeu prive.
