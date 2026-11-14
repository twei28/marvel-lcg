# Lot GS-8 : gabarits PROCESSUS-CARTE (Supreme Intelligence, Starforce, Seeds of Corruption, Nega-Bomb)

Mesures du 20/10/2026, copie `gs8-supreme-intelligence`. Cas : `tools/cas/gs8_supreme_intelligence.py` (75 cas `[gs8]`, 75/75 verts a la derniere passe). Substitution : `tools/substituer_pack.py <gd> <port> gs` (31/31 cartes a module ont au moins un cas rouge sans leur module ; empreinte md5 du pack identique avant/apres). Static : `verifier_appels_modules.py galactic_storm` OK (calibre : un appel inexistant plante dans gs206 a ete vu), `verifier_api_cartes.py` : aucune faute dans galactic_storm. Questions ouvertes : `.planning/todos/2026-10-20-gs8-questions.md`. Moteur : `defs/supreme_intelligence_moteur.md`.

### gs195 : Supreme Intelligence (I)

- [x] Etape 2 : cartes de reference : sk179, fne/kingpin ReponseForceeSoutien (AfterUnitBeDefeated), sf011 (boost), nt008 (soin)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « a KREE minion », « AFTER ... defeated », « if THAT minion has the ELITE trait » (trait gagne compris : EtaitElite), « heal ... the VILLAIN ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 13*, SCH 2, ATK 1, Stage 1 ; soin 1, 1 carte de boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Infantry non ELITE (soin, 0 boost) ; Ronan ELITE (soin + 1 boost) ; Infantry ELITE par gs201 (boost) ; contre-cas non KREE.
      Substitution : 3/4 rouges (vert : le contre-cas non KREE, absence assumee).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs196 : Supreme Intelligence (II)

- [x] Etape 2 : cartes de reference : gs195 (meme helper) ; Toughness base desc
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : identiques a gs195 ; Toughness = carte Tenace a l'entree (cas Setup expert). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 14*, SCH 2, ATK 2, Stage 2, Toughness.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : ELITE vaincu (soin + boost), non ELITE (soin seul), Setup expert (Tenace, 14 PV).
      Substitution : 2/2 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs197 : Supreme Intelligence (III)

- [x] Etape 2 : cartes de reference : gs195 sans condition
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « give IT » = le mechant, aucune condition de trait. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 15*, SCH 3, ATK 2, Stage 3, Toughness.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Infantry non ELITE vaincu : soin + boost, PV 15.
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs198a : Protectors of the Kree Empire (1A)

- [x] Etape 2 : cartes de reference : next_evol/40139a, gmw/16082a (SetupCards.SetAsideCards), aos/50104b (RandomChoice), gmw/16107a (AttachTo2)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH STARFORCE minion » (Supremor compris, Q1), « 1 of THEM at random », « FIRST player », « Attach Holding Tank to the VILLAIN ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Stage 1 ; 10 STARFORCE -> 9 de cote, 1 en jeu ; Tank 7*.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Setup (9 de cote, 1 en jeu, Tank attache, 7 pions) ; Setup expert ; Setup a 2 joueurs (14 pions, 26 PV).
      Substitution : 3/3 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI (mise de cote, attachement) : couvert par le cas plateau de gs200 (Tank attache) ; la mise de cote des sbires se voit dans la reserve du scenario (chemin existant, non teste au plateau).

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs198b : Protectors of the Kree Empire (1B)

- [x] Etape 2 : cartes de reference : aos/50104b, paibok/sk145b, gmw/16082b (Advance) ; AJOUT moteur pour l'objectif fige
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « INSTEAD », « remove ALL threat from HERE » (Crise ignoree, Q7), « RANDOM set aside », « THEN, if 5 OR LESS », « advance to 2A ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : objectif 6 (fixe), escalade 2 (fixe), depart 0 ; seuil <= 5.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : complete -> 0 menace, 9 -> 8 de cote ; 6 de cote -> avance 2B ; objectif atteint par pose : sbire en jeu AVANT l'avance (discriminant) ; objectif fige (+3 ignore) ; temoin 2B (11 -> 14).
      Substitution : 2/5 rouges par substitution du module (verts : 6->2B, indiscernable sans module car 1B s'acheve vers 2A, d'ou le cas discriminant ajoute et vu rouge ; objectif fige porte par le MOTEUR : vu rouge ligne moteur neutralisee « 9 au lieu de 6 » ; temoin 2B, absence assumee).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs199a : The Endless Mind (2A)

