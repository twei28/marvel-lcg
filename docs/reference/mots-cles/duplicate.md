# Duplicate (trait MAISON, Multiple Man / R. Tim Morris)

**Texte imprimé / définition** : « DUPLICATE. » (ligne de traits) sur les 4 alliés Dupe, les trois événements de combat de Multiple Man (Someone's Got This, We've Got This, He's Got This), Dupes Gone Bad ×3 et Emperor Madrox. Aucune carte du pack ne le lit dans son texte.

**Mécanisme moteur** : un TRAIT sans effet propre (RRG 1.8 « Traits » : un trait n'a aucun effet en soi). Il est dans `cards.json` (`traits: ["DUPLICATE", ...]`) et a été ajouté à `CardFace.TRAITS` (`src/game/card/face/card_face.py`, ajout du 04/11/2026) : sans cela `HasTrait("DUPLICATE")` ne trouve rien. Aucun script ne l'utilise.

**Carte exemple** : `mm002` Dupe (traits `DUPLICATE`, `X-FACTOR`), lu directement depuis `desc`/`traits`.

**Pièges connus** : « Duplicate » n'est PAS « Dupe » : « a Dupe ally » désigne un allié dont le NOM est Dupe (voir `dupe.md`). Aucune carte officielle du dépôt ne porte « Duplicate ».

**Variantes maison** : c'est lui-même un trait maison.
