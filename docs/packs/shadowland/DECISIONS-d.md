# Shadowland : decisions de l'agent D (Ninja Swarm sl028-sl036, Black Flower sl072-sl078)

Format : decision, raisonnement. Aucune question n'a pu etre posee a l'utilisateur (pas de livret officiel).

1. **Creeping Corruption (sl072a/b) : le joueur « est vaincu » = son identite est vaincue.** Selon la Rules Reference, un joueur est elimine quand son identite est vaincue ;
   le moteur fait deja `Identity.OnBeDefeated -> Player.Eliminate`. On passe donc par `Faces.DefeatUnits([identite])` (les interruptions de defaite restent valables) et non par
   `Player.Eliminate` direct. Dans une partie a un joueur la partie est perdue ; a plusieurs, la regle d'elimination habituelle s'applique.
2. **« When Defeated » d'un sbire : la carte vaincue est encore en jeu pendant la resolution** (comportement du moteur, conforme a la RR : une carte vaincue quitte le jeu
   APRES ses capacites « When Defeated »). Consequence pour Bo Staff / Fukiya / Katana / Kusarigama / Shuriken : le sbire Teamwork qu'ils revelent trouve le sbire
   vaincu comme « autre sbire NINJA en jeu » et s'active. Mesure par le cas `sl034 ... SEUL NINJA en jeu`.
3. **Teamwork (NINJA)** est lu dans `desc` (natif, `Teamwork: NINJA`, ajoute sur sl029-sl034, absent de la transcription automatique). Regle de jeu reelle : `v16_all`
   (seul le sbire qui arrive s'active) ; les cas posent `regles: [v16_all, v18_all]`. Sous la regle par defaut du moteur (pre-1.6) tous les sbires Teamwork de meme trait s'activeraient.
4. **« the first minion with the teamwork keyword »** : premier dans l'ordre de defausse (la carte du dessus d'abord) ; « with the teamwork keyword » = mot-cle IMPRIME
   (`printed_teamwork`), car une carte defaussee n'a plus de mots-cles courants.
5. **« The defeating player »** : le joueur qui a vaincu le sbire ; a defaut (vaincu par un effet sans joueur : retaliate...) le joueur avec qui il etait engage.
6. **Kirigi, « either spends 2 resources of any type or shuffles Kirigi »** : choix du joueur ; la branche « depenser » n'est offerte que si elle est payable (sinon le moteur
   la reduirait au plus gros morceau payable). S'il choisit de depenser, Kirigi reste defausse.
7. **Corrections de `data/cards.json`** apres relecture des scans : Teamwork NINJA (sl029-sl034), Toughness (sl030), Boost 1 (sl036), StartingThreat 1 par joueur (sl075),
   StartingThreat 1 et Acceleration 2 (sl076), Permanent/Setup/MaxPerUnit (sl072a) et Permanent/MaxPerUnit (sl072b). L'ATQ « 1★ / 3★ » est celle du texte : la valeur reste 1 / 3.
