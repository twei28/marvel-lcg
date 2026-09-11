# Hellcat (jakxin, `hc`) : gabarits PROCESSUS-CARTE, une carte à la fois

Relevé et arbitrages : `2026-09-11-hellcat-releve-des-cartes.md`.
Cas : `tools/test_capacites.py`, bloc « Pack « hellcat » » (46 cas, filtre `hc0`).
Substitution : `tools/substituer_pack.py <game_dir> 45000 hc` (bilan en fin de fichier).
Plateau : `ui-app/src/board/hellcat-cartes-accrochees.test.ts` (3 tests).
Autoplay : `hellcat`, `hellcat_she_hulk`, témoin `spider_man`, Rhino ×8.

Conventions communes à tout le pack :
- **Cartes accrochées** = cartes glissées face visible sous la carte identité
  (`PlaceCardHere` / `GetPlacedCardArea`), lues par le plateau comme des
  cartes portées (`bind_object_id`). Les améliorations sans « Attach to »
  n'en font PAS partie (règle officielle, arbitrage du portage).
- Étape 8 (autoplay) : commune au pack, voir bilan.
- Étape 8 bis : seules les cartes qui changent ce qu'on VOIT ont un cas
  plateau ; le cas commun `hellcat-cartes-accrochees.test.ts` couvre
  l'accroche (vu VERT d'emblée : c'est une couverture, pas un correctif ;
  l'émission moteur est confirmée par `to_descriptor.py:136`).

### hc001a : * Hellcat (héroïne)

- [x] Étape 2 : dd001a (`AfterPlayerPlayedCard` + `paid_resources`), ze011
      (ressource à coût `CostFunc.Custom`), ze014 (`PlaceCardHere`).
- [x] Étape 5 : « a card » → ÉVÉNEMENT (arbitrage utilisateur, notice) ;
      « to a maximum of 3 » → condition ; « Limit twice per round » → deux
      Response `LimitOncePerRound` + condition « pas déjà accrochée » ;
      « Discard 1 attached card → generate » → coût Custom + `conditions`
      (sinon `UndoRequest`). Résultat : conforme.
- [x] Étape 6 : max 3, twice, 1 ressource : identiques desc/script.
- [x] Étape 7 : « Response : un événement à [mental] joué se retrouve
      accroché » ; « Empowered — défausser une carte accrochée génère un
      [mental] » ; témoin « SANS [mental] imprimé n'est pas accroché ».
- [x] Étape 7 bis : limite OUI. Témoin « LIMITE twice per round : trois
      événements joués, deux accrochés » (chiffre 2). ⚠ « maximum of 3 » non
      mesurable en un round (2 Response + 1 Hedy = 3 exactement, un 4e est
      déjà bloqué par la limite) : assumé.
- [x] Étape 8 bis : OUI (glisse des cartes) → cas plateau commun.

Carte terminée : OUI.

### hc001b : * Patsy Walker (alter-ego)

- [x] Étape 2 : 45156 (`WhenUnitSchemeAgainst(…, Villain, "You")`).
- [x] Étape 5 : « draw 1 card → » = coût, pioche d'abord ; « reduce … by 1 »
      → `GainSCHForThisScheme(-1)`. Conforme.
- [x] Étape 6 : 1 carte, 1 menace.
- [x] Étape 7 : « carte piochée à [mental], 1 menace de moins » (3 → 4 au
      lieu de 5) + témoin « sans [mental], menace pleine » (5).
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc002 : * Iron Man (allié signature)

- [x] Étape 2 : 04032 (`AfterUnitUseBasicPower`), 45016 (`ChooseAbilities`).
- [x] Étape 5 : « once per turn » → une fois par ROUND (arbitrage technique,
      vocabulaire officiel). Conforme.
- [x] Étape 6 : coût 3, 2/2/3, 1 [mental], 2 cartes.
- [x] Étape 7 : « redresse l'identité » (Genius parti, Hellcat prête).
      ⚠ Le second choix (« Draw 2 cards ») n'est pas atteignable : le pilote
      prend toujours la première option. À vérifier en partie réelle.
