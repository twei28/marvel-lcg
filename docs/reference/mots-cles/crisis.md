# Crisis

**Texte imprimé / définition** : « Crisis. » Un schéma annexe avec ce mot-clé force une réponse immédiate du joueur : il doit être vaincu avant que le threat puisse être retiré du schéma principal. Le compteur `Crisis` (`1`, `2`, ...) fixe le nombre de charges de crise.

**Mécanisme moteur** : clé `desc.Crisis` sur la carte, lue nativement par le moteur. `CanCrisis` (`src/game/card/face/attribute/has_crisis.py`) enregistre l'attribut `Crisis` -> `printed_crisis`, restaure la valeur à chaque `OnResetKeywords` via `GainCrisis`. Quand un schéma Crisis entre en jeu, `SetCrisisEffectedBy()` marque le schéma principal comme étant affecté par le crisis, ce qui empêche l'accrual de thwart via l'interface de contrôle de menace (UI). **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01108` : Crowd Control (`desc` contient `"Crisis": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `01108.py` trouvé dans `src/cards/pack` : cette carte ne porte que le mot-clé Crisis, sans capacité imprimée annexe.

**Pièges connus** : Crisis affecte le schéma principal via l'UI (blocage thwart), pas via une règle de perte de PV ou une incapacité légale de thwart ; le moteur refuse juste le clic thwart jusqu'au crisis résolu. Ne pas confondre avec Peril qui agit de manière similaire mais force une résolution immédiate. Si une future carte cumule Crisis avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Crisis lui-même.

**Variantes maison** : aucune recensée pour l'instant.
