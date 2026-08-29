# Guard

**Texte imprimé / définition** : « Guard. *(While this minion is engaged with
you, you cannot attack the villain.)* » Tant qu'un sbire Guard est engagé avec
un joueur, CE joueur ne peut pas attaquer le vilain. C'est un compteur
(`Guard 1`, `Guard 2`, ...), réinitialisé à sa valeur imprimée à chaque reset
des mots-clés.

**Mécanisme moteur** : clé `desc.Guard` sur la carte, lue nativement par
le moteur. `HasGuard` (`src/game/card/face/attribute/has_guard.py`)
enregistre l'attribut `Guard` -> `printed_guard`, restaure la valeur à
chaque `OnResetKeywords` via `GainGuard`, qui appelle aussi
`ClearGuardPatrolEffectTargets` / `SetGuardPatrolEffectedBy`
(`src/game/card/face/card_type/minion.py`) : ce dernier marque les VILAINS de
la zone de jeu comme « affectés par » ce sbire, ce qui est l'indication visible
côté UI. L'interdiction elle-même est appliquée par
`Villain.CanBeAttackBy()` (`src/game/card/face/base/villain.py`), qui renvoie
`False` dès qu'un sbire engagé avec le joueur initiateur répond `IsGuard()`,
sauf si l'effet ignore le mot-clé (`effect.IsIgnoreKeyword('Guard', effect)`).
`Villain.GetGuardFaces()` renvoie la liste des sbires responsables du blocage.
`GainGuard` pose un `assert Minion.IsType(self)` : Guard est réservé aux
sbires. **Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01101` : Hydra Mercenary (`desc` contient `"Guard":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01101.py` trouvé dans `src/cards/pack` : cette carte n'a pas de capacité
imprimée distincte nécessitant un script.

**Pièges connus** :
- Guard bloque **uniquement l'attaque du vilain**. Les autres sbires restent
  attaquables, y compris le sbire Guard lui-même, qui est justement la façon
  normale de lever le blocage.
- Guard ne touche PAS le thwart : c'est Patrol qui interdit de contrecarrer le
  complot principal. Les deux passent par la même plomberie
  (`SetGuardPatrolEffectedBy`) mais ne bloquent pas la même chose ; ne pas
  confondre les deux fiches.
- La restriction est **par joueur** : un sbire Guard engagé avec un autre
  joueur ne vous empêche pas d'attaquer le vilain.
- Certains effets contournent le blocage via
  `effect.IsIgnoreKeyword('Guard', effect)` ; vérifier ce point avant de
  conclure à un bug de ciblage.
- Si une future carte cumule Guard avec une capacité imprimée annexe (par
  exemple une réaction au combat), vérifier via `find` si un script existe pour
  cette carte : le script devra porter uniquement cette capacité annexe, jamais
  le mot-clé Guard lui-même.

**Variantes maison** : aucune recensée pour l'instant.
