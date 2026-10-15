# Michelangelo (TMNT Heroes v3, Inkwire) : rapport de PHASE A

Date : 2026-10-15. Branche : `worktree-agent-ad454a967bc010e16`.
**PHASE A = construction seulement.** Aucun harnais lance (`test_capacites`,
`autoplay`, `verifier_tous_les_decks`, `substituer_pack`), aucun cas de test
ecrit, aucun gabarit `PROCESSUS-CARTE.md` rempli, aucune carte « terminee ».
Rien n'a ete teste en jeu : le moteur ne monte meme pas dans cet
environnement (`aiohttp` absent, Python 3.12 au lieu de 3.10).

Source : `TMNT Heroes-20261014T200300Z-1-001.zip`, dossier
`TMNT Heroes/Michelangelo v3/` (24 PNG), extrait SEUL dans le scratchpad. Les 24
scans ont ete lus un par un (vision). Les doublons (3/4, 5/6, 7/8, 9/10 du deck ;
3/4/5 de « Bad Stuff ») ont en plus ete compares PIXEL A PIXEL : ils ne different
que par le numero « n/15 » ou « n/5 » du bandeau.

## 1. card_id crees (17, prefixe `tm`, pack `michelangelo`, set 164)

Aucun `tm*` n'existait (verifie sur `cards.json` : aucun id commencant par
`tm`, `tl`, `td`, `tr`). Prefixe declare dans `tools/prefixes_fanmade.json`
(`verifier_prefixes.py` vert, et calibre : rouge sur la copie sans la declaration).

Set `Michelangelo` (dossier de scripts `michelangelo/michelangelo/`) :

| card_id | Nom | Type | Exemplaires | Script |
|---|---|---|---|---|
| tm001a | * Michelangelo | Hero | 1 | oui |
| tm001b | * Mikey | AlterEgo | 1 | oui |
| tm002 | * Slash | Ally | 1 | oui (etoile Perçant) |
| tm003 | Call for Help | Event | 1 | oui |
| tm004 | Impulsive | Event | 2 | oui |
| tm005 | Kaiten | Event (ATTACK) | 2 | oui |
| tm006 | Majime | Event (ATTACK, THWART) | 2 | oui |
| tm007 | Optimism | Resource | 2 | oui |
| tm008 | * Mikey's Couch | Support | 1 | oui |
| tm009 | * I'm Here to Help | PlayerSideScheme | 1 | oui |
| tm010 | * Mikey's Skateboard | Upgrade | 1 | oui |
| tm011 | * Michelangelo's Nunchuck | Upgrade (Restricted) | 1 | oui |
| tm012 | * Michelangelo's Other Nunchuck | Upgrade (Restricted) | 1 | oui |
| tm013 | All Alone | Obligation (GiveTo « Mikey ») | 1 | oui |

Set `Michelangelo Nemesis` (dossier `michelangelo/michelangelo_nemesis/`) :

| card_id | Nom | Type | Exemplaires | Script |
|---|---|---|---|---|
| tm014 | Sewer Problems | SideScheme (Crisis, 4 par heros, Boost 3) | 1 | oui |
| tm015 | * Wyrm | Minion nemesis (Toughness) | 1 | oui |
| tm016 | Smash! | Treachery | 3 | oui |

