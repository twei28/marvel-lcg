# Compteurs « corrupt », « scorned » et « damned » (scénario Mephisto, Neptune)

**Texte imprimé / définition** : compteurs nommés, sans règle propre. **corrupt** : posés sur les attachements BARGAIN de Corruptive Offers (« place 1 corrupt counter here → … ») ; quand l'attachement est défaussé (ou que Soul Gambling est révélée), X<par joueur> cartes du dessus du deck sont mises de côté, X = nombre de corrupt counters. **scorned** : posés sur le side scheme Culling the Damned (« After a MYSTIC minion is defeated, place one scorned counter here ») ; à la défaite, le joueur regarde X cartes en Damnation. **damned** : posés sur Demon Amalgam (modulaire Damned, mp121) à sa révélation (X = nombre de sbires MYSTIC dans la défausse de rencontre) ; il a +1 point de vie par compteur.

**Mécanisme moteur** : `'corrupt'`, `'scorned'` et `'damned'` ajoutés à `CardFace.COUNTER` (`card_face.py`, 09/11/2026), comme `chi` ou `corruption`. Poser : `Faces.PlaceCountersOn(...)`, dépenser en coût : `CostFunc.Counter(...)` (modèle : `chi-counter.md`). Traduction française (`compteurs-fr.ts`, testée dans `compteurs-fr.test.ts`) : corrupt = corruption, scorned = mépris, damned = damnation.

**Cartes exemples** : mp111-mp114 et mp115/116 (corrupt), mp017 (scorned), mp121 (damned) ; cas dans `tools/test_capacites.py`.

**Pièges connus** : sans l'entrée dans `COUNTER`, `IsCounter` refuse le nom (constaté sur d'autres packs).

**Variantes maison** : compteurs maison.
