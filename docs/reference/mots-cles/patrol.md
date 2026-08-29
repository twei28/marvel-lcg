# Patrol

**Texte imprimé / définition** : « Patrol. *(While this minion is engaged with
you, you cannot thwart the main scheme.)* » Tant qu'un sbire Patrol est engagé
avec un joueur, CE joueur ne peut pas contrecarrer le complot principal. C'est
un compteur (`Patrol 1`, `Patrol 2`, ...), réinitialisé à sa valeur imprimée à
chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Patrol` sur la carte (réservée aux sbires,
`GainPatrol` pose un `assert Minion.IsType(self)`), lue nativement par le
moteur. `HasPatrol` (`src/game/card/face/attribute/has_patrol.py`) enregistre
l'attribut `Patrol` -> `printed_patrol` et restaure la valeur à chaque
`OnResetKeywords` via `GainPatrol`, qui appelle
`ClearGuardPatrolEffectTargets` / `SetGuardPatrolEffectedBy`
(`src/game/card/face/card_type/minion.py`) : ce dernier marque les COMPLOTS
PRINCIPAUX de la zone de jeu comme « affectés par » ce sbire, ce qui est
l'indication visible côté UI. L'interdiction elle-même est appliquée par
`MainScheme.CanBeThwartBy()`
(`src/game/card/face/card_type/scheme_main.py`) : si la carte visée est bien le
complot principal et que `MainScheme.GetPatrolFaces(effect)` n'est pas vide, la
méthode renvoie `False`, sauf si l'effet ignore le mot-clé
(`effect.IsIgnoreKeyword('Patrol', effect)`) ou si l'initiateur n'est pas un
joueur (`effect.IsPlayerInitiator()`). **Aucun script requis** pour ce mot-clé :
c'est une des « bases automatiques » du guide.

**Carte exemple** : `16119` : Badoon Lieutenant (`desc` contient `"Patrol":
"1"`), lu directement depuis `desc`, aucun script requis. Le script `16119.py`
existe et code la capacité de boost imprimée (« If this activation is a scheme,
this card gets +2 boost icons for this activation »), pas le mot-clé lui-même :
le moteur lit `Patrol` nativement dans `desc`, aucun module n'est nécessaire
pour lui.

**Pièges connus** :
- Patrol n'a **rien à voir avec les règles d'engagement**. Il ne rend pas le
  sbire engageable par n'importe quel joueur, il interdit un thwart.
- Seul le **complot principal** est bloqué : les complots annexes restent
  contrecarrables, et le sbire lui-même reste attaquable, ce qui est la façon
  normale de lever le blocage.
- La restriction est **par joueur** : un sbire Patrol engagé avec un autre
  joueur ne vous empêche pas de contrecarrer.
- Un effet dont l'initiateur n'est pas un joueur n'est pas bloqué, et certains
  effets contournent le blocage via `IsIgnoreKeyword('Patrol', ...)`.
- Patrol ne s'applique qu'aux sbires, jamais aux autres types de cartes.
- Patrol partage avec Guard la plomberie `SetGuardPatrolEffectedBy`, mais les
  deux ne bloquent pas la même chose (complot principal pour Patrol, vilain
  pour Guard) ; ne pas confondre les deux fiches.
- Si une future carte cumule Patrol avec une capacité imprimée distincte,
  vérifier via `find` si un script existe : le script devra porter uniquement
  cette capacité annexe, jamais le mot-clé Patrol lui-même.

**Variantes maison** : aucune recensée pour l'instant.
