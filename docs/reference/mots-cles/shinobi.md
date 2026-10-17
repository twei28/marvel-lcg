# Shinobi (classes Bushido, Ninjutsu, Kuji-Kiri, Taijutsu) et Path

**Texte imprimé / définition** : mécanique propre au héros **Jennika** (TMNT Heroes v3, Inkwire),
jamais définie dans un livret de règles de ce zip. Elle se lit sur les cartes :
- `tj004` Decisive Strike : « *(This card is both a Jennika card and a Taijutsu card.)* » ;
  `tj003` Apparition : Kuji-Kiri ; `tj005` Moonlighting : Ninjutsu ; `tj006` Fearless Resolve :
  Bushido (« *This is both a Jennika card, and a Bushido card.* ») ;
- `tj001a` Ninja Senpai : « When you play a **Shinobi** card, Jennika gets +1 THW, +1 ATK and +1 DEF
  until the end of the round. *(Limit once per round for each Shinobi.)* » ;
- `tj011` Sōsaiken (type imprimé **PATH**) : « Response: After you play a Shinobi card, exhaust this
  card → draw 1 card. » ;
- `tj009` Tekko-Kagi : « generate a [wild] resource for a Shinobi card. » ;
- le dos du Path (`Sosaiken Cardback.png`, **non transcrit en carte** : insert de règles) : « You may add
  any combination of Shinobi cards (Bushido, Ninjutsu, Kuji-Kiri, or Taijutsu) to your deck. You cannot add
  aspect cards. You may add Basic cards. [...] Dual Shinobi cards trigger **both** Shinobi types when
  played. »

