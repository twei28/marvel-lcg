# TMNT Shinobi, socle et Paths : questions ouvertes pour l'utilisateur (17/10/2026)

> Réponses rendues le 17/10/2026, voir shinobi-reponses.md (les mentions « NON terminée » / « provisoire » ci-dessous sont historiques : cartes levées).

Sources : zip « TMNT Shinobi » (livret `Shinobi Book PNGs` pages 1-12 + `Shinobi Path Rulebook.pdf`, 11 dos de Path « Cardback »,
11 fronts de Path). Scans : `/tmp/.../zip-shinobi/TMNT Shinobi/` (dossiers `Shinobi Paths`, `Shinobi Paths/ Hybrid Shinobi Paths
(Advanced)`, `Shinobi Book PNGs`). Une question à la fois, scan à l'appui (consigne : montrer l'image avant chaque question).
Lecture PROVISOIRE retenue entre parenthèses ; chaque question dit ce qu'elle change EN JEU.

## Q-S1 : se001 Kagemusha : « Shadow Stride » (scan) ou « Walk in Shadows » (livret) ?
- Scan : `Shinobi Paths/Kagemusha.png`. Le scan imprime « *Shadow Stride* — Hero Action: Exhaust this card → cloak your hero ».
  Le livret (page 1 sur la carte exposée, page 2 dans le texte « The Kagemusha ability "Walk in Shadows" ... ») la nomme
  « Walk in Shadows ».
- Options : (a) **le scan, « Shadow Stride »** (recommandée : la règle du projet fait foi du scan) ; (b) « Walk in Shadows »
  (livret) ; (c) autre.
- Effet en jeu : AUCUN sur la mécanique (seul le nom de la capacité, en italique sur la carte). Provisoire : (a).
- Statut de la carte : comportement prouvé (14 cas), libellé en attente. `se001` : **NON terminée** (attend Q-S1, nom seul).

## Q-S2 : se004 Shihan : que peut rendre Recenter, une carte « Taijutsu » ou aussi « Kuji-Kiri/Ninjutsu » ?
- Scans : `Shinobi Paths/Shihan.png` (texte imprimé : « *Recenter* — Hero Interrupt: When the player phase ends, discard the top
  2 cards of your deck → **return 1 Taijutsu card** from your discard pile to your hand ») ; livret page 8, FAQ : « Q: If I
  start my game with the Shihan Path, may I return a **Kuji-Kiri/Ninjutsu** card to my hand at the end of the player phase?
  A: Yes. » (dos `Shihan Cardback.png` : « ... return 1 Taijutsu card »).
- Le texte imprimé et le dos disent Taijutsu ; la FAQ répond « Yes » pour une carte Kuji-Kiri/Ninjutsu (une Dual qui n'est
  pas Taijutsu). Contradiction ou coquille de la FAQ (pour « Kuji-Kiri/Taijutsu », la Dual KT1/KT2) ?
- Options : (a) **texte imprimé : seulement les cartes Taijutsu, dont les Dual Taijutsu (BT, KT, NT)** (recommandée, c'est la
  lecture littérale du scan et du dos) ; (b) FAQ à la lettre : n'importe quelle carte Shinobi de la défausse ; (c) Taijutsu +
  les Dual Kuji-Kiri/Ninjutsu (KN) ; (d) autre.
- Effet en jeu : (a) Recenter ne ramène que du Taijutsu ; (b) Shihan ramène aussi du Bushido, Kuji-Kiri, Ninjutsu : bien plus fort.
- Provisoire : (a). `se004` : **NON terminée** (attend Q-S2).

## Q-S3 : les Paths sont-ils réservés aux héros TMNT ?
- Source : livret pages 1-8. Rien n'y limite les Paths ou les cartes Shinobi aux héros TMNT (« players », « your hero »).
- Options : (a) **tous les héros** (recommandée : lecture littérale, c'est ce qui est codé ; le moteur n'en dépend pas) ;
  (b) héros TMNT seulement : ajouter les six sets « TMNT Shinobi * » à `sets_exclusifs` de `data/arts_alternatifs.json`
  (mécanisme déjà utilisé par les aspects TMNT, une ligne de configuration).
- Effet en jeu : Spider-Man (par exemple) peut ou non choisir Kagemusha et jouer des cartes Shinobi dans le deck-builder.
- Provisoire : (a).

## Q-S4 : The Last Ronin et les héros qui imposent leur règle d'aspect
- Scans : `Hybrid Shinobi Paths (Advanced)/The Last Ronin Cardback.png` : « You may add **any combination** of aspect cards
  (Aggression, Justice, Leadership, Protection). You may add **only one copy of any card** to your deck. ». Livret page 5 :
  « Follow your Path deck-building rules **in conjunction with** the standard deck-building rules. »
