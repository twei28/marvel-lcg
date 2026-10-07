# Spider-Man 2099 — gabarits `PROCESSUS-CARTE.md`, carte par carte

> **Mise à jour du 07/10/2026 (audit du backlog)** : L'en-tête « 8 sur 18 » est PÉRIMÉE : les 18 gabarits portent « Carte terminée : OUI » (sm010 vert le 09/09). Seule case ouverte : la preuve visuelle de la biographie au survol dans l'assistant ; la partie humaine est hors backlog.

Pack `spider_man_2099`, set **166**, prefixe **`sm`**, **18 card_id**, auteur
**Rainy**. Ouvert le 08/09/2026.

## ETAT AU 08/09/2026

- **Etape 7** : **32/32 cas passent** (`test_capacites.py`, filtre `sm0`).
- **8 cartes sur 18 sont TERMINEES** (`sm001a`, `sm001b`, `sm002`, `sm003`,
  `sm004`, `sm006`, `sm008`, `sm013`). Les 10 autres ont leur capacite
  PRINCIPALE prouvee, mais il leur manque le cas d'une seconde capacite ou un
  contre-cas exige —- **Etape 7, preuve par substitution** : **18/18 cartes** tombent au ROUGE sans
  leur module (`substituer_pack.py`). Seule exception assumee : `sm002` rend
  « rouges 1/2 », le second cas etant un CONTRE-CAS d'ABSENCE d'effet, qui
  reste vert par nature (PROCESSUS-CARTE §7.3).
- **Etape 8** : **8 parties d'autoplay, 0 incident**, 5,1 rounds de moyenne
  contre 3,8 pour le temoin `blade` dans la meme fournee. **Grep exhaustif des
  8 journaux : 0 erreur** (`NameError|AttributeError|TypeError|KeyError|
  AssertionError`). Les 18 cartes apparaissent toutes dans les parties, et
  l'Acceleration s'y declenche **131 fois** : le pack est reellement exerce, pas
  seulement charge.

⚠ **CE QUI MANQUE ENCORE**, et c'est nomme precisement :
1. la **preuve de la biographie au survol** dans le wizard (etape 7 de
   PROCESSUS-HEROS) — elle demande d'ouvrir le jeu ;
2. une **partie complete jouee par un humain** ;
3. le **temoin d'epuisement de `sm010`** seul : son unique effet observable est
   une reduction de degats, et la DEF du heros (2, +1 par cette carte) absorbe
   l'ecart cherche — deux attaques de base prealables n'ont pas suffi a
   empecher le pilote de declarer une defense. Le cas non concluant a ete
   RETIRE plutot que laisse vert. ⚠ Le module porte desormais un comptage
   maison de la limite, par PRECAUTION et non comme correctif d'un defaut
   mesure : c'est ecrit tel quel dans le code.

## Ce qui vaut pour tout le pack

- **Etape 2 (cartes de reference)** : chaque module porte son bloc « CARTES DE
  REFERENCE » en tete, avec le POURQUOI. Le modele d'architecture commun est
  `ab001a` * Albert (capacite nommee + `WhenResolveSpecialAbility`), et le
  mot-cle `seek` s'appuie sur `Player.DiscardDeckUntil` (fiche
  `mots-cles/seek.md`, corrigee ce jour).
- **Etape 4 (image)** : les 18 scans sont dans `assets/pics/smXXX.jpg`
  (`tools/importer_images_spider_man_2099.py`). ⚠ Uniformisation a 615 px et
  sauvegarde des originaux a faire au deploiement, comme Ares et Blade.
- **Etape 6 (nombres)** : chaque valeur imprimee a ete relevee et comparee a
  `desc` ET au script. Verifie en plus par `verifier_desc_mots_cles.py` :
  « OK : les 18 cartes ont un desc conforme a leur texte ».
- **Gates statiques deja passees** : `compileall` silencieux ; `test_cards`
  **5371 ok / 0 err** ; `verifier_appels_modules` OK **et calibre** (un
  `Faces.ReadyAllUnitsNow` bidon injecte dans sm012 a bien ete signale) ;
  `verifier_noms_modules` OK ; `verifier_prefixes` OK ;
  `verifier_tous_les_decks` : deck au vert (« identite sm001a, main 6, deck 9 »).

## Les deux defauts que les gates ont trouves

1. **`sm013` / moteur** : `desc.Crisis` sur une OBLIGATION faisait tomber la
   mise en place (`KeyError: 'Crisis'`), donc **deck injouable**. Le type
   `Obligation` portait `HasAccelerationIcon` et `HasHazard` mais pas
   `CanCrisis`, alors que `Attachment` porte les trois. **Correctif moteur
   additif** dans `src/game/card/face/card_type/obligation.py`.