**Définition retenue (16/10/2026)** : une **carte Shinobi** est une carte qui porte l'une des quatre
**classes** Bushido, Ninjutsu, Kuji-Kiri, Taijutsu. Les cartes de Jennika qui n'impriment AUCUNE de ces
phrases (Composure, Jenny's Crib, Bow, les deux Tekko-Kagi) ne sont **pas** Shinobi
(`.planning/tmnt/jennika-questions.md`, Q2).

**Mécanisme moteur** : la classe est portée par `desc.Class`, séparée par un point-virgule, comme
« Campaign;Aggression » : `"Hero;Taijutsu"`, `"Hero;Kuji-Kiri"`, `"Hero;Ninjutsu"`, `"Hero;Bushido"`.
Les quatre noms ont été ajoutés à `ClassCard.CARD_CLASS` (`src/game/card/face/base/card_player.py`,
fichier moteur partagé, additif) ; ils ne sont **pas** des aspects (`ASPECT_CLASS_TYPE` inchangé).
Le filtre « une carte Shinobi » est `CardFinder(card_classes=CLASSES_SHINOBI)` (`CarteShinobi()` dans
`cards/pack/jennika/jennika/__init__.py`) ; `CardFinder.card_class` / `card_classes` lisent
`ClassCard.IsClass`. **Aucun script** pour la classe elle-même.

« Limit once per round **for each Shinobi** » : lecture retenue = une fois par round pour CHACUNE des
quatre classes. D'où QUATRE capacités `WhenPlayerPlayCard(Interrupt, "You", CardFinder(card_class=X))`
sur `tj001a`, chacune avec son propre `LimitOncePerRound()`. Les cartes « Dual Shinobi » d'autres sets
(deux classes à la fois) déclencheraient les deux capacités : « trigger both Shinobi types ». Aucune
carte Dual n'existe dans ce dépôt.

**Carte exemple** : `tj001a` (la limite par classe), `tj011` (la Réponse de la Voie), `tj009`
(ressource wild réservée).

**Pièges connus** :
- le Path est un **type de carte** imprimé que le moteur n'a pas ; `tj011` est un **Support**
  (Permanent, mis de côté, mis en jeu par le Setup de `tj001b`, modèle `58002` Ionic Physiology de
  Wonder Man). Question Q3 ;
- `CardFinder(card_class="Hero")` ne désigne rien : « Hero » est converti en `IdentitySpecific` à la
  lecture du desc (`card_player.py`) ;
- `etat_attendu` du harnais compte la Réponse de la Voie : elle pioche 1 carte après une carte Shinobi,
  ce qui change la main d'un cas qui la compte.

**Variantes maison** : c'est elle-même une variante maison (aucun mot-clé officiel).

---

## TMNT Shinobi (Inkwire, 17/10/2026) : le système des Paths (livret « Shinobi Path Rulebook »)

Le zip « TMNT Shinobi » (103 cartes joueur : 4 Paths standard + 7 Paths hybrides + 80 Shinobi + 12 Dual Shinobi, plus les
11 DOS de Path et un livret de 12 pages) généralise ce qui n'était qu'esquissé par Jennika. Packs : `tmnt_shinobi_bushido`
(sb, 20), `_kuji_kiri` (sj, 20), `_ninjutsu` (sa, 20), `_taijutsu` (sh, 20), `_dual` (sc, 12), `_paths` (se, 11) ; sets
202-207 ; numérotation figée (scans B1.., K1.., N1.., T1.., Dual BK1..NT2, Paths) par
`tools/tmnt_shinobi_numerotation.tsv`. Crédit imprimé « TMNT Shinobi By: Inkwire ».

**Texte du livret** (traduit de l'anglais ; pages dans `Shinobi Book PNGs`) :
- Quatre TYPES Shinobi : **Bushido** (liseré turquoise), **Kuji-Kiri** (rose), **Ninjutsu** (violet), **Taijutsu** (orange). Les
  cartes Shinobi **ne comptent NI comme aspect NI comme Basic** pour déclencher des capacités.
- ÉTAPE 1 : au deck-building on choisit UN **Path** (type de carte PATH, Permanent, « You get -1 hand size ») ; on le met en jeu
  au Setup. **Sans Path, AUCUNE carte Shinobi** dans le deck. Chaque Path autorise des types Shinobi, UN aspect au choix
  (Aggression, Justice, Leadership ou Protection) et les cartes Basic. Les Paths ne sont pas des Soutiens.
- ÉTAPE 2 : règles standard EN PLUS de celles du Path ; jusqu'à 3 exemplaires de chaque carte Shinobi, sauf unique (✦).
- **Dual Shinobi** : compte comme LES DEUX types (construction ET jeu) ; il suffit qu'UN des deux soit autorisé par le Path.
- Hybrides : types imprimés en traits, en bas à droite ; **The Last Ronin** : les quatre types, combinaison libre d'aspects,
  UN seul exemplaire de toute carte.
- FAQ p.8 : Shihan peut inclure une Dual Ninjutsu/Taijutsu ; Ashigaru une Dual Bushido/Kuji-Kiri ; Cloaked / Dazed sur un
  personnage Steady / Stalwart : oui ; un seul Cloaked et un seul Dazed par personnage.

**Mécanisme moteur** :
- **Classes** : `desc.Class = "Bushido"` ou, pour une Dual, `"Bushido;Kuji-Kiri"` (aucune classe de plus à ajouter : les
  quatre noms sont dans `ClassCard.CARD_CLASS` depuis Jennika). `ClassCard.IsClass` parcourt la liste : une Dual est
  reconnue pour CHACUNE de ses classes par `IsClass`, `CardFinder(card_class=X)` et `CardFinder(card_classes=[...])`
  (prouvé par `[se] se006` / `se005`, qui portent 2 et 4 classes). `IsClass("Aspect")` et `IsClass("Basic")` restent faux.
- **Helpers partagés** (`src/cards/pack/__init__.py`, visibles de tout module de carte) : `CLASSES_SHINOBI`,
  `CarteShinobi(*classes)`, `EstShinobi(face, *classes)`, `PayeAvecUnEvenement(effect, *traits)`, `ShinobiCloak(effect,
  faces)`, `ShinobiDaze(effect, faces)`.
- `CarteShinobi()` / `EstShinobi()` EXCLUENT les Paths (qui portent pourtant les classes de leurs types) : un Path n'est pas une « carte Shinobi » du deck.
- **Path** : fiche `path.md` (type, mise en jeu au Setup pour n'importe quel héros, -1 taille de main, classe = types).
- **Compteur samurai / trait OATH** : fiche `samurai-counter.md`.
- **Tuck** (The Last Ronin, Kanpeki) : fiche `tuck.md`.
- **Règles de construction** : `data/shinobi_paths.json` (transcription) ; `public/js/deckbuilder/paths-shinobi.js` (miroir) ;
  `regles.js` (`validerDeck`) ; tests `tools/tests-lanceur/regles-shinobi.test.mjs`.

**Cartes de référence** : `se001`-`se011` (les Paths), `jennika/tj004` (payée par un événement), `jennika/tj006` (OATH).

**Pièges connus** (en plus de ceux de Jennika) :
- le nom de capacité imprimé sur le scan de Kagemusha est « Shadow Stride » ; le livret (p.1 et p.2) dit « Walk in Shadows » ;
- la FAQ de Shihan (p.8) demande si « un Kuji-Kiri/Ninjutsu » peut être rendu par Recenter : texte imprimé « 1 Taijutsu card »
  (question Q-S2, `.planning/tmnt/shinobi-socle-questions.md`) ;
- l'icône de ressource de Light of Foot (Ashigaru) est une étoile : c'est le MÊME glyphe que « generate a [star] resource » de
  `jennika/tj009` (découpe des deux scans comparée le 17/10/2026), donc [wild] ;
- les cartes `sb`/`sj`/`sa`/`sh`/`sc` portent `desc.Class` = leur(s) type(s) Shinobi SEUL(S) (jamais « Hero ») : cartes de
  joueur choisies au deck-building, contrairement aux Shinobi de Jennika (« Hero;Taijutsu », signatures).
