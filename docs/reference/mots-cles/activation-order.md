# Activation Order (The Vault, Kajislav)

**Texte imprimé / définition** : « Each villain in this scenario has the text "**Activation Order X**". This text determines the order in which the
villains activate. » (insert The Vault p.2). Règles du livret :
- Étape 2 de la phase du méchant, **moins de vilains que de joueurs** : le vilain de plus petit ordre active contre le 1er joueur, le 2e plus petit
  contre le 2e joueur, etc. ; on recommence jusqu'à ce que chaque joueur ait subi UNE activation (exemple : 4 joueurs, Nekra 6 et Venom 8 : Nekra→J1,
  Venom→J2, Nekra→J3, Venom→J4).
- **Autant ou plus de vilains que de joueurs** : même distribution, puis les vilains pas encore activés continuent contre le 1er joueur, le 2e... jusqu'à ce que
  tous les vilains en jeu aient activé une fois (exemple : 2 joueurs, 4 vilains Batroc 1, Mentallo 2, Nekra 6, Venom 8 : Batroc→J1, Mentallo→J2, Nekra→J1,
  Venom→J2).
- Si l'Interruption forcée du complot principal fait entrer un nouveau vilain pendant l'étape 2, il n'active que si son ordre dépasse celui du vilain qui
  vient d'activer.
- **Sbires** : s'il y a autant ou moins de vilains que de joueurs, ils activent comme d'habitude après le vilain ; s'il y en a plus, ils activent après la
  PREMIÈRE activation d'un vilain contre le joueur auquel ils sont engagés.
- F.A.Q. : si le vilain d'ordre 1 est étourdi, la carte d'état REMPLACE son activation ; le suivant (ordre 6) active contre le 2e joueur.
- « The villain » (cartes de rencontre) = le vilain de plus petit ordre ; une carte JOUEUR choisit le vilain visé ; une carte attachée à un vilain désigne ce vilain.

**Mécanisme moteur** : `desc.ActivationOrder` (entier, lu par `Villain.activation_order`, `card/face/base/villain.py`). La règle se pose à la mise en place :
`Villains.SetRule(effect, Villains.Rule(the_villain="LowestActivationOrder", player_cards="PlayerChooses", activation_order=True))` (vt017a). Avec
`activation_order=True`, `World.VillainPhase.enemy_activation` appelle `Enemies.ActivationVillainsParOrdre` (au lieu de la boucle « un vilain par joueur »).
Formule : N = max(V, P) activations ; la k-ième (de 0) est le vilain de rang k % V (ordre croissant, recalculé à chaque pas pour voir les entrants) contre le
joueur de rang k % P ; les sbires d'un joueur activent avec la première activation dirigée contre lui (`DoActivateAgainstYouInternal(villains=[...],
include_minion="Engaged"|"None")`). `Villains.ParOrdreDActivation(villains)` donne le tri (ordre croissant, à égalité l'ordre d'arrivée).

**Carte exemple** : `vt001`-`vt016` (Batroc, Mentallo, Grey Gargoyle, Hydro-Man, Mad Thinker, Nekra, Vapor, Venom : ordres 1 à 8). Cas :
`tools/cas/the_vault_b.py` (9 cas : livret p.2, sbires, FAQ étourdi, « the villain »).

**Pièges connus** :
- Un test de plusieurs vilains qui les met en jeu avec `Puzzle.PutIntoPlay` ne les met PAS dans la zone des vilains : `BuildVillainDeck` + `RevealNextVillain()`.
- `SOCLE` des cas : retirer le complot du Rhino (`01097b`), sinon « the main scheme » vise le complot du Rhino, pas `vt017b`.
- Spider-Man a « Great Responsibility » (01061) en main : il interrompt les placements de menace du test ; `main_exclusive: ["01090"]`.
- Cas non couvert en partie : un vilain qui entre en jeu PENDANT l'étape 2 (la règle « ordre supérieur » est codée dans `ActivationVillainsParOrdre`, sans cas dédié).

**Variantes maison** : mot-clé maison propre au scénario The Vault (fiche créée le 25/10/2026 d'après l'insert ; aucune définition officielle).
