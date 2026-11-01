# Hellfire Hunt, scénario 5 « Cassandra Nova » (Dipsome), préfixe `hf` : gabarits PROCESSUS-CARTE

Worktree `Marvel-LCG-campagnes`, branche `campagnes-fanmade`. Pack `hellfire_hunt_cassandra_nova` (set 245) : scénario hf601-hf621, modules Mind Control hf371-hf376 et Mutant Extinction Agenda hf381-hf388 (38 cartes).
Scénarios : `hellfire_cassandra_nova` (standard : Nova I puis II) et `hellfire_cassandra_nova_expert` (Nova II puis III). Cas : `tools/cas/hellfire_cassandra_nova.py` (noms `[hf] hf6.. / hf37.. / hf38..`, vérificateur `hfn_etat`).
Génération : `docs/packs/hellfire-hunt-cassandra-nova/generer_donnees.py` (données + images), `textes_fr.py` (textes français), `campagne.py` (fichier de campagne), `substitution.py` (preuve par substitution), ce fichier par `generer_gabarits.py`.
Le module **Immensity** (hf351-hf358) est porté par l'agent de Torn : le scénario le référence par `hf_immensity`.

## Ce qui est fait et ce qui reste (honnête)

- Chaque carte : entrée `cards.json`, script, image (`assets/pics/<id>.jpg`, petit côté 615 px, q88), au moins un cas SUJET vert, preuve par substitution lue ci-dessous, texte français (`textes-fr-fanmade.ts`).
- **Aucune carte n'est « terminée : OUI »** : une vraie partie jouée par un humain dans le navigateur n'a pas été faite (aucun outil ne remplace ce juge). Voir « Autoplay » pour ce que le pilote a joué.
- Doutes de règle : `QUESTIONS.md` (7 entrées, choix provisoires codés).

## Autoplay (étape 8)

`tools/autoplay.py` (jeu de travail `.game-src-hfn-snap`, profil `equilibre`, 01/11/2026) : **20 parties**, journaux `/tmp/autoplay_<deck>_<scenario>_normal_equilibre_<graine>.log`.

| Deck | Scénario | Parties | V / D | Rounds moyens | Bloquées (`!`) | Tracebacks (grep exhaustif NameError/AttributeError/TypeError/KeyError/AssertionError/Traceback) |
|---|---|---|---|---|---|---|
| `sunspot_hellfire` | `hellfire_cassandra_nova` (standard) | 4 | 0 / 4 | 4,8 | 0 | 0 |
| `sunspot_hellfire` | `hellfire_cassandra_nova_expert` | 4 | 0 / 4 | 4,8 | 0 | 0 |
| `spider_man` (TÉMOIN) | `hellfire_cassandra_nova` | 4 | 0 / 4 | 4,8 | 0 | 0 |
| `spider_man` (TÉMOIN) | `hellfire_cassandra_nova_expert` | 4 | 0 / 4 | 4,0 | 0 | 0 |
| `sunspot_hellfire`, EN MODE CAMPAGNE (`AUTOPLAY_REGLES=mode_campaign`, carnet `Recruited Allies = hf013;hf014;hf025`) | standard + expert | 2 + 2 | 0 / 4 | 2,5 / 4,0 | 0 | 0 (Rally the Survivors présente dans les journaux : la mise en place de campagne tourne) |

- Taux de blocage identique au témoin (0 partout) : le scénario ne fige aucune partie. Les défaites viennent du complot principal complété (11 parties sur 20) ou de l'élimination des joueurs (9 sur 20) : le pilote est une heuristique et le scénario est dur (3 compteurs → Cassandra Domination, escalade par joueur) ; **aucune victoire en autoplay**, la victoire est prouvée par cas (`hf602 VICTOIRE`, `hf603 VICTOIRE (expert)`).
- Journal lu (partie `sunspot_hellfire` standard, graine 1) : mise en jeu de Cassandra Domination au Setup, compteurs posés après chaque activation, Domination déclenchée (3 retirés, 2 menaces sur chaque manigance choisies par le pilote), Hero Action du complot utilisée, `Take_2_damage` choisi à la fin de tour, avancée vers Silent Takeover ; aucune ligne d'erreur.

## Cartes

### hf371 : Psychic Aegis (Mind Control, attachement)

