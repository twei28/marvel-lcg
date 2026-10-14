# Retaliate

**Texte imprimé / définition** : « Retaliate 1. *(After this character is
attacked, deal 1 damage to the attacking character.)* » Après qu'un personnage
Retaliate a été attaqué, l'attaquant subit un nombre de dégâts égal à la valeur
de Retaliate. C'est un compteur (`Retaliate 1`, `Retaliate 2`, ...),
réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Retaliate` sur la carte, lue nativement
par le moteur. `HasRetaliate`
(`src/game/card/face/attribute/can_retaliate.py`) enregistre l'attribut
`Retaliate` -> `printed_retaliate`, restaure la valeur à chaque
`OnResetKeywords` via `GainRetaliate`, et fournit
`ResolveRetaliate(atk_message)` qui applique les dégâts en retour en
s'appuyant sur la classe `Retaliate(GameRule)` de
`src/game/effect/rule.py` comme justification de l'effet. Trois conditions y
sont vérifiées avant le `attacker.TakeDamage(...)` : l'attaquant existe et
n'est pas vaincu, l'attaque n'est pas à distance (`atk_message.IsRanged()`) et
le défenseur n'est pas vaincu, et l'attaque n'ignore pas le mot-clé
(`atk_message.IsIgnoreRetaliate()`). Sinon un `Message.AfterIgnoreKeywordOnCard`
est émis à la place. L'appel vient de `can_attack.py` et de
`src/game/effect/effect_invoke.py`. **Aucun script requis** pour ce mot-clé.

**Carte exemple** : `01040a` : * Black Panther (`desc` contient
`"Retaliate": "1"`), lu directement depuis `desc`, aucun script requis.
Aucun fichier `01040a.py` trouvé dans `src/cards/pack` : cette face de
carte n'a pas de capacité imprimée distincte nécessitant un script.

**Pièges connus** : trois cas où Retaliate ne se déclenche pas, tous lisibles
dans `ResolveRetaliate` : attaque **à distance** (`IsRanged()`), défenseur ou
attaquant **déjà vaincu** au moment de la résolution, et attaque qui **ignore
Retaliate** (`IsIgnoreRetaliate()`). Aucun rapport en revanche avec Quickstrike :
ce mot-clé n'est pas une règle d'ordre de résolution des dégâts, c'est une
attaque déclenchée quand un sbire s'engage avec un héros (voir sa fiche), et il
n'a aucune interaction particulière avec Retaliate. Si une future carte
cumule Retaliate avec une capacité imprimée annexe (déclencheur sur les
dégâts infligés, par exemple), vérifier via `find` si un script existe
pour cette carte : le script devra porter uniquement cette capacité
annexe, jamais le mot-clé Retaliate lui-même. La carte `03009` (Captain
America's Shield) illustre ce piège concret ailleurs dans le catalogue :
elle a un script (`AbilityFactory.GiveKeywordToAttached`), mais ce script
code sa capacité d'ATTACHEMENT (donner Defense 1 et Retaliate 1 à
Captain America), pas le mot-clé Retaliate en tant que tel.

**Variantes maison** : aucune recensée pour l'instant.


**Rules Reference 1.8 (22/07/2026)** : Retaliate devient « Forced Response : After this character is attacked, deal X damage to the attacker », résolu avec les autres réponses forcées « after attacks / after is attacked », dans l'ordre choisi (le bullet 1.7 « 1. after takes damage 2. Retaliate X 3. after attacked » est supprimé). Moteur : règle `v18_retaliate` (posée par `v18_all`). Sous cette règle, `EventManager.RegisterPlayRule` pose UNE réponse forcée de règle pour toute la partie (`CanRetaliate.AbiliteRiposte()`, sur `AfterUnitAttackUnit`, pour toute cible attaquée qui a Retaliate), et les deux appels directs (`can_attack.py`, `effect_invoke.py`) sont sautés ; « attaquant vaincu » se relit sur l'état du monde après la fenêtre. Pas une capacité par carte : un premier essai l'ajoutait dans `CardFactory.CreateFace` et cassait les faces créées sans carte (`TreatAsMinion` : mw026 Veranke, av014, av015, sw023). Sans la règle (sauvegardes d'avant), rien n'est ajouté : les identifiants d'effets, donc le rejeu, restent identiques. Cas : `[RR1.8] wx009 riposte` (Radioactive Man à 1 PV : sa réponse forcée fait défausser avant la riposte, et le témoin 1.7).
