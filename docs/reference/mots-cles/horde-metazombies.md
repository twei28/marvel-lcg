# Jeton actif, Horde deck et decks signature (maison, scénario `the_hunger_core`, préfixe `hg`)

**Texte imprimé / définition** (livret officiel, pages 3-6) :
- « Only one activates. The active Metazombie token decides which villain activates each villain phase, and it
  rotates along the row... At the end of each villain phase, the token moves to the next Metazombie in the row, to
  the right. From the last one it goes back to the first. If the active Metazombie is defeated, the token moves
  immediately to the next one in the row, which resolves any remaining activations. If no Metazombie is left, the
  token moves to The Hunger Core. »
- « Putting a Metazombie into play: take the top card of the Horde deck and place it at the right end of the row...
  Shuffle its signature deck and place it facedown next to it. If the Horde deck is empty, shuffle its discard pile
  to make a new one; if both are empty, nothing happens. Maximum 3. »
- « When a Metazombie is defeated: discard the cards attached to it, put it in the Horde discard pile and set its
  signature deck aside next to it. »
- « Signature decks: Each Metazombie has its own signature deck... never shuffled into the encounter deck... come
  out with Metazombie Power!... A discarded signature card goes to the bottom of its Metazombie's signature deck,
  not the encounter discard pile. »

**Ce que c'est** : ce scénario a DEUX sortes de « méchant » en jeu simultanément (le Cœur et jusqu'à 3 Metazombies,
tous des `Villain` — page 3 : « A Metazombie is a villain for all purposes »), avec UN SEUL qui s'active par phase
méchant (le jeton actif), ET un deck de méchants séparé du deck de rencontre (le Horde deck, 9 cartes), ET un
mini-deck privé par Metazombie en jeu (son deck signature, 3 à 6 cartes).

**Mécanisme moteur**, trois briques distinctes, toutes dans `src/cards/pack/the_hunger_core/commun.py` :

| Besoin | Brique réutilisée |
|---|---|
| plusieurs méchants simultanés, « le méchant » = celui avec le jeton | brique commune du 20/10/2026, `Villains.SetRule(effect, Villains.Rule(the_villain="Active", player_cards="TheVillain"))` (fiche [[mechants-multiples]]), posée au Setup de `hg004a` |
| faire avancer le jeton | `Villains.SetActive` (native) via `commun.PasserLeJeton` (fin de phase méchant) et `commun.JetonApresDefaite` (Metazombie actif vaincu), plus `commun.MettreUnMetazombieEnJeu` (jeton sur le Cœur -> le Metazombie qui entre le reprend ; c'est aussi ce qui pose le jeton sur le premier Metazombie à la mise en place). Branchés UNE fois par `commun.ReglesDuScenario` (`AbilityType.Scenario`, modèle Sinister Six `27100a`), incluse dans `CapacitesDuCoeur` (le Cœur reste en jeu du Setup à la victoire). Pas la même fabrique qu'Alien vs. Predator (`PasserLeCompteur`), qui avance après CHAQUE activation : ici le jeton ne bouge qu'une fois par phase |
| Metazombie vaincu | `commun.QuandMetazombieVaincu` sur `WhenUnitBeDefeated` (le vaincu est ENCORE en jeu) : attachements de son deck signature au FOND de ce deck (FAQ p. 8), jeton au suivant s'il était actif, puis carte dans la défausse du Horde deck. La sortir à ce moment empêche `Villain.OnBeDefeated` de l'« avancer » (sans ce crochet, `AdvanceVillainStage` la retirait de la partie : elle ne revenait jamais) |
| un second deck de méchants, hors deck de rencontre | modèle `player.additional_deck`/`additional_discard_pile` (fiche [[registered]], `player.py:97`) mais lié au SCÉNARIO : `Deck2(scenario, DeckType.AdditionalDeck, Villain)` + `Deck2(..., DeckType.AdditionalDiscardPile, Villain)`, liés par `BindDiscardPile` ; `commun.HordeDeck`/`ConstruireLeHordeDeck`/`MettreUnMetazombieEnJeu` |
| un mini-deck PAR Metazombie en jeu | `Deck2(metazombie.card, DeckType.AdditionalDeck, CardFace)`, créé et mélangé À LA DEMANDE (première consultation), stocké sur l'objet `Card` lui-même (`commun.DeckSignatureDe`) ; la défausse « vers le fond » utilise `Card.MoveToBottom`, pas `Faces.MoveAllTo` (qui n'a pas de variante « bottom ») |