- Les règles du Path s'AJOUTENT à celles du héros ; mais « any combination of aspect cards » contredit la règle d'un aspect
  de la plupart des héros, et un Path « un aspect » contredit un héros qui en exige 2 (Spider-Woman) ou 4 (Adam Warlock).
- Options : (a) **le Path l'emporte seulement pour Last Ronin (combinaison libre), pour les Paths à un aspect la règle la plus
  stricte vaut sauf si elle empêcherait le héros d'avoir son nombre d'aspects requis** (recommandée, c'est ce qui est codé) ;
  (b) le héros garde TOUJOURS sa règle d'aspect (Last Ronin ne donne alors que les quatre types Shinobi et le plafond d'un
  exemplaire) ; (c) le Path remplace toujours la règle d'aspect du héros.
- Effet en jeu : (a) un deck Last Ronin peut mêler les 4 aspects ; Spider-Woman garde ses 2 aspects avec un Path à un aspect ;
  (b) Last Ronin n'ouvre pas les aspects ; (c) Spider-Woman avec un Path n'aurait qu'un aspect.
- Provisoire : (a) (`validerDeck`, tests `regles-shinobi.test.mjs`).

## Q-S5 : Jennika et un Path choisi : cumul ou refus ?
- Source : dos `Sosaiken Cardback.png` (la Voie de Jennika, déjà en jeu par son Setup) et livret page 2 (« select a Shinobi Path card »,
  UN Path).
- Jennika a sa Voie propre (`tj011`, Path imprimé). Peut-elle en plus choisir un des 11 Paths ?
- Options : (a) **non : un seul Path par héros, Sosaiken est sa Voie** (recommandée, c'est ce qui est codé : le deck-builder
  refuse « ce héros a déjà sa Voie ») ; (b) oui, cumul : deux Paths, -2 de taille de main (Jennika 4 -> 2) ; (c) oui, mais à la
  place de Sosaiken (nouvelle règle de Setup à écrire).
- Effet en jeu : (a) aucun changement pour Jennika ; (b) taille de main très basse, deux capacités de Voie ; (c) Jennika sans
  Sosaiken.
- Provisoire : (a). Aucune carte à rouvrir : c'est une règle de deck-builder (`deck/starter/jennika.json`, `metadata.deckbuilding.path`).

## Q-S6 : « Your hero gains the NINJA trait » (Kagemusha) contre « You gain the MYSTIC trait » (Onmyōdō)
- Scans : `Shinobi Paths/Kagemusha.png` (« **Your hero** gains the NINJA trait. ») et `Onmyodo.png` (« **You** gain the MYSTIC trait. »),
  idem Yamabushi (TEMPORAL), Onigari (PSIONIC), Ashigaru (SOLDIER) : « You gain ». Le livret p.2 : « Your hero gains the NINJA trait »
  (Kagemusha) mais « The Onmyōdō Path passively grants the MYSTIC trait ».
- Options : (a) **littéral : « Your hero » = la forme héros seulement (Kagemusha), « You » = les deux formes de l'identité (les
  quatre autres)** (recommandée, c'est ce qui est codé) ; (b) les cinq donnent le trait aux deux formes ; (c) les cinq seulement
  à la forme héros.
- Effet en jeu : le trait de l'alter-ego (par exemple une carte qui demande « votre identité a le trait MYSTIC » en forme civile).
- Provisoire : (a).

## Notes sans question (relevées, aucune décision en jeu)
- Coquille de crédit : le scan `Taijutsu/T3 Stiff Jab.png` imprime « **MC** Custom Content By: Inkwire » au lieu de « TMNT Shinobi
  By: Inkwire » (à reporter à l'agent des cartes Taijutsu).
- Les cartes Shinobi `sb/sj/sa/sh/sc` n'ont pas encore de script : leurs agents fixent leurs propres questions dans
  `.planning/tmnt/shinobi-<pack>-questions.md`.
- Trois homonymes de noms officiels (cartes différentes, à confirmer sur le scan par l'agent concerné) : `sj001` Foresight (mw009,
  vp008), `sa008` Smoke Bombs (27139), `sh008` Drop In (nt004) : voir `tools/tmnt_shinobi_numerotation.tsv`, colonne `note`.
- Lecture du livret page 3 : « Once per turn, the Samurai ability » ; la carte imprime seulement « Exhaust this card » : l'inclinaison
  fait la limite (la Voie se redresse en fin de phase), identique en pratique ; aucune limite codée en plus.
- Cloaked / Dazed : « un seul par personnage » (déjà codé, `cloaked.md`, `dazed.md`) ; « Tough avant Cloaked, Cloaked et Dazed en
  même temps » : déjà en place (Shredder, Baxter).
