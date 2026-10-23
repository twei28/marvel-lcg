# Linked (Lié)

**Texte imprimé / définition** : « Linked (X). » Une carte **Linked (X)** est
mise de côté quand la carte nommée **X** entre dans la partie ; elle n'est
accessible que par les effets de X. Officiel : `43034` Combat Specialist
(Linked (Specialized Training)), `49033` Surge (New Recruits)...
Scénario Bebop & Rocksteady : `tk106` Channel 6 News, `tk107` Eastman Theater,
`tk108` Powder Keg, `tk109` Power Play, tous « Linked (Welcome to the Jungle) ».

**Mécanisme moteur** : clé `desc.Linked = "<nom ou card_id de X>"`, lue à
l'ouverture du catalogue (`cards/database.py`, `CardsDB.linked_papers`) ; quand
la carte X est fabriquée (`CardFactory.GenerateCard`, `create_linked_faces`),
chaque carte liée est fabriquée **dans la zone de mise de côté**
(`world.aside_deck`). Aucun script pour le mot-clé lui-même : la carte X décide
de leur sort (ici `tk101` Welcome to the Jungle : « Each player may choose 1
set-aside NYC card and put it into play »).

**Carte exemple** : `43021` Specialized Training (modèle officiel du
« When Defeated » qui met en jeu une carte liée) ; `tk101`.

**Pièges connus** :
- Les cartes liées officielles portent `"Class": "Basic"` et `"set_name": ""` ;
  les quatre `tk106`-`tk109` font pareil. ⚠ `estCarteJoueur`
  (`public/js/deckbuilder/regles.js`) accepte la classe Basic : comme pour les
  cartes liées officielles, rien dans le deck-builder ne les masque.
- « put it into play » : `face.PutIntoPlay(joueur, effect, under_control=True)`.
  Une manigance de joueur liée (`tk108`, `tk109`) doit en plus poser
  `not_count_player_side_scheme_limit` à l'entrée en jeu (modèle `ip002a`).
- `FindCardPaper("Welcome to the Jungle")` cherche par NOM : le nom doit rester
  unique dans tout le catalogue.

**Variantes maison** : « Linked (A, B, or C) » a TROIS noms (Shadowland, set Dark Protege, sl018 a sl027) : `desc.Linked` n'accepte qu'un nom, donc rien n'y est ecrit ; la liste est lue dans le texte imprime par `VilainsLies` (`cards/pack/shadowland/__init__.py`) et `sl001a` melange dans le deck de rencontre les seules cartes liees au vilain tire (les autres restent de cote).
