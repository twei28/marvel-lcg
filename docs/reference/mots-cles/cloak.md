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

**Cartes Ninjutsu (TMNT Shinobi, 17/10/2026)** : `sa001`-`sa020` (pack `tmnt_shinobi_ninjutsu`) tournent toutes autour de Cloaked.
Quatre usages, par `ShinobiCloak` / `DiscardCloaked` (`cards/pack/__init__.py`, `tmnt_shinobi_ninjutsu/__init__.py`) :
- poser : « cloak your hero » (`sa002`, `sa006`, `sa011`, `sa020`), « cloak her / them / an ally / a friendly character / your identity »
  (`sa017`, `sa009`, `sa007`, `sa008`, `sa014`) ;
- condition de jeu « Play only if your hero is cloaked » (`sa001`, `sa004`, `sa005`) : `JouableSiHerosCamoufle` = identité en forme
  HÉROS portant une carte Cloaked (en alter-ego il n'y a pas de héros : faux, question Q-N1) ; « your identity is cloaked » (`sa018`) :
  `IdentiteCamouflee`, les deux formes ;
- coût « Cloak a character you control → » (`sa003`) : `CoutCamoufler` (le personnage ne doit pas déjà porter sa carte) ;
- coût « Discard a cloaked status card from your hero / a character you control / your identity → » (`sa010`, `sa011`, `sa014`, `sa015`,
  `sa019`) : `CoutDefausserCloaked("hero" | "controlled" | "identity")` = `CostFunc.Custom(CardFinder(has_status="Cloaked", ...), DiscardCloaked)`,
  modèle `sk049` (Tough). Sans carte Cloaked chez un personnage valide, l'action n'est pas proposée.
Règles du livret p.8 prouvées en jeu : un seul Cloaked par personnage même Solide ; Coriace avant Cloaked ; la défense d'un personnage camouflé
prend le +2 DEF puis la carte part avant l'excédent (`sa002`) ; les dégâts consécutifs résolvent après le +2 ATQ/CTR (`sa017`).
⚠ Statut avant Interruption : un allié camouflé voit sa carte résoudre avant toute Interruption (`sa009`, question Q-N3).
