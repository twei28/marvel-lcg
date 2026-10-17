# Jeton « smoke counter » (TMNT Shinobi Ninjutsu, Inkwire)

**Texte imprimé / définition** : `sa008` Smoke Bombs (amélioration ITEM) : « *Uses (2 smoke counters)*. Max 1 per player.
*Hero Action*: Exhaust this card and remove 1 smoke counter from it → cloak a friendly character. » Un « smoke counter » est un
compteur nommé, sans règle propre.

**Mécanisme moteur** : `'smoke'` est dans `CardFace.COUNTER` (`card_face.py`, 17/10/2026, additif). `Uses` est NATIF
(`desc.Uses = "2,smoke"`, fiche `uses.md`) : le moteur pose 2 compteurs à l'entrée en jeu et défausse la carte au dernier retiré.
Coût : `CostFunc.Exhaust("This")` + `CostFunc.Counter("This", 1, 'smoke')`. « Max 1 per player » = `desc.MaxPerUnit = 1`
(l'amélioration est jouée devant le joueur : `CanPlayThisUpgradeCard()`). Libellé français : « fumée ».

**Carte exemple** : `sa008` Smoke Bombs. ⚠ HOMONYME de `27139` Smoke Bombs (Goblin Gear, ATTACHEMENT du vilain à « bomb counters »),
sans aucun rapport de règles : confirmé sur le scan.

**Pièges connus** :
- deux utilisations (2 compteurs) puis la carte part : le cas `[sa] sa008` le mesure ;
- « a friendly character » : identités ET alliés de tous les joueurs (`SetTarget(Friend)`), jamais un ennemi ;
- le « Max 1 per player » ne se mesure que si la 1re copie est ATTACHÉE à l'identité (`Puzzle.AttachReel`) : `Puzzle.PutIntoPlay`
  la pose sans l'inventaire de l'identité et le compte reste à 0.

**Variantes maison** : tout est maison.
