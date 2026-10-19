# Finitions et fluidité — 18 octobre 2026

## Changements

- Multijoueur : suivi de la résolution même si elle partage la clé de son annonce ; commandes de choix de l’hôte et « Prêt » disponibles sur table. Accord distinct pour chaque état et après le rangement des cartes.
- Bouton « Continuer » dans le bandeau pendant la lecture des grandes cartes ; inactif durant les déplacements. Le raccourci Espace reste disponible.
- Indication explicite pendant l'arrivée des cartes, leur placement et le vol des jetons.
- Survol et focus d'un choix d'amélioration : aperçu et surbrillance de la vraie carte, remontée au-dessus des cartes voisines.
- Calcul compact après résolution : valeur imprimée, bonus, Boost, DÉF, réductions connues et résultat. Les préventions particulières conservent le résultat réel au lieu d'afficher une égalité fausse.
- Déplacements natifs en transform 3D ; suppression du recalcul permanent des destinations. Actualisation sur changement réel de disposition, à partir de la position affichée, en conservant l'échéance.
- Prédécodage des images avant l'entrée, ombres fixes, pulsation par opacité. Les durées de lecture et de vol sont conservées.
- Boutons de lecture d'au moins 44 px sur petite hauteur ou pointeur tactile.

## Mesure de fluidité

Même parcours réel Klaw et même navigateur automatisé local ; intervalles requestAnimationFrame recueillis pendant les entrées et départs.

| Mesure | Avant | Après |
| --- | ---: | ---: |
| Images observées | 91 | 326 |
| Intervalle médian | 66,7 ms | 16,7 ms |
| 95e percentile | 349,9 ms | 33,5 ms |
| Intervalles > 34 ms | 69,2 % | 4,9 % |

Cette mesure locale indique une amélioration nette ; elle ne garantit pas le même débit sur chaque ordinateur ou téléphone. Résumés et captures dans [verification-fluidite-2026-10-18](verification-fluidite-2026-10-18/).

## Vérifications

- TypeScript : succès ; construction locale et contrôle de sortie : succès.
- 286 tests ciblés : succès (lecture, déroulé, décisions, calculs, multijoueur et dimensions des questions).
- Gardes visuels : 14 défenses × 4 fenêtres et 7 questions × 4 fenêtres, aucun bouton rogné.
- 5 contrôles navigateur sur fixture : succès, dont cadre incliné, absence de double panneau et départ des jetons au clic.
- Parcours réels validés : Rhino, Klaw à deux boosts, sélection d'améliorations, plusieurs défenseurs avec Hulk vaincu, petite fenêtre paysage 1050 × 480, boost ★ mettant un sbire en jeu, changement de stade du méchant avec lecture centrale.

Le petit écran est une émulation de dimensions en navigateur de bureau, pas une mesure sur téléphone physique. Les parties de vérification utilisent exclusivement le serveur de test 2493 ; la partie principale 2345 reste intacte.