Deck de depart : 15 cartes signature (`tm002`, `tm003`, `tm004`x2, `tm005`x2,
`tm006`x2, `tm007`x2, `tm008`, `tm009`, `tm010`, `tm011`, `tm012`), obligation
`tm013`, set nemesis `tm014`, `tm015`, `tm016`x3, `player_deck` VIDE (aucune
decklist d'aspect dans le zip).

## 2. Fichiers modifies ou crees

Crees :
- `Fusion/marvel-lcg-src/src/cards/pack/michelangelo/__init__.py`
- `.../michelangelo/michelangelo/__init__.py`, `tm001a.py`, `tm001b.py`, `tm002.py` a `tm013.py`
- `.../michelangelo/michelangelo_nemesis/__init__.py`, `tm014.py`, `tm015.py`, `tm016.py`
- `Fusion/marvel-lcg-src/deck/starter/michelangelo.json`
- `Fusion/marvel-lcg-src/data/nemesis/michelangelo_nemesis.json`
- `Fusion/marvel-lcg-src/tools/importer_images_michelangelo.py` (recette des images)
- `.planning/tmnt/michelangelo-phase-a.md` (ce fichier)

Modifies :
- `Fusion/marvel-lcg-src/data/cards.json` (pack `michelangelo`, 17 entrees, champ `custom: "Inkwire"`, checksum recalcule par le vrai `Types.DictChecksum`)
- `Fusion/marvel-lcg-src/data/sets_info.json` (`164. Custom (Michelangelo)`, checksum recalcule)
- `Fusion/marvel-lcg-src/tools/prefixes_fanmade.json` (prefixe `tm`)
- `Fusion/marvel-lcg-src/public/js/prepare/heros-info.js` (bio `tm001a`)
- `ui-app/src/board/textes-fr-fanmade.ts` (17 textes FR, `tm001a` a `tm016`)

Images : 17 JPEG `assets/pics/tm001a.jpg` a `tm016.jpg` ecrits dans le worktree
(615 px de petit cote, qualite 88) par `tools/importer_images_michelangelo.py`.
**`assets/pics/` est gitignore : ces fichiers ne sont PAS dans le commit.** Pour
les avoir dans le jeu reel, relancer la recette sur le zip extrait :
`python3 tools/importer_images_michelangelo.py "<extrait>/TMNT Heroes/Michelangelo v3"`.
`outils/uniformiser-scans.py` n'a pas ete lance (chemins `/mnt/c/...` en dur,
sauvegarde des originaux hors depot) : la recette en reproduit la regle.
`tm014` (Sewer Problems) est livree en portrait avec la carte tournee de 90
degres : la recette la remet a l'endroit (verifie a l'oeil, 882x615).

Non touches : aucun fichier moteur partage (`card_face.py`, `factory.py`,
`app.js`, `test_capacites.py`, `autoplay.py`). Traits neufs (NUNCHUCK, NINJA,
TURTLE, MUTANIMAL, TEENAGER, NYC, SEWERS, WORMS) : le champ `traits` n'est lu a
l'execution que par Teamwork (precedent sunfire, qui a ajoute NINJA sans toucher
l'enum). Pas de bouton onomatopee dans `app.js` (cosmetique facultative).

Fichiers PARTAGES avec les trois autres agents (conflits de fusion previsibles) :
`cards.json` et `sets_info.json` (insertion juste avant `checksum`, **recalculer
les deux checksums apres fusion** : `recalculer_checksums.py`),
`prefixes_fanmade.json`, `textes-fr-fanmade.ts` (fin de fichier),
`heros-info.js` (fin de fichier). Le numero de set `164` a probablement ete pris
aussi par un autre agent : renumeroter a la fusion.

## 3. Verifications statiques faites (et leurs limites)

- Tous les `.py` compilent (`py_compile`), JSON valides, `node --check heros-info.js` vert.
- `verifier_prefixes.py` : vert (calibre : rouge sur une copie sans le prefixe `tm`).
- Homonymes : AUCUN des 17 noms n'existe dans `cards.json` ni `cards_custom.json`
  (script calibre : trouve bien « Rhino »).
