# Batman (ES) : gabarits PROCESSUS-CARTE

Pack `batman`, prefixe `bm`, set 229, auteur ES (« Sealed 6.12.2022 »). Resultats du 26/10/2026. **Aucune carte n'est terminee : il manque une partie reelle jouee par un humain.**

## Notes de reprise

- Fait : donnees (28 entrees), images (28), scripts (24 modules), deck de depart, textes FR, biographie, 42 cas `[bm]`, test d'affichage, preuve par substitution, autoplay, verifications statiques.
- Moteur modifie (tous marques `# CORRECTIF`) : `src/game/card/factory.py` (liste blanche ls005 : `bm005`), `src/game/puzzle/puzzle.py` (methodes de TEST `SetDeterrenceDeck`, `ShuffleDeterrence`). Rien d'autre.
- Conception : le deck de dissuasion est `additional_deck`, sa defausse `additional_discard_pile` (dessines par le plateau comme « Special deck ») ; `card.bind_discard_pile` renvoie une carte RESOLUE dans cette defausse ; une carte defaussee SANS etre resolue est remelangee dans le deck rencontre a la fin de l'effet (`RangerSiNonResolue`, defausse auxiliaire du livret).

- **Passe du 26/10/2026 (corrections issues des verdicts)** : 56 cas `[bm]` verts (14 de plus : Trillionaire sur soutien + temoin, Contingency Plan DEF + temoin, Split Decision Hazard + 3 cas d'icones de defausse, Two-Face remelange x2, Heads I Win icones + egalite a deux joueurs, Tails You Lose x2). Substitution des modules modifies (bm001b, bm008, bm016, bm017) : rouges attendus, modules restaures a l'identique (diff contre la sauvegarde). Helpers modifies dans `src/cards/pack/batman/__init__.py` : `IconesDesCartesDefaussees` (nouveau), `ReactionDeSplitDecision`, `RemelangerEnAttente` (appelle `ApresMelange`). Deck `batman` : monte une partie (verifier_tous_les_decks, ce deck seul). Autoplay 8 parties Batman (`rhino`, normal, equilibre) : 0 victoire / 8 defaites (6 complot accompli, 2 joueurs elimines), 0 erreur sur les 8 journaux, 0 partie bloquee ; temoin spider_man : 0 / 8, 0 erreur. Les cartes de nemesis (Split Decision, Two-Face, Heads I Win, Tails You Lose) n'ont pas ete tirees dans ces parties : elles ne sont prouvees que par les cas. `verifier_appels_modules batman` et `verifier_prefixes` OK (non calibres sur une erreur volontaire cette fois).

## Questions en attente (une par carte, option A = celle codee)

Voir la ligne « Question » de chaque carte ci-dessous. **26/10/2026** : les questions ont ete tranchees par les regles (RR v1.8 + livret de l'auteur) puis par l'utilisateur ; detail dans `VERDICTS-REGLES-2026-10-26.md` et `docs/rapports/2026-10-26-arbitrages-heros-fanmade.md`. Decision de l'utilisateur : bm020 « Investigate » = ignore (reste d'ancienne version). Restent hors de ce pack : les reskins bm023-025 (copies par titre).

## Gabarits

### bm001a : Batman (heros, Justice League)

- [x] Etape 2 : carte(s) de reference : 01028 Superhuman Strength (reponse a une attaque de l'identite) ; bm001b (deck de dissuasion)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « attacks or thwarts » : DEUX capacites (`AfterUnitAttackEnd`, `AfterUnitThwartEnd`), toutes deux « Hero Response » ; « a maximum of 3 in a round » : compte par joueur, remis a zero au round suivant (`MelangesCeRound`)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : PV 11, ATK 2, THW 2, DEF 2, main 5 (scan) = `cards.json`
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : valeurs imprimees ; reponse apres une attaque (melange d'une carte CHOISIE) ; apres un contre ; plafond de 3 melanges par round (4 attaques, Batman redresse entre deux) = temoin d'epuisement
      Resultat : substitution : rouges 3/4 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir ci-dessus.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (le deck de dissuasion est le « Special deck » deja dessine).
- Question : Le plafond de 3 melanges est-il par JOUEUR (code) ou pour toute la table ?

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm001b : Bruce Wayne (alter ego)

- [x] Etape 2 : carte(s) de reference : 09001b Doctor Strange / ip001b Iron Patriot (deck annexe) ; il001b (`UpdateNextCardPlayCost`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « begins the game with a Deterrence deck » : 15 cartes mises de cote (`BeginGameWithSetAside`), le joueur en CHOISIT 8 au Setup (question « Choose 8 deterrence cards », les 7 autres sont retirees du jeu) ; « next ... card played this round » : une AMELIORATION est reduite de 1, un SOUTIEN (Quincarrier VEHICLE) ne l'est PAS (le calcul de cout du moteur n'atteint pas le filtre pour un soutien) : ecart du moteur NON corrige
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : PV 11, REC 3, main 6 (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : valeurs imprimees ; Setup = 8 cartes dans le deck de dissuasion, defausse vide ; Trillionaire reduit Grapple Gun (cout 3) a 2 ; temoin sans l'Action ; temoin d'epuisement (2e Action refusee, `declencher_tolerant`)
      Resultat : substitution : rouges 3/5 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir ci-dessus.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (le deck de dissuasion est le « Special deck » deja dessine).
- **Correction du 26/10/2026 (verdict regles)** : la reduction filtre par TRAIT, soutiens compris. Mesure : The Batcave (LOCATION, cout 2) se paie avec UNE seule ressource apres l'Action (cas + temoin, substitution : rouge sans module). La note « le moteur ne le fait pas » du script etait perimee, elle ne se reproduit plus (aucun changement de moteur n'a ete necessaire).

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm001c : Batman (heros, Lantern)

- [x] Etape 2 : carte(s) de reference : bm001a (meme script, nom « FEAR ME!!! »)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : face alternative declaree dans `metadata.hero_alts` du deck
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : memes valeurs que bm001a (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : AUCUN : le harnais ne sait pas monter une face `hero_alts` (`Puzzle.ChangeToFace` leve un AssertionError) ; script identique a bm001a (diff verifie)
      Resultat : substitution : AUCUN CAS — gate non tenue.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : A confirmer en partie reelle : la face Lantern se choisit et se joue comme bm001a.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm001d : Bruce Wayne (alter ego, Lantern)

- [x] Etape 2 : carte(s) de reference : bm001b (meme script)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : face alternative `hero_alts`
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : memes valeurs que bm001b (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : AUCUN : meme limite que bm001c ; script identique a bm001b
      Resultat : substitution : AUCUN CAS — gate non tenue.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : A confirmer en partie reelle.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm002 : Robin (Damian Wayne)

- [x] Etape 2 : carte(s) de reference : defeated.py `AfterUnitDefeatedUnit`, thwart.py `AfterUnitThwartAndRemoveLastThreat` ; `ChooseOrder` (paibok)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « or » : deux capacites ; « You may discard one » (0 ou 1) ; « in any order » (`ChooseOrder`) ; une dissuasion defaussee ainsi n'est pas resolue : remelangee dans le deck rencontre
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 3, PV 3, ATK 2*, THW 1*, RES G (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : apres avoir vaincu un ennemi ; apres la derniere menace retiree ; une carte de dissuasion defaussee est remelangee (aucune dans la defausse rencontre)
      Resultat : substitution : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : Le choix de l'ordre des cartes replacees est-il bien au joueur (code) ? Les degats / menaces de Robin viennent-ils aussi des effets d'evenements (non : seulement ses attaques et contres) ?

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm003 : Violent Means

- [x] Etape 2 : carte(s) de reference : 01021 Gamma Slam ; sm004 Rapid Strikes (une cible par coup)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : deux phrases « Deal 2 damage to an enemy » : deux cibles CHOISIES separement
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES R (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : deux fois 2 degats sur le vilain
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : —

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm004 : I Am the Night

- [x] Etape 2 : carte(s) de reference : sm004 Rapid Strikes (`GetCostX`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « X times (to a maximum of 3) » (plafond lu dans le code : `min(X, 3)`) ; « up to 2 » ; « the last threat on that scheme » : `if_this_remove_last_threat` ; le cout X compte les RESSOURCES depensees (YY = 2)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout X, RES Y (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : X = 1 (carte a une ressource) ; X = 2 (YY) ; derniere menace -> 1 degat a un sbire
      Resultat : substitution : rouges 3/3.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : Le plafond de 3 repetitions n'est pas mesure (le harnais ne paie qu'UNE carte avec `surpayer`, et une menace de 7 accomplit le complot) : lu dans le code.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm005 : Intimidate

- [x] Etape 2 : carte(s) de reference : sn004 (interruption sur `WhenBoostCardWouldTurnedFaceUp`), bg007 (`WhenPlayerRevealCard`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « revealed OR flipped as a boost card » : DEUX capacites de jeu (declaration `factory.py`, lecon ls005) ; « cancel » = deux drapeaux (surge, carte de boost supplementaire) lus par la carte de dissuasion ; « may pay 1 resource of any type » (`AskSpendResources`)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 0, RES B (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : la dissuasion revelee ne gagne pas Renfort (surge 0) ; temoin sans Intimidate (surge 1)
      Resultat : substitution : rouges 1/2 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : Le « remelange dans le deck » apres paiement n'est pas mesure (le pilote decline le paiement).

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm006 : The Batcave

- [x] Etape 2 : carte(s) de reference : sk043 (`GiveKeywordToInPlayWhenApplyThis`), im001b (`GainCard`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « look at the top 5 », « Choose one and add it to your hand », « Shuffle the remaining cards into your deck » ; +2 REC
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES Y (scan) ; REC 3 + 2 = 5
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : +2 REC ; Action d'alter ego : une carte en main, la Batcave inclinee
      Resultat : substitution : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/batman-plateau.test.ts`.
- Question : —

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm007 : Oracle

- [x] Etape 2 : carte(s) de reference : hercules 59001b (`Reveal`), `Search.EncounterCard`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « search the encounter deck » (pas la defausse) ; « reveal the chosen card » : elle passe par SON When Revealed (marquee resolue) ; « shuffle the encounter deck » apres
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES B (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : cherche, revele (Smoke Cloud desoriente), la carte va dans la defausse de dissuasion, Oracle inclinee
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : —

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm008 : Contingency Plan

- [x] Etape 2 : carte(s) de reference : 34034 Psychic Kicker (`WhenUnitUseBasicPower` temporaire)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ignoring any crisis icons » (`ignore_crisis`) ; « basic power » = ATQ ou CTR ; « his NEXT use ... this round »
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES B (scan) ; 2 menaces
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : retire 2 menaces, la carte est defaussee
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- **Correction du 26/10/2026 (verdict regles, RR BASIC POWER : 5 pouvoirs de base)** : la DEF est maintenant PROPOSEE (3 options : attaque, contre, defense). Cas : choix DEF, Rhino attaque (2 + 4) -> 2 degats au lieu de 4 (vu ROUGE avant, vert apres) ; temoin sans la carte : 4. Le +2 ATK et le +2 THW restent non mesures (branches existantes, non modifiees).

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm009 : Batsuit

- [x] Etape 2 : carte(s) de reference : 01036 Mark V Armor (`GiveKeywordToAttached("You", health=)`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « You get +3 hit points » (le joueur) ; « Batman gets +1 DEF » (la carte nommee)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES R ; +3 PV, +1 DEF (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : PV max 11 -> 14, DEF 2 -> 3
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/batman-plateau.test.ts`.
- Question : —

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm010 : Grapple Gun

- [x] Etape 2 : carte(s) de reference : sm004 (`UnitIgnoreKeywordIcons`), 01025 (`ChangeToOtherIdentityForm`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ignores the guard keyword AND the patrol keyword » ; Interruption (pas « de heros ») ; « exhaust Grapple Gun -> change your form »
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 3, RES Y (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : Batman frappe Rhino malgre Hydra Mercenary (Guard) ; l'interruption change la forme et incline la carte
      Resultat : substitution : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : —

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm011 : Batarangs

- [x] Etape 2 : carte(s) de reference : resolve.py `AfterCardResolveAbility`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When Revealed effect OR boost ability » : le filtre du moteur ne connait pas « Boost », la condition lit le type de la capacite resolue ; « deal 1 damage to an enemy »
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES R (scan) ; 1 degat
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : apres le When Revealed de Smoke Cloud, 1 degat a Rhino
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : La reponse sur le BOOST n'est pas mesuree (une seule condition, partagee avec Utility Belt).

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm012 : Utility Belt

- [x] Etape 2 : carte(s) de reference : sm/27083 (`Faces.ResolveAbility` WhenRevealed), `CanSurge.GainSurge(-n)`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « 1 additional time » ; « cancel its surge effect » : le surge etant deja pris, on le retire (`GainSurge(-surge)`) ; « exhaust Utility Belt » (cout)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : cout 2, RES G (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : Sudden Strike rejouee : 3 + 3 = 6 degats, la ceinture inclinee, surge de la carte a 0
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : Le mode « boost -> rejouer le When Revealed » n'est pas mesure.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm013 : Ghosts of the Past

- [x] Etape 2 : carte(s) de reference : 01160 Legal Work (meme squelette)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « You may flip » ; « Choose » deux branches ; « Search and remove ALL of the deterrence cards from the encounter deck » (pas de la defausse) ; « Add these cards to your deterrence deck » ; « Shuffle the encounter deck. Discard this card »
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : Boost 2 (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : branche 2 : les cartes du deck rencontre rejoignent le deck de dissuasion (taille 1), plus aucune dans le deck rencontre
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : La branche 1 (incliner Bruce Wayne, retirer la carte) n'a pas de cas : meme squelette que 01160.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm014 : Split Decision (complot annexe nemesis)

- [x] Etape 2 : carte(s) de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When a Deterrence card is revealed » : la fonction `ReactionDeSplitDecision` est appelee au debut du When Revealed de chaque dissuasion ; « odd number of boost icons » = icones CHIFFREES (`CountTotalBoostIcons`)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : menace de depart 4, Boost 2 (scan) ; +2 menaces
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : dessus du deck = 01101 (1 icone) -> defausse, +2 menaces sur le complot principal
      Resultat : substitution : non lancee.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/batman-plateau.test.ts`.
- **Correction du 26/10/2026 (verdict regles)** : l'icone est un DANGER (Hazard), identique a 01107 Breakin' & Takin' : `desc.Hazard = "1"` ajoute dans `cards.json` ; cas `[bm] bm014 ... porte UNE icone Danger (Hazard)` : ROUGE sans la donnee, vert avec (preuve manuelle, la donnee n'est pas un module). Une dissuasion retournee en BOOST n'est pas « revelee » : pas de declenchement (A confirme, RR BOOST). **Livret de l'auteur** : si l'effet lit les icones d'une dissuasion defaussee sans etre resolue, on lit le dessus de la defausse rencontre (telle qu'avant l'effet), a defaut on defausse UNE AUTRE carte : `IconesDesCartesDefaussees` (`batman/__init__.py`). Trois cas (dessus de la defausse a 0 icone, temoin a 1 icone, defausse vide), vus ROUGES avant le correctif, verts apres.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm015 : Two-Face (sbire nemesis)

- [x] Etape 2 : carte(s) de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « After a deterrence card is shuffled into the encounter deck » : le moteur n'a aucun message, c'est `MelangerUneDissuasion` qui le reveille (`ApresMelange`) ; « Max twice per round » ; Steady + Villainous (cles du `desc`)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : PV 4, ATK 0, SCH 0, Boost 2 (scan) ; +1/+1
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : apres un melange : MNG 1, ATQ 1 ; temoin d'epuisement : 3 melanges dans le round -> 2 / 2 seulement
      Resultat : substitution : non lancee.
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : voir ci-dessus.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : cas plateau `ui-app/src/board/batman-plateau.test.ts`.
- **Correction du 26/10/2026 (verdict regles)** : le remelange du livret (dissuasion defaussee sans etre resolue) est un « shuffled into the encounter deck » : `RemelangerEnAttente` appelle maintenant `ApresMelange` une fois par carte remelangee. Cas : un remelange (Heads I Win defausse bm018) +1/+1 ; deux remelanges (bm018 + bm019) +2/+2 ; les deux vus ROUGES sans la boucle (manuel : boucle neutralisee -> rouge, remise -> vert). « Max twice » : par Two-Face et par round, confirme (A). Ghosts of the Past ne mele aucune dissuasion (il les retire du deck) : sans objet.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm016 : Heads I Win

- [x] Etape 2 : carte(s) de reference : nt015 / rescue_rainy 90128 (`DealIndirectDamage`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « The player with the MOST remaining hit points » (egalite : le premier joueur, code) ; « indirect damage equal to the number of boost icons discarded »
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : Boost 2 (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bm018 + 01101 defausses (2 icones) -> 2 degats indirects ; surge puisqu'une dissuasion a ete defaussee (remelangee a la fin de l'effet)
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- **Correction du 26/10/2026 (verdict regles)** : (1) egalite de PV restants : le PREMIER JOUEUR choisit parmi les ex aequo (RR FIRST PLAYER), cas a deux joueurs (Batman 10 PV apres 1 degat, Peter Parker 10 PV, choix de Peter Parker) vu ROUGE avant (degats sur Batman) ; (2) les icones d'une dissuasion defaussee se lisent par `IconesDesCartesDefaussees` (livret) : bm018 + 01101 sans dessus de defausse -> 1 degat indirect (et non 2, ancienne valeur) ; bm018 + 01101 avec 01099 (2 icones) au dessus de la defausse -> 3. Choix d'interpretation : une carte que l'effet a lui-meme defaussee n'est pas relue comme « dessus de la defausse » (on prend la carte de la defausse d'AVANT l'effet) pour eviter de compter deux fois la meme carte.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm017 : Tails You Lose

- [x] Etape 2 : carte(s) de reference : `DiscardRandomHandCards`
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « odd number of boost icons » ; « the FIRST player discards 2 cards AT RANDOM »
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : Boost 2 (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : bm018 (1 icone) + une carte sans icone -> impair -> 2 cartes defaussees (main 5 -> 3)
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- **Correction du 26/10/2026** : meme regle du livret que bm016 (`IconesDesCartesDefaussees`, hors du verdict ecrit mais meme texte « references icons »). Cas : dissuasion + dessus de defausse a 1 icone -> impair, main 5 -> 3 ; temoin sans carte a 1 icone -> pair, main 5.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm018 : Sudden Strike (dissuasion)

- [x] Etape 2 : carte(s) de reference : 01164 Titania's Fury (When Revealed + Boost)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « If Batman is in play » (forme HEROS) ; « an enemy of your choice » ; « gains surge » ; boost : « the activating enemy » (`message.activating_enemy`)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : Boost 1 + [star] (scan) ; 3 degats / 2 degats
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : 3 degats sur Rhino + carte dans la defausse de dissuasion ; alter ego : aucun degat ; en boost : 2 degats a l'ennemi qui s'active
      Resultat : substitution : rouges 2/3 ⚠ un cas reste vert sans module.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (le deck de dissuasion est le « Special deck » deja dessine).
- Question : La carte pose-t-elle son surge meme quand Batman n'est pas en jeu (code : oui, comme imprime) ?

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm019 : Smoke Cloud (dissuasion)

- [x] Etape 2 : carte(s) de reference : 01028 (statut pose par `Faces.GiveStatus`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Confuse an enemy » ; boost : -2 aux degats de l'attaque / a la menace de la manigance de l'activation (`ReduireLActivation`, champ `additional_value` de l'attaque)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : [star] seul (scan) ; -2
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : revelee : ennemi desoriente ; en boost contre une attaque : 0 degat au lieu de 2
      Resultat : substitution : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (le deck de dissuasion est le « Special deck » deja dessine).
- Question : La reduction de MENACE (activation = manigance) n'est pas mesuree.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm020 : Detective Work (dissuasion)

- [x] Etape 2 : carte(s) de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « Choose a player » (solo : le joueur) ; « two cards in their discard pile » ; « bottom OR shuffle » (choix)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : Boost 1 + [star] (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : deux cartes de la defausse placees sous le deck (defausse 3 -> 1)
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (le deck de dissuasion est le « Special deck » deja dessine).
- Question : « Investigate » (boost) n'est defini ni dans le livret ni dans le moteur officiel : aucun effet code. Le fichier du zip s'appelle « UncoveringthePlan » mais la carte imprimee dit « Detective Work » : nom imprime retenu.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm021 : Vigilantism (dissuasion)

- [x] Etape 2 : carte(s) de reference : bm004 (une cible par point de menace)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « divided as you choose » : un point a la fois ; boost : « up to 2 » sur le complot PRINCIPAL
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : Boost 1 + [star] (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : 5 menaces -> 3
      Resultat : substitution : rouges 1/1.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (le deck de dissuasion est le « Special deck » deja dessine).
- Question : Le boost (retirer 2 menaces du complot principal) n'est pas mesure.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm022 : Shadow of the Bat (dissuasion)

- [x] Etape 2 : carte(s) de reference : bg007 (deux options), 01035 (`canbe_ready`)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « choose one » : piocher OU redresser ; boost : « prevent ALL threat and damage » (`additional_value` -99)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : [star] seul (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : revelee : pioche (deck de dissuasion -> defausse) ; en boost : 0 degat au lieu de 2
      Resultat : substitution : rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (le deck de dissuasion est le « Special deck » deja dessine).
- Question : L'option « redresser » n'est pas mesuree.

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm023 : Energy (Basic, reskin)

- [x] Etape 2 : carte(s) de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucune capacite (ressource YY, Max 1)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : YY (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : aucun module
      Resultat : substitution : non lancee.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : Carte a part (code) ou art alternatif de 01088 ?

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `batman` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Batman » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Batman » dans la modale du héros et les trois ressources à l'écran).

### bm024 : Genius (Basic, reskin)

- [x] Etape 2 : carte(s) de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucune capacite (ressource BB, Max 1)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : BB (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : aucun module
      Resultat : substitution : non lancee.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : Carte a part (code) ou art alternatif de 01089 ?

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

### bm025 : Strength (Basic, reskin)

- [x] Etape 2 : carte(s) de reference : —
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : aucune capacite (ressource RR, Max 1)
      Resultat : conforme au texte lu sur le scan (voir « Question »).
- [x] Etape 6 : nombres texte <-> code : RR (scan)
      Resultat : identiques dans `cards.json` et le script.
- [x] Etape 7 : cas test_capacites par capacite, preuve par substitution : aucun module
      Resultat : substitution : non lancee.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay ciblé : voir « Autoplay » plus bas.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON.
- Question : Carte a part (code) ou art alternatif de 01090 ?

Carte terminee : NON (provisoire) : aucune partie reelle jouee par un humain ; question ci-dessus.

## Autoplay, verifications et ce qui reste a verifier en partie reelle

- **Autoplay** (`tools/autoplay.py .game-src-bm2 --deck batman --vilains rhino --difficultes normal --profils equilibre --parties 8`) : 8 parties, 0 victoire, 5,6 rounds en moyenne, **0 incident, 0 exception** (grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback` sur les 8 journaux : 0). Temoin Spider-Man : 8 parties, 0 victoire, 6,9 rounds, 0 exception. Les cartes sont jouees : Sudden Strike, Smoke Cloud, Detective Work, melanges, Oracle, Robin, Batarangs, Utility Belt apparaissent dans les journaux. Le pilote retient « les 8 premieres » dans la question du Setup (bm018 x3, bm019 x3, bm020 x2) : Vigilantism et Shadow of the Bat ne sont donc pas dans ses decks.
- **42 cas `[bm]` verts** (`tools/cas/batman.py`, `CAS_PREFIX=bm_ ... test_capacites.py .game-src-bm 41800 ... "[bm]"`).
- **Substitution** (`tools/substituer_pack.py ... bm0`, pack sauvegarde puis restaure, identique) : voir le resultat de chaque carte ; bm001c / bm001d sans cas (faces `hero_alts`, le harnais ne sait pas les monter) ; les cas qui restent verts sont des cas de DONNEES (valeurs imprimees) ou des temoins d'absence.
- **Statique** : `verifier_prefixes` OK ; `verifier_appels_modules ... batman` OK ; `verifier_cibles` OK ; `verifier_traductions_fr` OK ; tests UI : plateau (4), vocabulaire statuts / evenements, textes FR (19) verts.
- **A verifier en partie reelle** : (1) la question « Choose 8 deterrence cards » au Setup (affichage, annulation) ; (2) le choix de la carte a melanger (vue du deck de dissuasion, defausse de dissuasion visible) ; (3) une dissuasion defaussee sans etre resolue qui REVIENT dans le deck rencontre ; (4) Intimidate en boost et sa fenetre de paiement ; (5) Utility Belt rejouant un When Revealed ; (6) les faces Lantern (bm001c/bm001d) ; (7) le boost de Smoke Cloud contre une MANIGANCE ; (8) la reduction de cout de Trillionaire sur un SOUTIEN (ecart connu) ; (9) Split Decision sur une dissuasion retournee en boost ; (10) la biographie au survol dans l'assistant.
