# Buffy (Buffy Summers, la Tueuse) : gabarits PROCESSUS-CARTE, 31/10/2026

Pack `buffy` (prefixe `bf`, set 237, auteur RyCoRan). Scripts : `src/cards/pack/buffy/{buffy,buffy_nemesis,buffy_hellmouth}/` (32 cartes + 1 fiche modele). Cas : `tools/cas/buffy.py` (56 cas, noms commencant par le card_id) ; deck `buffy` ; textes FR : `ui-app/src/board/textes-fr-fanmade.ts` ; biographie : `public/js/prepare/heros-info.js` (`bf001a`).

**Aucune carte n'est « terminee »** (PROCESSUS-HEROS : « pas de heros a moitie valide »). Le pack est COMPLET (identite, deck de 15, obligation, set nemesis de 5, paquet HELLMOUTH et cartes liees) et JOUABLE de bout en bout dans le harnais ; ce qui manque est dit dans « Manques » : aucune partie reelle jouee par un humain, et plusieurs LECTURES provisoires a faire valider (liste « Questions en attente »).

## Questions tranchees par l'utilisateur (31/10/2026)

1. **bf019 Prophecy Girl** : interruption quand les degats laisseraient Buffy a 3 PV ou moins (lecture codee CONFIRMEE).
2. **bf020 Welcome to Sunnydale** : une icone de boost a trois branches + l'etoile = boost 1 (CONFIRME).
3. **bf026 The Gentlemen** : interdit les Actions des cartes d'un AUTRE joueur (lecture codee CONFIRMEE).
4. **bf025 Normal Again** : DECISION : a 0 compteur sanity l'obligation se DEFAUSSE. Code ecrit ; cas `bf025 ... se defausse` REJOUE a la reprise : rouge au premier essai par defaut de MESURE (`Puzzle.PlaceCounters` AJOUTE un delta et l'obligation entre deja avec 3 compteurs : le cas en posait 4), corrige par `Puzzle.Counter(.., -2)` ; vert, et rouge sans module (substitution).
5. **bf010 Sunnydale Library** : « identity-specific » = classe Hero (CONFIRME).

## Source

