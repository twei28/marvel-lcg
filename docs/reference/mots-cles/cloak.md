# Cloak

**Texte imprimé / définition** : le mot est imprimé en verbe, sans définition ni
rappel entre parenthèses :
- `tl015` * Karai : « **When Revealed**: Cloak Karai. » et « **When Defeated**:
  Cloak the villain. » ;
- `tl016` Foot Soldiers : « **When Revealed**: Cloak Foot Soldiers. » ;
- `td005` Improvised Tactics : « Cloak two friendly characters. » (une des trois
  options de « choose two »).

**Définition retenue (16/10/2026)** : « Cloak X » = **poser une carte d'état
Cloaked sur X**. La carte d'état, imprimée sur le scan « Cloaked » du zip
« TMNT Enemies / Shredder v3 » (Inkwire), porte la règle ; elle est décrite dans
`cloaked.md` (un seul effet, le premier qui arrive : +2 au prochain pouvoir de
base / à la prochaine activation, OU −2 aux prochains dégâts, puis la carte part).

**Mécanisme moteur** : `Cloak(effect, face)` dans
`src/cards/pack/leonardo/leonardo_nemesis/__init__.py` pose l'état par
`Faces.GiveStatus([face], "Cloaked", effect)` (= `face.GainStatus("Cloaked",
effect)`), et ne fait rien si la cible n'existe plus (`face is None`). Les trois
appels de `tl015` (×2) et `tl016` y passent. `td005` n'y passe pas (cibles
choisies) : elle choisit deux personnages amis et appelle `Faces.GiveStatus`
elle-même.

**Carte exemple** : `tl016` : Foot Soldiers (un seul effet, `Cloak`).

**Pièges connus** :
- `Cloak the villain` (When Defeated de Karai) vise le VILAIN, pas Karai : la
  carte est posée sur le vilain en jeu (`Worlds.FindCardOnField(card_type=Villain)`).
- `Cloak Karai` / `Cloak Foot Soldiers` : la carte elle-même (le sbire qui vient
  d'être révélé), pas le vilain.
- `td005` : « **two** friendly characters » = exactement deux quand il y en a au
  moins deux (identités et alliés de TOUS les joueurs,
  `Worlds.GetOnFieldFriendlyCharacters`), sinon tous ceux qui existent. L'option
  fait partie d'un « choose two, pas deux fois la même » : elle reste proposée
  même avec un seul ami (fidèle au texte, le moteur choisit ce qui existe).
- Pas de plafond : Cloaked s'empile (voir `cloaked.md`).

**Variantes maison** : aucune.

**Cartes joueur de l'aspect Protection (16/10/2026)** : `up007` Cyber Ninja (« cloak Cyber Ninja », sur
lui-même), `up023` Lookout (« cloak your hero »), `up024` Nobody (« place a tough or cloaked status card »).
Toutes par `Faces.GiveStatus([...], "Cloaked", effect)`. Cas : `tools/cas/tmnt_aspect_protection.py`.

**Preuves** : `tools/cas/cloaked_cartes.py` (tl015 Karai révélée / vaincue, tl016,
td005), avec preuve par substitution (le stub rétabli, les 4 cas échouent).
