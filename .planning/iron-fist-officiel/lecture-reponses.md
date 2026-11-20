# Iron Fist officiel : réponses de l'utilisateur à la lecture des cartes (19/10/2026)

Questions posées une à une, en multi-choix, carte à l'appui. Rien n'est encore créé (ni `cards.json`, ni script, ni image).

1. **Où s'attache une Technique mise en jeu par Danny Rand (Meditation) ou par Book of the Iron Fist ?**
   → **Sur l'identité du joueur**, sans choix. Raison : toutes les Techniques parlent d'« Iron Fist ». (À coder : mise en jeu attachée à la carte identité, face héros ou alter ego.)
2. **Quand Danny se retourne en Iron Fist, que deviennent les Techniques en jeu (elles redeviennent Temporary) ?**
   → **Défaussées à la fin du round** (lecture littérale du mot-clé). Source : l'article officiel de Fantasy Flight dit que retourner Danny Rand supprime Temporary « pour aussi longtemps qu'il reste en alter ego » ; aucun ruling sur le retour en héros. (À coder : « Your Technique cards lose temporary » = effet actif seulement face Danny visible ; la défausse de fin de round (`ProcessTemporary`) regarde alors l'état courant.)
3. **The Way of Things : les deux « a scheme » peuvent-elles être la même manigance ?**
   → **Au choix, la même ou une autre.** (À coder : deux choix de cible indépendants.)
4. **Deep Breathing sans aucune carte « Iron Fist » dans le deck ?**
   → **Tout le deck est défaussé, rien n'est ajouté** (lecture littérale de « until »).
5. **Les jetons de chi au retournement de l'identité ?**
   → **Ils restent sur l'identité.** Source officielle : le Rules Reference (v1.5 et v1.7) dit qu'au changement de forme le personnage conserve ses dégâts, cartes de statut, effets durables, attachements, jetons et son état prêt/épuisé. Le chi ne bouge donc pas ; la Forced Response de la face héros ne le ramène à 4 qu'en forme héros.

## Reste à faire avant création (PROCESSUS-CARTE.md)
- Étape 2 : carte de référence du moteur pour chaque capacité (compteur à poser « ici » : modèle `calm` de Lockjaw `lj017` ; retaliate X dynamique ; « Hero Resource » ; « lose temporary »).
- Nouveaux éléments moteur : compteur `chi`, traits (Technique, Martial Artist, K'un-Lun, Persona, Skill, Superpower).
- Scans haute définition à la sortie du pack (novembre 2026) ; les 11 cartes lues en 300 px sont à relire.