**Carte exemple** : `hg004a` (Setup : `Villains.SetRule` + `ConstruireLeHordeDeck`), `hg046` Metazombie Power!
(`RevelerLeDessusDuDeckSignature` sur `LeMetazombieActif(effect)`), `commun.ReglesDuScenario` (jeton, défaite, Infection).

**Pièges connus** :

- **Le jeton n'avance PAS après chaque activation**, contrairement au modèle Alien vs. Predator : une seule
  activation par Metazombie actif par ronde (« once against each player, in player order »), puis `PasserLeJeton`
  une fois en fin de phase méchant. Copier `PasserLeCompteur` tel quel serait un piège.
- **`JetonApresDefaite` n'est PAS `PasserLeJeton`** : à la défaite de l'actif, le jeton va au Metazombie
  SUIVANT À DROITE du vaincu (en bouclant), vaincu exclu. Au moment du `WhenUnitBeDefeated`, le vaincu est
  ENCORE dans la rangée : prendre « le premier restant » (l'ancienne version, jamais branchée avant le
  27/10/2026) donnait un mauvais résultat dès que le vaincu n'était pas le premier.
- **`Villains.All(effect)` doit refléter l'ordre d'entrée en jeu** (gauche → droite) pour que l'avance du jeton ait
  un sens ; aucun tri explicite n'est fait, à vérifier en partie réelle si l'ordre de la zone méchant ne suit pas
  l'ordre d'entrée (§9 du guide).
- **Un deck signature créé une fois reste attaché à la carte `Card` tant qu'elle existe**, y compris vaincue (le
  livret : « its signature deck aside next to it » — PAS détruit). S'il entre en jeu une seconde fois (repiochée du
  Horde deck après un passage en défausse), `DeckSignatureDe` le retrouve tel quel plutôt que d'en recréer un
  (cohérent avec « it »).
- **Chewie (Survivor deck) discard un Metazombie OU un Zombie** par son action : ne pas confondre avec
  `QuandMetazombieVaincu`, qui ne s'applique qu'à une VRAIE défaite (dégâts à 0 PV), pas à une défausse directe.
- **`AbilityType.Scenario` reste actif HORS JEU** : les trois stades du Cœur portent `ReglesDuScenario`, et le stade
  suivant (encore dans le deck des stades) déclenchait chaque règle une seconde fois (mesuré en autoplay le
  27/10/2026). D'où la condition `coeur_en_jeu` sur chaque règle : ne jamais la retirer.
- **Les règles du livret sont portées par le Cœur** : un cas de test monté sur un autre scénario (Rhino) ne les
  a que si `hg001` (ou hg002/hg003) est en jeu. Contre-cas « sans le Cœur » dans `tools/cas/the_hunger_core.py`.
- **Infection (livret p. 5)** : la pose « 1 compteur par attaque d'un ennemi ZOMBIE/METAZOMBIE qui blesse le
  héros » est dans `ReglesDuScenario` (`AfterUnitAttackAndDamageUnit(..., Hero, ...)`). La LIMITE (7, 6 en
  expert : héros vaincu, sa version zombie entre en jeu) et le choix de la récupération de base (soigner OU
  retirer 3 Infection) ne sont PAS codés au 27/10/2026.

**Variantes maison** : aucune à ce jour.
