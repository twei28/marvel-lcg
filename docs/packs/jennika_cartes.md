# Jennika (TMNT Heroes v3, Inkwire) : gabarits PROCESSUS-CARTE

Preuves du 16/10/2026. Pack `jennika` (prefixe `tj`, set « 185. Custom (Jennika) », a renumeroter a la fusion
avec les autres heros TMNT), 16 `card_id` : `tj001a` Jennika, `tj001b` Jenny, `tj002` a `tj010` signature,
`tj011` Sosaiken (la Voie, mise de cote), `tj012` obligation, `tj013` a `tj015` set `Jennika Nemesis`.
Source : zip « TMNT Heroes-20261014T200300Z-1-001.zip », dossier « TMNT Heroes / Jennika v3 » (25 PNG ;
sept doublons de numero seulement, un seul `card_id` chacun ; « Sosaiken Cardback.png » = dos de la Voie, insert de
regles de construction, AUCUNE carte creee).

**Preuves, en une phrase par outil**
- Cas `test_capacites` : `Fusion/marvel-lcg-src/tools/cas/tmnt_jennika.py` (prefixe `[jennika]`), **95 cas, tous verts**
  (`tools/test_capacites.py .game-src <port> <rapport> "[jennika]"`).
- Substitution : `tools/substituer_pack.py "$PWD/.game-src" 47200 tj` : **15/15 modules** ont au moins un cas rouge sans
  leur module (`tj013` n'a pas de module : sa preuve est la mutation du `desc`, ci-dessous). Les cas qui restent verts sous
  un module vide sont de deux sortes, assumees carte par carte : TEMOINS D'ABSENCE (« l'action n'est pas proposee »,
  « ne declenche rien ») et BASES `desc` automatiques (Retaliate, Toughness, Boost, Uses, Restricted, Permanent,
  statistiques). Empreinte des modules identique avant / apres, `git status` propre.
