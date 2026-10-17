# TMNT Shinobi, les 11 Paths (`se001`-`se011`) : gabarits PROCESSUS-CARTE (17/10/2026)

Pack `tmnt_shinobi_paths` (set 207, « TMNT Shinobi Paths », Inkwire). Scans : `Shinobi Paths/*.png` et `Shinobi Paths/ Hybrid Shinobi Paths
(Advanced)/*.png` (fronts), `* Cardback.png` (dos = règles de construction, transcrites dans `data/shinobi_paths.json`).
Classement contre les officielles : **NOUVELLE** pour les 11 (aucun art alternatif ni reskin ; type PATH et système inexistants
côté officiel). Cas : `Fusion/marvel-lcg-src/tools/cas/tmnt_shinobi_paths.py` (filtre `[se] seNNN`, 91 cas).
Questions ouvertes : `.planning/tmnt/shinobi-socle-questions.md` (Q-S1, Q-S2 concernent des cartes).

Preuve par substitution : module remplacé par `GetAbilities -> []`, cas relancés, rouges comptés (script jetable, ports 28100-28199 :
`substituer_pack.py` écarte ses ports de 60 par carte, hors de la plage). Les cas qui restent VERTS sans module sont des témoins
d'ABSENCE (forme alter-ego, trait absent sans Path, action non proposée faute de coût, témoin « sans Bodyguard ») ou des cas du
moteur (Path du deck mis en jeu au Setup, classes) : assumé, listé carte par carte.

Éléments communs à tous les Paths : « Permanent » (base automatique `desc.Permanent`, fiche `permanent.md`, aucun script) ;
« You get -1 hand size » = `GiveKeywordToInPlayWhenApplyThis("You", hand_size=-1)`, modèle `sentinel/st005b` (`04165` Martial Law),
2 cas par Path (forme héros 5 -> 4, forme alter-ego 6 -> 5, valeurs de Spider-Man) rouges sans module ; mise en jeu au Setup par
`PlayerSetup.MettreLesPathsDeCoteEtEnJeuAuSetup` (cas `se001` / `se005` « choisi au deck-building », rouges SANS l'appel moteur :
`total=0, en_jeu=0`, vus ROUGES par substitution du 17/10/2026). Étape 8 (autoplay ciblé) : NON faite sur ces cartes (consigne :
pas de batterie ; aucun deck de test contient encore de carte Shinobi portée). Étape 8 bis : voir `se005` (seul Path qui change ce
qu'on voit), cas plateau `ui-app/src/board/tmnt-shinobi-paths-plateau.test.ts` (5 tests, verts d'emblée : le correctif générique
d'attachement à plusieurs étages de `zones.ts` couvre déjà une carte glissée sous une Voie ; témoin négatif présent, donc pas de
« vu rouge sans correctif » possible ici, dit clairement).

### se001 : Kagemusha (Path, Ninjutsu)

- [x] Étape 2 : référence : Cloak : `tmnt_aspect_protection/up023` Lookout (`Faces.GiveStatus([hero], "Cloaked", effect)`, fiches
      `cloak.md`, `cloaked.md`) : même cible (le héros), même effet ; « Hero Action: Exhaust this card → » : `jennika/tj011` / `WhenInYourPlayTurn
      (HeroAction)` + `CostFunc.Exhaust("This")` ; trait gagné : `hunting_season/hs092` (`GiveKeywordToInPlayWhenApplyThis(..., trait=)`).