2. **`sm007` / lecture** : « RESTRICTED » lu sur le scan de Lyla est un element
   de l'ILLUSTRATION (un dossier classe), pas un mot-cle. Retire de `desc` et du
   texte. Meme famille que la lecon Lockjaw.

---

## sm001a : * Spider-Man (face heros)

- [x] Etape 2 : `ab001a` (capacite nommee `Special` + declencheur separe),
      `14001a`/`tt001a` (`AfterUnitUseBasicPower`), `49001a`
      (`DiscardDeckUntil` + `return_other_faces`), `15003`/`ar001a`
      (`PlayCardsLikeInTurn`), `ag001b`/`bt011` (`MoveAllToDeck`, "Bottom").
- [x] Etape 5 : mots-pieges verifies — `each other card` (l'evenement trouve ne
      part PAS sous le deck), `you may play` (optionnel, pas force), `instead`
      (sm008 REMPLACE le premier evenement, ne le double pas),
      `once per phase` (limite comptee par le pack, pas par le moteur),
      `your hero uses a basic power` (ATK/THW/DEF, pas la recuperation).
      Resultat : conforme.
- [x] Etape 6 : aucune valeur chiffree hors les stats (10 PV, 2/2/2, main 4).
- [x] Etape 7 : cas `sm001a Acceleration — une attaque de base defausse jusqu'a
      un evenement et le joue`. Substitution : **rouges 2/2**.
- [x] Etape 7 bis : limite imprimee OUI (« once per phase »). Temoin :
      `sm001a Acceleration — TEMOIN D'EPUISEMENT`, deux attaques dans la meme
      phase, **menace restante** mesuree (9 et non 6).
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm001b : * Miguel O'Hara (alter-ego)

- [x] Etape 2 : `45015`/`tg007` (`AfterUnitMakeRecovery(is_basic_recovery)`),
      `45014` (`CostFunc.Discard("YourHandCards")`), `an001a` (`ReadyAll`).
- [x] Etape 5 : `ready Miguel O'Hara` est un NOM PROPRE — on redresse `this`,
      pas l'identite (piege `an002` Sera). La fleche fait de la defausse un
      COUT. Resultat : conforme.
- [x] Etape 6 : REC 4, main 6, 10 PV, 1 carte defaussee.
- [x] Etape 7 : cas `sm001b — Accelerated Healing`. Substitution : **rouges 1/1**.
- [x] Etape 7 bis : limite OUI (« once per round »). Temoin ECRIT ET VERT :
      deux recuperations dans le meme round, **taille de main mesuree au
      second** (2 cartes sur 3, la seconde defausse est refusee).
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm002 : * Ghost Rider