- [x] Étape 2 : carte(s) de référence : 16149 Power Stone (Setup + `AttachToFaceWhenPutIntoPlay(Villain)`), mt012 (`UnitCannotBeConfused`), sk147 (Cost("BB") + `PlayerActionToDiscardThis`), `PlayersCannotDamageUnit`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `Setup` natif ; `attached character cannot be confused` ; `damage from a player while that player is confused` (initiateur = joueur) ; `Action` (pas Hero Action : alter-ego possible) ; [mental][mental] = `BB` (verifie sur hf110) ; Boost etoile = reveler.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf371.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Setup 1, coût BB : cas (Action payee par 2 Genius).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf371` x7 (mise en place, non-desorientation + temoin, degats bloques + temoin, Action, Boost).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 6/8 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement posé sur le VILAIN : `ui-app/src/board/cassandra-nova-plateau.test.ts` (dessinée, `portePar` = Nova) + table vue dans Chromium (`captures/cassandra-nova-voiles/voile-psychic-aegis.png`). Aucun correctif nécessaire : le plateau la dessinait déjà (cas écrit après coup, pas de ROUGE à montrer).

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf372 : False Reality (Mind Control, attachement)

- [x] Étape 2 : carte(s) de référence : sk147 (Hero Action BB), sk194 / `WhenSchemeWouldRemoveThreat`, ar007 (`LimitOncePerPhase`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : MOTEUR additif `PreventRemoval` ; `that player` (controleur du personnage qui contre) ; `Then` : desorientation APRES ; `once per phase` (temoin d'epuisement) ; Hero Action.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf372.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Prevention 2, coût BB : cas (Jessica Jones THW 2 : 3 reste 3 ; temoin sans carte : 3 -> 1).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf372` x4 (nominal, temoin, EPUISEMENT, Action).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 3/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? OUI : `hf372 TEMOIN D'EPUISEMENT` (second retrait de la phase non empeche : 3 -> 2)
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement posé sur le COMPLOT PRINCIPAL : même test (`portePar` = complot) ; aucun correctif nécessaire.

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf373 : Mind Maze (Mind Control, attachement)

- [x] Étape 2 : carte(s) de référence : sk147 (`WhenUnitWouldThwart(ForcedInterrupt, "AttachedIdentity")`), `message.SetBeInstead`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `When YOU thwart` (l'identite, pas un allie : temoin) ; `instead` (le contre n'a pas lieu) ; `Then, you are confused` ; Action BB.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf373.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Coût BB : cas.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf373` x4 (remplacement, attache, temoin allie, Action).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 4/4**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : attachement posé sur l'IDENTITÉ : même test (`portePar` = identité) ; aucun correctif nécessaire.

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf374 : Illusory Attacks (Mind Control, traiterie 1/2)

- [x] Étape 2 : carte(s) de référence : mt011 (`IsConfused` sur personnages amis ET ennemis).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `each confused character in play` (amis de tous les joueurs ET ennemis) ; `You are confused` AVANT les degats.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf374.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Boost 1 + etoile ; 1 degat : cas (identite 1, Black Cat 1, Hydra Bomber 1, Jessica 0).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf374 Illusory Attacks` + Boost.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 2/2**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf375 : Illusory Attacks (2/2)