- Controle etape 10 de PROCESSUS-HEROS (signature d'un autre heros) : `player_deck`
  vide, donc rien a controler.
- `verifier_appels_modules.py` : **NON UTILISABLE** ici (le moteur ne s'initialise
  pas : `ModuleNotFoundError: aiohttp`, sur une COPIE du moteur dans le
  scratchpad, jamais sur le depot). Remplace par une verification GROSSIERE
  maison (`noms_existent.py`, hors depot) : chaque `X.methode` des modules doit
  exister quelque part dans `src/`. Calibree (attrape `Faces.ZzzPasLaMethode`).
  **Limite : n'attrape que les fautes de frappe, pas une methode qui existe mais
  pas sur CE type.** La vraie gate `verifier_appels_modules` reste due en phase C.
- Resources : l'icone de ressource de chaque carte a ete COMPAREE a des cartes du
  pack Lady Sif de ressource connue (planche de recoupe : `ls010`=R poing rouge,
  `ls005`=Y eclair jaune, `ls007`=B noeuds bleus, `ls002`=G etoile verte). Resultat :
  tm002, tm005, tm010 = R ; tm003, tm004, tm009, tm011, tm012 = Y ; tm006, tm008 = B ;
  tm007 = G. (Pas de carte de ressource connue DANS le pack : la comparaison est
  faite contre un pack voisin, meme famille d'icones.)

## 4. Lecture des cartes : ce qui est certain, ce qui ne l'est pas

Tout est lisible. Points de lecture, non bloquants :
- « Hero Spin » : voir question 8.
- Cout imprime de `tm009` : le coin superieur droit est un cartouche sans chiffre
  lisible. Ecrit `Cost: 0` (cas de toutes les manigances-joueur officielles).
- Les « [star] » : seul `tm002` Slash en porte un (texte + etoile pleine a cote du 3
  d'ATQ). Les etoiles CREUSES sous THW/ATQ de Slash sont des degats consecutifs
  (`THW "0*"`, `ATK "3**"`).
- `tm014` : l'icone au centre est lue comme CRISIS (voir question 7).
- `tm015` : le trait imprime « WORMS! » est range `WORMS`.
- L'insert (« Michelangelo Insert.png ») n'est pas une carte : ses regles sont
  integrees aux scripts (Nunchuck entrent inclines par l'Action d'alter-ego ;
  « +1 a un pouvoir de base apres un evenement » ; « reduire de 1 + 1 degat » ;
  la manigance ne pioche que sous forme de heros).

## 5. Questions en attente (8)

Ordre = ordre de priorite. Chaque question est liee a un `# TODO-QUESTION` dans le
script concerne. Les scripts sont ecrits pour l'option RECOMMANDEE (la plus
litterale), sauf mention contraire.

### Question 1 : `tm001b` Mikey / `tm009` I'm Here to Help : d'ou vient la manigance au Setup ?

Texte imprime (tm001b) : « **Setup**: Put the I'm Here to Help player side scheme
into play. » ; tm009 est la carte « MICHELANGELO (12/15) », donc l'une des 15 du
deck ; tm003 la cherche dans « your deck and discard pile ».

1. **(recommande, ecrit)** Fouiller le deck au Setup (`WhenCardSetup` +
   `Search.PlayerCard(card_ids=["tm009"])` + `PutIntoPlay`), tm009 restant dans
   `hero_deck` (15 cartes). En jeu : la manigance est TOUJOURS en jeu des le tour 1 ;
   le deck de depart pioche 14 autres cartes ; une fois defaite, elle va en defausse
   et tm003 peut la recuperer. Le deck est melange par la fouille.
2. La mettre de cote (`set_aside` + `BeginGameWithSetAside`, hero_deck a 14). En
   jeu : meme resultat au tour 1 mais le deck fait 14 cartes, et tm003 ne la
   trouverait qu'en defausse apres une premiere defaite. Contredit « 12/15 » et le
   « deck » de tm003.
3. Autre (precise).

### Question 2 : `tm006` Majime : X = degats declares ou degats reellement subis ?

Texte : « **Hero Action** (attack/thwart): Take X damage (to a maximum of 3) →
remove X threat from a scheme and deal X damage to an enemy. »

1. **(recommande, ecrit)** X = le nombre DECLARE (0 a 3), meme si Robuste ou une
   prevention annule les degats (un cout de degats est paye meme prevenu, cf.
   `CostFunc.DealDamage`). En jeu : un heros Robuste subit 0 mais retire/inflige X ;
   la carte est plus forte avec Robuste.
2. X = degats reellement subis (comme `dt028` Pay It Forward). En jeu : Robuste ou
   une prevention reduit X, donc l'effet ; la carte est plus fidele a l'esprit
   « je paie du sang pour de l'effet ».
3. Autre (precise).

### Question 3 : `tm001a` Booyakasha : deplacer de la menace, defaite et Crise

Texte : « move up to 3 threat from one scheme to another scheme. You cannot move
threat onto a side scheme with 5[per_hero] or more threat on it. »

1. **(recommande, ecrit)** `MoveThreat` du moteur : une annexe videe est VAINCUE
   (effets « When Defeated » sans joueur vainqueur), Crise ne bloque PAS un
   deplacement depuis la manigance principale, le minimum propose est 1. En jeu :
   on peut finir une annexe en deplacant sa menace ; on peut drainer la principale
   meme sous Crise.
2. Comme 1, mais Crise bloque aussi les deplacements DEPUIS la principale. En jeu :
   Booyakasha ne contourne plus Crise.
3. Interdire de vider entierement une annexe. En jeu : jamais de defaite par
   deplacement.
4. Autre (precise).

### Question 4 : `tm004` Impulsive : sans WEAPON en jeu ?

Texte : « Place 2 threat on the main scheme → ready Michelangelo and a WEAPON you
control. Draw 1 card. »

1. **(recommande, ecrit)** Se joue sans arme : on pose 2 menaces, on redresse le
   heros, on pioche. En jeu : carte jouable partout (mais on paie 2 menaces sans
   gain d'arme).
2. Injouable sans WEAPON controlee. En jeu : on ne paye jamais les 2 menaces pour
   un redressement partiel ; la carte est morte en main sans Nunchuck.
3. Autre (precise).

### Question 5 : `tm009` : « only the Michelangelo player can trigger this ability »

Texte : « **Hero Interrupt**: When this scheme is defeated, draw 3 cards (only the
Michelangelo player can trigger this ability). » + insert : « you must be in hero
form to draw the 3 cards ».

1. **(recommande, ecrit)** Interruption de HEROS (forme de heros exigee par le
   type) ET l'initiateur doit etre le PROPRIETAIRE de la carte ; le proprietaire
   pioche. En jeu : si un autre joueur defait la manigance, ou si Michelangelo est en
   alter-ego, personne ne pioche.
2. Sans test de proprietaire : le joueur qui a le controle pioche. En jeu :
   identique en solo, differe seulement en multijoueur.
3. Autre (precise).

### Question 6 : `tm011` / `tm012` : « Each NUNCHUCK upgrade you control gains »

1. **(recommande, ecrit)** Chaque carte donne SA capacite a TOUS les NUNCHUCK que
   vous controlez, elle-meme comprise (`GiveAbilityToInPlayWhenApplyThis`). En jeu :
   avec les deux en jeu, chaque Nunchuck porte les deux capacites (2 bonus +1, 2
   ripostes par round maximum) ; avec une seule, elle ne porte que sa propre
   capacite. C'est la lecture de l'insert « either NUNCHUCK (or both) ».
2. Chaque carte ne porte que sa propre capacite. En jeu : au plus 1 bonus +1 et 1
   riposte (une par carte), l'insert « either (or both) » devient decoratif.
3. Autre (precise).

### Question 7 : `tm014` Sewer Problems : l'icone centrale est-elle Crisis ?

Le texte imprime ne mentionne aucun mot-cle ; l'icone au centre (eclat avec « ! »)
est identique a celle de `01108` Crowd Control (Crisis 1). 4 menaces PAR HEROS,
3 icones Boost.

1. **(recommande, ecrit)** Crisis 1 (`desc.Crisis = "1"`). En jeu : tant que la
   manigance est en jeu, on ne retire pas de menace de la principale.
2. Pas de mot-cle (icone decorative). En jeu : simple manigance annexe.
3. Autre (precise).

### Question 8 : « Hero Spin » : variante, art alternatif ?

Le dossier ne contient QU'UNE face heros, nommee « 0 Michelangelo Hero Spin.png »
(stats THW 1 / ATQ 1 / DEF 2, libelle HERO). Il n'y a aucun second fichier a
comparer, donc pas de variante visible.

1. **(recommande, ecrit)** « Hero Spin » = la face heros unique, ids `tm001a`.
   En jeu : rien de plus a gerer.
2. Il manque une autre face heros (a fournir) : la creer en `tm001c`/`tm001d` avec
   `metadata.hero_alts` (GUIDE §5.3) une fois le scan fourni.
3. Autre (precise).

## 6. Capacites a tester en phase C (par card_id)

Rappel : un cas `test_capacites` par capacite, preuve par substitution, temoin
d'epuisement pour toute limite imprimee (AUCUNE limite imprimee dans ce pack),
puis autoplay >= 8 parties et `verifier_tous_les_decks`.

- **tm001a** : Booyakasha part apres CHAQUE pouvoir de base (ATQ, CTR, DEF, pas REC) ;
  deplacement de 1 a 3 menaces entre deux manigances ; destination annexe a 5 par
  heros refusee, 4 acceptee (1 et 2 joueurs) ; source annexe videe = defaite ;
  Crise et deplacement depuis la principale (question 3) ; une seule question posee.
- **tm001b** : Setup met tm009 en jeu (en vraie partie, PAS seulement via Puzzle) ;
  Action : cout (defausse 1) paye, 0/1/2 Nunchuck trouves deck + defausse, ENTRES
  INCLINES, deck melange ; Action injouable sans carte en main.
- **tm002** : Slash ATQ avec Perçant (annule Robuste), Riposte 1, Robuste a l'entree,
  degats consecutifs (THW 1, ATQ 2).
- **tm003** : cherche un allie OU tm009 dans deck + defausse, ajoute a la main,
  melange ; refus si rien.
- **tm004** : +2 menaces sur la principale, heros redresse, arme choisie redressee,
  pioche 1 ; cas sans arme (question 4).
- **tm005** : 3 degats, branche etourdir / desorienter payee par l'epuisement d'UN
  Nunchuck PRET ; sans Nunchuck pret : seulement les 3 degats ; libelle attaque.
- **tm006** : X de 0 a 3, degats subis, retrait de X menaces d'une manigance, X
  degats a un ennemi ; X=0 ; avec Robuste (question 2) ; libelle attaque/contre.
- **tm007** : Reponse apres depense : soigne 1 a l'identite ET pioche 1 (a pleine
  sante : la pioche part quand meme) ; generee en wild.
- **tm008** : +1 REC pour « Mikey » en alter-ego seulement ; Action : epuise, choisit
  0 a 2 cartes de la defausse, les melange dans le deck.
- **tm009** : hors limite des manigances-joueur ; Reponse forcee : -1 menace en fin de
  phase des joueurs ; defaite : le proprietaire pioche 3 en forme de heros seulement ;
  Setup (tm001b) la pose sans depasser la limite ; jouable depuis la main.
- **tm010** : Reponse apres changement de forme (dans les DEUX sens), epuise le
  Skateboard, redresse l'identite.
- **tm011** : donne la Reponse de heros a tous les Nunchuck controles (elle-meme
  comprise) ; apres un evenement, epuise, +1 a un pouvoir choisi jusqu'a la fin du
  round ; empilement avec deux Nunchuck ; Restricted (pas plus de 2).
  ⚠ MEME instance d'`Ability` enregistree chez deux porteurs : verifier que les deux
  declenchent (voir question 6).
- **tm012** : meme montage, Interruption de heros : degats d'ATTAQUE seulement,
  -1 degat, 1 degat a l'attaquant ennemi, epuise ; pas de declenchement hors attaque.
- **tm013** : a la revelation : passe en alter-ego, epuise allies et soutiens du
  joueur donne ; changement de forme interdit ; Action d'alter-ego : epuise
  l'identite ET defausse 1 carte, retire de la partie.
- **tm014** : a la revelation, chaque joueur defausse 3 cartes de SON deck ; Crise
  (question 7) ; menace 4 par heros.
- **tm015** : Robuste a l'entree ; vaincu -> remelange dans le deck rencontre.
- **tm016** : 2 degats indirects a l'identite et aux allies du joueur.
- **Deck complet** : le deck `michelangelo` doit monter (hero_deck 15, `player_deck`
  vide) ; `verifier_tous_les_decks` ; une partie complete jouee.

## 7. Risques identifies a l'ecriture (phase C devra les trancher)

1. `tm011`/`tm012` : instance d'`Ability` partagee entre porteurs (`RegisterGiven`).
2. `tm009` hors limite : `not_count_player_side_scheme_limit` pose par
   `WhenCardSetup("This")` ; verifier que `Setup` se declenche quand la carte est
   MISE EN JEU (par tm001b ou jouee de la main), pas seulement au Setup du deck
   (precedent : `jj/61007`, qui est jouee de la main).
3. `tm009` Interruption de heros via `WhenSchemeBeDefeated(HeroInterrupt)` : aucun
   precedent exact ; la limite est aussi defaite par la Reponse forcee de fin de
   phase.
4. `tm001b` : deux `Search.PlayerCard(may=True)` successifs pour « up to 2 » :
   verifier qu'on peut s'arreter apres le premier et que le « Shuffle » n'est pas
   rejoue de facon genante ; `PutIntoPlay(..., exhaust=True)` d'une amelioration (sur
   quel personnage est-elle attachee ?).
5. `tm005` : `MayChooseOneAbility` + deux `ForChoiceAbility` portant chacun un
   `CostFunc.Exhaust(... from_where=["YouControlCards"])` : verifier que le cout
   est demande APRES le choix de la branche et que « Cancel » est propose.
6. Textes francais (`ui-app`) : rien n'apparait dans le jeu tant que
   `ui-app/deployer.sh` n'a pas tourne. « manigance annexe de joueur » est ma
   traduction de « player side scheme » (a verifier sur le glossaire officiel).
7. La bio `tm001a` n'a PAS ete confirmee au survol du heros dans le wizard
   (preuve exigee par PROCESSUS-HEROS etape 7) : non fait en phase A.