- [x] Etape 2 : cartes de reference : falcon/53033 (ShuffleAllTo), aos/50104b (mis de cote)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH set aside STARFORCE », « INTO the encounter deck ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Stage 2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : revelee : 9 de cote -> 0, 9 dans le deck rencontre.
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI (deplacement de zone vers le deck) : chemin existant, non teste au plateau.

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs199b : The Endless Mind (2B)

- [x] Etape 2 : cartes de reference : regle moteur « If this stage is completed, the players lose the game » (scheme_main.py, lue dans le texte)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : coquille « completes » traitee comme « completed » (decision GS-0 Q4) ; aucun script. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : depart 1*, escalade 1*, objectif 11*.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : 11 menaces -> partie perdue ; temoin objectif 11 -> 14.
      Substitution : AUCUN MODULE (regle native) : pas de substitution possible ; le cas mesure la defaite.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs200 : Holding Tank

- [x] Etape 2 : cartes de reference : next_evol/40156 (ReduceCharacterTakeDamageBy), dt128 (AfterUnitTookDamage Enemy), uses.md
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the VILLAIN », « from EACH ATTACK », « an ENEMY takes ANY amount » (0 = rien), « from HERE » ; Victory 0 defaussee (Q4). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : Uses 7*, reduction 2, 1 pion.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : attaque 2 -> 0, aucun pion ; 3 degats hors attaque -> 3 et 6 pions ; sbire touche -> 6 pions ; dernier pion -> parti, attaque suivante entiere.
      Substitution : 4/4 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI. Cas plateau `ui-app/src/board/supreme-intelligence-plateau.test.ts` : Holding Tank dessine, porte par le mechant, pions « intégrité » ; VU ROUGE avant l'ajout `integrity: 'intégrité'` dans `compteurs-fr.ts` (libelle brut), vert apres.

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs201 : Genetic Augmentation

- [x] Etape 2 : cartes de reference : jubilee/47026 (meme phrase), hercules/59002 (ELITE), sk232 (ATK+)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « the KREE minion », « MOST REMAINING », « Otherwise surge », « +2 hit points AND ELITE ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : ATK+ 1, +2 PV, 1 icone de boost, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : s'attache a Infantry (5 restants > Ren-Varr 2), 7 PV, ELITE, ATK 3 ; sans KREE -> Renfort.
      Substitution : 2/2 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI. Meme fichier : Genetic Augmentation dessinee, portee par Kree Infantry (attachement a un sbire engage : chemin d'affichage EXISTANT, le cas n'a pas ete vu rouge faute de correctif a ecrire).

Carte terminee : OUI

### gs202 : Kree Infantry

- [x] Etape 2 : cartes de reference : sm/sandman/27067 (WhenDefeated), 50134 (PlaceThreatOnSchemes MainScheme)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « on the MAIN scheme », « 2 » fixe. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 5, SCH 1, ATK 2, Guard, Patrol, 1 boost, x4 ; 2 menaces.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : vaincu -> 2 menaces sur 1B ; Garde et Patrouille portees.
      Substitution : 1/2 rouges (vert : mots-cles desc, aucun module par nature).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs203 : Ren-Varr

- [x] Etape 2 : cartes de reference : 27067, next_evol/40156 (Tough au mechant)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « When DEFEATED » (Vulnerable defausse != vaincu). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 5, SCH 2, ATK 1, Vulnerable, Acceleration, 2 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : vaincu -> mechant Tenace ; etourdi -> defausse, pas de Tenace.
      Substitution : 1/2 rouges (vert : contre-cas Vulnerable, absence assumee).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI (statut Tenace/Sonne pose) : chemin d'affichage natif des cartes d'etat, non teste au plateau.

Carte terminee : OUI

### gs204 : Supremor

- [x] Etape 2 : cartes de reference : mts/hela/21137a (ThisGainKeyword + OnEvent.Victory), aos/50127 (VictoryDisplay.FindCardSize)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH KREE MINION », « in the VICTORY DISPLAY », suivi continu (gs207 en retire). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 3 (★ = renvoi), +1 par sbire, Villainous, 2 boost, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : 2 Starforce en vitrine -> 5 PV ; Ronan vaincu apres l'entree en jeu -> 4 PV.
      Substitution : 2/2 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (PV seulement).

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs205 : Loyalty to Supremor

- [x] Etape 2 : cartes de reference : cw/56111 (meme phrase)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH minion » (pas seulement KREE). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : menace 3*, Acceleration, 1 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Ren-Varr gagne Garde.
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs206 : Selective Breeding

- [x] Etape 2 : cartes de reference : falcon/53033
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH KREE MINION », « from the encounter DISCARD PILE ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : menace 6 (fixe), Amplify, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : 2 Infantry rejoignent le deck, Hydra Mercenary reste.
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs207 : Supremor Seed

