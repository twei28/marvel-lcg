# Aspect TMNT Justice (`uj`, pack `tmnt_aspect_justice`) : gabarits PROCESSUS-CARTE

16/10/2026, branche `aspects-uj`. 40 scans `uj001`-`uj040` (numérotation figée par
`Fusion/marvel-lcg-src/tools/tmnt_aspects_numerotation.tsv`). Scans relus un à un (outil Read sur le PNG).

## Preuves communes (valent pour toutes les fiches ci-dessous)

- **Cas** : `Fusion/marvel-lcg-src/tools/cas/tmnt_aspect_justice.py`, filtre `[uj]` : **126/126 verts**
  (passe finale, `PARALLELES=6`, ports 32800+). Régression `[rampage]` 6/6 et `[reskin]` 11/11 verts.
- **Substitution, une seule passe pour tout le pack** : les 19 modules `uj0*.py` retirés du dossier ET
  l'`ability_link` retiré des 20 reskins (`entrees.py sans_lien=...`), même filtre : **61 cas rouges,
  60 verts**. Les 60 verts sont TOUS attendus et listés : les 24 TÉMOINS sur les officielles, les cas de
  DONNÉES (bandeaux `unique_also` ×17, Max 1 per player uj007, limite par round uj024, MYSTIC uj040,
  Toughness uj012) et les CONTRE-CAS d'absence d'effet (uj004, uj005 ×2, uj006/uj009 Tenace, uj016 ×2,
  uj018 refus, uj019 témoin, uj020, uj026 plafond, uj028 ×2 témoins, uj033, uj034 allié, uj037). Toute
  capacité a au moins un cas qui ROUGIT sans son module / son lien. Ajoutés après cette passe : 4 cas
  Zebulon (substitution à part : 3 rouges sans `uj039.py`, le contre-cas « mis en jeu par effet » vert) et
  le cas « THEN » de Mona Lisa (rouge avec l'ancien module, voir uj020).
- **Données** : `test_cards.py` sur tout le catalogue (port 33300) : 6601 cartes construites, 0 erreur.
  `verifier_appels_modules.py ... tmnt_aspect_justice` : « OK », CALIBRÉ (un appel inexistant planté dans
  uj027 a été vu : « 1 appel(s) inexistant(s) », puis retiré). `verifier_prefixes.py` : OK.
- **Autoplay** (étape 8) : contre Rhino, normal, profil équilibré, Spider-Man avec 25 cartes Justice TMNT :
  deck A (cartes scriptées, `scratchpad/uj/deck-uj-A.json`) 8 parties : 1 V / 7 D, 8,4 rounds ; deck B
  (reskins, `deck-uj-B.json`) 8 parties : 0 V / 8 D, 6,9 rounds ; TÉMOIN Spider-Man de départ 8 parties :
  0 V / 8 D, 6,9 rounds. Blocages (« ! ») : 0 / 0 / 0. Seconde fournée deck A après le correctif de Mona
  Lisa (graines 11-18) : 0 V / 8 D, 6,1 rounds, 0 blocage. Grep `NameError|AttributeError|TypeError|
  KeyError|AssertionError|Traceback` sur les 32 journaux : **0 partout**. Le deck A et le témoin sont au même
  niveau (pilote heuristique, Spider-Man contre Rhino perd aussi avec son deck de départ).
  Cartes ACTIVÉES dans les journaux A+B (lignes « s'active » / « entre en jeu ») : toutes sauf uj005
  Delirium, uj010 Float Like a Butterfly, uj024 One Way or Another, uj026 Ram-Shell, uj040 Zone of Silence
  (Spider-Man n'est pas MYSTIC : injouable, attendu). Lecture ligne à ligne : voir chaque fiche.
- **Plateau** (étape 8 bis) : `ui-app/src/board/tmnt-justice-plateau.test.ts`, 8/8 verts. Vu ROUGE : le cas
  des noms français des compteurs (élan / brûlure / corde) sans l'ajout de `compteurs-fr.ts` (1 rouge,
  7 verts). Les 7 autres (glissée sous un SOUTIEN, attaches sur sbire / manigance / allié, Cloaked) passent
  sur le code existant : aucun correctif d'affichage n'a été nécessaire, ils n'ont donc pas de « rouge
  avant correctif » à montrer (ils gardent l'affichage).
- **Images** : `tools/importer_images_tmnt_aspects.py <zip> <assets/pics> uj` : 40 images (assets/pics est
  hors git).
- **Texte FR** : bloc « TMNT Justice (uj) » de `ui-app/src/board/textes-fr-fanmade.ts`, public régénéré.
- **Ressources** : vérifiées contre les cartes du MÊME pack dont la fiche officielle déclare la ressource :
  poing rouge = R (uj001 ↔ 58016 R), nœuds bleus = B (uj003 ↔ 04049 B), éclair jaune = Y (uj002 ↔ 26034 Y).
  Les 20 reskins portent la même icône que leur officielle. uj015 : aucune icône (comme 61036).
- **Mot-clé** : fiches lues avant le code : rampage, toughness, vulnerable, cloak, cloaked, tuck, uses,
  restricted, temporary, starting, acceleration.

## Reskins IDENTIQUES (`ability_link`, aucun script)

Pour chacun : module de l'officielle relu (aucun nom ni card_id comparé en dur ; `grep -rn '"<id>"'
src/game src/engine` vide, sauf 30019 cité dans un COMMENTAIRE de `card.py`, le correctif vise le type
`MainScheme`), clés moteur recopiées dans `desc` (MaxPerUnit, MaxPerDeck, Temporary), traits et citation du
scan. Étape 7 bis : limite imprimée NON, sauf uj024. Étape 8 bis : NON sauf uj025 / uj035 (attache à une
manigance : rendu générique, déjà couvert par le test plateau de Chance Encounter).

### uj001 : Battlefield Benevolence (↔ 58016)
- [x] 2 : 58016 par lien. [x] 5 : texte du scan = 58016 mot à mot (« Heal 2 damage from an enemy →
  confuse that enemy »). [x] 6 : coût 1, R. [x] 7 : cas + témoin (Rhino 3 → 1 dégât, Confused), rouge sans
  lien. [x] 7 bis : NON. [x] 8 : jouée (journaux B). [x] 8 bis : NON (statut d'ennemi, rendu existant).
Carte terminée : OUI.

### uj003 : Clear the Area (↔ 04049)
- [x] 2/5/6 : identique, coût 1, B. [x] 7 : cas + témoin (2 → 0, pioche 1), rouge sans lien. [x] 7 bis :
  NON. [x] 8 : jouée. [x] 8 bis : NON.
Carte terminée : OUI.

### uj007 : Disguise (↔ 47013)
- [x] 2/5/6 : identique (« Exhaust Disguise and your identity »), coût 1, B, MaxPerUnit 1. [x] 7 : cas +
  témoin (5 → 3, les deux inclinés), rouge sans lien ; cas de donnée Max 1 per player (vert, donnée).
  [x] 7 bis : NON (« Max 1 per player » n'est pas une limite d'usage). [x] 8 : jouée. [x] 8 bis : NON.
  Note : le texte FR officiel de 47013 oublie « et votre identité » ; le texte uj007 le rétablit.
Carte terminée : OUI.

### uj010 : Float Like a Butterfly (↔ 41017)
- [x] 2/5/6 : identique, coût 2, Y, MaxPerUnit 1. [x] 7 : cas + témoin (ATK 2 + 1 = 3 sur Rhino
  désorienté), rouge sans lien. [x] 7 bis : NON. [ ] 8 : jamais activée en autoplay (le pilote n'attaque
  pas d'ennemi désorienté) ; 0 traceback. [x] 8 bis : NON.
Carte terminée : OUI (activation en partie non observée, voir rapport).

### uj011 : For Justice! (↔ 01060)
- [x] 2/5/6 : identique, coût 2, Y ; icône [mental] du texte = nœuds bleus. [x] 7 : 2 cas + 2 témoins
  (payé B : 6 → 2 ; payé R : 6 → 3), rouges sans lien. [x] 7 bis : NON. [x] 8 : jouée. [x] 8 bis : NON.
Carte terminée : OUI.

### uj013 : Heroic Conditioning (↔ 58021)
- [x] 2/5/6 : identique, coût 3, R, MaxPerUnit 1. [x] 7 : cas + témoin (+3 PV, +1 THW), rouge sans lien.
  [x] 7 bis : NON. [x] 8 : jouée. [x] 8 bis : NON.
Carte terminée : OUI.

### uj014 : Heroic Intuition (↔ 01065)
- [x] idem : coût 2, Y. Cas + témoin (+1 THW), rouge sans lien. Jouée en autoplay.
Carte terminée : OUI.

### uj015 : Innate Perception (↔ 61036)
- [x] 2/5/6 : identique, coût 2, aucune ressource, MaxPerDeck 1. [x] 7 : cas + témoin « +1 THW », rouge
  sans lien. ⚠ Le mot-clé Starting (même module 61036, `WhenGameBeginSetup`) n'a PAS de cas sur uj015 : le
  harnais ne sait monter une mise en place qu'avec un deck de départ existant qui contient la carte ; les
  cas 61036 existants (« Starting ACCEPTE / REFUSE ») couvrent le module. [x] 8 : en autoplay, 26 lignes
  d'activation (la question Starting est posée et acceptée à la mise en place). [x] 8 bis : NON.
Carte terminée : OUI, sauf preuve harnais de Starting sur uj015 (vue en autoplay seulement).

### uj017 : Know Your Enemy (↔ 60023)
- [x] identique, coût « 1* », B. Cas + témoin : 2 × 1 menace (5 → 3) ; Discount 1 (Daredevil 60039
  MARTIAL ARTIST en jeu, aucune ressource en main : jouée), rouges sans lien. Jouée en autoplay.
Carte terminée : OUI.

### uj022 : Move in Shadow (↔ 60027)
- [x] identique (nom au singulier sur le scan, fichier « Move in Shadows »), coût « 2* », Y, MaxPerUnit 1,
  Temporary 1. Cas + témoin (sa propre Réponse : 5 → 4), rouge sans lien. Discount et Temporary : même
  module / donnée que l'officielle, sans cas dédié sur uj022 (Discount prouvé sur uj017, même fabrique
  `DiscountAbility`). Jouée en autoplay.
Carte terminée : OUI.

### uj024 : One Way or Another (↔ 22015)
- [x] identique, coût 0, B. Cas + témoin (01107 révélée, main 3), rouge sans lien. [x] 7 bis : « Max 1 per
  round » = limite : TÉMOIN D'ÉPUISEMENT (2 copies en main, une jouée, la 2e refusée alors que 2 manigances
  annexes restent) + contre-cas (sans copie jouée : jouable). ⚠ Sous substitution le témoin reste vert (sans
  lien la carte n'a plus de capacité de jeu) : la limite est portée par `MaxOnePerRound()` du module 22015.
  [ ] 8 : jamais jouée en autoplay. [x] 8 bis : NON.
Carte terminée : OUI (non observée en autoplay).

### uj025 : Overwatch (↔ 30019)
- [x] identique, coût 0, R, MaxPerUnit 1. Cas + témoin (1 menace contrée sur la principale → 1 retirée de
  01107, Overwatch défaussée), rouge sans lien. Jouée et activée en autoplay (14 lignes). 8 bis : attache à
  une manigance, rendu générique.
Carte terminée : OUI.

### uj029 : Skilled Investigator (↔ 04047), uj030 : Stealth Strike (↔ 08013 = 37014), uj031 : Stealth Training (↔ 60028), uj032 : Three Steps Ahead (↔ 47015), uj035 : Under Surveillance (↔ 06031)
- [x] chacune : texte identique, coût / ressource identiques (0 R, 3 B, 2 R, 3 B, 2 Y), MaxPerUnit recopié
  pour les améliorations. Cas + témoin chacune (pioche 1 ; sbire tué → 2 menaces ; Rhino sonné ; 2 types
  → 2 × 2 ; seuil +4), rouges sans lien. Toutes jouées en autoplay.
Cartes terminées : OUI (les cinq).

### uj040 : Zone of Silence (↔ 21050)
- [x] identique sauf la coquille « 4 card cards » (affichage corrigé, question Q-uj040). Coût 1, B,
  MaxPerDeck 1. Cas + témoin avec Doctor Strange (MYSTIC) : 4 défaussées → 4 menaces (ligne de base du deck
  écrite dans le cas) ; Spider-Man : injouable (donnée). Rouges sans lien (la capacité). [ ] 8 : injouable
  pour Spider-Man (attendu), non observée.
Réponse du 17/10/2026 : « 4 cards » (texte affiché corrigé) confirmé ; (« 4 card cards » du scan = coquille).
Carte terminée : OUI.

### uj023 : Night-Blade (Leo) (↔ 08011 Agent Coulson) — reclassée IDENTIQUE
- Le TSV la classe MODIFIEE ; relu : seul le NOM change (et les traits, qui sont des données), exactement le
  cas de Bo-Wing (ua006) : lien. Module 08011 relu (« This », recherche PREPARATION, aucun nom en dur).
- [x] 6 : coût 3, PV 3, THW 2*, ATK 1*, B. [x] 7 : cas + témoin (08018 Spycraft va en main), rouge sans
  lien ; bandeau « ✦ Agent Coulson » → `unique_also` (3 cas, Q-R1). [x] 8 : 24 lignes d'activation.
Carte terminée : OUI.

### uj036 : Venus (Bonnie) (↔ 51014 Manifold)
- Lien posé selon l'option recommandée de **Q-uj036** (« a discard pile »). Cas + témoin (40018 en main),
  rouge sans lien ; bandeau « ✦ Manifold » (3 cas). Jouée en autoplay.
Réponse du 17/10/2026 : « a discard pile » est une coquille, **comme Manifold : SA défausse** (code déjà ainsi, lien 51014).
Carte terminée : OUI.

## Cartes MODIFIÉES (script propre, copie adaptée)

### uj002 : Chance Encounter (RESKIN de 26034 par `ability_link`)
- [x] 2 : 26034 (déclencheur, recherche) ; 30019 (« Attach to a scheme » = `CanPlayThisUpgradeCard(Scheme2)`).
- [x] 5 : « a scheme » (principale ou annexe) ; « attached SIDE scheme » ; « your deck and discard pile ».
- [x] 6 : coût 0, Y, MaxPerUnit 1.
- [x] 7 : jouable sur la principale (rouge sans module) ; annexe vaincue → 60039 en main (rouge sans module).
- [x] 7 bis : NON. [x] 8 : jouée (journaux A). [x] 8 bis : OUI (attache à manigance) : test plateau vert.
**Mise à jour du 17/10/2026 (Réponse du 17/10/2026)** : coquille confirmée, « Attach to a SIDE scheme » comme l'officielle 26034.
Retour à l'officielle : entrée avec `"ability_link": "26034"` (RECETTES §11), script propre `uj002.py` SUPPRIMÉ, texte affiché
corrigé en « side scheme » (FR « manigance annexe »). Module 26034 relu : aucun nom ni card_id en dur ; `MaxPerUnit 1` reste dans
le `desc` (non transmis par le lien).
- Étape 7 : 3 cas + 3 TÉMOINS 26034 (même chiffre) : seule la principale en jeu -> PAS jouable ; une annexe (01107) en jeu ->
  jouable ; annexe attachée vaincue -> 60039 en main. **Substitution (retrait de `ability_link`)** : 2 cas ROUGES (« PAS jouable
  sur la principale », « annexe vaincue -> allié »), témoins verts ; le cas « jouable avec annexe » reste vert sans lien (le
  vérificateur `max_par_joueur_jouable` ne mesure pas la cible : assumé). 6/6 verts avec le lien.
- Étape 8 bis : test plateau `tmnt-justice-plateau.test.ts` inchangé (attache à une manigance quelle qu'elle soit).
Carte terminée : OUI.

### uj019 : Mission Training
- [x] 2 : 34016 (`CanPlayThisUpgradeCard` + `GiveKeywordToAttached(Ally, thwart=1, health=2)`), wx012 pour
  le filtre. [x] 5 : « NINJA OR MUTANIMAL ally » ; « Max 1 TRAINING upgrade per ally » : ⚠ 34016 ne la code
  PAS ; codée ici (filtre de cible). [x] 6 : coût 1, B, +1 / +2.
- [x] 7 : sur Night-Blade : +1 THW +2 PV (rouge sans module) ; Daredevil seul : injouable (rouge) ; Max 1
  TRAINING : 2e copie injouable (rouge) + témoin jouable.
- [x] 7 bis : la clause « Max 1 TRAINING per ally » a son témoin (montage à deux copies). [x] 8 : jouée.
  [x] 8 bis : attache à un allié, test plateau vert.
Carte terminée : OUI.

### uj026 : Ram-Shell (Raph) (↔ 61016)
- [x] 2 : 61016. ⚠ Écart VOULU avec son module : le « You may discard » est DANS la Réponse (scan), pas une
  Action séparée. ⚠ Déclencheur : 61016 écrit `"You"`, que `CheckWhichCard` ne connaît pas ; SONDE sur
  l'officielle (cas « SONDE 61016 », hors `[uj]`) : 0 compteur après un contre → la Réponse de 61016 ne part
  JAMAIS. Ici `"YouControlCharacter"`.
- [x] 5 : « a character you control » ; « to a maximum of 8 » ; « You MAY discard » ; « for each momentum
  counter here ». [x] 6 : coût 4, PV 3, 2**/2**, R, plafond 8.
- [x] 7 : contre du héros → 1 élan (rouge sans module) ; 2e contre (Ram-Shell elle-même) + défausse → 2
  dégâts à Rhino (rouge) ; plafond 8 (vert sous substitution : absence). Bandeau « ✦ Spider-Woman » : 2 cas
  (le sens inverse est retiré : 61016 reste « jouable » même contre une 2e copie d'elle-même, défaut de
  l'officielle, signalé).
- [x] 7 bis : NON (le plafond n'est pas une limite d'usage). [ ] 8 : jamais posée en autoplay (coût 4).
  [x] 8 bis : compteur momentum « élan » : test plateau, vu rouge sans le nom FR.
Carte terminée : OUI (non observée en autoplay).

### uj028 : Screwloose (↔ 60021 Dagger) et uj038 : Wingnut (↔ 60020 Cloak)
- [x] 2 : 60021 / 60020 ; leurs modules comparent les NOMS « Cloak » / « Dagger » en dur : script propre,
  noms remplacés par Wingnut / Screwloose. [x] 5 : « Wingnut loses EACH [acceleration] icon » ; « If
  Wingnut is IN PLAY » ; « Exhaust AND spend [energy][energy] » ; « find » (main, deck, défausse, lecture
  de 60020). [x] 6 : uj028 coût 3, PV 3, THW 1**, ATK 2**, Y ; uj038 coût 3, PV 2, THW 2, ATK 1, B,
  Acceleration 1.
- [x] 7 : icône [acceleration] 1 → 0 avec Screwloose (rouge sans module) + témoin ; -1 dégât consécutif
  (2 → 1, rouge) + témoin ; Wingnut : Screwloose du deck en jeu (rouge). Bandeaux « ✦ Dagger » / « ✦ Cloak »
  (3 cas chacun).
- [x] 7 bis : NON. [x] 8 : journal A : Wingnut payé en défaussant Screwloose + Dreadmon, puis « trouve »
  Screwloose en défausse et le met en jeu (lecture de 60020 : la recherche inclut la défausse). [x] 8 bis :
  NON (icône, rendu existant).
Cartes terminées : OUI (les deux).

### uj039 : Zebulon (↔ 61017 Squirrel Girl)
- [x] 2 : 61017. Compteur « scorch » AJOUTÉ à `CardFace.COUNTER`. [x] 5 : « After you PLAY FROM YOUR HAND »,
  « for each card in your hand (max 4) », « Remove 1 scorch counter → ». [x] 6 : coût 2, PV 2, 1*/1*, B.
- [x] 7 : joué avec 2 cartes restantes → 2 scorch (rouge sans module) ; 5 cartes → plafond 4 (rouge) ;
  Action : 2 → 1 scorch, 5 → 4 menaces (rouge) ; mis en jeu par effet : 0 (contre-cas). Bandeau « ✦ Squirrel
  Girl » (3 cas).
- [x] 7 bis : NON. [x] 8 : 24 lignes d'activation (journaux A). [x] 8 bis : compteur « brûlure » : test
  plateau, vu rouge sans le nom FR.
Carte terminée : OUI.

## Cartes NOUVELLES (script propre)

### uj004 : Cowabunga (Mikey)
- [x] 2 : RECETTES §1 (`AfterCardEnterPlay`), `CostFunc.Discard("YourHandCards", card_type=Resource)`,
  tv001b (soin). [x] 5 : « enters play » ; « discard a RESOURCE card → » (coût) ; « draw 2 AND heal 2 » ;
  « a friendly character ». [x] 6 : coût 2, PV 2, THW 2* (le TSV disait 1 : le scan dit 2), ATK 1*, B.
- [x] 7 : pioche 2 + soin 3 → 1, Strength défaussée (rouge) ; contre-cas sans carte ressource.
- [x] 7 bis : NON. [x] 8 : 21 lignes d'activation. [x] 8 bis : NON.
Carte terminée : OUI.

### uj005 : Delirium
- [x] 2 : wx012 (« attacked this turn » via `world.stat.this_turn_made_attack`), wd098 (`apply`), 37034
  (« When attached minion leaves play »). Fiche vulnerable lue. [x] 5 : « a MINION » ; « YOUR HERO attacked
  THIS TURN » ; « non-ELITE » ; « Interrupt » optionnel ; « leaves play ». [x] 6 : coût 1, B, 2 menaces.
- [x] 7 : jouable après attaque du héros / injouable sans (rouge sans module pour la chaîne) ; sbire
  non-ELITE vulnérable, désorienté → défaussé → Interruption 5 → 3 (rouge) ; ELITE (01102) : reste en jeu.
- [x] 7 bis : NON. [ ] 8 : jamais jouée en autoplay (le pilote ne joue pas la carte après une attaque).
  [x] 8 bis : attache à un sbire engagé, test plateau vert.
Carte terminée : OUI (non observée en autoplay).

### uj006 : Dire Straits (Rampage 3)
- [x] 2 : ua015 (Rampage, NYC), 04049, sk029. [x] 5 : coût additionnel ; « a scheme » ; « NYC SUPPORT » ;
  « ready YOUR hero ». [x] 6 : « 1* », Y, Rampage 3, 3 menaces.
- [x] 7 : payé (3 dégâts, 3 cartes, 5 → 2, héros reste incliné) ; NYC (tr008) → héros prêt ; deck de 2
  (décision confirmée : jouable) ; Tenace : coût non payé, rien. Rouges sans module (sauf Tenace, absence).
- [x] 7 bis : NON. [x] 8 : jouée 4 fois (journaux A), puis glissée sous Mona Lisa et rejouée. [x] 8 bis : NON.
Carte terminée : OUI.

### uj008 : Dreadmon
- [x] 2 : 19012 / tl009 (`AfterAllyTakeConsequentialDamage`), bw015 (`WhenRoundEnd(ForcedInterrupt)`).
  [x] 5 : « DREADMON takes consequential damage » ; « ready HIM » ; « Forced Interrupt » obligatoire,
  « discard ». [x] 6 : coût 3, PV 3, 2**/2**, Y.
- [x] 7 : attaque → 2 dégâts consécutifs → prêt (rouge) ; refus → incliné ; fin de round → défaussé (rouge).
- [x] 7 bis : NON. [x] 8 : journal A : « Dreadmon s'active → redressé » (15 lignes). [x] 8 bis : NON.
Carte terminée : OUI.

### uj009 : Feral Cunning (Rampage 2)
- [x] 2 : ua015, 58016. [x] 5 : « 1 damage AND confuse IT » (même cible, effets indépendants).
  [x] 6 : « 2* », B, Rampage 2, 1 dégât.
- [x] 7 : payé (2 dégâts, 2 cartes, Rhino 1 dégât + Confused) ; Tenace sur l'identité : rien ; sbire Tenace :
  dégât absorbé MAIS désorienté. Rouges sans module (sauf Tenace identité, absence).
  ⚠ Piège harnais noté : payer avec 01089 alors que le deck n'a QUE des 01089 retire une carte du deck
  (`Puzzle.Gain` reprend la copie du deck) : payé avec 01088.
- [x] 7 bis : NON. [x] 8 : jouée 1 fois. [x] 8 bis : NON.
Carte terminée : OUI.

### uj012 : Hatamoto (Donnie)
- [x] 2 : 62012 (`WhenUnitDefendAgainstAttack(Interrupt, "This")`), fiche toughness. [x] 6 : coût 3, PV 3,
  THW 1*, ATK 2*, R, Toughness 1.
- [x] 7 : Tough à l'entrée (donnée) ; défend contre Rhino → 5 → 4 (rouge sans module).
- [x] 7 bis : NON. [x] 8 : 16 lignes d'activation. [x] 8 bis : NON.
Carte terminée : OUI.

### uj016 : Inspector Ishida
- [x] 2 : 61017 (`AfterYouPlayThisFromHand`), 52021 (`LookAtDeck` + `PlaceOnTopInAnyOrder`).
  [x] 5 : « FROM YOUR HAND » ; « choose » une branche. [x] 6 : coût 3, PV 3, THW 2*, ATK 2**, R.
- [x] 7 : choix 1 : 5 → 3 (rouge) ; choix 2 : menace intacte, cartes restées dans le deck rencontre (vert
  sous substitution : la réorganisation n'a pas d'effet mesurable sans connaître l'ordre choisi) ; mise en jeu
  par effet : rien.
- [x] 7 bis : NON. [x] 8 : 21 lignes d'activation. [x] 8 bis : NON.
Carte terminée : OUI ; la branche « réordonner » n'est pas prouvée par substitution.

### uj018 : Lita
- [x] 2 : aa019 (« After <allié> thwarts »), 52021 (`LookAtDeck`), `MayChooseOneAbility`. [x] 5 : « look »
  toujours ; « You MAY discard 1 card TO add that card ». [x] 6 : coût 3, PV 3, THW 2*, ATK 1*, Y.
- [x] 7 : défausse 01088 → 01090 en main (rouge) ; refus : rien ne bouge.
- [x] 7 bis : NON. [x] 8 : 23 lignes d'activation. [x] 8 bis : NON.
Carte terminée : OUI.

### uj020 : Mona Lisa
- [x] 2 : 60030 (tuck), ar007 (`PlayCardsLikeInTurn`), RR v1.8 « THEN ». Fiche tuck lue.
- [x] 5 : « THWART EVENT in YOUR discard pile » ; « Action » ; « paying its cost » ; « THEN, discard » :
  seulement si la carte a été jouée. ⚠ Première version : défausse inconditionnelle ; l'autoplay l'a montrée
  (Peter Parker en alter-ego activait Mona Lisa, ne pouvait pas jouer Dire Straits, perdait les deux).
  Corrigé, cas « THEN » vu ROUGE avec l'ancien code.
- [x] 6 : coût 0, B, unique.
- [x] 7 : glisse 04049 (rouge) ; Action : 04049 jouée 5 → 3, Mona Lisa défaussée (rouge) ; carte impayable :
  Mona Lisa reste (rouge avec l'ancien code) ; sans événement THWART : rien.
- [x] 7 bis : NON. [x] 8 : journal A : glisse Dire Straits, puis la rejoue en forme héros (Rampage payé).
  [x] 8 bis : OUI (carte glissée sous un SOUTIEN) : test plateau vert.
Carte terminée : OUI.

### uj021 : Mondo Gecko
- [x] 2 : td005 / tl016 (`Faces.GiveStatus(..., "Cloaked")`), fiches cloak / cloaked. [x] 5 : « cloak HIM » ;
  maximum 1 Cloaked (condition). [x] 6 : coût 2, PV 2, 1*/1*, B.
- [x] 7 : jouée → Cloaked (rouge sans module). [x] 7 bis : NON. [x] 8 : 21 lignes. [x] 8 bis : OUI (carte
  d'état sur un allié) : test plateau vert.
Carte terminée : OUI.

### uj027 : Sally Pride
- [x] 2 : 27046 (`AfterUnitAttackOrThwart`), 04049. [x] 6 : coût 3, PV 2, 2*/2*, R.
- [x] 7 : attaque → 5 → 3 (rouge) ; contre → 5 − 2 − 2 = 1 (rouge). [x] 7 bis : NON. [x] 8 : 18 lignes.
  [x] 8 bis : NON.
Carte terminée : OUI.

### uj033 : Tomoe Ame
- [x] 2 : sk029 / 52001a (`AfterUnitDefeatedUnit` + `AfterUnitDefeatedScheme`). [x] 5 : « TOMOE AME
  defeats » ; « SIDE scheme OR MINION ». [x] 6 : coût 3, PV 3, THW 2*, ATK 3**, Y.
- [x] 7 : tue 01101 → pioche (rouge) ; vainc 01107 → pioche (rouge) ; Rhino survit : rien.
- [x] 7 bis : NON. [x] 8 : 18 lignes. [x] 8 bis : NON.
Carte terminée : OUI.

### uj034 : Turtle Line
- [x] 2 : 54018 Bambino (même gabarit : restricted conditionnel, Uses), sk064 (`Friend`). Compteur « rope »
  AJOUTÉ à `CardFace.COUNTER`. [x] 5 : « friendly character » ; restricted SEULEMENT sur une identité ;
  deux coûts ; Uses (sortie au dernier pion, moteur). [x] 6 : coût 2, Y, Uses 3, 2 menaces.
- [x] 7 : héros contre → 5 − 1 − 2 = 2, 2 cordes, inclinée (rouge) ; sur un allié après attaque (rouge) ;
  dernier pion → quitte le jeu (rouge) ; restricted 1 sur le héros (rouge) / 0 sur un allié, jouée avec
  cible (absence). ⚠ Un `Puzzle.Attach` APRÈS la mise en jeu ne recalcule pas `restricted` (montage, pas jeu
  réel) : les cas jouent la carte avec sa cible.
- [x] 7 bis : NON. [x] 8 : jouée 1 fois (5 lignes). [x] 8 bis : attache + compteur « corde » : test plateau.
Carte terminée : OUI.

### uj037 : Watch the Exits
- [x] 2 : `DiscountAbility` (`ReduceCostToPlayThis(1, conditions=...)`), ua015, 27159, sk029.
  [x] 5 : « IF YOU CONTROL a NYC SUPPORT » ; « Hero Response » ; « a MINION engages YOU » ; « discard → »
  coût ; « 2 threat AND ready ». [x] 6 : coût 2, R, réduction 1.
- [x] 7 : tr008 en jeu : jouée avec une seule ressource (rouge) ; sans NYC : reste en main ; sbire engage →
  5 → 3 + héros prêt + défaussée (rouge).
- [x] 7 bis : NON. [x] 8 : jouée 1 fois. [x] 8 bis : NON.
Carte terminée : OUI.
