# Audit de la phase du méchant « Sur la table » — 17 octobre 2026

Audit uniquement : aucune correction du code de l’application. Les captures, vidéos et relevés sont conservés avec ce rapport.

## Périmètre et méthode

- Lecture de `DeroulePhase.tsx`, `CoucheRencontreSurTable.tsx`, `places-rencontre.ts`, `mesures-plateau.ts`, `table-calee.ts`, `board.tsx`, des feuilles de style et des tests associés.
- Deux parcours complets en partie réelle locale : Rhino / Spider-Man puis Klaw / Spider-Man, seed 4321, écran 1280 × 720, mode « Sur la table », animations autorisées. Serveur d’audit séparé sur le port 2479 ; aucune reconstruction ou publication de l’interface.
- Sur Klaw : relevé du DOM et de la géométrie des cartes toutes les 75 ms, 371 échantillons. Les horodatages cités ci-dessous sont ceux de `klaw/chronologie.json`, relatifs au chargement de la page.
- Les deux scripts de parcours sont arrivés au bout. Ce sont des explorations avec captures : leur succès ne certifie pas la conformité visuelle.
- Les 22 tests unitaires de placement et de calage exécutés lors du premier diagnostic passent. La grande suite `DeroulePhase.test.tsx` n’a pas de résultat final récupéré ; elle n’est donc pas déclarée validée.

Limites : les deux phases observées se sont jouées en alter ego, donc avec manigance. La commande prévue pour passer en héros n’a pas produit d’attaque dans le parcours Klaw. Les deux boosts de son attaque, la défense, les autres résolutions de boost ★, le multijoueur et le mobile ne sont pas validés visuellement par cet audit. Les conclusions correspondantes restent des constats de code ou des risques, explicitement indiqués.

## Constats observés

### 1. Priorité haute — une rencontre est déjà en jeu pendant sa lecture

**Rhino :** la barre annonce « Peter Parker révèle Casser et Emporter », la carte est présentée près du paquet et une autre représentation est déjà face visible dans la zone des manigances annexes. Voir [rhino/008.png](rhino/008.png).

**Klaw :** à 21 124 ms, la révélation de « Klaw l’Immortel » commence ; l’objet 66 est simultanément présent dans la couche de lecture et dans la table, à `[307,61,85,137]`. Voir [klaw/007.png](klaw/007.png) et le relevé temporel.

**Effet joueur :** le résultat de l’arrivée est visible avant la validation et avant le trajet censé conduire la carte à cette place.

**Cause dans le code :** `cartesAVenir()` masque les entrées des étapes suivantes, mais exclut l’étape actuellement lue. `majInstantanes(..., rafraichirEntrees=true)` rafraîchit précisément les instantanés d’entrée pour qu’ils contiennent la carte en jeu. Cette règle convient à une présentation « entrée à son écran », mais pas à « lecture, validation, puis arrivée ».

### 2. Priorité haute — la même rencontre part pendant qu’elle est encore présentée

Sur Klaw, à 21 163 ms, l’objet 66 existe à la fois sous `.est-revelee` et sous `.est-depart`, alors que la barre affiche toujours « Peter Parker révèle Klaw l’Immortel ». La copie en départ reste présente pendant que la copie de lecture devient entièrement visible. À ces deux représentations s’ajoute la carte de la table du constat 1.

**Effet joueur :** plusieurs exemplaires visuels et un départ qui ne correspond pas à une fin de lecture compréhensible.

**Cause probable :** l’effet de départ est déclenché par tout changement de clé d’étape. Il vérifie que les clés diffèrent, sans vérifier que l’identité de la carte change ni que la lecture a été validée. Une même carte peut passer d’une étape d’entrée à une étape de révélation. Le parcours ne journalise pas les clés internes ; ce déclencheur précis reste une explication de code, pas une trace directe des clés.

### 3. Priorité haute — le bilan apparaît avant la fin du dernier trajet

Sur Klaw, à 23 263 ms, la barre affiche déjà « Fin de la phase du méchant » et propose de terminer, tandis que la rencontre 66 commence un nouveau départ. Ce départ ne disparaît qu’à 25 363 ms.

**Effet joueur :** la phrase suivante est disponible pendant qu’une action précédente est encore en cours.

**Cause certaine dans le code :** le vol de rencontre dure 2 000 ms dans `CoucheRencontreSurTable`, mais ne publie pas d’état d’attente au parent. `avancer()` retient les clics pendant les vols de jetons, pas pendant les vols de cartes rencontre. La suite du récit et le vol ont donc des rythmes indépendants.

### 4. Priorité moyenne — les rencontres sont agrandies près du paquet, pas au centre

Confirmé sur Assaut, les Ruées, Casser et Emporter et Klaw l’Immortel. Voir [rhino/005.png](rhino/005.png), [rhino/008.png](rhino/008.png) et [klaw/007.png](klaw/007.png).

`placeDeLaRevelee()` place explicitement la carte à côté du deck avec un agrandissement de 1,7. Sur Klaw, la carte horizontale de lecture mesure environ 176 × 132 px, près du bord supérieur gauche : la présentation centrale et la grande taille demandées ne sont pas réalisées.

### 5. Priorité moyenne — le boost apparaît directement au centre dans le parcours mesuré

Le premier échantillon contenant le boost 72, à 15 630 ms, le montre déjà au centre à `[534,224,248,354]`, entièrement opaque. Tous les échantillons suivants gardent exactement cette position jusqu’à 17 188 ms. Aucun trajet depuis le paquet n’est relevé, malgré une transition prévue de 900 ms.