- [x] Étape 5 : mots-pièges : « YOUR HERO gains the NINJA trait » (forme héros seulement, `"YourHero"`) ; « You get -1 hand size » (`"You"`) ;
      « Hero Action » ; « cloak YOUR HERO » (jamais l'alter-ego) ; une seule Cloaked par personnage. Résultat : texte = code.
- [x] Étape 6 : nombres : -1 (taille de main) ; aucun autre nombre imprimé. Résultat : conforme dans `desc` (Permanent 1) et le script.
- [x] Étape 7 : 14 cas. Action : « Hero Action ... cloak » (rouge sans module) ; NINJA hero / absent alter-ego / absent sans Path ; -1 hand size x2 ;
      Path du deck x4 (Setup, témoin sans Path, main de départ 5, témoin 6) ; heros déjà camouflé : pas de seconde carte. Rouges sans
      module : 8/14 ; verts sans module : Setup (engine) x3, « Hero Action non proposée en alter-ego », « alter-ego sans NINJA », « sans Path pas
      NINJA » (absences).
- [x] Étape 7 bis : limite imprimée ? NON (le livret dit « once per round » : l'inclinaison la réalise). Témoin d'épuisement quand même :
      cas « la Voie inclinée ne propose plus Shadow Stride » (0 action disponible après usage ; rouge sans module).
- [ ] Étape 8 : non faite (voir plus haut).
- [x] Étape 8 bis : NON (statut, pas de glissement).

Carte terminée : **OUI**. Q-S1 résolue (réponse du 17/10/2026, `shinobi-reponses.md`) : le nom retenu est « Shadow Stride » (le scan). Comportement entièrement prouvé (14 cas).

### se002 : Onmyōdō (Path, Kuji-Kiri)

- [x] Étape 2 : référence : « look at the top N of any deck » : `gwenpool/gp008` Comicbook Panels (`LookAtDeck` + `ChooseAbilities` sur les decks
      proposés) ; « gains the MYSTIC trait » : `hs092`. Comparable : même regard sur un deck, même choix du deck ; ici 2 cartes et les decks des
      autres joueurs.
- [x] Étape 5 : « YOU gain the MYSTIC trait » (les deux formes) ; « top 2 cards of ANY deck » (son deck, ceux des autres joueurs, le deck
      rencontre ; UN seul) ; « put them back in the SAME ORDER » : regarder ne déplace rien (rien à remettre ; contraste avec « in any order »).
      Résultat : texte = code.
- [x] Étape 6 : 2 (cartes regardées), -1 (main). Conforme.
- [x] Étape 7 : 9 cas : regarder le deck rencontre / son deck / le deck d'un autre joueur (partie à deux) (mesure : les 2 cartes du dessus
      deviennent visibles du joueur, la 3e non, taille du deck inchangée, Voie inclinée) ; MYSTIC alter-ego / absent sans Path ; Hero Action absente
      en alter-ego ; épuisement ; -1 hand size x2. Rouges sans module : 7/9 ; verts : Hero Action absente en alter-ego, pas de MYSTIC sans Path.
- [x] Étape 7 bis : limite imprimée ? NON (inclinaison) ; témoin d'épuisement : « plus d'Insight après usage dans le même round ».
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON (regarder n'affiche rien de persistant).

Carte terminée : **OUI**.

### se003 : Samurai (Path, Bushido)

- [x] Étape 2 : référence : coût sur compteurs d'une AUTRE carte : `jennika/tj006` Fearless Resolve (`CostFunc.Counter`, « from IT »), non réparti ;
      pour « a total of 2 ... from among OATH upgrades you control » : `CostFunc.Custom` + sélecteur « This » portant une condition globale
      (`check_effect_fn`, comme `CostFunc.LookAtDeck`) ; « ready your hero and draw 1 card » : `Faces.ReadyAll` + `DrawUp`. Fiche `samurai-counter.md`.
- [x] Étape 5 : « a TOTAL of 2 » (réparti librement, 2 retirés en tout) ; « from AMONG OATH upgrades YOU control » (trait OATH, sous son contrôle) ;
      « Exhaust this card AND remove » (deux coûts) ; « ready YOUR HERO » (le héros) « AND draw 1 card » (les deux). Résultat : texte = code.
- [x] Étape 6 : 2 (compteurs), 1 (carte) ; -1 (main). Conforme.
- [x] Étape 7 : 9 cas : usage normal (2 compteurs d'une amélioration : défaussée par Uses, héros redressé, main +1, Voie inclinée) ; répartition libre
      (2+1 -> 1 restant) ; 1 compteur au total : action non proposée ; 1+1 sur deux améliorations : proposée ; compteurs sur une amélioration non OATH :
      ignorés ; épuisement ; alter-ego : non proposée ; -1 hand size x2. Rouges sans module : 6/9 ; verts : 1 compteur au total (absence), compteurs non
      OATH (absence), alter-ego (absence).
- [x] Étape 7 bis : limite imprimée ? NON sur la carte (le livret dit « once per turn ») ; l'inclinaison fait la limite : cas « la Voie inclinée ne propose
      plus Way of the Warrior » malgré des compteurs restants (chiffre : 0 action).
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON (les compteurs samouraï sont déjà couverts par `ScanCard.jetons.test.tsx`).

Carte terminée : **OUI**. Non prouvé : « you control » face à l'OATH d'un AUTRE joueur (aucun cas à deux joueurs).

### se004 : Shihan (Path, Taijutsu)

- [x] Étape 2 : référence : « When the player phase ends » : `skrull_menace/paibok/sk145b` (`WhenPlayerPhaseEnd`) ; coût « discard the top N cards of your
      deck → » : `rainy/rescue_rainy/90122` (`CostFunc.DiscardDeckTopCards`) ; retour d'une carte de la défausse en main : `Faces.AddToHand`.
- [x] Étape 5 : « When the PLAYER phase ends » = `WhenPhaseEnd("Player")`, envoyé par `world.py` APRÈS la pioche de fin de phase (`PlayersEndPhase`) et avant la phase
      du méchant : c'est la précision de la FAQ ; « discard the top 2 cards of YOUR deck → » (coût payé AVANT le choix : une Taijutsu défaussée par le coût peut être
      rendue) ; « 1 TAIJUTSU card » (Dual Taijutsu comprises) ; « to your HAND » ; Hero Interrupt. Résultat : texte = code, sauf la FAQ (Q-S2).
- [x] Étape 6 : 2 (cartes), 1 (carte), -1 (main). Conforme.
- [x] Étape 7 : 7 cas : usage (deck 4 -> 2, Taijutsu rendue, non-Taijutsu laissée) ; Taijutsu défaussée par le coût rendue ; aucune Taijutsu : coût payé, rien ne revient ;
      témoin Ninjutsu non rendue ; Hero Interrupt absent en alter-ego ; -1 hand size x2. Rouges sans module : 5/7 ; verts : témoin Ninjutsu et alter-ego (absences).
- [x] Étape 7 bis : limite imprimée ? NON ; une fois par fin de phase (message unique), pas de témoin d'épuisement possible hors du message.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.

- [x] Réponse Q-S2 (17/10/2026) : « Taijutsu + Dual Kuji-Kiri/Ninjutsu » : Recenter rend une carte de classe Taijutsu (Dual Taijutsu comprises) OU une Dual
      Kuji-Kiri/Ninjutsu (sc007, sc008) ; le texte affiché reste « 1 Taijutsu card ». Script modifié ; +2 cas (Dual KN sc007, Dual Taijutsu sc011) : 9 cas au total ;
      substitution : ancien script -> le cas sc007 rouge (1/2 passes), nouveau script -> 9/9.

Carte terminée : **OUI**.

### se005 : ✦ The Last Rōnin (Path hybride, unique, Bushido + Ninjutsu + Kuji-Kiri + Taijutsu)

- [x] Étape 2 : référence : tuck : `donatello/td012` (plafond « Max N » en condition de l'action, `AttachedCardCanPlayLikeInHand`), `casey_jones/tc013` Casey's Bag (« play » seulement : décision
      déjà prise, pas de `also_spend`/`also_discard`) ; tuck en coût : `bp/51018` (`CostFunc.TuckCardHere`). Fiche `tuck.md`.
- [x] Étape 5 : « You MAY play cards tucked here AS IF they were in your hand » (jouer seulement) ; « (Max 2 tucked cards) » (condition de l'action) ; « Action » (les deux formes) ;
      « Exhaust this card AND tuck 1 SHINOBI card from YOUR HAND under here » (deux coûts, la carte doit être Shinobi, de la main) ; « → draw 1 card ».
- [x] Étape 6 : 2 (max glissées), 1 (carte glissée), 1 (pioche), -1 (main). Conforme.
- [x] Étape 7 : 12 cas : Kanpeki (Voie inclinée, Shinobi glissée dessous hors de la main, +1 pioche) ; seule une Shinobi est glissable (la Basic reste en main) ; aucune Shinobi : non proposée ;
      2 glissées : non proposée ; 1 glissée : proposée ; Action proposée aussi en alter-ego ; carte glissée jouable comme en main (`IsLikeInHand()` vrai, la défausse non) ; témoin sous un autre
      hôte (faux) ; 4 classes reconnues ; Path du deck mis en jeu au Setup ; -1 hand size x2. (⚠ la clé `jouer` du harnais amène une carte absente en main : elle ne prouve rien ici, d'où
      `IsLikeInHand()`.) Rouges sans module : 7/12 ; verts : 4 classes et Setup (moteur), Kanpeki non proposée faute de Shinobi / avec 2 glissées (absences),
      témoin sous un autre hôte (absence). Passe complète `[se]` du 17/10/2026 : 91/91.
- [x] Étape 7 bis : limite imprimée ? OUI, « Max 2 tucked cards » : témoins : 2 glissées -> action non proposée, 1 glissée -> proposée (chiffre : 0 / 1 action disponible).
- [ ] Étape 8 : non faite.
- [x] Étape 8 bis : OUI (carte glissée sous la Voie). Cas plateau : `ui-app/src/board/tmnt-shinobi-paths-plateau.test.ts`, vert d'emblée (correctif générique déjà en place), témoin négatif.

Carte terminée : **OUI**. Non prouvé : le TUCK avec une Dual Shinobi réelle (aucune carte Dual n'est encore portée) ; `CardFinder(card_classes=...)` sur une Dual est prouvé sur la classe du Path lui-même (4 classes).

### se006 : Yoshimitsu (Path hybride, Bushido + Kuji-Kiri)

- [x] Étape 2 : référence : « +N hit points » : `04160b` Improved Attack Upgrade ; « take 1 damage AND exhaust » : `45043` Blood Rage ; « +1 THW, +1 ATK, +1 DEF until the end of the round » :
      `jennika/tj001a` (`GainUntilRoundEnd`).
- [x] Étape 5 : « You get +2 hit points » (les deux formes) ; « Take 1 damage AND exhaust this card » (deux coûts) ; « +1 THW, +1 ATK, +1 DEF until the END OF THE ROUND » ; Hero Action.
- [x] Étape 6 : -1, +2, 1 dégât, +1/+1/+1. Conforme.
- [x] Étape 7 : 9 cas : +2 PV héros / alter-ego ; Magnificence (1 dégât, Voie inclinée, +1/+1/+1) ; bonus disparu à la fin du round (dégât resté) ; épuisement ; alter-ego : non proposée ;
      classes DUAL (Bushido ET Kuji-Kiri reconnues, ni aspect ni Basic) ; -1 hand size x2. Rouges sans module : 7/9 ; verts : alter-ego (absence), classes (moteur).
- [x] Étape 7 bis : limite imprimée ? NON (inclinaison) ; témoin d'épuisement : plus de Magnificence après usage.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.

Carte terminée : **OUI**.

### se007 : Yamabushi (Path hybride, Kuji-Kiri + Taijutsu)

- [x] Étape 2 : référence : « exhaust this card AND your hero » : deux `CostFunc.Exhaust` (`This`, `YourHero`) ; « draw N. Choose and discard 1 card from your hand » : `DrawUp` + `AskDiscardFaces`
      (`player_phase.py`).
- [x] Étape 5 : « Exhaust this card AND YOUR HERO » (le héros doit être prêt) ; « draw 3 cards » (exactement 3) ; « Choose and discard 1 card from your HAND » (toute la main) ; « gain the TEMPORAL trait ».
- [x] Étape 6 : 3 (pioche), 1 (défausse), -1 (main). Conforme.
- [x] Étape 7 : 7 cas : Meditate (main 1 + 3 - 1 = 3, Voie et héros inclinés) ; héros déjà incliné : non proposée ; héros prêt : proposée ; épuisement ; TEMPORAL ; -1 hand size x2. Rouges
      sans module : 6/7 ; vert : héros déjà incliné (absence).
- [x] Étape 7 bis : limite imprimée ? NON ; témoin d'épuisement : plus de Meditate après usage.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.

Carte terminée : **OUI**.

### se008 : Onigari (Path hybride, Kuji-Kiri + Ninjutsu)

- [x] Étape 2 : référence : « After you defeat a minion OR side scheme » : `skrull_menace/hulkling_kajislav/sk029` / `52001a` Silk (deux capacités : `AfterUnitDefeatedUnit` + `AfterUnitDefeatedScheme`) ;
      « cloak your hero and draw 1 card » : `up023` Lookout.
- [x] Étape 5 : « a MINION or SIDE scheme » (pas le vilain, pas le complot principal) ; « YOU defeat » ; « cloak your hero AND draw 1 card » (les deux, même si déjà camouflé) ; Hero Response ; « gain the PSIONIC trait ».
- [x] Étape 6 : 1 (pioche), -1 (main). Conforme.
- [x] Étape 7 : 6 cas : sbire vaincu (camouflé, +1 carte, Voie inclinée) ; complot annexe vaincu (même effet) ; témoin sbire attaqué sans être vaincu (rien) ; PSIONIC ; -1 hand size x2. Rouges sans module :
      5/6 ; vert : témoin « sans défaite » (absence).
- [x] Étape 7 bis : limite imprimée ? NON (inclinaison, une fois par redressement ; deux capacités, UNE seule inclinaison).
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.

Carte terminée : **OUI**.

### se009 : Ashigaru (Path hybride, Bushido + Taijutsu)

- [x] Étape 2 : référence : `jennika/tj009` Tekko-Kagi (`CanGenerateResources(HeroResource, Resources("G"))` + `CostFunc.Exhaust("This")`) ; « if you paid for X with this resource » : `ex_operation` de
      `CanGenerateResources` (message `WhenPlayerPayingResources`, `paying_card`).
- [x] Étape 5 : « generate a [wild] resource » : l'icône étoile est LE MÊME glyphe que celui de tj009 (découpes comparées le 17/10/2026) ; « Hero Resource » ; « If you paid for a SHINOBI card WITH THIS RESOURCE » (la
      ressource de la Voie, une carte Shinobi, un paiement de jeu) ; « draw 1 card ».
- [x] Étape 6 : 1 (pioche), -1 (main). Conforme.
- [x] Étape 7 : 6 cas : une Shinobi payée par la Voie pioche 1 ; une carte non Shinobi (Mockingbird, coût 3) payée par la Voie : aucune pioche ; une Shinobi payée sans la Voie (déjà inclinée) : aucune
      pioche ; SOLDIER ; -1 hand size x2. Rouges sans module : 5/6 ; vert : Shinobi payée sans la Voie (absence).
- [x] Étape 7 bis : limite imprimée ? NON (inclinaison, une ressource par redressement).
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.

Carte terminée : **OUI**. Non prouvé : le chemin « Dual Shinobi payée par la Voie » (aucune Dual portée).

### se010 : Onmitsu (Path hybride, Ninjutsu + Taijutsu)

- [x] Étape 2 : référence : « After you play an <filtre> » : `jennika/tj011` / `michelangelo/tm011` (`AfterPlayerPlayedCard`) ; « take 1 damage → » : `45043` Blood Rage ; « daze an enemy » :
      `Faces.GiveStatus(..., "Dazed", ...)` (`dazed.md`, `tx016` Wrapped Up).
- [x] Étape 5 : « an ATTACK OR DEFENSE EVENT » (un événement portant l'un des traits) ; « After YOU play » ; « take 1 damage → daze » (le dégât est un coût) ; « daze AN ENEMY » (sbire ou vilain, un seul Dazed par personnage).
- [x] Étape 6 : 1 (dégât), -1 (main). Conforme.
- [x] Étape 7 : 6 cas : événement ATTACK (tj004) -> 1 dégât + Rhino hébété ; événement DEFENSE (01003 Backflip) -> idem ; témoin d'un non-événement : rien ; ennemi déjà hébété : une seule carte ; -1 hand size x2.
      Rouges sans module : 5/6 ; vert : témoin non-événement (absence).
- [x] Étape 7 bis : limite imprimée ? NON.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON (le statut Dazed a son badge, `effets-statuts.test.ts`).

Carte terminée : **OUI**. Non prouvé : un événement THWART seul ne déclenche pas (aucun événement THWART seul sous la main).

### se011 : Yōjimbō (Path hybride, Bushido + Ninjutsu)

- [x] Étape 2 : référence : `56047` "I Can Do This All Day" (`WhenUnitWouldAttack(HeroInterrupt, Enemy, op).SetTarget("YourHero")` + `DeclareDefender`).
- [x] Étape 5 : « When AN enemy attacks » (n'importe quel ennemi) ; « declare YOUR HERO as the defender » ; « WITHOUT EXHAUSTING THEM » (le héros reste prêt, mesuré) ; « exhaust THIS card → » ; Hero Interrupt.
- [x] Étape 6 : -1 (main). Conforme.
- [x] Étape 7 : 6 cas : Bodyguard (héros défenseur prêt, Voie inclinée) ; témoin : sans Bodyguard le héros qui défend s'incline ; alter-ego : non disponible ; Voie déjà inclinée : le héros défend normalement
      et s'incline ; -1 hand size x2. Rouges sans module : 3/6 ; verts : témoin, alter-ego, Voie inclinée (absences).
- [x] Étape 7 bis : limite imprimée ? NON (inclinaison) ; témoin d'épuisement : Voie inclinée -> pas de Bodyguard.
- [ ] Étape 8 : non faite. [x] Étape 8 bis : NON.

Carte terminée : **OUI**.
