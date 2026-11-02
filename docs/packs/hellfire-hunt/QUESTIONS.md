# Hellfire Hunt (fondations et campagne) : vrais doutes restants

Chaque entrée : ce qui bloque, les lectures possibles, la recommandation. Décidé d'après le livret (`ruleBookPages/file_compressed.pdf`, p.20 pour les decks).

## 1. Deck de Sunspot incomplet : 10 cartes absentes
Livret p.20 : Aggression `Finishing Blow (x3)` ; Basic `Cecilia Reyes`, `For What's Right (x3)`, `X-Force Strike (x3)`. Aucune n'existe dans `data/cards.json` (recherche par nom, tous sets) ni dans le zip.
Lectures : (a) ce sont des cartes officielles que le catalogue ne contient pas (à importer) ; (b) des cartes maison de l'auteur, non livrées. Effet en jeu : `deck/starter/sunspot_hellfire.json` a 15 cartes au lieu de 25.
Recommandation : fournir les images/données de ces 4 cartes ; en attendant, le deck monte une partie (verifier_tous_les_decks) mais il est plus court que celui du livret.

## 2. Nemesis « Mutant Kidnapping » (p.20) = so016 « Political Persecution » ?
Le livret cite `Mutant Kidnapping` ; le catalogue a `so016 Political Persecution` en carte nemesis. Même emplacement ? À confirmer sur le scan de so016.

## 3. Marvel Girl : X-Gene (x2) mais « Max 1 per player »
Le deck `rachel_summers.json` ne porte qu'un X-Gene. Lecture A : suivre la limite imprimée (1) ; B : suivre la liste du livret (2). Recommandation : A.

## 4. Joueur éliminé en campagne experte (livret p.7)
« Le joueur éliminé peut rejoindre en plaçant un pion d'accélération pour restaurer son identité. » Implémenté : il revient avec sa dernière valeur de PV au carnet et peut être soigné par le pion (question habituelle), sans que le pion soit imposé. Lecture stricte : le pion est le prix du retour. Recommandation : garder l'implémentation (le retour reste gratuit mais sans soin automatique).

## 5. Potential Ally aux scénarios 2 et 5
Le livret ne demande de mélanger une Potential Ally qu'aux scénarios 1, 3 et 4 (p.8, 12, 14) ; la mise en place les mélangeait à chaque scénario. Corrigé d'après le livret. Si l'auteur voulait les mélanger aussi aux scénarios 2 et 5, ajouter 2 et 5 à `NIVEAUX_POTENTIAL_ALLY` (`campaign.py`).

## 6. Emma Frost recrutée deux fois ?
Vaincre Emma Frost's Redemption (scénario 2) met Emma en jeu et la note recrutée ; le scénario 3 dit pourtant « shuffle Emma Frost into the Recruited Mutants deck » si la case est cochée. Lecture retenue : une seule Emma (alliée unique), pas de doublon.
