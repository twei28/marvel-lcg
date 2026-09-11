# Éclair (ressource maison, `L`)

**Texte imprimé / définition** : le pack fan-made Zeus (Mozilla) imprime sur
ses quatre Thunder Strike une icône de ressource qui n'existe pas dans le jeu
officiel, un éclair droit. Ce n'est PAS l'énergie : Zeus exige de payer un
même événement « avec une énergie ET un éclair » (*Skyfather's Tempest*).
Vocabulaire fixé le 11/09/2026 : **énergie** = la ressource officielle jaune ;
**éclair** = celle-ci.

**Mécanisme moteur** : cinquième couleur à part entière, lettre `L`, ajoutée
le 11/09/2026 (`src/game/element/rbyg.py`, champ `l`). Elle se déclare comme
les autres : `"RES": "L"` dans `desc`, `Cost("YL")` pour un coût typé, jeton
`[[lightning]]` dans les narrations, `GetColor("L")` pour la compter.
- Un joker (`G`) vaut aussi un éclair (défaut `convert_green_res=True`).
- Un éclair paie tout coût générique, et ne paie PAS un coût typé d'une autre
  couleur : « Requirement (énergie) » le refuse.
- Plateau : `ui-app/src/board/icones-ressources.tsx`, entrée `lightning`,
  rendue en SVG bleu électrique. Deckbuilder : classe `icon-lightning`.
- Gate : `ui-app/src/board/noms-ressources.test.ts` relit la table du moteur
  et celle du plateau et exige les cinq lettres des deux côtés.
- Test : `tools/test_couleur_eclair.py` (26 cas, sans partie ni port).

**Carte exemple** : aucune livrée à ce jour ; le pack Zeus suivra
`PROCESSUS-HEROS.md`. Le relevé complet est dans
`.planning/todos/2026-09-11-zeus-releve-des-cartes.md`. Spec et plan dans
`docs/superpowers/specs/2026-09-11-cinquieme-couleur-de-ressource-design.md`
et `docs/superpowers/plans/2026-09-11-cinquieme-couleur-de-ressource.md`.

**Pièges connus** :
- **Ne pas lire l'éclair comme une énergie.** La première version du relevé
  Zeus l'a fait sur toutes les cartes ; le set némésis, lui, vise bien
  l'ÉNERGIE officielle, pas l'éclair.
- `DeclareResourceType()` propose désormais `L` à toute carte qui fait nommer
  un type (Psylocke, Iron Lad, Mojo). C'est la règle : un type existe pour
  tout le monde. Passer `l=False` si une carte doit s'en tenir aux quatre
  officiels.
- Les jetons à un crochet `[energy]` des textes français ne sont pas rendus
  en icône aujourd'hui (ils s'affichent tels quels dans l'aperçu) ;
  `[lightning]` suivra le même sort. Hors périmètre de la couleur.

**Variantes maison** : c'est la variante. Aucune autre ressource maison dans
le projet.
