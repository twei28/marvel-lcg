# Initiative

**Texte imprimé / définition** : « INITIATIVE. SKRULL. » : la première ligne de traits de `sk263` * Crusader
(allié de campagne, Skrull Menace, Kajislav). Le mot est imprimé dans la police des traits, en italique gras, sans texte de
rappel entre parenthèses ni définition : **ce n'est pas un mot-clé**, c'est un TRAIT. Le brief de portage demandait de
chercher un éventuel « mot-clé maison » : recherche faite (moteur, 4 000 cartes du catalogue, les cinq transcriptions de
Skrull Menace, le livret de campagne), aucune règle ne définit « Initiative ».

**Mécanisme moteur** : aucun. Le trait est déclaré dans le `Literal` `TRAITS` de
`src/game/card/face/card_face.py` (purement déclaratif, comme `LIZARD` ou `HYBRID` : `TRAITS` n'est qu'un type) et porté par
`paper.traits` (`"traits": ["INITIATIVE", "SKRULL"]` dans `data/cards.json`). `HasTrait("INITIATIVE")` répond vrai ; aucune
capacité du jeu ne le lit.

**Carte exemple** : `sk263` : * Crusader. Aucune ligne du script ne lui est consacrée ; le script porte seulement la Réponse
imprimée (« After Crusader enters play, choose a player → deal 1 damage to the villain and each minion engaged with that
player. Draw 1 card for each enemy defeated this way. »).

**Pièges connus** :
- Ne pas confondre avec le SET officiel « The Initiative » (pack `cw`, scénario Iron Man) : c'est le nom d'un ensemble de
  rencontre (`data/encounter_sets/the_initiative.json`), pas un trait de carte.
- Ne pas inventer un comportement (priorité, première activation...) : le texte de la carte n'en dit aucun. Si l'auteur
  révèle une règle (le trait pourrait être lu par une carte de l'extension non fournie), l'ajouter ici ET dans
  `defs/campagne_cartes_questions.md` (Q1).

**Variantes maison** : aucune.