- Mutation du `desc` (preuve des bases automatiques et des classes Shinobi) : voir la section dediee en fin de fichier.
- `tools/verifier_appels_modules.py "$PWD/.game-src" 47191 jennika` : « OK : tous les appels de jennika existent ».
  **Calibre** : une erreur volontaire (`this.PlaceThreatInexistant`) dans `tj002.py` est bien vue
  (« n'existe pas », 1 appel inexistant), puis le fichier est restaure (§9 de `PROCESSUS-CARTE.md`).
- `DECK_NOM=jennika tools/verifier_tous_les_decks.py "$PWD/.game-src" 47400` : « identite tj001b, main 5, deck 10 »
  (main = taille de main de Jenny : la Voie, mise de cote, n'amputait pas la main). **Calibre** : un deck dont la
  premiere carte est `tj999` echoue au setup (`AssertionError: name_or_id='tj999'`).
- `tools/test_cards.py` : 6430 modules, 0 erreur (construction de toutes les capacites, jennika comprise).
- Autoplay : `tools/autoplay.py --deck jennika --vilains rhino,klaw --difficultes normal --profils equilibre --parties 8` :
  **16 parties, 0 traceback** (grep exhaustif `NameError|AttributeError|TypeError|KeyError|AssertionError|Traceback`
  sur les 16 journaux : 0). Temoin `leonardo`, memes parametres : 16 parties, 0 traceback, memes causes de fin (10
  « All players were eliminated », 6 « The Main Scheme was Completed »), rounds tenus 4,1 / 5,4 (temoin) contre 4,1 / 5,9.
  Les deux decks perdent toutes les parties : leur `player_deck` est vide (consigne du 06/09/2026), le harnais le
  complete avec des ressources inertes. Journal lu : la Voie entre en jeu a chaque partie (32 « entre en jeu »), pioche
  apres les cartes Shinobi (44 lignes « Sosaiken s'active » / « Jennika pioche 1 carte » sur le jeu de journaux), les
  Tekko-Kagi s'equipent et s'inclinent ; seule erreur relevee : `01119` Solid-Sound Body (carte OFFICIELLE, « Hero Action
  failed », sans rapport avec le pack), les « paiement abandonne » sont des messages du moteur apres cet echec, presents
  aussi dans le journal du temoin.
- Plateau (etape 8 bis) : `ui-app/src/board/tmnt-jennika-plateau.test.ts`, **31 cas verts**
  (`cd ui-app && npx vitest run src/board/tmnt-jennika-plateau.test.ts`), `tsc --noEmit` vert. Le cas se pose sur
  `dessinee(...)` de `plateau-de-test.ts`. Sensibilite prouvee en CASSANT temporairement puis restaurant quatre lignes de
  rendu : (A) `peutPayer` de `interaction.ts` -> 4 cas rouges (Tekko-Kagi non cliquables) ; (B) `attachees` de `zones.ts` -> 17
  rouges ; (C) `exhausted` de `card-model.ts` -> 6 rouges ; (D) zone `retirees` de `zones.ts` -> 1 rouge (obligation retiree).
  Aucun vrai trou d'affichage trouve : l'UI etait deja correcte, il n'y a donc PAS de correctif a faire preceder d'un cas
  rouge. Les Tekko-Kagi sont dessinees comme des ameliorations ordinaires : la paire 14/15 (illustration continue) n'est
  PAS declaree au registre des panoramas (consigne : signaler seulement).
- Vitest complet : 3612 verts, **2 rouges hors perimetre** (`bulles-arts-alternatifs.test.ts`, qui lit `assets/pics` : la
  copie de travail n'a que les 16 JPEG de Jennika, pas les arts alternatifs officiels).

**Icones de ressource verifiees par decoupe** du coin bas-gauche contre des cartes officielles du jeu de base (`01003`
physique R, `01004` mental B, `01012` energie Y, `01043d` wild G, scans 300x434) : tj002 B, tj003 Y, tj004 R, tj005 B,
tj006 R, tj007 Y, tj008 R, tj009 Y, tj010 Y : TOUTES conformes a `cards.json`. L'etoile du texte de tj009 est le glyphe
« wild » de `04033` Finesse (decoupe cote a cote). L'icone centrale de tj013 est celle de `H` (Hazard) de
`public/fonts/ChampionsIcons.ttf` (fiche `hazard.md`, troisieme methode) : `Hazard 1`. Les deux fleches rouges de
tj012, tj013, tj015 = Boost 2 ; trois fleches sur tj014 = Boost 3. Le rond orange de tj014 / tj015 = PV 1.

**Questions en attente (lectures provisoires, `TODO-QUESTION` dans les scripts)** : `.planning/tmnt/jennika-questions.md`
(Q1 limite « for each Shinobi », Q2 quelles cartes sont Shinobi, Q3 type Path : RESOLUE le 16/10/2026, vrai type Path dans le moteur, Q4 Voie mise de
cote ou dans le deck, Q5 Apparition : deux moities independantes). Une carte dont la lecture est provisoire porte
« OUI (lecture provisoire Qn) » : elle est prouvee POUR CETTE LECTURE ; si l'utilisateur en choisit une autre, la preuve
est a refaire.

**Moteur partage touche (minimal, additif)** : `src/game/card/face/base/card_player.py` (`CARD_CLASS` : `Bushido`,
`Ninjutsu`, `Kuji-Kiri`, `Taijutsu`), `src/game/card/face/card_face.py` (`COUNTER` : `samurai`). Cote UI :
`ui-app/src/board/vocabulaire-moteur.ts` (deux gabarits de libelles d'obligation).

**Hors preuve (a dire noir sur blanc)** : aucune PARTIE REELLE jouee par un humain dans le navigateur ; la fiche biographie
au survol du heros dans l'assistant de preparation n'a pas ete constatee (aucun navigateur ici) : l'entree `tj001a` de
`public/js/prepare/heros-info.js` est ecrite et son JavaScript est syntaxiquement valide ; la traduction posee en
francais (`textes-fr-fanmade.ts` + copie publique regeneree) n'a pas ete vue sur un scan ; le « Setup » est prouve par la
VRAIE mise en place du harnais (la Voie est fabriquee par `BeginGameWithSetAside`), mais le harnais complete aussi un
deck vide : ne pas s'y fier pour le contenu du `set_aside` (PROCESSUS-HEROS, etape 3).

---

### tj001a : Jennika (Ninja Senpai)
- [x] Étape 2 : `ho006` / `05011` (`WhenPlayerPlayCard`, RECETTES §1) ; `ls004` / `tm011` (`GainUntilRoundEnd`) ; `once_per.py`
      (`LimitOncePerRound`). Aucun mot-cle officiel ; « Shinobi » = notion du pack (`mots-cles/shinobi.md`).
- [x] Étape 5 : mots-pieges : « Jennika gets » (nom propre = face HEROS), « for each Shinobi » (lecture par classe, Q1), « Interrupt »
      (sans « Hero »), « until the end of the round », « a Shinobi card » (une classe portee, Q2). Résultat : OK.
- [x] Étape 6 : PV 12, ATQ 1, CTR 1, DEF 2, main 4 ; bonus +1/+1/+1. Résultat : OK (cas « statistiques imprimees »).
- [x] Étape 7 : quatre cas (Ninjutsu, Taijutsu, Kuji-Kiri, Bushido : +1/+1/+1), deux Shinobi differents +2, temoin Composure
      +0, alter ego +0, fin de round. Rouge 8/11 sans module (les trois verts : temoin Composure, temoin alter ego,
      statistiques `desc`).
- [x] Étape 7 bis : limite OUI ; temoin d'epuisement : deux Ninjutsu dans le meme round -> ATQ +1 et non +2 ; limite PAR classe
      (Ninjutsu puis Bushido : +2) ; cas `jennika_limite_renouvelee` : 4 capacites, une seule verrouillee apres une Ninjutsu,
      aucune apres la fin du round.
- [x] Étape 8 : autoplay 16 parties, 0 traceback (journal : la capacite se declenche sur les cartes Shinobi jouees).
- [x] Étape 8 bis : NON (le bonus se lit sur la jauge, aucune trace sur la table).
Carte terminée : OUI (lecture provisoire Q1, Q2)

### tj001b : Jenny (alter ego)
- [x] Étape 2 : Setup : `wonder_man/58001b` + `58002` (mise de cote + mise en jeu, `BeginGameWithSetAside`) ; Action :
      `michelangelo/tm001b` (deux recherches `may`, mise en jeu inclinee).
- [x] Étape 5 : « under your control », « up to 2 », « deck AND discard pile », « exhausted », cout de defausse, « Action »
      (pas `AlterEgoAction`, modele `si001b`). Résultat : OK.
- [x] Étape 6 : REC 3, PV 12, main 5. Résultat : OK.
- [x] Étape 7 : Setup (la VRAIE mise en place : Voie en jeu, sous controle, un seul exemplaire, main 5) ; Action : 2 Tekko-Kagi
      (deck + defausse) ; une seule ; aucune ; seules les TEKKO-KAGI sont cherchees ; temoin main vide. Rouge 6/9.
- [x] Étape 7 bis : NON. Étape 8 : OK.
- [x] Étape 8 bis : OUI. Cas « tj001b Jenny Setup » (la Voie est dessinee en soutien, la copie mise de cote ne l'est pas) et
      « tj001b Jenny Action » (deux Tekko-Kagi attachees a l'identite, couchees, absentes de la pile du deck), sensibilite
      (B) et (C).
Carte terminée : OUI (lecture provisoire Q4)

### tj002 : Composure (x3)
- [x] Étape 2 : `mts/adam_warlock/21040` Quantum Magic (MEME texte).
- [x] Étape 5 : « Action » (deux formes), « a card in YOUR discard pile », tout type de carte. Étape 6 : cout 1, [mental]. OK.
- [x] Étape 7 : alter ego, forme heros, un evenement repris ; les autres cartes restent en defausse. Rouge 3/3.
- [x] 7 bis NON ; 8 OK ; 8 bis NON (une carte revient en main).
Carte terminée : OUI

### tj003 : Apparition (x2, Kuji-Kiri)
- [x] Étape 2 : `michelangelo/tm006` Majime (deux effets, deux cibles choisies dans le corps) ; `CanBeThwartBy` (Patrouille / Crise).
- [x] Étape 5 : « Action (thwart) », « from A scheme », « confuse AN enemy », independance des deux moities (Q5). Résultat : OK.
- [x] Étape 6 : cout 2, [energy], retrait 2 ; classe `Hero;Kuji-Kiri`. OK.
- [x] Étape 7 : principal, annexe + sbire, CRISE (le principal n'est plus une cible, annexe Crise 3 -> 1) et temoin sans Crise,
      menace plafonnee, forme heros. Rouge 6/6.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (Desoriente pose sur l'ennemi : carte de statut dessinee sur lui, cas « tj003 Apparition,
      tj004 Decisive Strike »).
Carte terminée : OUI (lecture provisoire Q5)

### tj004 : Decisive Strike (x2, Taijutsu)
- [x] Étape 2 : `05015` Tackle (degats puis statut) ; `tl003` / `tl006` (« if you paid ... ») ; lecture du paiement par CARTES :
      `effect.context.paid_this_res_effects` (la carte payeuse est `e.this`).
- [x] Étape 5 : « paid WITH AN ATTACK EVENT » (evenement portant le trait ATTACK, defausse pour sa ressource ; une autre copie
      paie), « deal 3 damage » PUIS « stun THAT enemy », libelle `(attack)`. Résultat : OK.
- [x] Étape 6 : cout 2, [physical], 3 degats. OK.
- [x] Étape 7 : sans evenement ATTACK (carte ressource) : pas d'etourdissement ; avec Haymaker 01087 (ATTACK) : etourdi ; avec
      Backflip 01003 (DEFENSE/SKILL) : pas d'etourdissement ; Repulsor Blast 01031 (ATTACK) : etourdi (Rhino) / sbire vaincu.
      Rouge 5/5.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (carte Stunned dessinee sur l'ennemi).
Carte terminée : OUI

### tj005 : Moonlighting (x2, Ninjutsu)
- [x] Étape 2 : `tl016` / `tl015` / `td005` (`Faces.GiveStatus(..., "Cloaked")`) ; fiches `cloak.md`, `cloaked.md`.
- [x] Étape 5 : « Cloak JENNIKA » (le heros, pas le vilain), « Hero Action ». Étape 6 : cout 0, [mental]. OK.
- [x] Étape 7 : Cloaked sur tj001a (pas sur Rhino) ; Cloaked servie (ATQ 1 + 1 Senpai + 2 = 4) ; deux cartes empilees, chacune
      agit une fois (ATQ 1 + 1 + 2 + 2 = 6). Rouge 3/3.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (carte Cloaked dessinee sous Jennika, sous Street Phantoms).
Carte terminée : OUI

### tj006 : Fearless Resolve (x2, Bushido)
- [x] Étape 2 : `vz032` Klyntar Tendrils / `mf008` (Exhaust + Counter) ; `Faces.ReadyAll`. Mot-cle Uses (`uses.md`).
- [x] Étape 5 : « remove 2 samurai counters » (les DEUX d'un coup), « Exhaust Fearless Resolve AND remove », « ready JENNIKA ».
      Étape 6 : cout 1, [physical], Uses 2,samurai ; compteur `samurai` declare. OK.
- [x] Étape 7 : entre avec 2 compteurs (base `desc`, vert sans module) ; action : Jennika redressee et la carte quitte le jeu
      (rouge) ; Hero Action seulement en forme heros, carte inclinee, un seul compteur : temoins d'absence ; un allie incline
      n'est pas redresse. Rouge 2/6 (les quatre verts : compteurs `desc`, trois temoins d'absence).
- [x] 7 bis NON (aucune limite imprimee) ; 8 OK ; 8 bis OUI (compteurs `samurai` dessines, couchee, defaussee).
Carte terminée : OUI

### tj007 : Jenny's Crib
- [x] Étape 2 : `bkw/black_widow/08005` Safe House #29 ; `sunfire/sf010` (deux couts) ; `DrawUp`, `Faces.ReadyAll`.
- [x] Étape 5 : « Alter-Ego Action », deux couts (incliner ET defausser), « ready YOUR IDENTITY ». Étape 6 : cout 1, [energy]. OK.
- [x] Étape 7 : pioche 1 + identite redressee + Crib inclinee ; temoins : forme heros, main vide, Crib deja inclinee (action non
      proposee). Rouge 1/4 (le cas nominal ; les trois autres sont des temoins d'absence).
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (Crib couchee, identite prete).
Carte terminée : OUI

### tj008 : Jennika's Bow
- [x] Étape 2 : `vz032` (choix degats / menace) ; `ho010` (amelioration a Hero Action) ; `tm011` (Reponse sur un evenement).
- [x] Étape 5 : « damage OR threat » (un seul), « ATTACK OR THWART event » (OU, type Event), « ready THIS ». Restricted : base
      automatique. Étape 6 : cout 3, [physical]. OK.
- [x] Étape 7 : branche degats, branche menace ; Reponse apres Decisive Strike (ATTACK) et Apparition (THWART) ; temoins :
      alter ego, Composure, amelioration. Rouge 4/8 (les quatre verts : temoins d'absence + `desc` Restricted).
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (arc couche / redresse).
Carte terminée : OUI

### tj009 : Jennika's Tekko-Kagi (paire 14/15 avec tj010)
- [x] Étape 2 : `leonardo/tl011` (MEME montage : octroi d'une ressource wild restreinte, couple Can/Do) ; `04033` Finesse.
- [x] Étape 5 : « EACH TEKKO-KAGI upgrade you control GAINS », « Hero RESOURCE », « [wild] for a SHINOBI card ». Étape 6 : cout 1,
      [energy]. OK.
- [x] Étape 7 : deux Tekko-Kagi paient Decisive Strike ; une seule paie Fearless Resolve ; Composure et 01063 refusees ; alter
      ego : rien ; l'octroi cesse quand tj009 part ; deux porteurs, effets distincts ; autre joueur : pas d'octroi. Rouge 4/9
      (les verts : refus de Composure / d'aspect, alter ego, octroi qui cesse, tj010 qui s'octroie l'interruption).
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (Tekko-Kagi cliquables comme source de paiement, sensibilite (A)).
Carte terminée : OUI (lecture provisoire Q2)

### tj010 : Jennika's Other Tekko-Kagi (paire 14/15 avec tj009)
- [x] Étape 2 : `tm012` (octroi) ; `cw/56017` (+ATQ et Perçant a l'attaque de base) ; `mf008` (incliner) ; `tm001b` (defausse).
- [x] Étape 5 : « EACH TEKKO-KAGI gains », « BASIC attack », deux couts avant la fleche, « +2 ATK FOR THAT ATTACK », Perçant. OK.
- [x] Étape 6 : +2 ATQ ; cout 1, [energy]. OK.
- [x] Étape 7 : +2 ATQ et Perçant (Rhino Tenace prend 3 et perd Tenace) ; l'octroi atteint tj009 ; temoins : sans l'arme (0 degat,
      Tenace seulement), main vide, arme inclinee, evenement d'attaque (pas une attaque de base). Rouge 2/8.
- [x] 7 bis NON ; 8 OK ; 8 bis NON (aucune trace sur la table).
Carte terminée : OUI

### tj011 : Sōsaiken (la Voie, type imprime PATH)
- [x] Étape 2 : `wonder_man/58002` Ionic Physiology (Permanent, mise de cote) ; `tm011` (Reponse + Exhaust).
- [x] Étape 5 : « Response » (deux formes), « After YOU play a Shinobi card », cout d'inclinaison. Permanent : base automatique
      (`permanent.md`). Étape 6 : aucun cout, aucun nombre. OK.
- [x] Étape 7 : pioche apres Ninjutsu, apres Bushido (amelioration), en alter ego ; temoin Composure ; temoin d'epuisement (deux
      Moonlighting : une seule pioche) ; indicateur Permanent. Rouge 4/7 (verts : mise en place, temoin, `desc`).
- [x] TYPE PATH (16/10/2026, decision utilisateur Q3) : type `Path` (`card_type/path.py`), rangee dans l'aire de soutien. Cas
      `jennika_voie_type` (Path et pas Support ; `GetOnFieldSupports` et `GetControlCardsByType(support=True)` ne la voient
      pas ; reste une carte en jeu) : ROUGE avant le type (Support/Support), vert apres ; cas `jennika_voie_permanente` (un
      `RemoveAllFromGame` d'un autre set, Rhino, ne la retire pas) : rouge quand la garde de `HasPermanent` est neutralisee,
      vert sinon. Plateau : genre `path`, etiquette « Voie », zone des soutiens (vitest).
- [x] 7 bis : NON (aucune limite imprimee). 8 OK.
- [x] Étape 8 bis : OUI (Voie dessinee en genre `path`, etiquette « Voie », zone des soutiens, couchee apres sa Reponse).
Carte terminée : OUI (lecture provisoire Q4)

### tj012 : Personality Adjustment (obligation)
- [x] Étape 2 : `qsv/14024` Need for Speed (MEME squelette).
- [x] Étape 5 : « You MAY flip », « Exhaust JENNY » (alter ego + identite prete), « remove FROM THE GAME », seconde branche = 3
      menaces PUIS defausse. Étape 6 : Boost 2, GiveTo « Jenny ». OK.
- [x] Étape 7 : branche 1 (retiree de la partie), branche 2 (3 menaces, defaussee), forme heros bascule refusee (une seule
      branche legale), bascule acceptee puis branche 1, Jenny deja inclinee. Rouge 5/5.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (zone des obligations, cartes retirees, defausse de rencontre) ; sensibilite (D).
Carte terminée : OUI

### tj013 : Dun Import Exports (manigance annexe némésis)
- [x] Étape 2 : `gmw/16066` Blockade (`Hinder`, `StartingThreat`) ; `core/01107` (Hazard).
- [x] Étape 5 : « Hinder 1[per_hero] » (desc `1*`), « Incite 2 », icone Hazard (decoupe contre le glyphe). Aucun script.
- [x] Étape 6 : menace de depart 2 (non par joueur), Entrave 1 par joueur, Incite 2, Hazard 1, Boost 2. Résultat : OK.
- [x] Étape 7 : base `desc` automatique, aucun module : preuve par MUTATION du `desc` (section ci-dessous), cinq cas rouges.
      Cas : 3 menaces en solo (2 + 1), 4 a deux joueurs (2 + 2), Incite 2 sur le principal, 1 icone Hazard, 2 icones de boost.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (jeton de menace dessine, zone des manigances annexes).
Carte terminée : OUI

### tj014 : Phantasm (sbire némésis)
- [x] Étape 2 : `leonardo/tl015` Karai (`WhenUnitBeDefeated`, Cloak) ; fiches `cloak.md`, `retaliate.md`, `toughness.md`.
- [x] Étape 5 : « each PHANTOMS MINION in play » (sbires seulement, tous les joueurs, Phantasm lui-meme compris), Riposte 1 /
      Ténacité / Boost 3 : bases `desc`. Étape 6 : MNG 2, ATQ 2, PV 1, Boost 3. OK.
- [x] Étape 7 : When Defeated : chaque PHANTOMS Cloaked, un sbire non PHANTOMS non, seul : aucune erreur (rouge 2/2 sur les cas
      positifs) ; bases `desc` : mutation (section ci-dessous).
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (cartes Cloaked sous les sbires, Phantasm en defausse de rencontre).
Carte terminée : OUI

### tj015 : Street Phantoms (sbire némésis, x3)
- [x] Étape 2 : `leonardo/tl016` Foot Soldiers (MEME effet). Étape 5 : « Cloak STREET PHANTOMS » (la carte elle-meme).
- [x] Étape 6 : MNG 1, ATQ 1, PV 1, Boost 2, Ténacité. OK.
- [x] Étape 7 : When Revealed : Cloaked sur la carte (rouge 1/1 sur le cas nominal) ; bases `desc` : mutation.
- [x] 7 bis NON ; 8 OK ; 8 bis OUI (carte Cloaked sous Street Phantoms).
Carte terminée : OUI

---

## Mutation du `desc` (bases automatiques et classes Shinobi)

Les cartes sans module (`tj013`) et les bases lues dans le `desc` ne peuvent pas etre prouvees par substitution : on les
prouve en MUTANT temporairement `data/cards.json` (script jetable, checksum recalcule par `tools/recalculer_checksums.py`),
en relancant les 95 cas, puis en restaurant (`git checkout -- data/cards.json`, checksum « inchange » au retour). Mutations
appliquees en une passe, chacune sur une cle que ne lit qu'un groupe de cas distinct :

| Mutation | Cas qui tombent au rouge |
|---|---|
| `tj013` : Hinder, Incite, Hazard, Boost retires | les 5 cas de tj013 (menace 3 solo, 4 a deux joueurs, Incite, icone Hazard, icones de boost) |
| `tj014` : Retaliate, Toughness, Boost retires, ATQ et MNG ramenes a 1 | Riposte, Tenace (entree + premier coup), Boost 3, valeurs imprimees : 5 cas |
| `tj015` : Toughness, Boost retires | Tenace (cas rendu non vacueux : voir ci-dessous), Boost 2 : 2 cas |
| `tj006` : Uses retire | compteurs a l'entree, Hero Action, redressement : 3 cas |
| `tj008` : Restricted retire | le cas `desc` Restricted |
| `tj011` : Permanent retire | le cas `desc` Permanent |
| classes `Hero;Taijutsu` etc. ramenees a `Hero` | les 4 cas par classe de tj001a, tj001a limites, tj009 (la ressource ne paie plus Fearless Resolve / Decisive Strike), tj011 (la Voie ne pioche plus) |
| ATQ 2 / main 5 de tj001a, REC 2 de tj001b | les 2 cas de statistiques imprimees |

Resultat : **37 cas sur 95 rouges** sous mutation, 58 verts (temoins d'absence, cas de module qui ne lisent aucune de ces
cles). Aucune cle mutee n'est restee sans cas rouge, sauf UNE, trouvee grace a cette passe : le cas « tj015 Street
Phantoms : Tenace » restait VERT avec Toughness retire, parce que son verificateur dedie (`jennika_desc`) ignorait en
silence la cle `statuts` (meme famille que §7bis de RECETTES-MOTEUR). Corrige : `jennika_desc` delegue desormais toutes
les cles qu'il ne lit pas a `etat_attendu`, et le meme cas est rouge sous la meme mutation (`tj015 ne porte pas le statut
Tough`).
