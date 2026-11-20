# Dupe (nom d'allié MAISON, Multiple Man / R. Tim Morris)

**Texte imprimé / définition** : « a Dupe ally » (17 textes du pack) = un ALLIÉ nommé « Dupe » (sous-titre « Jamie Madrox »), au nombre de 4 (mm002 à mm005). Les quatre sont des cartes DISTINCTES de même nom, avec une ressource imprimée différente (physique, mentale, énergie, polyvalente). « A different Dupe ally » (He's Got This) = une autre carte que celle qui vient d'être défaussée.

**Mécanisme moteur** : aucun attribut. Helpers du pack (`src/cards/pack/multiple_man/multiple_man_commun.py`) : `EstDupe(face)` (allié de nom « Dupe »), `DupesDuJoueur`, `DupesEnJeu`, `ChercherEtMettreUnDupe` (recherche deck + main + défausse, mise en jeu, option `epuise=True`, `different_de=`). Filtres de fabrique : `CardFinder(name="Dupe", card_type=Ally)`, `CardFinder(non_name="Dupe")` pour « seul un Dupe peut… ».

**Carte exemple** : `mm006` Someone's Got This (compte les Dupe en jeu), `mm012` Madrox Prime (`ThreatCannotBeRemovedFromWhile(by_character=CardFinder(non_name="Dupe"))`).

**Pièges connus** : « Only a Dupe ally can remove threat from this scheme » : DÉCISION UTILISATEUR (04/11) : aucune autre source ne le peut, événements du héros et Reabsorb Dupe compris (leur `by_face` n'est pas un Dupe). Le nom « Multiple Man » est aussi celui d'un allié officiel (14012, non unique) : sans conflit d'unicité.

**Variantes maison** : nom d'allié maison ; voir `duplicate.md` pour le trait.
