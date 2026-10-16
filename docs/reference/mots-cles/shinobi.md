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
