# Find

**Texte imprimé / définition** : « find [carte] » (Rules Reference v1.8, p. 19, FIND) : *« When instructed to find a card, a
player searches each game area where that card could be found (play area, set-aside area, player deck, discard pile,
encounter deck, etc.). »* Tout est fouillable sauf les cartes de rencontre face cachée en jeu (cartes distribuées ou cartes
de boost), la pile de victoire et les cartes retirées de la partie. « Find and reveal » un sbire DÉJÀ EN JEU : le joueur
s'y engage et résout ses « When Revealed », sans qu'il « entre en jeu ».

**Mécanisme moteur** : pas de mot-clé natif, une recherche suivie d'une action.
- Deck rencontre (+ défausse) : `Search.EncounterCard(effect, include_discard_pile=True, name="...", card_type=Treachery)`
  (`game/operate/search.py`), qui rend la carte ou `None`. Ajouter `include_set_aside=True` pour la zone mise de côté.
- Révéler ce qu'on a trouvé : `face.Reveal(joueur, effect)`.
- Carte déjà en jeu (« find ... Pursued by the Past ») : `Worlds.FindCardOnField(effect, name="...")`.
- Cartes du set némésis du joueur : `player.set_aside_nemesis_sets` (voir `01190`, `45075b`).
- Branche « If you cannot » : le `None` de la recherche, JAMAIS une erreur.
- Ce n'est PAS « seek » (voir [[seek]]) : `find` ne défausse rien et ne traverse pas le deck carte par carte.

**Carte exemple** : `hp013` Identity Crisis (pack `wasp_hank_pym`) : « find Shadow of the Past and reveal it. If you cannot,
place 7 pursuit counters on Pursued by the Past » ; `hp018` Submit or Perish (recherche d'Ultron dans le deck et la défausse) ;
`sk193a` (`Search.EncounterCard` + `Reveal`).

**Pièges connus** :
- **Chercher une carte « absente » avant d'écrire qu'elle manque.** `01190` Shadow of the Past (set Standard) et `45075a/b`
  Pursued by the Past (Standard III) sont des cartes OFFICIELLES du moteur : la note « absentes du zip » du pack Wasp (26/10/2026)
  était fausse et avait fait coder `hp013` sans sa branche à 5 compteurs. Un `grep` dans `data/cards.json` d'abord.
- `45075a` ne réagit qu'à un compteur « pursuit » posé PAR UN JOUEUR (`message.place_player`, `sender_token.py` :
  `get_place_player`). L'effet d'une obligation a le VILAIN pour initiateur et un message d'unité : `place_player` vaut `None`
  et rien ne se passe, sans erreur. Poser les compteurs avec `GameRule(joueur.GetIdentity())` comme `by_effect`
  (modèle `iron_lad`). `by_player=` de `Faces.PlaceCountersOn` est accepté mais IGNORÉ.
- Pour tester une carte à deux faces (`45075a` / `45075b`) : `Puzzle.PutIntoPlay('45075a,45075b')`. Avec la seule face `a`,
  le retournement ne fait rien.

**Variantes maison** : aucune.
