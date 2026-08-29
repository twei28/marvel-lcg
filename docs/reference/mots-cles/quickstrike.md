# Quickstrike

**Texte imprimé / définition** : « Quickstrike. *(After this minion engages
your hero, it attacks.)* » Dès qu'un sbire Quickstrike s'engage avec un héros,
il attaque immédiatement. Ce n'est **pas** une règle d'ordre de résolution des
dégâts, c'est une attaque supplémentaire déclenchée par l'engagement. C'est un
compteur (`Quickstrike 1`, `Quickstrike 2`, ...), réinitialisé à sa valeur
imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Quickstrike` sur la carte, lue nativement
par le moteur. `HasQuickstrike`
(`src/game/card/face/attribute/can_quickstrike.py`) enregistre l'attribut
`Quickstrike` -> `printed_quickstrike`, restaure la valeur à chaque
`OnResetKeywords` via `GainQuickstrike`, et expose `IsQuickstrike()`. La
sous-classe `CanQuickstrike` fournit `ResolveQuickstrike(player)` : si la carte
est en jeu, si `IsQuickstrike()` et si `player.IsHero()`, elle fabrique l'effet
`Quickstrike(self)` (`src/game/effect/rule.py`) et déclenche
`DoAttackYou(player, effect)` pour un `Enemy`, ou `BasicAttack` pour les autres
porteurs de `CanAttack`. L'appel se fait dans `Minion.OnEngagePlayer`
(`src/game/card/face/card_type/minion.py`), juste après
`Message.WhenMinionEngagePlayer` et avant `Message.AfterMinionEngagePlayer`.
**Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01167` : * Vulture (`desc` contient `"Quickstrike":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01167.py` trouvé dans `src/cards/pack` : cette carte porte aussi
`Nemesis: Spider-Man`, un autre mot-clé, sans que cela nécessite de script
propre (le nemesis est également géré nativement).

**Pièges connus** :
- Quickstrike n'a **rien à voir avec un ordre de résolution des dégâts** face à
  Retaliate. C'est une attaque déclenchée à l'engagement, point.
- Le déclenchement est conditionné à `player.IsHero()` : un sbire qui s'engage
  avec un joueur en alter-ego n'attaque pas.
- Il se déclenche à l'**engagement**, pas à chaque activation. Un sbire déjà
  engagé qui le reste ne rejoue pas son Quickstrike. En revanche un sbire mis
  en jeu directement engagé y passe : `Minion.OnWhenCardEnterPlay` appelle
  `OnEngagePlayer` quand `card.area.flags.is_engaged` est vrai.
- Ne pas coder l'attaque à la main dans le `.py` d'une carte Quickstrike : le
  moteur l'orchestre depuis le compteur `desc`. Si une future carte cumule
  Quickstrike avec une capacité imprimée annexe, vérifier via `find` si un
  script existe pour cette carte : le script devra porter uniquement cette
  capacité annexe, jamais le mot-clé Quickstrike lui-même.

**Variantes maison** : aucune recensée pour l'instant.
