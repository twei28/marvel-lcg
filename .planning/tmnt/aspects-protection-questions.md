# Aspect TMNT Protection (up) : questions ouvertes pour l'utilisateur

Une question par carte, multichoix, option recommandée en premier. Scans :
`scratchpad/zip-aspect/TMNT Aspect/Protection/<fichier>` (zip « TMNT Aspect » d'Inkwire).

---

## Q-UP1 : up030 Redirection Mastery : que veut dire « exactly defend an attack » ?

- Scan : `Protection/Redirection Mastery.png`
- Texte imprimé : « Play under any player's control. Max 1 per player.
  **Hero Response**: After you **exactly defend** an attack, deal damage to the attacker equal to your DEF for
  that attack. »
- La tournure « exactly defend » n'existe dans aucune carte officielle ni dans les Rules Reference.

Options :
1. **(recommandée)** « Défense exacte » : la Réponse ne part que si la valeur de l'attaque (boosts compris)
   est **exactement égale** à votre DEF (le coup est paré pile, 0 dégât et 0 DEF perdue). Ce qui change en jeu :
   la carte est rare à déclencher, mais renvoie alors toute votre DEF à l'attaquant.
2. « exactly » est superflu : **après chaque défense** de votre héros contre une attaque, l'attaquant subit des
   dégâts égaux à votre DEF. En jeu : se déclenche à chaque défense (bien plus fort).
3. « exactly » = « sans subir de dégâts » (attaque ≤ DEF), comme Unflappable. En jeu : intermédiaire.
4. Autre (précise).

État : carte saisie (données, image, texte), **sans script** en attendant la réponse : en partie elle ne fait
rien. Carte NON terminée.

---

## Q-UP2 : up018 "I Can Do This All Day" : « Hero Action » au lieu de « Hero Interrupt »

- Scan : `Protection/I Can Do This All Day.png`
- Texte imprimé : « **Hero Action** *(defense)*: When an enemy attacks, declare your hero as the defender
  without exhausting them. » ; l'officielle `56047` dit « **Hero Interrupt** *(defense)* ».
- Une Action ne peut pas porter de déclencheur « When » : coquille probable du reskin (même famille que
  Unified Strike « Hero Response: When »).

Options :
1. **(recommandée)** Coquille : la carte est l'officielle 56047 (Hero Interrupt). C'est ce qui est codé
   (`ability_link` 56047) ; en jeu : se joue pendant l'attaque d'un ennemi.
2. Corriger aussi le texte affiché de la carte TMNT en « Hero Interrupt ».
3. Autre (précise).

État : codé selon l'option 1, cas verts ; carte NON terminée tant que la réponse n'est pas donnée.

---

## Q-UP3 : up024 Nobody (Angel Bridge) : homonyme de `ta002` Nobody (Angel Bridges, allié d'Alopex)

- Scan : `Protection/Nobody.png` (crédit « TMNT Heroes By: Inkwire »)
- Les deux cartes sont uniques et portent le même titre « Nobody » : la règle d'unicité les empêche d'être en
  jeu en même temps (un joueur Alopex qui a ta002 en jeu ne peut pas jouer up024, et inversement). Les deux
  cartes sont différentes (ta002 : coût 2, 1/1, effets liés à Prey ; up024 : coût 3, réponse tough/cloaked).

Options :
1. **(recommandée)** C'est voulu (même personnage) : on garde l'unicité sur le titre, rien à faire.
2. Ce sont deux versions distinctes qui doivent pouvoir coexister (exception d'unicité à coder).
3. Autre (précise).

État : codé selon l'option 1 (règle normale) ; carte NON terminée tant que la réponse n'est pas donnée.