À 17 263 ms, le rangement automatique a commencé. Le boost disparaît avec le changement d’étape vers 17 638 ms, avant que sa transition de rangement de 900 ms ait pu finir.

**Effet joueur :** apparition au centre, rangement automatique, puis disparition interrompue. Le geste complet « sortir du paquet, lire, rejoindre sa place » n’est pas garanti.

**Cause probable de l’apparition directe :** la mesure des ancres et le changement d’état vers `centre` ne garantissent pas un premier rendu peint à la position du paquet. Une transition CSS ne suffit pas si le premier état visible est déjà l’état d’arrivée.

### 6. Priorité moyenne — le départ peut changer brutalement la taille de la carte

Pour l’objet 66, la représentation de lecture stabilisée mesure 176 × 132 px ; la représentation de départ relevée à 21 163 ms mesure 299 × 224 px. Elle grossit donc au moment où elle est censée rejoindre la table.

**Cause à examiner :** le calcul `sortie.de.w / sortie.vers.w` est appliqué comme échelle à une `ScanCard` dont la géométrie peut varier avec l’orientation et la taille transmise par `--card-w`. Les boîtes mesurées ne constituent pas une garantie que les dimensions visibles initiales du vol correspondent à celles de la lecture.

## Constats de code et risques restant à reproduire

### 7. Les boosts se rangent au minuteur, sans validation de lecture

Le rangement est déclenché 1 700 ms après que tous les boosts sont comptés comme vus, indépendamment du clic du joueur et de la fin réelle de leur trajet d’entrée. Le changement d’étape peut ensuite démonter ces cartes avant leur arrivée.

**Rectification du premier topo :** les « environ 0,8 seconde de lecture » étaient un calcul théorique, si le trajet d’entrée de 900 ms se joue entièrement. Dans le parcours mesuré, ce trajet n’est pas visible et le boost reste plutôt environ 1,6 seconde déjà au centre avant de commencer à se ranger. Le défaut certain est le minuteur indépendant de la lecture, pas une durée universelle de 0,8 seconde.

### 8. L’ordre des boosts est contradictoire dans les différents morceaux de code

Le commentaire de la couche décrit « première carte au milieu, deuxième à côté, puis rangement ». Le déroulé initialise pourtant `boostsMontres` avec tous les boosts en mode table. Un test exige explicitement leur sortie ensemble. Les commentaires conservent aussi d’anciennes demandes différentes : un boost par clic, tous ensemble, puis séquence coordonnée.

Il faut distinguer ces contradictions d’un défaut démontré en partie : le parcours Klaw n’a pas produit d’attaque à deux boosts. Il confirme un boost de manigance seulement. La demande actuelle de l’utilisateur sur la lecture centrale reste la référence ; cet audit ne tranche pas à sa place un ancien choix de cadence.

### 9. L’attente pendant un vol de jeton ne suspend pas toute la présentation suivante

Dans l’enveloppe sur table, le contenu textuel est masqué par `enVolDeJeton`, mais `CoucheRencontreSurTable` reste montée avec `actif` et reçoit l’étape courante, qui peut déjà être la suivante. `EffetsSurTable` n’est pas non plus conditionné par ce vol.

Cela permet un décalage entre ce qui commence à apparaître et la barre temporairement masquée. Ce mécanisme est visible dans le code ; l’apparition précise d’un boost de l’étape suivante pendant un vol précédent reste à reproduire avec une trace ciblée.

### 10. La destination est mesurée pendant que la table peut encore se réorganiser

Le départ relève sa destination une seule fois au changement de clé. Les cartes de la table peuvent encore être en animation ou changer de place. Les fonctions de mesure cherchent aussi des `.scan-card` sans exclure systématiquement la couche de présentation, qui réutilise les mêmes identifiants.

Risques : destination prise sur une représentation temporaire, arrivée sur une position périmée ou départ abandonné lorsqu’aucune destination n’est mesurable. Ne pas attribuer ces trois manifestations à une seule cause sans reproduction dédiée.

## Pourquoi les tests actuels peuvent laisser passer ces défauts

- Les tests de placement valident les coordonnées prévues actuellement, donc aussi le placement près du paquet.
- Le test unitaire de sortie des boosts exige leur sortie simultanée et le passage par un seul geste ; il ne mesure pas le temps de lecture ni la fin des trajets.
- `phase-sur-table.spec.ts` repose sur un état enregistré et indique lui-même qu’il ne vérifie pas le rythme du moteur réel. Il cherche aussi d’anciens éléments `.deroule-rond` et `.deroule-recit`, alors que le rendu actuel emploie `.tsm-acteur` et `.tsm-phrase`.
- La configuration générale Playwright utilise `reducedMotion: 'reduce'`. Les deux explorations de cet audit forcent au contraire `no-preference`, nécessaire pour voir les chevauchements.

## Priorités de reprise, sans implémentation

1. Une carte doit avoir une seule présentation active et son arrivée en jeu doit correspondre à la validation annoncée.
2. La lecture, le départ et l’arrivée doivent informer le récit de leur avancement ; la barre suivante ne doit pas dépendre d’un minuteur distinct.
3. Vérifier le trajet réel depuis le paquet et la continuité de taille au départ, puis le placement central des rencontres.
4. Reproduire une attaque de Klaw à deux boosts, les défenses et les effets ★ avant de conclure sur toute la phase.

Ce rapport n’a apporté aucune correction aux sources, aux styles ou aux tests du jeu. Le lancement du moteur a seulement régénéré ses artefacts de lancement ; les nouveaux fichiers durables de cet audit sont ce rapport et ses preuves.