1. **Drive** « Buffy (Vampire Slayer) (12-25) » : 11 fichiers, 8 cartes distinctes (bf001a/b, bf002-bf007 hors Pointy End etc.), listees en entier (connecteur : pagination 5 + 6, verifie avec `pageSize` 200). Telechargees par `curl -sL "https://drive.google.com/uc?export=download&id=<id>"`.
2. **Images envoyees par l'utilisateur en cours de session** (le Drive ne montrait pas ces fichiers au connecteur) : 10 cartes joueur (Pointy End, Crimson Scythe, Sunnydale Library, Watcher's Guidance, Redeemed, Stakeout, Mr. Pointy, Kendra, Willow, Angel, Chosen One, Prophecy Girl, Genius, Strength, Energy) puis 13 cartes encounter (set nemesis, obligation, Gentlemen, paquet HELLMOUTH, Hush) et une illustration de Buffy (affiche violette, non utilisee : aucun emplacement d'art dans le pack). **Genius, Strength, Energy** sont les ressources basiques officielles `01089`, `01090`, `01088` illustrees par l'auteur : NON importees (art alternatif possible plus tard, pas un contenu de jeu).
Scans ramenes a 615x882 (petit cote 615, comme `outils/uniformiser-scans.py`) dans `assets/pics/bf0*.jpg` (dossier ignore par git). Le RGBA est aplati sur noir. **Chaque image a ete lue a l'oeil pour le texte, les statistiques et les icones de boost.**

**Numerotation** : bf001a/b identite ; bf002 Giles ; bf003 Slay Time x2 ; bf004 Bring on the Night x2 ; bf005 Slayer Strike x2 ; bf006 Faith (allie) ; bf007 Slayer Scythe ; bf008 Pointy End x2 (8/15 et 9/15) ; bf009 Crimson Scythe ; bf010 Sunnydale Library ; bf011 Watcher's Guidance ; bf012 Redeemed ; bf013 Stakeout ; bf014 Mr. Pointy ; bf015 Kendra ; bf016 Willow ; bf017 Angel ; bf018 Chosen One ; bf019 Prophecy Girl ; bf020-bf024 set nemesis `Buffy Nemesis` (Welcome to Sunnydale 1/5, Spike 2/5, Drusilla 3/5, Hush 4/5, The Harvest 5/5) ; bf025 obligation Normal Again ; bf026 The Gentlemen ; bf027-bf032 paquet `Buffy Hellmouth` (Harvest, Becoming, Enemies Aligned, The Master, Faith sbire, Angelus). Fiche modele `buffy_redeemed_ally`.

**Deck de heros (15 cartes, les numeros « n/15 »)** : bf002 (1), bf003 x2 (2-3), bf004 x2 (4-5), bf005 x2 (6-7), bf008 x2 (8-9), bf009 (10), bf010 (11), bf011 (12), bf012 (13), bf013 (14), bf014 (15). `obligations = [bf025]`, `nemesis_set = [bf020..bf024]`, `player_deck` vide. Cartes hors deck : Faith allie, Scythe, Kendra, Willow, Angel, Chosen One, Prophecy Girl (liees ou sans numero).

**Mise en place reelle** (prouvee en partie, journal `verifier_tous_les_decks`) : l'alter-ego cree les six cartes HELLMOUTH MISES DE COTE (`BeginGameWithSetAside`), leurs cartes liees se creent par `desc.Linked` (card_id : `bf006 -> bf031`, `bf007 -> bf029`, `bf017 -> bf032`, `bf018 -> bf028`, `bf019 -> bf027`, `bf026 -> bf023`), puis son Setup retrouve et REVELE Harvest (complot annexe, 3 menaces) et The Master (sbire, engage avec Buffy). Chaine : Harvest -> Becoming -> Enemies Aligned + Faith sbire ; The Master -> Angelus ; Faith -> Faith allie ; Angelus -> Angel ; Becoming -> Chosen One ; Harvest -> Prophecy Girl ; Enemies Aligned -> Scythe.

**Modification du MOTEUR** (toutes additives) : traits `SLAYER`, `WATCHER`, `HELLMOUTH` et compteur `sanity` dans `card_face.py` ; trois aides de test dans `puzzle.py` (`AddTraitToPaper`, `RenamePaper`, `SendCardSetup`). Partages touches : `data/cards.json`, `data/sets_info.json` (checksums recalcules par `Types.DictChecksum`, verifie avant sur les fichiers d'origine), `tools/prefixes_fanmade.json`, `tools/traits_fr_maison.json`, `ui-app/src/board/traits-fr.ts` et ses generes.

## Cartes de substitution

Seuls les cas de `bf001a` (bonus) et `bf004` (Bring on the Night) utilisent encore des manigances OFFICIELLES a qui `Puzzle.AddTraitToPaper` donne le trait HELLMOUTH (`01107`/`01109`, avec `01108` sans le trait en temoin) : mesurer un decompte de 0 a 2 exige de poser des manigances a volonte dans la zone de victoire, ce que les vraies manigances HELLMOUTH (3 a 4 menaces, Hinder) ne permettent pas simplement. Tous les AUTRES cas utilisent les vraies cartes.

## Verifications faites (31/10/2026)

- **Cas** : `tools/test_capacites.py .game-src 42000 <rapport> bf0` : **56/56**.
- **Substitution** (`tools/substituer_pack.py ... bf0`, pack sauvegarde avant, identique apres) : **33/33 modules** avec au moins un cas rouge sans leur module. Verts restants = contre-cas d'ABSENCE d'effet voulus : bf001a (3 temoins), bf007 / bf008 / bf009 (carte non jouable ou alter-ego), bf021 (carte du deck qui n'est pas une traitrise).
- **Gates statiques** : `test_cards` 7844 OK / 0 erreur ; `verifier_api_cartes` 8856 fichiers, 0 en faute ; `verifier_prefixes` OK ; `verifier_appels_modules ... buffy` OK (**calibre** une fois avec une erreur volontaire `this.PlaceThreatOn`, detectee, fichier retire) ; `audit_cartes` : aucune remarque sur `bf*`.
- **Deck** : `verifier_tous_les_decks` : `buffy` monte (identite `bf001b`, main 6, deck 9) ; passe des 177 decks : 177/177 montent une partie (31/10/2026, apres l'ajout des 32 cartes).
- **Etape 10 de PROCESSUS-HEROS** : aucune carte signature d'un autre heros dans un deck (controle fait sur 177 decks avant l'ajout du set nemesis ; les ids du deck `buffy` sont tous du set `Buffy`).
- **Textes FR** : 25 textes ajoutes ; `textes-fr-fanmade.test.ts` et `vocabulaire-statuts.test.ts` verts (17 tests) apres correction du vocabulaire (Perforation -> Perçant, Excès -> Déferlement, Obstacle -> Entrave, « en forme d'alter ego » -> « sous forme d'alter ego »).
- **Icones de ressource** : les 8 premieres cartes, puis bf008-bf018 a la reprise, verifiees par comparaison avec des cartes officielles (voir « Reprise ») ; lecture : Pointy End = physique, Crimson Scythe = energie, Library/Guidance/Redeemed = mental, Stakeout / Kendra = physique, Mr. Pointy / Willow / Angel / Chosen One = wild ; bf019 : aucune.
- **Autoplay** (rhino, normal, equilibre, 8 parties) : toutes terminees, 0 exception (grep sur les 8 journaux), 0 victoire, 2,0 rounds (« Main Scheme completed » : Harvest, The Master et l'obligation arrivent des la mise en place, et le pilote ne joue que 15 cartes signature). Pas une mesure d'equilibrage.

## Reprise du 31/10/2026 (soir)

- **Batterie complete** `test_capacites.py` sans filtre (port 38000, PARALLELES=4, ~2 h 45) : **10516/10528**. 12 echecs : les 4 `sg` (Squirrel Girl, CONNUS d'avant), `bf025` (cas jamais rejoue, corrige ensuite, voir Questions tranchees 4) et **7 cas `[wn]` (She-Hulk Why Not : wn001a x4, wn002, wn003, wn008)**, tous « degats sur Rhino = attendu + 2 » (une activation de She-Hulk contre Rhino au passage en forme heros). ⚠ **Pas une regression de mes modifs** : memes 7 echecs (17/24) avec `card_face.py` et `puzzle.py` remis a HEAD (git stash cible, restaure et compare octet a octet), ET sur un checkout propre de HEAD (git worktree). A voir par la session `wn` (le commit d2021f56 annoncait 24/24 vert).
- **Cas bf0** : 57 -> **78/78** (21 cas ajoutes). **Substitution** (`tools/substituer_pack.py ... bf0`, pack sauvegarde avant, identique apres) : **33/33 modules** avec au moins un cas rouge ; verts restants = temoins d'absence (bf001a x3, bf007, bf008, bf009, bf021, bf022 Teamwork, bf031, bf032) + le boost de Hush (icones natives dans `desc`, sans script).
- **Points desormais mesures** : Bring on the Night « remove threat » (`preferer_option`) ; Slayer Strike X = 1 (Whiplash intact) et X = 3 ; Watcher's Guidance branches 2 et 3 ; Willow [physical] et [energy] ; Redeemed THW = SCH imprime (Whiplash SCH 2 : -2 menaces), degat consequent, et attaque ; Drusilla : Teamwork (avec The Master en jeu elle s'active a l'entree, sans lui non) et « each scheme » (annexe 1 -> 2, complot 2 -> 3) ; Hush : peril sur une carte revelee (`IMPRIME['peril']` ajoute a `test_capacites.py`, additif) et boost 2 ; boost 1 de Welcome to Sunnydale + « Reveal this card » ; overkill de Pointy End (8 sur Hydra PV 3 : 5 au vilain) et de Faith (exces 1 sur Willow abattue -> identite) ; perforation d'Angelus (Tough ignoree, 2 degats).
- **Pieges de mesure (corriges, pas contournes)** : Hydra Mercenary a **Garde** (impossible de viser Rhino tant qu'il est la) ; Pointy End coute 3 (il faut 3 ressources dans la main EN PLUS d'elle) ; Buffy DEFEND par defaut les attaques d'ennemi (`passer_sur_option='Defense'`) et elles portent des cartes de boost (deck vide + 8 Armored Rhino Suit, comme les cas `wn`) ; **Willow prend 1 degat CONSEQUENT apres son contre** (ses `1*` imprimes) : un soin de 2 sur 2 degats laisse 1.
- **Icones de ressource** bf008-bf018 comparees (planche) a des cartes officielles de ressource connue : poing = physique (01003, 01008), eclair = energie (01002, 01006), mental (01004, 01005), etoile = wild (01011, 01020) : **toutes conformes** a `desc` ; bf019 : aucune ressource sur le scan, comme dans `desc`.
- **Gates** : `test_cards` 7844 OK / 0 erreur ; `verifier_api_cartes` 8856 fichiers, 0 en faute ; `verifier_prefixes` OK ; `verifier_appels_modules buffy` OK ; `verifier_tous_les_decks` **177/177** ; vitest `textes-fr-fanmade` + `vocabulaire-statuts` + `buffy-plateau` : 20/20.
- **Navigateur (31/10 soir, Chromium via le Playwright de `ui-check`, moteur local `launcher_fast.py --no-browser`, extension Chrome toujours non connectee)** :
  - **Biographie (PROCESSUS-HEROS etape 7) : PROUVEE.** Wizard Solo > Fan-made > « Buffy » : le panneau « Biographie » deplie affiche le texte, Identite civile (Buffy Summers), Base (Sunnydale, Californie), Equipes (The Scooby Gang), Ennemis (The Master, Harvest), Premiere apparition (Buffy the Vampire Slayer (1992)). Aucune erreur de page.
  - **Vraie partie Buffy vs Rhino (deck « Brutish Aggression » propose)** : mise en place OK (Harvest en manigance annexe a 4 menaces, The Master engage, pile HELLMOUTH de 6 -> 4 cartes) ; action **Chosen** (Mr. Pointy en main, deck 39 -> 38) ; **Changer de forme** ; jeu de **Mr. Pointy** (texte FR « Restreint », « Percant » affiches) ; **attaque de base percante** sur The Master (Tenace retiree, 3 -> 2) ; **Slay Time** : The Master vaincu (exces -2 affiche), **Angelus entre en jeu** (7/7, pile HELLMOUTH 4 -> 3, Faith dessus) ; Reponse **Chosen One** proposee puis jouee (pioche, deck 38 -> 37) ; phase du mmechant : Rhino et Angelus attaquent (Riposte de Mr. Pointy : Rhino 13/14, Angelus 6/7), **Bring on the Night** proposee en interruption sur la revelation de Bomb Scare, payee et jouee : Bomb Scare finit en defausse rencontre, jamais en jeu ; passage au round 2 sans erreur console.
  - **Chaine HELLMOUTH complete en vraie partie (2e partie, `/sandbox_command` pour poser la menace a 1 et redresser Buffy, contres joues a la souris)** : Harvest contree -> Becoming revelee + Prophecy Girl attachee a Buffy ; Becoming contree -> Enemies Aligned + Faith sbire reveles + Chosen One attachee ; Enemies Aligned contree -> **Slayer Scythe en jeu**. Les deux manigances HELLMOUTH en zone de victoire donnent a Buffy **THW/ATQ/DEF 3 (+2)** (bonus de bf001a vu a l'ecran).
  - **Non atteint en vraie partie** : Angel (vaincre Angelus), Hush (action a 3 ressources), Redeemed, la reduction de cout de Slay Time (un clic a declenche la fenetre de fin de phase avant que Big Bang soit joue). Toujours mesures par le harnais seulement.
  - A regarder par l'utilisateur : la zone « HELLMOUTH » montre la pile mise de cote **face visible** (carte du dessus lisible : Angelus, puis Faith) ; le choix de deck demande une « Proposition de deck » (aucun deck de depart, comme Major Victory : `player_deck` vide voulu).
- **Traduction (31/10 soir, a la demande de l'utilisateur)** : textes FR des 32 cartes (`textes-fr-fanmade.ts`) + biographie + traits (SLAYER = TUEUSE, WATCHER = OBSERVATEUR) deja en place ; `ui-app/deployer.sh` lance (deploiement LOCAL seulement : `Fusion/marvel-lcg-src/public/app`, dossier ignore par git ; rien n'est parti en ligne). Voile FR regarde carte par carte au survol / dans la fenetre de revelation (Chromium) : **26 cartes vues, propres** (bf001a/b, bf002 a bf016, bf018 a bf020, bf023, bf027 a bf032 ; glossaires des mots-cles Restreint, Percant, Deferlement, Patrouille, Vilenie, Tenacite, Garde, Victoire 0 affiches). **Non vues** (survol impossible dans mes parties de test) : bf017 Angel, bf021 Spike, bf022 Drusilla, bf024 The Harvest, bf025 Normal Again, bf026 The Gentlemen.
  - Defauts trouves et corriges PAR DONNEES / hors composant du voile : (1) **bf029 Enemies Aligned** (manigance couchee, texte imprime plus gros que ce que l'effaceur attend) : « play. » restait en anglais sous le francais -> gomme `GOMMES.bf029` + zone manuelle `ZONES_MANUELLES.bf029` dans `zones-corrections.ts` (restent de tres pales traces de l'ancienne ligne) ; (2) **`CoucheRevelation.tsx` et `PanneauManigance.tsx`** passaient les traits bruts du monde (`t_HELLMOUTH`) au voile : la fenetre de revelation affichait « T_HELLMOUTH. » (defaut GENERAL, pas propre a Buffy) -> retrait du prefixe `t_` comme dans `mise-en-place-pas-a-pas.ts`. Aucun fichier de la session traduction (`TraductionPosee.tsx`, `traduction-posee.ts`) n'a ete modifie.
  - Observation d'affichage : la zone « HELLMOUTH » du plateau change de libelle quand il ne reste qu'une carte (Angelus : « ELITE »), le libelle semble pris sur le premier trait de la carte du dessus.
- Ce qui garde chaque carte a « Carte terminee : NON » : la partie humaine complete (chaine HELLMOUTH jusqu'au bout, multijoueur) n'a pas ete jouee.
- **Points encore non mesures** : multijoueur (Watcher's Guidance a un autre joueur, Scythe offerte, The Gentlemen, `ChoisirUnJoueur`), et le rendu plateau reel de la mise de cote.

## Correctif du 01/11/2026 : icones de manigance imprimees (trouve en relisant le pack RoboCop)

Les quatre manigances annexes de Buffy portent une ICONE imprimee que `desc` n'avait pas (« icone non reconnue », piege deja documente) : **bf020 Welcome to Sunnydale = Crise** (« ! »), **bf027 Harvest = Danger/Hazard** (croix dans un cadre), **bf028 Becoming** et **bf029 Enemies Aligned = Amplification** (avion + croix). Verifiees par comparaison avec les scans officiels `01108`, `01107`, `16054`. Ajoutees a `desc` (`Crisis`, `Hazard`, `Amplify` = 1), checksum recalcule, 4 cas `icones` (rouges avec l'ancien `cards.json`, verts apres) : **bf0 82/82**. Effet en jeu : Harvest (en jeu des la mise en place) fait piocher +1 carte de rencontre par phase du mechant ; Welcome to Sunnydale empeche de retirer des menaces du complot principal tant qu'elle est en jeu ; Becoming et Enemies Aligned ajoutent une icone de boost a chaque carte boost revelee. Ce n'etait donc pas cosmetique : la partie jouee en Chromium le 31/10 tournait sans ces trois effets.

## Ecarts assumes

- **`desc.Linked` par card_id** (pas par nom) : « Harvest » est aussi une traitrise officielle (`05029`), « Faith » nomme l'allie ET le sbire. `FindCardPaper` accepte un card_id (`mots-cles/linked.md`).
- **`bf001b` Setup** : les six cartes HELLMOUTH sont creees mises de cote par `BeginGameWithSetAside` ; « Find the Harvest (complot annexe) and The Master (sbire), and reveal them » = deux recherches (deck rencontre, defausse, mise de cote) filtrees par TYPE, suivies de `Reveal`.
- **`bf027`-`bf032`** : « find X » = `Search.SearchForCard(deck rencontre + defausse + mise de cote)` ; « the set-aside X » = mise de cote SEULE ; « under any player's control » = `ChoisirUnJoueur` (solo : le joueur, a plusieurs il choisit) ; le joueur qui a vaincu = `GetDefeatingPlayer` / `GetKillerPlayer`, a defaut le premier joueur.
- **`bf012` Redeemed** : fiche modele `buffy_redeemed_ally` (trait SLAYER, ATQ/CTR `0*`) ; la Reponse « attach to it » est OPTIONNELLE.
- **`bf016` Willow** : « uses a basic power » = ATQ ou CTR (pas de DEF d'allie) ; trois branches payees chacune par UNE ressource du bon type.
- **`bf001a`** : « Buffy gets » est un nom propre : bonus sur la face HEROS seulement (contre-cas alter-ego). « each basic power » = ATQ, CTR, DEF (pas REC). Decompte = manigances annexes (joueur ou rencontre) portant le trait HELLMOUTH dans la zone de victoire.
- **`bf004`** : « an encounter card » = TOUT type de carte (type `None`, modele 01075), pas seulement les traitrises (modele 09007). Interruption de HEROS, `"AnyPlayer"`. Si le nombre de manigances HELLMOUTH est 0, la revelation est annulee sans autre effet.
- **`bf005`** : X cartes defaussees en cout, `targets[:X]`. ⚠ `accepter_choix` (le pilote prend le MAXIMUM de la fourchette) est ce qui fait defausser plus de 0 carte ; `surpayer` paie des RESSOURCES et ne sert a rien ici (premier essai : 0 degat). X = 1, 2 et 3 mesures (reprise).
- **`bf003`** : `UpdateNextCardPlayCost(joueur, -exces, in_this="Phase")`, joueur = celui qui joue la carte. L'exces n'existe qu'a la DEFAITE (recette 7duodecies) : un ennemi qui survit ne reduit rien (temoin).

## Defauts de MESURE de mes propres cas (corriges, pas contournes)

- `AddTraitToPaper` n'agissait pas sur une carte DEJA creee (le deck de rencontre du scenario l'est des la mise en place) : 4 cas rouges (bf001a bonus, bf004 x2 ...). L'aide fait maintenant relire la fiche aux faces existantes (`ResetTrait`). Les temoins etaient verts pour de mauvaises raisons tant que ce defaut durait : seul le cas NOMINAL le voyait.
- `bf005` : « Whiplash introuvable en jeu » etait un echec de MESURE, pas de carte : Whiplash (PV 4) est VAINCU par les 4 degats. Attendu corrige en `hors_jeu`.

## Manques (a dire noir sur blanc)

1. **Partie reelle seulement PARTIELLE** (voir « Reprise » : chaine jusqu'a Angelus et Bring on the Night faite en Chromium, le reste non). A regarder en priorite : la chaine HELLMOUTH au complet (Harvest -> Becoming -> Faith / Enemies Aligned -> Scythe, The Master -> Angelus), la Reponse « Chosen One », Hush (peril sur chaque carte rencontre, puis l'action de 3 ressources), Redeemed, Slayer Strike (le pilote prend le MAXIMUM de cartes a defausser).
2. **Multijoueur** non teste : Watcher's Guidance, la Scythe (`AnyPlayerCanDoThis`), The Gentlemen, `ChoisirUnJoueur`, Giles / Sunnydale Library (« choose a player »).
3. **Cas plateau (etape 8 bis)** : `ui-app/src/board/buffy-plateau.test.ts`, 3 cas verts (Mr. Pointy sur Buffy, allie racheté + Redeemed attachée, The Master et Harvest). ⚠ Passes au vert directement (le correctif generique de `zones.ts` existait) : jamais vus rouges. Le rendu reel de la mise de cote n'est PAS verifie.
4. ~~Batterie complete~~ FAITE (reprise du 31/10 soir) : aucune regression imputable a `card_face.py` / `puzzle.py` (voir « Reprise »). Les 7 echecs `[wn]` sont anterieurs a mes modifs.
5. ~~Biographie~~ PROUVEE dans le wizard (31/10 soir, Chromium). L'entree existe (`bf001a`), chargee sans erreur par node.
6. Images non versionnees (`assets/pics/` ignore par git) : a recopier sur une autre machine. Les 3 ressources basiques illustrees (Genius, Strength, Energy) et l'illustration violette de Buffy ne sont PAS importees.
7. Boosts des cartes encounter lus sur les scans (Welcome to Sunnydale : 1, a confirmer).

---

### bf001a : * Buffy (face heros)

- [x] Etape 2 : carte(s) de reference : `mw001a` Madame Web (`ThisGainKeyword(fn, attack=1, thwart=1, defense=1)`) ; `howard_the_duck/hd002` et `ThisGainKeywordWhileFaceIsInVictoryDisplay` (decompte de la zone de victoire, `OnEvent.Victory`) ; `hd001a` (`AfterCardEnterPlay(Response, <type>, op).LimitOncePerRound()`).
- [x] Etape 5 : mots-pieges verifies : « Buffy gets » (nom propre : face heros seule) ; « each basic power » (ATQ, CTR, DEF) ; « for each ... in the victory display » (zone de victoire, trait HELLMOUTH, manigance annexe) ; « a minion enters play » (tout sbire) ; Response nu (pas Hero Response) ; « Limit once per round ». Resultat : conforme.
- [x] Etape 6 : nombres texte <-> code : PV 10, ATQ 1, CTR 1, DEF 1, main 5 (scan) = `desc` ; +1 par manigance ; 1 carte piochee. Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : bonus (2 HELLMOUTH -> +2/+2/+2), Chosen One (main 1 -> 2). Rouges 3/6 sans module ; les 3 verts sont des temoins d'absence.
- [x] Etape 7 bis : limite imprimee ? OUI. Temoin d'epuisement : `bf001a Chosen One — TEMOIN D'EPUISEMENT` : deux sbires dans le meme round, main a 2 et non 3. Rouge sans module (main a 1).
- [x] Etape 8 : autoplay cible : voir l'en-tete.
- [x] Etape 8 bis : la carte change-t-elle ce qu'on VOIT ? NON (jauges de stats et pioche).

Carte terminee : NON : aucune partie reelle humaine ; le bonus se mesure sur des manigances HELLMOUTH de substitution (les vraies sont a 3-4 menaces).

### bf001b : * Buffy Summers (face alter-ego)

- [x] Etape 2 : `ok001b` / `an001b` (`WhenCardSetup`, recherche deck + defausse + `GainCard`) ; `mv013` (`Search.EncounterCard(include_set_aside=True)` + `Reveal`) ; `Faces.SetAside` ; fiches `mots-cles/find.md` et `setup.md` (lues APRES l'ecriture du script : elles ont fait ajouter la zone de mise de cote).
- [x] Etape 5 : mots-pieges verifies : « deck AND discard pile » ; « Set ... aside, out of play » ; « Find ... and reveal them » (deux recherches, apres la mise de cote) ; Action nue sans limite ; « Harvest » nu = traitrise officielle (filtre Minion). Resultat : conforme, avec l'hypothese « sbires » ecrite plus haut.
- [x] Etape 6 : PV 10, REC 3, main 6 (scan) = `desc`. Aucun autre nombre.
- [x] Etape 7 : Setup (deux sbires reveles, HELLMOUTH mise de cote, la non-HELLMOUTH reste), Setup avec un sbire « The Master » HELLMOUTH mis de cote puis retrouve dans la zone de mise de cote, Setup avec la traitrise 05029 (reste dans le deck), Chosen depuis le deck, Chosen depuis la defausse, Chosen sans Mr. Pointy (main inchangee). Rouges 5/6 sans module (le vert : « Harvest » nu).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : voir l'en-tete (l'Action « Chosen » apparait dans le journal, sans effet : Mr. Pointy n'existe pas).
- [ ] Etape 8 bis : met des cartes de cote (OUI), pas de cas plateau : voir Manque 4.

Carte terminee : NON : aucune partie reelle humaine ; Setup mesure sur la vraie partie (Harvest et The Master reveles), Chosen sur le vrai Mr. Pointy.

### bf002 : * Rupert Giles

- [x] Etape 2 : `hd001a` (`AfterCardEnterPlay(Response, "This", op)`) ; `25008` (`SetTarget(Scheme2)` + `RemoveThreatFromSchemes`).
- [x] Etape 5 : mots-pieges verifies : « a scheme » (principal OU annexe) ; « 3 threat instead if Watcher's Guidance is in play » (valeur choisie a la resolution, par le nom). Resultat : conforme.
- [x] Etape 6 : cout 3, THW 2*, ATQ 1*, PV 3, ressource mentale ; 2 puis 3 menaces. Resultat : vert.
- [x] Etape 7 : 6 -> 4 menaces sans Watcher's Guidance ; 6 -> 3 avec (substitution 01093). Rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : Giles jouee dans la partie 1 sans exception.
- [x] Etape 8 bis : NON.

Carte terminee : NON : aucune partie reelle humaine (Watcher's Guidance reelle, bf011).

### bf003 : Slay Time (x2)

- [x] Etape 2 : `13013` Into the Fray (`if_this_attack_deal_excess_damage`) ; `16169` Sure Gamble (`UpdateNextCardPlayCost(.., in_this="Phase")`).
- [x] Etape 5 : mots-pieges verifies : « excess damage » (a la defaite seulement, 7duodecies) ; « the next card YOU play » (joueur de l'evenement) ; « this phase » ; « for each point » (reduction = exces). Resultat : conforme.
- [x] Etape 6 : cout 2, ressource physique ; 4 degats ; reduction de 1 par point. Vert.
- [x] Etape 7 : Hydra Mercenary (PV 3) prend 4 : 1 d'exces, Giles (3) coute 2 et est jouee avec une seule carte restante ; temoin Rhino (survit) : Giles reste en main. Rouges 2/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : la carte est piochee et utilisee comme ressource dans les journaux (jamais jouee comme attaque : le pilote reste en alter-ego).
- [x] Etape 8 bis : NON.

Carte terminee : NON : aucune partie reelle humaine. Le second exemplaire a le meme `card_id` : un seul jeu de cas.

### bf004 : Bring on the Night (x2)

- [x] Etape 2 : `09007` Protective Ward (`WhenPlayerRevealCard(HeroInterrupt, "AnyPlayer", .., "All", .., from_encounter=True).SetPlay()` + `CancelAllEffectsAndDiscardIt`) ; `01075` Black Widow (type `None`) ; `ChooseAbilities` + `ForChoiceAbility`.
- [x] Etape 5 : mots-pieges verifies : « an encounter card » (tout type) ; « cancel all of its effects and discard it » (avant le choix) ; « equal to the number of HELLMOUTH side schemes in the victory display » ; « damage to an enemy OR remove threat » (un seul). Resultat : conforme.
- [x] Etape 6 : cout 2, ressource mentale ; nombre lu a la resolution. Vert.
- [x] Etape 7 : sbire annule et 2 degats (2 HELLMOUTH) ; temoin 0 HELLMOUTH (annule, 0 degat) ; traitrise annulee (Rhino ne guerit pas, 5 + 2 = 7). Rouges 3/3. La branche « remove threat » est mesuree a la reprise (`preferer_option`).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : non jouee (alter-ego).
- [x] Etape 8 bis : NON (annulation + degats / menace).

Carte terminee : NON : aucune partie reelle humaine ; decompte mesure sur des manigances de substitution.

### bf005 : Slayer Strike (x2)

- [x] Etape 2 : `03006` Shield Toss (meme texte sans le retour du bouclier).
- [x] Etape 5 : mots-pieges verifies : « X cards ... X enemies » (X = defausse reelle) ; « from your hand » ; « 4 damage to X enemies » (4 a chacun). Resultat : conforme.
- [x] Etape 6 : cout 0, ressource energie ; 4 degats. Vert.
- [x] Etape 7 : X = 2 : Rhino prend 4, Whiplash est vaincu ; les 3 cartes en defausse. Rouge sans module (1/1). X = 1 et X = 3 mesures a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay cible : non jouee (alter-ego).
- [x] Etape 8 bis : NON.

Carte terminee : NON : aucune partie reelle humaine.

### bf006 : * Faith

- [x] Etape 2 : `wt020` / `40024` (`WhenUnitWouldBeDefeated(Interrupt, "This", op)`) ; `Faces.ReadyAll` ; `CardFinder2(trait, Friend)`. Mot-cle `linked` (fiche `mots-cles/linked.md`).
- [x] Etape 5 : mots-pieges verifies : « When Faith is defeated » (interruption AVANT la defaite) ; « a friendly SLAYER character » (identite ou allie, Faith elle-meme incluse) ; « ready ». « Linked (Faith minion) » : pas de `desc.Linked` (voir Ecarts). Resultat : conforme.
- [x] Etape 6 : cout 3, THW 1*, ATQ 2*, PV 3, ressource wild. Vert.
- [x] Etape 7 : Buffy inclinee, Faith vaincue : Buffy redressee. Rouge sans module (1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : jamais en jeu (Linked).
- [x] Etape 8 bis : NON.

Carte terminee : NON : aucune partie reelle humaine ; accessible en partie par `bf031` (Linked par card_id).

### bf007 : * Slayer Scythe

- [x] Etape 2 : `06008` God of Thunder (`CanGenerateResources(HeroResource, ..)` + `Exhaust("This")`) ; `fne/echo/60043` (`AnyPlayerCanDoThis`). `Restricted` lu dans `desc`.
- [x] Etape 5 : mots-pieges verifies : « Hero Resource » (forme heros seule) ; « any player may trigger » ; « [wild] ». « Linked (Enemies Aligned) » : pas de `desc.Linked` (voir Ecarts). Resultat : conforme.
- [x] Etape 6 : cout 2, ressource wild, Restricted 1. Vert.
- [x] Etape 7 : Giles (3) payee grace a la Scythe, la Scythe s'incline ; temoin alter-ego : Scythe prete, Giles en main. Rouges 1/2.
- [x] Etape 7 bis : limite imprimee ? NON.
- [x] Etape 8 : autoplay : jamais en jeu (Linked).
- [x] Etape 8 bis : NON.

Carte terminee : NON : aucune partie reelle humaine ; accessible par `bf029` ; ressource offerte a un autre joueur non testee.

---

## Cartes ajoutees apres reception des images (bf008-bf032)

Chaque carte : etapes 2, 5, 6, 7 faites ; etape 7 bis : aucune limite imprimee sur ces cartes (la limite de bf001a est dans sa fiche) ; etape 8 : autoplay de 8 parties du deck complet, 0 exception, aucune de ces cartes lue dans un journal ligne a ligne ; etape 8 bis : voir « Manques » 3.

### bf008 : Pointy End (x2)

- [x] Etape 2 : carte(s) de reference : 01053 Relentless Assault (`AttackProperty(overkill=True)`) ; mv005 (`Exhaust(.., name=..)`).
- [x] Etape 5 : mots-pieges verifies : « Exhaust Mr. Pointy » = cout ; « an enemy » ; « overkill » (l'exces n'est PAS mesure). Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 3, [physical], 8 degats (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : 8 degats a Rhino + Pointy incline ; temoin sans Pointy : en main (rouges 1/2).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf009 : Crimson Scythe

- [x] Etape 2 : carte(s) de reference : dr006 Awaken Nature (each enemy / each scheme) ; 08018 (condition de jeu).
- [x] Etape 5 : mots-pieges verifies : « Play only if you control the Slayer Scythe » ; « each scheme / each enemy » ; 1 [per_hero] (mesure en SOLO seulement). Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 2, [energy] (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : menace -1 et 1 degat a Rhino ET Whiplash ; temoin sans Scythe (rouges 1/2).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf010 : Sunnydale Library

- [x] Etape 2 : carte(s) de reference : `GiveKeywordToInPlayWhenApplyThis` (ra001b) ; mv001b (`SetTarget("Players")`).
- [x] Etape 5 : mots-pieges verifies : « Buffy Summers gets » nom propre (alter-ego) ; « that player shuffles from THEIR discard pile » ; identity-specific = classe Hero (QUESTION 5). Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 1, [mental], +2 REC (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : +2 REC ; Giles revient de la defausse (rouges 2/2).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf011 : Watcher's Guidance

- [x] Etape 2 : carte(s) de reference : 40197 Safehouse (`ChooseAbilities`, `AnyPlayerCanDoThis`).
- [x] Etape 5 : mots-pieges verifies : « Action » nue (deux formes) ; « an identity » (toute identite) ; une branche ; MULTIJOUEUR non teste. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 1, [mental] (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : branche 1 mesuree seule : menace 3 -> 2 (rouges 1/1). Branches 2 et 3 mesurees a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf012 : Redeemed

- [x] Etape 2 : carte(s) de reference : 51036 Redemption, 34009 Mind Control (`TakeControlOfAttachedMinion`) ; 27189b (`AttachTo2`).
- [x] Etape 5 : mots-pieges verifies : « non-ELITE » ; Response optionnelle ; THW = SCH imprime et degat consequent 1 : rendus par `TreatAsAlly`, mesures a la reprise. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 4, [mental] (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : le sbire entre en jeu, la carte s'y attache, il porte le trait SLAYER (rouges 1/1). THW et degat consequent mesures a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf013 : Stakeout

- [x] Etape 2 : carte(s) de reference : 08010 Widow's Bite (texte identique).
- [x] Etape 5 : mots-pieges verifies : « Hero Response (attack) » ; « discard » = cout ; « that minion ». Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 1, [physical], 2 degats (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : 2 degats et Sonne, defaussee (rouges 1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf014 : * Mr. Pointy

- [x] Etape 2 : carte(s) de reference : 43009 Adamantium Lacing ; 04012 Black Knight (`is_basic_attack=True, piercing=True`).
- [x] Etape 5 : mots-pieges verifies : « Buffy » face heros ; « basic attacks » seulement ; Restricted : `desc`. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 1, [wild] (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Riposte 1 ; l'attaque de base ignore Tenace de Sandman (rouges 2/2).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf015 : * Kendra

- [x] Etape 2 : carte(s) de reference : 01066 Hawkeye (`ThisEnterPlayWithCounters`, `CostFunc.Counter`).
- [x] Etape 5 : mots-pieges verifies : « enters play with 3 stake counters » ; « remove 1 » = cout ; Victory 0 : `desc`. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 0, [physical], THW 1*, ATQ 1*, PV 3 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : 3 compteurs a l'entree ; -1 et 2 degats (rouges 2/2).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf016 : * Willow

- [x] Etape 2 : carte(s) de reference : 49013 Kid Omega (`ForChoiceAbilityWithCost`) ; `AfterUnitUseBasicPower`.
- [x] Etape 5 : mots-pieges verifies : « uses a basic power » (ATQ ou CTR) ; trois branches, UNE ressource. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 3, [wild], THW 1*, ATQ 1*, PV 3 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : branche [mental] mesuree (menace 4 -> 3 par le contre, puis -2 = 1) ; branches [physical] et [energy] mesurees a la reprise (le soin de 2 laisse 1 degat : consequent imprime).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf017 : * Angel

- [x] Etape 2 : carte(s) de reference : 04012 (piercing) ; bt001b (`AfterUnitChangeForm`).
- [x] Etape 5 : mots-pieges verifies : « After YOU change to alter-ego form » ; « attacks » (pas seulement de base) ; Linked (Angelus) par card_id. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 4, [wild], THW 2*, ATQ 2*, PV 3 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : soin de 1 au passage en alter-ego ; attaque perforante contre Sandman (rouges 2/2).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf018 : Chosen One

- [x] Etape 2 : carte(s) de reference : mv001a (`Cost("1")`) ; `Faces.ReadyAll`.
- [x] Etape 5 : mots-pieges verifies : « Exhaust AND spend 1 resource » : deux couts ; « ready Buffy » = le heros. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : cout 2, [wild] (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Buffy redressee, carte inclinee (rouges 1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf019 : Prophecy Girl

- [x] Etape 2 : carte(s) de reference : `WhenUnitWouldTakeDamage` ; mv012 ; `Search.SearchForCard`.
- [x] Etape 5 : mots-pieges verifies : LECTURE PROVISOIRE (QUESTION 1) ; « under your control » ; « remove this card from the game ». Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : sans cout (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Buffy 10 PV subit 8 : Kendra en jeu, carte retiree (rouges 1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf020 : Welcome to Sunnydale

- [x] Etape 2 : carte(s) de reference : 50085 Mad Science, 30031 Bora ; 16140 (`RevealThisCard`).
- [x] Etape 5 : mots-pieges verifies : Hinder 1[per_hero] : `desc` ; « each VAMPIRE minion » ; boost lu 1 (QUESTION 2). Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : menace 3, Hinder 1* (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : icone d'acceleration sur Spike (mesure : 2 avec The Master deja en jeu) ; temoin non VAMPIRE (rouges 2/2). Le boost « Reveal this card » est mesure a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf021 : * Spike

- [x] Etape 2 : carte(s) de reference : 01050 / 01024 (`AfterUnitAttackEnd`) ; `Worlds.DiscardEncounterTopCard`.
- [x] Etape 5 : mots-pieges verifies : « attacks AND damages a character » (`damaged_targets`) ; « treachery » ; « heal ALL ». Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : SCH 2, ATQ 2*, PV 5, boost 2 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : traitrise : Spike soigne ; temoin sbire : garde ses 2 degats (rouges 1/2, le vert est le temoin). ⚠ `defausse_rencontre` lit une AUTRE pile que celle ou Spike defausse : cle retiree.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf022 : * Drusilla

- [x] Etape 2 : carte(s) de reference : 30031 Bora (`PlaceThreatOnSchemes("EachScheme")`) ; Teamwork natif.
- [x] Etape 5 : mots-pieges verifies : « attacks YOU » ; « each scheme » ; Teamwork : `desc`, mesure a la reprise. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : SCH 1, ATQ 2*, PV 5, boost 2 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : menace du complot 2 -> 3 (rouges 1/1). Teamwork et « each scheme » (annexes) mesures a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf023 : Hush

- [x] Etape 2 : carte(s) de reference : 39064 (`peril=1` sur `EncounterCard`) ; 60122 (Hero Action payee).
- [x] Etape 5 : mots-pieges verifies : « each encounter card gains peril » : mesure a la reprise ; `Cost("YBR")` ; Gentlemen LIES. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : boost 2 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : les trois ressources payees : Hush defaussee, Gentlemen en jeu (rouges 1/1). Le PERIL et le boost sont mesures a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf024 : The Harvest

- [x] Etape 2 : carte(s) de reference : mv016 (`ChooseAbilities`) ; 01061 (`TakeDamage`) ; Caught Off Guard (`DiscardControlCards(upgrade, support)`).
- [x] Etape 5 : mots-pieges verifies : « upgrade or support » (pas d'allie) ; « highest-cost » = cout imprime ; degats normaux. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : boost 2 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : branche 1 : soutien defausse ; branche 2 : 4 degats (Redeemed, cout 4) (rouges 2/2). ⚠ le pilote joue Bring on the Night en interruption : main isolee dans les cas.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf025 : Normal Again

- [x] Etape 2 : carte(s) de reference : blade (`thirst`, `Uses`) ; `AfterUnitUseBasicPower` ; mv012 (`GetGaveToPlayer`).
- [x] Etape 5 : mots-pieges verifies : « After YOU use a basic power » (tous) ; compteur `sanity` ajoute a l'enum ; Victory 0 : `desc`. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : boost 2, Uses 3 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : 3 compteurs, -1 apres une attaque de Buffy (rouges 1/1). Le palier 0 n'a pas d'effet imprime.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf026 : * The Gentlemen

- [x] Etape 2 : carte(s) de reference : 01112 False Alarm ; 44032 / 27153 (`PlayersCannotTriggerAbility`).
- [x] Etape 5 : mots-pieges verifies : « ALREADY confused » lu avant ; « request Action » (QUESTION 3) ; Linked (Hush). Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : SCH 2, ATQ 2, PV 4, boost 2 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : desorientee ; deja desorientee : soutien defausse (rouges 2/2). La restriction d'Action n'a PAS de cas.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf027 : Harvest

- [x] Etape 2 : carte(s) de reference : 43021 (`WhenSchemeBeDefeated` + mise de cote) ; mv013.
- [x] Etape 5 : mots-pieges verifies : « find Becoming and reveal » ; « the set-aside Prophecy Girl » ; « Harvest » = aussi traitrise 05029 (filtre de type). Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : menace 3, Hinder 1*, Victory 0 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : contree : Becoming revelee et Prophecy Girl en jeu (rouges 1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf028 : Becoming

- [x] Etape 2 : carte(s) de reference : 43021 ; mv013.
- [x] Etape 5 : mots-pieges verifies : deux recherches ; « Faith MINION » (type) ; « the set-aside Chosen upgrade ». Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : menace 3, Hinder 2*, Victory 0 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Enemies Aligned, Faith sbire et Chosen One en jeu (rouges 1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf029 : Enemies Aligned

- [x] Etape 2 : carte(s) de reference : 43021.
- [x] Etape 5 : mots-pieges verifies : « the set-aside Slayer Scythe ». Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : menace 4, Hinder 3*, Victory 0 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Scythe en jeu (rouges 1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf030 : * The Master

- [x] Etape 2 : carte(s) de reference : 32159 Fabian Cortez ; Toughness / Victory natifs.
- [x] Etape 5 : mots-pieges verifies : « engaged with YOUR identity » ; PV 3 par joueur. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : SCH 2, ATQ 2, PV 3* (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Angelus entre en jeu (deux Damage : Tenace absorbe le premier) (rouges 1/1).
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf031 : * Faith (sbire)

- [x] Etape 2 : carte(s) de reference : 27078 (overkill) ; 32159 ; `ChoisirUnJoueur`.
- [x] Etape 5 : mots-pieges verifies : « the set-aside Faith ALLY » (type Ally) ; « under ANY player's control » ; Patrol, Villainous : `desc`. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : SCH 2, ATQ 2*, PV 6, boost 2 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Faith allie en jeu (rouges 1/1). Overkill de ses attaques mesure a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

### bf032 : * Angelus

- [x] Etape 2 : carte(s) de reference : 04012 ; 32159 ; `ChoisirUnJoueur`.
- [x] Etape 5 : mots-pieges verifies : « Angel » (type Ally) ; Guard, Victory : `desc`. Resultat : conforme, sauf mention.
- [x] Etape 6 : nombres texte <-> code : SCH 2, ATQ 2*, PV 7, boost 2 (scan = `desc`). Resultat : vert.
- [x] Etape 7 : cas par capacite, preuve par substitution : Angel en jeu (rouges 1/1). Piercing de ses attaques mesure a la reprise.
- [x] Etape 7 bis : limite imprimee ? NON.
- [ ] Etape 8 bis : ce qu'on VOIT ? cas plateau NON ecrit (voir Manques 3).

Carte terminee : NON : aucune partie reelle humaine ; points non mesures : voir « Reprise » et « Manques » ; questions en attente en tete du fichier.

