# Tour supplémentaire et « end this turn » (« take an additional turn », « end this turn »)

**Texte imprimé / définition** : « Take an additional turn after this one. At the end of this turn, perform each of the following
in order: discard any number of cards, and discard down to your hand size; draw up to your hand size; ready all of your cards »
(`rm007` Temporal Reversal) et « Discard this obligation **and end this turn** » (`rm013` Memory From The Future). Pas des mots-clés
officiels : deux MÉCANIQUES du pack `rachel_summers` (`rm`, Dipsome), absentes du moteur officiel (aucune carte du dépôt ne donne un
tour de plus, ni ne finit le tour du joueur à sa place).

**Mécanisme moteur** (CORRECTIFS du 26/10/2026, tous derrière un drapeau de joueur, rien ne change tant qu'il est à zéro) :
- **Drapeaux** `player.flag` : `RM_TOUR_SUPPLEMENTAIRE` (nombre de tours en plus) et `RM_FIN_DE_TOUR` (un tour à finir), déclarés dans
  `PlayerFlag.FLAG` (`player_flag.py`).
- **Un tour de plus** : la carte fait `joueur.flag.Update("RM_TOUR_SUPPLEMENTAIRE", 1)`. `World.PlayerPhase` (`world.py`) rejoue, juste
  après le tour du joueur (donc avant le joueur suivant), `FinDeTourSupplementaire()` puis un tour complet (`BeginTurn`, `PlayerTurn`,
  `EndTurn`), tant que le drapeau est positif. `has_finished_turn_this_round` repasse à faux pendant ce second tour.
- **Les trois étapes** : `PlayerPhase.FinDeTourSupplementaire()` (`player_phase.py`) = `MayDiscardHandCardsAndDrawUpToMax` (celles de la
  fin de phase : défausser autant qu'on veut et au moins jusqu'à la taille de main, puis piocher jusqu'à la taille de main) puis
  redresser `GetControlCards()` et leurs améliorations (même périmètre que `EndPhase`).
- **Finir le tour** : la carte fait `joueur.flag.Set("RM_FIN_DE_TOUR", 1)` (`PlayerActionToDiscardThis(.., ex_operation=fn)`). La boucle
  d'actions du tour (`EventManager`, message `WhenPlayerInTurn`) lit le drapeau en tête de chaque tour de boucle, le remet à zéro et
  s'arrête comme si le joueur avait choisi de finir. `BeginTurn` le remet à zéro à chaque tour.
- **Harnais** (`puzzle.py`) : `Puzzle.BeginPlayerTurn()` (envoie `WhenPlayerTurnBegin` + `AfterPlayerTurnBegin`, la mise en place d'un cas
  se joue DANS un tour déjà ouvert) et `Puzzle.FinDeTourSupplementaire()` (les trois étapes seules).

**Carte exemple** : `rm007` Temporal Reversal (« Max 1 per round » = `.MaxOnePerRound()`), `rm013` Memory From The Future.

**Pièges connus** :
- Le harnais joue le cas DANS une question du pilote : la boucle d'actions du tour n'a pas tourné depuis la carte. Le vérificateur
  `rm_etat` (clé `rm_tour_fini`) la REJOUE par `Message.WhenPlayerInTurn(joueur, round_id).Send()` : drapeau lu, remis à zéro, aucune
  question posée. Le tour de plus de `World.PlayerPhase` n'est pas exerçable par un cas : seul l'autoplay le montre (ligne « Additional turn »
  du journal).
- « At the end of THIS turn » : les trois étapes se font à la fin du tour qui a joué la carte, avant le tour de plus (pas à la fin du tour de plus).
- Les capacités « après le début de votre tour » (Chronoskimming, Captain Britain, Hound Program) repartent au début du tour de plus.

**Variantes maison** : aucune autre.
