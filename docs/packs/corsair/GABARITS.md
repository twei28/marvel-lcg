# Corsair (Christopher Summers, Starjammers) : gabarits PROCESSUS-CARTE, 26/10/2026

Pack `corsair` (préfixe `cr`, set 224, auteurs Phenexian et Mysteltainn). Scripts : `src/cards/pack/corsair/{corsair,corsair_nemesis}/`.
Cas : `tools/cas/corsair.py` (54 cas `[cr]`) ; plateau : `ui-app/src/board/corsair-plateau.test.ts` ; decks `corsair` (obligation Irresponsible
Cad) et `corsair_making_amends` (variante, obligation alternative) ; recettes `RECETTES-MOTEUR.md` §30 ; fiches `mots-cles/tuck.md`, `uses.md`.

**Aucune carte n'est « terminée »** : il manque la partie réelle jouée par un humain (voir la fin), et plusieurs cartes portent une question de
règle en suspens (choix provisoire codé, consigne utilisateur du 25/10/2026 : les questions sont gardées pour la fin).

Lecture de la substitution (`substituer_pack.py`, `rouges N/M`) : les cas qui restent verts sans module sont des **valeurs imprimées**, des
**contre-cas d'absence** ou des **témoins** (assumés ci-dessous). Autoplay : 8 parties Corsair contre Rhino (1 victoire, 5 « manigance
accomplie », 2 « tous éliminés »), 0 exception, 0 blocage ; témoin `spider_man` 8 parties (0 victoire), 0 blocage. Pack identique avant/après
substitution (md5 `c706981c…`).

**26/10/2026, après les correctifs d'arbitrage** (cr001a, cr003, cr007-009, cr016) : autoplay relancé, 8 parties Corsair contre Rhino (1 victoire, 5 « manigance accomplie », 2 « tous éliminés »), 0 exception
(grep NameError / AttributeError / TypeError / KeyError / AssertionError sur les 8 journaux : 0), 0 blocage ; témoin `spider_man` 8 parties (0 victoire, 0 exception, 0 blocage). Decks `corsair` et
`corsair_making_amends` : OK (`verifier_tous_les_decks`, deck par deck). Substitution : pack identique avant/après (md5 `92ec54c1…`).

---

### cr001a : Corsair (face héros)
- [x] Étape 2 : références : jouer comme en main : `tc013` Casey's Bag / `td012` (`AttachedCardCanPlayLikeInHand`, SANS `also_spend`) ;
      Pocket Universe Gems : `65001a` Wave (`AfterCardsBeSpendAsResource`) + `60037a` Echo (ranger depuis la défausse).
- [x] Étape 5 : mots-pièges : « play » ≠ « spend » (FAQ : on ne dépense pas une carte glissée) ; « discarded **to pay for a cost** » (coût =
      avant la flèche ou « spend », FAQ) ; « **once per round** » PARTAGÉE entre les deux chemins. Résultat : DEUX chemins codés (dépense de
      ressources ; défausse en coût `CostFunc.Discard`), un marqueur de round sur l'identité.
      **CORRIGÉ le 26/10/2026 (arbitrage RR « Cost » : dépenser des ressources = défausser des cartes de la main)** : au chemin ressources la carte est
      DÉFAUSSÉE (zone de ressources -> défausse) PUIS glissée depuis la défausse : la Réponse écoute `AfterCardDiscard` (`from_area.flags.is_resources_area`)
      et non plus `AfterCardsBeSpendAsResource`. Corsair's Rapier (cr003) voit donc cette défausse. Gemmes et Rapier répondent à la MÊME défausse,
      déclenchés ensemble : `ToujoursEnDefausse` (helper du set) empêche la 2e de glisser une carte déjà glissée (constaté : sans garde, la carte était
      glissée DEUX fois).
