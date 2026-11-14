# Hellfire Hunt, scénario 4 « Torn » + modules Negasonic Teenage Warhead et Immensity (Dipsome, préfixe `hf`) : gabarits PROCESSUS-CARTE

Worktree `Marvel-LCG-campagnes`, branche `campagnes-fanmade`. Pack `hellfire_hunt_torn` (set 244), module plat `src/cards/pack/hellfire_hunt_torn/` (30 cartes : `hf501`-`hf510`, `hf341`-`hf348`, `hf351`-`hf358`).
Scénarios : `hellfire_torn` (Emma Frost A1/A2) et `hellfire_torn_expert` (B1/B2). Cas : `tools/cas/hellfire_torn.py` (noms `[hf] <card_id> ...`, vérificateur `hft_etat`).
Génération des données : `docs/packs/hellfire-hunt-torn/generer_donnees.py` ; textes français : `textes_fr.py` ; carnet : `campagne.py` ; recettes : `recettes.py` ; preuve par substitution : `substituer_prive.py`
(copie PRIVÉE du pack : `tools/substituer_pack.py` poserait ses stubs dans les sources partagées, que le scénario Cassandra Nova lit via Immensity).
Doutes de règle : `QUESTIONS.md` (8 questions). **Aucune carte n'est « terminée : OUI » : aucune partie jouée par un humain dans le navigateur.**

### hf501a : Emma Frost, face A1 (standard, active)