- [x] Etape 2 : cartes de reference : sk271 (WhenSchemeBeDefeated + defeating player + MayChooseOneAbility), aos/50127
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « The DEFEATING player », « MAY », « 1 KREE MINION », « FROM ... IN » (deplacement). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : menace 4*, Hazard, 2 boost, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : dejoue -> Ronan vitrine -> defausse ; refus « Cancel » -> reste ; Ronan retire -> le bonus +1 ATK tombe (cas gs214 TEMOIN).
      Substitution : 1/2 rouges (vert : refus, absence assumee).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs208 : Summon Reinforcements

- [x] Etape 2 : cartes de reference : standard_skrull/sk257 (DoSchemes), baxter/tx009 + sk233 (DiscardEncounterCardsUntil + Reveal)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AT LEAST 1 ... SET ASIDE », « the VILLAIN schemes », « Otherwise », « REVEAL it ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 2 boost, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : STARFORCE de cote -> 2 menaces sur 1B ; aucun -> Infantry revelee.
      Substitution : 2/2 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs209 : Cadmi-M the Pursuer

- [x] Etape 2 : cartes de reference : next_evol/40006 (works_in_the_victory_display)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « WHILE ... in the victory display », « gains retaliate 1 ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 1, ATK 1, Retaliate 1, Villainous, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : vaincu -> Rhino Riposte 1 ; temoin en jeu -> 0.
      Substitution : 1/2 rouges (vert : temoin hors vitrine).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs210 : Doctor Minerva

- [x] Etape 2 : cartes de reference : 40006
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « +1 SCH ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 2, ATK 1, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : vaincu -> Rhino SCH +1 (ATK inchangee).
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs211 : Inndig-O the Accuser

- [x] Etape 2 : cartes de reference : 40006
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « +1 ATK », cumul avec Ronan. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 1, ATK 2, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : vaincu -> ATK +1 (SCH inchange).
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs212 : Korath the Pursuer

- [x] Etape 2 : cartes de reference : gs209
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : cumul : Riposte 2. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 1, ATK 1, Retaliate 1, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Cadmi-M + Korath vaincus -> Riposte 2.
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs213 : Protector

- [x] Etape 2 : cartes de reference : 40006 (steady=1)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « gains STEADY ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 1, ATK 1, Steady, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : vaincu -> Rhino Solide ; Protector Solide (desc).
      Substitution : 1/2 rouges (vert : Steady imprime, base desc).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs214 : Ronan the Accuser

- [x] Etape 2 : cartes de reference : gs211
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : cumul +2 ; le bonus tombe quand Supremor Seed le retire. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 1, ATK 2, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Inndig-O + Ronan -> +2 ATK ; retire par gs207 -> ATK imprimee.
      Substitution : 1/2 rouges (vert : temoin de retrait, absence assumee).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs215 : Shatterax

- [x] Etape 2 : cartes de reference : 27078 / ho016 (UnitAttackGainKeyword), helper AttaquesDuMechantEnVitrine (NoOutOfPlayLimit)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « SHATTERAX's attacks » / « the VILLAIN's attacks » en vitrine. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 1, ATK 1★, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : attaque propre sur alter ego Tenace : Tenace defaussee + 1 degat ; en vitrine Rhino : 2 degats malgre la Tenace ; temoin 0.
      Substitution : 2/3 rouges (vert : temoin).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs216 : Ultimus

- [x] Etape 2 : cartes de reference : gs215, 27078
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « ULTIMUS's attacks » / « the VILLAIN's attacks » : Deferlement. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : HP 8, SCH 1, ATK 1★, Victory 1, 3 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : en vitrine : exces 1 sur Spider-Man ; attaque propre (ATK 2 avec gs201) : exces 1 ; temoin 0.
      Substitution : 2/3 rouges (vert : temoin).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs217 : Starformation

- [x] Etape 2 : cartes de reference : ares/ar014 (boost a chaque sbire), next_evol/40156 (Tough)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH STARFORCE minion » (en jeu), « AND », « Otherwise » -> mechant. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Ronan en jeu : Tenace + 1 carte de boost (pas le mechant) ; aucun : mechant Tenace + 1 boost.
      Substitution : 2/2 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI (statut Tenace/Sonne pose) : chemin d'affichage natif des cartes d'etat, non teste au plateau.

Carte terminee : OUI

### gs218 : Manipulated Memories