- [x] Étape 6 : nombres : PV 10, ATK 1, THW 2, DEF 2, HS 5 (scan) = `desc` = cas de valeurs imprimées. Résultat : vert.
- [x] Étape 7 : cas : jouer une carte glissée (payée par 01088 ; la ressource dépensée est à son tour glissée) ; Gemmes par dépense de ressources ;
      Gemmes par coût de défausse (Plan B 27024) ; contre-cas défausse hors coût. Substitution : rouges 4/6 (les 2 verts : valeurs imprimées,
      contre-cas « pas de coût »).
      **26/10/2026** : +1 cas « une carte SKILL dépensée en ressource n'est glissée QU'UNE fois (Gemmes et Rapier) » ; substitution relancée : **rouges 4/7**
      (3 verts : valeurs imprimées, contre-cas « pas de coût », et ce nouveau cas, vert aussi sous substitution parce que Rapier SEUL glisse la
      carte SKILL : c'est une GARDE contre le double glissement, pas la preuve de Gemmes ; la preuve de Gemmes = les cas « dépensée en ressource »).
      **Honnêteté** : « Rapier voit la défausse de la dépense » n'est pas mesurable par un cas : le pilote choisit Gemmes, Rapier reste prêt, et l'état
      final est le même qu'avant le correctif. Garanti par construction (la Réponse de Gemmes part de `AfterCardDiscard`), pas par un rouge/vert.
- [x] Étape 7 bis : limite imprimée OUI. Témoin d'épuisement : « deux cartes jouées dans le round -> UNE seule glissée » (`cr_nb_glissees == 1`).
- [x] Étape 8 : autoplay : 8 parties, 0 exception ; journal lu (cartes glissées et jouées). 
- [x] Étape 8 bis : la carte change ce qu'on VOIT (glisse sous l'identité) : OUI. Cas plateau `corsair-plateau.test.ts` (3 cas verts ; fixture écrite à
      la main sur le modèle `echo-photographic-reflexes`, aucun correctif d'affichage n'était nécessaire : pas de « vu rouge »).
Carte terminée : NON (provisoire) : partie réelle humaine. (Question 1 tranchée le 26/10/2026 : option A confirmée, avec le correctif ci-dessus.)

### cr001b : Christopher Summers (face alter ego)
- [x] Étape 2 : `ok001b` (`WhenCardSetup` + `Search.PlayerCard` + `GainCard`). Règle de deck « STARJAMMER de n'importe quel aspect » : `regles.js`
      (précédent `cyclops`, id de deck `corsair` et `corsair_making_amends`).
- [x] Étape 5/6 : PV 10, REC 3, HS 6, OUTLAW. Setup résolue après le mulligan (FAQ). Résultat : vert.
- [x] Étape 7 : cas Setup (cr003 en main au montage) + valeurs imprimées. Substitution : rouges 1/2 (le vert : valeurs imprimées).
- [x] Étape 7 bis : NON. Étape 8 : autoplay ci-dessus. Étape 8 bis : NON (la règle de deck vit côté deckbuilder, test node à ajouter si besoin).
Carte terminée : NON (provisoire) : le deckbuilder n'a pas de test node propre à cette règle (écart noté).

