# Deterrence (carte de dissuasion, deck de dissuasion)

**Texte imprimé / définition** : mot-clé maison du pack `batman` (« Batman (Sealed 6.12.2022) », ES). Batman part avec **15 cartes de
dissuasion** (5 titres × 3, trait `DETERRENCE`, type Traîtrise). **Avant la partie le joueur en retient 8** (le « deterrence deck »). Quand
une capacité de Batman le permet (« choose a deterrence card and shuffle it into the encounter deck », 3 fois par round au plus) : il en
prend UNE dans ce deck et elle est **mélangée dans le deck de rencontre**. Une carte de dissuasion **résolue** (révélée, ou résolue comme carte
de boost) va dans la **défausse de dissuasion**. Une carte **défaussée du deck de rencontre sans avoir été résolue** va dans une **défausse
auxiliaire temporaire** ; quand l'effet qui l'a défaussée est fini, on la remélange dans le deck de rencontre. Deck de dissuasion vide : on y
remélange sa défausse, sans pénalité.

**Mécanisme moteur** : aucune règle du moteur changée. Le deck de dissuasion est `joueur.additional_deck` (le « Special deck » que le plateau
dessine déjà), sa défausse `joueur.additional_discard_pile`. Montage : `BeginGameWithSetAside(15 ids, MonterLeDeckDeDissuasion)` sur
l'alter ego (`bm001b`) ; au Setup, `ChooseAbilities` (range 8-8) retient 8 cartes, les 7 autres sont retirées du jeu. `PreparerDissuasion`
pose `card.bind_discard_pile = additional_discard_pile` (une carte RÉSOLUE y retourne seule) et un crochet `WhenCardWouldDiscard` : une carte non
résolue (drapeau `resolu` faux) est notée dans `joueur.bm_attente` et remélangée par `AfterResolveEffect` à la fin de l'effet fautif
(`RangerSiNonResolue` / `RemelangerEnAttente`). `MarquerResolue` est le premier geste du When Revealed et du Boost de chaque carte. Tout vit dans
`src/cards/pack/batman/__init__.py`.

**Carte exemple** : `bm018` Sudden Strike (`src/cards/pack/batman/batman_deterrence/bm018.py`) ; `bm001a` Batman (mélange, 3 par round) ;
`bm002` Robin (dissuasion défaussée sans être résolue : remélangée).

**Pièges connus** :
- ⚠ `Puzzle.Reveal('bm018')` ne cherche PAS dans le deck de dissuasion (`FindOrCreateFace`) : il fabrique une carte neuve, non préparée. Les cas
  montent la carte par `Puzzle.SetDeterrenceDeck(...)` puis `Puzzle.ShuffleDeterrence(...)` (deux méthodes de test ajoutées à `puzzle.py`).
- ⚠ Une carte à DEUX capacités de jeu (Intimidate : révélation + boost) doit être déclarée dans la liste blanche de `game/card/factory.py`
  (leçon `ls005`), sinon la partie plante au setup.
- ⚠ « Cancel its surge effect » (Intimidate, Utility Belt) : drapeaux sur la carte (`sans_surge`, `sans_boost_sup`) lus par ses propres
  opérations ; Utility Belt agit APRÈS la première résolution, donc retire le surge déjà pris (`GainSurge(-surge)`). Sous la règle `v18_surge`,
  `ResolveSurge` DISTRIBUE une carte rencontre face cachée (`DealEncounterCards`) : un cas ne voit pas la carte suivante révélée, il mesure
  `card.surge` (clé `bm_surge`).
- ⚠ « If Batman is in play » = l'identité en forme HÉROS (`Worlds.FindCardOnField(name="Batman", card_type=Hero)`) : Bruce Wayne n'est pas Batman.
- ⚠ Un cas qui attaque plusieurs fois de suite doit REDRESSER Batman entre deux (`Puzzle.Ready`).
- ⚠ Menace d'un cas : rester sous le seuil d'accomplissement du complot principal (7 contre Rhino).
- Aucun message du moteur ne dit « une carte est mélangée dans le deck de rencontre » : Two-Face (« after a deterrence card is shuffled ») est réveillé
  par la fonction qui mélange (`ApresMelange`).

**Variantes maison** : aucune autre carte du jeu ne porte le trait.
