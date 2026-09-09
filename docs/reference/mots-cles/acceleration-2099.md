# Acceleration (capacité d'identité, Rainy) — homonyme de l'icône

⚠ **Ce n'est PAS le mot-clé `acceleration.md`.** Deux notions portent le même
mot. L'icône officielle pose de la menace au début de la phase vilain et se
déclare dans `desc.Acceleration` ; la capacité décrite ici est une **capacité
imprimée d'identité**, propre au pack fan-made **Spider-Man 2099** (Rainy),
et n'a aucun rapport. Ne jamais réutiliser `desc.Acceleration` ni
`HasAccelerationIcon` pour elle.

**Texte imprimé / définition** : sur `sm001a` * Spider-Man (face héros) :

> *Acceleration* — [star] **Response**: After your hero uses a basic power,
> seek an event from your deck. You may play that event. Place each other
> card you discarded this way on the bottom of your deck in the order you
> discarded them. *(Limit once per phase.)*

Six cartes du pack testent ensuite « **if you played this card using your
*Acceleration* ability** » ou « after you resolve your *Acceleration*
ability ». Le nom de la capacité est donc un **marqueur** que les autres
cartes lisent, pas seulement de la saveur.

**Mécanisme moteur** :

- Le « seek » est `Player.DiscardDeckUntil(effect, card_type=Event,
  return_other_faces=autres)` (voir `seek.md`) : il DÉFAUSSE depuis le dessus
  du deck jusqu'à défausser un événement.
- « You may play that event » : `Player.PlayCardsLikeInTurn([face], effect)`
  — la carte est dans la défausse, donc `is_like_in_hand` est posé par la
  fonction elle-même (`player_action.py:904`). ⚠ `if_not_play_discard_it`
  vaut `True` par défaut : c'est bien ce qu'on veut, l'événement non joué
  reste défaussé, puis part sous le deck comme les autres.
- « on the bottom of your deck in the order you discarded them » :
  `Faces.MoveAllToDeck(autres, deck, "Bottom", effect)` — la position est un
  **argument positionnel** (RECETTES §2), et l'ordre est celui de la liste
  rendue par `return_other_faces`, qui est déjà l'ordre de défausse.
- **Le marqueur.** Aucune primitive moteur ne dit « cette carte a été jouée
  par telle capacité ». Le pack pose donc son propre témoin sur le joueur au
  moment de l'appel à `PlayCardsLikeInTurn`, et les six cartes le lisent
  dans leur `conditions`. Helper commun du pack :
  `src/cards/pack/spider_man_2099/spider_man_2099/__init__.py`.

**Carte exemple** : `sm001a` * Spider-Man (l'identité qui porte la capacité) ;
`sm003` Accelerated Decoy pour la lecture du marqueur (« do both instead »).

**Pièges connus** :

- ⚠ **« After your hero uses a basic power »** est
  `AfterUnitUseBasicPower(type, "You", op, powers=["ATK","THW","DEF"])`
  (RECETTES §1, modèles `14001a`, `tt001a`). La **récupération** n'est pas un
  pouvoir de base au sens de ce message : elle a son propre
  `AfterUnitMakeRecovery`, et elle n'existe qu'en alter-ego, où cette face
  n'est pas en jeu.
- ⚠ **« Limit once per phase »** exige un témoin d'épuisement
  (PROCESSUS-CARTE 7 bis) : deux pouvoirs de base dans la MÊME phase, et un
  chiffre mesuré au second (taille du deck inchangée).
- ⚠ `sm008` Accelerated Vision donne « one additional time per phase (but
  still once per trigger) » : la limite ne peut donc pas être un simple
  `LimitOncePerPhase()` du moteur, qui ne sait pas compter jusqu'à deux. Le
  pack compte lui-même, par phase, dans le même helper que le marqueur.
- ⚠ Si le deck est épuisé sans trouver d'événement, l'insert tranche :
  mélanger la défausse en un deck neuf, puis placer dessous les cartes
  défaussées par la capacité. `DiscardUntil` gère déjà le remélange
  (`deck.py:483`) ; ce qui reste à la charge de la carte, c'est l'ordre final.

**Variantes maison** : `sm011` Spinnerets et `sm012` Web Cape se branchent
« after you resolve your *Acceleration* ability », c'est-à-dire **même quand
aucun événement n'a été joué** ; `sm010` Hyper-Agility, elle, exige
explicitement « **without playing an event** ». Trois portées différentes du
même déclencheur : les lire mot à mot.
