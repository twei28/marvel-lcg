# Just a Core X (maison, scénario `the_hunger_core`, préfixe `hg`)

**Texte imprimé** (livret officiel, page 4) : « Just a Core X. The Core does not attack. When it activates against
a player in hero form, instead of attacking, that player deals themself X facedown encounter cards. Against an
alter-ego it schemes as usual. If a card would make the Core attack, it gains Surge instead of resolving the
attack. If a card would make a Metazombie attack or activate and there are none in play, it also gains Surge. »

**Mécanisme moteur** : modèle quasi mot pour mot de la moitié « attaque » de `HIDDEN`
(`galactic_storm/hala_ultimatum/__init__.py`, `VillainNAttaquePasTantQuilEstCache`, fiche
[[immunite-cartes-joueur]]) : `AbilityFactory.WhenUnitWouldAttack(ForcedInterrupt, "This", op)` +
`message.SetBeInstead(effect)`. Différence : Kree Leader redirige TOUJOURS ; le Cœur ne redirige QUE contre un
joueur en forme HÉROS (`message.against_player` existe ET ce joueur est en forme Hero — l'activation contre un
ALTER-EGO est déjà convertie en manigance par la règle de base du moteur, donc `WhenUnitWouldAttack` ne se
déclenche normalement même pas dans ce cas : « Against an alter-ego it schemes as usual » décrit le comportement
PAR DÉFAUT du moteur, pas un cas à coder).

« If a card would make the Core attack, it gains Surge instead » : second filet, pour une attaque forcée par une
AUTRE carte que l'activation normale du Cœur (aucune carte du pack ne le fait à ce jour — rien à coder tant
qu'aucune carte livrée n'en a besoin, noter le filet manquant si un futur ajout au pack en a besoin).

**Carte exemple** : `hg001`/`hg002` Just a Core 1, `hg003` Just a Core 2.

**Pièges connus** :

- **Ne pas coder la moitié « alter-ego »** : elle n'existe pas en tant que texte à transcrire, c'est la règle de
  base « the villain schemes against an alter-ego instead of attacking » déjà native au moteur.
- **Le second filet (Surge) n'est PAS implémenté** faute de carte qui le déclenche dans ce pool fermé de 76 cartes
  (vérifié : aucune carte ne fait « make the Core attack » autrement que son activation normale). Ce point est à
  vérifier en partie réelle si un ajout futur au pack change la donne (§9 du guide).
- **Le second filet pour un Metazombie seul en jeu** (« a card would make a Metazombie attack... and there are none
  in play ») relève du même constat : aucune carte du pool actuel ne force un Metazombie absent à attaquer. Rien à
  coder pour l'instant.

**Variantes maison** : aucune à ce jour.