### cr002 : Hepzibah
- [x] Étape 2 : `47012` Husk (`WhenUnitUseBasicPower(Interrupt, "This")`, `message.GainValue`). La défausse d'une carte glissée sous UN AUTRE hôte ne
      passe pas par `CostFunc.Discard` (« ThisPlaceCards » vise la carte qui porte l'effet) : faite dans l'opération.
- [x] Étape 5/6 : « uses a basic power » (attaque ET menée) ; « +3 to that power for this use » ; coût 3, PV 3, ATK 2*, THW 0*. Résultat : vert.
- [x] Étape 7 : attaque +3 (5 dégâts), menée +3 (3 menaces), contre-cas sans carte glissée, valeurs imprimées. Substitution : rouges 2/4 (verts :
      contre-cas, valeurs imprimées).
- [x] Étape 7 bis : NON. Étape 8 : autoplay. Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle.

### cr003 : Corsair's Rapier
- [x] Étape 2 : `03009` (+1 ATQ attaché), `47004` (Hero Response + `Exhaust("This")`), `60037a` (ranger depuis la défausse).
- [x] Étape 5 : « after you discard a **SKILL** card from your **hand** » ; FAQ « for any reason » : depuis la main OU la zone de ressources (une carte
      dépensée part de la main). Résultat : codé ainsi.
- [x] Étape 6 : coût 1, Restricted 1, MaxPerUnit 2. Étape 7 : +1 ATQ (héros) ; contre-cas alter ego ; SKILL défaussée -> glissée + Rapier incliné ;
      contre-cas non SKILL. Substitution : rouges 2/5 (verts : contre-cas et témoins d'absence).
      **26/10/2026** : la condition ET l'opération vérifient que la carte attend encore dans la défausse (`ToujoursEnDefausse`) : Gemmes (cr001a) peut l'avoir
      glissée avant elle (voir cr001a). Substitution relancée : rouges 2/5 (les 3 verts : contre-cas et le contre-cas Gloves voisin).
- [x] Étape 7 bis : NON. Étape 8 : autoplay. Étape 8 bis : OUI (glisse) : couvert par le cas plateau commun.
Carte terminée : NON (provisoire) : partie réelle humaine. (Question 2 tranchée le 26/10/2026 : A confirmé.)

### cr004 : Pulse Blaster (x2)
- [x] Étape 2 : `16036` Particle Cannon (`ThisEnterPlayWithCounters` + `CostFunc.Counter`). PAS de clé `Uses` (elle défausserait la carte).
- [x] Étape 5/6 : 3 compteurs de charge, coût 1, Restricted. « After you attack » ; « if you removed the LAST counter ... tuck it ». Résultat : vert.
- [x] Étape 7 : 3 compteurs à l'entrée ; -1 compteur et +1 dégât après une attaque ; dernier compteur -> glissée sous Corsair (hors jeu). Substitution :
      rouges 3/3.
- [x] Étape 7 bis : NON. Étape 8 : autoplay. Étape 8 bis : OUI (glisse) : plateau.
Carte terminée : NON (provisoire) : question 3.

### cr005 : Corsair's Gloves
- [x] Étape 2 : `01008` Web-Shooter (`CanGenerateResources(HeroResource)`), `conditions` sur `Message.CheckPlayerCanPayCost`.
- [x] Étape 5/6 : « for a card tucked under Corsair » seulement ; coût 2. Résultat : vert.
- [x] Étape 7 : paie la carte glissée jouée (Gants inclinés) ; contre-cas : ne paie pas une carte de la main. Substitution : rouges 1/2 (vert : contre-cas).
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay.
Carte terminée : NON (provisoire) : partie réelle.

### cr006 : Ace Pilot
- [x] Étape 2 : `47004` (`AfterPlayerPlayedCard(HeroResponse, "You", ...)`) ; trait `traits=[...]` = OU.
- [x] Étape 5/6 : « ATTACK **or** THWART event » ; « ready your identity **and** a VEHICLE you control » : les deux. Coût 2.
- [x] Étape 7 : redresse l'identité après un événement THWART ; redresse aussi un VEHICLE (08023 Quincarrier). Substitution : rouges 2/2.
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay.
Carte terminée : NON (provisoire) : question 4.

### cr007 : Parry (x2)
- [x] Étape 2 : `03033` Expert Defense (`WhenUnitDefendAgainstAttack(HeroInterrupt, "YourHero")`, `GainDEFForThisAttack`) ; `DrawUp(n)` ; `nt005` pour
      « the last card you played ».
- [x] Étape 5 : « the **last** card you played » : la carte en cours de résolution est écartée de `stat.game_played_cards`. Résultat : codé ainsi.
      **CORRIGÉ le 26/10/2026 (RR : aucune borne de round)** : la liste est celle de TOUTE LA PARTIE (`PlayerStat.game_played_cards`, CORRECTIF moteur, vidée
      seulement à la mise en place) ; avant, `this_round_played_cards` : Riposte (phase du vilain) puis Remise (tour suivant) ne se voyaient pas.
- [x] Étape 7 : défense +3 (aucun dégât subi) et pioche 1 ; pioche 3 après Remise ; traits DEFENSE SKILL. Substitution : rouges 1/3 (deux cas restent verts sans module, dont
      les valeurs imprimées ; l'autre n'a pas été analysé : à relire).
      **26/10/2026** : +1 cas « Remise jouée au round PRÉCÉDENT compte encore (pioche 3) », avec `Puzzle.PlayersNewRound()` entre les deux : VU ROUGE
      (« main = 1 carte(s) (attendu 3) ») avant le correctif, vert après. Substitution : **rouges 2/4** (verts : valeurs imprimées ET « défense +3 et pioche 1 »,
      qui reste vert sans module : écart ANTÉRIEUR, le cas ne distingue pas « Parry jouée » de « Parry restée en main » ; non corrigé ici, hors périmètre).
- [x] Étape 7 bis : NON. Étape 8 : autoplay (Parry jouée, pioche lue au journal). Étape 8 bis : NON.
Carte terminée : NON (provisoire) : partie réelle humaine. (Question 5 tranchée le 26/10/2026 : B appliquée, la Remise du round précédent compte.)

### cr008 : Riposte (x2)
- [x] Étape 2 : `37011` Bishop (`AfterUnitAttackYou(Response, Enemy)`), `19007` Payback (`SetPlay().SetLabel('attack')`), `05015` (statut).
- [x] Étape 5 : « After an enemy attacks you » (l'attaquant du message) ; « if the last card you played was Parry, stun ». 4 dégâts, coût 1.
- [x] Étape 7 : 4 dégâts à Rhino ; sonné après Parry ; valeurs imprimées. Substitution : rouges 2/3 (vert : valeurs imprimées).
      **26/10/2026** : +1 cas « Parry jouée au round PRÉCÉDENT compte encore (ennemi sonné) » : VU ROUGE (« 01094 ne porte pas le statut Stunned ») avant
      le correctif, vert après. Substitution relancée : **rouges 3/4** (vert : valeurs imprimées).
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay.
Carte terminée : NON (provisoire) : partie réelle humaine. (Question 5 : voir cr007.)

### cr009 : Remise (x2)
- [x] Étape 2 : `01021` Gamma Slam (`HeroAction` + `SetLabel('attack')`), `nt005`. 3 dégâts, coût 1.
- [x] Étape 7 : 3 dégâts ; après Riposte : 4 + 3 = 7 et héros redressé ; contre-cas sans Riposte (héros reste incliné). Substitution : rouges 3/3.
      **26/10/2026** : +1 cas « Riposte jouée au round PRÉCÉDENT compte encore, Corsair se redresse » : VU ROUGE (« cr001a est incliné alors qu'il devrait être
      prêt ») avant le correctif, vert après. Substitution relancée : **rouges 4/4**.
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay.
Carte terminée : NON (provisoire) : partie réelle humaine. (Question 5 : voir cr007.)

### cr010 : Trick up my Sleeve (x3)
- [x] Étape 2 : `01023` (`SetLabel('thwart')`, `RemoveThreatFromSchemes`), `05015` (statut Désorienté). 4 menaces, coût 2.
- [x] Étape 5 : « You **may** discard a card tucked under Corsair to confuse » : facultatif ; la défausse est le coût du statut. Résultat : vert.
- [x] Étape 7 : 6 -> 2 menaces ; avec une carte glissée : ennemi désorienté et une carte glissée de moins. Substitution : rouges 2/2.
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay.
Carte terminée : NON (provisoire) : partie réelle.

### cr011 : Irresponsible Cad (obligation)
- [x] Étape 2 : `01160` Legal Work (`WhenThisObligationGiveToYou`), `hc013` (obligation révélée = en jeu : coder retrait ET défausse), `GainSurge`.
- [x] Étape 5 : « Cyclops **or** Havok » (toutes versions, `NomNu`) ; « Otherwise, gains surge, **then** discard » (Renfort d'abord). Résultat : vert.
- [x] Étape 7 : Cyclops défaussé -> retirée de la partie ; autre allié -> Renfort + défaussée (défausse RENCONTRE, vue au journal). Substitution : 2/2.
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay.
Carte terminée : NON (provisoire) : question 6.

### cr012 : Making Amends (obligation alternative, deck `corsair_making_amends`)
- [x] Étape 2 : `01160` (squelette identique : `YouMayFlipToYourAlterEgoForm` + deux branches, la 1re réservée à l'alter ego). Étape 5/6 : boost 2.
- [x] Étape 7 : 1re branche (alter ego : incline, retirée) ; 2e branche (alter ego DÉJÀ incliné : le pilote prend la 2e) : une carte contrôlée
      défaussée, Renfort, obligation défaussée. Substitution : 2/2. Étape 7 bis/8 bis : NON. Étape 8 : le deck variante monte une partie (passe decks).
Carte terminée : NON (provisoire) : question 7.

### cr013 : D'Ken (sbire némésis)
- [x] Étape 2 : `58027` Brother vs. Brother (« additional cost to attack »). PV 5, ATQ 1, SCH 1, boost 2, Villainous (`desc`), ELITE KING SHI'AR.
- [x] Étape 7 : attaquer D'Ken coûte une carte de la main ; main vide -> attaque empêchée ; valeurs imprimées. Substitution : rouges 2/3 (vert : valeurs
      imprimées). Étape 7 bis/8 bis : NON. Étape 8 : autoplay (0 exception ; l'effet de D'Ken n'a pas été repéré au journal).
Carte terminée : NON (provisoire) : question 8.

### cr014 : Slave Pits of Chandilar (manigance annexe)
- [x] Étape 2 : `gs119` Imprisoned on Chandilar (glisser sous une manigance, rendre à la défaite), `50081` (`TuckCardUnderHere` = face cachée), `58027`
      (défausse choisie). Menace 2 par joueur, 1 icône Accélération, boost 3.
- [x] Étape 5 : « each player **who cannot** discards » ; « under its **owner's** control ». Résultat : codé ainsi.
- [x] Étape 7 : l'allié est glissé face cachée ; sans allié ni soutien PERSONA : défausse 1 carte ; vaincue : l'allié revient (dégâts effacés, mesure
      distinctive) ; menace de départ 2. Substitution : rouges 3/4 (vert : valeur imprimée).
- [x] Étape 7 bis/8 bis : OUI (glisse sous manigance) : cas plateau (2 cas verts). Étape 8 : non couverte par l'autoplay (Rhino ne la révèle pas).
Carte terminée : NON (provisoire) : question 9.

### cr015 : Shi'ar Bodyguard (sbire némésis, x2)
- [x] Étape 2 : `UnitCannotBeAttacked` (`do_attack.py:990`), `gb018` (boost), `Faces.GiveStatus(..., "Tough")`. PV 4, ATQ 2, SCH 1, Guard + Toughness (`desc`).
- [x] Étape 5 : « Players cannot attack ELITE **minions** » (le vilain n'est pas concerné). Étape 7 : D'Ken (ELITE) non attaquable avec le garde du corps en jeu ;
      valeurs imprimées. Substitution : rouges 1/2 (vert : valeurs imprimées).
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay. Le Boost (donner « robuste » au vilain et aux sbires ELITE) n'a pas de cas : non mesuré.
Carte terminée : NON (provisoire) : le Boost n'a pas de cas ; question 10.

### cr016 : Shi'ar Battle Cruiser (environnement)
- [x] Étape 2 : `gb018` (`WhenVillainPhaseEnd` + `TakeIndirectDamage`), `60122` (Hero Action de carte de rencontre, `SetCost`). Boost 1.
- [x] Étape 5 : **Alliance** : la clé `desc.Alliance` fait planter TOUTE partie sur une carte de rencontre (`HasAlliance` n'existe que pour `Event`).
      **CORRIGÉ le 26/10/2026 (RR « Alliance » : « While paying costs for this card, any player may contribute »)** : la capacité de jeu (Hero Action) est marquée
      `ability.cout_en_groupe = True` (même marque que `sk280`, lue par `CheckAnyPlayerMayHelpPay`) : tout joueur aide à payer les YY ; seule l'inclinaison de
      l'identité reste au joueur actif. Fiche `mots-cles/alliance.md` complétée.
- [x] Étape 7 : fin de phase du vilain -> 1 dégât indirect ; Hero Action « incliner l'identité et dépenser YY » -> défaussée. Substitution : 2/2.
      **26/10/2026** : +1 cas « ALLIANCE (2 joueurs), l'autre joueur paie les YY » (la main de Corsair ne couvre pas YY, celle du joueur 2 a 01088) : VU ROUGE
      (« cr016 est encore en jeu ; cr001a n'est pas incliné ») avant le correctif, vert après. Substitution : **rouges 3/3**.
- [x] Étape 7 bis/8 bis : NON. Étape 8 : autoplay.
Carte terminée : NON (provisoire) : partie réelle humaine (le paiement à deux se joue à deux joueurs : à voir à l'écran). (Question 11 tranchée le 26/10/2026 : B.)

### cr017, cr018, cr019 : Energy / Genius / Strength (reskins Basic, art de Phenexian et Mysteltainn)
Aucun module (ressources). Valeurs `RES` YY / BB / RR, « Max 1 per deck ». Précédent Hellcat (`hc023-hc026`) et Roz (`rz013-rz015`).
Carte terminée : NON (provisoire) : question 12.
- [x] **26/10/2026, arbitrage reskins** (RR « A copy of a card is defined by title » + GUIDE §12 bis) : ces trois ressources ne changent que l'image de `01088` / `01089` / `01090` : ART ALTERNATIF des ressources doubles. Traitement, comme Gwenpool / Beast / Binary : collection `corsair` dans `COLLECTIONS` (`ui-app/src/board/variantes.ts`) ET dans `COLLECTIONS_RESSOURCES` (`public/js/prepare/app.js`, proposée par défaut au héros « Corsair » : `collectionDuHeros`). Les cartes restent dans `cards.json` (précédent TMNT / Gwenpool).
      « Max 1 per deck » par TITRE : `validerDeck` (`public/js/deckbuilder/regles.js`, `cleCopie` = titre|sous-titre) compte déjà `01088` + le reskin comme un même titre ; **aucun correctif nécessaire**, preuve : `tools/tests-lanceur/regles-ressources-doubles-par-titre.test.mjs` (4 verts : chaque reskin du dépôt + son officielle = « Trop d’exemplaires de « Energy » : 2/1 », deux mêmes reskins idem, un seul légal, trois titres différents sans gêne). Le moteur n'applique pas MaxPerDeck (seul le constructeur le juge).
      Collection : `ui-app/src/board/resources-art-packs-fanmade-2026-10.test.ts` (45 verts : ordre Energy/Genius/Strength, wizard aligné, images présentes ; ROUGE vu avant le câblage : 18 échecs sur 27, puis rouge à nouveau en retirant l'entrée du wizard).
      Carte terminée : NON (provisoire) : partie réelle humaine (voir la collection « Corsair » dans la modale du héros et les trois ressources à l'écran).

---

## Questions en attente (une par carte ; l'option A est celle qui est codée)

> **26/10/2026 : TOUTES TRANCHÉES** (règles + scans, `VERDICTS-REGLES-2026-10-26.md`) : 1, 3, 4, 7 à 10 et 12 : option A confirmée ; **2** : A confirmée
> (réserve sur 1 corrigée, voir cr001a) ; **5** : B appliquée (liste de TOUTE la partie, `PlayerStat.game_played_cards`) ; **11** : B appliquée (`cout_en_groupe`) ;
> **6** (cr011 / cr012, « Discard a card you control ») : DÉCISION UTILISATEUR du 26/10/2026 : en jeu seulement, option A codée. Le texte ci-dessous est
> conservé pour mémoire.

1. **cr001a Pocket Universe Gems** : « discarded to pay for a cost ». A : les deux chemins (dépense de ressources de la main, et défausse en coût
   `CostFunc.Discard`), UNE limite par round ; au chemin ressources la carte est rangée depuis la zone de ressources (elle n'est jamais « défaussée »
   pour les autres cartes). B : dépense de ressources seulement.
2. **cr003 Rapier** : « discard a SKILL card from your hand ». A : toute défausse depuis la main OU dépense en ressource (FAQ « for any reason »). B :
   uniquement les défausses d'effet/coût, pas la dépense de ressources.
3. **cr004 Pulse Blaster** : jouée depuis sous Corsair. A : elle revient avec 3 compteurs neufs. B : elle reste à 0 compteur (injouable utilement).
4. **cr006 Ace Pilot** : « ready your identity and a VEHICLE you control ». A : l'identité est redressée même sans VEHICLE. B : sans VEHICLE en jeu,
   rien ne se redresse.
5. **cr007 / cr008 / cr009** : « the last card you played ». A : la dernière carte jouée DANS LE ROUND (le moteur ne garde que la liste du round). B : dans
   toute la partie (la Remise jouée en fin de round précédent compterait ; demande un changement du moteur).
6. **cr011 Irresponsible Cad** : « Discard a card you control ». A : au choix du joueur parmi ses cartes en jeu (alliés, améliorations, soutiens,
   hors identité) ; Cyclops/Havok reconnus par leur nom, toutes versions. B : aussi les cartes glissées sous Corsair.
7. **cr012 Making Amends** : « Exhaust Christopher Summers and tell someone you love them ». A : seule l'inclinaison est exigée par le moteur (le geste
   à la table est laissé aux joueurs). B : sans objet côté moteur.
8. **cr013 D'Ken** : « As an additional cost to attack D'Ken, you must discard a card ». A : valable pour toute attaque d'un héros OU d'un allié
   (la carte est défaussée de la main du joueur qui contrôle l'attaquant). B : héros seulement.
9. **cr014 Slave Pits** : « an ally or PERSONA support they control ». A : chaque joueur en choisit UN ; s'il n'en a pas, il défausse 1 carte de sa
   main. B : tous ses alliés et soutiens PERSONA sont glissés.
10. **cr015 Shi'ar Bodyguard** : « Players cannot attack ELITE minions ». A : aucun joueur (ni son allié) ne peut attaquer un sbire ELITE, même engagé
    avec un autre joueur. B : seuls les sbires engagés avec le joueur concerné.
11. **cr016 Shi'ar Battle Cruiser** : « Alliance ». A (écart actuel) : le mot est imprimé mais sans effet, le joueur actif paie YY seul. B : paiement
    collectif (demande une extension moteur de `Alliance` aux cartes de rencontre).
12. **cr017-cr019** : reskins d'art. A : cartes à part (précédent Hellcat/Roz). B : arts alternatifs des ressources officielles.

## À vérifier en partie réelle (aucun outil du projet ne le voit)
- Une partie complète avec Corsair choisi dans Fan-made (tuile « Corsair », variante « Making Amends » à l'ouverture de sa fenêtre).
- **Cliquer une carte glissée sous Corsair pour la jouer** à l'écran (le moteur l'offre, le plateau la dessine ; le geste de clic n'est PAS prouvé).
- La fenêtre « Pocket Universe Gems » (réponse optionnelle) à chaque dépense de ressources, et son silence après la 1re utilisation du round.
- Les deux icônes de ressource lues à l'œil : Gloves (mental), Remise/Ace Pilot/Rapier/Pulse Blaster (énergie), Parry/Riposte (physique) :
  comparées à des cartes officielles de glyphe connu (01028 mental, 01027 énergie, 01024 physique), pas découpées pixel par pixel.
- La biographie au survol dans l'assistant (entrée `heros-info.js`).
- Le Boost de Shi'ar Bodyguard et la Setup d'un joueur multijoueur de Slave Pits.

## Cas ajoutés le 26/10/2026 (rapport « problèmes à corriger », partie B)

- **cr001a, cas « Gemmes ÉPUISÉES » ** (`tools/cas/corsair.py`) : cr006 payée par 01088 (Gemmes la glisse, limite d'une fois par round atteinte), puis cr009 payée par cr007 (SKILL) : seule Corsair's Rapier peut la glisser, elle s'incline. Mesure : `cr_glissees = [01088, cr007]`, `exhausted = [cr003]`.
  Preuve : vert ; **rouge** quand `cr003` ignore la zone de ressources (mutant qui simule l'ancien comportement : « la carte dépensée n'est pas vue comme défaussée »). Limite honnête : le dossier `corsair` n'a pas d'historique git (pack non commité), l'ancien code de `cr001a` lui-même ne peut pas être rejoué ; c'est la moitié Rapier du correctif qui est prouvée.
- **cr007 Parry, +3 DEF mesuré** : attaque boostée (Rhino 2 + Shocker boost 2 = 4 contre DEF 2). Avec Parry : 0 dégât, la carte est en défausse (jouée), main = 1 (la pioche). Contre-cas sans Parry : 2 dégâts. Le cas d'origine (« degats_identite 0 ») ne prouvait rien : Rhino seul (ATK 2) ne passe pas la DEF 2 de Corsair.
  Preuve : **rouge** avec `GainDEFForThisAttack(0)` (mutant), contre-cas vert sous mutant (il mesure bien l'absence d'effet) ; fichiers restaurés, md5 identiques.
- Passe `[cr]` complète : 57/57 verts.
Carte terminée : NON (provisoire) : partie humaine non faite.
