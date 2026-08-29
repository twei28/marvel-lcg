# Villainous

**Texte imprimé / définition** : « Villainous. » Un minion avec ce mot-clé ignore les règles normales d'engagement et peut devenir un boost sans être engagé au préalable. Le compteur `Villainous` (`1`, `2`, ...) fixe le nombre de charges disponibles.

**Mécanisme moteur** : clé `desc.Villainous` sur la carte, lue nativement par le moteur. `HasVillainous` (`src/game/card/face/attribute/has_villainous.py`) enregistre l'attribut `Villainous` -> `printed_villainous`, restaure la valeur à chaque `OnResetKeywords` via `GainVillainous`, et hérite de `CanBoost` pour surcharger `GetBoostCardNum()` qui retourne 1 si le minion est Villainous. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `11041` : * Deathunt 9000 (`desc` contient `"Villainous": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `11041.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (entrée en jeu comme boost et attribution de Tough), pas le mot-clé Villainous.

**Pièges connus** : Villainous est un mot-clé de minion uniquement ; il n'affecte que le mécanisme d'engagement du minion concerné. Ne pas confondre avec d'autres mots-clés de vilain comme Retaliate ou Guard qui s'appliquent aussi aux minions mais portent sur les dégâts ou le ciblage. Si une future carte cumule Villainous avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Villainous lui-même.

**Variantes maison** : aucune recensée pour l'instant.
