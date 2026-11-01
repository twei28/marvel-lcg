# Hellfire deck (deck de TABLE avec défausse propre, scénario 4 « Torn » de Hellfire Hunt)

**Texte imprimé / définition** : complot 1A The Hellfire Club's Revenge : « Shuffle every ELITE, HELLFIRE minion to create the Hellfire deck and set it next to the encounter deck. » Livret p. 14 :
« The Hellfire deck has its own discard pile. When a ELITE, HELLFIRE minion is defeated or otherwise discarded, place it in the Hellfire discard pile. If the Hellfire deck is ever empty, shuffle Hellfire
discard pile into the Hellfire deck. There is no penalty for doing this. » Complot 1B : « each player not engaged with an ELITE, HELLFIRE minion reveals the top card of the Hellfire deck ».

**Mécanisme moteur** : maison, sans mot-clé. `cards.pack.hellfire_hunt_torn.DeckHellfire(effect)` crée À LA DEMANDE un `Deck2` de type `AdditionalDeck` (propriétaire = le scénario) et un `AdditionalDiscardPile`,
ajoutés à `world.additional_decks` / `additional_discard_piles` (le descripteur du monde les publie, comme le deck Recruited Mutants) ; état gardé sur `monde.hf_hellfire = (deck, défausse)`.
`ConstruireLeDeckHellfire` (Setup de 1A) déplace les sbires ELITE HELLFIRE du deck de rencontre dans le deck et pose sur chaque carte `card.bind_discard_pile = défausse` : c'est ce qui envoie un sbire
vaincu ou défaussé dans la défausse Hellfire (`Card.Discard`). `RevelerDuDeckHellfire` remélange la défausse dans le deck s'il est vide (aucune carte distribuée) puis `face.Reveal(joueur, effect)`.
Table : `ui-app/src/board/zones.ts` (`sontDuHellfire` : deck et défausse dont TOUTES les cartes ont les traits `t_ELITE` et `t_HELLFIRE`) les pose sous le deck de rencontre.

**Carte exemple** : `hf503a` (Setup), `hf503b` (révélation au début de la phase des joueurs), `hf505` Protect Students (coût « reveal 1 card from the Hellfire deck »), `hf354` (le manteau cherche Cassandra dans le deck).
Cas : `tools/cas/hellfire_torn.py` (`[hf] hf503a ...`, `[hf] hf503b ...`), plateau : `ui-app/src/board/torn-hellfire-plateau.test.ts`.

**Pièges connus** :
- le complot 1B révèle un sbire dès la 1re phase des joueurs : un cas qui ne vise pas le Hellfire deck doit retirer ce sbire (`Puzzle.RemoveMinionsInPlay()`, clé `libre`) ;
- `CartesDuHellfire` ne CRÉE jamais le deck (le scénario 5 joue Immensity sans Hellfire deck) ; `Puzzle.PutIntoHellfireDeck` / `Puzzle.EmptyHellfireDeck` (AJOUT moteur) le créent / le vident ;
- White Queen (Perfection, hf301/hf302) ne peut pas entrer en jeu pendant que le VILAIN White Queen y est (scénario 1) : correctif du 01/11/2026 dans `hellfire_hunt_white_queen/__init__.py` (voir QUESTIONS n°6).

**Variantes maison** : aucune.