- [x] Etape 2 : cartes de reference : agatha_harkness/aa018 (attachement + regle de cout + Action + boost during_scheme), sm/27181 (same_type), requirement.md
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOUR identity », « EACH EVENT in YOUR HAND » (allie non touche), requirement INCLUS dans le cout (Q6), « SAME TYPE », Boost manigance/sinon. Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 2 ressources ; 1 boost + ★, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Haymaker avec Strength : reste en main ; temoin sans attachement : 3 degats ; avec Genius : 3 degats ; Hulk (allie) entre en jeu ; Action -> defaussee ; Boost manigance -> Desoriente ; Boost attaque -> Sonne.
      Substitution : 4/7 rouges (verts : temoin sans attachement, paiement mental et allie = absences d'effet assumees).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI. Meme fichier : Manipulated Memories dessinee, portee par l'identite (chemin existant, pas vu rouge).

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs219 : Psychic Shackles

- [x] Etape 2 : cartes de reference : iron_patriot/ip035 (PlayersCannotPlayCardWhile + HasColorPrinted)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « PLAYERS », « cannot PLAY », « PRINTED [mental] ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : menace 3 + Hinder 1* = 4, 2 boost.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Maria Hill reste en main (menace 4) ; Hulk se joue ; sans le complot Maria Hill se joue.
      Substitution : 1/3 rouges (verts : deux temoins).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs220 : Mental Torture

- [x] Etape 2 : cartes de reference : wolv/35037 (DiscardRandomHandCards), ip035
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « 1 RANDOM », « IF a [mental] ... THIS WAY », « stun YOUR IDENTITY » (Q5). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 carte, 1 boost, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Genius defausse -> Sonne ; Strength defausse -> rien.
      Substitution : 2/2 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI (statut Tenace/Sonne pose) : chemin d'affichage natif des cartes d'etat, non teste au plateau.

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs221 : Whisper in the Mind

- [x] Etape 2 : cartes de reference : sm/27135 Loose Ends (Search.SearchForCard obligation_give_to + Reveal / surge)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « YOUR obligation », « a COPY », « If ... NOT revealed ... SURGE », Boost « victory display OR removed » (Q2). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 1 boost + ★, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Eviction Notice trouvee et revelee ; introuvable -> Renfort ; obligation EN COURS de revelation non trouvee -> Renfort (regression autoplay : vue ROUGE sans le correctif, verte avec) ; Boost vitrine -> deck ; Boost retiree -> deck.
      Substitution : 4/4 rouges (substitution avant le cas de regression ; ce dernier vu rouge a la main, correctif retire).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)

### gs222a : Nega-Bomb

- [x] Etape 2 : cartes de reference : raphael/tr014 (AfterResolveVillainPhaseStep 1), gmw/16034 (ThisEnterPlayWithCounters), mut_gen/32065a (Flip)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « AFTER resolving step ONE », « remove 1 ... If NO time counter », « flip AND REVEAL » (le retournement revele deja : un Reveal en plus revelait deux fois, constate au journal). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : menace 8*, Setup, Victory 0, 4 pions time.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Setup : en jeu, 8 menaces, 4 pions ; phase du mechant : 4 -> 3 ; dernier pion -> Detonation.
      Substitution : 2/2 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : OUI. Meme fichier : Nega-Bomb complot annexe dessine avec ses pions « temps » (chemin existant, pas vu rouge).

Carte terminee : OUI

### gs222b : Detonation

- [x] Etape 2 : cartes de reference : luke_cage/62028 (DamageProperty ignore_tough), 40110 (GetControlCharacters)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH friendly character AND minion », « X = threat HERE / nombre (ROUNDED UP) », « IGNORING tough », « Remove from the game ». Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 7 menaces / 3 cibles -> 3.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Spider-Man (Tenace) 3 degats, Black Cat et Hydra Mercenary vaincus, Detonation retiree.
      Substitution : 1/1 rouge.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI

### gs223 : Green Interference

- [x] Etape 2 : cartes de reference : aos/50029, all-purpose-counter.md (FAQ), 27135 (surge)
- [x] Etape 5 : texte-contre-code : mots-pieges verifies : « EACH card in play », « 1 », « IF NO counter -> SURGE », Boost « A card » (Q3). Texte relu contre le SCAN (pas seulement la transcription).
      Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : 2 boost + ★, x2.
      Resultat : identiques dans cards.json (desc), le script et le scan.
- [x] Etape 7 : cas test_capacites : Nega-Bomb 4 -> 3 et sbire 2 -> 1 ; aucun compteur -> Renfort ; Boost : Nega-Bomb 4 -> 3.
      Substitution : 3/3 rouges.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : 48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B (partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree.
- [x] Etape 8 bis : NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs).

Carte terminee : OUI (lecture provisoire, question ouverte : voir le fichier de questions)
