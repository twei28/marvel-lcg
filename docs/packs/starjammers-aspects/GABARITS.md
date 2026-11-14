# Starjammers Aspects (Phenexian et Mysteltainn, préfixe `sy`, pack `starjammers_aspects`, set 233) : gabarits PROCESSUS-CARTE

50 cartes (sy001-sy050 = numéro imprimé 77-126 moins 76) + 1 gabarit technique `sy_thorn_ally` (allié face cachée de Kalyx). Transcription : `TRANSCRIPTIONS.md`.
Données : `tools/importer_cartes_starjammers_aspects.py` (cards.json) ; images : `tools/importer_images_starjammers_aspects.py` ; scripts : `src/cards/pack/starjammers_aspects/` ;
cas : `tools/cas/starjammers_aspects.py` (filtre `[sy]`) ; plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` ; FR : `ui-app/src/board/textes-fr-fanmade.ts` (bloc starjammers_aspects).
Questions en attente : `QUESTIONS.md`.

**Ressources** : icônes lues à l'écran ET contre le même pack (cr017-cr019 : éclair jaune = énergie `Y`, molécule bleue = mental `B`, poing rouge = physique `R`, étoile verte = wild `G`) + contrôle
automatique de la couleur du coin de chaque scan (50/50 conformes).
**Cartes Linked** : sy018 Blade of the Phoenix (Korvus) et sy043 Thorn Crew (Kalyx) sont fabriquées mises de côté par `desc.Linked` (fiche linked.md).

**Aucune carte n'est « terminée : OUI »** : aucune partie réelle jouée par un humain, deux lectures du texte en attente (QUESTIONS.md), et le deck-builder des Starjammers reste à vérifier en partie.
**Autoplay (étape 8)** : FAIT le 26/10/2026 : 8 parties contre Rhino (normal, profil équilibré, graines 1 à 8) avec un deck de TEST (identité Corsair + les 48 cartes sy hors Linked en `player_deck`, jamais livré) et 8 parties témoin avec le deck `corsair` :
sy : 0 victoire / 8 (5 manigance accomplie, 3 héros éliminé), 7,1 rounds en moyenne, 0 incident ; témoin corsair : 1 victoire / 8, 4,5 rounds, 0 incident. Grep exhaustif NameError / AttributeError / TypeError / KeyError / AssertionError : 0 sur les 16 journaux. Le journal montre
Kalyx + Thorn Crew (allié THORN face cachée), Standing Still, Reckless *, Binary, Korvus, etc. joués. Seuls messages : des « paiement abandonné » quand le pilote paie un `Requirement ([energy][mental][physical])` avec trop peu de couleurs (limite connue du pilote, `vv002`),
jamais sur le témoin. Le 0 % ne mesure pas les cartes (deck aléatoire hors règle d'aspect).


### sy001 : * Ch'od — Ally Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 08011 Agent Coulson (`AfterCardEnterPlay(Response, "This")` + `Search.PlayerCard(include_player_deck, include_discard_pile, trait=...)` + `GainCard`) ; `traits=[...]` d'un CardFinder est un OU (RECETTES §4, cr006). « a VEHICLE **or** TECH card » : tout type de carte (allie, soutien, amelioration, evenement) portant l'un des deux traits.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy001.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 4, HP 5, ATK 3**, THW 2**, RES R, Class Basic} ; traits ['STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : entree en jeu -> cherche un VEHICLE dans le deck (The Starjammer) et l'ajoute a la main | cherche un TECH dans la DEFAUSSE (Energy Cannon sy023) et l'ajoute a la main | CONTRE-CAS, ni VEHICLE ni TECH dans le deck -> la main reste vide
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/3 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy001` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy002 : * Corsair (Christopher Summers) — Ally Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 53018 Spectrum (« After you play X from your hand » = `AfterPlayerPlayedCard(Response, "You", "This", op)` + `.SetTarget("UsedToPayForThis")` + `this.TuckCardUnderHere(effect.targets, effect)`) ; `AfterUnitAttackOrThwart` (do_attack.py:1156) ; cr001a (cartes glissees sous une carte : `GetPlacedCardArea`).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy002.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ TEXTE CONTRADICTOIRE (question en attente) : « Interrupt » + « After you play » : une Interruption part AVANT. Code en REPONSE (le
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 4, HP 3, ATK 2*, THW 2*, RES Y, Class Basic} ; traits ['STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : joue depuis la main -> les 2 cartes utilisees pour le payer sont glissees sous lui | apres son attaque, ajoute a la main une carte glissee sous lui
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy002` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy003 : * Hepzibah — Ally Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 16019 Rocket Raccoon (`WhenUnitWouldAttackUnit(Interrupt, "This", Enemy-type, op)` + `GainForThisActive(effect, message, attack=N)` + `message.GainOverKill(effect)`) ; 27043 / rl006 (`CostFunc.Exhaust(trait="WEAPON", from_where=["YouControlCards"])`). « exhaust a WEAPON you control » est DEVANT la fleche : un COUT (Hepzibah ne peut pas se payer elle-meme : elle n'a pas le trait). « attacks an ENEMY » : villain ou sbire (`Enemy`) ; l'Interruption est facultative.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy003.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 1*, THW 1*, RES Y, Class Basic} ; traits ['STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 4 cas `test_capacites` (nom = card_id) : attaque avec un WEAPON (Pirate's Rapier incline) -> +2 ATQ : 1 + 1 (Rapier) + 2 = 4 degats | CONTRE-CAS, sans WEAPON l'Interruption n'est pas offerte (ATQ 1 : 1 degat) | CONTRE-CAS, le WEAPON deja incline ne peut pas payer (2 degats : 1 + 1 du Rapier) | l'attaque gagne overkill : 4 degats sur un sbire a 1 PV, l'exces (3) passe au vilain
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/4 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy003` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy004 : * Sikorsky — Ally Basic

- [x] Étape 2 : cartes de référence : Carte de reference : 45048 Triage (`AfterCardEnterPlay(Response, "This")` + `HealthUnits(targets, N)` + `canbe_heal=True`). Difference : « a CHARACTER » sans trait ni « friendly » : tout personnage soignable (allie, identite, mais aussi un ennemi).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy004.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, HP 2, ATK 1*, THW 1*, RES B, Class Basic} ; traits ['AERIAL', 'PSIONIC', 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : entree en jeu -> soigne 1 a Spider-Man (3 -> 2) ; PV 2, STARJAMMER | « a character » : soigne aussi un ENNEMI (Rhino 3 -> 2)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy004` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy005 : * Waldo — Ally Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 14001a Quicksilver (`AfterUnitUseBasicPower(Response, "This", op, powers=[...])`) ; cr006 Ace Pilot (ready « a VEHICLE you control » : recherche des cartes en jeu portant le trait, controlees par le joueur, choix du joueur). L'etoile d'une Response est une convention d'IMPRESSION (RECETTES §1), pas un `NonKeywordStar`. « a basic power » : les trois. « a VEHICLE you control » : allie, soutien ou amelioration (Jet Bike attache) ; Waldo lui-meme n'est pas un VEHICLE.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy005.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 1*, THW 2*, RES B, Class Basic} ; traits ['ANDROID', 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : apres son attaque de base, redresse un VEHICLE que l'on controle (The Starjammer) | apres son CONTRE de base, redresse aussi le VEHICLE | CONTRE-CAS, un allie incline SANS le trait VEHICLE (Mockingbird) reste incline
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/3 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy005` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy006 : * Raza Longknife — Ally Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 12011 Ant-Man (`ThisGainKeyword(fn, health=1, change_on_event=...)` ; la valeur se relit a chaque changement) ; rl001a (`change_on_event=OnEvent.AttachedMove(Upgrade)`). `GetAttachedUpgrades()` : les ameliorations ATTACHEES a la carte (pas celles posees pres de l'identite).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy006.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 2*, THW 1*, RES R, Class Basic} ; traits ['CYBORG', 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : +1 PV avec Pirate's Rapier attache (3 -> 4), STARJAMMER et CYBORG | PV imprimes 3 sans amelioration | CONTRE-CAS, une amelioration attachee a UN AUTRE allie ne compte pas
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/3 ⚠ un cas reste vert sans module (cas rejoués en vraie pose le 26/10/2026). Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy006` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy007 : Life-Bonded Crewmates — Event Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : hc020 Green Hell (`desc.TeamUp` + `.SetPlay().SetTarget("TeamUp")` obligatoire, fiche teamup.md) ; 12020 Swarm Tactics ; 45048 Triage (`HealthUnits`) ; 08011 / bp51014 (`Search.PlayerCard` + `GainCard`). « Action » : PAS « Hero Action » : jouable en forme heros comme en alter ego. « Heal 2 damage from Corsair AND Hepzibah » : 2 chacun. « Search your discard » : la DEFAUSSE seulement (pas le deck) ; « an event » : tout evenement, y compris celui-ci s'il y est deja.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy007.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES R, MaxPerDeck 1, TeamUp Corsair;Hepzibah, Class Basic} ; traits [] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Corsair + Hepzibah : soigne 2 a chacun et ramene un evenement de la defausse | CONTRE-CAS, sans Hepzibah en jeu le Team-Up n'est pas jouable
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy007` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy008 : Steadfast Companions — Event Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : hc020 Green Hell / 12020 (`desc.TeamUp` + `SetTarget("TeamUp")`) ; `Faces.GiveStatus(cibles, "Tough", effect)` ; 08011 (`Search.PlayerCard`). « each a tough status card » : une carte Tenace PAR personnage ; un personnage deja Tenace n'en recoit pas une seconde (regle des statuts). « Search your DECK » : le deck seulement, pas la defausse.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy008.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES B, MaxPerDeck 1, TeamUp Ch'od;Raza Longknife, Class Basic} ; traits [] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Ch'od + Raza Longknife : une carte Tenace chacun et une amelioration cherchee au deck | CONTRE-CAS, sans Raza Longknife en jeu le Team-Up n'est pas jouable
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy008` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy009 : * Skillful Execution — PlayerSideScheme Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 59028 Evaluate Threat / ul040 Weasel In (`CanPlayThisSchemeCard().SetPlay()` + `WhenSchemeBeDefeated(WhenDefeated, "This", op)` + `Players.ForEachPlayer`) ; 36018 (`ReduceCostToPlayFaceWhen(CardFinder(...), N, "You")`) ; `RegisterTemp(.., unregister_after_exec=False, until_phase_end=True)` pour la duree.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy009.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « each player MAY search » (facultatif) ; « the cost of EACH SKILL played this phase » : TOUTES les cartes SKILL jouees pendant la phase,
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 0, RES Y, StartingThreat 2*, Victory 0, Class Basic} ; traits [] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : menace de depart 2 (2 par joueur), Victory 0 | vaincue -> cherche une carte SKILL (Inconspicuous 04038) ; son cout baisse de 1 pour la ph | TEMOIN de cout, sans elle Inconspicuous (cout 1) ne se joue pas a main vide
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/3 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy009` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy010 : * Center Section Garden — Support Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 45015 Sidekick (`AfterUnitMakeRecovery(.., "You", op, is_basic_recovery=True)` + `HealthUnits`) ; wt010 (`SetTarget(check_fn=.., Identity|Ally)` pour « votre identite ou un allie ») ; recette `AlterEgoResponse` (RECETTES §4bis). « your identity OR a STARJAMMER character » : l'identite du joueur (quel que soit son trait) ET tout personnage ami portant le trait.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy010.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES B, Class Basic} ; traits ['LOCATION', 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : apres une recuperation de base (alter ego), soigne 2 a l'identite et s'incline | soigne un personnage STARJAMMER (Sikorsky 1 -> 0) au lieu de l'identite | CONTRE-CAS, en forme HEROS la Response n'existe pas (Alter-Ego Response)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/3 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy010` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy011 : * Standing Still — Support Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : as022 Spider-Verse (`CanGenerateResources(Resource, Resources(..), ..).SetCostFunc(Exhaust("This")) .AnyPlayerCanDoThis()` ; « Action » imprimee, `AbilityType.Resource` ecrit : ecart technique du GUIDE §9) ; la fabrique a deja `for_player_whose_identity_has_trait`, mais pour UN trait : ici DEUX (« OUTLAW or STARJAMMER »), d'ou une condition ecrite. « for a player whose identity has the trait » : le joueur qui PAIE (`message.GetToPlayer()`), pas forcement le proprietaire : `AnyPlayerCanDoThis()` + la condition de trait. Sans trait, la ressource n'est pas offerte meme a son proprietaire.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy011.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ Une seule `CanGenerateResources` par carte. « a [wild] resource » : `Resources("G")`.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, RES B, Class Basic} ; traits ['LOCATION', 'PLANET'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Corsair (STARJAMMER) paie Sikorsky (cout 2) avec Standing Still + 1 carte physique | CONTRE-CAS, Spider-Man (ni OUTLAW ni STARJAMMER) ne peut pas s'en servir
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy011` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy012 : * The Starjammer — Support Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 33020 Utopia (`GiveKeywordToInPlayWhenApplyThis("You", if_each_of_your_allies_has_trait=.., ally_limit=1)`) ; 20010 Venom's Pistol / tg009 Frogjolnir (`WhenUnitUseBasicPower(HeroInterrupt, finder, op)` + `Exhaust("This")` + `message.GainValue(+1, effect)`, qui route vers ATK / THW / DEF). « If EACH of your allies » : sans allie, la condition est vraie (tous les allies, aucun) ; `if_each_of_your_allies_has_trait` recalcule a chaque changement de la zone des allies. « a STARJAMMER character » : identite OU allie portant le trait (Honorary Starjammer et Captain of the Starjammer le donnent).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy012.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES Y, Class Basic} ; traits ['STARJAMMER', 'VEHICLE'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 5 cas `test_capacites` (nom = card_id) : tous les allies STARJAMMER -> limite d'allies +1 (4 allies restent en jeu) | CONTRE-CAS, un allie SANS le trait (Mockingbird) -> pas de bonus, un allie part | Hero Interrupt : Corsair (STARJAMMER) attaque, +1 ATQ (1 -> 2 degats) et s'incline | un allie STARJAMMER (Sikorsky) attaque aussi avec +1 ATQ | CONTRE-CAS, Spider-Man (sans le trait) attaque sans bonus et le soutien reste pret
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 4/5 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy012` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy013 : Honorary Starjammer — Upgrade Basic

- [x] Étape 2 : cartes de référence : Carte de reference : sk064 Fantastic Four Member (62037 Black Belt) : le MEME texte mot pour mot a un trait pres (`CanPlayThisUpgradeCard(Friend, conditions=[identite a le trait])` + `*GiveKeywordToAttached("Character", health=1, trait=..)` ; « Max 1 per character » = `desc.MaxPerUnit "1"`). « Play only if YOUR IDENTITY has the trait » : l'identite du joueur, pas un personnage ami.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy013.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 0, RES Y, MaxPerUnit 1, Class Basic} ; traits ['TITLE'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : Corsair l'attache a Mockingbird -> +1 PV et le trait STARJAMMER | CONTRE-CAS, Spider-Man (identite sans le trait) ne peut pas la jouer | « Max 1 per character » : la 2e copie ne se pose pas sur le meme personnage
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 3/3. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; cas « Max 1 per character » mesuré (sy013).
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy013` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy014 : Pirate's Rapier — Upgrade Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(Ally)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ; `UnitAttackGainKeyword(attacker, piercing=True, conditions=[..])` (do_attack.py:828) pour « its attacks gain piercing ».
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy014.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « its attacks » : les attaques de l'allie PORTEUR (pas de toutes les allies) : condition `message.attacker is porteur`.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES R, MaxPerUnit 1, Class Basic} ; traits ['WEAPON'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 4 cas `test_capacites` (nom = card_id) : +1 ATQ au porteur (Sikorsky 1 -> 2 degats) et son attaque perce la Tenacite | CONTRE-CAS, un allie SANS Rapier (Sikorsky nu) ne perce pas : Tenace consomme, 0 degat | CONTRE-CAS, l'attaque d'un AUTRE allie (Mockingbird) ne perce pas | seule une STARJAMMER la recoit (Mockingbird n'est pas une cible a l'attache)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/4 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy014` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy015 : Stolen Goods — Upgrade Basic

- [x] Étape 2 : cartes de référence : Cartes de reference : ze011 Mount Olympus / hc001a Empowered (`CanGenerateResources(.., conditions=[..]).SetCostFunc(..)`) ; `CostFunc.Discard("This")` pour « Discard this card → ». « only if YOU have the OUTLAW trait » : l'identite du joueur ; la condition doit etre dans `conditions` (sinon la ressource est OFFERTE au paiement meme quand elle est interdite, RECETTES §4). Aucune cible d'attache imprimee : l'amelioration entre en jeu pres de l'identite (comme 01034-like) : `CanPlayThisUpgradeCard()`. « Max 2 per deck » = `desc.MaxPerDeck "2"`, lu par le moteur et par le deck-builder.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy015.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 0, RES G, MaxPerDeck 2, Class Basic} ; traits ['ITEM'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Christopher Summers (OUTLAW, alter ego) paie Sikorsky avec [wild][wild] et la defausse | CONTRE-CAS, Spider-Man (pas OUTLAW) ne peut pas la depenser
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy015` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy016 : * Binary (Carol Danvers) — Ally Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : dt002 Moon Knight (`DiscardDeckTopCards`... + `FacesCounter.GetPrintedResources(faces)` : `res.r / res.y` sont les icones IMPRIMEES, un wild (`res.g`) ne compte pas comme physique ou energie ; un `if` par ligne, car une carte peut avoir plusieurs icones) ; 01083 Mockingbird (stun) ; RECETTES §2. « If you discard a printed [physical] resource » : AU MOINS UNE des 4 cartes (une seule fois, pas une fois par carte). Les deux conditions sont independantes : 3 degats ET sonne si les deux icones sont defaussees.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy016.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 5, HP 4, ATK 3*, THW 2*, RES Y, Class Aggression} ; traits ['AERIAL', 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 4 cas `test_capacites` (nom = card_id) : 4 cartes defaussees dont une [physical] ET une [energy] -> 3 degats et Sonne | CONTRE-CAS, uniquement du [mental] defausse -> ni degats ni Sonne | uniquement du [physical] -> 3 degats, PAS de Sonne | uniquement de l'[energy] defausse -> Sonne, PAS de degats
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 3/4 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy016` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy017 : * Korvus Rook'shir — Ally Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : tk101 / ul040 (carte `Linked` : `desc.Linked` sur sy018 la fait fabriquer MISE DE COTE des que Korvus est cree, fiche linked.md ; on la lit par `Worlds.GetSetAsideAreaCards`) ; nt016 (`this.AttachTo2(cible, effect)`) ; valk/valkyrie (« find X and attach » : recherche dans le set-aside, puis en jeu). « find » : la lame vit dans la zone mise de cote ; aucune lame disponible (deja attachee ou defaussee) : rien ne se passe.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy017.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 1*, THW 1*, RES R, Class Aggression} ; traits ['PSIONIC', "SHI'AR", 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : entree en jeu -> trouve Blade of the Phoenix (mise de cote, Linked) et l'attache a lui
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy017` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy018 : * Blade of the Phoenix — Upgrade Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(Ally)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ; bc002 (`attack_consequential_damage` de `GiveKeywordToAttached`, RECETTES §5 : ajouter un degat consequent passe par la VALEUR, jamais par un temp sur `WhenAllyWouldTakeConsequentialDamage`) ; fiche linked.md (« Linked » = mise de cote par la creation de Korvus). « If the attached ally doesn't have PSIONIC » : le +1 depend du trait du porteur, relu quand ses traits changent.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy018.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ Un allie a 0 degat consequent imprime n'en subit pas non plus : le +1 s'ajoute a la valeur imprimee (Korvus 1* -> 2).
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES YB, Class Aggression, Linked Korvus Rook'shir} ; traits ['ARTIFACT', 'WEAPON'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : +2 ATQ ; sans PSIONIC (Mockingbird) il subit 1 degat consequent EN PLUS (3 degats, 2 subis | CONTRE-CAS, PSIONIC (Sikorsky) : +2 ATQ mais seulement le degat consequent imprime (1)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy018` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy019 : * Marvel Girl (Rachel Summers) — Ally Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : 16019 Rocket Raccoon (`WhenUnitWouldAttack...(Interrupt, "This", op)` + `message.GainOverKill(effect)`) ; 16046 Hand Cannon (`message.GainOverKill`) ; `message.GainPiercing` / `GainRanged` (do_attack.py, memes methodes) ; RECETTES §2 (choix `ChooseAbilities(ForChoiceAbility(...).SetHasNoTargetEffect())`). « When Marvel Girl attacks » : toute attaque (de base ou par une carte), contre n'importe quel ennemi. UN SEUL mot-cle a la fois.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy019.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 2*, THW 2**, RES B, Class Aggression} ; traits ['PSIONIC', 'STARJAMMER', 'X-MEN'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : choix « piercing » : perce la Tenacite (2 degats passent, ATQ 2) | choix « overkill » : sbire a 1 PV, l'exces (1) passe au vilain | choix « ranged » : contre un sbire a Riposte 1 (Whiplash), elle ne subit pas la Riposte
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 3/3. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy019` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy020 : Critical Blow — Event Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : gam/18020 Hit and Run (« deal N damage to an enemy, remove N threat from a scheme » : `SetTarget(Enemy)` + `SetTarget2(Scheme2)`, label 'attack','thwart') ; night_thrasher/nt006 (`this.DealDamage(.., property=AttackProperty(piercing=True))`) ; fiche requirement.md (`desc.Requirement "YBR"`, base automatique : aucun script). « threat equal to the DAMAGE DEALT this way » : le total rendu par `DealDamage` (un ennemi qui encaisse 0 -> 0 menace retiree). « This attack gains piercing » : le perforant defausse la Tenacite de la cible avant les degats (RR « Piercing »).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy020.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, RES Y, Requirement YBR, Class Aggression} ; traits ['ATTACK', 'THWART'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : 4 degats perforants a Rhino TENACE et 4 menaces retirees (5 -> 1) | CONTRE-CAS Requirement : sans [mental] payee la carte ne se joue pas | sbire a 3 PV, 4 degats : menace retiree = degats INFLIGES (4)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/3 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy020` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy021 : Outlaw Justice — Event Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : 48032 Gunboat Diplomacy (MEME structure : `desc.Alliance`, `CostFunc.Exhaust(Select.Alliance([T1, T2]))`, X relu sur les cartes inclinees `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`, repartition par deux `ChooseAbilities` a `repeat_rules="Threat"` / `"Health"`) ; 23032 As One! (X = somme des `face.attack`). Ici X = ATQ cumulee (pas CTR). « among enemies in play » / « among schemes in play » : repartition LIBRE entre tous les ennemis / toutes les manigances (0 a X choix).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy021.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES Y, Class Aggression, Alliance 1} ; traits ['ATTACK', 'THWART'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Sikorsky (STARJAMMER) + Bug (GUARDIAN) : X = 1 + 1 = 2 -> 2 degats a Rhino et 2 menaces re | CONTRE-CAS, sans personnage GUARDIAN la carte n'est pas jouable (Alliance : 2 traits requi
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy021` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy022 : Reckless Attack — Event Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : us004 Reckless (« Take X damage → remove X threat and deal X damage » : le cout « degats subis » ecrit DANS l'operation, RR Cost « not considered paid unless all of that damage was taken ») ; gam/18020 Hit and Run (`SetPlay().SetLabel(..).SetTarget(Enemy)`) ; RECETTES §3 (`CountTotalBoostStarAndBoost` : « each icon ([star] and [boost]) »).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy022.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ Le cout (defausse + degats a l'identite) est PAYE AVANT les 4 degats, dans `CoutImprudent` (helper du pack).
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES R, Class Aggression} ; traits ['ATTACK'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 4 cas `test_capacites` (nom = card_id) : carte defaussee a 2 icones (boost 1 + etoile) -> 2 degats a l'identite puis 4 a Rhino | une etoile SEULE (Sonic Boom) compte pour 1 icone -> 1 degat a l'identite | aucune icone -> 0 degat a l'identite, les 4 degats partent quand meme | CONTRE-CAS, degats a l'identite PREVENUS (Tenace) -> le cout n'est pas paye, aucun degat a
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 3/4 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy022` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy023 : Energy Cannon — Upgrade Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : 48032 Gunboat Diplomacy (repartition LIBRE entre ennemis : `ForChoiceAbility(..).SetTarget(Enemy, range=(0, X), repeat_rules="Health")` + `this.DealDamage(targets, 1, effect)`) ; rl008 / us007 (compteurs `charge` : `Faces.PlaceCountersOn`) ; fiche restricted.md (`desc.Restricted`, base automatique).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy023.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « Discard Energy Cannon → deal X » : X se lit AVANT la defausse (la carte perd ses compteurs en quittant le jeu) ; la defausse est donc
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES Y, Restricted 1, Class Aggression} ; traits ['TECH', 'WEAPON'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Action -> 1 compteur charge et s'incline | Hero Action avec 2 compteurs -> 2 degats repartis (1 Rhino, 1 sbire), la carte est defauss
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy023` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy024 : Longarm Blaster — Upgrade Aggression

- [x] Étape 2 : cartes de référence : Cartes de reference : sk019 / ra008 (`AfterUnitDefendAgainstAttack(Response, "You", op)`) ; falcon/53024 (`CostFunc.Exhaust("Attached", card_type=Ally)` pour « exhaust the attached ally ») ; 01074 Inspired (`CanPlayThisUpgradeCard(..)`). « After YOU defend » : l'identite du joueur qui defend (pas l'allie porteur) ; « the attached ally's PRINTED attack » : l'ATQ IMPRIMEE (`printed_attack`), sans les bonus (Pirate's Rapier, Blade of the Phoenix).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy024.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES B, MaxPerUnit 1, Class Aggression} ; traits ['TECH', 'WEAPON'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : apres sa defense, Raza (porteur) s'incline -> X = son ATQ IMPRIMEE (2, malgre +1 du Rapier | CONTRE-CAS, le porteur est deja incline -> la Response n'est pas offerte
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy024` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy025 : * Havok (Alex Summers) — Ally Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : cr002 Hepzibah (`WhenUnitUseBasicPower(.., "This", op)` + `message.GainValue(N, effect)`, carte glissee sous un AUTRE hote : le choix et la defausse sont faits dans l'operation) ; 53021 / 53018 (`TuckCardUnderHere(faces, effect)`) ; fiche tuck.md.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy025.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « each icon ([star] AND [boost]) » : `CountTotalBoostStarAndBoost` (RECETTES §3), PAS `CountTotalBoostIcons` ; dans la zone « glissee »
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 4, HP 3, ATK 1*, THW 1*, RES B, Class Justice} ; traits ['STARJAMMER', 'X-MEN'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : entree en jeu -> les 3 cartes du dessus du deck rencontre sont glissees SOUS lui | pouvoir de base -> defausse la carte glissee et gagne +1 par icone (Repair Sequence : boos | CONTRE-CAS, aucune carte glissee -> pas de bonus (ATQ 1 : 1 degat)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/3 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy025` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy026 : * Polaris (Lorna Dane) — Ally Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : sh014 Minarai / leonardo tl009 (`AfterAllyTakeConsequentialDamage(.., "This", op, conditions=[..])`, filtre `from_performing="Thwart"`) ; `AfterUnitThwartAndRemoveLastThreat` (thwart.py:157) pour « removed the last threat » : `message.thw_message.remove_the_last_threat` ; `Faces.GiveStatus([this], "Tough", effect)`. « takes consequential damage FROM THWARTING » : seulement apres une MENEE (pas une attaque). « removed the LAST threat from A scheme » (au moins une manigance a perdu sa derniere menace, `remove_the_last_threat`). Polaris doit rester EN JEU (vaincue par ses propres degats consecutifs : rien a donner).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy026.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 2**, THW 2*, RES Y, Class Justice} ; traits ['STARJAMMER', 'X-MEN'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 3 cas `test_capacites` (nom = card_id) : sa menee retire la DERNIERE menace d'une manigance -> elle subit 1 degat consecutif puis r | CONTRE-CAS, il reste de la menace sur la manigance -> pas de carte Tenace | CONTRE-CAS, apres une ATTAQUE (degat consecutif) -> pas de carte Tenace
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/3 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy026` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy027 : Freedom Fighters — Event Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : 27006 Web Binding (`WhenEnemyWouldActivate(.., op).SetPlay().SetLabel()` + `message.SetBeInstead(effect)` = « cancel that activation ») ; 48032 Gunboat Diplomacy (`desc.Alliance`, `CostFunc.Exhaust(Select.Alliance([T1, T2]))`, X relu sur `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`) ; gam/18020 (`SetTarget(Scheme2)`).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy027.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ TEXTE CONTRADICTOIRE (question en attente, QUESTIONS.md) : « Response » + « When the villain activates » : une Reponse part APRES, or
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES R, Class Justice, Alliance 1} ; traits ['THWART'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : le vilain manigance -> annulation ; Sikorsky (STARJAMMER) + Cannonball (X-MEN) : X = 1 + 1 | CONTRE-CAS, sans personnage X-MEN la carte reste en main
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy027` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy028 : Masterstroke — Event Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : 15004 / ho014 (`Worlds.DiscardEncounterCards(n, effect)` + `FacesCounter.CountTotalBoostIcons`) ; 08013 / 16155 (`ChooseAbilities(ForChoiceAbility(..))` + `.SetTarget(Scheme2)`) ; ag001b / bt011 (`Faces.MoveAllToDeck([face], deck, "Top", effect)`, position en argument POSITIONNEL) ; fiche requirement.md.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy028.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « boost icons ([boost]) » : les icones chiffrees SEULES (`CountTotalBoostIcons`, l'etoile n'est pas une icone de boost ici) ;
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, RES B, Requirement YBR, Class Justice} ; traits ['THWART'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : 4 cartes defaussees ; branche « retirer la menace » : Shocker (boost 2) retire 2 menaces | branche « replacer la carte sur le deck et piocher » : 4 cartes replacees, 4 piochees
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy028` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy029 : Reckless Maneuver — Event Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : sy022 Reckless Attack (meme cout, helper `CoutImprudent`) ; us004 Reckless ; gam/18020 Hit and Run (`SetPlay().SetLabel(..).SetTarget(Scheme2)` + `RemoveThreatFromSchemes`).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy029.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES R, Class Justice} ; traits ['THWART'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : carte a 2 icones -> 2 degats a l'identite puis 4 menaces retirees (6 -> 2) | CONTRE-CAS, degats prevenus (Tenace) -> cout non paye, aucune menace retiree
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy029` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy030 : * Helek — Support Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : `ReduceCostToPlayThis(N, your_identity_has_traits=[..])` (resources.py:657) ; 45049 Stepford Cuckoos (« a player reveals a treachery », `AfterPlayerRevealCard(.., "AnyPlayer", Treachery, op)`) ; as022 (`CanPlayThisSupportCard`). « that player draws » : le joueur qui a REVELE (`message.to_player`), pas forcement le proprietaire de Helek. Reduction : « your identity has STARJAMMER » (Honorary / Captain l'accordent aussi). Cout de base 2 : gratuit pour un STARJAMMER.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy030.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES B, Class Justice} ; traits ['KREE', 'PERSONA'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 4 cas `test_capacites` (nom = card_id) : reduction de 2 pour un STARJAMMER (cout 2 -> 0) : Corsair le joue sans ressource | CONTRE-CAS, Spider-Man (sans le trait) ne le joue pas sans ressource (cout 2) | un joueur revele une traitrise -> Helek s'incline, ce joueur pioche 1 carte | CONTRE-CAS, une carte qui n'est pas une traitrise (sbire) -> pas de pioche
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/4 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy030` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy031 : Disruptor Ray — Upgrade Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : 16046 Hand Cannon (`desc.Uses "N,charge"` + `CostFunc.Counter("This", 1, 'charge')`) ; rl012 / `face.TreatAsIfBlank( effect, until_round_end=True)` (face_action.py:9 : « treat as blank » temporaire, TRAITS conserves) ; fiches uses.md, restricted.md. « an attachment, NON-ELITE minion, or side scheme » : trois types possibles (un sbire ELITE n'est pas une cible). « Until the end of the ROUND » : `until_round_end`. Le dernier compteur retire defausse la carte (Uses).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy031.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES B, Restricted 1, Uses 2,charge, Class Justice} ; traits ['TECH', 'WEAPON'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Action -> Whiplash (Riposte 1) est traite comme sans texte : Spider-Man l'attaque sans sub | TEMOIN, sans le rayon la Riposte 1 de Whiplash blesse Spider-Man (1 degat)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy031` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy032 : Tactical Teleporter — Upgrade Justice

- [x] Étape 2 : cartes de référence : Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(..)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ; 22005 Evasive Maneuvering / 32002 Shadowcat (`UnitIgnoreKeywordIcons(finder, guard=True, patrol=True, crisis=True)`, play.py:517).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy032.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « Attached ally ignores... » : seulement le PORTEUR (condition `message.effect.this is porteur`) ; `UnitIgnoreKeywordIcons` appelle la
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES Y, MaxPerUnit 1, Class Justice} ; traits ['TECH'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 4 cas `test_capacites` (nom = card_id) : +1 CTR (Sikorsky 1 -> 2 menaces retirees) | le porteur ignore la GARDE : il attaque le vilain malgre un sbire a Garde engage | le porteur ignore la PATROUILLE : il menace la manigance principale malgre un sbire a Patr | CONTRE-CAS, sans la carte la Garde empeche d'attaquer le vilain (Sikorsky nu)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 3/4 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy032` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy033 : * Cyclops (Scott "Slim" Summers) — Ally Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : 14001a Quicksilver (`AfterUnitUseBasicPower(Response, "This", op, powers=[..])`) ; 45048 Triage (`SetTarget(Unit2, ..)`) ; hc020 / wt006 (`face.GainUntilPhaseEnd(effect, attack=..)`) ; l'etoile d'une Response est une convention d'IMPRESSION (RECETTES §1). « ANOTHER character » : pas Cyclops ; « THAT basic power » : celui que Cyclops vient d'utiliser (`message.power` -> ATK / THW / DEF / REC) ; « until the end of the phase » : `GainUntilPhaseEnd`.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy033.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, HP 2, ATK 1*, THW 1*, RES R, Class Leadership} ; traits ['CHAMPION', 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : apres son attaque, un AUTRE personnage (Spider-Man) gagne +1 ATQ jusqu'a la fin de la phas | apres sa MENEE le bonus est de +1 CTR (pas ATQ)
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy033` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy034 : * Keeyah — Ally Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : bw024 (`attaquant.BasicAttack(cibles, effect)`) ; 61023 Grapnel Launcher (`BasicThwart` n'epuise pas de lui-meme : « without exhausting » acquis) ; `ally.BasicAttack` / `BasicThwart` : les degats consecutifs de l'allie s'appliquent comme d'habitude. « the SAME basic power » : ATQ ou CTR (les allies n'ont pas de recuperation) ; « ANOTHER ally » : pas Keeyah ; l'allie choisi n'a pas besoin d'etre pret. Les cibles de ce pouvoir se choisissent dans l'operation (apres l'allie).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy034.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 1*, THW 2*, RES Y, Class Leadership} ; traits ['KREE', 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : apres son attaque, Sikorsky attaque AUSSI sans s'incliner (2 degats a Rhino) et subit son 
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy034` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy035 : * Lilandra (Lilandra Neramani) — Ally Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : dt066 Misty Knight (`WhenInYourPlayTurn(Action, op).SetCostFunc(Exhaust("This")).SetCostFunc(CostFunc.DealDamage(1, "This"))`) ; `AbilityFactory.WhenAllyWouldTakeConsequentialDamage` (friend.py:427) + `message.ReduceDamage(n, effect)` ; `RegisterTemp(.., unregister_after_exec=False, until_phase_end=True)` (effect.py:211) pour « until the end of the phase ». « does not take consequential damage » : tous les degats consecutifs de l'allie choisi, attaque comme contre, jusqu'a la fin de la phase.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy035.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 1*, THW 2*, RES B, Class Leadership} ; traits ['PSIONIC', "SHI'AR", 'STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Action (s'incline et subit 1 degat) -> Sikorsky attaque SANS subir son degat consecutif | CONTRE-CAS, un AUTRE allie (Mockingbird) que celui choisi subit son degat consecutif
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy035` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy036 : Decisive Action — Event Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : 61023 Grapnel Launcher (`hero.BasicThwart(cibles, effect)` n'epuise pas ; « without exhausting (even if you are exhausted) » acquis) ; wt006 (`GainUntilPhaseEnd(effect, attack=1, thwart=1)`) ; us004 (cibles d'une carte a deux effets : `SetTarget(Enemy)` + `SetTarget2(Scheme2)`).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy036.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « Your HERO » : la face heros (Hero Action) ; les +1 sont accordes AVANT l'attaque et le contre (« gets +1 ATK and +1 THW until the end
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, RES Y, Requirement YBR, Class Leadership} ; traits ['ATTACK', 'THWART'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : +1 ATQ/+1 CTR, attaque (3 degats) et menee (2 menaces) de base SANS s'incliner
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy036` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy037 : Far-Flung Family — Event Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : 26035 Joining Forces (« a total of 1 X ally and 1 Y ally » : `range=(1, 2)` + `select_rule="MustIncludeTraits"` : UNE carte qui porte les deux traits satisfait les deux) ; 48032 Gunboat Diplomacy (`desc.Alliance` + `CostFunc.Exhaust(Select.Alliance([T1, T2]))`) ; 08011 (`Search.PlayerCard`).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy037.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « as a group, the players search THEIR decks » : les joueurs, DANS L'ORDRE, cherchent chacun dans son deck ce qui manque encore (le 1er joueur
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 4, RES B, Class Leadership, Alliance 1} ; traits [] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Corsair (STARJAMMER) + Nightcrawler (X-MEN) -> un STARJAMMER et un X-MEN du deck entrent e | CONTRE-CAS, sans personnage X-MEN le cout n'est pas payable
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy037` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy038 : Reckless Charge — Event Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : sy022 Reckless Attack (cout `CoutImprudent`) ; 42031 Flying Formation (« ready up to 3 characters » : `SetTarget(Unit2, range=(0, 3), canbe_ready=True)` + `Faces.ReadyAll`).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy038.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ « up to 3 » : 0 a 3 cibles (le minimum 0 est ici imprime). « characters » : heros, allies (le pilote du harnais prend le minimum).
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES R, Class Leadership} ; traits ['TACTIC'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : carte a 2 icones -> 2 degats a l'identite, puis 3 personnages inclines se redressent
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy038` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy039 : Targeting Station — Support Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : us007 / 04064 (`desc.Uses "N,ammo"` + `CostFunc.Counter("This", 1, 'ammo')`) ; rl006 (`CostFunc.Exhaust(.., from_where= ["YouControlCards"])`) ; fiche uses.md (le dernier compteur retire defausse la carte). « a character YOU control » : identite ou allie ; le cout ne peut pas viser le soutien lui-meme (pas un personnage).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy039.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES B, Uses 3,ammo, Class Leadership} ; traits ['LOCATION', 'TECH', 'WEAPON'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : Action -> s'incline le personnage choisi (Spider-Man), 1 compteur de munitions de moins, 3
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy039` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy040 : * Captain of the Starjammer — Upgrade Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : 06007 Asgard / 03xxx (`*GiveKeywordToAttached("You", trait=..)` = « YOU gain trait » : l'IDENTITE, les deux faces ; RECETTES §3) ; 14001a Quicksilver (`AfterUnitUseBasicPower(HeroResponse, "You", op)`) ; sy033 (`GainUntilPhaseEnd(effect, **bonus)`). « YOU gain the trait » : identite = heros ET alter ego. « each STARJAMMER ALLY you control » : les allies (pas l'identite), controles par le joueur. L'amelioration entre en jeu pres de l'identite (aucune cible d'attache imprimee) ; unique (✦).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy040.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, RES Y, Class Leadership} ; traits ['TITLE'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : l'identite (alter ego comme heros) gagne STARJAMMER | apres un pouvoir de base, chaque allie STARJAMMER (Sikorsky) gagne +1 ; pas Mockingbird
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy040` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy041 : Jet Bike — Upgrade Leadership

- [x] Étape 2 : cartes de référence : Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(Ally)` + `*GiveKeywordToAttached(Ally, thwart=1)`) ; 03xxx / `AfterCardAttachTo( Response, "This", Unit2, op)` (RECETTES §3 : `message.to_face` = le porteur ; part aussi pour l'attache initiale). « After YOU attach Jet Bike » : l'attache faite en JOUANT la carte ; l'allie se redresse meme s'il etait pret (sans effet).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy041.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES Y, MaxPerUnit 1, Class Leadership} ; traits ['VEHICLE'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : attachee a Sikorsky incline -> +1 CTR/+1 ATQ et Sikorsky se redresse
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy041` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy042 : * Kalyx — Ally Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 01135 Ultron / `Enemies.PutYouDeckTopCardAsFacedownMinion` (enemies.py:444 : `player.PopPlayerDeckCards(n, process)` + `face.card.SetAsCard(<gabarit>)` + `PutIntoPlay`) ; ul040 / tk101 (carte `Linked` : sy043 est fabriquee MISE DE COTE des que Kalyx est creee, fiche linked.md) ; wt020 (`TreatAsAlly`).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy042.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ Le gabarit d'allie face cachee `sy_thorn_ally` (cards.json, pic « player », ATQ 1, CTR 1, PV 1, trait THORN) porte les valeurs de base que
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 4, HP 3, ATK 1*, THW 1*, RES R, Class Protection} ; traits ['STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : entree en jeu -> trouve Thorn Crew (mise de cote, Linked) et la met en jeu | pouvoir de base -> la carte du dessus du deck entre en jeu FACE CACHEE comme allie THORN
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 2/2. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy042` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy043 : Thorn Crew — Support Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 01140 Ultron Drones (`GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Drone Minion"), base_sch=1, base_atk=1, base_health=1)` + `AfterUnitBeDefeated(ForcedResponse, ..)`) ; fiches linked.md, permanent.md.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy043.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : ⚠ Le moteur n'a pas de `base_thw` pour un allie : les valeurs de base sont portees par le GABARIT `sy_thorn_ally` (cards.json, ATQ 1, CTR 1,
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {RES R, Permanent 1, Class Protection, Linked Kalyx} ; traits [] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : un allie THORN vaincu -> la carte retourne dans la DEFAUSSE de son proprietaire sous sa fa
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 0/1 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy043` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

- ⚠ **Preuve par substitution NON obtenue pour sy043** (rouges 0/1) : le moteur envoie déjà l'allié vaincu à la défausse de son propriétaire sous sa face imprimée (cas vert module retiré). La Réponse forcée de Thorn Crew est donc redondante avec la règle moteur ; les valeurs de base (ATQ 1, CTR 1, PV 1) sont portées par le gabarit `sy_thorn_ally` (QUESTIONS.md n°4). Carte conservée pour fidélité au texte.

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy044 : * K-Zzat — Ally Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 01083 Mockingbird (`Faces.GiveStatus(.., "Stunned", ..)`) ; dt066 Misty Knight (`CostFunc.DealDamage(1, "This")` ; la cible du cout se designe par un selecteur) ; `AfterUnitAttackEnd(type, "This", op)` (RECETTES §1 : `message.attacked_targets`). « deal 1 damage to a FRIENDLY character » est DEVANT la fleche : un COUT, au choix du joueur parmi les personnages amis (K-Zzat peut se viser). « stun THE ATTACKED enemy » : la cible de l'attaque, si elle est encore en jeu (un ennemi vaincu ne se sonne pas).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy044.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, HP 3, ATK 2*, THW 1*, RES Y, Class Protection} ; traits ['STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : apres son attaque, 1 degat a un personnage ami (Spider-Man) -> Rhino est SONNE
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy044` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy045 : * Tolo Hawk — Ally Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 54012 Captain America (`AfterCardEnterPlay(Response, "This")` + `SetTarget(trait=..., card_type=Unit2, canbe_ready=True)` + `Faces.ReadyAll`) ; ub029 Michelangelo (`Friend` pour « friendly character »). « a friendly STARJAMMER character » : identite ou allie ami (de n'importe quel joueur) portant le trait ; `canbe_ready` ecarte les personnages deja prets (Tolo Hawk entre en jeu pret : il ne se redresse pas lui-meme).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy045.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, HP 2, ATK 1*, THW 1*, RES R, Class Protection} ; traits ['STARJAMMER'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : entree en jeu -> redresse un personnage STARJAMMER ami incline (Sikorsky) | CONTRE-CAS, un allie SANS le trait (Mockingbird) reste incline
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy045` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy046 : Ready for Anything — Event Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 01083 Mockingbird (Sonne) ; dt002 (`GiveStatus` « Confused ») ; 19001a / tg010 (`Faces.GiveStatus([identite], "Tough", effect)`). « Stun AND confuse AN enemy » : le MEME ennemi, cible obligatoire (pas de `range=(0, ..)`, RECETTES §6).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy046.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 3, RES B, Requirement YBR, Class Protection} ; traits ['CONDITION'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : Rhino SONNE et DESORIENTE, l'identite recoit une carte Tenace
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy046` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy047 : Reckless Defense — Event Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 01003 Backflip (`WhenUnitWouldTakeDamage(Interrupt, who, op, is_from_attack=True).SetPlay().SetLabel('defense')` + `message.PreventDamage("All", effect)`) ; sy022 (cout `CoutImprudent`, RR Cost : prevention partielle = cout non paye = rien n'est prevenu). « a CHARACTER » : tout personnage ami (allie ou identite), pas seulement vous ; « Hero Interrupt » : forme heros.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy047.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 0, RES R, Class Protection} ; traits ['DEFENSE'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Rhino attaque un heros incline (2 degats) ; carte defaussee sans icone -> TOUS les degats  | CONTRE-CAS, sans la carte les 2 degats de Rhino passent
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy047` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy048 : Rogue Heroics — Event Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : sy021 Outlaw Justice / 48032 Gunboat Diplomacy (cout `Select.Alliance`, X = ATQ cumulee, repartition LIBRE) ; 01083 Mockingbird (`Faces.GiveStatus(.., "Stunned", ..)`). « Stun each character damaged THIS WAY » : les ennemis qui ont reellement perdu des PV (une Tenacite qui annule les degats : pas de Sonne) ; un ennemi vaincu n'est plus en jeu. Les PV sont releves AVANT/APRES chaque cible.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy048.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 2, RES R, Class Protection, Alliance 1} ; traits ['ATTACK'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : Sikorsky + Bug : 2 degats a Rhino, Rhino est SONNE | CONTRE-CAS, Rhino TENACE : les degats sont annules, il n'est PAS sonne
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON. Une carte qui ne fait que chiffrer ou déclencher une réponse.
- [x] Texte français : clé `sy048` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy049 : Armored Space Suit — Upgrade Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 01074 Inspired (`CanPlayThisUpgradeCard(..)` + `*GiveKeywordToAttached(Ally, trait="AERIAL")`) ; sy041 Jet Bike (`AfterCardAttachTo(Response, "This", Unit2, op)` : `message.to_face` = le porteur, RECETTES §3 : un compteur/statut pose AVANT l'attache est perdu) ; `Faces.GiveStatus([porteur], "Tough", effect)`.
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy049.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1, RES R, MaxPerUnit 1, Class Protection} ; traits ['ARMOR', 'TECH'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 2 cas `test_capacites` (nom = card_id) : attachee a Raza -> trait AERIAL et carte d'etat Tenace | CONTRE-CAS, Raza sans la carte n'est pas AERIAL ni Tenace
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/2 ⚠ un cas reste vert sans module. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? OUI (« Max N per deck / ally / character » : règles de deck / de pose lues nativement par le moteur (`desc.MaxPerDeck`, `desc.MaxPerUnit`), pas de « limite par round »)
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy049` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

### sy050 : Plasnet Launcher — Upgrade Protection

- [x] Étape 2 : cartes de référence : Cartes de reference : 16046 Hand Cannon (`desc.Uses "N,charge"` + `CostFunc.Counter("This", 1, 'charge')`) ; brawn/bw008 (`GainUntilRoundEnd( effect, attack=N)`) ; 40053 / 44046 (`desc.Cost "N*"` = N par heros) ; fiches uses.md, restricted.md. « the villain gets -1 ATK » : le (premier) vilain ; cumulatif si l'Action est reutilisee (la carte est incline : une fois par round).
- [x] Étape 5 : texte-contre-code : script relu phrase par phrase contre le scan (`assets/pics/sy050.jpg`, transcription `TRANSCRIPTIONS.md`) ; mots-pièges et choix : voir l'en-tête du module.
      Résultat : conforme ; texte imprimé = champ `text` de cards.json.
- [x] Étape 6 : nombres texte <-> code : `desc` = {Cost 1*, RES B, Restricted 1, Uses 3,charge, Class Protection} ; traits ['TECH', 'WEAPON'] ; relus sur le scan, identiques dans le script.
      Résultat : conforme.
- [x] Étape 7 : 1 cas `test_capacites` (nom = card_id) : Action -> Rhino perd 1 ATQ pour le round (2 -> 1), 1 compteur de charge de moins, le lance
      Preuve par substitution (`tools/substituer_pack.py`, module remplacé par un stub) : rouges 1/1. Un cas qui reste vert sans module est une valeur imprimée, un contre-cas d'absence ou un témoin (assumé, voir la liste des cas ci-dessus).
- [x] Étape 7 bis : limite imprimée ? NON
      Résultat : aucun « Limit once per round/phase » imprimé sur cette carte ; les plafonds de pose sont ceux du moteur.
- [x] Étape 8 : autoplay ciblé : voir l'en-tête de ce fichier (deck de test Corsair + 48 cartes sy, 8 parties contre Rhino, témoin Corsair).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI (attache / glisse / compteur / statut / allié face cachée). Cas plateau : `ui-app/src/board/starjammers-aspects-plateau.test.ts` (vert dès l'écriture : le plateau dessinait déjà ces cas, aucun correctif).
- [x] Texte français : clé `sy050` dans `ui-app/src/board/textes-fr-fanmade.ts` (présent).

Carte terminée : NON (provisoire) : aucune partie réelle jouée par un humain ; autoplay : voir l'en-tête.

## Cartes Linked masquées dans le deck-builder (26/10/2026)

`sy018` Blade of the Phoenix et `sy043` Thorn Crew sont `Linked` : mises de côté par leur carte, jamais dans le deck d'un joueur (RR « Linked »). `estCarteJoueur` (`public/js/deckbuilder/regles.js`) rend désormais `false` pour toute carte à `desc.Linked`. Test : `tools/tests-lanceur/deckbuilder-linked.test.mjs` (rouge avant, vert après) ; `regles-starjammers-aspects.test.mjs` mis à jour (48 proposées + 2 masquées).
⚠ La règle vaut pour TOUTES les cartes Linked du catalogue : 21 autres (officielles et fan-made : 43034-43037, 49033-49036, 51036, 53034, 55063-55066, tk106-109, ul041-043) étaient proposées à tort et ne le sont plus. Aucun deck livré n'en contient (vérifié).