- [x] Étape 2 : carte(s) de référence : Réponse forcée après activation : `AfterEnemyActivationEnd` (activate.py) + `Worlds.DiscardEncounterTopCard` (hf101a) ; Interruption de défaite : 16080a Collector (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `RemoveThreatFromSchemes` + `card.Flip`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `after ... activates` (chaque activation, une par joueur) ; `each scheme` = principale ET annexes (`EachScheme`) ; `would be defeated ... instead` (la défaite n'a pas lieu, les dégâts restent) ; `if it has the PSIONIC trait` (trait lu sur la carte défaussée).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : PV 7 par joueur (`7*`), ATQ 1 (étoile), MNG 2 (étoile), traits HELLFIRE PSIONIC X-MEN ; +1 menace / 5 menaces retirées.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 4 cas : hf501a Reponse forcee : apres son complot, defausse 1 carte (PSIONIC : Astral Trap) -> +1 menace sur CHAQUE ma ; hf501a Reponse forcee : TEMOIN, la carte defaussee n'est pas PSIONIC (Bomb Scare) -> aucune menace de plus (pr ; hf501a Interruption forcee : serait vaincue (7 degats) -> elle se RETOURNE (hf501b, PV infinis), 5 menaces par ; hf501a Interruption forcee : TEMOIN, 6 degats (< 7 PV) -> aucun retournement, aucune menace retiree
      Résultat : rouges 2/4 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf501a Reponse forcee : TEMOIN, la carte defaussee n'est pas PSIONIC (Bomb Scare) ->  | hf501a Interruption forcee : TEMOIN, 6 degats (< 7 PV) -> aucun retournement, aucune .
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf501b : Emma Frost, face A2 (standard, retournée, PV infinis)

- [x] Étape 2 : carte(s) de référence : `WhenEnemyWouldActivate` + `SetBeInstead` (sl037) ; `AfterPhaseEnd(ForcedResponse, "Villain")` ; `can_health.py OnFlip` (retour des PV en quittant une face infinie).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `instead` (aucune manigance, aucune carte de boost, aucun dégât) ; `After the end of the villain phase` (pas la phase des joueurs : témoin) ; `then set ... hit point dial to her printed hit points` (natif au retournement).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : `HP: INF`, ATQ/MNG « étoile » seuls (0*) ; 2 cartes défaussées.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 6 cas : hf501b PV infinis : 100 degats ne la vainquent pas ; hf501b Interruption forcee : quand elle activerait, defausse 2 cartes du dessus du deck de rencontre A LA PLAC ; hf501b Reponse forcee : apres la fin de la phase du vilain, elle se retourne (hf501a) et ses PV sont remis a l ; hf501b Reponse forcee : le CYCLE complet (serait vaincue -> face infinie -> fin de la phase du vilain) : elle  ; hf501b Reponse forcee : TEMOIN, la fin de la phase des JOUEURS ne la retourne pas ; hf501b INTEGRATION (phase du mechant jouee en entier) : vaincue pendant la phase des joueurs -> face infinie ;
      Résultat : rouges 4/6 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf501b PV infinis : 100 degats ne la vainquent pas | hf501b Reponse forcee : TEMOIN, la fin de la phase des JOUEURS ne la retourne pas.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf502a : Emma Frost, face B1 (expert, active)

- [x] Étape 2 : carte(s) de référence : idem hf501a ; `Worlds.DiscardEncounterCards(2, effect)` rend les faces défaussées.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `for each PSIONIC card discarded in this way` (+1 menace PAR carte PSIONIC, sur chaque manigance) ; défaite -> retournement comme A1.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : PV 8 par joueur, ATQ 2, MNG 2 (étoiles), 2 cartes défaussées.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 5 cas : hf502a mise en place EXPERT : Emma Frost B1 en jeu (PV 8, ATK 2, SCH 2), meme complot, Puppetry et deck Hellfi ; hf502a Reponse forcee : apres son complot, defausse 2 cartes ; DEUX cartes PSIONIC -> +2 menaces sur chaque ma ; hf502a Reponse forcee : UNE seule carte PSIONIC sur les deux -> +1 seulement (principale 4, Puppetry 14) ; hf502a Reponse forcee : TEMOIN, aucune carte PSIONIC -> aucune menace de plus (principale 3, Puppetry 13) ; hf502a Interruption forcee : serait vaincue (8 degats) -> elle se retourne (hf502b), 5 menaces partent de chaq
      Résultat : rouges 3/5 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf502a mise en place EXPERT : Emma Frost B1 en jeu (PV 8, ATK 2, SCH 2), meme complot | hf502a Reponse forcee : TEMOIN, aucune carte PSIONIC -> aucune menace de plus (princi.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf502b : Emma Frost, face B2 (expert, retournée, PV infinis)

- [x] Étape 2 : carte(s) de référence : `WhenEnemyWouldActivate` (+ `message.to_player`) ; `joueur.DealEncounterCards(1)` ; sl037.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `activates AGAINST A PLAYER` (`to_player` non nul) ; `instead` : l'activation n'a pas lieu ; `facedown` : carte distribuée, pas révélée.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : `HP: INF` ; 1 carte face cachée.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 2 cas : hf502b Interruption forcee : quand elle s'active contre un joueur, il recoit une carte de rencontre FACE CACHE ; hf502b Reponse forcee : apres la fin de la phase du vilain, elle se retourne (hf502a) et ses PV sont remis (8 
      Résultat : rouges 2/2 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf503a : The Hellfire Club's Revenge (1A)

- [x] Étape 2 : carte(s) de référence : `WhenCardSetup("This")` (hf104a, deck de rencontre fouillé à la mise en place) ; deck de table (`hellfire_hunt.RecruitedMutants`) ; manigance annexe de la zone mise de côté (27102a) ; `hellfire_hunt.campaign.MiseEnPlace(4)` ; `WriteCampaignLogAtGameOver` (mts/campaign.py) avec `ReleveTorn`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `Shuffle every ELITE, HELLFIRE minion` (les DEUX traits ; White Queen x2 de Perfection compris) ; `set it next to the encounter deck` ; `CONTROLLED side face up` ; `Choose 3 modular sets` : le scénario livre les 3 recommandés (l'écran de préparation choisit, rien ne l'impose) ; carnet : tout allié sorti de la zone mise de côté est noté (livret p. 14).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Deck Hellfire de 5 sbires à 1 joueur et les 3 modules recommandés ; Puppetry 8 + Entrave 5 = 13.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 8 cas : hf503a mise en place : Emma Frost A1 en jeu (PV 7), complot 1B, Nova's Psychic Puppetry (face A) a 13 menaces, ; hf503a Setup : Nova's Psychic Puppetry est mise en jeu face CONTROLLED (8 + Hinder 5 = 13 menaces, Permanent) ; hf503a Setup : les sbires ELITE HELLFIRE de TOUS les modules sont retires du deck de rencontre et forment le H ; hf503a Setup : TEMOIN, les sbires HELLFIRE qui ne sont PAS elite ne vont pas dans le Hellfire deck (Hellfire P ; hf503a Setup de campagne (mode campagne reel) : Xavier's Institute en jeu, 16 allies de cote, une manigance PO ; hf503a Setup de campagne : TEMOIN, HORS campagne Xavier's Institute n'est PAS en jeu ; hf503a CARNET SORTANT a la victoire : les allies Recruited en jeu, dans un deck/defausse de joueur, dans le de ; hf503a CARNET SORTANT a la DEFAITE : aucun allie n'est note (on rejoue sans penalite) ; l'estampille reste cel
      Résultat : rouges 5/8 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf503a Setup : TEMOIN, les sbires HELLFIRE qui ne sont PAS elite ne vont pas dans le  | hf503a Setup de campagne : TEMOIN, HORS campagne Xavier's Institute n'est PAS en jeu | hf503a CARNET SORTANT a la DEFAITE : aucun allie n'est note (on rejoue sans penalite).
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI
      Cas plateau : `ui-app/src/board/torn-hellfire-plateau.test.ts` (vu ROUGE avant `sontDuHellfire` dans `zones.ts` : 3 échecs sur 4, puis vert). OUI : deck et défausse Hellfire (piles de la table)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf503b : Free Cassandra Nova (1B)

- [x] Étape 2 : carte(s) de référence : `WhenPlayerPhaseBegin(ForcedInterrupt)` (ls013) ; `face.Reveal(joueur, effect)` depuis un deck annexe ; scheme_main.py (« If this scheme is completed, the players lose the game »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `At the start of the player phase` (dès le round 1) ; `in player order` (premier joueur d'abord) ; `not engaged with an ELITE, HELLFIRE minion` (un sbire HELLFIRE non élite ne retient pas) ; deck vide -> défausse remélangée SANS pénalité ; `cannot win unless` : Emma ne peut jamais être vaincue (A1 se retourne, A2 PV infinis).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Seuil 15 par joueur, départ 1, escalade 1 par joueur.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 11 cas : hf503b Valeurs imprimees : menace de depart 1, escalade 1 (par joueur), seuil 15 : 14 menaces de plus ne compl ; hf503b « If this scheme is completed, the players lose the game » : le seuil de 15 est atteint -> partie perdu ; hf503b Interruption forcee : au debut de la phase des joueurs, un joueur SANS sbire ELITE HELLFIRE engage reve ; hf503b Interruption forcee : TEMOIN, un joueur DEJA engage avec un sbire ELITE HELLFIRE ne revele rien (le dec ; hf503b Interruption forcee : un sbire HELLFIRE NON elite engage (Hellfire Pawn) ne retient PAS le joueur : il  ; hf503b Hellfire deck VIDE : sa defausse est remelangee dedans SANS penalite (aucune carte de rencontre distrib ; hf503b Hellfire deck ET defausse vides : rien n'est revele, aucune erreur ; hf503b Hellfire deck : un sbire ELITE HELLFIRE VAINCU va dans la defausse HELLFIRE (pas dans celle du deck de  ; hf503b Hellfire deck : un sbire ELITE HELLFIRE simplement DEFAUSSE (pas vaincu) va aussi dans la defausse HELL ; hf503b A DEUX JOUEURS : chaque joueur sans sbire ELITE HELLFIRE engage revele une carte du Hellfire deck, dans ; hf503b A DEUX JOUEURS : un joueur DEJA engage avec un sbire ELITE HELLFIRE ne revele pas ; l'autre revele (une
      Résultat : rouges 7/11 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf503b Valeurs imprimees : menace de depart 1, escalade 1 (par joueur), seuil 15 : 14 | hf503b « If this scheme is completed, the players lose the game » : le seuil de 15 es | hf503b Interruption forcee : TEMOIN, un joueur DEJA engage avec un sbire ELITE HELLFI | hf503b Hellfire deck ET defausse vides : rien n'est revele, aucune erreur.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf504a : Nova's Psychic Puppetry, face A (CONTROLLED)

- [x] Étape 2 : carte(s) de référence : 27102a Light at the End (`WhenLastThreatRemoveFromThisScheme` + `card.Flip`, Permanent + Hinder) ; `ReponseSbireEliteVaincu` (`WhenUnitBeDefeated(ForcedResponse)` + `AskChooseFace`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `each HELLFIRE minion` (PAS seulement ELITE) défaussé (l'ELITE va dans la défausse Hellfire) ; `each player a facedown card` ; `another side scheme / Otherwise ... here` ; `the last threat` (pas une menace restante) ; Permanent natif.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Menace de départ 8, Entrave 5 par joueur (13 à 1 joueur), 5 menaces retirées.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 6 cas : hf504a Interruption forcee : derniere menace retiree -> chaque sbire HELLFIRE en jeu est defausse (l'ELITE va  ; hf504a Interruption forcee : TEMOIN, il reste de la menace (13 - 12 = 1) -> aucune defausse, la carte ne se re ; hf504a Permanent : la carte reste en jeu a 0 menace (elle se retourne, elle n'est pas vaincue ni defaussee) :  ; hf504a Reponse forcee : un sbire ELITE HELLFIRE est vaincu par le joueur -> 5 menaces partent d'UNE AUTRE mani ; hf504a Reponse forcee : AUCUNE autre manigance annexe -> les 5 menaces partent d'ICI (13 -> 8) ; hf504a Reponse forcee : TEMOIN, un sbire HELLFIRE NON elite vaincu (Hellfire Pawn) -> aucune menace retiree
      Résultat : rouges 4/6 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf504a Interruption forcee : TEMOIN, il reste de la menace (13 - 12 = 1) -> aucune de | hf504a Reponse forcee : TEMOIN, un sbire HELLFIRE NON elite vaincu (Hellfire Pawn) ->.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI
      Cas plateau : `ui-app/src/board/torn-hellfire-plateau.test.ts` (vu ROUGE avant `sontDuHellfire` dans `zones.ts` : 3 échecs sur 4, puis vert). OUI : menace posée au retournement (face B 13)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf504b : Nova's Psychic Puppetry, face B (FRAGMENT)

- [x] Étape 2 : carte(s) de référence : 27102b Light at the End (face B : `Worlds.SetGameOver(True)`) ; `GiveKeywordToInPlayWhenApplyThis(..., trait=...)` (cw/56097b).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `the players win the game` (victoire, pas défaite) ; `Each HELLFIRE minion gains the ILLUSION trait` (sbires déjà en jeu ET ceux qui entrent) ; face A vidée ne fait PAS gagner (témoin).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Menace de départ 1 + Entrave 12 par joueur = 13 ; trait FRAGMENT (ajouté à l'énumération `TRAITS`).
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 7 cas : hf504b Interruption forcee : derniere menace retiree -> Emma Frost s'echappe : les joueurs GAGNENT la partie ; hf504b Interruption forcee : TEMOIN, il reste 1 menace sur la face B -> la partie n'est PAS gagnee ; hf504b Interruption forcee : TEMOIN, la face A (CONTROLLED) vidée ne fait PAS gagner ; hf504b « Each HELLFIRE minion gains the ILLUSION trait » : un Hellfire Pawn en jeu devient ILLUSION ; hf504b ILLUSION : TEMOIN, sur la face A (CONTROLLED) le Hellfire Pawn n'est pas ILLUSION ; hf504b ILLUSION : TEMOIN, un sbire NON HELLFIRE (Hydra Mercenary) ne gagne pas le trait ; hf504b Reponse forcee : un sbire ELITE HELLFIRE vaincu -> 5 menaces d'une AUTRE manigance annexe (Psychic Bulw
      Résultat : rouges 3/7 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf504b Interruption forcee : TEMOIN, il reste 1 menace sur la face B -> la partie n'e | hf504b Interruption forcee : TEMOIN, la face A (CONTROLLED) vidée ne fait PAS gagner | hf504b ILLUSION : TEMOIN, sur la face A (CONTROLLED) le Hellfire Pawn n'est pas ILLUS | hf504b ILLUSION : TEMOIN, un sbire NON HELLFIRE (Hydra Mercenary) ne gagne pas le tra.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf505 : Protect Students (obligation)

- [x] Étape 2 : carte(s) de référence : 04166 Anti-Hero Propaganda (`GiveKeywordToInPlayWhenApplyThis(Hero, attack=-1, defense=-1)`) ; im009 (`CostFunc.Custom`) ; `Worlds.GetOnFieldFriendlyCharacters`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `Your hero` (du joueur qui porte l'obligation : `control_by="You"`) ; `reveal 1 card from the Hellfire deck` est une PARTIE DU COÛT (deck et défausse vides : action impayable) ; `each friendly character` (identités et alliés de tous les joueurs).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : ATQ -1, DEF -1 ; 1 dégât soigné ; Boost 2.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 4 cas : hf505 revelee : « Your hero gets -1 ATK, and -1 DEF » (Spider-Man heros : ATQ 2 -> 1, DEF 3 -> 2) ; hf505 : TEMOIN, sans la carte l'attaque et la defense du heros sont celles imprimees ; hf505 Action d'alter-ego : incliner l'identite ET reveler 1 carte du Hellfire deck -> 1 degat soigne sur CHAQU ; hf505 Action d'alter-ego : TEMOIN, deck ET defausse Hellfire VIDES -> le cout (reveler) ne peut pas etre paye 
      Résultat : rouges 3/4 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf505 : TEMOIN, sans la carte l'attaque et la defense du heros sont celles imprimees.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf506 : Uncover The Truth (obligation, Hazard)

- [x] Étape 2 : carte(s) de référence : 04045 / 27131 (`WhenInYourPlayTurn(AlterEgoAction).SetTarget(SchemeSide2)`) ; `HealthUnits`, `RemoveThreatFromSchemes`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `heal 5 damage FROM THE VILLAIN` (le texte soigne le vilain : respecté) ET `remove 5 threat from a side scheme` (les deux parties) ; `Discard this obligation` ; icône Hazard (« carte penchée + croix », comparée à 01180).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : 5 dégâts soignés, 5 menaces retirées, Hazard 1, Boost 2.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 3 cas : hf506 Action d'alter-ego : incliner l'identite -> soigne 5 degats du vilain ET retire 5 menaces d'une maniganc ; hf506 Action d'alter-ego : le soin du vilain est plafonne a ses degats (2 degats -> 0) et les 5 menaces parten ; hf506 Hazard : l'icone (carte penchee + croix) fait compter 1 icone Hazard en jeu une fois la carte revelee
      Résultat : rouges 2/3 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf506 Hazard : l'icone (carte penchee + croix) fait compter 1 icone Hazard en jeu une.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf507 : Psychic Bulwark

- [x] Étape 2 : carte(s) de référence : `GiveKeywordToInPlayWhenApplyThis(Minion, guard=1, patrol=1)` (27142 / hf313) ; `Faces.GiveStatus` ; fiches guard.md, patrol.md.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `Each minion` (tous, pas seulement HELLFIRE, y compris ceux qui entrent après) ; Boost : `each minion a tough status card` (en jeu au moment du boost) ; Victory 1 natif.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Menace de départ 9, Victory 1, Boost 2.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 4 cas : hf507 revelee : menace de depart 9 ; « Each minion gains guard and patrol » : un sbire en jeu (Weapons Runner) ; hf507 Guard/Patrol : un sbire qui ENTRE APRES la carte les a aussi ; hf507 Guard/Patrol : TEMOIN, sans la carte, Weapons Runner n'a ni Guard ni Patrol ; hf507 Boost : « Give each minion a tough status card » : un sbire en jeu (Weapons Runner) devient Tenace
      Résultat : rouges 3/4 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf507 Guard/Patrol : TEMOIN, sans la carte, Weapons Runner n'a ni Guard ni Patrol.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf508 : Psychic Entanglement

- [x] Étape 2 : carte(s) de référence : 27107 Brute Force Barricade (`ThreatCannotBeRemovedFromWhile(SchemeSide2, effect.this != message.trigger)`) ; hf029 (`WhenSchemeBeDefeated`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `OTHER side schemes` (pas elle-même, pas la principale) ; vaut pour les effets de carte (interruption d'Emma) ET la contrarie ; `When Defeated` : une carte face cachée à CHAQUE joueur ; Victory 1 -> pile de victoire.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Menace de départ 8, Victory 1, Boost 2.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 5 cas : hf508 revelee : menace de depart 8 ; « Threat cannot be removed from other side schemes » : la contrarie du he ; hf508 : TEMOIN, sans la carte la meme contrarie retire 1 menace (5 -> 4) ; hf508 : on PEUT contrarier Psychic Entanglement elle-meme (8 -> 7) et le complot principal n'est pas vise ; hf508 : l'interruption de defaite d'Emma Frost retire 5 menaces de la principale et d'ELLE-MEME, pas de Puppet ; hf508 When Defeated : defaite -> chaque joueur recoit une carte face cachee ; Victory 1 : elle va dans la pile
      Résultat : rouges 3/5 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf508 : TEMOIN, sans la carte la meme contrarie retire 1 menace (5 -> 4) | hf508 : on PEUT contrarier Psychic Entanglement elle-meme (8 -> 7) et le complot prin.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf509 : Psionic Paragon

- [x] Étape 2 : carte(s) de référence : `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=Emma Frost), health=10)` (21160 / 01140) ; 39035 Dial M for Mojo (`incite=1` sur `EncounterCard`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `+10 hit point` (plat) ; `Each ILLUSION card gains incite 1` (carte pas encore en jeu : traîtrise, attachement) ; `each player with no engaged minions` ; Paragon est vaincue par l'interruption d'Emma si elle a moins de 5 menaces.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Menace de départ 4 par joueur, +10 PV, incite 1, Boost 2.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 7 cas : hf509 revelee : menace 4 (par joueur) ; « Emma Frost gets +10 hit point » : PV 7 -> 17 ; hf509 : TEMOIN, sans la carte Emma Frost garde ses 7 PV ; hf509 When Revealed : un joueur SANS sbire engage recoit 1 carte face cachee ; hf509 When Revealed : TEMOIN, un joueur ENGAGE avec un sbire n'en recoit pas ; hf509 « Each ILLUSION card gains incite 1 » : reveler une carte ILLUSION (Astral Trap) pose 1 menace sur le co ; hf509 Incite : TEMOIN, sans la carte la meme revelation ne pose aucune menace (principale 1) ; hf509 Incite : TEMOIN, une carte NON ILLUSION (Bomb Scare) ne pose pas de menace
      Résultat : rouges 3/7 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf509 : TEMOIN, sans la carte Emma Frost garde ses 7 PV | hf509 When Revealed : TEMOIN, un joueur ENGAGE avec un sbire n'en recoit pas | hf509 Incite : TEMOIN, sans la carte la meme revelation ne pose aucune menace (princi | hf509 Incite : TEMOIN, une carte NON ILLUSION (Bomb Scare) ne pose pas de menace.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf510 : Hellfire Assault

- [x] Étape 2 : carte(s) de référence : `ThreatCannotBeRemovedFromWhile("This", by_thwarting=False)` (scheme.py) ; hf110 (`WhenCardBecomeBoost("This", RevealThisCard)`) ; hf120 (`villain.DoAttackYou` / `DoSchemes`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `except by thwarting` (la contrarie retire, l'effet d'Emma non) ; `defeated BY A PLAYER` (`has_defeating_player=True`) ; `if it is White Queen` (le SBIRE de Perfection, pas le vilain) ; `schemes` : manigance contre le joueur.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Menace de départ 1 par joueur.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 6 cas : hf510 revelee : menace de depart 1 ; « Threat cannot be removed from here except by thwarting » : l'interrupti ; hf510 : la CONTRARIE du heros retire bien de la menace (6 -> 5) ; hf510 Reponse forcee : un sbire HELLFIRE (Hellfire Pawn) est vaincu PAR UN JOUEUR -> Emma Frost MANIGANCE (SCH ; hf510 Reponse forcee : le sbire vaincu est WHITE QUEEN -> Emma Frost ATTAQUE le joueur (ATQ 1 : 1 degat sur l' ; hf510 Reponse forcee : TEMOIN, un sbire qui n'est PAS HELLFIRE vaincu (Weapons Runner) -> Emma ne fait rien (p ; hf510 Boost : « Reveal this card » : Emma s'active (boost) et la carte est REVELEE (menace de depart 1 sur ell
      Résultat : rouges 3/6 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf510 : la CONTRARIE du heros retire bien de la menace (6 -> 5) | hf510 Reponse forcee : le sbire vaincu est WHITE QUEEN -> Emma Frost ATTAQUE le joueu | hf510 Reponse forcee : TEMOIN, un sbire qui n'est PAS HELLFIRE vaincu (Weapons Runner.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf341 : * Negasonic Teenage Warhead (sbire ELITE HELLFIRE)

- [x] Étape 2 : carte(s) de référence : 40105a (`WhenUnitAttackYou(ForcedInterrupt)` + `message.GetAgainstPlayer()`) ; 40160 (soutiens) ; rc012 (`joueur.GetControlUpgrade`) ; hf321 (boost + `GetToPlayer`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `When ... attacks you` = AVANT l'attaque (Interruption forcée) ; `a support OR upgrade you control, if able` (prêt, au choix du joueur) ; Steady et Toughness natifs.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : PV 4, ATQ 2*, MNG 1, Steady, Toughness, Boost 1 + étoile.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 7 cas : hf341 sbire : PV 4, ATQ 2, MNG 1, Steady, Toughness (carte Tenace a l'entree en jeu), ELITE HELLFIRE ; hf341 Interruption : quand elle ATTAQUE le joueur, celui-ci doit incliner un soutien (Helicarrier) -> incline ; hf341 Interruption : une AMELIORATION (Spider-Tracer sur le heros) peut etre inclinee a la place d'un soutien  ; hf341 Interruption : « if able » : aucun soutien ni amelioration -> rien n'est incline, l'attaque a lieu (le h ; hf341 Interruption : TEMOIN, un soutien DEJA incline n'est pas un candidat (reste incline, aucune erreur) ; hf341 Interruption : TEMOIN, elle ne vise que l'attaque CONTRE le joueur : le vilain qui attaque ne fait rien  ; hf341 Boost : « Exhaust a support or upgrade you control » : Emma s'active (Negasonic en boost) -> Helicarrier
      Résultat : rouges 3/7 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf341 sbire : PV 4, ATQ 2, MNG 1, Steady, Toughness (carte Tenace a l'entree en jeu), | hf341 Interruption : « if able » : aucun soutien ni amelioration -> rien n'est inclin | hf341 Interruption : TEMOIN, un soutien DEJA incline n'est pas un candidat (reste inc | hf341 Interruption : TEMOIN, elle ne vise que l'attaque CONTRE le joueur : le vilain .
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf342 : Perception Manipulation (x2 : hf342, hf343)

- [x] Étape 2 : carte(s) de référence : hf305 Psychic Mirage (`AttachToFaceWhenPutIntoPlay("YourIdentity")`, `CardCannotReady("AttachedCharacter")`) ; hf110 (`PlayerActionToDiscardThis().SetCost(Cost(...))`) ; `identite.ChangeToOtherIdentityForm`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `Spend [mental][mental]` : DEUX ressources mentales (Genius en donne deux) ; `Alter-Ego Action` ; `cannot be readied` ; Boost : `Change your form` (alter-ego -> héros).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Boost 0 + étoile ; coût `Cost("BB")`.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 5 cas : hf342 Perception Manipulation revelee : s'attache a l'identite ; « cannot be readied » : incline puis `Ready`  ; hf342 cannot be readied : TEMOIN, sans la carte `Ready` redresse l'identite ; hf342 Action d'alter-ego : depenser [mental][mental] (un Genius imprime deux ressources mentales) -> la carte  ; hf342 Action d'alter-ego : TEMOIN, des ressources PHYSIQUES (Strength) ne paient pas [mental][mental] -> la ca ; hf342 Boost : « Change your form » : Emma s'active, le joueur passe de l'alter-ego a la forme heros
      Résultat : rouges 4/5 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf342 cannot be readied : TEMOIN, sans la carte `Ready` redresse l'identite.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf343 : Perception Manipulation (exemplaire de hf342)

- [x] Étape 2 : carte(s) de référence : identique à hf342 (même script `from .hf342 import GetAbilities`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir hf342.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : voir hf342.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 1 cas : hf343 Perception Manipulation (2e exemplaire) : meme effet (attachee a l'identite, ne se redresse pas)
      Résultat : rouges 1/1 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf344 : Mind Over Matter (x2 : hf344, hf345)

- [x] Étape 2 : carte(s) de référence : hf321 (`face.Reveal`) ; 40160 / `ThisCardGainSurge` ; `Worlds.GetEncounterDiscardPileCards` (le dessus en tête).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `topmost` = la plus récente ; `attachment` = type Attachement ; `Otherwise ... surge` ; Boost `Exhaust your HERO` (forme héros seulement : un allié défend pour ne pas fausser la mesure).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Boost 1 + étoile.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 5 cas : hf344 Mind Over Matter : revele la PLUS HAUTE ATTACHEMENT de la defausse de rencontre (Astral Trap, au-dessus  ; hf344 Mind Over Matter : sans attachement dans la defausse, la carte gagne surge (la carte suivante, Psychic B ; hf344 Boost : « Exhaust your hero » : Emma attaque, un ALLIE defend (le heros reste pret) puis la carte en boo ; hf344 Boost : TEMOIN, meme attaque, meme defenseur, avec une carte de boost sans effet : le heros reste PRET ; hf344 Boost : TEMOIN, en forme ALTER-EGO rien n'est incline (pas de heros)
      Résultat : rouges 3/5 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf344 Boost : TEMOIN, meme attaque, meme defenseur, avec une carte de boost sans effe | hf344 Boost : TEMOIN, en forme ALTER-EGO rien n'est incline (pas de heros).
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf345 : Mind Over Matter (exemplaire de hf344)

- [x] Étape 2 : carte(s) de référence : identique à hf344 (même script `from .hf344 import GetAbilities`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir hf344.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : voir hf344.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 1 cas : hf345 Mind Over Matter (2e exemplaire) : meme effet (revele l'attachement de la defausse)
      Résultat : rouges 1/1 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf346 : Matter Manipulation (x3 : hf346, hf347, hf348)

- [x] Étape 2 : carte(s) de référence : `Search.PlayerCard(... cost_less_than)` (checker.py : borne INCLUSIVE, d'où `cout - 1`) ; jubilee 47003 (`PutIntoPlay`) ; 40160 (surge).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `same type` (Ally/Support/Upgrade) ; `less than` STRICT (coût 0 : impossible) ; `your deck and discard pile` ; `Otherwise` : surge si rien n'est mis en jeu (défausse faite) : voir QUESTIONS n°5.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Boost 2.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 6 cas : hf346 Matter Manipulation : defausse Helicarrier (soutien, cout 3) et met en jeu un soutien MOINS CHER du deck ; hf346 Matter Manipulation : la recherche couvre aussi la DEFAUSSE du joueur (Aunt May y est) ; hf346 Matter Manipulation : TEMOIN, aucune carte MOINS CHERE du meme type (un autre Helicarrier, cout 3, n'est ; hf346 Matter Manipulation : TEMOIN, un AUTRE TYPE moins cher (une amelioration Spider-Tracer, cout 1) n'est pa ; hf346 Matter Manipulation : sans carte controlee la carte gagne surge ; hf346 Matter Manipulation : une carte de cout 0 (Energy Channel) defaussee -> aucune carte moins chere possibl
      Résultat : rouges 6/6 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf347 : Matter Manipulation (exemplaire de hf346)

- [x] Étape 2 : carte(s) de référence : identique à hf346 (même script `from .hf346 import GetAbilities`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir hf346.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : voir hf346.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 1 cas : hf347 Matter Manipulation (2e exemplaire) : meme effet
      Résultat : rouges 1/1 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf348 : Matter Manipulation (exemplaire de hf346)

- [x] Étape 2 : carte(s) de référence : identique à hf346 (même script `from .hf346 import GetAbilities`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir hf346.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : voir hf346.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 1 cas : hf348 Matter Manipulation (3e exemplaire) : meme effet
      Résultat : rouges 1/1 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf351 : * Cassandra Nova (sbire ELITE HELLFIRE PSIONIC)

- [x] Étape 2 : carte(s) de référence : wd064 Princess Python / pt019 Mr. Hyde (`Search` + `PutIntoPlay` + `AttachTo2` depuis le When Revealed) ; 01121 (boost « put into play engaged with you »).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `Find` (livret p. 4 : toutes les zones : deck de rencontre, défausse, mise de côté) ; le manteau est attaché À ELLE ; Steady natif.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : PV 2, ATQ 3, MNG 3, Steady, Boost 0 + étoile.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 5 cas : hf351 sbire : PV 2, ATQ 3, MNG 3, Steady, ELITE HELLFIRE PSIONIC ; hf351 When Revealed : cherche le manteau (Cassandra's Telepathic Cloak) dans le deck de rencontre et le met en ; hf351 When Revealed : le manteau peut etre dans la DEFAUSSE de rencontre ; hf351 When Revealed : sans manteau nulle part, elle entre quand meme en jeu (rien d'autre ne se passe) ; hf351 Boost : « Put Cassandra Nova into play engaged with you » : Emma s'active (boost) et Cassandra arrive en
      Résultat : rouges 3/5 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf351 sbire : PV 2, ATQ 3, MNG 3, Steady, ELITE HELLFIRE PSIONIC | hf351 When Revealed : sans manteau nulle part, elle entre quand meme en jeu (rien d'a.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf352 : Illusory Duty

- [x] Étape 2 : carte(s) de référence : `Worlds.DiscardEncounterCards(3)` ; `Search.SearchForCard(... include_removed_area, obligation_give_to=joueur)` ; `Faces.RemoveAllFromGame`.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `If no obligation was NOT revealed` (double négatif : QUESTIONS n°1) ; `your obligation` (donnée à ce joueur) ; `removed-from-game area` ; `remove this card from the game`.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : 3 cartes défaussées, Boost 2.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 4 cas : hf352 Illusory Duty : defausse 3 cartes ; une OBLIGATION defaussee (Narrow Minded) est REVELEE ; la carte ne q ; hf352 Illusory Duty : AUCUNE obligation dans les 3 cartes -> cherche l'obligation du JOUEUR (Eviction Notice)  ; hf352 Illusory Duty : l'obligation du joueur peut aussi etre dans la DEFAUSSE de rencontre ; hf352 Illusory Duty : TEMOIN, une obligation parmi les 3 cartes -> on ne cherche PAS la sienne (Eviction Notic
      Résultat : rouges 4/4 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf353 : Mental Paralysis

- [x] Étape 2 : carte(s) de référence : 41029 / hf308 (`Faces.GiveStatus([identite], ...)`) ; Surge natif.
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `You` = l'identité du joueur qui révèle / subit le boost ; Stunned ET Confused (deux statuts) ; Surge natif.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Boost 3 + étoile, Surge.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 2 cas : hf353 Mental Paralysis revelee : le joueur est Sonne ET Desoriente (alter-ego), la carte a Surge ; hf353 Boost : « You are stunned and confused » : Emma s'active (Mental Paralysis en boost), le joueur est Sonn
      Résultat : rouges 2/2 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf354 : Cassandra's Telepathic Cloak

- [x] Étape 2 : carte(s) de référence : 02020 Hysteria (`AttachToFaceWhenPutIntoPlay`) ; sk033 / wt017 (`*UnitCannotTakeDamage`) ; hf101a (`AfterUnitAttackYou`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `cannot take ANY amount of damage` (prévention totale tant que le manteau est en jeu) ; `If she is not in play, find ..., reveal her, attach` ; `After Cassandra attacks YOU` (pas un autre sbire, pas un autre joueur).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Boost 1.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 5 cas : hf354 Cloak revelee, Cassandra DEJA en jeu : s'attache a elle ; « cannot take any amount of damage » : 2 degat ; hf354 Cassandra Nova : TEMOIN, sans le manteau 2 degats la VAINCRAIENT ; hf354 Cloak revelee, Cassandra ABSENTE : la cherche dans le Hellfire deck, la REVELE et s'attache a elle ; hf354 Reponse forcee : apres l'attaque de Cassandra contre le joueur, le manteau est defausse : 1 degat PREVEN ; hf354 Reponse forcee : TEMOIN, l'attaque d'un AUTRE sbire ne defausse pas le manteau
      Résultat : rouges 4/5 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf354 Cassandra Nova : TEMOIN, sans le manteau 2 degats la VAINCRAIENT.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf355 : Jumpstart (x2 : hf355, hf356)

- [x] Étape 2 : carte(s) de référence : 04119 (`AttachToFaceWhenPutIntoPlay(... highest_printed_hp=True, if_cannot_gain_surge=True)`) ; 02020 Hysteria (`message.GiveAdditionalBoostCardForThisActivation`) ; Villainous (Black Bishop hf311).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `highest hit-point` : PV imprimés (QUESTIONS n°4) ; `attacks YOU` ; `1 additional boost card` : un sbire non Villainous n'a pas de boost -> il en reçoit une ; Boost : `Deal yourself 1 facedown card`.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : SCH +2, ATQ étoile (0*), Boost 0 + étoile.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 5 cas : hf355 Jumpstart revelee : s'attache au sbire aux PV IMPRIMES les plus hauts (Hellfire Pawn 3 contre Weapons Ru ; hf355 Jumpstart : sans sbire en jeu, la carte gagne surge (la carte suivante, Psychic Bulwark, est revelee) ; hf355 Interruption forcee : l'attaque du sbire VILLAINOUS (Black Bishop ATQ 1) contre le joueur recoit 1 carte ; hf355 Interruption forcee : TEMOIN, sans Jumpstart la meme attaque ne recoit que la carte de boost du Villaino ; hf355 Boost : « Deal yourself 1 facedown encounter card » : Emma s'active (Jumpstart en boost), le joueur reco
      Résultat : rouges 4/5 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf355 Interruption forcee : TEMOIN, sans Jumpstart la meme attaque ne recoit que la c.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf356 : Jumpstart (exemplaire de hf355)

- [x] Étape 2 : carte(s) de référence : identique à hf355 (même script `from .hf355 import GetAbilities`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir hf355.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : voir hf355.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 1 cas : hf356 Jumpstart (2e exemplaire) : meme effet (s'attache au sbire aux PV les plus hauts)
      Résultat : rouges 1/1 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf357 : Narrow Minded (x2 : hf357, hf358)

- [x] Étape 2 : carte(s) de référence : 11049 Fear of Kang / 40160 (`PlayerActionToDiscardThis(AlterEgoAction).SetCostFunc(CostFunc.Exhaust("YourIdentity"))`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : `Alter-Ego Action` (forme alter-ego seulement) ; icône AMPLIFY (avion + croix), comparée à 16054 ; `HasAmplify` ajouté au type Obligation (sinon `KeyError`).
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : Boost 2, Amplify 1.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 2 cas : hf357 Narrow Minded : Action d'alter-ego, incliner l'identite -> la carte est defaussee ; hf357 Narrow Minded : icone AMPLIFY (`desc.Amplify`) : 1 icone Amplify en jeu une fois revelee
      Résultat : rouges 1/2 sans le module ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : hf357 Narrow Minded : icone AMPLIFY (`desc.Amplify`) : 1 icone Amplify en jeu une foi.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

### hf358 : Narrow Minded (exemplaire de hf357)

- [x] Étape 2 : carte(s) de référence : identique à hf357 (même script `from .hf357 import GetAbilities`).
- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : voir hf357.
      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code).
- [x] Étape 6 : nombres texte ↔ code : voir hf357.
      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan).
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : 1 cas : hf358 Narrow Minded (2e exemplaire) : meme effet (Action d'alter-ego, incliner -> defaussee)
      Résultat : rouges 1/1 sans le module.
- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.
- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)

Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.

## Autoplay (étape 8, commun aux 30 cartes) : 32 parties, grep d'erreurs = 0

`tools/autoplay.py <game_dir> --deck <deck> --vilains <scénario> --difficultes <niveau> --profils equilibre --parties 8` (graines 1 à 8, profil « équilibré »), journaux `/tmp/autoplay_*.log` :

| Deck | Scénario | Niveau | Parties | Victoires | Fin de partie | Rounds (moyenne) | Tracebacks / erreurs |
|---|---|---|---|---|---|---|---|
| `sunspot_hellfire` | `hellfire_torn` | standard | 8 | 0 | 6 complot principal complété, 2 joueur éliminé | 4,0 | 0 / 0 |
| `sunspot_hellfire` | `hellfire_torn` | expert | 8 | 0 | 7 complot, 1 éliminé | 3,5 | 0 / 0 |
| `rachel_summers` (Marvel Girl) | `hellfire_torn` | standard | 8 | 0 | 5 complot, 3 éliminés | 3,6 | 0 / 0 |
| `sunspot_hellfire` (TÉMOIN) | `rhino` | standard | 8 | 0 | 6 complot, 2 éliminés | 3,4 | 0 / 0 |

`grep -c "Traceback"` et `grep -c "NameError|AttributeError|TypeError|KeyError|AssertionError"` sur les 32 journaux : 0 partout. Le pilote ne gagne aucune partie, ni contre Torn ni contre le TÉMOIN (decks de départ de 15 cartes, pilote
heuristique) : le taux de blocage n'est donc pas discriminant, les durées (3,4 à 4,0 rounds) sont comparables. **Journal lu** : mise en place (« AdditionalDeck<5> va être mélangé » = le Hellfire deck), un sbire ÉLITE HELLFIRE révélé à
chaque début de phase des joueurs, Emma qui complote (« Free Cassandra Nova reçoit 5 pion(s) » = MNG 2 + icônes de boost), Réponse forcée d'Emma (« +1 menace » sur la principale et Puppetry), `hf341` / `hf301` « défaussée vers AdditionalDiscardPile<1> »
(défausse Hellfire) dans les parties 2, 3 et 4. **Jamais lu en partie** : la défaite d'Emma (le pilote ne l'atteint pas), le retournement de Puppetry et la victoire : ils ne sont prouvés que par les cas (dont `hf501b INTEGRATION`, phase du méchant entière)
et les épreuves de campagne.

## Portes (gates) lancées sur le pack

- `python -m compileall -q src/cards/pack/hellfire_hunt_torn src/game/puzzle src/game/card/face/card_type/obligation.py` : OK.
- `tools/verifier_appels_modules.py <game_dir> <port> hellfire_hunt_torn` : « OK : tous les appels de hellfire_hunt_torn existent » (gate étalonnée : voir plus bas).
- `tools/test_cards.py` : 8103 ok, 0 erreur (930 cartes sans `GetAbilities`, hors périmètre).
- `tools/audit_cartes.py` : 0 type d'argument, 0 construction impossible, 0 erreur de module ; **2 `marqueur_sans_capacite` (hf504a, hf504b : « Response »)** : faux positif, la Réponse forcée « After an ELITE, HELLFIRE minion is defeated » est une `DelayAbility`
  (`WhenUnitBeDefeated` sur une carte autre que `"This"`, `SetSecondType(ForcedResponse)`) que l'audit ne reconnaît pas ; elle est prouvée par les cas `[hf] hf504a Reponse forcee ...` et `[hf] hf504b Reponse forcee ...`.
- `tools/verifier_prefixes.py` : OK. `tools/verifier_campagnes.py` : OK. `tools/verifier_scenes_campagne.py` : OK. `tools/verifier_pages_campagnes.py` : OK.
- `ui-app` : `npx tsc --noEmit` OK ; vitest `textes-fr-fanmade`, `traduction-public`, `vocabulaire-statuts`, `vocabulaire-moteur`, `dico-en`, `torn-hellfire-plateau` verts.

## Finitions du 01/11/2026 (session « finitions Hellfire Hunt »)

- Outil de preuve sur COPIE PRIVEE (jamais sur les sources partagees) : `docs/packs/hellfire-hunt/substituer_prive.py <pack> <port> <sortie.json>` (generalisation de celui de Torn ; `HFF_TAG='[hfc]'` pour les fondations). Mutations ponctuelles : un seul fragment du module retire, le cas doit tomber au rouge.
- **hf510 Hellfire Assault, branche White Queen** : le cas « Emma ATTAQUE le joueur » n'assertait que la menace de la principale (vraie aussi sans le module) : ajout de `degats_identite: 1` ; mutation (`emma.DoAttackYou` remplace par `pass`) -> ROUGE. Avant : vert module vide, donc non prouve.
