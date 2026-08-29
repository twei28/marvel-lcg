# Guard

**Texte imprimé / définition** : « Guard. » Un minion avec ce mot-clé doit
être combattu ou surmonté en priorité : tant qu'il est engagé, les autres
minions ou le vilain ne peuvent pas être attaqués, et lui seul peut
recevoir du thwart tant qu'il reste en jeu (sauf effet contraire). C'est
un compteur (`Guard 1`, `Guard 2`, ...), réinitialisé à sa valeur imprimée
à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Guard` sur la carte, lue nativement par
le moteur. `HasGuard` (`src/game/card/face/attribute/has_guard.py`)
enregistre l'attribut `Guard` -> `printed_guard`, restaure la valeur à
chaque `OnResetKeywords` via `GainGuard`, qui appelle aussi
`ClearGuardPatrolEffectTargets` / `SetGuardPatrolEffectedBy` pour recalculer
les cibles valides d'attaque/thwart affectées par Guard/Patrol. La
priorité de ciblage est appliquée ailleurs dans le moteur (sélection de
cibles, `card_finder`). **Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01101` : Hydra Mercenary (`desc` contient `"Guard":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01101.py` trouvé dans `src/cards/pack` : cette carte n'a pas de capacité
imprimée distincte nécessitant un script.

**Pièges connus** : Guard est associé à Patrol dans le moteur (même
mécanisme de restriction de cible, `GuardPatrolEffectedBy`) ; ne pas
confondre les deux fiches. Si une future carte cumule Guard avec une
capacité imprimée annexe (par exemple une réaction au combat), vérifier
via `find` si un script existe pour cette carte : le script devra porter
uniquement cette capacité annexe, jamais le mot-clé Guard lui-même.

**Variantes maison** : aucune recensée pour l'instant.