- [x] Étape 2 : carte(s) de référence : = hf374.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf374.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf375.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf374.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf375 Illusory Attacks (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf376 : Mind Shatter (Mind Control, traiterie)

- [x] Étape 2 : carte(s) de référence : `Player.DiscardHandCards((0, "All"))`, Peril natif.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : QUESTIONS.md n°2 (main apres defausse, moitie arrondie au superieur) ; `each identity in play` (2 joueurs : [1, 1]) ; main vide : 0.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf376.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Peril 1, boost 1 : cas (main de 4 -> 2 degats ; 3 -> 2 ; 0 -> 0 ; 2 joueurs -> 1 chacun).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf376 Mind Shatter` x4.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 3/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf381 : Mutant Extinction Agenda (manigance annexe)

- [x] Étape 2 : carte(s) de référence : 27142 (boost `PutThisIntoPlay`), `GiveKeywordToInPlayWhenApplyThis(<finder>, attack=1, scheme=1)`, `SchemeCannotLeavlPlayWhile` (defeated.py).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `each SENTINEL minion` (temoin Hydra Bomber) ; `cannot be defeated while` + etat coince (QUESTIONS.md n°5) ; `Victory 1` natif (pile de victoire : cas) ; `in player order` ; boost = mettre en jeu SANS When Revealed.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf381.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Menace 2[per_hero], Victory 1, boost 1 : cas (menace 2 ; Wild Sentinel ATK 3, SCH 2).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf381` x7 (When Revealed + bonus, temoin non-SENTINEL, defaite remplacee, temoin sans SENTINEL + Victory, Boost, derniere SENTINEL partie, temoin menace restante).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 3/7 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
      Lecture des verts : Les cas verts sans module : temoin non-SENTINEL, temoin sans SENTINEL (+ Victory natif), temoin menace restante, ET « la DERNIERE SENTINEL part -> manigance vaincue » (la manigance etant deja vaincue a 0 menace sans le module, le cas ne distingue pas : seule la moitie « reste en jeu » est PROUVEE par substitution ; l'autre moitie est exercee, pas prouvee).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf382 : Wild Sentinel (sbire, 1/4)

- [x] Étape 2 : carte(s) de référence : sl033-sl034 (`WhenUnitBeDefeated(WhenDefeated, "This")`), 39015b (`WhenCardWouldDiscard` + `SetBeInstead` + `MoveToBottom`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `The defeating player` (pas de joueur vainqueur = pas de choix : temoin) ; `instead of the discard pile` (jamais dans la defausse : cas negatif) ; `take 2 damage` (a l'identite du vainqueur).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf382.jpg`).
- [x] Étape 6 : nombres texte ↔ code : PV 4, ATK 2, SCH 1, boost 3 : cas `hf382 Wild Sentinel : valeurs imprimees`.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf382` x4 (valeurs, 2 degats, dessous du deck, vaincue sans joueur).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 2/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf383 : Wild Sentinel (2/4)

- [x] Étape 2 : carte(s) de référence : = hf382.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf382.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf383.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf382.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf383 Wild Sentinel (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf384 : Wild Sentinel (3/4)

- [x] Étape 2 : carte(s) de référence : = hf382.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf382.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf384.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf382.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf384 Wild Sentinel (illustration 3)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf385 : Wild Sentinel (4/4)

- [x] Étape 2 : carte(s) de référence : = hf382.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf382.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf385.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf382.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf385 Wild Sentinel (illustration 4)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf386 : E for Extinction (traiterie ATTACK, 1/2)

- [x] Étape 2 : carte(s) de référence : hf111 (`TakeIndirectDamage`), hf381 (`MettreUneSentinelle`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `for each SENTINEL minion in play, deal 1 indirect damage to each player` (N degats par joueur, repartis par lui) ; sans SENTINEL : cherche et met en jeu engagee.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf386.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Boost 1 : cas (2 SENTINEL = 2 degats ; 0 SENTINEL = recherche).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf386` x2.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 2/2**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf387 : E for Extinction (2/2)

- [x] Étape 2 : carte(s) de référence : = hf386.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf386.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf387.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf386.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf387 E for Extinction (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf388 : Worldwide Sentinel Deployment (manigance annexe)

- [x] Étape 2 : carte(s) de référence : hf381 (`UneSentinelleParJoueur`) ; mots-cles/hazard.md (icone lue sur le scan).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `Each player ... in player order` (2 joueurs : 2 SENTINEL) ; Hazard 1 (icone au centre, une carte penchee a croix) ; Victory 1.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf388.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Menace 3[per_hero] (6 a deux joueurs), Hazard 1, Victory 1, boost 2 : cas.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf388` x1 (2 joueurs).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf601 : Cassandra Nova (I), vilain

- [x] Étape 2 : carte(s) de référence : Reponse forcee apres activation CONTRE le joueur : `AfterEnemyActivatesAgainstYou`, comparable parce que sk255 reagit a l'activation d'un ennemi (attaque ou complot) ; compteur nomme sur l'identite : hg `PoserInfection` (meme geste `Faces.PlaceCountersOn([identite], ...)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `against you` (joueur VISE, pas le joueur courant : cas 2 joueurs) ; `activates` = attaque ET complot (2 cas) ; `This` seulement (temoin sbire) ; `your identity card` = l'identite quelle que soit la forme (cas changement de forme).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf601.jpg`).
- [x] Étape 6 : nombres texte ↔ code : PV 15[per_hero] (`15*`), ATK 1, SCH 2, Stage I : cas `hf604a mise en place` (PV 15, ATK 1, MUMMUDRAI, PSIONIC).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf601 Reponse forcee` x4 (attaque, complot, temoin sbire, deux joueurs) + `hf607 compteur sur l'identite : il reste quand le joueur change de forme`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 3/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : compteurs « Cassandra Controls » sur l'IDENTITÉ : même test (`compteurs.cassandra_controls`) et libellé français `compteurs-fr.ts` (« contrôle de Cassandra »), TÉMOIN vu ROUGE sans l'entrée du libellé ; badge « 2 » vu sur Peter Parker dans Chromium.

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf602 : Cassandra Nova (II), vilain

- [x] Étape 2 : carte(s) de référence : When Revealed sur un vilain : `WhenThisRevealed(None, op)` (01096 Rhino III) ; Steady natif (`desc.Steady`) ; Reponse forcee : hf601.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `each identity` (tous les joueurs, dans l'ordre : cas 2 joueurs = [1, 1]) ; Steady (cle `steady`).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf602.jpg`).
- [x] Étape 6 : nombres texte ↔ code : PV 18[per_hero], ATK 2, SCH 3, Steady : cas `hf602 When Revealed` (solo : PV 18, ATK 2 ; 2 joueurs : PV 36, steady).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf602 When Revealed` x2 (2 joueurs, solo).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 2/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
      Lecture des verts : Le cas VICTOIRE reste vert sans module : « dernier stade du vilain vaincu = victoire » est NATIF ; hf602 est prouve par ses cas When Revealed (compteurs, PV, Steady).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : voir hf601 (compteurs posés sur chaque identité au dévoilement).

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf603 : Cassandra Nova (III), vilain (expert)

- [x] Étape 2 : carte(s) de référence : hf602 + `MainScheme.PlaceAccelerationToken` (hf104b).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `1[per_hero] acceleration tokens` = UN PAR JOUEUR (cas solo 1, 2 joueurs 2) ; `on the main scheme` (le complot COURANT : hf605b en expert) ; Stalwart natif.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf603.jpg`).
- [x] Étape 6 : nombres texte ↔ code : PV 20[per_hero], ATK 3, SCH 3, Stalwart : cas expert 2 joueurs (PV 40, ATK 3, Stalwart, 2 jetons, compteurs [2, 2]).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf603 When Revealed (EXPERT)` x2 (2 joueurs, solo ; compteur de depart du stade II = 1, donc 2 apres le stade III).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 2/3 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
      Lecture des verts : Le cas VICTOIRE (expert) reste vert sans module : natif ; hf603 est prouve par ses cas When Revealed (acceleration par joueur, compteurs, Stalwart).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : voir hf601 (compteurs + jetons d'accélération sur le complot).

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf604a : Diplomatic Sabotage 1A (Setup + mise en place de CAMPAGNE)

- [x] Étape 2 : carte(s) de référence : Retrait de sbires homonymes : hf104a ; environnement mis de cote puis en jeu : `world.aside_deck` (campaign.py) ; mise en place de campagne : `CampaignSetup(5)` (cards.pack.hellfire_hunt.campaign, modele skrull_menace).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `minion named Cassandra Nova` : `Minion.IsType` (le vilain porte le meme nom) ; `In expert mode, advance to stage 2A` : porte par hf604b (voir recette) ; campagne : `WhenCampaignSetup` n'est envoye qu'en mode campagne.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf604a.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Menace de depart (dans hf604b), cases `Contents` / `Setup` : texte seul. Campagne : `tools/epreuves_campagnes.py` bloc hellfire (3 epreuves).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf604a mise en place` (standard), `hf604a mise en place EXPERT`, `hf604a Setup : le sbire ... hf351 ... RETIRE` ; 3 epreuves de campagne `hellfire — ...` (victoire, defaite, expert : PV restants + pion Acceleration).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 4/4**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf604b : Diplomatic Sabotage 1B

- [x] Étape 2 : carte(s) de référence : Reponse forcee de fin de tour d'un complot : sk193b ; Hero Action payee en defaussant le deck de rencontre : gb006b ; `LimitOncePerRoundPerPlayer` : 27065.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `you must choose` (forced=True : pas de choix de passer) ; `take 2 damage` (directs, a l'identite) ; `once per round per player` ; `if there is Cassandra Controls counter on YOUR identity` (le joueur dont le tour finit) ; Hero Action = forme heros seulement.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf604b.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Cible 7[per_hero], escalade +1[per_hero], depart 1[per_hero], 1 menace, 2 degats, 5 cartes : cas (menace 1 -> 2, degats 2, 5 cartes defaussees).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf604b Reponse forcee` x4 (menace, degats, temoin sans compteur, 2 joueurs) + `hf604b Action de heros` x3 (nominal, TEMOIN D'EPUISEMENT, sans compteur).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 5/7 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? OUI : `hf604b Action de heros : TEMOIN D'EPUISEMENT` (2 compteurs au depart, 1 seul retire apres DEUX actions du meme round, 5 cartes defaussees et pas 10)
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf605a : Silent Takeover 2A

- [x] Étape 2 : carte(s) de référence : Recherche du sbire nemesis : hf321 Echoes of Enmity (`Search.EncounterCard(..., is_nemesis=joueur)`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `each player` (boucle sur tous les joueurs) ; `finds` (deck + defausse + zone de cote) ; `engaged with themself`.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf605a.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Texte seul (aucun nombre).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf605a When Revealed` x2 (Vulture nemesis de Spider-Man mis en jeu ; sans nemesis rien ne plante).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/2 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf605b : Silent Takeover 2B

- [x] Étape 2 : carte(s) de référence : hf604b (meme squelette) ; `Player.DealEncounterCards`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `deal yourself 1 facedown encounter card` (a SOI, face cachee, pas revelee tout de suite : cle `distribuees`).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf605b.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Cible 11[per_hero], depart 2[per_hero], 2 menaces, 1 carte, 6 cartes : cas (menace 2 -> 4 ; 1 carte distribuee ; 6 cartes defaussees).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf605b Reponse forcee` x2 (menace, carte distribuee) + `hf605b Action de heros` (6 cartes + temoin d'epuisement).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 3/3**
- [x] Étape 7 bis : limite imprimée ? OUI (meme cas : seconde action tolerante refusee)
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf606a : Mutant Extermination 3A

- [x] Étape 2 : carte(s) de référence : `Player.DealEncounterCards` (hf118).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `each character they control` = identite + allies (cas 1 allie : 2 cartes ; temoin sans allie : 1).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf606a.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Texte seul.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf606a When Revealed` x2.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 2/2**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf606b : Mutant Extermination 3B (dernier stade)

- [x] Étape 2 : carte(s) de référence : hf604b ; gb006b (`IfThisSchemeStageIsCompletedPlayersLoseTheGame`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `When this scheme is completed` ne correspond pas a la phrase LUE par le moteur (« If this stage/scheme is completed ») : capacite posee a la main (vue rouge sans module) ; `discard 1 card from your hand` : le JOUEUR choisit ; main vide -> option retiree.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf606b.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Cible 13[per_hero], depart 3[per_hero], 3 menaces, 1 carte, 7 cartes : cas (menace 3 -> 6, defaite a 13, temoin 12).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf606b Reponse forcee` x3 (menace, defausse, main vide) + `hf606b Action de heros` + `hf606b : complot COMPLETE -> les joueurs PERDENT` + TEMOIN a 12.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 4/6 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
      Lecture des verts : Le cas « complot COMPLETE -> les joueurs PERDENT » reste vert sans module : la regle du dernier stade est NATIVE (`World.AdvanceMainScheme`, « The Final Stage of the Main Scheme was Completed ») ; la capacite explicite est redondante mais fidele au texte imprime.
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf607 : Cassandra Domination (environnement)

- [x] Étape 2 : carte(s) de référence : Seuil sur compteur d'identite : hg `limite_atteinte` (`AfterCounterPlacedOn(..., at_least=)`) ; choix a options dynamiques : mt011 (`ChooseAbilities` + `ForChoiceAbility(condition=)`) ; degats indirects : `Player.AssignDamage`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `at least 3` ; `remove 3` ; `each scheme` (principale ET annexes : cas 1 manigance annexe) ; `another friendly character` (jamais soi-meme ; autres identites comprises : cas 2 joueurs) ; FAQ p.22 : options impossibles retirees (5 cas : allie a 2 PV, aucun ami, deja etourdi, deja desoriente, deux exclusions).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf607.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Seuil 3, retire 3, 2 menaces, 3 degats : cas (menace 1 -> 3 ; 3 degats = Jessica Jones PV 3 vaincue).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf607 Reponse forcee` x3 branches + 5 cas FAQ + 2 joueurs + 2 cas de SEUIL (2 compteurs : rien ; 4 d'un coup : une resolution, il en reste 1) + `hf607 compteur ... forme`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 10/12 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
      Lecture des verts : Verts sans module : le compteur reste apres changement de forme (propriete du moteur) et le seuil de 2 compteurs (absence d'effet).
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : environnement en jeu dès la mise en place (même test + capture Chromium `voile-cassandra-domination.png`) ; libellés des trois branches en français (`vocabulaire-moteur.test.ts`).

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf608 : Exploding Their Head (obligation)

- [x] Étape 2 : carte(s) de référence : Obligation du joueur qui la revele (`GiveTo` vide) : 32099 ; fin de tour : `AfterPlayerTurnEnd(ForcedResponse, "AttachedPlayer")` ; Peril : mot-cle natif (`mots-cles/peril.md`), pose par `WhenPlayerRevealCard`.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `cards you control` (alliés, ameliorations, soutiens) ; `total resource cost is at least 2` (cout imprime) ; `Take 1 damage for each card` ; `Otherwise` (QUESTIONS.md n°1) ; `Then, discard this card` ; `you revealed` (porteur de l'obligation).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf608.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Cout 2, 1 degat par carte : cas (Black Cat cout 2 : 1 degat ; deux ameliorations cout 1 : 2 degats ; cout 1 seul : carte rencontre).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf608 Obligation revelee` + `deux cartes de cout 1` + `Otherwise` + `Peril` (+ temoin sans obligation).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 4/5 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : obligation posée dans la zone du joueur (même test, hf610 ; capture `voile-exploding.png`).

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf609 : Exploding Their Head (2e exemplaire)

- [x] Étape 2 : carte(s) de référence : = hf608.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf608.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf609.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf608.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf609 Exploding Their Head (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf610 : Psychic Control (obligation, 1/3)

- [x] Étape 2 : carte(s) de référence : 32099 (Forced Response + Alter-Ego Action « Exhaust your identity -> discard this card »), hf120 (`villain.DoSchemes`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `Cassandra Nova schemes` (contre le porteur, +2 menaces en solo, + son compteur par sa propre Reponse) ; `Confuse your identity, then, discard` (ordre) ; `Alter-Ego Action` : forme alter-ego seulement (temoin heros).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf610.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Boost 3 : cas `hf610 Boost 3 imprime` (1 + 3 = 4 degats).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf610 Reponse forcee` + `Action d'alter-ego` + TEMOIN forme heros + Boost 3.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 2/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? OUI : obligation posée dans la zone du joueur (même test ; capture `voile-psychic-control.png`).

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf611 : Psychic Control (2/3)

- [x] Étape 2 : carte(s) de référence : = hf610.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf610.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf611.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf610.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf611 Psychic Control (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf612 : Psychic Control (3/3)

- [x] Étape 2 : carte(s) de référence : = hf610.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf610.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf612.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf610.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf612 Psychic Control (illustration 3)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf613 : Shatter Your Mind (traiterie, 1/3)

- [x] Étape 2 : carte(s) de référence : `Worlds.DiscardEncounterCards` (WQ `DefausserEtCompterIcones`) ; `set_name` d'une carte : sp006b.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `double the villain's stage number` (1, 2 ou 3) ; `each time ... is discarded` (un compteur par carte, pose un a un) ; `a Cassandra Nova card` (QUESTIONS.md n°4) ; la carte revelee va elle aussi a la defausse (+1 dans les chiffres).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf613.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Boost 2 : cas (1 + 2 = 3 degats) ; 2 / 4 cartes selon le stade.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf613 When Revealed` x3 (stade I : 2 cartes Nova, temoin 1 seule ; stade II : 4 cartes + Domination) + Boost 2.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 3/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf614 : Shatter Your Mind (2/3)

- [x] Étape 2 : carte(s) de référence : = hf613.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf613.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf614.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf613.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf614 Shatter Your Mind (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf615 : Shatter Your Mind (3/3)

- [x] Étape 2 : carte(s) de référence : = hf613.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf613.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf615.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf613.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf615 Shatter Your Mind (illustration 3)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf616 : Psychic Combo (1/2)

- [x] Étape 2 : carte(s) de référence : `villain.DoActivate(joueur, effect)` (27082, 27136) ; boost d'attaque : ts201 (`would_atk_message.GainPiercing`) ; `GainOverKill` (sender_damage.py).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `activates against you` PUIS `You are stunned` (ordre) ; `this activation is an attack` (forme heros) / `Otherwise` (complot) ; `equals to the number of counters on YOUR identity` lu AVANT la Reponse du vilain.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf616.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Boost 1 (+ etoile) : cas (3 menaces de plus que sans carte = 1 icone + 1 compteur ; overkill : 1 degat d'exces ; piercing : Black Cat Tenace est blessee).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf616 When Revealed` x2 (complot, attaque) + Boost attaque (overkill + TEMOIN) + Boost attaque PIERCING (+ TEMOIN) + Boost complot (+ TEMOIN).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 5/8 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf617 : Psychic Combo (2/2)

- [x] Étape 2 : carte(s) de référence : = hf616.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf616.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf617.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf616.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf617 Psychic Combo (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf618 : Psychic Leech (1/2)

- [x] Étape 2 : carte(s) de référence : `Player.DiscardAllHands` (rend le nombre), `Player.DrawUp("Max")`, `CanHealth.HealHealth` (hf122).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `if you cannot` JUGE CARTE PAR CARTE (cas mixte : 1 degat, 2 cartes = 1 soin + 1 compteur) ; ordre imprime : defausse, pioche, puis soins ; main vide : rien.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf618.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Boost 1 ; 1 degat de soin par carte : cas (5 degats - 2 cartes = 3).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf618 When Revealed` x4 (blessee, sans degat, mixte, main vide).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 3/4 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf619 : Psychic Leech (2/2)

- [x] Étape 2 : carte(s) de référence : = hf618.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : = hf618.
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf619.jpg`).
- [x] Étape 6 : nombres texte ↔ code : = hf618.
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf619 Psychic Leech (illustration 2)`.
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 1/1**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf620 : Global Opinion Controls (manigance annexe)

- [x] Étape 2 : carte(s) de référence : Texte vide : 39064 / bf023 (`GiveKeywordToInPlayWhenApplyThis(Support, treat_as_blank=True)`) ; menace a la revelation : hf125 ; boost : hf124.
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `each support` (de tous les joueurs ; temoin Med Team) ; `in play` (toutes les identites : cas 2 joueurs) ; `your identity card` (joueur vise) ; menace de depart 2 FIXE (pas par joueur).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf620.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Menace 2, boost etoile : cas (2 + 2 compteurs = 4 ; 2 + 3 = 5 a deux joueurs ; boost : 2 + 1 = 3 declenche Domination).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf620 When Revealed` x3 (2 compteurs, temoin 0, 2 joueurs) + `Texte des soutiens VIDE` (+ temoin) + `Boost` (+ temoin).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 4/7 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

### hf621 : The Hate Machine (manigance annexe)

- [x] Étape 2 : carte(s) de référence : 27106 / 27142 (`PlayersCannotAttackWhile`, `PlayersCannotThwartWhile`) ; boost : hf110 (`RevealThisCard`).
- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : `you cannot` = le heros, PAS ses allies (QUESTIONS.md n°7 ; temoin allie) ; `Cassandra Nova` seulement (temoin sbire) ; `at least 1 counter on YOUR identity` (temoin sans compteur).
      Résultat : conforme au scan (relu à l'écran, `assets/pics/hf621.jpg`).
- [x] Étape 6 : nombres texte ↔ code : Menace 2, boost etoile : cas (2 + 1 compteur = 3).
      Résultat : conforme.
- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : `hf621` x9 (menace, attaque bloquee, 3 temoins attaque, thwart bloque, 2 temoins thwart, boost revele).
      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **rouges 4/8 (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)**
- [x] Étape 7 bis : limite imprimée ? NON
- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).
- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (la jauge est couverte)

Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.