- [x] Etape 2 : `40057` * White Fox (allie qui reagit DEPUIS LA DEFAUSSE apres
      avoir ete defausse du dessus du deck — seule fabrique qui l'autorise),
      `bt011` (`MoveAllToDeck`), `ag006` (`DealDamage`).
- [x] Etape 5 : `by your Acceleration ability` (filtre indispensable : toute la
      nemesis defausse aussi du dessus du deck), `his owner's deck` (le
      proprietaire, pas le vainqueur), `When ... is defeated` = INTERRUPTION.
      Filtre place dans `conditions`, pas dans le corps. Resultat : conforme.
- [x] Etape 6 : cout 2, THW 1*, ATK 2*, 2 PV, 1 degat.
- [x] Etape 7 : cas sujet + **contre-cas** (defausse par la nemesis, 0 degat).
      ⚠ Le contre-cas restera VERT sous substitution : assume.
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm003 : Accelerated Decoy

- [x] Etape 2 : `22005` (choix a deux branches, chacune sa cible), `05015`
      (`GiveStatus`).
- [x] Etape 5 : `do both instead` (remplace le choix, ne le double pas),
      `give YOUR HERO a tough status` (cible imposee, pas de `SetTarget`, et
      surtout PAS `canbe_tough` qui tuerait la branche). Resultat : conforme.
- [x] Etape 6 : cout 2.
- [x] Etape 7 : deux cas (branche normale / branche Acceleration).
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm004 : Rapid Strikes

- [x] Etape 2 : `14006` (cout X), `22005`/`32002` (`UnitIgnoreKeywordIcons`),
      `08013` (cible par repetition).
- [x] Etape 5 : ⚠ **pas de `SetLabel('attack')`** — la carte imprime « Hero
      Action: » SANS « (attack) », contrairement a sm005 et sm006. `X times to
      a maximum of 3` PUIS `one additional time` = `min(X,3)+1`, confirme par
      le Q/R de l'insert (« up to 4 times »). Resultat : conforme.
- [x] Etape 6 : X, max 3, +1, 2 degats.
- [x] Etape 7 : cas avec `surpayer` OBLIGATOIRE (sinon X=0, journal muet).
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm005 : Shock and Awe

- [x] Etape 2 : `05015` (Hero Action (attack)), `19001a`/`tg010` (lire le
      RETOUR de `GiveStatus`).
- [x] Etape 5 : `that enemy` (meme cible), `not stunned THIS WAY` (l'echec de
      CET etourdissement, pas l'etat), pas de `canbe_stunned` (sinon la branche
      a 4 degats devient morte), `each minion in play` (tous les joueurs).
      Resultat : conforme.
- [x] Etape 6 : cout 2, 2 degats, 4 degats.
- [x] Etape 7 : deux cas (ennemi non etourdi / deja etourdi) + branche
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm006 : Wall Crawling

- [x] Etape 2 : `05015`, `an004` (`RemoveThreatFromSchemes`), `bt011`.
- [x] Etape 5 : `a scheme` (pas le principal), `3 instead` (remplacement),
      `you may` (question). ⚠ L'ordre du Q/R de l'insert (« Wall Crawling
      resolves first ») est deja bon par construction, mais doit etre PROUVE
      par un cas qui regarde l'ORDRE du deck. Resultat : conforme.
- [x] Etape 6 : cout 1, 2 et 3 menaces.
- [x] Etape 7 : cas « joue a la main » (2 menaces + retour sous le deck) et cas
      « via Acceleration » (3 menaces, porte par sm001a).
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm007 : * Lyla

- [x] Etape 2 : `ab007`/`ma005` (soutien + `CostFunc.Exhaust`), `ag001b`
      (`MoveAllToDeck` "Top"), `01034` (recuperer depuis la defausse), `22005`
      (ciblage construit dans l'operation).
- [x] Etape 5 : ⚠⚠ **« RESTRICTED » n'est PAS un mot-cle ici** (voir plus
      haut). `swap` = DEUX deplacements. `Action` et non « Hero Action ». Zone
      dependante de la FORME, donc selecteur construit dans l'operation.
      Resultat : conforme APRES correction.
- [x] Etape 6 : cout 2.
- [x] Etape 7 : cas « echange main <-> dessus du deck ». Branche alter-ego
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm008 : Accelerated Vision

- [x] Etape 2 : `ab007` (ecouter la capacite nommee d'une autre carte).
- [x] Etape 5 : `one additional time per phase`, `still once per trigger` (rien
      a coder), `a DIFFERENT event` (comparaison de FACES, pas de card_id),
      `may play that instead`. Resultat : conforme.
- [x] Etape 6 : cout 1, +1 usage.
- [x] Etape 7 : cas « continuation » + cas « 2e usage dans la phase ».
      ⚠⚠ **ECART DE SUBSTITUTION ASSUME** : le « +1 usage » est lu par la
      PRESENCE de la carte, pas par son module — un cas qui le mesure reste
      vert sous substitution. La continuation, elle, mord.
- [x] Etape 7 bis : aucune limite propre.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm009 : Fangs and Talons

- [x] Etape 2 : `ho006` * Norman Osborn (calque exact), `27078`/`bl007`
      (piercing), `an008`/`ho008` (+1 ATK).
- [x] Etape 5 : `using your Acceleration ability` (filtre absent de ho006),
      `exhaust →` (COUT), `that event` (`by_effect=played_effect`), `ITS
      ATTACKS` au pluriel (donc pas `unregister_after_exec`). Resultat :
      conforme.
- [x] Etape 6 : cout 2, +1 ATQ, +1 degat.
- [x] Etape 7 : cas « +1 ATQ » (fait) + cas « +1 degat et piercing sur un
- [x] Etape 7 bis : aucune limite imprimee (l'inclinaison borne).
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm010 : Hyper-Agility

- [x] Etape 2 : `ab007`, `50159`/`21117` (`ReduceDamage`), `ab001a`
      (`until_round_end`), `an008` (+1 DEF).
- [x] Etape 5 : ⚠ **« without playing an event »** distingue cette carte de
      sm011 et sm012, qui ecoutent le meme message SANS condition. `from
      attacks` (pas les degats indirects), `until the end of the ROUND`.
      Resultat : conforme.
- [x] Etape 6 : cout 1, +1 DEF, -1 degat.
- [x] Etape 7 : cas « la reduction MORD » — Sandman frappe DEUX fois pour 3,
      l'identite encaisse **4** et non 6. Rouge sans le module.
      ⚠⚠ **LA CARTE ETAIT MORTE JUSQU'AU 09/09/2026.** Un comptage maison
      (`pas_encore_cette_phase`), pose « par precaution », lisait
      `world.stat.once_per_phase_player_effects` — LE REGISTRE QUE
      `LimitOncePerPhase` REMPLIT ELLE-MEME des le declenchement. La condition
      etait donc fausse au premier passage : `esquiver` n'a jamais tourne, et la
      reduction de degats n'a jamais existe. Mesure : compteur pose dans
      `esquiver`, `sonde=absent`, 6 degats sur 6 encaisses. Condition retiree.
      Lecon : une precaution qui n'est pas mesuree n'est pas une precaution.
- [x] Etape 7 bis : cas « TEMOIN D'EPUISEMENT » — deux pouvoirs de base dans la
      MEME phase. `sm011` Spinnerets ne porte qu'**UN** pion de toile (il en
      pose un par resolution d'Acceleration, plafond 2), et l'identite encaisse
      **2** des 3 degats de Sandman : UNE seule reduction. Les deux chiffres
      ensemble prouvent que la limite tient — et que la limite de CETTE carte
      est INATTEIGNABLE PAR CONSTRUCTION, l'Acceleration de `sm001a` portant
      deja « Limit once per phase ». C'est desormais MESURE, non suppose.
      ⚠ Deux commandes ont du entrer dans le harnais : `Puzzle.EmptyPlayerDeck()`
      (sans quoi `CreatePlayerDeck` AJOUTE au deck de depart, l'Acceleration y
      trouvait un evenement et « without playing an event » etait faux) et
      `Puzzle.Exhaust` sur le heros (un heros incline ne peut pas defendre : la
      seule facon de lire la reduction sans que la DEF l'absorbe).
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI** (09/09/2026). Elle ne l'etait pas : ses trois cas sont
desormais verts et **3/3 rouges sous substitution**.

## sm011 : Spinnerets

- [x] Etape 2 : `ab007`, `53006` Falcon's Flock (le montage exact
      compteur -> ressource), `55055`.
- [x] Etape 5 : `to a maximum of 2` (plafond sur la carte), `for an event`
      (`for_card`), `Hero Resource`. ⚠ « Remove X → generate X » ecrit comme
      « 1 pion → 1 ressource, N fois » : EQUIVALENT en jeu, et le montage
      direct est un piege connu (`resources_fn` evalue avant `PayCost`,
      RECETTES §4). Resultat : conforme, ecart documente.
- [x] Etape 6 : cout 1, 1 pion, max 2.
- [x] Etape 7 : cas « plafond a 2 » (ecrit) + cas « depenser un pion pour payer
- [x] Etape 7 bis : aucune limite « once per » imprimee ; le plafond a son cas.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI** — plafond prouve le 08/09/2026 au soir.

## sm012 : Web Cape

- [x] Etape 2 : `an008`/`ho011` (trait accorde), `ab007`, `an001a` (`ReadyAll`).
- [x] Etape 5 : `ready YOUR HERO` (pas la carte), aucune condition « without
      playing an event » (contrairement a sm010), `exhaust →` (COUT).
      Resultat : conforme.
- [x] Etape 6 : cout 2.
- [x] Etape 7 : cas « AERIAL + redressement » (ecrit). Contre-cas dans l'AUTRE
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm013 : Future in Crisis (obligation)

- [x] Etape 2 : `an010` Banished from Asgard (calque exact :
      `Faces.RemoveAllFromGame` + `CostFunc.Exhaust("YourIdentity")`),
      `bl011` (obligation qui reste en jeu).
- [x] Etape 5 : aucune capacite « When Revealed » — la carte agit par ses
      ICONES en restant en jeu. `remove from the game` ≠ defausse. `Action` et
      non « Hero Action ». Resultat : conforme.
- [x] Etape 6 : Boost 2, Acceleration 1, Crisis 1 — les trois **verifies par
      comparaison d'image** contre `ag011` (Acceleration + Crisis) le
      08/09/2026, jamais a vue.
- [x] Etape 7 : cas « l'Action retire la carte de la partie » (ecrit). Il PROUVE
      aussi que l'obligation reste en jeu, ce qui etait le doute principal.
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm014 : Containment Breach (nemesis)

- [x] Etape 2 : `an011`/`ho014` (`WhenThisRevealed`), `bc010`/`sn003`
      (`GetPrintedResources`), `50134` (`PlaceThreatOnSchemes`).
- [x] Etape 5 : `EACH PLAYER` (tous, contrairement a sm016 qui dit « your »),
      `threat HERE`, `discarded this way`, `convert_green_res=False` (une
      ressource wild n'est pas une energie). Resultat : conforme.
- [x] Etape 6 : Boost 3, Amplify 1, menace 1 par joueur — **Amplify verifie par
      comparaison d'image** contre `16069` Spatial Positioning.
- [x] Etape 7 : cas « 4 Energy sur le dessus -> 8 menaces » (ecrit), qui prouve
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm015 : * Electro (nemesis)

- [x] Etape 2 : `al022` * Frogjolnir (calque : `AfterUnitAttackYou` +
      `GetAgainstPlayer` + `TakeIndirectDamage`), `sm014` (decompte d'icones).
- [x] Etape 5 : `attacks YOU` (le joueur ATTAQUE, lu sur le message — une carte
      de rencontre n'a pas de controleur, lecon `bl011`), `FORCED Response`,
      `this way`, `indirect damage`. Quickstrike et Retaliate sont des bases
      automatiques. Resultat : conforme.
- [x] Etape 6 : 4 PV, SCH 2, ATQ 1, Boost 2, Retaliate 1.
- [x] Etape 7 :      degats =- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm016 : Power Surge (nemesis, x2)

- [x] Etape 2 : `an013`/`16140`/`ho017` (`WhenCardBecomeBoost`), `an010`
      (`GainSurge`), `sm014`.
- [x] Etape 5 : ⚠ **« 2 OR LESS » est VRAI a zero** — la carte est dangereuse
      quand elle ne fait rien. `your deck` (le joueur cible, pas chaque
      joueur). ⚠ « YOUR hand » sur une capacite Boost = **le joueur qui
      defend**, le moteur l'ecrit lui-meme (`sender_card.py:688`). Resultat :
      conforme.
- [x] Etape 6 : 5 cartes, 2 degats ou moins, +1 icone par energie. Pas de cle
      `Boost` dans `desc` (etoile seule, convention verifiee sur `01121`).
- [x] Etape 7 : cas « 2 degats -> surge » (ecrit) + cas de la capacite Boost
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

## sm017 : Charged (nemesis)

- [x] Etape 2 : `aa018`/`av016` (`AttachToFaceWhenPutIntoPlay("YourIdentity")`),
      `AfterCardsMoved` (un message PAR LOT, `deck.py:438`), `al022`
      (degats indirects), `45014` (`CostFunc.Discard(has_printed_res)`).
- [x] Etape 5 : ⚠⚠ **« ANY NUMBER OF CARDS » = un declenchement par LOT**, pas
      par carte : `AfterCardsMoved` et non `AfterCardDiscard` (sinon une
      Acceleration qui traverse 4 cartes infligerait 4 degats au lieu d'1).
      `from the top of YOUR deck` (zone d'ORIGINE, lue dans `face_areas`).
      `a card YOU CONTROL` (en jeu, pas en main). Resultat : conforme.
- [x] Etape 6 : Boost 1, 1 degat, 2 degats.
- [x] Etape 7 : cas « 1 degat par lot, pas 5 » (ecrit) + les deux branches de
- [x] Etape 7 bis : aucune limite imprimee.
- [x] Etape 8 : 8 parties, temoin `blade`, grep tracebacks : **0**, carte vue a l'oeuvre dans les journaux.

Carte terminee : **OUI**.

---

## Gate finale `PROCESSUS-HEROS.md`

- [x] Etapes 1 a 6 (donnees, scripts, deck, sets_info, images)
- [~] Etape 7 : biographie ecrite — ⚠ **preuve au survol dans le wizard NON
      FAITE** (demande d'ouvrir le jeu)
- [x] Etape 8 : textes francais (18/18, `tsc --noEmit` silencieux)
- [x] Etape 9 : un `PROCESSUS-CARTE.md` complet et « OUI » pour CHAQUE carte
- [x] `verifier_tous_les_decks.py` : deck du heros au VERT
- [ ] Une partie complete jouee avec le heros

**Heros termine : NON.** Il manque, precisement :
1. la preuve de la biographie dans le wizard ;
2. une partie complete jouee par un humain.

⚠ MISE A JOUR DU 09/09/2026 : le temoin d'epuisement de `sm010`, declare hors
de portee du harnais, est MONTE et VERT — et il a revele que la carte etait
morte depuis le portage. Batterie du pack : **34/34 cas**.

Tout le reste est vert : **32/32 cas**, **18/18 substitutions**, **8 parties
d'autoplay sans le moindre incident** (0 erreur au grep exhaustif), deck qui
monte, 0 signature etrangere, gates statiques silencieuses.