- [x] Étape 7 bis : OUI. Témoin « deux pouvoirs de base, un seul Genius
      dépensé » (main = 1).
- [x] Étape 8 bis : NON.

Carte terminée : OUI (second choix à voir en partie réelle).

### hc003 : * Cat Suit

- [x] Étape 2 : 05023 (`GiveKeywordToAttached("You", health=3)`), tg006,
      21191 (`UnitIgnoreKeywordIcons(patrol=True, while_use_basic_thw=True)`).
- [x] Étape 5 : « +3 hit points » ; « exhaust and spend → +2 THW and ignore
      patrol ». ⚠ LIMITE ASSUMÉE : Patrouille verrouille la CIBLE avant que
      l'interruption ne soit proposée ; l'ignorance n'aide que si la cible
      était déjà légale (même famille que 15012).
- [x] Étape 6 : +3, +2, 1 [mental].
- [x] Étape 7 : « +3 points de vie » (14) ; « contre de base : incline,
      dépense, +2 CTR » (6 → 2, inclinée, main 0).
- [x] Étape 7 bis : NON (l'inclinaison est la limite naturelle).
- [x] Étape 8 bis : NON.

Carte terminée : OUI (patrouille : limite documentée).

### hc004 : * Hellcat's Claws

- [x] Étape 2 : 10009 (`GiveKeywordToAttached(CardFinder(name=…), attack=1)`),
      10003 (`WhenUnitMakeAttack(is_basic_attack=True)` + `GainATKForThisAttack`),
      `GainPiercing`.
- [x] Étape 5 : « Hellcat gets » → nom propre, face héros. Conforme.
- [x] Étape 6 : +1, +2, 1 [mental].
- [x] Étape 7 : « +1 ATQ et attaque de base +2 perçant à travers Robuste »
      (5 dégâts sur Rhino Robuste, inclinée, main 0).
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc005 : Helluva Punch (×3)

- [x] Étape 2 : dd004 (`OnlyHasColor("B")` + `AttackProperty(overkill=…)`).
- [x] Étape 5 : « an additional 2 » = 6 en un seul appel (déferlement sur le
      total). Conforme.
- [x] Étape 6 : 4, 2, coût 2.
- [x] Étape 7 : « payée uniquement en [mental] : 6 dégâts et déferlement »
      (Hydra Bomber à 2 PV vaincu, 4 sur Rhino) ; témoin « payée en
      [energy] : 4, pas de déferlement » (Rhino intact).
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc006 : On the Prowl (×2)

- [x] Étape 2 : 90119, 15012 (ignorance déclarée), fiche `crisis.md`.
- [x] Étape 5 : « ignores the crisis icon and patrol keyword » →
      `SetIgnoreKeyword('Crisis', 'Patrol', condition=si_payé_mental)` :
      vraie au ciblage (rien de payé), tranchée à la résolution. ⚠ Corrigé
      le jour même : déclarée sans condition, la Crise ne mordait plus jamais
      (témoin rouge). Conforme.
- [x] Étape 6 : 4, 2, coût 2.
- [x] Étape 7 : « payée en [mental] : 6 menaces malgré la Crise » (6 → 0) ;
      « payée en [energy] sans Crise : 4 » (6 → 2) ; témoin « payée en
      [energy] sous Crise : rien ne part » (6).
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc007 : Cat-Like Reflexes (×2)

- [x] Étape 2 : 14014 (`WhenUnitDefendAgainstAttack` + `GainDEFForThisAttack`),
      recherche manuelle (aucun `CardFinder` n'exclut un nom).
- [x] Étape 5 : « not named Cat-Like Reflexes » → filtre par nom. Conforme.
- [x] Étape 6 : +2, coût 1.
- [x] Étape 7 : « +2 DEF, et une carte [mental] remonte de la défausse »
      (Rhino 2 + boost 1 contre DEF 4 : 0 dégât ; main +1). ⚠ Le pilote
      choisit n'importe quelle carte [mental] de la défausse (la main de
      départ y tombe) : mesure par taille de main.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc008 : Illusion (×2)

- [x] Étape 2 : 45016 (`ChooseAbilities` + `ForChoiceAbility` ciblées).
- [x] Étape 5 : « for each card attached to your identity » → cartes
      glissées (pas les améliorations). Conforme.
- [x] Étape 6 : 1 par carte, coût 1.
- [x] Étape 7 : « soigne 1 par carte accrochée : deux accrochées, Hellcat
      regagne 2 » (3 → 1, puis Illusion s'accroche : 3 accrochées).
      ⚠ Le second choix (menace) n'est pas atteignable par le pilote
      (première option toujours) : à vérifier en partie réelle.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON (l'accroche est couverte par hc001a).

Carte terminée : OUI (branche menace à voir en partie réelle).

### hc009 : * Mental Training

- [x] Étape 2 : 28017 Honed Technique (`WhenPlayerPlayCard` +
      `WhenFaceWouldDealDamage` temporaire), `WhenSchemeWouldRemoveThreat`
      (`message.value += 1`, relu après envoi, scheme.py:142).
- [x] Étape 5 : « using ONLY » → `OnlyHasColor("B")` en condition (28017 se
      contente de `using_res`) ; ATTACK ou THWART → conditions (pas de liste
      dans `CardFinder(trait=…)`). Conforme.
- [x] Étape 6 : 1 dégât / 1 menace, coût 2.
- [x] Étape 7 : « Helluva Punch en [mental] : 7 » ; « On the Prowl en
      [mental] : 7 menaces » (8 → 1) ; témoin « payée en [energy] : 4 ».
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc010 : * Outer Demons

- [x] Étape 2 : dd001a (héros villainous), `WhenBoostCardTurnedFaceUp`
      (`boost_for_card`), 10009 (Forced Response après changement de forme).
      Moteur : paramètre `villainous` ajouté à `GiveKeywordToAttached`
      (asset.py, asset_helper.py, environment_helper.py).
- [x] Étape 5 : « gains villainous » → continu ; « cancel its Boost ability.
      Then heal 1 » → `CancelBoostAbility` + soin, `canbe_cancel=None` pour
      que le soin parte même sans effet Boost ; « After you change form,
      discard ». ⚠ ÉCART ASSUMÉ : boost à l'ATTAQUE de base seulement, pas au
      contre (moteur, comme dd001a).
- [x] Étape 6 : 1 soin, coût 2.
- [x] Étape 7 : « attaque de base tire une carte boost, +1 ATQ, soin 1 »
      (Rhino 3, Hellcat 2 → 1, Repair Sequence en défausse de rencontre) ;
      témoin « sans elle, aucune carte boost » ; « changer de forme la
      défausse ».
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : OUI en théorie (carte boost révélée) mais TRANSITOIRE :
      la carte boost passe par la zone de boost puis la défausse pendant la
      résolution, exactement comme pour un ennemi (déjà dessinée). Pas de
      cas plateau propre : à regarder en partie réelle.

Carte terminée : OUI (contre de base : écart documenté).

### hc011 : * Hedy Wolfe

- [x] Étape 2 : ze010 (Alter-Ego Action à coût Exhaust), ze014
      (`Search.PlayerCard(include_player_deck=False, include_discard_pile=True,
      has_printed_res="B")` puis `PlaceCardHere`).
- [x] Étape 5 : conforme.
- [x] Étape 6 : 1 carte, coût 1.
- [x] Étape 7 : « une carte [mental] de la défausse s'accroche » (Genius
      sous Patsy, Hedy inclinée) ; « les cartes accrochées SURVIVENT au
      changement de forme » (la zone est celle de la CARTE).
- [x] Étape 7 bis : NON (inclinaison).
- [x] Étape 8 bis : OUI → cas plateau commun.

Carte terminée : OUI.

### hc012 : * She-Hulk (alliée signature alternative)

- [x] Étape 2 : 28018 (`AfterYouPlayThisFromHand` + `paid_resources`), 01051
      Tigra (`AfterUnitAttackAndDefeatUnit(…, "This", Minion)`), `Gain(effect,
      1, health=n)`.
- [x] Étape 5 : conforme.
- [x] Étape 6 : +1/mental, coût 3, 2/2/3.
- [x] Étape 7 : « +1 PV par [mental] : Genius + Chase Them Down = 6 PV » ;
      « vainc un sbire : un événement [mental] de la défausse revient en main ».
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc013 : Mental Episode (obligation)

- [x] Étape 2 : ag005 (`ChangeToForm(AlterEgo, …)`), `RemoveAllFromGame`.
- [x] Étape 5 : « If not, discard this card » DOIT être codé (une obligation
      révélée entre en jeu et y reste). Conforme après correction.
- [x] Étape 6 : 1 dégât par carte, seuil 2.
- [x] Étape 7 : « deux accrochées : alter-ego, 2 dégâts, RETIRÉE » ; « une
      accrochée : 1 dégât, défaussée » (zone lue sur la carte).
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc014 : Battle for a Soul (manigance annexe)

- [x] Étape 2 : `GiveKeywordToInPlayWhenApplyThis(finder, scheme=1|attack=1,
      get_new_value=fn)` (liste !), `WhenEnemyWouldActivate`, `Enemy.DoActivate`.
- [x] Étape 5 : « +X where X is the number of cards attached to Hellcat » →
      valeur relue à l'application ; « they also activate against the player
      the other is engaged with » → `DoActivate(cible)`, multijoueur.
- [x] Étape 6 : 2 menaces, boost 2.
- [x] Étape 7 : « Daimon gagne +X ATQ » (2 accrochées : 1 + 2 + boost 1 = 4) ;
      témoin sans accrochée (2). ⚠ « +X SCH » de Blackheart : même fabrique,
      même fonction, non mesuré séparément. ⚠ L'Interruption forcée (double
      activation) est MULTIJOUEUR : hors de portée du harnais solo, à
      vérifier en partie réelle à deux.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI (double activation : à voir à deux joueurs).

### hc015 : * Blackheart / hc016 : * Daimon Hellstrom

- [x] Étape 2 : 48033 (`Worlds.GetNextPlayer`), `Minion.EngagePlayer`,
      `ThisCardGainSurge`. Toughness / Stalwart / Villainous : bases auto.
- [x] Étape 5 : « cannot be in the same play area » appliqué à la RÉVÉLATION
      seulement (écart : un déplacement ultérieur n'est pas surveillé).
      « If he cannot, this card gains surge » : en solo, surge + le sbire ne
      reste pas en jeu (insert de l'auteur). Conforme.
- [x] Étape 6 : 4 PV, 1/2 et 3/1, boost 2.
- [x] Étape 7 : hc015 « révélé alors que Daimon est engagé : surge, hors
      jeu » (Repair Sequence semée révélée) ; témoin « révélé seul : entre en
      jeu » ; hc016 symétrique. ⚠ Branche multijoueur (« engages with the next
      player ») hors de portée du harnais solo.
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Cartes terminées : OUI (branche à deux joueurs : partie réelle).

### hc017 : Hot as Hell (×2)

- [x] Étape 2 : 07058 Headbutt, 31001a (`GetControlUpgrade`), `AskChooseFaces`.
- [x] Étape 5 : « an upgrade you control » → choix du joueur ; `GetIdentity()`
      (alter-ego encaisse aussi). Conforme.
- [x] Étape 6 : dégâts = coût imprimé.
- [x] Étape 7 : « Cat Suit (2) défaussée, 2 dégâts » ; témoin « sans
      amélioration, 0 ».
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc018 : * Firestar

- [x] Étape 2 : 28018, 23016 (`CostFunc.Counter("This", 1, 'fire')`), ss012.
      Compteur `fire` ajouté à l'enum COUNTER et à `compteurs-fr.ts` (« feu »).
- [x] Étape 5 : « ★ Interrupt » → Interrupt ordinaire (arbitrage utilisateur).
- [x] Étape 6 : 1 pion/mental, 2 dégâts, coût 3, 1/1/3.
- [x] Étape 7 : « entre en jeu avec 3 pions feu (3 mental) » ; « attaque :
      retire un pion, 2 dégâts en plus » (3 sur Rhino, pion 1 → 0).
- [x] Étape 7 bis : NON (les pions sont la limite).
- [x] Étape 8 bis : OUI (compteur) → couvert par la jauge de compteurs
      existante (`compteurs`), libellé « feu » ajouté.

Carte terminée : OUI.

### hc019 : * Captain Marvel (Monica Rambeau)

- [x] Étape 2 : `WhenUnitUseBasicPower(Interrupt, "This")`, `CostFunc.Spend`
      (`return_res`), ze014, `Faces.ShuffleAllTo`.
- [x] Étape 5 : « matching printed resource » → couleur de la ressource
      DÉPENSÉE, lue sans conversion du joker. Conforme.
- [x] Étape 6 : 1 ressource, coût 3, 2/2/3.
- [x] Étape 7 : « dépense 1 ressource, une carte de même couleur remonte de la
      défausse dans le deck » (deck vide → 1 ; le Genius dépensé est lui-même
      candidat, mesure par taille).
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc020 : Green Hell / hc021 : Hell-Iron

- [x] Étape 2 : 14018 (`.SetTarget("TeamUp")`, EXIGÉ par le chargeur),
      45016 (`GainUntilPhaseEnd(attack=2)`), ze001b (recherche deck+défausse).
- [x] Étape 5 : « Ready X and Y » → cibles TeamUp ; « until the end of the
      phase ». Conforme.
- [x] Étape 6 : +2, coût 1 / coût 1.
- [x] Étape 7 : hc020 « redresse les deux, +2 ATQ » (attaque 4) + témoin
      « sans She-Hulk, injouable » ; hc021 « redresse les deux, une
      amélioration du deck en main ».
- [x] Étape 7 bis : NON (Max 1 per deck : desc).
- [x] Étape 8 bis : NON.

Cartes terminées : OUI.

### hc022 : Divas

- [x] Étape 2 : `conditions=` maison (« any 2 of 4 » inexprimable en
      `desc.TeamUp`), `AskChooseFaces` ×3, `AddToHand`, `ShuffleAllTo`.
- [x] Étape 5 : « each with a different printed resource » → trois choix
      successifs, couleur prise retirée. Conforme. ⚠ Le deckbuilder n'applique
      aucune restriction Team-Up à cette carte (écart).
- [x] Étape 6 : 3 cartes, 1 en main, coût 0.
- [x] Étape 7 : « deux divas en jeu : trois couleurs, une en main, deux au
      deck » ; témoin « Hellcat seule : injouable ».
- [x] Étape 7 bis : NON.
- [x] Étape 8 bis : NON.

Carte terminée : OUI.

### hc023 : Chase Them Down (reskin) / hc024-hc026 : Energy, Genius, Strength (reskins)

- [x] Étape 2 : hc023 = copie ligne à ligne de core/01052.py ; ressources :
      aucun module (comme 01088-01090).
- [x] Étape 5/6 : textes identiques aux officielles.
- [x] Étape 7 : hc023 « après que Hellcat vainc un ennemi, 2 menaces en
      moins » (5 → 3). Ressources : payantes dans une dizaine de cas du pack
      (hc024-026 ne sont pas dans les cas : les officielles y jouent leur
      rôle, mêmes `desc`).
- [x] Étape 8 bis : NON.

Cartes terminées : OUI.

## Bilan substitution / autoplay

(rempli après exécution, voir ci-dessous)
