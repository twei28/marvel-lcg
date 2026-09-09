# Seek (mot-clé maison, Rainy)

**Texte imprimé / définition** : « Seek a minion from the encounter deck »,
« seek an event from your deck ».

> ### ✅ DÉFINITION DE L'AUTEUR, TROUVÉE LE 08/09/2026
>
> L'insert du pack **Spider-Man 2099** la donne noir sur blanc :
>
> > **New Keyword: Seek.** The seek keyword is a shorthand term for an ability
> > that **discards cards from the top of a deck until a certain type of card
> > is discarded**. For example, "Seek an event from your deck." is shorthand
> > for "Discard cards from the top of your deck until you discard an event."
>
> ⚠ **Ce n'est PAS une recherche.** La version retenue au dépôt jusqu'à cette
> date — « chercher la carte dans la zone, la prendre, mélanger » — ne
> défaussait rien : elle donnait le même résultat visible (on obtient la
> carte) en cachant tout le coût réel (le deck se vide, la défausse se
> remplit, et les cartes traversées sont perdues pour ce tour). Sur
> Spider-Man 2099 la différence n'est même pas subtile : `sm002` Ghost Rider
> se déclenche « after Ghost Rider is **discarded** by your *Acceleration*
> ability », donc la lecture « recherche » rendrait la carte inerte.
>
> **Arbitrage utilisateur du 08/09/2026 : corriger partout.**

**Mécanisme moteur** : deux primitives natives, une par zone, et elles
existaient déjà — c'est bien la lecture qui était fausse, pas l'outillage.

- Deck du **joueur** : `Player.DiscardDeckUntil(effect, card_type=Event,
  return_other_faces=autres)` (`player_action.py:1028`). Rend la carte
  trouvée, remplit `autres` avec les cartes traversées.
- Deck **rencontre** : `Worlds.DiscardEncounterCardsUntil(effect,
  card_type=Minion, return_other_faces=autres)` (`worlds.py:540`), même
  contrat. Modèles officiels : `01116b`, `01117a`, `45147b`, `ag013`.
- Les deux passent par `Deck.DiscardUntil` (`deck.py:443`), qui **défausse
  aussi la carte trouvée** avant de la rendre. Une carte « mise en jeu »
  ensuite part donc de la **défausse**, pas du deck.
- Le remélange en fin de deck est géré par `DiscardUntil` lui-même
  (`deck.py:483`).

**Carte exemple** : `sm001a` * Spider-Man (Spider-Man 2099), la carte qui
porte la définition de l'auteur dans son propre pack.

**Pièges connus** :

- ⚠ **Sans `include_encounter_discard_pile`, la défausse n'est pas fouillée**
  — et avec la vraie définition, la question ne se pose plus : on ne fouille
  rien, on défausse depuis le dessus.
- ⚠ La carte trouvée arrive dans la **défausse**. La remettre en jeu ou en
  main est une étape SÉPARÉE (`Faces.AddToHand`, `PutIntoPlay`), qu'il faut
  écrire.
- ⚠ Un deck vide rend `None` : toute carte qui « seek » doit prévoir la
  branche sans trouvaille.

**Ne relèvent PAS de ce mot-clé** (vérifié texte en main le 08/09/2026) :

| Carte | Texte imprimé | Pourquoi |
|---|---|---|
| `56007` Hunted | « **search** the encounter deck and discard pile » | carte **officielle**, le mot « seek » n'y figure pas |
| `br011` Hammer Time | « **Search** the encounter deck for a minion » | Rainy écrit « search » ici, pas « seek » |

**Cartes réellement concernées par la correction du 08/09/2026** : `br005`
Star Jump (« Seek a minion from the encounter deck »), `br009` Oathbrother
(« seek an event from your deck »), `ar001a` * Ares (« Seek a minion from the
encounter deck »).

**Variantes maison** : « Find a Beta Ray Bill card » (`br005`, troisième
puce) est un autre verbe, et **celui-là est bien une recherche** : il n'est
pas touché par la correction.
